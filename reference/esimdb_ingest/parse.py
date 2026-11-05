"""Turning an eSIMDB plan record into a row of the master schema.

Two principles run through this file:

  1. Blank beats invented. If eSIMDB does not carry a field, the column is
     empty. It is never filled with a guess, and never with the word
     "unknown" unless eSIMDB itself signalled uncertainty.

  2. Anything derived rather than copied gets recorded in `parse_basis`, so
     you can always see why a row says what it says.

What eSIMDB's API actually carries, and what it does not, is written up in
the README under "What the source does and doesn't give you".
"""

from __future__ import annotations

import html
import re
from typing import Any

# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------


def clean_name(raw: Any) -> str:
    """Plan names arrive HTML-escaped and sometimes with stray whitespace."""
    if not raw:
        return ""
    return re.sub(r"\s+", " ", html.unescape(str(raw))).strip()


def tri_bool(value: Any) -> str:
    """eSIMDB uses null for 'we don't know', which is not the same as false."""
    if value is True:
        return "true"
    if value is False:
        return "false"
    return ""


def mb_to_gb(mb: Any) -> float | None:
    if mb is None:
        return None
    try:
        return round(float(mb) / 1000.0, 4)
    except (TypeError, ValueError):
        return None


def kbps_label(kbps: Any) -> str:
    """128 -> '128kbps', 1000 -> '1Mbps'."""
    if kbps in (None, ""):
        return ""
    try:
        v = float(kbps)
    except (TypeError, ValueError):
        return ""
    if v <= 0:
        return ""
    if v >= 1000 and abs(v / 1000 - round(v / 1000, 2)) < 1e-9:
        mbps = v / 1000
        return f"{mbps:g}Mbps"
    return f"{v:g}kbps"


# --------------------------------------------------------------------------
# Unlimited / allowance
# --------------------------------------------------------------------------

# Only these count as the source calling a plan unlimited. eSIMDB has no
# boolean for it, so the plan name is the evidence.
UNLIMITED_RE = re.compile(
    r"(?<![a-z])(unlimited|unltd|ilimitad\w*|illimit\w*|無制限)(?![a-z])", re.I
)

# "500MB/Day", "1GB/day", "0.49GB/day", "3 GB per day"
DAILY_IN_NAME_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(GB|MB)\s*(?:/|per\s*)\s*day", re.I
)


def parse_allowance(plan: dict[str, Any]) -> dict[str, Any]:
    """Work out the data story for one plan.

    eSIMDB gives `capacity` in megabytes and `dataCapPer` which is null,
    "day" or "month". A daily cap plus an "Unlimited" name is the standard
    way providers dress up a throttled daily allowance.
    """
    basis: list[str] = []
    name = clean_name(plan.get("name"))
    capacity_mb = plan.get("capacity")
    cap_per = plan.get("dataCapPer")
    period = plan.get("period")

    capacity_gb = mb_to_gb(capacity_mb)

    unlimited = bool(UNLIMITED_RE.search(name))
    if unlimited:
        basis.append("unlimited=from plan name")

    daily_gb: float | None = None
    data_gb: float | None = None
    total_gb: float | None = None

    if cap_per == "day":
        daily_gb = capacity_gb
        basis.append("daily=capacity with dataCapPer=day")
    elif cap_per == "month":
        # A monthly recurring allowance. Not a trip total.
        data_gb = capacity_gb
        basis.append("data_gb=capacity with dataCapPer=month (recurs monthly)")
    else:
        m = DAILY_IN_NAME_RE.search(name)
        if m:
            amount = float(m.group(1))
            daily_gb = round(amount / 1000, 4) if m.group(2).upper() == "MB" else amount
            basis.append("daily=parsed from plan name")
        elif capacity_gb is not None and capacity_gb > 0:
            data_gb = capacity_gb
            basis.append("data_gb=capacity (fixed bundle)")

    # A total is only calculable for a metered daily plan of known length.
    # For a genuinely unlimited plan there is no total to state.
    if daily_gb is not None and not unlimited:
        try:
            days = int(period)
            if days > 0:
                total_gb = round(daily_gb * days, 4)
                basis.append("total=daily x validity_days")
        except (TypeError, ValueError):
            pass
    elif data_gb is not None:
        total_gb = data_gb

    if capacity_mb == 0 and not unlimited:
        basis.append("capacity=0 in source; allowance left blank")

    return {
        "unlimited": unlimited,
        "data_gb": data_gb,
        "daily_data_gb": daily_gb,
        "total_data_gb": total_gb,
        "parse_basis": basis,
    }


# --------------------------------------------------------------------------
# Voice and SMS
# --------------------------------------------------------------------------

# eSIMDB's telephony object looks like:
#   {"dialingCode": "+44",
#    "voice": {"inbound": true, "outbound": true},
#    "sms":   {"inbound": true, "outbound": false}}
#
# It describes native cellular voice and SMS on a real number, which is why
# a plan with no telephony object is data-only rather than "unknown". It has
# no field for app-based calling, so this pipeline never emits app_based.


def direction_vocab(block: Any) -> str:
    if not isinstance(block, dict):
        return "none"
    inbound = bool(block.get("inbound"))
    outbound = bool(block.get("outbound"))
    if inbound and outbound:
        return "incoming_and_outgoing"
    if inbound:
        return "incoming_only"
    if outbound:
        return "outgoing_only"
    return "none"


