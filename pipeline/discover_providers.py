"""Provider discovery: find each eSIM provider's own site and any affiliate programme.

Reads leads from data/providers/leads.csv (names and, where known, websites).
For every lead it:

  1. finds the provider's own site, guessing from the name if no URL is known,
     and only accepting a guess whose page mentions eSIM and the provider's name;
  2. reads robots.txt and skips anything it disallows;
  3. reads the homepage, looks for affiliate / partner / creator links, and
     tries a handful of common programme paths if none are linked;
  4. on each programme page, recognises the network from its signup links
     (Impact, Awin, CJ, PartnerStack ...) and reads any published commission
     and cookie length;
  5. records the evidence URL and the date for every claim.

Nothing here is a verified fact. Every row comes out as status=needs_review,
and a person confirms it before it counts.

Polite by design: one request at a time, a pause between requests, a page cap
per provider, an honest User-Agent, and robots.txt honoured.

Usage:
    python3 pipeline/discover_providers.py                 # every lead
    python3 pipeline/discover_providers.py --only airalo,nomad
    python3 pipeline/discover_providers.py --limit 10
    python3 pipeline/discover_providers.py --resume        # skip leads already done today
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import socket
import sys
import time
import warnings
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

warnings.filterwarnings("ignore", message=".*OpenSSL.*")

import requests  # noqa: E402
from bs4 import BeautifulSoup  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LEADS = ROOT / "data" / "providers" / "leads.csv"
OUT_DIR = ROOT / "data" / "providers"
CACHE = ROOT / ".cache" / "discovery"

USER_AGENT = "eSIMSortedBot/0.1 (+https://esim-sorted.co.uk; provider discovery)"
DELAY_SECONDS = 2.5
TIMEOUT = 15
MAX_PAGES_PER_PROVIDER = 10

# ---------------------------------------------------------------------------
# What we look for
# ---------------------------------------------------------------------------

# Words in a link's text or URL that suggest an affiliate-type programme.
PROGRAMME_WORDS = re.compile(
    r"affiliat|ambassador|creator|influencer|partner\s*program|partners?\b|"
    r"earn\s+with|become\s+a\s+partner|publisher|commission",
    re.I,
)
# Customer refer-a-friend schemes are not affiliate programmes; record separately.
REFERRAL_WORDS = re.compile(r"refer\s*(a|-a-)?\s*friend|invite\s+friends|referral", re.I)
# Business partner pages (resellers, B2B, carriers) are a different thing too.
B2B_WORDS = re.compile(r"reseller|wholesale|b2b|for\s+business|white[\s-]?label|api\s+partner|enterprise", re.I)

COMMON_PATHS = [
    "/affiliate", "/affiliates", "/affiliate-program", "/affiliate-programme",
    "/partners", "/partner", "/ambassador", "/creators", "/influencers",
]

# Network fingerprints, matched against every URL and the raw HTML of a page.
NETWORKS: List[Tuple[str, re.Pattern]] = [
    ("impact", re.compile(r"impact\.com|impactradius|\.pxf\.io|\.sjv\.io|evyy\.net|7eer\.net|ojrq\.net|impact-affiliate", re.I)),
    ("awin", re.compile(r"awin1?\.com|zenaps\.com|ui\.awin", re.I)),
    ("cj", re.compile(r"\bcj\.com|anrdoezrs\.net|dpbolvw\.net|jdoqocy\.com|kqzyfj\.com|tkqlhce\.com|emjcd\.com", re.I)),
    ("partnerstack", re.compile(r"partnerstack\.com|grsm\.io", re.I)),
    ("tapfiliate", re.compile(r"tapfiliate\.com", re.I)),
    ("rewardful", re.compile(r"rewardful\.com|getrewardful", re.I)),
    ("everflow", re.compile(r"everflow\.io", re.I)),
    ("firstpromoter", re.compile(r"firstpromoter\.com", re.I)),
    ("refersion", re.compile(r"refersion\.com", re.I)),
    ("shareasale", re.compile(r"shareasale\.com", re.I)),
    ("rakuten", re.compile(r"rakutenadvertising\.com|linksynergy\.com", re.I)),
    ("partnerize", re.compile(r"partnerize\.com|prf\.hn", re.I)),
    ("admitad", re.compile(r"admitad\.com", re.I)),
    ("tradedoubler", re.compile(r"tradedoubler\.com", re.I)),
    ("goaffpro", re.compile(r"goaffpro\.com", re.I)),
    ("uppromote", re.compile(r"uppromote\.com", re.I)),
    ("tolt", re.compile(r"tolt\.io", re.I)),
    ("postaffiliatepro", re.compile(r"postaffiliatepro\.com", re.I)),
    ("leaddyno", re.compile(r"leaddyno\.com", re.I)),
    ("trackdesk", re.compile(r"trackdesk\.com", re.I)),
    ("promotekit", re.compile(r"promotekit\.com", re.I)),
]

PCT = re.compile(r"(\d{1,2}(?:\.\d{1,2})?)\s?%")
COMMISSION_CONTEXT = re.compile(r"commission|earn|revenue\s+share|payout|per\s+sale|reward", re.I)
COOKIE_PATTERNS = [
    re.compile(r"(\d{1,3})[\s-]*days?\s+(?:cookie|tracking|attribution|referral\s+window)", re.I),
    re.compile(r"cookie[^.%]{0,40}?(\d{1,3})\s*-?\s*days?", re.I),
]


# ---------------------------------------------------------------------------
# Pure helpers (unit-tested, no network)
# ---------------------------------------------------------------------------

def name_base(name: str, slug: str) -> str:
    """The alphanumeric core of a provider's name, for guessing and matching."""
    cleaned = re.sub(r"[^a-z0-9]", "", name.lower())
    return cleaned or re.sub(r"[^a-z0-9]", "", slug.lower())


