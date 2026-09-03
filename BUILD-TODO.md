# eSIM Coach — build tracker

Created 2026-09-02 from an audit of the repo. There was no tracker before this;
`LAUNCH-PLAN.md` is a seven-day plan written 8 July that the project never started,
and `README.md` describes the intended system rather than the current state.

Convention: `[x]` done, `[~]` in progress, `[ ]` open, `[!]` needs a decision.

## Safety pass — 2026-09-02

Version control only; no feature work, nothing generated, no importer run.

The July rebuild is committed and pushed. It went up as seven commits rather than
one, so the history reads as what happened: `.gitignore` and the tracked `.DS_Store`
files, then `Archive Build/`, then the data pipeline, then the site rebuild, then
the removal of the superseded automation, then the workflow, then the planning docs.
`Archive Build/` deliberately precedes the deletions.

What is still open here is deployment, not preservation: the domain, the Sheet
secret, and the auto-push-with-no-review trap below.

## Current state (2026-09-02)

The build is genuinely finished and the launch is genuinely not started. Every
generated file on disk dates from 9 July 2026.

- Generator works end to end: `scripts/update_plans.py` (reads sources from
  `data/config.json`, normalises, computes GBP/GB and GBP/day, ranks, writes
  `plans.json` and `sitemap.xml`), `scripts/build_static.py` (renders `index.html`
  and every page from `content.py`), `scripts/content.py` (four evergreen articles,
  three legal pages).
- On disk: `index.html` with 19 plan cards and a working region filter, 7 content
  pages, `sitemap.xml` (8 URLs), `robots.txt`, `CNAME`, styles, logo.
- Supporting material: a 7-file `prompts/` pack, a 4-email welcome sequence in
  `automation/`, `data/SHEET-SETUP.md`, and a daily GitHub Action at
  `.github/workflows/update.yml` (06:17 UTC, rebuild and auto-commit).
- Plan data is the 19-row sample set. No real prices have ever been loaded.

## Blocking — do these first

- [x] **[!] Commit the July rebuild** — 2026-09-02. Seven commits on top of
  `ef64adb`, pushed to `origin/main` as `a53b4be`. `Archive Build/` went in FIRST,
  before the deletions, so the originals are recoverable two ways.
  - The deletions themselves are safe: `automation/n8n/flow.json`,
    `google_sheets/apps_script.gs`, `data/sources/*` and `terms.md` all survive
    inside `Archive Build/`, and the old logo was renamed to `assets/img/logo.png`.
    But that safety net is untracked too.
- [x] **The remote serves the wrong site** — fixed 2026-09-02. `origin/main` is now
  `a53b4be`. Verified against the GitHub API rather than trusting the push: the July
  files (`about.html`, `data/config.json`, the HTML policy pages, `robots.txt`,
  `sitemap.xml`, `prompts/`) all resolve on the remote, and the superseded ones
  (`automation/n8n/flow.json`, `google_sheets/apps_script.gs`, `privacy-policy.md`,
  `terms.md`) all 404.
- [x] **`.github/` is untracked** — fixed 2026-09-02. `update.yml` is on the remote
  and confirmed present there.
- [ ] **[!] Set `SHEET_CSV_URL`** in Settings -> Secrets and variables -> Actions.
  Until it is set the daily Action runs against the sample CSV, so it will "succeed"
  daily while publishing nothing real. The workflow is live now, so this matters.
- [ ] **The domain is unattached.** `esim.coach` serves a TLS certificate that does
  not match the hostname, so the site is unreachable over HTTPS. The repo carries no
  host config (no `_headers`, no `netlify.toml`) to say which deploy option was
  chosen. Decide, then wire it.

## Launch plan — where it actually stopped

- [x] Day 1, build the skeleton — done, locally.
- [ ] Day 1, deploy — never happened. See the domain and remote items above.
- [ ] **Day 2, real plan data.** `data/config.json` has a real published-Sheet CSV
  URL as the *primary* source with `enabled: true`, yet `plans.json` is still the 19
  sample rows. So the Sheet has either never been pulled or returned nothing. One
  run finds out which.
- [ ] **Day 3, affiliates.** All 19 `product_url` values still carry
  `ref=YOUR_AFFILIATE_ID`. Nothing suggests any programme was applied to. Approvals
  take days, so this should start the day the site is reachable, not after the
  content work. LAUNCH-PLAN names Airalo, Nomad, Holafly and Saily.
- [ ] **Day 4, content.** `content.py` holds only the four evergreen pages and the
  legal set. No destination guides (Japan, Europe, USA, Thailand) despite those
  being the whole SEO plan.
- [ ] **Day 5, SEO.** No analytics tag and no Search Console verification meta in
  any generated page.
- [ ] **Day 6, email.** The 4-email sequence is written; there is no signup form
  anywhere on the site and nothing connects to an email tool.
- [ ] Day 7, automate and check — blocked on everything above.

## Honesty problems

- [ ] **[!] The pin contradicts the disclosure, twice.**
  `config.json` sets `pin_providers: ["Honest Mobile"]`, which puts all three Honest
  Mobile plans at ranks 1-3 with "Top pick" ribbons. Meanwhile `about.html` says
  ranking is "driven only by the value maths" and `affiliate-disclosure.html` says
  commercial relationships have "no bearing on where its plans appear". This is a
  disclosure problem, not a wording nitpick. Either drop the pin, or label it as
  placement and rewrite both pages.
- [ ] **"Top pick" is overloaded** — the same badge marks the pinned provider and
  reads as an editorial verdict. No separate sponsored/featured styling exists.
- [ ] **The site would publish two-month-old sample prices under a "refreshed daily"
  claim.** Plan rows are timestamped 2026-07-08, the footer says "Data refreshed
  daily" and the hero says "Updated 09 Jul 2026".

## Housekeeping and small traps

- [ ] Adding an article takes two edits in two files — `PAGES` in `content.py` and
  the hardcoded list in `write_sitemap()`. Easy to forget the second and ship an
  unlisted page. Derive one from the other.
- [ ] The Action's commit step is `git add plans.json sitemap.xml index.html *.html`,
  which will not pick up anything in a subdirectory. A future `/guides/` folder would
  silently never publish.
- [x] `Archive Build/` — decided 2026-09-02: kept and committed as-is (21 files,
  128KB) in `57ba2f7`, before the deletions landed. Safe to delete from the working
  tree whenever you trust the history; the files are in both places until then.
- [x] `.gitignore.html` — deleted 2026-09-02. It was a gitignore body saved with an
  `.html` extension, tracked, and would have deployed as a page. Recoverable from
  history if it turns out to have been wanted.
- [ ] **Auto-push with no review.** The workflow holds `contents: write` and pushes
  straight to main, and the Sheet URL is committed in plain text. Once the Sheet is
  wired, a bad spreadsheet edit goes live unattended and anyone with the repo can
  read the source URL.
