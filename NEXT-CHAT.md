# Prompt for the next eSIM Coach chat

Do the safety session first (`../SAFETY-SESSION.md`) — the entire July rebuild is
uncommitted and one careless git command erases it. Nothing below is worth starting
until that is done.

Name the chat: **eSIM Coach — deploy and monetise**

---

Copy everything below the line.

---

Read `BUILD-TODO.md` in the connected folder, then `LAUNCH-PLAN.md` and
`data/config.json`.

**Where things stand.** The build is genuinely finished and the launch genuinely
never started. Everything on disk dates from 9 July 2026. The generator works end
to end, the site renders 19 plan cards with a working region filter, seven content
pages, a sitemap and the legal set. `LAUNCH-PLAN.md` lays out seven days from files
on disk to a live earning site, and the project is still on day one.

**The job, in order.**

1. **Make the site reachable.** `esim.coach` currently serves a TLS certificate
   that does not match the hostname, and the repo carries no host config — no
   `_headers`, no `netlify.toml` — so nobody knows which of the three deploy
   options was actually chosen. Work out what state the domain and DNS are in, pick
   a host, connect it to the pushed repo, and confirm HTTPS works from outside.
   Some of this needs my logins; hand me the steps rather than guessing.
2. **Apply to the affiliate programmes the same day.** Airalo, Nomad, Holafly and
   Saily. Approvals take days and it is the only clock I do not control, so this
   goes before the content and data work, not after.
3. **Find out whether the Google Sheet source has ever worked.**
   `data/config.json` has a real published-Sheet CSV URL as the primary source with
   `enabled: true`, yet `plans.json` is still the 19 sample rows. So it has either
   never been pulled or returned nothing. One run of `scripts/update_plans.py`
   answers it. Then load real prices for the four providers and verify a few
   against the providers' live sites — do not trust generated prices.
4. **Confirm the daily Action actually runs.** Check the Actions tab the next day
   for a committed refresh. Note that the workflow needs `SHEET_CSV_URL` set as a
   repo secret, and that its commit step is `git add plans.json sitemap.xml
   index.html *.html`, which will silently miss anything in a subdirectory — so a
   future `/guides/` folder would never publish. Fix that while you are in there.
5. **Swap the placeholder affiliate ids** as approvals land. All 19 `product_url`
   values carry `ref=YOUR_AFFILIATE_ID`. Test one link end to end before trusting
   any of them.

**One thing to raise with me before step 1, because it is a disclosure problem.**
`config.json` sets `pin_providers: ["Honest Mobile"]`, which puts all three of
their plans at ranks 1 to 3 with "Top pick" ribbons. Meanwhile `about.html` says
ranking is "driven only by the value maths" and `affiliate-disclosure.html` says
commercial relationships have "no bearing on where its plans appear". Two published
pages currently say something that is not true. Either the pin goes, or both pages
get rewritten and the placement gets labelled as placement with its own styling —
the "Top pick" badge currently does double duty as an editorial verdict and a paid
slot. Ask me which, do not decide it for me.

Also flag before launch: the footer says "Data refreshed daily" and the hero says
"Updated 09 Jul 2026", over two-month-old sample prices. That cannot go live as is.

**Things to hold onto**

- Adding an article takes two edits in two files — `PAGES` in `scripts/content.py`
  and the hardcoded list in `write_sitemap()`. Derive one from the other so a page
  cannot ship unlisted.
- The workflow holds `contents: write` and pushes straight to main with no review,
  and the Sheet URL is committed in plain text. Once the Sheet is wired, a bad
  spreadsheet edit goes live unattended.
- `.gitignore.html` is a gitignore body saved with an `.html` extension and it is
  tracked. It would deploy as a page.
- `Archive Build/` is an untracked duplicate of the old scaffold, including an n8n
  flow and a Google Apps Script the current build does not use.

**Working rules**

- Ask before writing code and before anything that changes what the public sees.
- Verify prices against the providers rather than trusting the sheet or the sample.
- Plain English, British spelling.
- Update `BUILD-TODO.md` in the same session and tell me what to tick off on the
  board.
