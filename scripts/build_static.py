#!/usr/bin/env python3
"""eSIM Coach — build the static site.

Renders index.html from plans.json + config, and renders every evergreen /
legal page defined in content.py. All pages share one header, footer and
stylesheet, so the site stays consistent with almost no hand-written HTML.

Run:  python3 scripts/build_static.py   (run update_plans.py first)
"""
import json, pathlib, html
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "data" / "config.json").read_text())
SITE = CFG["site"]
CUR = CFG.get("currency_symbol", "$")

import sys
sys.path.insert(0, str(ROOT / "scripts"))
from content import PAGES  # noqa: E402

NAV = [
    ("/", "Home"),
    ("/what-is-esim.html", "What is eSIM"),
    ("/how-to-install-esim.html", "Install guide"),
    ("/why-esim.html", "Why eSIM"),
    ("/about.html", "About"),
]


def head(title, desc, path):
    canonical = SITE["base_url"].rstrip("/") + path
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{html.escape(canonical)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<link rel="icon" href="/assets/img/logo.png">
<link rel="stylesheet" href="/assets/styles.css">
</head>
<body>"""


def header(active):
    links = "".join(
        f'<a href="{href}" class="{"active" if href == active else ""}">{html.escape(label)}</a>'
        for href, label in NAV
    )
    return f"""
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/">
      <img src="/assets/img/logo.png" alt="{html.escape(SITE['brand'])} logo">
      <span>{html.escape(SITE['brand'])}</span>
    </a>
    <button class="nav-toggle" aria-label="Toggle menu" onclick="document.body.classList.toggle('nav-open')">☰</button>
    <nav class="site-nav">{links}</nav>
  </div>
</header>"""


def footer():
    year = datetime.now(timezone.utc).year
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <p class="disclosure">Some links on {html.escape(SITE['brand'])} are affiliate links. If you buy through them we may earn a commission at no extra cost to you. Prices and plans change often — always confirm on the provider's site.</p>
    <nav class="footer-nav">
      <a href="/about.html">About</a>
      <a href="/privacy-policy.html">Privacy</a>
      <a href="/terms.html">Terms</a>
      <a href="/affiliate-disclosure.html">Affiliate disclosure</a>
    </nav>
    <p class="copy">&copy; {year} {html.escape(SITE['brand'])}.</p>
  </div>
</footer>
<script src="/assets/app.js" defer></script>
</body>
</html>"""


def render_card(p):
    data = p.get("data_gb")
    data_disp = "Unlimited" if data == "unlimited" else f"{data:g}GB"
    ppg = p["metrics"].get("price_per_gb")
    ppd = p["metrics"].get("price_per_day")
    value = f"{CUR}{ppg:.2f}/GB" if ppg else (f"{CUR}{ppd:.2f}/day" if ppd else "")
    price = p.get("price")
    price_disp = f"{CUR}{price:.2f}" if isinstance(price, (int, float)) else "—"
    placement = p.get("placement")
    top_pick = p.get("top_pick")
    classes = "card" + (" top-pick" if top_pick else "") + (" placement" if placement else "")
    tags = ""
    if top_pick:
        tags += '<span class="ribbon ribbon-top">Top pick</span>'
    if placement:
        tags += '<span class="ribbon ribbon-paid">Paid placement</span>'
    ribbon = f'<div class="ribbons">{tags}</div>' if tags else ""
    return f"""
    <article class="{classes}" data-region="{html.escape(p.get('region',''))}">
      {ribbon}
      <div class="rank">#{p.get('rank','')}</div>
      <h3>{html.escape(p.get('provider',''))}<small>{html.escape(p.get('plan_name',''))}</small></h3>
      <p class="meta">{html.escape(p.get('region',''))} &middot; {html.escape(p.get('country',''))}</p>
      <p class="specs">{data_disp} &middot; {p.get('validity_days','')} days</p>
      <p class="price">{price_disp}<span class="value">{value}</span></p>
      <a class="cta" href="{html.escape(p.get('product_url','') or '#')}" target="_blank" rel="nofollow sponsored noopener">Get this plan</a>
    </article>"""


def build_index():
    data_file = ROOT / "plans.json"
    plans = json.loads(data_file.read_text()) if data_file.exists() else []
    filters = '<button class="filter active" data-filter="all">All</button>' + "".join(
        f'<button class="filter" data-filter="{html.escape(r)}">{html.escape(r)}</button>'
        for r in SITE["regions"]
    )
    cards = "".join(render_card(p) for p in plans) or '<p class="empty">No plans yet. Run the data refresh.</p>'
    stamps = [p.get("timestamp") for p in plans if p.get("timestamp")]
    checked = ""
    if stamps:
        newest = max(stamps)
        try:
            shown = datetime.fromisoformat(newest).strftime("%d %b %Y")
        except ValueError:
            shown = newest[:10]
        checked = f" Prices last checked {shown}."
    body = f"""
<section class="hero">
  <div class="wrap">
    <h1>{html.escape(SITE['brand'])}</h1>
    <p class="tagline">{html.escape(SITE['tagline'])}</p>
    <p class="sub">Travel eSIM plans ranked by real value: cost per GB and per day.{checked}</p>
  </div>
</section>
<section class="controls"><div class="wrap filters">{filters}</div></section>
<main class="wrap"><div class="grid" id="grid">{cards}</div></main>"""
    page = head(f"{SITE['brand']} — {SITE['tagline']}", SITE["description"], "/") \
        + header("/") + body + footer()
    (ROOT / "index.html").write_text(page)
    return len(plans)


def build_pages():
    for path, meta in PAGES.items():
        page = head(f"{meta['title']} — {SITE['brand']}", meta["desc"], "/" + path) \
            + header("/" + path) \
            + f'<main class="wrap article"><h1>{html.escape(meta["title"])}</h1>{meta["body"]}</main>' \
            + footer()
        (ROOT / path).write_text(page)
    return len(PAGES)


def main():
    n = build_index()
    m = build_pages()
    print(f"Built index.html ({n} plans) + {m} content pages")


if __name__ == "__main__":
    main()
