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
- [~] **The domain is being replaced.** `esim.coach` serves a TLS certificate that does
  not match the hostname, so the site is unreachable over HTTPS. The repo carries no
  host config (no `_headers`, no `netlify.toml`) to say which deploy option was
  chosen. Decide, then wire it.

## Launch plan — where it actually stopped

- [x] Day 1, build the skeleton — done, locally.
- [ ] Day 1, deploy — never happened. See the domain and remote items above.
- [~] **Day 2, real plan data.** `data/config.json` has a real published-Sheet CSV
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

- [x] **[!] The pin contradicted the disclosure, twice.** Settled 2026-09-03.
  `config.json` sets `pin_providers: ["Honest Mobile"]`, which puts all three Honest
  Mobile plans at ranks 1-3 with "Top pick" ribbons. Meanwhile `about.html` says
  ranking is "driven only by the value maths" and `affiliate-disclosure.html` says
  commercial relationships have "no bearing on where its plans appear". This is a
  disclosure problem, not a wording nitpick. Either drop the pin, or label it as
  placement and rewrite both pages.
- [x] **"Top pick" was overloaded** — the same badge marks the pinned provider and
  reads as an editorial verdict. No separate sponsored/featured styling exists.
- [~] **The site would publish two-month-old sample prices under a "refreshed daily"
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

## Session 2026-09-03 — what changed

**The host question is answered: GitHub Pages, already connected.** `esim.coach`
serves a working site over plain HTTP right now, and the response headers say
`server: GitHub.com`. So Option C in `prompts/07-deploy.md` was taken at some
point, the `CNAME` file is doing its job, and the repo is already wired to Pages.
Nothing new to sign up for and nothing to pay for. The site it serves is the
October 2025 eSIMRanker scaffold, because the July build has never been pushed.

**HTTPS fails because of one stray DNS record.** `esim.coach` resolves to five A
records: the four correct GitHub Pages IPs (`185.199.108-111.153`) plus
`192.64.119.69`, which is Namecheap parking. Requests that land on the fifth get
Namecheap's certificate, which is the hostname mismatch, and its presence also
stops GitHub completing its own certificate. Nameservers are
`dns1/dns2.registrar-servers.com`, so the domain sits on Namecheap BasicDNS.
Fix: delete that one A record, add `www` as a CNAME to `mistertyr.github.io`,
then re-save the custom domain in repo Settings → Pages and tick Enforce HTTPS.

**The July rebuild is committed but not pushed.** Working tree is clean, seven
commits sit on top of `ef64adb`, and both `.github/` and `Archive Build/` are
tracked. So a stray `git clean -fd` can no longer erase anything. But `origin`
still has none of it, so the only copy is this Mac until someone runs
`git push origin main`. That push is also what replaces the live 2025 site.

**The Google Sheet works.** Fetched the published CSV directly: HTTP 200, 22 data
rows, correct headers. It has simply never held anything but the July sample data
- same rows, same `2026-07-08` timestamps, every `product_url` still carrying
`ref=YOUR_AFFILIATE_ID`. Providers in it: Airalo 8, Honest Mobile 3, Nomad 3,
Holafly 2, Saily 2, Sim Local 2, Jetpac 1, SMARTY 1. So the pipeline is sound and
the sheet is the right place to put real prices. Note the generator can only reach
it with working network - it fails to the local sample CSV otherwise, quietly.

**The pin is now disclosed rather than hidden.** Decision: Honest Mobile keeps the
top three slots as paid placement, and the site says so. Implemented:
- `update_plans.py` records `value_rank` before placement is applied, and awards
  `top_pick` to the plan that wins on value alone. That badge cannot be bought.
- `build_static.py` renders two separate labels: green "Top pick" for merit,
  neutral outlined "Paid placement" for the pinned slots. A plan can carry both,
  and Honest Mobile's Smart SIM Global currently does, honestly.
- `styles.css` gains `.ribbons`, `.ribbon-top` and `.ribbon-paid`; `.card.featured`
  becomes `.card.top-pick` and `.card.placement`.
- `content.py` rewrites the "How we're funded" paragraph in about.html and the
  "How it affects rankings" answer in affiliate-disclosure.html to state the paid
  arrangement plainly.

