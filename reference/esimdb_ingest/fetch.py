"""HTTP layer: polite fetching, retries, checkpoints, raw archiving.

Rules this file enforces:
  - one request at a time per worker, with a delay between them
  - exponential backoff with jitter on 429 and 5xx
  - if the site starts consistently refusing us, stop the run rather than
    keep hammering (see Settings.abort_after_consecutive_failures)
  - every successful response is written to disk before it is parsed, so a
    crashed run can be resumed without re-downloading
"""

from __future__ import annotations

import gzip
import json
import os
import random
import threading
import time
from typing import Any

import requests

from .config import BASE_URL, USER_AGENT, Settings


def _decompress_if_needed(body: bytes, content_encoding: str | None) -> bytes:
    """A safety net. requests unpacks gzip and deflate itself, but if a server
    sends brotli or zstd anyway, unpack it here rather than failing on bytes
    that are not text."""
    encoding = (content_encoding or "").strip().lower()
    if encoding in ("", "gzip", "deflate", "identity"):
        return body
    if encoding == "br":
        for module in ("brotli", "brotlicffi"):
            try:
                return __import__(module).decompress(body)
            except ImportError:
                continue
            except Exception:
                return body
        return body
    if encoding == "zstd":
        try:
            import zstandard

            return zstandard.ZstdDecompressor().decompress(body)
        except Exception:
            return body
    return body


class Blocked(Exception):
    """Raised when eSIMDB looks like it is deliberately refusing us."""


class FetchError(Exception):
    def __init__(self, url: str, reason: str, status: int | None = None):
        super().__init__(f"{url}: {reason}")
        self.url = url
        self.reason = reason
        self.status = status


class Fetcher:
    def __init__(self, settings: Settings):
        self.s = settings
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-GB,en;q=0.9",
                # Only what requests can decompress on its own. Asking for
                # brotli gets you raw compressed bytes unless the brotli
                # package is installed, and it usually is not.
                "Accept-Encoding": "gzip, deflate",
                "Referer": BASE_URL + "/",
            }
        )
        self._lock = threading.Lock()
        self._last_request = 0.0
        self._consecutive_failures = 0
        self.failures: list[dict[str, Any]] = []
        self.request_count = 0
        self.bytes_downloaded = 0
        os.makedirs(self.s.raw_dir, exist_ok=True)

    # -- pacing ---------------------------------------------------------

    def _wait_turn(self) -> None:
        with self._lock:
            gap = time.monotonic() - self._last_request
            if gap < self.s.delay_seconds:
                time.sleep(self.s.delay_seconds - gap)
            self._last_request = time.monotonic()

    # -- raw archive ----------------------------------------------------

    def raw_path(self, key: str) -> str:
        ext = ".json.gz" if self.s.raw_gzip else ".json"
        return os.path.join(self.s.raw_dir, key + ext)

    def _write_raw(self, key: str, payload: bytes) -> None:
        if not self.s.keep_raw:
            return
        path = self.raw_path(key)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".part"
        if self.s.raw_gzip:
            with gzip.open(tmp, "wb") as fh:
                fh.write(payload)
        else:
            with open(tmp, "wb") as fh:
                fh.write(payload)
        os.replace(tmp, path)

    def read_raw(self, key: str) -> Any | None:
        path = self.raw_path(key)
        if not os.path.exists(path):
            return None
        try:
            opener = gzip.open if self.s.raw_gzip else open
            with opener(path, "rb") as fh:
                return json.loads(fh.read().decode("utf-8"))
        except Exception:
            return None

    # -- the fetch ------------------------------------------------------

    def get_json(self, path: str, key: str, use_cache: bool = False) -> Any:
        """Fetch one endpoint. `key` names the raw archive file."""
        if use_cache:
            cached = self.read_raw(key)
            if cached is not None:
                return cached

        url = BASE_URL + path
        attempt = 0
        while True:
            attempt += 1
            self._wait_turn()
            try:
                resp = self.session.get(url, timeout=self.s.timeout_seconds)
                self.request_count += 1
                status = resp.status_code

                if status == 200:
                    body = resp.content
                    self.bytes_downloaded += len(body)
                    body = _decompress_if_needed(body, resp.headers.get("Content-Encoding"))
                    try:
                        data = json.loads(body.decode("utf-8"))
                    except Exception as exc:
                        encoding = resp.headers.get("Content-Encoding", "none")
                        raise FetchError(
                            url,
                            f"response was not JSON (content-encoding: {encoding}): {exc}",
                            status)
                    self._write_raw(key, body)
                    with self._lock:
                        self._consecutive_failures = 0
                    return data

                if status in (401, 403) or (
                    status == 200 and "captcha" in resp.text[:500].lower()
                ):
                    # A deliberate refusal. Do not try to work around it.
                    raise Blocked(
                        f"eSIMDB returned {status} for {url}. Stopping the run - "
                        "ask them for API access rather than pushing harder."
                    )

                if status == 404:
                    raise FetchError(url, "not found (404)", status)

                if status == 429 or 500 <= status < 600:
                    if attempt > self.s.max_retries:
                        raise FetchError(
                            url, f"gave up after {attempt - 1} retries (HTTP {status})", status
                        )
                    self._sleep_backoff(attempt, resp.headers.get("Retry-After"))
                    continue

                raise FetchError(url, f"unexpected HTTP {status}", status)

            except (requests.Timeout, requests.ConnectionError) as exc:
                if attempt > self.s.max_retries:
                    raise FetchError(url, f"network error after retries: {exc}")
                self._sleep_backoff(attempt, None)
                continue

    def _sleep_backoff(self, attempt: int, retry_after: str | None) -> None:
        if retry_after:
            try:
                time.sleep(min(float(retry_after), self.s.backoff_cap))
                return
            except ValueError:
                pass
        delay = min(self.s.backoff_base ** attempt, self.s.backoff_cap)
        time.sleep(delay + random.uniform(0, 1.0))

    def record_failure(self, kind: str, key: str, url: str, reason: str) -> None:
        self.failures.append(
            {"kind": kind, "key": key, "url": url, "reason": reason}
        )
        with self._lock:
            self._consecutive_failures += 1
            n = self._consecutive_failures
        if n >= self.s.abort_after_consecutive_failures:
            raise Blocked(
                f"{n} requests failed in a row. Stopping so we do not keep "
                "hammering eSIMDB. Check the failed-requests CSV, wait, then "
                "resume - the run picks up from the checkpoint."
            )


class Checkpoint:
    """Records which destinations have been fetched, so a run can resume."""

    def __init__(self, path: str):
        self.path = path
        self._lock = threading.Lock()
        self.data: dict[str, Any] = {"run_id": None, "done": [], "failed": []}
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as fh:
                    self.data = json.load(fh)
            except Exception:
                pass

    @property
    def done(self) -> set[str]:
        return set(self.data.get("done", []))

    def mark(self, key: str, ok: bool = True) -> None:
        with self._lock:
            bucket = "done" if ok else "failed"
            if key not in self.data.setdefault(bucket, []):
                self.data[bucket].append(key)
            self._save()

    def start_run(self, run_id: str, fresh: bool) -> None:
        with self._lock:
            if fresh or self.data.get("run_id") != run_id:
                self.data = {"run_id": run_id, "done": [], "failed": []}
            self._save()

    def clear(self) -> None:
        with self._lock:
            self.data = {"run_id": None, "done": [], "failed": []}
            if os.path.exists(self.path):
                os.remove(self.path)

    def _save(self) -> None:
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        tmp = self.path + ".part"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(self.data, fh)
        os.replace(tmp, self.path)
