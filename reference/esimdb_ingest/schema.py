"""The output columns.

MASTER_COLUMNS is your schema CSV, in your order, unchanged.

EXTRA_COLUMNS are appended after it. They carry things worth keeping that
your 57 columns had nowhere to put - the full price table, why a row says
what it says, and what still needs checking against the provider. Run with
--strict-schema to drop them and emit exactly the 57.
"""

MASTER_COLUMNS = [
    "provider", "plan_name", "region", "country", "data_gb", "validity_days",
    "price", "product_url", "timestamp", "plan_id", "provider_slug",
    "provider_verified", "plan_type", "coverage_countries", "coverage_regions",
    "daily_data_gb", "total_data_gb", "unlimited", "throttle_speed",
    "validity_info", "currency", "price_usd", "price_gbp", "price_eur",
    "price_local", "price_per_gb", "promo_enabled", "promo_price_usd",
    "promo_price_gbp", "promo_price_eur", "promo_price_local", "promo_code",
    "new_user_only", "subscription", "pay_as_you_go", "has_5g",
    "network_types", "low_latency", "tethering", "telephony", "sms",
    "phone_number", "phone_number_country", "networks", "activation_policy",
    "kyc_required", "can_top_up", "possible_throttling", "fair_use_policy",
    "device_compatibility", "provider_url", "esimdb_url", "uk_inbound",
    "uk_outbound", "uk_traveller_relevant", "source", "last_verified",
]

EXTRA_COLUMNS = [
    "dialing_code",          # kept whole where it maps to more than one country
    "prices_json",           # every currency eSIMDB quoted, not just three
    "promo_prices_json",
    "speed_limit_kbps",      # eSIMDB's speedLimit - a cap, not a post-cap throttle
    "coverage_count",
    "subscription_period",
    "has_ads",
    "parse_basis",           # why the allowance columns say what they say
    "qa_flags",              # things a human should look at
    "needs_verification",    # true when this plan is in a priority check group
    "verification_reasons",
    "verification_priority", # 1 = check first, 3 = housekeeping, blank = fine
    "first_seen_country",    # the destination request that first returned it
    "link_type",             # affiliate | provider_site | none
    "run_id",
]

COVERAGE_COLUMNS = [
    "plan_id", "country_code", "country_name", "country_slug", "region",
    "subregions", "provider", "provider_slug", "plan_name", "plan_type",
    "coverage_source", "run_id",
]

PROVIDER_COLUMNS = [
    "provider_id", "provider_slug", "provider", "certified", "plan_count",
    "countries_count", "countries", "promo_code", "promo_discount",
    "promo_is_percentage", "promo_expired", "ios_app", "android_app",
    "web_purchase", "no_sign_up", "apple_pay", "google_pay", "crypto_payment",
    "referral_program", "esimdb_url", "uk_coverage", "run_id",
]

CHANGE_COLUMNS = [
    "change_type", "plan_id", "provider", "provider_slug", "plan_name",
    "field", "old_value", "new_value", "previous_run_id", "run_id",
    "detected_at",
]

FAILED_COLUMNS = ["kind", "key", "url", "reason", "run_id", "detected_at"]


def all_columns(strict: bool = False) -> list[str]:
    return list(MASTER_COLUMNS) if strict else MASTER_COLUMNS + EXTRA_COLUMNS