**The refresh claim is out until it is true.** The hero read "Updated <today>" from
the clock, so it would have claimed today's date over July prices on every build.
It now reads "Prices last checked 08 Jul 2026", taken from the newest `timestamp`
in `plans.json`. The footer's "Data refreshed daily" is removed until the daily
Action has actually run once.

## Still open after this session

- [ ] Push. `git push origin main` from Marty's own terminal - the sandbox has no
  GitHub credentials. Nothing above reaches the public until this happens.
- [ ] Delete the `192.64.119.69` A record at Namecheap, add the `www` CNAME, then
  re-save the custom domain in Settings → Pages and enable Enforce HTTPS.
- [ ] `site.description` in `config.json` still says "refreshed daily", and it goes
  into the meta description and og:description of every page. Same claim, same
  problem, not yet fixed.
- [ ] Apply to Airalo, Nomad, Holafly and Saily the day the site is reachable.
- [ ] Put real prices in the Sheet, then verify a few against the providers' live
  sites before publishing.
- [ ] Set `SHEET_CSV_URL` as a repo secret so the Action can read the Sheet.
- [ ] Widen the Action's `git add` so subdirectories publish.
- [ ] Derive the sitemap list from `PAGES` so a page cannot ship unlisted.
- [ ] `.gitignore.html` is still tracked and would deploy as a page.

## Raised by Marty, 2026-09-03

- [x] **[!] The domain name needed rethinking.** Marty does not like `esim.coach`.
  Find alternatives before the DNS and HTTPS work is finished, because redoing it
  later costs more than doing it now. What a change touches: the `CNAME` file at the
  repo root, `site.base_url` in `data/config.json`, `SITE_BASE_URL` in the Action,
  the A records and `www` CNAME at Namecheap, the custom domain in repo Settings →
  Pages, and every absolute URL already written into `sitemap.xml`. None of it is
  hard, but all of it has to move together. Worth checking availability and price on
  a shortlist first, and worth deciding whether to keep `esim.coach` pointed at the
  new name as a redirect rather than dropping it.

- [ ] **[!] Capture every UK eSIM deal, not a hand-typed sample.** The Sheet holds 22
  rows across 8 providers, all entered by hand, all dated 8 July. That does not
  scale and it will drift out of date between edits. Two separate questions to
  settle before building anything:
  - Scope. "UK eSIM deals" can mean plans for visitors coming to the UK, plans for
    UK travellers going abroad, or both. The site is currently built around the
    second. The answer changes which providers matter and which pages get written.
  - Source. Options, roughly cheapest first: keep the Sheet but widen it to every
    provider worth listing and set a review cadence; pull structured feeds from the
    affiliate networks once the four applications are approved, since most publish
    product data; or scrape provider pricing pages on a schedule, which is the most
    complete and by far the most fragile. A feed-plus-Sheet hybrid is probably the
    realistic answer, with the Sheet as the override layer for anything a feed gets
    wrong.
  - Either way the pipeline already reads a CSV and does not care where it came
    from, so this is a source problem rather than a rebuild.

## Domain decision, 2026-09-03

**Chosen: `esimsorted.co.uk`.** Confirmed available at the registry (Nominet RDAP)
on 3 September. `esimsorted.com`, `.uk`, `.net`, `.org` and `.org.uk` are all free
too.

**Buy `.co.uk` and `.com` together, skip the rest.** About $15.40 a year for the
pair at registry-standard pricing. `.co.uk` is canonical because the audience and
the operator are both UK. The `.com` is worth $11 as a defensive hold and because
the UK-inbound half of the audience (Americans searching for a UK eSIM) trusts a
`.com`. Point it at the canonical with a free URL redirect in Namecheap's DNS,
since GitHub Pages only accepts one custom domain.

**Let `esim.coach` lapse.** It registers cheap and renews at $62.31 a year against
$11.08 for a `.com` and $5.66 for a `.co.uk`. Nothing public links to it and it has
no traffic to preserve, so there is no case for paying five times the going rate to
keep a redirect alive.

**Scope decided at the same time.** The site is built for the UK traveller going
abroad, and that stays the spine: the homepage, the destination guides, and all four
affiliate programmes are outbound products. A UK-inbound section comes next as a
deliberate content cluster rather than an afterthought, because that is the only
part of this market where a UK-run site has an edge worth having. The Sheet already
carries the inbound products without the site admitting it - SMARTY, Sim Local's UK
80GB on EE, and two of Honest Mobile's three plans are UK plans.

