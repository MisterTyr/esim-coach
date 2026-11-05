"""Our own provider links.

eSIMDB's outbound buy links carry eSIMDB's affiliate ID, so we cannot use
them. This module reads data/provider_links.csv - a file we maintain by
hand - and turns it into the links the site actually publishes.

The file has one row per provider_slug. Everything except the slug can be
blank, and a blank row simply means "we have no link for this provider yet".

Columns
    provider_slug      join key, matches providers.csv
    provider           provider name, for reading the file by eye
    provider_url       the provider's real website, https://
    affiliate_network  awin | impact | direct | ""      (free text)
    affiliate_status   none | pending | approved
    affiliate_id       our publisher/advertiser ID on that network
    link_template      our tracking link, with {dest} where the destination
                       URL goes. {dest_encoded} gets it percent-encoded.
                       Leave blank until the programme is approved.
    deeplink_supported true | false | unknown
    notes              anything worth remembering about this programme
    last_checked       YYYY-MM-DD, when we last looked at this row

Which link ends up on the site:
    approved + a template  ->  our tracking link
    otherwise              ->  the provider's own site, earning nothing
    neither                ->  blank, and the plan is marked not linkable
"""

from __future__ import annotations

import csv
import os
from urllib.parse import quote

COLUMNS = [
    "provider_slug", "provider", "provider_url", "affiliate_network",
    "affiliate_status", "affiliate_id", "link_template",
    "deeplink_supported", "notes", "last_checked",
]

FILENAME = "provider_links.csv"
ENCODING = "utf-8-sig"


def load(path: str) -> dict[str, dict]:
    """Read provider_links.csv. Missing file is fine - you get nothing back."""
    if not os.path.exists(path):
        return {}
    out: dict[str, dict] = {}
    with open(path, encoding=ENCODING, newline="") as fh:
        for row in csv.DictReader(fh):
            slug = (row.get("provider_slug") or "").strip()
            if slug:
                out[slug] = {k: (row.get(k) or "").strip() for k in COLUMNS}
    return out


def is_approved(link: dict) -> bool:
    return (link.get("affiliate_status", "").lower() == "approved"
            and bool(link.get("link_template")))


def product_url(link: dict | None, dest: str = "") -> tuple[str, str]:
    """Return (url, how) for a plan.

    `how` is one of: affiliate, provider_site, none. It goes in the CSV so
    you can tell at a glance which links earn and which do not.
    """
    if not link:
        return "", "none"
    site = link.get("provider_url", "")
    target = dest or site
    if is_approved(link) and target:
        tpl = link["link_template"]
        url = (tpl.replace("{dest_encoded}", quote(target, safe=""))
                  .replace("{dest}", target))
        return url, "affiliate"
    if site:
        return site, "provider_site"
    return "", "none"


def write_scaffold(path: str, providers: list[dict], existing: dict[str, dict] | None = None) -> int:
    """Write one row per provider, keeping anything already filled in."""
    existing = existing or {}
    rows = []
    for p in sorted(providers, key=lambda r: (r.get("provider") or "").lower()):
        slug = p.get("provider_slug") or p.get("slug") or ""
        if not slug:
            continue
        row = dict.fromkeys(COLUMNS, "")
        row.update(existing.get(slug, {}))
        row["provider_slug"] = slug
        row["provider"] = p.get("provider") or p.get("name") or row["provider"]
        rows.append(row)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding=ENCODING, newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return len(rows)