def name_cores(base: str) -> List[str]:
    """The name with any trailing "sim"/"esim" removed. Both readings are kept,
    because "breezesim" is breeze+sim but "travelesim" is travel+esim."""
    cores = []
    for suffix in ("esim", "sim"):
        if base.endswith(suffix) and len(base) > len(suffix):
            cores.append(base[: -len(suffix)])
    cores = [c.rstrip("-") for c in cores if c]
    return list(dict.fromkeys(cores)) or [base]


def candidate_domains(name: str, slug: str) -> List[str]:
    """Plausible homepages for a provider with no known site. Guesses only."""
    base = name_base(name, slug)
    hosts = [f"{base}.com", f"www.{base}.com", f"{base}.io", f"{base}.app", f"{base}.co", f"get{base}.com"]
    for core in name_cores(base):
        hosts += [f"{core}esim.com", f"{core}-esim.com", f"esim{core}.com", f"{core}sim.com", f"{core}.travel"]
    return [f"https://{h}/" for h in dict.fromkeys(hosts)]


def page_is_provider(html: str, name: str, slug: str, host: str = "") -> bool:
    """A guessed domain only counts if the page is plainly an eSIM seller of that name.

    The check runs on the page's visible text with the hostname taken out, and
    needs a real amount of text. Otherwise a parked domain like
    "sailyesim.com", whose only text is its own name, would pass.
    """
    text = visible_text(BeautifulSoup(html, "html.parser")).lower()
    if host:
        text = text.replace(host.lower().replace("www.", ""), " ")
    if len(text) < 800 or "esim" not in text:
        return False
    base = name_base(name, slug)
    squashed = re.sub(r"[^a-z0-9]", "", text)
    return base in squashed or any(len(c) >= 4 and c in squashed for c in name_cores(base))


def is_bot_challenge(status: int, html: str) -> bool:
    """Cloudflare and similar 'are you human' pages. We never try to get past these."""
    if status not in (403, 429, 503):
        return False
    h = html[:20000]
    return any(sig in h for sig in ("Just a moment", "cf-chl", "Attention Required", "challenge-platform", "captcha"))


def detect_networks(*blobs: str) -> List[str]:
    found = []
    for net, pat in NETWORKS:
        if any(pat.search(b or "") for b in blobs):
            found.append(net)
    return found


def find_commission(text: str) -> List[str]:
    """Percentages that sit near commission language. Returns e.g. ['10%', '15%']."""
    hits = []
    for m in PCT.finditer(text):
        window = text[max(0, m.start() - 120): m.end() + 120]
        if COMMISSION_CONTEXT.search(window):
            val = float(m.group(1))
            if 1 <= val <= 60:
                label = f"{m.group(1)}%"
                if label not in hits:
                    hits.append(label)
    return hits


def find_cookie_days(text: str) -> Optional[int]:
    for pat in COOKIE_PATTERNS:
        m = pat.search(text)
        if m:
            days = int(m.group(1))
            if 1 <= days <= 365:
                return days
    return None