### Rename checklist - all of it moves together

- [ ] Buy `esimsorted.co.uk` and `esimsorted.com` at Namecheap.
- [ ] **[!] Decide the brand name.** The domain change orphans "eSIM Coach". If it
  becomes "eSIM Sorted" then `site.brand` in `data/config.json`, the logo at
  `assets/img/logo.png`, every page title and the three legal pages all need to
  follow. Not decided yet.
- [ ] `CNAME` at the repo root: replace `esim.coach` with the new hostname.
- [ ] `site.base_url` in `data/config.json`.
- [ ] `SITE_BASE_URL` in `.github/workflows/update.yml`.
- [ ] `site.description` in `data/config.json` - drop "refreshed daily" while
  editing it, since the same false claim rides into the meta description and the
  Open Graph description of every page.
- [ ] Namecheap DNS on the new domain: four A records to `185.199.108-111.153`,
  `www` as a CNAME to `mistertyr.github.io`. Do not repeat the stray parking A
  record that broke HTTPS on `esim.coach`.
- [ ] Repo Settings → Pages: set the custom domain, wait for the certificate, then
  enable Enforce HTTPS.
- [ ] Rebuild so `sitemap.xml` and every absolute URL pick up the new base.
- [ ] Namecheap URL redirect on the `.com` pointing at the canonical.

**Do not do the old `esim.coach` DNS fix.** Deleting the `192.64.119.69` record and
issuing a certificate for a domain being abandoned is wasted work. The push to
GitHub is still worth doing today - it is the backup, and it does not depend on
which domain wins.

## Provider scouting, 2026-09-03

Started the longer provider list in `data/PROVIDER-SCOUTING.md`. Eight providers is
not a comparison site. Three tiers: apply now, add for coverage, and the UK-inbound
cluster for later.

- [ ] Apply to Airalo, Nomad, Holafly and Saily, plus Jetpac and Ubigi, the day the
  site is reachable.
- [ ] **Join Awin the same day.** It already carries Breeze eSIM UK, WorldSIM,
  eSIMania and Esim Prime, so one UK account reaches several merchants instead of
  chasing each in-house programme. Small joining deposit, refunded against earnings.
- [ ] Widen the Sheet to BNESIM, aloSIM, GigSky, Yesim and Roamless next, then work
  down the Tier 2 list.
- [ ] Record hotspot policy per plan. Holafly caps tethering and it is the most
  common complaint about travel eSIMs, so it belongs in the data rather than in a
  footnote. The Sheet has no column for it yet.
- [ ] Nothing from the scouting list goes in the Sheet until the price is checked on
  the provider's own site, with the date recorded in `timestamp`.

## Session 2026-09-04 — the rename, and why nothing has ever published

**GitHub Pages has been switched off the whole time.** The repo is private on a
free GitHub plan, and free-tier Pages only works on public repos. Settings →
Pages says so in as many words: "Upgrade or make this repository public to
enable Pages." So `main` has been correct since 2 September, the daily Action has
run and committed twice, and none of it has ever reached the web. What
`esim.coach` serves is a stale deployment of the October 2025 eSIMRanker
scaffold, left over from whenever Pages last built — GitHub still offers an
"Unpublish" button for it.

This also explains the earlier HTTPS diagnosis being a dead end. The stray
`192.64.119.69` A record is real, but even with perfect DNS the site would have
served the 2025 scaffold, because nothing was rebuilding it.

That stale page is an honesty problem while it stands. Its affiliate disclosure
says "Affiliate partners cannot pay for preferential placement", which stopped
being true the moment the Honest Mobile pin went in.

- [ ] **[!] Make the repo public, or pay for GitHub Pro** (~$4/month) to keep it
  private. Scanned the tracked files first: nothing sensitive beyond
  `hello@esim.coach` in the archived legal pages. `SHEET_CSV_URL` is a proper
  Actions secret. The plain-text Sheet URL in `data/config.json` is a
  publish-to-web link, already readable by anyone holding it, so going public
  costs obscurity rather than security. Recommendation: make it public.
- [ ] Once Pages is enabled, the old deployment needs replacing or unpublishing.

