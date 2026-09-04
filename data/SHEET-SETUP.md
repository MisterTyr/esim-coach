# Wire up a Google Sheet as the live data source

The pipeline pulls plans straight from a Google Sheet, so you (or anyone you
trust) can edit plans in a spreadsheet and the site updates on the next daily
run — no code, no commits.

It's already wired. You just provide the URL via the `SHEET_CSV_URL` environment
variable / GitHub secret.

## Steps (about 5 minutes)

1. **Create the Sheet.** New Google Sheet → File → Import → Upload
   `data/sample_plans.csv` → "Replace current sheet". You now have the right
   columns and the starter UK data.

2. **Keep the header row exactly:**

   `provider, plan_name, region, country, data_gb, validity_days, price,
   product_url, direction, voice_type, calls_included, sms_included,
   number_country, full_speed_gb, full_speed_period, post_cap_speed, hotspot,
   source_url, timestamp`

3. **Publish as CSV.** File → Share → Publish to web → choose the sheet/tab →
   format **Comma-separated values (.csv)** → Publish. Copy the URL. It looks
   like:
   `https://docs.google.com/spreadsheets/d/e/XXXX/pub?gid=0&single=true&output=csv`
   (An `.../export?format=csv` link works too if the sheet is link-viewable.)

4. **Give the pipeline the URL:**
   - **Locally:** `export SHEET_CSV_URL="https://…output=csv"` then run the scripts.
   - **On GitHub (for the daily cron):** repo → Settings → Secrets and variables →
     Actions → New repository secret → name `SHEET_CSV_URL`, paste the URL.

5. **Test it:**
   ```
   SHEET_CSV_URL="https://…output=csv" python3 scripts/update_plans.py && python3 scripts/build_static.py
   ```
   You'll see it pull from the Sheet instead of "skipping … no URL set".

## What each column means

| Column | What goes in it |
|---|---|
| `provider` | Company name, spelled the same way every time. |
| `plan_name` | The name the provider gives the plan. |
| `region` | One of Europe, North America, Asia, South America, Oceania, Africa, Global. |
| `country` | The country it covers, or `Multi`. |
| `data_gb` | A number, or the word `unlimited`. |
| `validity_days` | How many days it lasts. A whole number. |
| `price` | Number only, no `£`. |
| `product_url` | The link people click. Your affiliate link once you have one. |
| `direction` | `outbound` for UK travellers going abroad, `inbound` for visitors coming to the UK. Blank counts as outbound. |
| `voice_type` | `native` (real phone calls), `app_voip` (calls only through the provider's app), `external_voip` (data only, WhatsApp and the like work), `none`. |
| `calls_included` | Minutes, or `unlimited`. Only means anything when `voice_type` is `native`. |
| `sms_included` | A count, or `unlimited`. Same. |
| `number_country` | `UK`, `US`, and so on, if the plan gives you a real phone number. |
| `full_speed_gb` | For an `unlimited` plan, how much data you get before they slow you down. **Leave blank only if it is genuinely uncapped.** |
| `full_speed_period` | `per_day` or `per_plan` — whether that allowance is per day or for the whole plan. Airalo, Saily and Nomad cap per day; Ubigi caps per plan. Blank counts as `per_plan`. |
| `post_cap_speed` | What it slows to, e.g. `2Mbps`. |
| `hotspot` | `yes`, `capped` or `no` — whether you can share the connection to a laptop. |
| `source_url` | The provider page you took the price from. Your audit trail. |
| `timestamp` | The date you checked the price, e.g. `2026-09-04T09:00:00Z`. |

### Why `full_speed_gb` matters more than it looks

"Unlimited" is not one product. Ubigi's UK unlimited gives 25GB at full speed
over seven days and then drops to 2Mbps. A plan like that is not the same as one
with no cap at all, and it should not rank as though it were.

And most providers cap per **day**, not per plan. Airalo gives 3GB a day and
resets at midnight; Ubigi gives 25GB across a whole 7-day plan. Written down as
just a number, those look similar and are nothing like each other, which is why
`full_speed_period` exists.

So the ranking treats a capped unlimited plan as a plan of that size: fill in
`full_speed_gb` and `full_speed_period`, and it competes on price per full-speed
GB against ordinary sized plans. A per-day cap is multiplied by the number of
days, so Airalo's 30-day unlimited is scored as 90GB rather than 3GB. Leave it blank and the plan is treated as genuinely uncapped, which
puts it below the sized plans, ordered by price per day — because there is no
honest way to compare "unlimited" against "10GB" without inventing a figure for
how much someone uses.

Getting this wrong in the generous direction is the expensive mistake. A
throttled plan with a blank `full_speed_gb` is claiming more than it delivers.

## Checks that stop a bad edit publishing

The daily job runs unattended, so `update_plans.py` checks the data before it
writes anything. If a check fails, the run stops and the published files are
left exactly as they were. The limits live in the `checks` block of
`data/config.json`:

| Check | What it catches |
|---|---|
| `require_live_source` | The Sheet returned nothing and the run was about to publish the local sample file instead. This is the failure that would be hardest to spot. |
| `min_rows` | Most of the Sheet has gone missing. |
| `max_row_drop_pct` | Rows deleted by accident — a fall of more than this share against the last published set stops the run. |
| `max_price` | A price typed with the decimal point in the wrong place. |
| `max_stale_days` | Nobody has checked a price in months, so the site would be publishing numbers no one stands behind. |

Missing prices, zero prices, missing plan names and zero validity all stop the
run too. Placeholder affiliate links and unlimited plans with no `full_speed_gb`
print a warning but do not stop it.

To run against the sample file deliberately: `ALLOW_SAMPLE_DATA=1 python3 scripts/update_plans.py`.

## Paid placement

`pin_providers` in `data/config.json` floats a provider's plans to the top of
the list. That is a commercial arrangement, not a verdict, and the site says so:
pinned plans carry a "Paid placement" label.

The "Top pick" badge is separate and cannot be bought. It goes to whichever plan
wins on the value maths before placement is applied, which is recorded as
`value_rank` on every plan. A plan can carry both labels honestly.

Pinned providers still respect `per_provider_limit`, so they can't swamp the list.
