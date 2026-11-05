"""What we checked on the provider's own site.

eSIMDB does not carry networks, activation rules, fair use terms or device
compatibility, so those columns come out of the pipeline blank. We fill them
by hand, provider by provider, and keep the answers here in
data/provider_verification.csv.

They live in their own file for one reason: every pipeline run rebuilds
plans_master.csv from scratch. Anything typed straight into that file is
gone the next morning. Anything in here is joined back in on every run.

One row per provider, or per provider and country when the answer differs
by destination - which networks you get almost always does.

Columns
    provider_slug        join key
    country_code         ISO2, or blank for "true wherever this provider works"
    networks             the host networks, e.g. "EE; Three"
    activation_policy    when the clock starts, and how you install it
    fair_use_policy      the real limit behind an unlimited claim
    device_compatibility what the handset has to be
    source_url           the page we read it on
    last_verified        YYYY-MM-DD
    notes                anything that did not fit above

A country row wins over a blank-country row field by field, so a country
row only needs the bits that differ. Nothing here overwrites a value the
source already gave us.
"""

from __future__ import annotations

import csv
import os

COLUMNS = [
    "provider_slug", "country_code", "networks", "activation_policy",
    "fair_use_policy", "device_compatibility", "source_url",
    "last_verified", "notes",
]

FIELDS = ("networks", "activation_policy", "fair_use_policy",
          "device_compatibility")

FILENAME = "provider_verification.csv"
ENCODING = "utf-8-sig"


def load(path: str) -> dict[tuple[str, str], dict]:
    if not os.path.exists(path):
        return {}
    out: dict[tuple[str, str], dict] = {}
    with open(path, encoding=ENCODING, newline="") as fh:
        for row in csv.DictReader(fh):
            slug = (row.get("provider_slug") or "").strip()
            if not slug:
                continue
            code = (row.get("country_code") or "").strip().upper()
            out[(slug, code)] = {k: (row.get(k) or "").strip() for k in COLUMNS}
    return out


def lookup(table: dict, provider_slug: str, coverage: list[str]) -> dict:
    """The most specific row we hold for this plan.

    A single-country plan can match that country's row. A plan covering
    several countries only matches the provider-wide row - saying "you get
    EE" would be wrong for the other forty destinations.
    """
    if not table or not provider_slug:
        return {}
    merged = dict(table.get((provider_slug, "")) or {})
    if len(coverage) == 1:
        specific = table.get((provider_slug, coverage[0].upper()))
        if specific:
            # The country row wins where it says something, and stays quiet
            # where it does not - activation rules rarely change by country.
            merged.update({k: v for k, v in specific.items() if v})
    return merged


def apply_to(row: dict, entry: dict) -> None:
    """Fill the blank columns. Never overwrite what the source gave us."""
    if not entry:
        return
    for field in FIELDS:
        if not row.get(field) and entry.get(field):
            row[field] = entry[field]
    if entry.get("last_verified"):
        row["last_verified"] = entry["last_verified"]


def write_template(path: str, rows: list[dict]) -> int:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding=ENCODING, newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows([{k: r.get(k, "") for k in COLUMNS} for r in rows])
    return len(rows)
