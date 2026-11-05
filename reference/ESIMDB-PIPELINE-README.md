# eSIMDB ingestion for eSIM-Sorted.co.uk

Pulls every plan eSIMDB lists into the master schema, deduplicated, with the
plan-to-country relationships kept properly instead of exploded into fake
products.

## Running it

```bash
cd esimdb
pip install -r requirements.txt

# Try five destinations first. Takes about a minute.
python -m esimdb_ingest.run --out data --limit-countries 5

# The real thing. About 270 requests, 20-30 minutes, several GB downloaded.
python -m esimdb_ingest.run --out data
```

Other switches worth knowing:

```
--only uk,japan,france   just these destinations
--resume                 keep what's downloaded, retry only what failed
--from-cache             rebuild the CSVs from saved JSON, no requests at all
--strict-schema          emit exactly your 57 columns, no extras
--delay 2.5              slow it down further
```

`--from-cache` is the one you'll use most. Every response is saved, so you can
change the parsing and rebuild the whole dataset in seconds without touching
eSIMDB again.

## What comes out

Everything lands in `data/`:

| File | One row per |
|---|---|
| `plans_master.csv` | unique plan |
| `plan_coverage.csv` | plan and country pair |
| `providers.csv` | provider |
| `change_log.csv` | difference from the previous run |
| `failed_requests.csv` | request that failed after retries |
| `data_quality_report.txt` / `.json` | the run's counts |
| `run_manifest.json` | run ID, timing, totals, whether it was complete |
| `raw/` | every response as saved gzipped JSON |
| `previous/` | last complete run's master file, for comparison |

`plans_master.csv` starts with your 57 columns in your order, then adds a
handful of extras: the full price table as JSON, the dialling code, why the
allowance columns say what they say, what got flagged, and what's queued for
checking against the provider. `--strict-schema` drops them.

There's a sample set in `sample_output/` built from the offline fixture, so
you can see the shapes before running anything.

## How coverage works

eSIMDB has two endpoints and they carry different things:

- `/api/client/countries/{slug}/data-plans` returns every plan that works in
  that country, but doesn't say what else the plan covers.
- `/api/client/regions/{slug}/data-plans` returns only the multi-country
  plans, and those *do* carry a `coverages` list of country codes.

So the run does the regions first, builds a plan-to-coverage map from them,
then walks the destinations. A plan seen in a region response gets its real
coverage list. A plan that only ever appears on one destination's page is a
single-country plan and its coverage is that one country.

The result: a Europe plan covering 42 countries is one row in
`plans_master.csv` and 42 rows in `plan_coverage.csv`. Join on `plan_id`.

Deduplication is on eSIMDB's own `_id`. The composite fallback key only fires
for a record that arrives without one, and those rows are flagged.

## What the source does and doesn't give you

This matters, because your spec assumed some fields exist that don't.

**eSIMDB carries these, and they're mapped:**

plan ID, provider, plan name, coverage countries, data capacity (in
megabytes), whether the cap is daily or monthly, validity in days, whether
days are consecutive, prices in up to 49 currencies, promotional prices and
codes, new-user-only, subscription and its renewal period, pay as you go,
5G, low latency, tethering, top-ups, eKYC, possible throttling, reduced
speed after the cap, a speed limit, free-text validity notes, and telephony.

Telephony is better than expected. It looks like this:

```json
{"dialingCode": "+44",
 "voice": {"inbound": true, "outbound": true},
 "sms":   {"inbound": true, "outbound": false}}
```

That maps straight onto your controlled vocabulary — `incoming_and_outgoing`,
`incoming_only`, `outgoing_only`, `none` — with no inference. Across the
17,833 plans covering the UK, 135 carry a +44 number and 104 of those do
calls and texts both ways. That's your UK-visitor-with-a-real-number segment,
already identified.

**eSIMDB does not carry these at all:**

- underlying networks per country (no EE / O2 / Vodafone breakdown)
- activation policy
- fair use wording
- device compatibility
- the provider's own website
- a per-plan buy link (those are affiliate redirects built in the browser)
- a destination-currency price field

Those columns come out blank, on purpose. Filling them would mean inventing
data. They're the natural job for the provider-verification phase.

There is also **no unlimited flag**. Providers encode it in the plan name plus
a daily cap. So the pipeline treats the plan name as the evidence: a name
matching "unlimited" (or unltd / ilimitado / illimité / 無制限) sets
`unlimited=true`, and `dataCapPer: "day"` fills `daily_data_gb`. Where the
daily figure only appears in the name — "500MB/Day" — it's parsed from there
and `parse_basis` records that it was. An unlimited plan never gets a
calculated total, per your spec.

