#!/usr/bin/env python3
"""eSIM Sorted — build the static site.

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

GUIDES = [
    ("/esim-japan.html", "Japan"),
    ("/esim-europe.html", "Europe"),
    ("/esim-usa.html", "USA"),
    ("/esim-thailand.html", "Thailand"),
]

NAV = [
    ("/", "Home"),
    ("/what-is-esim.html", "What is eSIM"),
    ("/how-to-install-esim.html", "Install guide"),
    ("/why-esim.html", "Why eSIM"),
    ("/about.html", "About"),
]


def head(title, desc, path):
    base = SITE["base_url"].rstrip("/")
    canonical = base + path
    og_image = base + "/assets/img/logo.png"
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
<link rel="icon" href="/assets/img/favicon.png">
<link rel="apple-touch-icon" href="/assets/img/favicon.png">
<meta property="og:image" content="{og_image}">
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
    <a class="brand" href="/" aria-label="{html.escape(SITE['brand'])} home">
      <img src="/assets/img/logo-wordmark.png" alt="{html.escape(SITE['brand'])}">
    </a>
    <button class="nav-toggle" aria-label="Toggle menu" onclick="document.body.classList.toggle('nav-open')">☰</button>
    <nav class="site-nav">{links}</nav>
  </div>
</header>"""


def footer():
    year = datetime.now(timezone.utc).year
    guide_links = "".join(
        f'<a href="{href}">{html.escape(label)} guide</a>' for href, label in GUIDES
    )
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
    <nav class="footer-nav">{guide_links}</nav>
    <p class="copy">&copy; {year} {html.escape(SITE['brand'])}.</p>
  </div>
</footer>
<script src="/assets/app.js" defer></script>
</body>
</html>"""


def plan_notes(p):
    """The short plain-English lines under a plan. Only says something when
    there is something to say — a blank column produces no line."""
    m = p["metrics"]
    notes = []

    if m.get("capped_unlimited"):
        when = "each day" if p.get("full_speed_period") == "per_day" else ""
        speed = p.get("post_cap_speed")
        if speed and when:
            notes.append(f"Slows to {speed} once you have used the daily allowance, then starts again the next day.")
        elif speed:
            notes.append(f"Slows to {speed} once the full-speed data runs out.")
        else:
            notes.append("Slows down once the full-speed data runs out.")

    voice = (p.get("voice_type") or "").lower()
    if voice == "native":
        bits = []
        if p.get("calls_included"):
            bits.append(f"{p['calls_included']} calls")
        if p.get("sms_included"):
            bits.append(f"{p['sms_included']} texts")
        detail = " and ".join(bits)
        line = "Makes real phone calls"
        if detail:
            line += f" — {detail}"
        if p.get("number_country") == "UK":
            line += ", with a UK number"
        elif p.get("number_country"):
            line += f", with a {p['number_country']} number"
        notes.append(line + ".")
    elif voice == "app_voip":
        notes.append("Calls go through the provider's own app, not the phone dialler.")
    elif voice == "external_voip":
        notes.append("Data only. Apps like WhatsApp work, but it makes no ordinary calls.")
    elif voice == "none":
        notes.append("Data only, no calls or texts.")

    hotspot = (p.get("hotspot") or "").lower()
    if hotspot == "capped":
        notes.append("Sharing to another device is limited.")
    elif hotspot == "no":
        notes.append("You cannot share the connection to another device.")

    return notes


def render_card(p):
    m = p["metrics"]
    data = p.get("data_gb")
    full = m.get("full_speed_gb")
    if data == "unlimited":
        if full and p.get("full_speed_period") == "per_day":
            data_disp = f"Unlimited, {full:g}GB a day at full speed"
        elif full:
            data_disp = f"Unlimited, {full:g}GB at full speed"
        else:
            data_disp = "Unlimited"
    else:
        data_disp = f"{data:g}GB"

    ppg = m.get("price_per_gb")
    ppd = m.get("price_per_day")
    if ppg:
        value = f"{CUR}{ppg:.2f}/GB" + (" at full speed" if m.get("capped_unlimited") else "")
    elif ppd:
        value = f"{CUR}{ppd:.2f}/day"
    else:
        value = ""

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

    notes = plan_notes(p)
    notes_html = ""
    if notes:
        items = "".join(f"<li>{html.escape(n)}</li>" for n in notes)
        notes_html = f'<ul class="notes">{items}</ul>'

    return f"""
    <article class="{classes}" data-region="{html.escape(p.get('region',''))}">
      {ribbon}
      <div class="rank">#{p.get('rank','')}</div>
      <h3>{html.escape(p.get('provider',''))}<small>{html.escape(p.get('plan_name',''))}</small></h3>
      <p class="meta">{html.escape(p.get('region',''))} &middot; {html.escape(p.get('country',''))}</p>
      <p class="specs">{html.escape(data_disp)} &middot; {p.get('validity_days','')} days</p>
      {notes_html}
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
    <p class="sub">Ranked on what a pound actually buys: cost per gigabyte of full-speed data. Plans sold as unlimited are scored on the allowance you get before the provider slows you down.{checked}</p>
  </div>
</section>
<section class="controls"><div class="wrap filters">{filters}</div></section>
<section class="wrap"><p class="guide-strip">Going somewhere specific? <a href="/esim-japan.html">Japan</a>, <a href="/esim-europe.html">Europe</a>, <a href="/esim-usa.html">USA</a>, <a href="/esim-thailand.html">Thailand</a>.</p></section>
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


def build_robots():
    """Generated from config so the sitemap URL cannot drift from base_url."""
    base = SITE["base_url"].rstrip("/")
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n"
    )


def main():
    n = build_index()
    m = build_pages()
    build_robots()
    print(f"Built index.html ({n} plans) + {m} content pages + robots.txt")


if __name__ == "__main__":
    main()
