#!/usr/bin/env python3
import json, pathlib, html
ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DATA = SITE / "plans.json"
CFG = json.loads((ROOT / "data" / "sources" / "config.json").read_text())

def render_card(p):
    data_disp = (f"{p.get('data_gb')}GB" if isinstance(p.get('data_gb'), (int,float)) else "Unlimited")
    price = p.get("price_usd")
    return f"""
    <article class='card' data-region='{html.escape(p.get("region",""))}' data-provider='{html.escape(p.get("provider",""))}'>
      <div class='badge'>#{p.get("rank","")}</div>
      <h3>{html.escape(p.get("provider",""))} <small>{html.escape(p.get("plan_name",""))}</small></h3>
      <p class='meta'>{html.escape(p.get("region",""))} • {html.escape(p.get("country",""))}</p>
      <p class='meta'>{data_disp} • {p.get("validity_days","")} days</p>
      <p class='price'>${price}</p>
      <a class='cta' href='{html.escape(p.get("product_url",""))}' target='_blank' rel='nofollow sponsored'>Get Plan</a>
    </article>
    """

def render_filters():
    btns = ["<button data-filter='all' class='active'>All</button>"]
    btns += [f"<button data-filter='{html.escape(r)}'>{html.escape(r)}</button>" for r in CFG["site"]["regions"]]
    return "\n".join(btns)

def main():
    if not DATA.exists():
        (SITE / "plans.json").write_text("[]")
    plans = json.loads(DATA.read_text())
    html_doc = f"""<!doctype html>
<html lang='en'><head>
<meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>eSIMRanker — Best Value eSIM Plans</title>
<meta name='description' content='Automatically ranked eSIM plans by value ($/GB or $/day), refreshed daily.'>
<link rel='stylesheet' href='assets/styles.css'>
</head><body>
<header class='hero'>
  <h1>eSIMRanker</h1>
  <p class='tag'>Autonomous, always‑fresh eSIM deals</p>
  <nav class='filters'>{render_filters()}</nav>
  <nav class='evergreen'>
    <a href='what-is-esim.html'>What is an eSIM?</a>
    <a href='how-to-install-esim.html'>How to install</a>
    <a href='why-esim.html'>Why you need one</a>
  </nav>
</header>
<main id='grid'>
  {"".join(render_card(p) for p in plans)}
</main>
<footer class='ft'>
  <p>Affiliate disclosure: we may earn a commission. Updated daily.</p>
  <script src='assets/app.js'></script>
</footer>
</body></html>
"""
    (SITE / "index.html").write_text(html_doc)

if __name__ == "__main__":
    main()
