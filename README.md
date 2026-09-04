# eSIM Sorted

A low-maintenance, static travel-eSIM comparison site. It reads plan data from a
CSV (or a Google Sheet / API), ranks plans by real value ($/GB, or $/day for
unlimited), and rebuilds every page. No database, no server, no build framework —
just Python that writes HTML. A daily GitHub Action keeps it fresh on its own.

Domain: **esim-sorted.co.uk**

## How it works
```
data/sample_plans.csv  ──►  scripts/update_plans.py  ──►  plans.json + sitemap.xml
                                                              │
                            scripts/build_static.py  ◄────────┘
                                     │
                                     ▼
                    index.html + evergreen/legal pages (styled, shared header/footer)
```
- `data/config.json` — brand, domain, regions, ranking rules, data sources, affiliate UTM tags.
- `data/sample_plans.csv` — the plan data (swap in real plans; see `prompts/02`).
- `scripts/update_plans.py` — normalize → compute value metrics → rank → write JSON + sitemap.
- `scripts/build_static.py` — render `index.html` and all content pages from `content.py`.
- `scripts/content.py` — evergreen + legal page copy (edit here to change content).
- `assets/` — `styles.css`, `app.js` (region filter), logo.
- `.github/workflows/update.yml` — daily refresh + auto-commit.
- `automation/email-sequence.md` — 4-email welcome sequence.
- `prompts/` — copy-paste, token-light prompts to run the whole thing (start here).

## Run it locally
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
python3 scripts/update_plans.py    # writes plans.json + sitemap.xml
python3 scripts/build_static.py    # writes index.html + content pages
open index.html
```
(The scripts fall back gracefully if `requests`/`dateutil` aren't installed, as
long as you're using the local CSV source.)

## Get it live
See **LAUNCH-PLAN.md** for the 7-day path, and **prompts/07-deploy.md** for host
setup. Short version: push to GitHub, connect Cloudflare Pages (no build command,
serve root), point esim-sorted.co.uk at it.

## Adding content
- **Live data via Google Sheet:** set `SHEET_CSV_URL` to a published-Sheet CSV link
  and the pipeline pulls from it (falls back to `data/sample_plans.csv` if unset).
  Full steps in `data/SHEET-SETUP.md`.
- **Featured provider:** `pin_providers` in `data/config.json` floats a provider to
  the top with a "Top pick" badge (currently Honest Mobile).
- **More plans:** edit the Sheet or `data/sample_plans.csv`, rebuild.
- **Currency:** `currency_display` / `currency_symbol` in `data/config.json` (GBP by default).
- **New article:** add an entry to `PAGES` in `scripts/content.py` (`prompts/04`),
  add its filename to the sitemap list in `update_plans.py`, rebuild.
- **Change ranking:** `data/config.json` → `ranking.strategy` is `value`,
  `cheapest`, or `longest_validity`.

## Notes
- Prices change often. The pipeline is only as accurate as its source — verify
  before trusting generated data, and move to a Sheet/API source when you can.
- Outbound plan links carry `rel="nofollow sponsored"` and your UTM tags automatically.
- The previous scaffold is kept in `Archive Build/` for reference; this root build
  supersedes it.