def classify_links(base_url: str, soup: BeautifulSoup) -> Dict[str, List[str]]:
    """Sort a page's links into programme / referral / b2b / network buckets."""
    out = {"programme": [], "referral": [], "b2b": [], "network": []}
    host = urlparse(base_url).netloc.replace("www.", "")
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        url = urljoin(base_url, href)
        label = " ".join(a.get_text(" ", strip=True).split())[:80]
        probe = f"{label} {url}"
        link_host = urlparse(url).netloc.replace("www.", "")
        if detect_networks(url):
            out["network"].append(url)
        if link_host.startswith(("affiliate", "affiliates", "partners", "partner")) and host in link_host:
            out["programme"].append(url)
        elif B2B_WORDS.search(probe):
            out["b2b"].append(url)
        elif PROGRAMME_WORDS.search(probe):
            out["programme"].append(url)
        elif REFERRAL_WORDS.search(probe):
            out["referral"].append(url)
    for k in out:
        out[k] = list(dict.fromkeys(out[k]))[:8]
    return out


def sells_in_gbp(html: str) -> bool:
    return "£" in html or bool(re.search(r"\bGBP\b", html))


def visible_text(soup: BeautifulSoup) -> str:
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    return " ".join(soup.get_text(" ", strip=True).split())


# ---------------------------------------------------------------------------
# Polite fetching
# ---------------------------------------------------------------------------

class Fetcher:
    def __init__(self, delay: float = DELAY_SECONDS, use_cache: bool = True):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "en-GB,en;q=0.8"})
        self.delay = delay
        self.use_cache = use_cache
        self.last = 0.0
        self.robots: Dict[str, Optional[RobotFileParser]] = {}
        CACHE.mkdir(parents=True, exist_ok=True)

    def _wait(self):
        gap = time.monotonic() - self.last
        if gap < self.delay:
            time.sleep(self.delay - gap)
        self.last = time.monotonic()

    def allowed(self, url: str) -> bool:
        p = urlparse(url)
        origin = f"{p.scheme}://{p.netloc}"
        if origin not in self.robots:
            rp: Optional[RobotFileParser] = RobotFileParser()
            try:
                self._wait()
                r = self.s.get(origin + "/robots.txt", timeout=TIMEOUT)
                if r.status_code >= 400:
                    rp = None  # no robots.txt: everything allowed
                else:
                    rp.parse(r.text.splitlines())
            except requests.RequestException:
                rp = None
            self.robots[origin] = rp
        rp = self.robots[origin]
        return True if rp is None else rp.can_fetch(USER_AGENT, url)

    def get(self, url: str) -> Tuple[Optional[str], Optional[str], str]:
        """Returns (final_url, html, note). html is None on failure or disallow."""
        key = CACHE / (hashlib.sha1(url.encode()).hexdigest() + ".json")
        if self.use_cache and key.exists():
            d = json.loads(key.read_text())
            if d.get("day") == date.today().isoformat():
                return d["final"], d["html"], d["note"]
        if not self.allowed(url):
            return None, None, "robots.txt disallows"
        self._wait()
        try:
            r = self.s.get(url, timeout=TIMEOUT, allow_redirects=True)
        except requests.RequestException as e:
            return None, None, f"error: {type(e).__name__}"
        ctype = r.headers.get("content-type", "")
        if is_bot_challenge(r.status_code, r.text or ""):
            html, final, note = None, r.url, "blocked by bot protection"
        elif r.status_code >= 400 or "html" not in ctype:
            note = f"HTTP {r.status_code}" if r.status_code >= 400 else f"not HTML ({ctype[:30]})"
            html, final = None, r.url
        else:
            html, final, note = r.text, r.url, "ok"
        key.write_text(json.dumps({"day": date.today().isoformat(), "final": final, "html": html, "note": note}))
        return final, html, note


def resolves(url: str) -> bool:
    try:
        socket.gethostbyname(urlparse(url).netloc)
        return True
    except (socket.gaierror, UnicodeError):
        return False


# ---------------------------------------------------------------------------
# One provider
# ---------------------------------------------------------------------------

FIELDS = [
    "slug", "name", "site", "site_basis", "sells_in_gbp", "needs_browser",
    "programme", "networks", "commission", "cookie_days", "programme_url",
    "referral_scheme_url", "b2b_url", "evidence", "notes", "checked", "status",
]


