# Wire up a Google Sheet as the live data source

The pipeline can pull plans straight from a Google Sheet, so you (or anyone you
trust) can edit plans in a spreadsheet and the site updates on the next daily
run — no code, no commits.

It's already wired. You just provide the URL via the `SHEET_CSV_URL` environment
variable / GitHub secret. If that's unset, the site falls back to the local
`data/sample_plans.csv`, so nothing breaks either way.

## Steps (about 5 minutes)

1. **Create the Sheet.** New Google Sheet → File → Import → Upload
   `data/sample_plans.csv` → "Replace current sheet". You now have the right
   columns and the starter UK data, Honest Mobile included.

2. **Keep the header row exactly:**
   `provider, plan_name, region, country, data_gb, validity_days, price, product_url, timestamp`
   - `data_gb`: a number or the word `unlimited`
   - `price`: number only, no `£`
   - `region`: one of Europe, North America, Asia, South America, Oceania, Africa, Global

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

## Featuring a provider (e.g. Honest Mobile)
Honest Mobile is pinned to the top via `pin_providers` in `data/config.json`.
Add or remove provider names there to change who gets the "Top pick" treatment —
they float above the value ranking and get the featured badge. Pinned providers
still respect `per_provider_limit`, so they won't swamp the whole list.
