"""Comparing this run with the previous one.

Nothing is overwritten. The previous run's plans_master.csv is read from a
snapshot directory and every difference becomes a row in change_log.csv.
"""

from __future__ import annotations

import csv
import os
from datetime import datetime, timezone

# Fields worth raising a change event for, with the wording used in the log.
WATCHED = {
    "price": "price",
    "price_usd": "price in dollars",
    "price_gbp": "price in pounds",
    "price_eur": "price in euros",
    "data_gb": "data allowance",
    "daily_data_gb": "daily allowance",
    "total_data_gb": "total allowance",
    "unlimited": "unlimited claim",
    "validity_days": "validity",
    "validity_info": "validity wording",
    "throttle_speed": "slowed speed",
    "possible_throttling": "throttling",
    "has_5g": "5G",
    "network_types": "network types",
    "tethering": "hotspot",
    "telephony": "calls",
    "sms": "texts",
    "phone_number": "phone number",
    "phone_number_country": "phone number country",
    "coverage_countries": "countries covered",
    "coverage_regions": "regions covered",
    "plan_type": "plan type",
    "promo_enabled": "promotion",
    "promo_code": "promo code",
    "promo_price_usd": "promotional price in dollars",
    "promo_price_gbp": "promotional price in pounds",
    "subscription": "subscription",
    "pay_as_you_go": "pay as you go",
    "can_top_up": "top-ups",
    "kyc_required": "ID check",
    "product_url": "link",
}

PRICE_FIELDS = {"price", "price_usd", "price_gbp", "price_eur",
                "promo_price_usd", "promo_price_gbp", "promo_price_eur"}


def read_previous(path: str) -> dict[str, dict]:
    if not path or not os.path.exists(path):
        return {}
    out = {}
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            pid = row.get("plan_id")
            if pid:
                out[pid] = row
    return out


def _num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def diff(previous: dict[str, dict], current_rows: list[dict], run_id: str,
         previous_run_id: str = "") -> list[dict]:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    events: list[dict] = []
    current = {r["plan_id"]: r for r in current_rows}

    prev_providers = {r.get("provider_slug") for r in previous.values()}
    seen_new_providers: set[str] = set()

    def event(kind, row, field="", old="", new=""):
        events.append({
            "change_type": kind,
            "plan_id": row.get("plan_id", ""),
            "provider": row.get("provider", ""),
            "provider_slug": row.get("provider_slug", ""),
            "plan_name": row.get("plan_name", ""),
            "field": field,
            "old_value": old,
            "new_value": new,
            "previous_run_id": previous_run_id,
            "run_id": run_id,
            "detected_at": now,
        })

    for pid, row in current.items():
        old = previous.get(pid)
        if old is None:
            if previous:  # a first run is not "everything is new"
                slug = row.get("provider_slug")
                if slug and slug not in prev_providers and slug not in seen_new_providers:
                    seen_new_providers.add(slug)
                    event("new_provider", row)
                event("new_plan", row)
            continue

        for field, label in WATCHED.items():
            old_value = (old.get(field) or "").strip()
            new_value = str(row.get(field, "")).strip()
            if old_value == new_value:
                continue
            if field in PRICE_FIELDS:
                a, b = _num(old_value), _num(new_value)
                if a is not None and b is not None:
                    kind = "price_increase" if b > a else "price_decrease"
                    event(kind, row, label, old_value, new_value)
                    continue
            if field in ("data_gb", "daily_data_gb", "total_data_gb"):
                a, b = _num(old_value), _num(new_value)
                if a is not None and b is not None:
                    kind = "data_increase" if b > a else "data_decrease"
                    event(kind, row, label, old_value, new_value)
                    continue
            event("changed", row, label, old_value, new_value)

    for pid, old in previous.items():
        if pid not in current:
            event("discontinued_plan", old)

    return events


def snapshot_previous(out_dir: str) -> str:
    """Where the last run's master file is kept for comparison."""
    return os.path.join(out_dir, "previous", "plans_master.csv")


def rotate_snapshot(out_dir: str) -> None:
    """Copy this run's master file into previous/ ready for the next run."""
    import shutil

    src = os.path.join(out_dir, "plans_master.csv")
    if not os.path.exists(src):
        return
    dst = snapshot_previous(out_dir)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
