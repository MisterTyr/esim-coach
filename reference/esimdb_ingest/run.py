"""Run the ingestion.

    python -m esimdb_ingest.run --out data

Common variations:

    --limit-countries 5     small trial run before committing to the full one
    --only uk,japan,france  just these destinations
    --resume                keep what's already downloaded, retry the rest
    --from-cache            rebuild the CSVs from the saved raw JSON, no requests
    --strict-schema         emit only the 57 columns from the master schema
"""

from __future__ import annotations

import argparse
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

import os

from . import build, changes, links, outputs, verify
from .config import (BASE_URL, EP_COUNTRIES, EP_COUNTRY_PLANS, EP_PROVIDERS,
                     EP_REGION_PLANS, EP_REGIONS, SCHEMA_VERSION, Settings)
from .fetch import Blocked, Checkpoint, FetchError, Fetcher


def log(message: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}", flush=True)


def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Pull eSIMDB into the eSIM Sorted dataset.")
    p.add_argument("--out", default="data", help="output folder (default: data)")
    p.add_argument("--locale", default="en")
    p.add_argument("--concurrency", type=int, default=1,
                   help="parallel requests (default: 1 - do not raise this)")
    p.add_argument("--delay", type=float, default=4.0,
                   help="seconds between requests (default: 4.0)")
    p.add_argument("--limit-countries", type=int, default=0,
                   help="only the N most popular destinations, for a trial run")
    p.add_argument("--only", default="",
                   help="comma-separated destination slugs, e.g. uk,japan")
    p.add_argument("--skip-regions", action="store_true",
                   help="skip the region calls (you lose multi-country coverage)")
    p.add_argument("--resume", action="store_true",
                   help="keep already-downloaded responses and fetch the rest")
    p.add_argument("--from-cache", action="store_true",
                   help="rebuild outputs from saved raw JSON without any requests")
    p.add_argument("--strict-schema", action="store_true")
    p.add_argument("--no-raw", action="store_true", help="do not keep raw JSON")
    return p.parse_args(argv)


def settings_from_args(a: argparse.Namespace) -> Settings:
    return Settings(
        out_dir=a.out,
        locale=a.locale,
        concurrency=max(1, a.concurrency),
        delay_seconds=max(0.0, a.delay),
        limit_countries=a.limit_countries,
        only_countries=[s.strip() for s in a.only.split(",") if s.strip()],
        skip_regions=a.skip_regions,
        strict_schema=a.strict_schema,
        keep_raw=not a.no_raw,
    )