**The disclosure fix was already pushed.** `origin/main` is at `3d651aa`,
working tree clean, nothing left uncommitted from 3 September. Verified against
`origin/main` rather than the local copy. It just isn't visible to anyone.

### The rename is done locally — 28 files changed, not committed

- [x] `CNAME` → `esim-sorted.co.uk`. **Note the hyphen.** Marty registered the
  hyphenated form, not the `esimsorted.co.uk` this tracker had planned. Every
  reference below uses the hyphenated one.
- [x] `site.brand` → "eSIM Sorted". Brand decided.
- [x] `site.base_url` → `https://esim-sorted.co.uk`.
- [x] `site.description` rewritten, "refreshed daily" gone. It rode into the meta
  description and og:description of all eight pages; those are rebuilt.
- [x] `SITE_BASE_URL` and the bot name in `.github/workflows/update.yml`.
- [x] "eSIM Coach" replaced through `content.py`, the prompt pack, `README.md`,
  `LAUNCH-PLAN.md`, `automation/email-sequence.md` and the script docstrings.
- [x] **Cut the untrue disclosure line.** The claim that the paid placement is
  "open to any provider on the same terms" is gone from `content.py` and the
  rendered page. Marty confirmed it was not true.
- [x] Found and cut a second false refresh claim: `about.html` still said "The
  data refreshes daily" in the ranking explanation.
- [x] Rebuilt. 19 plans, 7 content pages, sitemap and robots regenerated.

Still open on the rename:

- [ ] **The logo.** Marty is supplying a new image rather than having one
  generated. `assets/img/logo.png` is untouched and still says "eSIM Coach".
- [ ] **The colour scheme.** Marty supplied a palette: Desert Sand `#ECC8AF`,
  Powder Blush `#E7AD99`, Dusty Rose `#CE796B`, Toasted Almond `#C18C5D`, Blue
  Slate `#495867`. Applied to the real plan cards in a preview artifact for him
  to choose light or dark ground. Worth knowing: none of the four warm colours
  pass WCAG AA for body text on a light background — Dusty Rose is the best at
  3.0 against 4.5 needed — so on a light site they can only be fills and edges,
  with Blue Slate carrying the type. All four pass on a dark ground.
- [ ] Buy the `.com` as a defensive hold and redirect it. Not bought yet.
- [ ] Namecheap DNS on `esim-sorted.co.uk`: four A records to
  `185.199.108-111.153`, `www` as a CNAME to `mistertyr.github.io`. Do not repeat
  the stray parking A record.
- [ ] Repo Settings → Pages: set the custom domain, wait for the certificate,
  enable Enforce HTTPS. Blocked on the repo being public.

### Traps closed this session

- [x] **The Action's `git add` missed subdirectories.** Now
  `git add plans.json sitemap.xml '*.html'` — the quoted glob matches at any
  depth, so a future `/guides/` folder will publish.
- [x] **The sitemap list was hardcoded separately from `PAGES`.** `write_sitemap`
  now derives it from `content.PAGES`, so a page cannot ship unlisted.
- [x] **`robots.txt` had `esim.coach` hardcoded and was not generated.** It would
  have pointed search engines at a dead sitemap after the rename. `build_static.py`
  now writes it from `base_url`.

Still open:

- [ ] Auto-push with no review. The workflow holds `contents: write` and pushes
  straight to main. Once the Sheet holds real prices, a bad spreadsheet edit goes
  live unattended the next morning.
- [ ] `Archive Build/` still committed, 21 files.

### Research folded in — 2026-09-04

Marty supplied a market research document covering UK outbound and UK inbound.
Filed as `data/MARKET-RESEARCH-2026-09.md`, with the parts that change the build
written up at the end of `data/PROVIDER-SCOUTING.md`. Nothing in it is verified,
so nothing goes in the Sheet until checked against the provider.

The sharpest finding is a correctness problem rather than a missing column:

- [ ] **"Unlimited" is not one thing, and the ranking treats it as though it is.**
  Ubigi's UK unlimited runs 25GB at full speed over seven days, then 2Mbps; the
  30-day gives 60GB. `update_plans.py` ranks unlimited plans on price per day, so
  a throttled plan and an uncapped one at the same price rank identically today.
  Fix needs `full_speed_gb` and `post_cap_speed` in the Sheet, then rank capped
  "unlimited" plans on price per full-speed GB.
