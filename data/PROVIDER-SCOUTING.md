# Provider scouting

Written 3 September 2026. The Sheet currently holds 8 providers and 22 hand-typed
rows. This is the longer list to grow it from, ordered by what to do first.

**Read the sourcing note before trusting a number.** Everything marked *(roundup)*
comes from comparison articles, not from the provider. Commission rates and cookie
windows in particular go stale fast and are often wrong in listicles. Treat this as
a list of who to look at, not as data to publish. Nothing here goes in the Sheet
until the price has been checked on the provider's own site.

## Tier 1 — apply now

The four already named in `LAUNCH-PLAN.md`, plus the ones a UK publisher can reach
with the least friction. Approvals are the clock we do not control, so these go in
before any content work.

| Provider | Why | Programme |
|---|---|---|
| Airalo | Widest coverage, most recognised name, biggest search volume | In-house, 8-10% *(roundup)* |
| Nomad | Strong plan variety, pause and reactivate | In-house *(roundup)* |
| Holafly | Unlimited plans, heavy brand spend, hotspot is capped | Partner programme, own page |
| Saily | Budget end, NordVPN-owned so the tracking is competent | 15%, 30-day cookie *(roundup)* |
| Jetpac | Airport lounge perk on delays, genuinely different angle | In-house *(roundup)* |
| Ubigi | Unrestricted tethering, dual network in Japan | Impact *(roundup)* |

## Tier 2 — add for coverage once Tier 1 is approved

Worth listing on the site whether or not the affiliate money is good, because a
comparison site with eight providers is not a comparison site.

BNESIM, aloSIM, GigSky, Yesim, Roamless, Instabridge, Esimatic, Roamify, Manet
Travel, eSIMo, Truely, SimOptions, Gigatel, Billion Connect, 4S eSIM, Voye,
Simbye, Virgin Connect, Amigo, Maya Mobile, eSIM Go, BreezeSim, eSIM4Travel,
eTravelSIM, Numero, KnowRoaming, WorldSIM. *(roundup)*

Realistic order: BNESIM, aloSIM, GigSky, Yesim and Roamless first. They show up in
every roundup, which means they have the review volume to be credible and the
traffic to be worth ranking against.

## Tier 3 — the UK-inbound cluster

Not needed for launch. This is the second content cluster, aimed at visitors coming
to the UK, where a UK-run site has an edge worth having. The Sheet already carries
three of these without the site admitting it.

SMARTY (Three UK), Sim Local, Honest Mobile, giffgaff, Lycamobile, plus the UK
plans that the Tier 1 travel providers already sell. All of these need checking
against their own sites - none of it is verified.

## The UK affiliate route

Awin is the practical network for a UK publisher, and it already carries eSIM
merchants: Breeze eSIM UK, WorldSIM, eSIMania and Esim Prime all run programmes
there. One Awin account reaches several merchants at once instead of applying to
each in-house programme separately, which matters when approvals are the
bottleneck. Awin charges a small joining deposit that is refunded against
earnings. Impact carries Ubigi. Most of the rest run in-house.

Apply to Awin the same day as the four in-house programmes. It is the cheapest way
to widen the provider list without widening the admin.

## Before anything here reaches the Sheet

- Check the price on the provider's own site, in GBP where they offer it.
- Record the date checked. The pipeline reads `timestamp` per row and the homepage
  now reports the newest one, so a stale row is visible rather than hidden.
- Confirm the affiliate link format before swapping any `product_url`, and test one
  click end to end.
- Note which providers cap or block hotspot use. Holafly caps it. That is the
  single most common complaint about travel eSIMs and it is a real ranking factor
  for a value site, not a footnote.

---

# Market research, 4 September 2026

Marty supplied a research document covering both directions of the market. It is
saved as `data/MARKET-RESEARCH-2026-09.md`. Nothing in it is verified against a
provider's own site, so it stays a list of who to look at, not data to publish.
The parts that change what we build are below.

## The finding that affects the ranking maths

