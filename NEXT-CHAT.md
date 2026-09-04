# Prompt for the next eSIM Coach chat

Name the chat: **eSIM Coach — deploy and monetise**

Written 4 September 2026, replacing the version from 2 September. The repo has
moved. It now lives at `~/git-repos/esim-coach`, outside iCloud. Connect that
folder, not the old one in Documents.

---

Copy everything below the line.

---

Read `BUILD-TODO.md` in the connected folder, then `data/PROVIDER-SCOUTING.md`,
`LAUNCH-PLAN.md` and `data/config.json`.

## Where things stand

**The site is live and has been publishing itself.** `esim.coach` is served by
GitHub Pages from `MisterTyr/esim-coach`, which was already connected — nobody
had to pick a host, it was done months ago. The daily Action committed and pushed
on its own on 3 and 4 September, rebuilding from the sample CSV because
`SHEET_CSV_URL` is not set as a repo secret.

**HTTPS is broken and deliberately not being fixed.** `esim.coach` has five A
records: the four correct GitHub Pages IPs plus `192.64.119.69`, a Namecheap
parking address. Requests landing on the fifth get the wrong certificate, and its
presence stops GitHub issuing its own. Do not fix it. The domain is being
replaced.

**The repo was rebuilt from a clean clone on 4 September.** The old copy in
`~/Documents/Claude/Projects/esim-coach` was inside iCloud-synced Documents and
became unreadable — git failed with `mmap failed: Operation canceled`, two objects
from a commit could not be read, and directory listings came back nonsense.
Nothing was lost. The old folder is still there and can be deleted once trusted.
Do not put repos back in Documents, and do not run two Cowork sessions against the
same repo.

## Decisions already made — do not reopen these

**The Honest Mobile pin stays and is disclosed.** They pay for the top three
homepage slots. `update_plans.py` now records `value_rank` before placement is
applied and awards `top_pick` to whatever wins on value alone, so the green
"Top pick" badge cannot be bought. Pinned plans carry a separate neutral "Paid
placement" badge. `about.html` and `affiliate-disclosure.html` both describe the
arrangement plainly. One claim in the disclosure needs checking: it says the
arrangement is open to any provider on the same terms. Cut that line if it is not
true.

**The domain becomes `esimsorted.co.uk`.** Confirmed available, along with the
`.com`. Buy both, roughly $15.40 a year for the pair, `.co.uk` canonical and the
`.com` redirected to it in Namecheap. Let `esim.coach` lapse — it renews at $62.31
against $11.08 for a `.com`. The rename checklist is in `BUILD-TODO.md` and every
item on it has to move together. The brand name has not been decided: if the site
becomes "eSIM Sorted" then `site.brand`, the logo, every page title and the three
legal pages follow.

**Scope is the UK traveller going abroad**, which is what the site already is and
where all four affiliate programmes sell. UK-inbound visitors come second, as a
deliberate content cluster rather than an afterthought, because that is the only
part of this market where a UK-run site has an edge. The Sheet already carries the
inbound products — SMARTY, Sim Local's UK 80GB on EE, and two of Honest Mobile's
three plans are UK plans.

## The job, in order

1. **Confirm the disclosure fix is pushed and live.** Fourteen files were changed
   on 4 September and left uncommitted for review. If they are still uncommitted,
   read the diff, commit and push. Then load `esim.coach` and check the badges and
   the two pages actually changed.
2. **Buy the domain and do the rename**, following the checklist in
   `BUILD-TODO.md`. Some of this needs Marty's logins — hand him the steps rather
   than guessing.
3. **Apply to the affiliate programmes the same day the new domain resolves.**
   Airalo, Nomad, Holafly, Saily, plus Jetpac and Ubigi. And join Awin, which
   already carries Breeze eSIM UK, WorldSIM, eSIMania and Esim Prime, so one UK
   account reaches several merchants. Approvals are the only clock Marty does not
   control.
4. **Put real prices in the Sheet.** The published CSV works — it returns HTTP 200
   and 22 rows — it has simply never held anything but the July sample data, all
   timestamped 2026-07-08 with placeholder affiliate ids. Check every price on the
   provider's own site before it goes in. Widen the provider list from
   `data/PROVIDER-SCOUTING.md`, starting with BNESIM, aloSIM, GigSky, Yesim and
   Roamless.
5. **Set `SHEET_CSV_URL` as a repo secret**, then re-enable the daily Action and
   watch one run before trusting it.
6. **Swap the placeholder affiliate ids** as approvals land. All 19 `product_url`
   values still carry `ref=YOUR_AFFILIATE_ID`. Test one link end to end.

## Traps still open

- The Action's commit step is `git add plans.json sitemap.xml index.html *.html`,
  which misses anything in a subdirectory. A future `/guides/` folder would never
  publish.
- Adding an article takes two edits in two files, `PAGES` in `scripts/content.py`
  and the hardcoded list in `write_sitemap()`. Derive one from the other so a page
  cannot ship unlisted.
- The workflow holds `contents: write` and pushes straight to main with no review,
  and the Sheet URL is committed in plain text. Once the Sheet holds real prices, a
  bad spreadsheet edit goes live unattended the next morning.
- `site.description` in `data/config.json` still says "refreshed daily", and it
  rides into the meta description and Open Graph description of every page.
- The Sheet has no column for hotspot policy. Holafly caps tethering, and it is the
  most common complaint about travel eSIMs, so it belongs in the data.
- `Archive Build/` is committed and kept, 21 files of the old scaffold including an
  n8n flow and a Google Apps Script the current build does not use.

## Working rules

- Ask before writing code and before anything that changes what the public sees.
- Verify prices against the providers rather than trusting the sheet or the sample.
- Plain English, British spelling.
- Update `BUILD-TODO.md` in the same session and say what to tick off on the board.

## Marty's additions

<!-- Add anything else here before starting the chat. -->
