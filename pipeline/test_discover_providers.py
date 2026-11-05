"""Offline tests for provider discovery. Synthetic HTML only, no network.

    python3 pipeline/test_discover_providers.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bs4 import BeautifulSoup  # noqa: E402

import discover_providers as d  # noqa: E402

HOME = """
<html><body>
<nav><a href="/plans">Plans</a><a href="/help">Help</a></nav>
<p>Travel eSIM from £4.50. Example Sim keeps you online in 190 countries.</p>
<footer>
  <a href="/affiliate-program">Affiliate Program</a>
  <a href="/refer">Refer a friend, get £3</a>
  <a href="/business">eSIM for business</a>
  <a href="https://app.impact.com/campaign-promo-signup/ExampleSim.brand">Join</a>
  <a href="mailto:hi@example.com">Email</a>
</footer>
</body></html>
"""

PROGRAMME = """
<html><body>
<h1>Join the Example Sim affiliate programme</h1>
<p>Earn 12% commission on every sale, and 5% on top-ups.
Our 30-day cookie means you get credit for late buyers.
Data plans from 1GB to 50GB, discounts of up to 70% off.</p>
<a href="https://examplesim.pxf.io/c/123/456/789">Apply</a>
</body></html>
"""


def test_classify_links():
    links = d.classify_links("https://www.examplesim.com/", BeautifulSoup(HOME, "html.parser"))
    assert links["programme"][0] == "https://www.examplesim.com/affiliate-program", links
    assert links["referral"] == ["https://www.examplesim.com/refer"], links
    assert links["b2b"] == ["https://www.examplesim.com/business"], links
    assert d.detect_networks(*links["network"]) == ["impact"]


def test_commission_and_cookie():
    text = d.visible_text(BeautifulSoup(PROGRAMME, "html.parser"))
    # 12% and 5% sit near commission language. 70% is a discount and over the cap.
    assert d.find_commission(text) == ["12%", "5%"], d.find_commission(text)
    assert d.find_cookie_days(text) == 30
    assert d.find_cookie_days("Cookie duration: 45 days") == 45
    assert d.find_cookie_days("No cookies here") is None


def test_networks():
    assert d.detect_networks("https://www.awin1.com/cread.php?awinmid=1") == ["awin"]
    assert d.detect_networks("https://brand.partnerstack.com/") == ["partnerstack"]
    assert d.detect_networks("https://example.com/") == []


FILLER = " Stay connected abroad with fast data in over 150 destinations." * 20


def test_guessing():
    cands = d.candidate_domains("Breeze SIM", "breeze")
    assert "https://breezesim.com/" in cands and "https://breezeesim.com/" in cands
    assert d.page_is_provider(f"<title>Breeze SIM</title><p>Buy an eSIM.{FILLER}</p>", "Breeze SIM", "breeze")
    assert not d.page_is_provider(f"<title>Breeze SIM</title><p>Broadband deals.{FILLER}</p>", "Breeze SIM", "breeze")
    assert not d.page_is_provider(f"<p>An eSIM shop.{FILLER}</p>", "Breeze SIM", "breeze")


def test_parked_domain_rejected():
    # A parked page whose only text is its own domain must not pass as the provider.
    parked = "<title>sailyesim.com</title><p>sailyesim.com is for sale. Buy this domain.</p>"
    assert not d.page_is_provider(parked, "Saily", "saily", "sailyesim.com")
    assert not d.page_is_provider(parked + "<p>" + "sailyesim.com " * 200 + "</p>", "Saily", "saily", "sailyesim.com")


def test_bot_challenge():
    assert d.is_bot_challenge(403, "<title>Just a moment...</title>")
    assert not d.is_bot_challenge(200, "<title>Just a moment...</title>")
    assert not d.is_bot_challenge(404, "<title>Not found</title>")


def test_gbp():
    assert d.sells_in_gbp(HOME)
    assert not d.sells_in_gbp("<p>From $4.50</p>")


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