**"Unlimited" is not one thing, and the value engine currently pretends it is.**
Ubigi's UK unlimited gives 25GB at full speed over seven days, then drops to
2Mbps; its 30-day product gives 60GB before the same drop. Holafly and others
have their own caps. `update_plans.py` ranks unlimited plans by price per day, so
right now a throttled plan and an unthrottled one at the same price rank
identically. That is a correctness problem in the engine, not a missing column.

Two fields fix it: `full_speed_gb` and `post_cap_speed`. Once they exist, an
unlimited plan with a full-speed allowance should rank on price per full-speed
GB, and only a genuinely uncapped plan should rank on price per day.

## The differentiator worth building around

Most comparison sites lump data-only plans in with voice-capable ones. They are
not equivalent products. A `voice_type` column with four values separates them:

1. `native` — real cellular voice on the SIM
2. `app_voip` — the provider's own app supplies calling (aloSIM bundles a Hushed
   number; Roamless sells numbers in-app)
3. `external_voip` — data only, but VoIP apps work
4. `none`

This matters commercially as well as editorially. In the UAE, VoIP is
restricted, so "WhatsApp calling works" is not the same claim as "the plan makes
phone calls". A filter for "includes calls" is something the big comparison
sites do not offer.

Providers the research flags as genuinely voice-capable: Orange Travel, Airalo
Discover+, some Nomad destination plans, Saily Global with the number add-on,
Roamless, and Three UK PAYG.

## Proposed Sheet columns

The research lists about thirty fields. That is more than a hand-maintained
Sheet will survive. These nine additions are the ones that change a ranking or a
buying decision:

| Column | Values | Why |
|---|---|---|
| `direction` | `outbound` / `inbound` | Splits the two content clusters. The Sheet already holds inbound rows the site does not admit to. |
| `voice_type` | `native` / `app_voip` / `external_voip` / `none` | The differentiator above. |
| `calls_included` | minutes, or `unlimited`, or blank | Only meaningful when `voice_type` is native. |
| `sms_included` | count, `unlimited`, or blank | As above. |
| `number_country` | `UK` / `US` / blank | A visitor wanting a +44 number needs this. |
| `full_speed_gb` | number, or blank if truly uncapped | Fixes the unlimited ranking. |
| `post_cap_speed` | e.g. `2Mbps` | Reader-facing detail for the same problem. |
| `hotspot` | `yes` / `capped` / `no` | Already on the list. Holafly caps it; most common complaint about travel eSIMs. |
| `source_url` | provider's own page | Audit trail alongside `timestamp`. |

## Providers to add, revised order

Unchanged first five: BNESIM, aloSIM, GigSky, Yesim, Roamless.

The research adds three the earlier list missed, all worth pulling forward:

- **Orange Travel** — the strongest data + calls + SMS product found anywhere in
  the research, covering 40+ European territories including the UK, and it sells
  a UK visitor eSIM too. It sits in both clusters.
- **Rewild Mobile** — UK-based, and came out cheapest on 1–10GB in the July 2026
  Which? comparisons across Australia, Japan, China, Turkey, Egypt, Morocco,
  Indonesia and the UAE. That is a lot of destination pages it would win.
- **Three UK PAYG** — the "best travel eSIM is often not a travel eSIM" case.
  £10 buys 40GB UK plus 6GB roaming across 70+ destinations with unlimited
  qualifying calls and texts in Europe. Nothing in the travel-eSIM set matches
  that for a UK traveller, and no travel-eSIM comparison site lists it.

## UK-inbound cluster, expanded

The research is firm that a visitor wanting a real +44 number is usually better
served by a domestic PAYG eSIM than by a product marketed as a travel eSIM. EE's
UK Travel eSIM is explicitly data-only at £15 for 7 days; O2 PAYG is £10 for
10GB with unlimited UK calls and texts and a real number.

Networks supporting PAYG eSIM as of April 2026: O2, Three, Vodafone, 1pMobile,
Asda Mobile, giffgaff, iD Mobile, Lebara, Lyca Mobile, Tesco Mobile. Lebara is
worth singling out for visitors who need to call home.

**So the inbound cluster should not restrict itself to "travel eSIMs".** That is
the edge a UK-run site has, and it is an editorial decision as much as a data one.