def main(argv=None) -> int:
    # Disabled 2026-11-05. eSIMDB's terms forbid scraping and using their plan
    # database for a competing product. This code is kept for reference only:
    # its parsing, change detection and verification logic are reused by our
    # own collectors. Do not re-enable it without eSIMDB's written permission.
    raise SystemExit("Disabled: eSIMDB's terms forbid scraping. See reference/README.md.")
    args = parse_args(argv)
    s = settings_from_args(args)

    run_id = f"run_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:6]}"
    started = time.time()
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    fetcher = Fetcher(s)
    checkpoint = Checkpoint(s.state_path)
    checkpoint.start_run(run_id, fresh=not (args.resume or args.from_cache))
    use_cache = args.from_cache or args.resume
    offline = args.from_cache

    links_path = os.path.join(s.out_dir, links.FILENAME)
    our_links = links.load(links_path)
    approved = sum(1 for v in our_links.values() if links.is_approved(v))
    log("Provider links: %d rows, %d approved affiliate programmes."
        % (len(our_links), approved))

    verified = verify.load(os.path.join(s.out_dir, verify.FILENAME))
    if verified:
        log("Provider checks on file: %d rows." % len(verified))

    dataset = build.Dataset(run_id, timestamp, links=our_links,
                            verified=verified)
    stats = {
        "run_id": run_id,
        "timestamp": timestamp,
        "schema_version": SCHEMA_VERSION,
        "source_endpoint": BASE_URL + "/api/client",
        "locale": s.locale,
    }

    try:
        log("Fetching the destination, region and provider lists.")
        countries = fetcher.get_json(EP_COUNTRIES.format(locale=s.locale),
                                     "reference/countries", use_cache)
        regions = fetcher.get_json(EP_REGIONS.format(locale=s.locale),
                                   "reference/regions", use_cache)
        providers = fetcher.get_json(EP_PROVIDERS.format(locale=s.locale),
                                     "reference/providers", use_cache)
        dataset.load_reference(countries, regions, providers)
        log(f"eSIMDB lists {len(countries)} destinations, {len(regions)} regions, "
            f"{len(providers)} providers.")

        targets = select_countries(countries, s)
        stats["destinations_available"] = len(countries)

        # Regions first: they carry the coverage lists, and having them in
        # hand means single-country plans are correctly identified as such.
        region_failures = 0
        if not s.skip_regions:
            log(f"Fetching {len(regions)} regions (these carry the coverage lists).")
            region_failures = fetch_group(
                fetcher, checkpoint, dataset, s, use_cache,
                [(r["slug"], EP_REGION_PLANS.format(slug=r["slug"], locale=s.locale),
                  f"regions/{r['slug']}", None, None) for r in regions if r.get("slug")],
                kind="region", offline=offline)
        stats["regions_processed"] = (0 if s.skip_regions else len(regions)) - region_failures
        stats["regions_failed"] = region_failures

        log(f"Fetching {len(targets)} destinations.")
        country_failures = fetch_group(
            fetcher, checkpoint, dataset, s, use_cache,
            [(c["slug"], EP_COUNTRY_PLANS.format(slug=c["slug"], locale=s.locale),
              f"countries/{c['slug']}", c.get("code") or c.get("_id"), c["slug"])
             for c in targets if c.get("slug")],
            kind="country", offline=offline)
        stats["destinations_processed"] = len(targets) - country_failures
        stats["destinations_failed"] = country_failures

    except Blocked as exc:
        log(f"STOPPED: {exc}")
        log("Writing out what was gathered before the stop, so the run is not "
            "wasted. The raw responses are kept too - resume with --resume.")
        blocked = True
        stats.setdefault("destinations_processed", 0)
        stats.setdefault("destinations_failed", 0)
        stats.setdefault("regions_processed", 0)
        stats.setdefault("regions_failed", 0)
    else:
        blocked = False

    # ---- build -------------------------------------------------------

    log("Building the master records.")
    rows = dataset.build_rows()
    coverage_rows = dataset.build_coverage_rows(rows)
    provider_rows = dataset.build_provider_rows()

    # Keep provider_links.csv in step with the provider list. Anything
    # already filled in is preserved; new providers arrive as blank rows.
    added = links.write_scaffold(links_path, provider_rows, our_links)
    if added != len(our_links):
        log("provider_links.csv now has %d rows (was %d)." % (added, len(our_links)))

    stats.update({
        "raw_plan_count": dataset.raw_plan_count,
        "duplicate_count": dataset.duplicate_count,
        "fallback_key_count": dataset.fallback_key_count,
        "provider_count": len(provider_rows),
        "request_count": fetcher.request_count,
        "bytes_downloaded": fetcher.bytes_downloaded,
        "esimdb_latest_update": dataset.latest_update,
    })

    log("Comparing with the previous run.")
    previous = changes.read_previous(changes.snapshot_previous(s.out_dir))
    change_rows = changes.diff(previous, rows, run_id)

    log("Writing files.")
    master_path = outputs.write_master(s.out_dir, rows, s.strict_schema)
    outputs.write_coverage(s.out_dir, coverage_rows)
    outputs.write_providers(s.out_dir, provider_rows)
    outputs.write_changes(s.out_dir, change_rows)
    outputs.write_failures(s.out_dir, [
        dict(f, run_id=run_id, detected_at=timestamp) for f in fetcher.failures])

    report = outputs.build_quality_report(rows, coverage_rows, stats)
    report["change_events"] = len(change_rows)
    outputs.write_quality_report(s.out_dir, report)

    outputs.write_manifest(s.out_dir, {
        "run_id": run_id,
        "started_utc": datetime.fromtimestamp(started, timezone.utc).isoformat(timespec="seconds"),
        "finished_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "duration_seconds": round(time.time() - started, 1),
        "source_endpoint": stats["source_endpoint"],
        "locale": s.locale,
        "schema_version": SCHEMA_VERSION,
        "destinations_available": stats.get("destinations_available", 0),
        "destinations_processed": stats.get("destinations_processed", 0),
        "destinations_failed": stats.get("destinations_failed", 0),
        "regions_processed": stats.get("regions_processed", 0),
        "regions_failed": stats.get("regions_failed", 0),
        "requests_made": fetcher.request_count,
        "bytes_downloaded": fetcher.bytes_downloaded,
        "raw_records": dataset.raw_plan_count,
        "unique_records": len(rows),
        "change_events": len(change_rows),
        "blocked_by_source": blocked,
        "complete": not blocked and stats.get("destinations_failed", 0) == 0
                    and stats.get("regions_failed", 0) == 0
                    and not s.only_countries and not s.limit_countries,
    })

    # Only rotate the snapshot when the run actually covered everything,
    # otherwise the next run would report a partial dataset as discontinuations.
    if (not blocked and stats.get("destinations_failed", 0) == 0
            and not s.only_countries and not s.limit_countries):
        changes.rotate_snapshot(s.out_dir)
    else:
        log("Partial run - not rotating the comparison snapshot.")

    print()
    print(outputs.render_report(report))
    log(f"Done in {round(time.time() - started)}s. Master file: {master_path}")
    return 0


