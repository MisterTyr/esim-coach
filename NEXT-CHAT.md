# Handover — eSIM Sorted

Read `BUILD-TODO.md` first (start at the bottom, "Session 2026-09-04, second
sitting"), then `data/PRICE-CHECK-2026-09-04.md`, then `data/config.json`.

## The one thing that explains everything

**GitHub Pages has never published this site.** The repo is private on a free
GitHub plan, and free-tier Pages only works on public repos. So `main` has been
correct since 2 September and nothing has ever reached the web. `esim.coach`
serves a stale October 2025 deployment whose disclosure page says affiliate
partners cannot pay for placement — which stopped being true when the Honest
Mobile pin went in. Nothing else on this list matters until Marty makes the repo
public or pays for GitHub Pro. A scan found nothing sensitive in the tracked
files. It is his click to make.

## Done and committed on 4 September — do not redo

The rename (`adf1c03`) is pushed. Then, in a second sitting:

- The logo is in and the site is **light**, built on Marty's palette. Dusty Rose
  is darkened to `#A85647` where white text sits on it; pure `#CE796B` fails
  contrast for body text.
- The unlimited ranking bug is fixed, and fixed properly: most providers cap
  **per day**, not per plan, so `full_speed_period` had to exist. Airalo's 30-day
  unlimited scores as 90GB, not 3GB.
- The daily Action now refuses to publish if the data looks wrong — most
  importantly if the Sheet returns nothing and it is about to publish the local
  sample file.
- Four destination guides written: Japan, Europe, USA, Thailand.
- Prices checked against providers for the first time. Results in
  `data/PRICE-CHECK-2026-09-04.md`, verified rows in `data/verified/`.

**Everything is committed locally. Marty has to push it** — no GitHub credentials
in the sandbox, and none on the mounted machine either.

## The first real job for the next chat

**Re-check prices from a UK connection.** Only Airalo and the UK networks came
back in pounds. Nomad, Holafly, Saily, Jetpac, Ubigi, Orange and Sim Local all
served dollars or euros, because their currency switchers are JavaScript and the
research ran from a US connection. Every price and every structural detail is
preserved in `PRICE-CHECK-2026-09-04.md`, so this is only re-reading a price
column, not redoing the work. Marty's own browser is in the UK — that is the
route.

## Then, in rough order

1. Load the verified rows into the Sheet. Honest Mobile first, because their
   current rows are wrong and they are the paid placement.
2. Decide whether UK network plans share a ranking with travel eSIMs. SMARTY at
   12p a GB would take every top slot. `direction` can split them.
3. Give Holafly's rows a card that says the throttle is unpublished. Blank
   currently reads as "no limit", which is a claim Holafly will not make.
4. Say on any inbound page that EE's UK Travel eSIM cannot call 999.
5. The workflow still holds `contents: write` and pushes straight to main. The
   sanity checks now stop bad *data*, but not a bad commit.

## Working rules

- Ask before writing code and before anything that changes what the public sees.
- Verify prices against the provider, never the sheet or a roundup.
- Plain English, British spelling.
- Update `BUILD-TODO.md` in the same session and say what to tick off.
