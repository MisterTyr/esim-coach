#!/usr/bin/env python3
import os, csv, io, json, hashlib, requests, pathlib
from datetime import datetime, timezone
from dateutil import parser as dateparser

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "data" / "outputs"
SITE_DIR = ROOT / "site"
CONFIG = json.loads((DATA_DIR / "sources" / "config.json").read_text())

def env_or_default(key, default=None):
    v = os.getenv(key)
    return v if v is not None else default

def fetch_csv_url(url):
    r = requests.get(url, timeout=30); r.raise_for_status()
    return list(csv.DictReader(io.StringIO(r.text)))

def fetch_csv_local(path):
    p = (ROOT / path).resolve()
    with open(p, newline="") as f:
        return list(csv.DictReader(f))

def to_float(x):
    try: return float(str(x).strip())
    except: return None

def normalize_row(row):
    provider = str(row.get("provider","")).strip()
    plan_name = str(row.get("plan_name","")).strip()
    region = str(row.get("region","")).strip() or "Global"
    country = str(row.get("country","")).strip() or "Multi"
    data_raw = str(row.get("data_gb","")).strip().lower()
    if data_raw in ("unlimited","∞","inf"):
        data_gb = None; unlimited = True
    else:
        data_gb = to_float(data_raw); unlimited = False
    validity_days = int(to_float(row.get("validity_days","")) or 0)
    price_usd = to_float(row.get("price_usd",""))
    url = str(row.get("product_url","")).strip()
    if url and "?" in url:
        url += f"&utm_source={CONFIG['affiliate']['utm_source']}&utm_medium={CONFIG['affiliate']['utm_medium']}&utm_campaign={CONFIG['affiliate']['utm_campaign']}"
    ts_raw = row.get("timestamp") or datetime.now(timezone.utc).isoformat()
    try: ts = dateparser.parse(ts_raw).astimezone(timezone.utc).isoformat()
    except: ts = datetime.now(timezone.utc).isoformat()
    price_per_gb = None
    if not unlimited and (data_gb and data_gb > 0) and price_usd:
        price_per_gb = round(price_usd / data_gb, 4)
    price_per_day = round(price_usd / validity_days, 4) if price_usd and validity_days>0 else None
    plan = {
        "provider": provider, "plan_name": plan_name, "region": region, "country": country,
        "data_gb": data_gb if not unlimited else "unlimited", "validity_days": validity_days,
        "price_usd": round(price_usd,2) if price_usd is not None else None,
        "product_url": url, "timestamp": ts,
        "metrics": {"price_per_gb": price_per_gb, "price_per_day": price_per_day, "unlimited": unlimited}
    }
    plan["id"] = hashlib.md5(f"{provider}|{plan_name}|{region}|{country}|{price_usd}|{validity_days}".encode()).hexdigest()[:10]
    return plan

def load_all():
    rows = []
    for s in CONFIG["sources"]:
        if not s.get("enabled", False): continue
        if s["type"] == "csv": rows.extend(fetch_csv_url(s["url"]))
        elif s["type"] == "csv_local": rows.extend(fetch_csv_local(s["path"]))
    return [normalize_row(r) for r in rows]

def score_value(p):
    m = p["metrics"]
    if m["unlimited"]:
        ppd = m["price_per_day"] if m["price_per_day"] is not None else 9999
        return (ppd, -p["validity_days"])
    else:
        ppg = m["price_per_gb"] if m["price_per_gb"] is not None else 9999
        return (ppg, -p["validity_days"])

def rank_plans(plans):
    strat = CONFIG["ranking"].get("strategy","value")
    if strat == "cheapest":
        plans.sort(key=lambda p: (p.get("price_usd") if p.get("price_usd") is not None else 9999))
    elif strat == "longest_validity":
        plans.sort(key=lambda p: (-p.get("validity_days",0), p.get("price_usd") if p.get("price_usd") is not None else 9999))
    else:
        plans.sort(key=lambda p: score_value(p))
    limit = CONFIG["ranking"].get("per_provider_limit",5)
    seen = {}; ranked = []
    for p in plans:
        prov = p["provider"]; seen.setdefault(prov,0)
        if seen[prov] >= limit: continue
        seen[prov] += 1; ranked.append(p)
    top_n = CONFIG["ranking"].get("daily_top_n",60)
    ranked = ranked[:top_n]
    for i,p in enumerate(ranked, start=1): p["rank"]=i
    return ranked

def write_outputs(plans):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR/"plans.json").write_text(json.dumps(plans, indent=2))
    (SITE_DIR/"plans.json").write_text(json.dumps(plans, indent=2))

def write_sitemap(base_url):
    now = datetime.utcnow().strftime("%Y-%m-%d")
    pages = ["/","/what-is-esim.html","/how-to-install-esim.html","/why-esim.html"]
    urls = [f"<url><loc>{base_url}{p}</loc><lastmod>{now}</lastmod></url>" for p in pages]
    xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">" + "".join(urls) + "</urlset>"
    (SITE_DIR/"sitemap.xml").write_text(xml)

def main():
    base_url = env_or_default(CONFIG["site"]["base_url_env"], "https://example.com")
    plans = [p for p in load_all() if p.get("price_usd") is not None]
    ranked = rank_plans(plans)
    write_outputs(ranked); write_sitemap(base_url)
    print(f"Wrote {len(ranked)} ranked plans.")

if __name__ == "__main__":
    main()
