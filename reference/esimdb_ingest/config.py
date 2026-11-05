"""Settings for the eSIMDB ingestion run.

Everything you'd reasonably want to change lives here. The command line
can override most of it - see run.py --help.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

BASE_URL = "https://esimdb.com"

# Endpoints confirmed live on 2026-09-06.
EP_COUNTRIES = "/api/client/countries?locale={locale}"
EP_REGIONS = "/api/client/regions?locale={locale}"
EP_PROVIDERS = "/api/client/providers?locale={locale}"
EP_COUNTRY_PLANS = "/api/client/countries/{slug}/data-plans?locale={locale}"
EP_REGION_PLANS = "/api/client/regions/{slug}/data-plans?locale={locale}"

SCHEMA_VERSION = "1.0.0"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


@dataclass
class Settings:
    out_dir: str = "data"
    locale: str = "en"

    # Politeness. eSIMDB started returning 403 at roughly one request a
    # second on 6 Sep 2026, so the defaults are now one worker and a four
    # second gap. That is about 20 minutes for a full run. Going faster is
    # how you get blocked.
    concurrency: int = 1
    delay_seconds: float = 4.0
    timeout_seconds: int = 120

    max_retries: int = 5
    backoff_base: float = 2.0
    backoff_cap: float = 60.0

    # Stop the whole run rather than grind on if the site starts refusing us.
    abort_after_consecutive_failures: int = 8

    # Keep the raw JSON. It is the only way to re-derive fields later
    # without re-fetching, and it is what change detection compares against.
    keep_raw: bool = True
    raw_gzip: bool = True

    # Emit only the 57 columns from the master schema, dropping the extra
    # diagnostic columns. Off by default because the extras are useful.
    strict_schema: bool = False

    # Testing / partial runs.
    limit_countries: int = 0  # 0 means all
    only_countries: list[str] = field(default_factory=list)  # slugs
    skip_regions: bool = False

    @property
    def raw_dir(self) -> str:
        return os.path.join(self.out_dir, "raw")

    @property
    def state_path(self) -> str:
        return os.path.join(self.out_dir, "checkpoint.json")
