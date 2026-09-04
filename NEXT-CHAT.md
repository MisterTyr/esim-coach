# Prompt for the next eSIM Sorted chat

Name the chat: **eSIM Sorted — brand, deploy and affiliate applications**

This is the eSIM Sorted project (renamed from eSIM Coach on 4 September). The
repo is at `~/git-repos/esim-coach` — the folder name still says coach, the
site does not. Connect that folder, not the old copy in
`~/Documents/Claude/Projects/esim-coach`, which is iCloud-synced and became
unreadable. Do not run two Cowork sessions against the same repo.

Read `BUILD-TODO.md` first, then `data/PROVIDER-SCOUTING.md` and
`data/config.json`.

## The one thing that explains everything

**GitHub Pages has never published this site.** The repo is private on a free
GitHub plan, and free-tier Pages only works on public repos — Settings → Pages
says "Upgrade or make this repository public to enable Pages." So `main` has
been correct since 2 September, the daily Action runs and commits fine, and
nothing has ever reached the web. `esim.coach` serves a stale October 2025
eSIMRanker deployment left over from before.

That stale page is a live honesty problem: its disclosure says "Affiliate
partners cannot pay for preferential placement", which stopped being true when
the Honest Mobile pin went in.

Nothing else on this list matters until Marty makes the repo public, or pays
for GitHub Pro to keep it private. A scan found nothing sensitive in the tracked
files. He was told this on 4 September and it is his click to make.

## Done on 4 September — do not redo

- The rename is committed as `adf1c03`. Domain `esim-sorted.co.uk` (**hyphenated**
  — the tracker's earlier `esimsorted.co.uk` plan is superseded), brand
  "eSIM Sorted", `CNAME`, `base_url`, `SITE_BASE_URL` and the rebuild all moved
  together.
- The untrue disclosure line is cut. It claimed the paid placement was "open to
  any provider on the same terms"; Marty confirmed it was not. A second false
  "data refreshes daily" claim in `about.html` went with it.
- Three silent-failure traps closed: the Action's `git add` now uses a quoted
  glob so subdirectories publish; `write_sitemap` derives from `content.PAGES`;
  `robots.txt` is generated from `base_url` instead of carrying a hardcoded
  domain.
- **The commit is local. Marty has to push it** — no GitHub credentials in the
  sandbox.

## Open, roughly in order

1. **Repo public**, then Settings → Pages → custom domain, then the Namecheap
   records. GitHub's docs are explicit that the custom domain goes in the repo
   settings *before* DNS, to close a takeover window. Records are four A records
   on `@` to `185.199.108-111.153` plus `www` CNAME to `mistertyr.github.io.` —
   and delete Namecheap's default parking records, which is precisely what broke
   HTTPS on `esim.coach`.
2. **The logo.** Marty is supplying the image himself. `assets/img/logo.png`
   still says "eSIM Coach".
3. **The colour scheme.** Marty's palette: Desert Sand `#ECC8AF`, Powder Blush
   `#E7AD99`, Dusty Rose `#CE796B`, Toasted Almond `#C18C5D`, Blue Slate
   `#495867`. A preview artifact applies it to the real plan cards in both a
   light and a dark treatment; he had not picked when the session ended. The
   constraint that decides it: none of the four warm colours pass WCAG AA for
   body text on a light ground (Dusty Rose is best at 3.0 against 4.5), so on a
   light site they can only be fills and edges with Blue Slate carrying the type.
   All four pass on dark. Keep the "Top pick" and "Paid placement" badges
   visibly distinct in shape as well as colour — that difference is doing real
   work now the placement is disclosed.
4. **Apply to the affiliate programmes the day the domain resolves.** Airalo,
   Nomad, Holafly, Saily, Jetpac, Ubigi, and join Awin (one UK account reaches
   Breeze eSIM UK, WorldSIM, eSIMania and Esim Prime). Approvals are the only
   clock Marty does not control.
5. **Real prices in the Sheet.** It has only ever held the July sample — 22 rows,
   all timestamped 2026-07-08, every `product_url` still `ref=YOUR_AFFILIATE_ID`.
   Check every price on the provider's own site before it goes in.
6. **Set `SHEET_CSV_URL` as a repo secret**, then watch one Action run.
7. Buy the `.com` as a defensive hold and redirect it.

## From the research folded in on 4 September

Marty's market research is at `data/MARKET-RESEARCH-2026-09.md`; the parts that
change the build are written up at the end of `data/PROVIDER-SCOUTING.md`.
Nothing in it is verified — none of it reaches the Sheet until checked against
the provider.

- **"Unlimited" is not one thing, and the ranking treats it as though it is.**
  Ubigi's UK unlimited gives 25GB at full speed over seven days then 2Mbps.
  `update_plans.py` ranks unlimited plans on price per day, so a throttled plan
  and an uncapped one at the same price rank identically today. This is a
  correctness bug in the value engine, not a missing column. Needs
  `full_speed_gb` and `post_cap_speed`.
- **A `voice_type` column** (`native` / `app_voip` / `external_voip` / `none`)
  is the differentiator worth building around. No large comparison site offers
  an "includes calls" filter.
- **Three providers to pull forward**: Orange Travel, Rewild Mobile and Three UK
  PAYG. Three's £10 PAYG — 40GB UK plus 6GB roaming across 70+ destinations with
  unlimited qualifying calls and texts in Europe — beats the travel-eSIM set for
  a UK traveller, and no travel-eSIM comparison site lists it.

## Traps still open

- The workflow holds `contents: write` and pushes straight to main with no
  review, and the Sheet URL is committed in plain text. Once the Sheet holds real
  prices, a bad spreadsheet edit goes live unattended the next morning.
- `Archive Build/` is committed and kept, 21 files of old scaffold.
- The old `~/Documents/Claude/Projects/esim-coach` folder still exists and can be
  deleted once the clean clone is trusted.

## Working rules

- Ask before writing code and before anything that changes what the public sees.
- Verify prices against the providers rather than trusting the sheet or the sample.
- Plain English, British spelling.
- Update `BUILD-TODO.md` in the same session and say what to tick off on the board.
