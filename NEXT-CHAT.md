# Handover — eSIM Sorted

**The site is being rebuilt from scratch.** Read `docs/BRIEF.md` first. The work
happens on the `rebuild` branch; `main` serves a holding page at
https://esim-sorted.co.uk until the switch-over.

## State on 5 November 2026

- The domain works: `esim-sorted.co.uk` resolves to GitHub Pages, and the repo
  is public. The old blockers in `BUILD-TODO.md` (repo private, DNS) are done.
- `main` (`7c8892c`) is a holding page. The old pages are gone from `main` but
  recoverable from `378ca3f`. The daily Action's schedule is paused, so it
  cannot rebuild the old table over the holding page.
- Phase 1 (the brief) is written. It's waiting on the six decisions at the
  bottom of `docs/BRIEF.md`.

## eSIMDB — read this before touching it

`~/git-repos/_archive/esimdb` holds a scraper and 627,826 plans pulled from
eSIMDB's client API on 6 September. Their terms forbid scraping and using their
database for a competing product, so **none of that data is published and the
scraper is not to be run again** unless eSIMDB gives written permission. The
code is ours and is to be brought into this repo (it is not in git anywhere).

## Working rules

- Ask before writing code and before anything that changes what the public sees.
- Verify prices against the provider, never a sheet, roundup or aggregator.
- Plain English, British spelling.
- Update `BUILD-TODO.md` in the same session and say what to tick off.