def discover(lead: Dict[str, str], f: Fetcher) -> Dict[str, str]:
    row = {k: "" for k in FIELDS}
    row.update(slug=lead["slug"], name=lead["name"], checked=date.today().isoformat(), status="needs_review")
    notes: List[str] = []
    pages = 0

    # 1. The provider's own site.
    home_html, site = None, None
    if lead.get("url"):
        site, home_html, note = f.get(lead["url"])
        pages += 1
        row["site_basis"] = lead.get("url_basis") or "from leads"
        if home_html is None:
            notes.append(f"known site failed: {note}")
            if note == "blocked by bot protection":
                row["programme"] = "check by hand"
    else:
        for cand in candidate_domains(lead["name"], lead["slug"]):
            if pages >= 6:
                break
            if not resolves(cand):
                continue
            final, html, note = f.get(cand)
            pages += 1
            if note == "blocked by bot protection":
                # Very likely the real site (lookalikes rarely pay for bot protection),
                # but we can't read it, so a person has to.
                row.update(site=cand, site_basis="guessed; site blocks automated visits: check by hand",
                           programme="check by hand", notes="bot protection on the site; not bypassed")
                return row
            if html and page_is_provider(html, lead["name"], lead["slug"], urlparse(final or cand).netloc):
                site, home_html = final, html
                row["site_basis"] = "guessed from name, page mentions eSIM and the name: confirm"
                break
        if not site:
            row["site_basis"] = "not found"
            row["notes"] = "no site found from the name; needs a manual search"
            return row
    row["site"] = site or lead.get("url", "")
    if home_html is None:
        row["notes"] = "; ".join(notes)
        return row

    soup = BeautifulSoup(home_html, "html.parser")
    links = classify_links(site, soup)
    text = visible_text(BeautifulSoup(home_html, "html.parser"))
    row["sells_in_gbp"] = "yes" if sells_in_gbp(home_html) else "not on homepage"
    if len(text) < 600:
        row["needs_browser"] = "yes"
        notes.append("homepage is mostly JavaScript; links may be missing")
    row["referral_scheme_url"] = links["referral"][0] if links["referral"] else ""
    row["b2b_url"] = links["b2b"][0] if links["b2b"] else ""

    # 2. Candidate programme pages: linked ones first, then common paths on the same site.
    origin = "{0.scheme}://{0.netloc}".format(urlparse(site))
    candidates = links["programme"] + [origin + p for p in COMMON_PATHS]
    networks = set(detect_networks(*links["network"]))
    evidence: List[str] = []
    if networks:
        evidence.append("homepage links to " + ", ".join(sorted(networks)))

    commission: List[str] = []
    cookie: Optional[int] = None
    programme_url = ""
    for url in dict.fromkeys(candidates):
        if pages >= MAX_PAGES_PER_PROVIDER:
            notes.append("page cap reached")
            break
        final, html, note = f.get(url)
        pages += 1
        if not html:
            continue
        psoup = BeautifulSoup(html, "html.parser")
        ptext = visible_text(BeautifulSoup(html, "html.parser"))
        looks_like_programme = bool(re.search(r"affiliate|commission|ambassador|creator program|influencer", ptext, re.I))
        if not looks_like_programme:
            continue
        page_links = [urljoin(final, a["href"]) for a in psoup.find_all("a", href=True)]
        nets = detect_networks(html, *page_links, final or "")
        networks.update(nets)
        c = find_commission(ptext)
        k = find_cookie_days(ptext)
        if not programme_url:
            programme_url = final or url
        if nets:
            evidence.append(f"{final}: {', '.join(nets)}")
        if c:
            commission.extend(x for x in c if x not in commission)
            evidence.append(f"{final}: commission {', '.join(c)}")
        if k and not cookie:
            cookie = k
            evidence.append(f"{final}: {k}-day cookie")
        # Stop once we have a programme page with something concrete on it.
        if programme_url and (nets or c):
            break

    row["networks"] = ", ".join(sorted(networks))
    row["commission"] = ", ".join(commission)
    row["cookie_days"] = str(cookie or "")
    row["programme_url"] = programme_url
    if programme_url or networks:
        row["programme"] = "likely" if (networks or commission) else "possible"
        if programme_url and not networks:
            notes.append("programme page found but no network link: may be in-house, or the signup is behind JavaScript")
    else:
        row["programme"] = "none found"
    row["evidence"] = " | ".join(evidence)
    row["notes"] = "; ".join(notes)
    return row


# ---------------------------------------------------------------------------
# Running it
# ---------------------------------------------------------------------------