`possible_throttling` is true when eSIMDB says so *or* when it gives a
reduced speed. `throttle_speed` is formatted from `reducedSpeed`: 128 becomes
`128kbps`, 1000 becomes `1Mbps`.

`phone_number_country` is filled only where the dialling code identifies one
country beyond doubt. +44 and +1 don't, so those rows keep the raw code in
`dialing_code` and leave the country blank rather than guessing.

## Plan type

- one country → `single_country`
- more than one, all in the same continent → `regional`
- across continents → `multi_country`
- 100+ countries, or 30+ across four continents → `global`

Continent means eSIMDB's top-level bucket (europe, asia, americas, africa,
oceania). The region *slugs* overlap heavily — an ordinary Europe plan sits in
europe, nordic, scandinavia, baltic and balkans at once — so they'd make a
Europe plan look global if used for this. The slugs are still kept, in
`coverage_regions`; `region` holds the continents.

## UK flags

`uk_inbound` is true when the coverage includes GB. `uk_outbound` is true when
the coverage includes anywhere that isn't GB. A UK-only tourist eSIM is
inbound. A Japan plan is outbound. A Europe plan including Britain is both.

Anything covering the UK gets its `product_url` pointed at the UK destination
page, since that's the page a UK reader wants.

## Change detection

Each run compares against `data/previous/plans_master.csv` and writes every
difference to `change_log.csv`: new plans, discontinued plans, new providers,
price rises and falls, allowance changes, validity changes, throttle changes,
voice and SMS appearing or disappearing, coverage changes, promotions starting
and ending.

The snapshot only rotates after a run that covered every destination without
failures. A partial run won't make the next one report half the catalogue as
discontinued.

## Quality flags and the verification queue

Nothing gets deleted for being incomplete. Rows get flagged instead, in
`qa_flags`: missing provider or name, no coverage, no usable validity, no
price, negative prices, validity over two years, unlimited with nothing
stated about the cap, no allowance parsed, zero price, malformed URL, no
native plan ID.

Separately, `needs_verification` marks the plans worth checking against the
provider's own site first, with `verification_reasons` saying why: UK inbound,
voice or SMS, provides a phone number, advertised unlimited, promotional
price, unusually cheap per GB, unusually large allowance, or already flagged.
That's your phase-two work queue, ready to go.

## Being a good citizen

One request at a time, four seconds apart, exponential backoff with jitter on
429 and 5xx, `Retry-After` honoured.

Those defaults exist because they had to. On 6 September 2026 a run at two
workers and 1.5 seconds got 403'd after about 60 destinations. eSIMDB is
watching the rate, so don't raise `--concurrency` and don't drop `--delay`
below about 3.

If eSIMDB returns 401 or 403, or eight requests fail in a row, the run stops
rather than pushing harder, and it does not try to work around anything. It
still writes out everything it gathered up to that point, and keeps the raw
responses, so `--resume` picks up from there. If you get blocked, leave it a
while before resuming. If it keeps happening, the right move is to email
eSIMDB for proper API access rather than tuning the delay upwards forever.

Every response is saved before it's parsed, and a checkpoint file records
what's done, so `--resume` picks up where it left off.

## Testing

```bash
python -m esimdb_ingest.tests.test_pipeline          # offline, no network
python -m esimdb_ingest.tests.make_sample_output out # writes example files
```

The fixture in `esimdb_ingest/tests/fixture.py` is real data taken from live
responses on 6 September 2026 and trimmed. It covers the awkward cases: a UK
number with two-way calls, outgoing-only telephony, an "unlimited" plan that's
really a daily allowance, a daily allowance stated only in the plan name, a
throttled plan, a promo, a monthly subscription, zero validity, a missing plan
name, and a regional plan with a real coverage list.

## If a request comes back "not JSON"

eSIMDB serves brotli-compressed responses and `requests` can't unpack those
without the `brotli` package, which is why it's in requirements.txt. If you
skipped the install you'll get a decode error on the first request. Fix:

```bash
pip install brotli
```

The run also asks for gzip only, and unpacks brotli or zstd itself as a
backstop if a server sends it anyway. The error message names the content
encoding the server actually used.

## Known limits

- The API has no pagination parameters that work, so a destination response
  arrives whole. The UK one is about 11MB gzipped. That's why the run is
  batched and why 1.5GB is the rough download figure.
- `price_local` and `promo_price_local` stay blank. eSIMDB quotes up to 49
  currencies but doesn't nominate one as the destination's, and picking one
  would be a guess. The full table is in `prices_json` if you want to derive
  it later.
- `provider_verified` is eSIMDB's own "certified" flag, not verification you
  did. `last_verified` stays blank until the provider-checking phase fills it.
- Endpoints can change. If they do, the four constants at the top of
  `config.py` are the only place that needs editing.
