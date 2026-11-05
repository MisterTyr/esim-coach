"""Re-apply the link rules and the verification queue to an existing plans_master.csv.

Why this exists: a full rebuild re-reads a gigabyte of cached JSON. When all
that changed is provider_links.csv or the verification rules, this rewrites
the affected columns in place instead, using the exact same functions the
pipeline uses. No re-fetch, no re-parse.

    python3 -m tools.apply_links [--data data]

Columns it rewrites:
    product_url, provider_url, link_type,
    networks, activation_policy, fair_use_policy, device_compatibility,
    last_verified,
    needs_verification, verification_reasons, verification_priority
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from esimdb_ingest import build, links, schema, verify  # noqa: E402

csv.field_size_limit(1 << 30)

NUMERIC = ("price_usd", "price_gbp", "price_eur", "promo_price_usd",
           "promo_price_gbp", "promo_price_eur", "price_per_gb",
           "data_gb", "total_data_gb")


def as_number(value: str):
    if value in ("", None):
        return value
    try:
        return float(value)
    except ValueError:
        return value


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data")
    args = ap.parse_args(argv)

    master = os.path.join(args.data, "plans_master.csv")
    table = links.load(os.path.join(args.data, links.FILENAME))
    approved = sum(1 for v in table.values() if links.is_approved(v))
    print("Provider links: %d rows, %d approved." % (len(table), approved))

    checks = verify.load(os.path.join(args.data, verify.FILENAME))
    print("Provider checks on file: %d rows." % len(checks))

    with open(master, encoding=links.ENCODING, newline="") as fh:
        reader = csv.DictReader(fh)
        columns = list(reader.fieldnames or [])
        for extra in ("verification_priority", "link_type"):
            if extra not in columns:
                columns.insert(columns.index("run_id"), extra)

        tmp = tempfile.NamedTemporaryFile(
            "w", encoding=links.ENCODING, newline="", delete=False,
            dir=args.data, suffix=".tmp")
        writer = csv.DictWriter(tmp, fieldnames=columns, extrasaction="ignore",
                                quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        writer.writeheader()

        counts = {"affiliate": 0, "provider_site": 0, "none": 0}
        priorities = {"1": 0, "2": 0, "3": 0, "": 0}
        total = 0
        verified_rows = 0
        for row in reader:
            total += 1
            link = table.get(row["provider_slug"], {})
            url, how = links.product_url(link)
            row["product_url"] = url
            row["provider_url"] = link.get("provider_url", "")
            row["link_type"] = how
            counts[how] += 1

            # eSIMDB never carries these, so clearing first lets a
            # correction in provider_verification.csv actually land.
            for field in verify.FIELDS + ("last_verified",):
                row[field] = ""
            coverage = [c for c in row["coverage_countries"].split(",") if c]
            entry = verify.lookup(checks, row["provider_slug"], coverage)
            verify.apply_to(row, entry)
            if entry:
                verified_rows += 1

            typed = dict(row)
            for f in NUMERIC:
                typed[f] = as_number(row.get(f, ""))
            reasons = build.verification_reasons(typed)
            row["needs_verification"] = "true" if reasons else "false"
            row["verification_reasons"] = "; ".join(reasons)
            row["verification_priority"] = build.verification_priority(typed, reasons)
            priorities[row["verification_priority"]] += 1
            writer.writerow(row)
        tmp.close()

    os.replace(tmp.name, master)
    print("Rewrote %d plans." % total)
    print("Links      affiliate %d | provider site %d | none %d"
          % (counts["affiliate"], counts["provider_site"], counts["none"]))
    print("Queue      priority 1 %d | 2 %d | 3 %d | not queued %d"
          % (priorities["1"], priorities["2"], priorities["3"], priorities[""]))
    print("Checked    %d plans carry details from a provider's own site."
          % verified_rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