def load_leads(only: Optional[Iterable[str]] = None, limit: Optional[int] = None) -> List[Dict[str, str]]:
    with open(LEADS, encoding="utf-8") as fh:
        leads = list(csv.DictReader(fh))
    if only:
        wanted = set(only)
        leads = [l for l in leads if l["slug"] in wanted]
    # Known sites first: quickest wins, and the most likely to be real.
    leads.sort(key=lambda l: (l["url"] == "", l["slug"]))
    return leads[:limit] if limit else leads


def write_review(rows: List[Dict[str, str]], path: Path) -> None:
    order = {"likely": 0, "possible": 1, "check by hand": 2, "none found": 3, "": 4}
    rows = sorted(rows, key=lambda r: (order.get(r["programme"], 3), r["networks"] == "", r["slug"]))
    found_site = sum(1 for r in rows if r["site"])
    likely = [r for r in rows if r["programme"] == "likely"]
    possible = [r for r in rows if r["programme"] == "possible"]
    by_net: Dict[str, int] = {}
    for r in rows:
        for n in filter(None, (x.strip() for x in r["networks"].split(","))):
            by_net[n] = by_net.get(n, 0) + 1
    lines = [
        f"# Provider discovery: {date.today().isoformat()}",
        "",
        "Nothing here is confirmed. Every row needs a person to open the evidence link.",
        "",
        f"- Leads checked: {len(rows)}",
        f"- Own site found: {found_site}",
        f"- Programme likely (network or commission seen): {len(likely)}",
        f"- Programme possible (page found, nothing concrete): {len(possible)}",
        "- By network: " + (", ".join(f"{k} {v}" for k, v in sorted(by_net.items(), key=lambda x: -x[1])) or "none"),
        "",
        "## Likely programmes",
        "",
        "| Provider | Network | Commission | Cookie | Programme page | GBP |",
        "|---|---|---|---|---|---|",
    ]
    for r in likely:
        lines.append(f"| {r['name']} | {r['networks'] or 'in-house?'} | {r['commission'] or '-'} | "
                     f"{(r['cookie_days'] + 'd') if r['cookie_days'] else '-'} | {r['programme_url'] or r['site']} | {r['sells_in_gbp']} |")
    lines += ["", "## Possible: a programme page exists, details not readable", ""]
    for r in possible:
        lines.append(f"- **{r['name']}**: {r['programme_url']} {('(' + r['notes'] + ')') if r['notes'] else ''}")
    lines += ["", "## Check by hand: the site blocks automated visits", ""]
    lines += [f"- **{r['name']}**: {r['site']}" for r in rows if r["programme"] == "check by hand"]
    lines += ["", "## No site found from the name", ""]
    lines += [f"- {r['name']} (`{r['slug']}`)" for r in rows if not r["site"]]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="comma-separated slugs")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--resume", action="store_true", help="skip leads already in today's output")
    ap.add_argument("--delay", type=float, default=DELAY_SECONDS)
    args = ap.parse_args(argv)

    today = date.today().isoformat()
    out_csv = OUT_DIR / f"discovery-{today}.csv"
    out_md = OUT_DIR / f"discovery-{today}.md"
    done: Dict[str, Dict[str, str]] = {}
    if args.resume and out_csv.exists():
        with open(out_csv, encoding="utf-8") as fh:
            done = {r["slug"]: r for r in csv.DictReader(fh)}

    leads = load_leads(args.only.split(",") if args.only else None, args.limit)
    f = Fetcher(delay=max(args.delay, 1.5))
    rows = list(done.values())
    for i, lead in enumerate(leads, 1):
        if lead["slug"] in done:
            continue
        try:
            row = discover(lead, f)
        except Exception as e:  # one bad site must not stop the run
            row = {k: "" for k in FIELDS}
            row.update(slug=lead["slug"], name=lead["name"], checked=today, status="needs_review",
                       notes=f"crashed: {type(e).__name__}: {e}"[:200])
        rows.append(row)
        print(f"[{i}/{len(leads)}] {lead['slug']:<22} site={'yes' if row['site'] else 'no ':<3} "
              f"programme={row['programme'] or '-':<10} {row['networks']}", flush=True)
        # Write as we go so a stopped run keeps its work.
        with open(out_csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(sorted(rows, key=lambda r: r["slug"]))
    write_review(rows, out_md)
    print(f"\nWrote {out_csv.relative_to(ROOT)} and {out_md.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