# Dialling codes that map to exactly one country. Shared codes (+1, +7, +44
# covers Crown Dependencies too) are deliberately left out - the code itself
# is recorded instead of a country guess.
DIALING_CODE_COUNTRY = {
    "+33": "FR", "+34": "ES", "+39": "IT", "+41": "CH", "+43": "AT",
    "+45": "DK", "+46": "SE", "+47": "NO", "+48": "PL", "+49": "DE",
    "+30": "GR", "+31": "NL", "+32": "BE", "+36": "HU", "+40": "RO",
    "+351": "PT", "+352": "LU", "+353": "IE", "+354": "IS", "+356": "MT",
    "+357": "CY", "+358": "FI", "+359": "BG", "+370": "LT", "+371": "LV",
    "+372": "EE", "+376": "AD", "+377": "MC", "+385": "HR", "+386": "SI",
    "+420": "CZ", "+421": "SK", "+81": "JP", "+82": "KR", "+852": "HK",
    "+65": "SG", "+61": "AU", "+64": "NZ", "+91": "IN", "+52": "MX",
    "+55": "BR", "+90": "TR", "+971": "AE", "+972": "IL", "+966": "SA",
}


def parse_telephony(plan: dict[str, Any]) -> dict[str, Any]:
    tel = plan.get("telephony")
    if not isinstance(tel, dict):
        return {
            "telephony": "none",
            "sms": "none",
            "phone_number": "false",
            "phone_number_country": "",
            "dialing_code": "",
        }

    code = (tel.get("dialingCode") or "").strip()
    return {
        "telephony": direction_vocab(tel.get("voice")),
        "sms": direction_vocab(tel.get("sms")),
        "phone_number": "true" if code else "false",
        # Only filled where the code identifies one country beyond doubt.
        "phone_number_country": DIALING_CODE_COUNTRY.get(code, ""),
        "dialing_code": code,
    }


# --------------------------------------------------------------------------
# Plan type and coverage
# --------------------------------------------------------------------------

GLOBAL_COVERAGE_THRESHOLD = 100   # countries - anything this wide is global
GLOBAL_MIN_WITH_SPREAD = 30       # ...or this wide across four continents


def classify_plan_type(coverage: list[str], continents: set[str]) -> str:
    """`continents` is the set of eSIMDB top-level buckets (europe, asia,
    americas, africa, oceania) the coverage touches - not the overlapping
    region slugs, which would make an ordinary Europe plan look global."""
    n = len(coverage)
    if n == 0:
        return "unknown"
    if n == 1:
        return "single_country"
    if n >= GLOBAL_COVERAGE_THRESHOLD or (
            len(continents) >= 4 and n >= GLOBAL_MIN_WITH_SPREAD):
        return "global"
    if len(continents) <= 1:
        return "regional"
    return "multi_country"


# --------------------------------------------------------------------------
# Pricing
# --------------------------------------------------------------------------

PREFERRED_HEADLINE = ("GBP", "USD", "EUR")


def parse_pricing(plan: dict[str, Any], billable_gb: float | None) -> dict[str, Any]:
    prices = plan.get("prices") or {}
    promo_prices = plan.get("promoPrices") or {}

    headline_currency = ""
    headline_price: float | None = None
    for cur in PREFERRED_HEADLINE:
        if cur in prices and prices[cur] is not None:
            headline_currency, headline_price = cur, prices[cur]
            break
    if not headline_currency and prices:
        headline_currency = sorted(prices)[0]
        headline_price = prices[headline_currency]

    def num(source: dict[str, Any], cur: str) -> Any:
        v = source.get(cur)
        return v if isinstance(v, (int, float)) else ""

    usd = plan.get("usdPrice")
    usd = usd if isinstance(usd, (int, float)) else num(prices, "USD")

    price_per_gb = ""
    if isinstance(usd, (int, float)) and usd > 0 and billable_gb and billable_gb > 0:
        price_per_gb = round(usd / billable_gb, 4)

    promo_enabled = bool(plan.get("promoEnabled"))
    plan_promo = plan.get("promo") or {}
    promo_usd = plan.get("usdPromoPrice")

    return {
        "currency": headline_currency,
        "price": headline_price if headline_price is not None else "",
        "price_usd": usd if isinstance(usd, (int, float)) else "",
        "price_gbp": num(prices, "GBP"),
        "price_eur": num(prices, "EUR"),
        "price_per_gb": price_per_gb,
        "promo_enabled": "true" if promo_enabled else "false",
        "promo_price_usd": promo_usd if isinstance(promo_usd, (int, float)) else "",
        "promo_price_gbp": num(promo_prices, "GBP"),
        "promo_price_eur": num(promo_prices, "EUR"),
        "promo_code": plan_promo.get("code") or "",
        "new_user_only": tri_bool(plan.get("newUserOnly")),
        "prices_json": prices,
        "promo_prices_json": promo_prices,
    }


# --------------------------------------------------------------------------
# Validity
# --------------------------------------------------------------------------


def parse_validity(plan: dict[str, Any]) -> dict[str, Any]:
    period = plan.get("period")
    try:
        days: Any = int(period)
        if days <= 0:
            days = ""
    except (TypeError, ValueError):
        days = ""

    notes: list[str] = []
    raw_info = clean_name(plan.get("validity_info"))
    if raw_info:
        notes.append(raw_info)
    if plan.get("isConsecutive"):
        notes.append("consecutive days")
    if plan.get("subscription"):
        sub_period = plan.get("subscription_period")
        notes.append(
            f"renews every {sub_period}" if sub_period else "recurring subscription"
        )
    return {"validity_days": days, "validity_info": "; ".join(notes)}