- [ ] **Add a `voice_type` column** — `native` / `app_voip` / `external_voip` /
  `none`. Most comparison sites lump data-only in with voice-capable plans. A
  "includes calls" filter is something the big sites do not offer, and in places
  like the UAE where VoIP is restricted the distinction is a real one.
- [ ] Nine proposed Sheet columns in total, listed in `PROVIDER-SCOUTING.md`. The
  research suggests about thirty; nine is what a hand-maintained Sheet survives.
- [ ] **Pull three providers forward**: Orange Travel (the strongest data + calls
  + SMS product found, and it sells a UK visitor eSIM too, so it sits in both
  clusters), Rewild Mobile (UK-based, cheapest on 1–10GB across most destinations
  in the July 2026 Which? comparisons), and Three UK PAYG (£10 for 40GB UK plus
  6GB roaming across 70+ destinations with unlimited qualifying calls and texts in
  Europe — nothing in the travel-eSIM set matches it, and no travel-eSIM
  comparison site lists it).
- [ ] The inbound cluster should not restrict itself to products marketed as
  travel eSIMs. EE's UK Travel eSIM is data-only at £15 for 7 days; O2 PAYG is £10
  for 10GB with unlimited UK calls, texts and a real +44 number. That gap is the
  edge a UK-run site has.

### What needs Marty, in order

1. Make the repo public (or upgrade). Nothing else reaches the web until this.
2. Supply the logo, and pick light or dark from the palette preview.
3. Namecheap DNS on `esim-sorted.co.uk`, then the custom domain in Settings → Pages.
4. Apply to Airalo, Nomad, Holafly, Saily, Jetpac, Ubigi and Awin the day it resolves.
5. Set `SHEET_CSV_URL` as a repo secret.

## Session 2026-09-04, second sitting — logo, light theme, real prices

The rename commit and the tracker update were both pushed before this session
started. `origin/main` is at `b172bcd`. The "Marty has to push it" item from the
last handover is done.

### The light rebuild is in

Marty supplied the logo: a horizontal lockup, dark type on transparent, in three
of the five palette colours — Blue Slate `#495867`, Dusty Rose `#CE796B`,
Toasted Almond `#C18C5D`. It was split into three files: `logo.png` (the full
lockup with the tagline, used for social sharing), `logo-wordmark.png` (no
tagline, used in the header) and `favicon.png` (the thumbs-up mark, square).
The header no longer prints the brand name beside the logo, because the logo
already contains it.

**That settled the light-or-dark question.** Dark type on a dark navy ground is
invisible, so the site went light. Blue Slate carries the type; the warm colours
are fills, edges and accents. One addition to the palette: **Dusty Rose is
darkened to `#A85647` wherever white text sits on it**, because pure `#CE796B`
only reaches 3.2:1 against white and body text needs 4.5. The pure colour is
still used for borders and the Top pick card edge, where nothing has to be read
off it.

The two badges stay distinct in shape as well as colour: "Top pick" is a solid
rose pill, "Paid placement" is a square outlined tag. That difference survives
being printed in black and white.

### The ranking bug is fixed, and the research changed the fix

`full_speed_gb` alone was not enough. Most providers cap **per day**, not per
plan — Airalo 3GB/day, Saily 5GB/day, Nomad 2GB/day — while Ubigi caps the whole
plan. Written as a bare number those look alike and are nothing like each other.

- `full_speed_period` (`per_day` / `per_plan`) is now in the schema. A per-day cap
  is multiplied by validity, so Airalo's 30-day unlimited scores as 90GB.
- `score_value` now ranks in three tiers: anything with a real full-speed GB
  figure on price per GB, genuinely uncapped plans below them on price per day,
  incomplete rows last. Marty chose "rank uncapped last" over assuming a usage
  figure.
- Nine more columns are in the pipeline and documented in `SHEET-SETUP.md`:
  `direction`, `voice_type`, `calls_included`, `sms_included`, `number_country`,
  `full_speed_gb`, `full_speed_period`, `post_cap_speed`, `hotspot`, `source_url`.
- The card now says "Unlimited, 3GB a day at full speed" and carries short plain
  lines about throttling, calls and hotspot limits.
- `about.html` and `affiliate-disclosure.html` were rewritten to describe the new
  ranking. They both still said "price per GB, or price per day for unlimited",
  which stopped being true the moment this landed.

