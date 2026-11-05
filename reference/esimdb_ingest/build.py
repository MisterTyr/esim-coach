"""Assembling the master dataset from the raw eSIMDB responses.

The shape of the problem:

  - The country endpoint returns every plan that works in that country, but
    does not say what else the plan covers.
  - The region endpoint returns only multi-country plans, and those do carry
    a `coverages` list of ISO2 codes.

So coverage is built from both. A plan seen in region responses gets its
real coverage list. A plan only ever seen on one country's page is a
single-country plan and its coverage is that country. Either way the plan is
stored once, and the country relationship lives in the coverage table.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from . import links as provider_links
from . import parse
from . import verify as provider_verify
from .config import BASE_URL


class Dataset:
    def __init__(self, run_id: str, timestamp: str,
                 links: dict[str, dict] | None = None,
                 verified: dict | None = None):
        self.run_id = run_id
        self.timestamp = timestamp
        # Our own provider links, keyed on provider_slug. See links.py.
        self.links = links or {}
        # What we checked on provider sites. See verify.py.
        self.verified: dict[tuple[str, str], dict] = verified or {}

        self.countries: dict[str, dict] = {}       # ISO2 -> country record
        self.country_by_slug: dict[str, dict] = {}
        self.regions: dict[str, dict] = {}         # slug -> region record
        self.providers: dict[str, dict] = {}       # provider id -> record

        self.plans: dict[str, dict] = {}           # plan_id -> raw plan
        self.plan_coverage: dict[str, set[str]] = defaultdict(set)
        self.coverage_source: dict[str, str] = {}  # plan_id -> region | country
        self.first_seen: dict[str, str] = {}       # plan_id -> country slug

        self.latest_update = ""
        self.raw_plan_count = 0
        self.duplicate_count = 0
        self.fallback_key_count = 0
        self._fallback_keys: dict[str, str] = {}

    # -- reference data -------------------------------------------------

    def load_reference(self, countries: list, regions: list, providers: list) -> None:
        for c in countries:
            code = c.get("code") or c.get("_id")
            if not code:
                continue
            self.countries[code] = c
            if c.get("slug"):
                self.country_by_slug[c["slug"]] = c
        for r in regions:
            if r.get("slug"):
                self.regions[r["slug"]] = r
        for p in providers:
            if p.get("_id"):
                self.providers[p["_id"]] = dict(p)

    def merge_provider_detail(self, provider_map: dict[str, dict]) -> None:
        """Country responses carry a fuller provider object than /providers."""
        for pid, detail in (provider_map or {}).items():
            existing = self.providers.setdefault(pid, {"_id": pid})
            for key, value in detail.items():
                if value is not None or key not in existing:
                    existing[key] = value

    # -- plan ingestion -------------------------------------------------

    def _plan_key(self, plan: dict) -> str:
        """eSIMDB's _id is the identifier. The fallback is only for records
        that somehow arrive without one - it is never used to merge two plans
        that both have IDs."""
        pid = plan.get("_id")
        if pid:
            return str(pid)
        signature = "|".join(
            str(x)
            for x in (
                plan.get("provider"),
                parse.clean_name(plan.get("name")),
                sorted(plan.get("coverages") or []),
                plan.get("capacity"),
                plan.get("period"),
                sorted((plan.get("prices") or {}).items()),
            )
        )
        if signature not in self._fallback_keys:
            self._fallback_keys[signature] = f"fallback:{len(self._fallback_keys):06d}"
            self.fallback_key_count += 1
        return self._fallback_keys[signature]

    def add_plans(self, plans: list[dict], *, source: str, country_code: str | None,
                  country_slug: str | None) -> None:
        for plan in plans or []:
            self.raw_plan_count += 1
            key = self._plan_key(plan)

            if key in self.plans:
                self.duplicate_count += 1
                # Prefer the record that carries coverages.
                if plan.get("coverages") and not self.plans[key].get("coverages"):
                    self.plans[key] = plan
            else:
                self.plans[key] = plan
            if country_slug and key not in self.first_seen:
                self.first_seen[key] = country_slug

            coverages = plan.get("coverages")
            if coverages:
                self.plan_coverage[key].update(coverages)
                self.coverage_source[key] = "region_endpoint"
            elif country_code:
                self.plan_coverage[key].add(country_code)
                self.coverage_source.setdefault(key, "country_endpoint")

    # -- derivation -----------------------------------------------------

    def regions_for(self, coverage: list[str]) -> list[str]:
        """Which eSIMDB regions a coverage list touches. A plan can belong to
        several, and all of them are kept."""
        hit: set[str] = set()
        codes = set(coverage)
        for slug, region in self.regions.items():
            region_codes = {c.get("code") for c in (region.get("countries") or [])}
            if region_codes and codes & region_codes:
                hit.add(slug)
        # eSIMDB's own top-level region label on each country, as a backstop.
        for code in codes:
            c = self.countries.get(code)
            if c and c.get("region"):
                hit.add(c["region"])
        return sorted(hit)

    def continents_for(self, coverage: list[str]) -> set[str]:
        """The broad continental bucket eSIMDB puts each country in. Used for
        classification, because the region slugs overlap heavily - a plain
        Europe plan sits in europe, nordic, scandinavia, baltic and balkans at
        once, which would otherwise make it look global."""
        return {
            self.countries[c]["region"]
            for c in coverage
            if c in self.countries and self.countries[c].get("region")
        }

    def _landing_slug(self, coverage: list[str], first_seen: str) -> str:
        """Which eSIMDB destination page to point at. The UK page wins for
        anything that covers the UK - that is the page a UK reader wants."""
        if "GB" in coverage:
            gb = self.countries.get("GB", {}).get("slug")
            if gb:
                return gb
        if first_seen:
            return first_seen
        for code in coverage:
            slug = self.countries.get(code, {}).get("slug")
            if slug:
                return slug
        return ""

    def provider_of(self, plan: dict) -> dict:
        return self.providers.get(plan.get("provider"), {})

    def build_rows(self) -> list[dict[str, Any]]:
        rows = []
        for plan_id, plan in self.plans.items():
            rows.append(self._build_row(plan_id, plan))
        rows.sort(key=lambda r: (r["provider"].lower(), r["plan_name"].lower(), r["plan_id"]))
        return rows

    def _build_row(self, plan_id: str, plan: dict) -> dict[str, Any]:
        provider = self.provider_of(plan)
        coverage = sorted(self.plan_coverage.get(plan_id, set()))
        covered_regions = self.regions_for(coverage)
        continents = self.continents_for(coverage)

        allowance = parse.parse_allowance(plan)
        telephony = parse.parse_telephony(plan)
        validity = parse.parse_validity(plan)
        billable = allowance["total_data_gb"] or allowance["data_gb"]
        pricing = parse.parse_pricing(plan, None if allowance["unlimited"] else billable)

        plan_type = parse.classify_plan_type(coverage, continents)
        uk_inbound = "GB" in coverage
        uk_outbound = any(code != "GB" for code in coverage)

        country_slug = self.first_seen.get(plan_id, "")
        provider_slug = provider.get("slug", "")
        esimdb_url = ""
        if provider_slug:
            landing = self._landing_slug(coverage, country_slug)
            esimdb_url = (f"{BASE_URL}/{landing}/{provider_slug}" if landing
                          else f"{BASE_URL}/provider/{provider_slug}")

        # Our link, never eSIMDB's - theirs carries their affiliate ID.
        link = self.links.get(provider_slug, {})
        our_url, link_type = provider_links.product_url(link)

        throttle = parse.kbps_label(plan.get("reducedSpeed"))
        possible_throttling = bool(plan.get("possibleThrottling")) or bool(throttle)

        row: dict[str, Any] = {
            # original schema
            "provider": provider.get("name", ""),
            "plan_name": parse.clean_name(plan.get("name")),
            "region": "|".join(sorted(continents)),
            "country": ",".join(coverage),
            "data_gb": allowance["data_gb"] if allowance["data_gb"] is not None else "",
            "validity_days": validity["validity_days"],
            "price": pricing["price"],
            "product_url": our_url,
            "timestamp": self.timestamp,
            # identifiers
            "plan_id": plan_id,
            "provider_slug": provider_slug,
            "provider_verified": parse.tri_bool(provider.get("certified")),
            "plan_type": plan_type,
            "coverage_countries": ",".join(coverage),
            "coverage_regions": "|".join(covered_regions),
            # data
            "daily_data_gb": allowance["daily_data_gb"] if allowance["daily_data_gb"] is not None else "",
            "total_data_gb": allowance["total_data_gb"] if allowance["total_data_gb"] is not None else "",
            "unlimited": "true" if allowance["unlimited"] else "false",
            "throttle_speed": throttle,
            "validity_info": validity["validity_info"],
            # pricing
            "currency": pricing["currency"],
            "price_usd": pricing["price_usd"],
            "price_gbp": pricing["price_gbp"],
            "price_eur": pricing["price_eur"],
            "price_local": "",           # see README: no destination-currency field in source
            "price_per_gb": pricing["price_per_gb"],
            "promo_enabled": pricing["promo_enabled"],
            "promo_price_usd": pricing["promo_price_usd"],
            "promo_price_gbp": pricing["promo_price_gbp"],
            "promo_price_eur": pricing["promo_price_eur"],
            "promo_price_local": "",
            "promo_code": pricing["promo_code"] or (provider.get("promoCode") or ""),
            "new_user_only": pricing["new_user_only"],
            "subscription": parse.tri_bool(plan.get("subscription")),
            "pay_as_you_go": parse.tri_bool(plan.get("payAsYouGo")),
            # network
            "has_5g": parse.tri_bool(plan.get("has5G")),
            "network_types": "5G" if plan.get("has5G") else "",
            "low_latency": parse.tri_bool(plan.get("isLowLatency")),
            "tethering": parse.tri_bool(plan.get("tethering")),
            # voice
            "telephony": telephony["telephony"],
            "sms": telephony["sms"],
            "phone_number": telephony["phone_number"],
            "phone_number_country": telephony["phone_number_country"],
            # not carried by the source - left blank on purpose
            "networks": "",
            "activation_policy": "",
            "kyc_required": parse.tri_bool(plan.get("eKYC")),
            "can_top_up": parse.tri_bool(plan.get("canTopUp")),
            "possible_throttling": "true" if possible_throttling else "false",
            "fair_use_policy": "",
            "device_compatibility": "",
            "provider_url": link.get("provider_url", ""),
            "esimdb_url": esimdb_url,
            # UK
            "uk_inbound": "true" if uk_inbound else "false",
            "uk_outbound": "true" if uk_outbound else "false",
            "uk_traveller_relevant": "true" if (uk_inbound or uk_outbound) else "false",
            "source": "esimdb_api",
            "last_verified": "",   # filled only by provider verification, phase 2
            # extras
            "dialing_code": telephony["dialing_code"],
            "prices_json": pricing["prices_json"],
            "promo_prices_json": pricing["promo_prices_json"],
            "speed_limit_kbps": plan.get("speedLimit") if plan.get("speedLimit") is not None else "",
            "coverage_count": len(coverage),
            "subscription_period": plan.get("subscription_period") or "",
            "has_ads": parse.tri_bool(plan.get("hasAds")),
            "parse_basis": "; ".join(allowance["parse_basis"]),
            "first_seen_country": country_slug,
            "link_type": link_type,
            "run_id": self.run_id,
        }

        provider_verify.apply_to(
            row, provider_verify.lookup(self.verified, provider_slug, coverage))

        flags = quality_flags(row, plan)
        row["qa_flags"] = "; ".join(flags)
        reasons = verification_reasons(row)
        row["needs_verification"] = "true" if reasons else "false"
        row["verification_reasons"] = "; ".join(reasons)
        row["verification_priority"] = verification_priority(row, reasons)
        return row

    # -- coverage table -------------------------------------------------

    def build_coverage_rows(self, master_rows: list[dict]) -> list[dict]:
        by_id = {r["plan_id"]: r for r in master_rows}
        out = []
        for plan_id, codes in self.plan_coverage.items():
            row = by_id.get(plan_id)
            if not row:
                continue
            for code in sorted(codes):
                country = self.countries.get(code, {})
                out.append({
                    "plan_id": plan_id,
                    "country_code": code,
                    "country_name": country.get("name", ""),
                    "country_slug": country.get("slug", ""),
                    "region": country.get("region", ""),
                    "subregions": "|".join(country.get("subregions") or []),
                    "provider": row["provider"],
                    "provider_slug": row["provider_slug"],
                    "plan_name": row["plan_name"],
                    "plan_type": row["plan_type"],
                    "coverage_source": self.coverage_source.get(plan_id, ""),
                    "run_id": self.run_id,
                })
        out.sort(key=lambda r: (r["country_code"], r["provider"].lower(), r["plan_id"]))
        return out

    # -- providers table ------------------------------------------------

    def build_provider_rows(self) -> list[dict]:
        out = []
        for pid, p in self.providers.items():
            features = p.get("features") or {}
            countries = p.get("countries") or []
            out.append({
                "provider_id": pid,
                "provider_slug": p.get("slug", ""),
                "provider": p.get("name", ""),
                "certified": parse.tri_bool(p.get("certified")),
                "plan_count": p.get("planCount", ""),
                "countries_count": len(countries),
                "countries": ",".join(countries),
                "promo_code": p.get("promoCode") or "",
                "promo_discount": p.get("promoDiscount") if p.get("promoDiscount") is not None else "",
                "promo_is_percentage": parse.tri_bool(p.get("promoPercentage")),
                "promo_expired": parse.tri_bool(p.get("promoExpired")),
                "ios_app": parse.tri_bool(features.get("iosApp")),
                "android_app": parse.tri_bool(features.get("androidApp")),
                "web_purchase": parse.tri_bool(features.get("webPurchase")),
                "no_sign_up": parse.tri_bool(features.get("noSignUp")),
                "apple_pay": parse.tri_bool(features.get("applePay")),
                "google_pay": parse.tri_bool(features.get("googlePay")),
                "crypto_payment": parse.tri_bool(features.get("cryptoPayment")),
                "referral_program": parse.tri_bool(features.get("referralProgram")),
                "esimdb_url": f"{BASE_URL}/provider/{p['slug']}" if p.get("slug") else "",
                "uk_coverage": "true" if "GB" in countries else "false",
                "run_id": self.run_id,
            })
        out.sort(key=lambda r: r["provider"].lower())
        return out


# --------------------------------------------------------------------------
# Quality checks and the verification queue
# --------------------------------------------------------------------------

SUSPICIOUS_PRICE_PER_GB = 0.05   # USD - cheaper than this is worth a look
LARGE_ALLOWANCE_GB = 500


def quality_flags(row: dict, plan: dict) -> list[str]:
    """Things a person should look at. Nothing here deletes a row."""
    flags = []
    if not row["provider"]:
        flags.append("missing provider")
    if not row["plan_name"]:
        flags.append("missing plan name")
    if not row["coverage_countries"]:
        flags.append("no coverage countries")
    if row["validity_days"] == "":
        flags.append("no usable validity")
    if row["price"] == "":
        flags.append("no price")
    for field in ("price", "price_usd", "price_gbp", "price_eur"):
        v = row[field]
        if isinstance(v, (int, float)) and v < 0:
            flags.append(f"negative {field}")
    if isinstance(row["validity_days"], int) and row["validity_days"] > 730:
        flags.append("validity over 2 years")
    if row["unlimited"] == "true" and not row["daily_data_gb"] and not row["throttle_speed"]:
        flags.append("unlimited with no stated daily cap or throttle speed")
    if row["unlimited"] == "false" and not row["data_gb"] and not row["daily_data_gb"]:
        flags.append("no data allowance parsed")
    if isinstance(row["price_usd"], (int, float)) and row["price_usd"] == 0:
        flags.append("zero price (free or promotional claim)")
    if row["product_url"] and not row["product_url"].startswith("https://"):
        flags.append("malformed url")
    if str(row["plan_id"]).startswith("fallback:"):
        flags.append("no native plan id - fallback key used")
    return flags


def _discount_percent(row: dict) -> float | None:
    """How far below the headline price the promo price sits, in percent.

    Uses whichever currency pair we actually have. Returns None when there
    is nothing to compare, which is common - eSIMDB quotes many plans in a
    currency we do not carry a promo figure for.
    """
    for full, promo in (("price_usd", "promo_price_usd"),
                        ("price_gbp", "promo_price_gbp"),
                        ("price_eur", "promo_price_eur")):
        a, b = row.get(full), row.get(promo)
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) and a > 0:
            return (a - b) / a * 100.0
    return None


# A discount this deep is worth checking. Anything shallower is the normal
# state of eSIMDB - 5 plans in 6 carry some sort of running discount, so
# flagging every one of them made the queue useless.
DEEP_DISCOUNT_PERCENT = 40.0


def verification_reasons(row: dict) -> list[str]:
    """Which plans are worth checking against the provider's own site first."""
    reasons = []
    if row["uk_inbound"] == "true":
        reasons.append("UK inbound")
    if row["telephony"] != "none" or row["sms"] != "none":
        reasons.append("voice or SMS")
    if row["phone_number"] == "true":
        reasons.append("provides a phone number")

    # Unlimited only matters when the provider has not said what the limit
    # actually is. Unlimited with a stated daily cap or throttle speed is a
    # described product, not a claim to check.
    if (row["unlimited"] == "true"
            and not row["daily_data_gb"] and not row["throttle_speed"]):
        reasons.append("unlimited with no stated limit")

    if row["promo_enabled"] == "true":
        pct = _discount_percent(row)
        promo_zero = any(isinstance(row.get(f), (int, float)) and row[f] == 0
                         for f in ("promo_price_usd", "promo_price_gbp",
                                   "promo_price_eur"))
        if promo_zero:
            reasons.append("promo price is zero")
        elif pct is not None and pct >= DEEP_DISCOUNT_PERCENT:
            reasons.append("discount over %d%%" % int(DEEP_DISCOUNT_PERCENT))

    ppg = row["price_per_gb"]
    if isinstance(ppg, (int, float)) and 0 < ppg < SUSPICIOUS_PRICE_PER_GB:
        reasons.append("unusually cheap per GB")
    for field in ("data_gb", "total_data_gb"):
        v = row[field]
        if isinstance(v, (int, float)) and v >= LARGE_ALLOWANCE_GB:
            reasons.append("unusually large allowance")
            break
    if row["qa_flags"]:
        reasons.append("has quality flags")
    return reasons


# Work the queue top down. 1 is money and reputation, 3 is housekeeping.
PRIORITY_1 = {"UK inbound", "voice or SMS", "provides a phone number"}
PRIORITY_2 = {"unlimited with no stated limit", "promo price is zero",
              "unusually cheap per GB", "unusually large allowance"}


def verification_priority(row: dict, reasons: list[str]) -> str:
    """1, 2, 3 or blank. Plans we can earn on come first within each band."""
    if not reasons:
        return ""
    rs = set(reasons)
    if rs & PRIORITY_1:
        return "1"
    if rs & PRIORITY_2 or any(r.startswith("discount over") for r in rs):
        return "2"
    return "3"
