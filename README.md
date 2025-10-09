# eSIMRanker — Autonomous Affinity Engine (Plug‑and‑Play)

A fully automated, low‑maintenance **eSIM deals** hub. Pulls plan data from CSV/APIs, normalizes, ranks (best value), rebuilds a static site, and syndicates a weekly roundup. Designed to run for **90+ days unattended**.

## What’s inside
- `site/` — static site (no DB). Renders from `site/plans.json` and simple HTML pages.
- `scripts/update_plans.py` — fetches sources → normalizes → computes value metrics → ranks → writes JSON + sitemap.
- `scripts/build_static.py` — renders homepage grid from the latest JSON; writes evergreen pages links.
- `.github/workflows/update.yml` — daily cron to refresh + commit.
- `automation/n8n/flow.json` — weekly email + social autopost (top plans by region).
- `automation/mailer/automation.md` — 4‑email evergreen sequence.
- `google_sheets/apps_script.gs` — optional Sheet consolidator for feeds.
- `data/sources/config.json` — toggle sources; set ranking rules; set site brand.

## One‑time setup (≈20–40 mins)
1) Create a **private GitHub repo** and add these files.
2) Enable hosting:
   - **Netlify** / **Cloudflare Pages**: deploy `/site` (no build step).
   - **GitHub Pages**: serve `/site` from the repo.
3) Add **Repo → Settings → Secrets and variables → Actions**:
   - `SITE_BASE_URL` e.g. `https://esimranker.example`
4) Edit `data/sources/config.json`:
   - Point the starter Google Sheet CSV (or keep local sample on). 
   - Replace `YOUR_AFFILIATE_*` placeholders.
5) Commit. The **daily cron** will update `plans.json`, `sitemap.xml`, and `index.html` automatically.

## Local dev
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
python scripts/update_plans.py
python scripts/build_static.py
open site/index.html
```

## Notes
- You can add more providers (Airalo, Nomad, Holafly, etc.) by feeding their CSV/API into the Sheet.
- Pricing currency normalization defaults to USD; set `currency_display` in config if you prefer GBP/EUR.
- Evergreen pages included: `what-is-esim.html`, `how-to-install-esim.html`, `why-esim.html`.