### The daily Action can no longer publish rubbish

`update_plans.py` checks the data before it writes anything, and leaves the
published files untouched if a check fails. Limits live in `checks` in
`config.json`. The most valuable one: **if the Sheet returns nothing and the run
is about to publish the local sample file, it stops.** That was the failure
nobody would have noticed. Verified working — the run refuses on this machine,
which has no network. Use `ALLOW_SAMPLE_DATA=1` to build from the sample on purpose.

### Prices checked against providers, and one big problem

Full write-up in `data/PRICE-CHECK-2026-09-04.md`. Verified rows are in
`data/verified/`. **Nothing has been loaded into the Sheet.**

- [ ] **Most of it is not in pounds.** The checks ran from a US connection and
  nearly every travel eSIM company sets currency client-side, so Nomad, Holafly,
  Saily, Jetpac, Ubigi, Orange and Sim Local all came back in dollars or euros.
  Real prices, wrong currency, and converting them ourselves would be inventing a
  number. **A second pass from a UK browser is the next job.** All the structure
  is preserved, so it only needs the price column re-read.
- [x] **Airalo, 25 rows in real GBP.** Their site honours `?currency=GBP`.
- [x] **The UK networks in real GBP** — Three, SMARTY, Honest Mobile, O2,
  giffgaff, EE.
- [ ] **Honest Mobile's Sheet rows are wrong, and they are the paid placement.**
  Smart SIM is £3.75 a month, not £45 a year, and it is an app-limited backup
  with no calls, texts or number. Classic is £12.15 / £17.50 / £25.00. They also
  show a lower "loyalty" price on every plan — decide which to display.
- [ ] **Airalo has stopped selling sized plans** on Japan, Europe, USA and
  Thailand. Unlimited only now.
- [ ] **Holafly publishes no throttle figure anywhere.** They cannot be listed as
  uncapped or as capped. Their rows need a card that says the limit is
  unpublished. Hotspot is capped at 1GB a day, confirmed.
- [ ] **EE's UK Travel eSIM cannot call 999.** Their own terms. Any inbound page
  has to say so.
- [ ] **The Three £10 claim was half right.** 40GB UK, 70+ destinations and
  unlimited calls and texts all hold, but the roaming data is only 6GB and every
  Three PAYG pack is speed-capped at 25Mbps from the first byte.
- [ ] **Rewild Mobile could not be verified at all.** Their pricing is behind a
  JavaScript picker. The "cheapest on 1–10GB" claim rests only on roundups.
- [ ] Affiliate rates confirmed from providers' own sites: Airalo 10% via Impact,
  Ubigi 10% / 60-day cookie via Impact, Saily 15% in-house, Jetpac "up to 15%",
  Nomad on Impact but rate unpublished, **Holafly publishes no rate at all**.
  These replace the roundup figures in `PROVIDER-SCOUTING.md`.

### Destination guides written

`esim-japan.html`, `esim-europe.html`, `esim-usa.html`, `esim-thailand.html`.
Deliberately light on prices — this site has already been burned by claims that
stopped being true, so the guides explain how the products differ and send people
to the live table for numbers. Linked from a strip under the homepage filters and
from the footer. The sitemap picks them up automatically now.

### Housekeeping done

- [x] `utm_source` hyphenated to `esim-sorted` to match the domain.
- [x] `Archive Build/` removed from the working tree and untracked. Still in
  history at `57ba2f7` if it is ever wanted.

### Still needing Marty, in order

1. **Make the repo public** (or pay for Pro). Nothing reaches the web until this.
2. Namecheap DNS on `esim-sorted.co.uk`, then the custom domain in Settings →
   Pages. Four A records to `185.199.108-111.153`, `www` CNAME to
   `mistertyr.github.io.`, and do not repeat the stray parking record.
3. Set `SHEET_CSV_URL` as a repo secret.
4. Apply to Airalo, Nomad, Holafly, Saily, Jetpac, Ubigi and Awin.
5. Decide whether UK network plans belong in the same ranking as travel eSIMs.
   SMARTY does 100GB for £12, which is 12p a GB against Airalo's best of about
   60p, so dropped in as-is they would take every top slot. The `direction`
   column can split them. This should be a choice, not an accident.
6. Buy the `.com` and redirect it.
