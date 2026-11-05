"""Writing the CSVs, the quality report and the run manifest."""

from __future__ import annotations

import csv
import json
import os
from typing import Any, Iterable

from . import schema

# Excel on a Mac reads UTF-8 properly only with a byte-order mark. These files
# are meant to be opened and eyeballed, so the BOM stays.
ENCODING = "utf-8-sig"


def _stringify(value: Any) -> Any:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, separators=(",", ":"), ensure_ascii=False) if value else ""
    if value is None:
        return ""
    return value


def write_csv(path: str, columns: list[str], rows: Iterable[dict]) -> int:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    count = 0
    with open(path, "w", encoding=ENCODING, newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns, extrasaction="ignore",
                                quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({c: _stringify(row.get(c, "")) for c in columns})
            count += 1
    return count


def write_master(out_dir: str, rows: list[dict], strict: bool) -> str:
    path = os.path.join(out_dir, "plans_master.csv")
    write_csv(path, schema.all_columns(strict), rows)
    return path


def write_coverage(out_dir: str, rows: list[dict]) -> str:
    path = os.path.join(out_dir, "plan_coverage.csv")
    write_csv(path, schema.COVERAGE_COLUMNS, rows)
    return path


def write_providers(out_dir: str, rows: list[dict]) -> str:
    path = os.path.join(out_dir, "providers.csv")
    write_csv(path, schema.PROVIDER_COLUMNS, rows)
    return path


def write_changes(out_dir: str, rows: list[dict]) -> str:
    path = os.path.join(out_dir, "change_log.csv")
    write_csv(path, schema.CHANGE_COLUMNS, rows)
    return path


def write_failures(out_dir: str, rows: list[dict]) -> str:
    path = os.path.join(out_dir, "failed_requests.csv")
    write_csv(path, schema.FAILED_COLUMNS, rows)
    return path


# --------------------------------------------------------------------------
# Quality report
# --------------------------------------------------------------------------


def _truthy(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def build_quality_report(rows: list[dict], coverage_rows: list[dict],
                         stats: dict[str, Any]) -> dict[str, Any]:
    def count(pred) -> int:
        return sum(1 for r in rows if pred(r))

    flagged: dict[str, int] = {}
    for r in rows:
        for flag in filter(None, (r.get("qa_flags") or "").split("; ")):
            flagged[flag] = flagged.get(flag, 0) + 1

    duplicate_ids = len(rows) - len({r["plan_id"] for r in rows})

    return {
        "run_id": stats.get("run_id"),
        "generated_at": stats.get("timestamp"),
        "destinations_processed": stats.get("destinations_processed", 0),
        "destinations_failed": stats.get("destinations_failed", 0),
        "destinations_available": stats.get("destinations_available", 0),
        "regions_processed": stats.get("regions_processed", 0),
        "regions_failed": stats.get("regions_failed", 0),
        "raw_plans_retrieved": stats.get("raw_plan_count", 0),
        "unique_plans": len(rows),
        "duplicate_plans_collapsed": stats.get("duplicate_count", 0),
        "duplicate_plan_ids_in_output": duplicate_ids,
        "plans_without_native_id": stats.get("fallback_key_count", 0),
        "coverage_rows": len(coverage_rows),
        "providers": stats.get("provider_count", 0),
        "plans_with_prices": count(lambda r: r["price"] != ""),
        "plans_with_gbp_price": count(lambda r: r["price_gbp"] != ""),
        "plans_with_5g": count(lambda r: _truthy(r["has_5g"])),
        "plans_with_tethering": count(lambda r: _truthy(r["tethering"])),
        "plans_with_voice": count(lambda r: r["telephony"] not in ("none", "")),
        "plans_with_sms": count(lambda r: r["sms"] not in ("none", "")),
        "plans_with_phone_number": count(lambda r: _truthy(r["phone_number"])),
        "plans_with_uk_number": count(lambda r: r.get("dialing_code") == "+44"),
        "unlimited_plans": count(lambda r: _truthy(r["unlimited"])),
        "unlimited_with_daily_cap": count(
            lambda r: _truthy(r["unlimited"]) and r["daily_data_gb"] != ""),
        "plans_with_explicit_throttle_speed": count(lambda r: r["throttle_speed"] != ""),
        "plans_possibly_throttled": count(lambda r: _truthy(r["possible_throttling"])),
        "subscription_plans": count(lambda r: _truthy(r["subscription"])),
        "pay_as_you_go_plans": count(lambda r: _truthy(r["pay_as_you_go"])),
        "promotional_plans": count(lambda r: _truthy(r["promo_enabled"])),
        "uk_inbound_plans": count(lambda r: _truthy(r["uk_inbound"])),
        "uk_outbound_plans": count(lambda r: _truthy(r["uk_outbound"])),
        "uk_relevant_plans": count(lambda r: _truthy(r["uk_traveller_relevant"])),
        "single_country_plans": count(lambda r: r["plan_type"] == "single_country"),
        "regional_plans": count(lambda r: r["plan_type"] == "regional"),
        "multi_country_plans": count(lambda r: r["plan_type"] == "multi_country"),
        "global_plans": count(lambda r: r["plan_type"] == "global"),
        "unknown_plan_type": count(lambda r: r["plan_type"] == "unknown"),
        "rows_with_quality_flags": count(lambda r: bool(r.get("qa_flags"))),
        "quality_flag_breakdown": dict(sorted(flagged.items(), key=lambda kv: -kv[1])),
        "queued_for_verification": count(lambda r: _truthy(r.get("needs_verification"))),
        "requests_made": stats.get("request_count", 0),
        "megabytes_downloaded": round(stats.get("bytes_downloaded", 0) / 1_048_576, 1),
        "schema_version": stats.get("schema_version"),
        "source_endpoint": stats.get("source_endpoint"),
        "locale": stats.get("locale"),
        "esimdb_latest_update": stats.get("esimdb_latest_update"),
    }


def write_quality_report(out_dir: str, report: dict[str, Any]) -> tuple[str, str]:
    json_path = os.path.join(out_dir, "data_quality_report.json")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)

    txt_path = os.path.join(out_dir, "data_quality_report.txt")
    with open(txt_path, "w", encoding=ENCODING) as fh:
        fh.write(render_report(report))
    return json_path, txt_path


LABELS = {
    "destinations_processed": "Destinations we got data for",
    "destinations_failed": "Destinations that failed",
    "destinations_available": "Destinations eSIMDB lists",
    "regions_processed": "Regions we got data for",
    "regions_failed": "Regions that failed",
    "raw_plans_retrieved": "Plan records seen (before removing repeats)",
    "unique_plans": "Unique plans kept",
    "duplicate_plans_collapsed": "Repeats collapsed",
    "duplicate_plan_ids_in_output": "Duplicate IDs left in the file (should be 0)",
    "plans_without_native_id": "Plans with no eSIMDB ID (fallback key used)",
    "coverage_rows": "Rows in the plan-to-country file",
    "providers": "Providers",
    "plans_with_prices": "Plans with a price",
    "plans_with_gbp_price": "Plans priced in pounds",
    "plans_with_5g": "Plans with 5G",
    "plans_with_tethering": "Plans that allow hotspot",
    "plans_with_voice": "Plans with real phone calls",
    "plans_with_sms": "Plans with real text messages",
    "plans_with_phone_number": "Plans that come with a phone number",
    "plans_with_uk_number": "Plans with a +44 number",
    "unlimited_plans": "Plans sold as unlimited",
    "unlimited_with_daily_cap": "...of those, ones with a stated daily allowance",
    "plans_with_explicit_throttle_speed": "Plans stating the slowed speed",
    "plans_possibly_throttled": "Plans that may be slowed",
    "subscription_plans": "Subscriptions",
    "pay_as_you_go_plans": "Pay as you go",
    "promotional_plans": "Plans with a discount running",
    "uk_inbound_plans": "Plans that work in the UK",
    "uk_outbound_plans": "Plans for leaving the UK",
    "uk_relevant_plans": "Plans useful to a UK traveller",
    "single_country_plans": "One-country plans",
    "regional_plans": "Regional plans",
    "multi_country_plans": "Multi-country plans",
    "global_plans": "Global plans",
    "unknown_plan_type": "Plans we could not classify",
    "rows_with_quality_flags": "Rows with something worth checking",
    "queued_for_verification": "Rows queued for checking against the provider",
    "requests_made": "Requests made to eSIMDB",
    "megabytes_downloaded": "Megabytes downloaded",
}

ORDER = list(LABELS.keys())


def render_report(report: dict[str, Any]) -> str:
    lines = [
        "eSIM Sorted - eSIMDB ingestion report",
        "=" * 44,
        f"Run:      {report.get('run_id')}",
        f"Finished: {report.get('generated_at')}",
        f"Source:   {report.get('source_endpoint')} (locale {report.get('locale')})",
        f"eSIMDB last updated its data: {report.get('esimdb_latest_update') or 'not stated'}",
        "",
    ]
    width = max(len(v) for v in LABELS.values()) + 2
    for key in ORDER:
        if key in report:
            lines.append(f"{LABELS[key]:<{width}}{report[key]}")

    breakdown = report.get("quality_flag_breakdown") or {}
    if breakdown:
        lines += ["", "What got flagged, and how often:"]
        for flag, n in breakdown.items():
            lines.append(f"  {n:>7}  {flag}")

    failed = report.get("destinations_failed", 0) + report.get("regions_failed", 0)
    lines += ["", "-" * 44]
    if failed:
        lines.append(
            f"Not complete: {failed} request(s) failed. See failed_requests.csv, "
            "then run again with --resume to retry only those."
        )
    else:
        lines.append(
            "Every destination and region eSIMDB lists was fetched successfully."
        )
    return "\n".join(lines) + "\n"


def write_manifest(out_dir: str, manifest: dict[str, Any]) -> str:
    path = os.path.join(out_dir, "run_manifest.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
    return path
