#!/usr/bin/env python3
"""eSIM Coach — refresh plan data.

Reads enabled sources from data/config.json, normalizes rows, computes value
metrics ($/GB, $/day), ranks by the configured strategy, and writes plans.json
plus sitemap.xml to the project root. No database, no build server.

Run:  python3 scripts/update_plans.py
"""
import os, csv, io, json, hashlib, pathlib
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    requests = None
try:
    from dateutil import parser as dateparser
except ImportError:
    dateparser = None

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "data" / "config.json").read_text())


def to_float(x):
    try:
        return float(str(x).strip())
    except Exception:
        return None


def fetch_csv_url(url):
    if requests is None:
        raise RuntimeError("requests not installed; run pip install -r scripts/requirements.txt")
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return list(csv.DictReader(io.StringIO(r.text)))


def fetch_csv_local(path):
    with open((ROOT / path).resolve(), newline="") as f:
        return list(csv.DictReader(f))


def parse_ts(raw):
    raw = raw or datetime.now(timezone.utc).isoformat()
    try:
        if dateparser:
            return dateparser.parse(raw).astimezone(timezone.utc).isoformat()
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(timezone.utc).isoformat()
    except Exception:
        return datetime.now(timezone.utc).isoformat()


def normalize_row(row):
    aff = CONFIG["affiliate"]
    provider = str(row.get("provider", "")).strip()
    plan_name = str(row.get("plan_name", "")).strip()
    region = str(row.get("region", "")).strip() or "Global"
    country = str(row.get("country", "")).strip() or "Multi"

    data_raw = str(row.get("data_gb", "")).strip().lower()
    if data_raw in ("unlimited", "inf", "∞"):
        data_gb, unlimited = None, True
    else:
        data_gb, unlimited = to_float(data_raw), False

    validity_days = int(to_float(row.get("validity_days", "")) or 0)
    price = to_float(row.get("price", row.get("price_usd", "")))

    url = str(row.get("product_url", "")).strip()
    if url:
        sep = "&" if "?" in url else "?"
        url += f"{sep}utm_source={aff['utm_source']}&utm_medium={aff['utm_medium']}&utm_campaign={aff['utm_campaign']}"

    price_per_gb = round(price / data_gb, 4) if (not unlimited and data_gb and price) else None
    price_per_day = round(price / validity_days, 4) if (price and validity_days > 0) else None

    plan = {
        "provider": provider,
        "plan_name": plan_name,
        "region": region,
        "country": country,
        "data_gb": "unlimited" if unlimited else data_gb,
        "validity_days": validity_days,
        "price": round(price, 2) if price is not None else None,
        "product_url": url,
        "timestamp": parse_ts(row.get("timestamp")),
        "metrics": {"price_per_gb": price_per_gb, "price_per_day": price_per_day, "unlimited": unlimited},
    }
    plan["id"] = hashlib.md5(
        f"{provider}|{plan_name}|{region}|{country}|{price}|{validity_days}".encode()
    ).hexdigest()[:10]
    return plan


def resolve_url(s):
    """A csv source's URL comes from its env var if set, else its literal url."""
    url = os.getenv(s["url_env"], "").strip() if s.get("url_env") else ""
    return url or s.get("url", "")


def read_source(s):
    if s["type"] == "csv":
        url = resolve_url(s)
        if not url or "YOUR_SHEET_ID" in url:
            print(f"- skipping '{s.get('name')}': no URL set "
                  f"(set env {s.get('url_env','SHEET_CSV_URL')} to your published-Sheet CSV link)")
            return []
        return fetch_csv_url(url)
    if s["type"] == "csv_local":
        return fetch_csv_local(s["path"])
    return []


def load_all():
    """Primary sources first. Sources marked "fallback": true are used only if
    the primary sources returned no rows, so a live Sheet replaces the local
    sample rather than being merged with it."""
    primary, fallback = [], []
    for s in CONFIG["sources"]:
        if not s.get("enabled"):
            continue
        try:
            got = read_source(s)
            (fallback if s.get("fallback") else primary).extend(
                [(s.get("name"), r) for r in got]
            )
            if got:
                print(f"- {s.get('name')}: {len(got)} rows")
        except Exception as e:
            print(f"! source '{s.get('name')}' failed: {e}")

    chosen = primary if primary else fallback
    if not primary and fallback:
        print("- using fallback source(s); no primary rows loaded")
    return [normalize_row(r) for _, r in chosen]


def score_value(p):
    m = p["metrics"]
    key = m["price_per_day"] if m["unlimited"] else m["price_per_gb"]
    return (key if key is not None else 9999, -p["validity_days"])


def rank_plans(plans):
    rk = CONFIG["ranking"]
    strat = rk.get("strategy", "value")
    if strat == "cheapest":
        plans.sort(key=lambda p: p.get("price") if p.get("price") is not None else 9999)
    elif strat == "longest_validity":
        plans.sort(key=lambda p: (-p.get("validity_days", 0), p.get("price") or 9999))
    else:
        plans.sort(key=score_value)

    # Record where each plan lands on value alone, before any paid placement
    # is applied. The Top pick badge is awarded from this, so it cannot be bought.
    for i, p in enumerate(plans, 1):
        p["value_rank"] = i

    # Paid placement: pinned providers float to the top, keeping their own value
    # order. Flagged separately from merit so the UI can label it as placement.
    pinned = [x.lower() for x in rk.get("pin_providers", [])]
    if pinned:
        for p in plans:
            p["placement"] = p["provider"].lower() in pinned
        plans.sort(key=lambda p: (0 if p["provider"].lower() in pinned else 1))

    limit = rk.get("per_provider_limit", 5)
    seen, ranked = {}, []
    for p in plans:
        prov = p["provider"]
        if seen.get(prov, 0) >= limit:
            continue
        seen[prov] = seen.get(prov, 0) + 1
        ranked.append(p)

    ranked = ranked[: rk.get("daily_top_n", 60)]
    for i, p in enumerate(ranked, 1):
        p["rank"] = i
    # Top pick goes to the best plan on value alone, paid placement or not.
    if ranked:
        min(ranked, key=lambda p: p.get("value_rank", 9999))["top_pick"] = True
    return ranked


def write_sitemap(base_url):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    pages = ["/", "/what-is-esim.html", "/how-to-install-esim.html", "/why-esim.html",
             "/about.html", "/privacy-policy.html", "/terms.html", "/affiliate-disclosure.html"]
    urls = "".join(
        f"<url><loc>{base_url}{p}</loc><lastmod>{now}</lastmod></url>" for p in pages
    )
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>\n")
    (ROOT / "sitemap.xml").write_text(xml)


def main():
    base_url = os.getenv("SITE_BASE_URL", CONFIG["site"]["base_url"]).rstrip("/")
    plans = [p for p in load_all() if p.get("price") is not None]
    ranked = rank_plans(plans)
    (ROOT / "plans.json").write_text(json.dumps(ranked, indent=2))
    write_sitemap(base_url)
    print(f"Wrote {len(ranked)} ranked plans to plans.json and sitemap.xml")


if __name__ == "__main__":
    main()