def select_countries(countries: list[dict], s: Settings) -> list[dict]:
    if s.only_countries:
        wanted = set(s.only_countries)
        return [c for c in countries if c.get("slug") in wanted]
    ordered = sorted(countries, key=lambda c: -(c.get("popularity") or 0))
    return ordered[: s.limit_countries] if s.limit_countries else ordered


def fetch_group(fetcher, checkpoint, dataset, s, use_cache, jobs, kind: str,
                offline: bool = False) -> int:
    """Fetch a batch of endpoints and feed the plans into the dataset."""
    failures = 0
    done = 0
    total = len(jobs)

    def work(job):
        slug, path, key, country_code, country_slug = job
        cached = fetcher.read_raw(key) if use_cache else None
        if cached is not None:
            return job, cached, None
        if offline:
            return job, None, FetchError(
                BASE_URL + path, "not in the local cache (--from-cache makes no requests)")
        try:
            return job, fetcher.get_json(path, key, use_cache), None
        except FetchError as exc:
            return job, None, exc

    # Batched on purpose. Some destination responses are 50MB once parsed,
    # so results are consumed and released rather than piling up in memory.
    batch_size = max(4, s.concurrency * 4)
    with ThreadPoolExecutor(max_workers=s.concurrency) as pool:
        for start in range(0, total, batch_size):
            batch = jobs[start:start + batch_size]
            futures = [pool.submit(work, job) for job in batch]
            for future in as_completed(futures):
                job, payload, error = future.result()
                slug, path, key, country_code, country_slug = job
                done += 1

                if error is not None:
                    failures += 1
                    checkpoint.mark(key, ok=False)
                    fetcher.record_failure(kind, key, BASE_URL + path, str(error))
                    log(f"  ({done}/{total}) {kind} {slug}: FAILED - {error}")
                    continue

                plans = (payload or {}).get("plans") or []
                dataset.add_plans(plans, source=kind, country_code=country_code,
                                  country_slug=country_slug)
                if payload.get("providers"):
                    dataset.merge_provider_detail(payload["providers"])
                if payload.get("latestUpdate"):
                    dataset.latest_update = payload["latestUpdate"]
                checkpoint.mark(key, ok=True)
                del payload
                if done % 10 == 0 or done == total:
                    log(f"  ({done}/{total}) {kind}s done, "
                        f"{len(dataset.plans)} unique plans so far")
            futures.clear()

    return failures


def write_failures_only(s: Settings, fetcher: Fetcher, run_id: str) -> None:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    outputs.write_failures(s.out_dir, [
        dict(f, run_id=run_id, detected_at=ts) for f in fetcher.failures])


if __name__ == "__main__":
    sys.exit(main())
