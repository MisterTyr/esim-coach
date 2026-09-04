#!/usr/bin/env python3
"""eSIM Sorted — refresh plan data.

Reads enabled sources from data/config.json, normalizes rows, computes value
metrics (per GB, per day), ranks by the configured strategy, and writes
plans.json plus sitemap.xml to the project root. No database, no build server.

Before it writes anything it runs a set of checks on the data. If the data
looks wrong the run stops and the published files are left alone, so a bad
spreadsheet edit cannot go live unattended.

Run:  python3 scripts/update_plans.py
"""
import sys
import os, csv, io, json, hashlib, pathlib
from datetime import datetime, timezone, timedelta

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


def clean(x):
    return str(x if x is not None else "").strip()


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
    provider = clean(row.get("provider"))
    plan_name = clean(row.get("plan_name"))
    region = clean(row.get("region")) or "Global"
    country = clean(row.get("country")) or "Multi"

    data_raw = clean(row.get("data_gb")).lower()
    if data_raw in ("unlimited", "inf", "∞"):
        data_gb, unlimited = None, True
    else:
        data_gb, unlimited = to_float(data_raw), False

    validity_days = int(to_float(row.get("validity_days", "")) or 0)
    price = to_float(row.get("price", row.get("price_usd", "")))

    # An "unlimited" plan with a full-speed allowance is not the same product as
    # one without. full_speed_gb is the amount you get before the provider slows
    # you down; blank means genuinely uncapped.
    full_speed_gb = to_float(row.get("full_speed_gb", ""))
    # Most providers cap per DAY (Airalo 3GB/day, Saily 5GB/day). Ubigi caps
    # per PLAN (25GB over 7 days). Same column, completely different product,
    # so the period has to be recorded or the maths is wrong by a factor of
    # however many days the plan lasts.
    full_speed_period = clean(row.get("full_speed_period")).lower() or "per_plan"
    post_cap_speed = clean(row.get("post_cap_speed"))

    direction = clean(row.get("direction")).lower() or "outbound"
    voice_type = clean(row.get("voice_type")).lower()
    calls_included = clean(row.get("calls_included"))
    sms_included = clean(row.get("sms_included"))
    number_country = clean(row.get("number_country")).upper()
    hotspot = clean(row.get("hotspot")).lower()
    source_url = clean(row.get("source_url"))

    url = clean(row.get("product_url"))
    if url:
        sep = "&" if "?" in url else "?"
        url += f"{sep}utm_source={aff['utm_source']}&utm_medium={aff['utm_medium']}&utm_campaign={aff['utm_campaign']}"

    # Whatever a buyer actually gets at full speed. For a capped "unlimited"
    # plan that is the full-speed allowance, which makes it comparable to an
    # ordinary sized plan instead of being ranked on price per day alone.
    if unlimited and full_speed_gb:
        if full_speed_period == "per_day" and validity_days > 0:
            billable_gb = full_speed_gb * validity_days
        else:
            billable_gb = full_speed_gb
    elif unlimited:
        billable_gb = None
    else:
        billable_gb = data_gb

    price_per_gb = round(price / billable_gb, 4) if (billable_gb and price) else None
    price_per_day = round(price / validity_days, 4) if (price and validity_days > 0) else None

    plan = {
        "provider": provider,
        "plan_name": plan_name,
        "region": region,
        "country": country,
        "direction": direction,
        "data_gb": "unlimited" if unlimited else data_gb,
        "validity_days": validity_days,
        "price": round(price, 2) if price is not None else None,
        "product_url": url,
        "source_url": source_url,
        "voice_type": voice_type,
        "calls_included": calls_included,
        "sms_included": sms_included,
        "number_country": number_country,
        "hotspot": hotspot,
        "post_cap_speed": post_cap_speed,
        "full_speed_period": full_speed_period,
        "timestamp": parse_ts(row.get("timestamp")),
        "metrics": {
            "price_per_gb": price_per_gb,
            "price_per_day": price_per_day,
            "unlimited": unlimited,
            "full_speed_gb": full_speed_gb,
            "full_speed_total_gb": billable_gb if (unlimited and full_speed_gb) else None,
            "capped_unlimited": bool(unlimited and full_speed_gb),
            "uncapped": bool(unlimited and not full_speed_gb),
        },
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
    sample rather than being merged with it.

    Returns (plans, used_fallback). The caller needs to know which, because
    quietly publishing the sample file is the failure this pipeline is most
    likely to make."""
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

    used_fallback = not primary and bool(fallback)
    chosen = primary if primary else fallback
    if used_fallback:
        print("- using fallback source(s); no primary rows loaded")
    return [normalize_row(r) for _, r in chosen], used_fallback


def score_value(p):
    """One ranking, three tiers.

    Tier 0 is everything with a real amount of full-speed data, ranked on price
    per GB. A capped "unlimited" plan belongs here, priced on its full-speed
    allowance rather than on price per day.

    Tier 1 is genuinely uncapped plans. There is no honest way to compare them
    on price per GB without inventing a usage figure, so they sit below the
    sized plans, ordered by price per day.

    Tier 2 is anything too incomplete to rank."""
    m = p["metrics"]
    ppg = m.get("price_per_gb")
    ppd = m.get("price_per_day")
    if ppg is not None:
        return (0, ppg, -p["validity_days"])
    if m.get("uncapped") and ppd is not None:
        return (1, ppd, -p["validity_days"])
    return (2, 9999, 0)


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


def run_checks(plans, used_fallback, previous_count):
    """Sanity checks on the data before anything is written.

    Returns (stoppers, warnings). Anything in stoppers means the run does not
    publish. The point is that the daily job runs unattended, so a spreadsheet
    someone half-edited should fail loudly rather than go live overnight."""
    c = CONFIG.get("checks", {})
    stop, warn = [], []

    if c.get("require_live_source", True) and used_fallback and os.getenv("ALLOW_SAMPLE_DATA") != "1":
        stop.append(
            "The live source returned no rows, so this run would publish the local "
            "sample file instead. Check the Sheet is still published to the web. "
            "Set ALLOW_SAMPLE_DATA=1 if you really do want the sample."
        )

    min_rows = c.get("min_rows", 1)
    if len(plans) < min_rows:
        stop.append(f"Only {len(plans)} usable rows, expected at least {min_rows}.")

    drop_pct = c.get("max_row_drop_pct")
    if drop_pct and previous_count and len(plans) < previous_count:
        lost = (previous_count - len(plans)) / previous_count * 100
        if lost > drop_pct:
            stop.append(
                f"Row count fell from {previous_count} to {len(plans)}, a drop of "
                f"{lost:.0f}%. Anything over {drop_pct}% stops the run in case rows "
                "were deleted by accident."
            )

    max_price = c.get("max_price", 1000)
    for p in plans:
        label = f"{p.get('provider','?')} / {p.get('plan_name','?')}"
        price = p.get("price")
        if price is None or price <= 0:
            stop.append(f"{label}: price is missing or zero.")
        elif price > max_price:
            stop.append(f"{label}: price is {price}, above the {max_price} sanity limit.")
        if not p.get("provider") or not p.get("plan_name"):
            stop.append(f"Row with price {price} has no provider or plan name.")
        if p.get("validity_days", 0) <= 0:
            stop.append(f"{label}: validity_days is missing or zero.")
        if p["metrics"]["unlimited"] and not p["metrics"]["full_speed_gb"]:
            warn.append(
                f"{label}: unlimited with no full_speed_gb, so it is being treated as "
                "genuinely uncapped and ranks below the sized plans. If the provider "
                "does throttle and simply will not say by how much, that is worth "
                "saying on the card rather than implying no limit."
            )
        if "YOUR_AFFILIATE_ID" in (p.get("product_url") or ""):
            warn.append(f"{label}: product_url is still a placeholder affiliate link.")

    stale_days = c.get("max_stale_days")
    stamps = [p.get("timestamp") for p in plans if p.get("timestamp")]
    if stale_days and stamps:
        try:
            newest = max(datetime.fromisoformat(s) for s in stamps)
            age = (datetime.now(timezone.utc) - newest).days
            if age > stale_days:
                stop.append(
                    f"The newest price was checked {age} days ago. Nothing has been "
                    f"updated in over {stale_days} days, so the site would be "
                    "publishing prices nobody has verified."
                )
        except ValueError:
            warn.append("Could not read the timestamps, so the staleness check was skipped.")

    return stop, warn


def write_sitemap(base_url):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    # Derived from content.PAGES so a page cannot ship unlisted.
    sys.path.insert(0, str(ROOT / "scripts"))
    from content import PAGES
    pages = ["/"] + ["/" + name for name in PAGES]
    urls = "".join(
        f"<url><loc>{base_url}{p}</loc><lastmod>{now}</lastmod></url>" for p in pages
    )
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>\n")
    (ROOT / "sitemap.xml").write_text(xml)


def main():
    base_url = os.getenv("SITE_BASE_URL", CONFIG["site"]["base_url"]).rstrip("/")
    loaded, used_fallback = load_all()
    plans = [p for p in loaded if p.get("price") is not None]

    plans_path = ROOT / "plans.json"
    try:
        previous_count = len(json.loads(plans_path.read_text())) if plans_path.exists() else 0
    except Exception:
        previous_count = 0

    stop, warn = run_checks(plans, used_fallback, previous_count)
    for w in warn:
        print(f"! {w}")
    if stop:
        print("\nStopped. Nothing was published. Problems found:")
        for s in stop:
            print(f"  - {s}")
        print("\nplans.json and sitemap.xml were left exactly as they were.")
        return 1

    ranked = rank_plans(plans)
    plans_path.write_text(json.dumps(ranked, indent=2))
    write_sitemap(base_url)
    print(f"Wrote {len(ranked)} ranked plans to plans.json and sitemap.xml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
