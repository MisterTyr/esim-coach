# Price check, 4 September 2026

First real check of provider prices since the project started. Everything here
was read off the provider's own website. Nothing came from a comparison article
or a roundup.

## Read this before you use any of it

**Most of it is not in pounds.** The checks ran from a US connection, and almost
every travel eSIM company sets its currency from where you appear to be, using
JavaScript that a fetching tool cannot click. So Nomad, Holafly, Saily, Jetpac,
Ubigi, Orange and Sim Local all came back in dollars or euros. Those figures are
real prices, just not the ones a British buyer sees, and converting them
ourselves would be inventing a number.

What survived as genuine pounds:

- **Airalo.** Their site honours a `?currency=GBP` link, so all 25 rows are real
  GBP. Saved as `data/verified/2026-09-04-travel-esims.csv`.
- **The UK networks** — Three, SMARTY, Honest Mobile, O2, giffgaff, EE. British
  companies selling in Britain, so there is no currency question. Saved as
  `data/verified/2026-09-04-uk-networks.csv`.

Everything else is preserved further down as-is, with its currency marked, so a
second pass from a UK connection only has to re-check the prices rather than
rebuild the whole picture.

## What changed our thinking

### 1. The throttle is usually per day, not per plan

This is the correction that matters most, and it arrived a few hours after we
built the column that gets it wrong.

- **Airalo**: 3GB a day at full speed, then 1Mbps, resetting every 24 hours.
- **Saily**: 5GB a day for Japan, USA and Thailand; 3GB a day for Europe. Then 1Mbps.
- **Nomad**: 2GB a day, then 512kbps.
- **Ubigi**: caps the *whole plan*, not the day — 25GB across a 7-day plan,
  60GB across a 30-day one, then 2Mbps.

So "25GB at full speed" means two completely different products depending on the
provider, and a single `full_speed_gb` column cannot tell them apart. The
pipeline now has `full_speed_period`, either `per_day` or `per_plan`, and works
out the comparable total from the two together. Without it, Airalo's 30-day
unlimited would have been ranked as a 3GB plan instead of a 90GB one.

### 2. Airalo has stopped selling sized plans on the big destinations

Japan, Europe, USA and Thailand are unlimited-only now. The old 1GB / 5GB / 10GB
package URLs still turn up in search results but they redirect to the
destination page. Any content we write that assumes "Airalo does a cheap 1GB
option" is out of date.

Their global Discover range still advertises "from £6.50", well below the
cheapest global unlimited at £18.50, so cheaper capped global packs probably do
still exist — that page would not render for us. Worth opening in a browser.

### 3. Holafly will not tell you what their limit is

Their destination pages market plain "unlimited data". Their terms say only that
speed "may be subject to a network service provider's fair use policy". There is
no number published anywhere on their own site.

That means we cannot list Holafly as capped, and we must not list them as
uncapped either — a blank `full_speed_gb` currently means "genuinely no limit",
which would be a claim Holafly themselves decline to make. **Their rows need a
card that says the limit is unpublished.**

What they do publish: hotspot is capped at **1GB a day**. On a 7-day plan you can
share 7GB in total. That is a real limitation on a product sold as unlimited, and
it is the most common complaint about travel eSIMs.

Also worth a spot-check: Holafly now charges the identical price ladder for every
destination — the same six prices for Japan, Thailand, USA and Europe alike.

### 4. Honest Mobile's data in the Sheet is wrong, and they are the paid placement

The Sheet has "Smart SIM Global, unlimited, 365 days, £45". The real Smart SIM is
**£3.75 a month**, and it is an app-limited backup data eSIM with no calls, no
texts and no phone number. It should probably not sit in a comparison table
beside full plans at all.

Their real Classic plans, from their own site: **4GB £12.15, 10GB £17.50,
Unlimited £25.00**. The unlimited drops to 3G speeds after 750GB. Their EU roaming
is only **5 days complimentary per trip**, which is much weaker than Three or
SMARTY, so placement copy must not imply otherwise.

One thing needs your decision: every Honest Mobile plan also shows a lower
"loyalty discount" price (£9.45 / £12.25 / £17.50). We have used the standard
price. The gap is large enough that they may expect the other one displayed.

### 5. EE's UK Travel eSIM cannot call 999

EE's own terms: the product "does not provide a number, number portability, or
the ability to make or receive non-internet phone calls and texts, **including
calls to emergency services**."

A visitor buying that as their only SIM has no way to call an ambulance. Whatever
else the inbound pages say, they have to say this.

### 6. The Three £10 claim was half right

The research said £10 buys 40GB UK plus 6GB roaming across 70+ destinations with
unlimited calls and texts in Europe. Checked on Three's own site: the 40GB, the
70+ destinations and the unlimited calls and texts all hold. **But the roaming
data is only 6GB, not the full 40GB**, and every Three pay-as-you-go pack carries
a blanket 25Mbps speed cap from the first byte — so their "Unlimited" at £35 is
unlimited at 25Mbps, which is not the same product as SMARTY's unlimited.

Three also runs a second, parallel auto-renew range where £10 buys 60GB at
50Mbps. Two £10 packs with different data and different speeds, on the same page.
Left out of the verified file until someone looks at it properly.

### 7. SMARTY's unlimited is genuinely uncapped

Their own page: "No restrictions. No speed caps", and tethering explicitly
allowed. That is rare enough to be a selling point. Note their much-quoted "12GB
fair use limit" is the **EU roaming** cap, not a UK one — easy to conflate.

## Affiliate programmes, from the providers' own sites

| Provider | Network | Rate | Cookie |
|---|---|---|---|
| Airalo | Impact | 10% of sale after discounts | not published |
| Nomad | Impact (moved Aug 2025) | not published | not published |
| Saily | In-house, affiliates.saily.com | 15% per new user | not published |
| Jetpac | In-house | "up to 15%" | not published |
| Ubigi | Impact | 10% on first purchase | 60 days |
| Holafly | Contact form only | **not published at all** | not published |
| Orange Travel | none found | — | — |
| Rewild Mobile | none found | — | — |

The commission rates in `PROVIDER-SCOUTING.md` that came from roundups can now be
replaced with these. Note Holafly publishes no rate whatsoever — you have to
apply and ask.

## Could not verify

- **Rewild Mobile: nothing at all.** Their travel pricing is entirely behind a
  JavaScript destination picker. The "cheapest on 1–10GB" claim rests only on
  third-party roundups and must not be published as checked. Their pack ladder
  is confirmed (1, 3, 5, 10, 20, 50GB) and their UK domestic plans are published
  in real GBP (4GB £12.50, 10GB £16.50, Unlimited £22.50 a month; EU roaming
  add-on £2.95 a day) — but those are UK SIM plans, not travel packs.
- **Lebara**: JavaScript-only. Recovered £10/30GB and £25 unlimited from page
  metadata, not rendered pages. eSIM support could not be confirmed at all, so no
  Lebara row can go live yet.
- **Sim Local**: served dollars on every UK-facing path. Confirmed their Three UK
  plans do include a real +44 number.
- **giffgaff**: could not confirm a brand-new joiner can order an eSIM directly
  rather than starting on a physical SIM. That matters for a visitor.
- **Airalo Discover+**, the calls-and-texts product: confirmed it gives a real US
  number with calls and SMS, but no live pricing page could be found.
- **Jetpac's lounge perk**: SmartDelay via LoungeKey, 1300+ lounges, 24-hour
  advance flight registration — all confirmed on their homepage. The delay
  threshold, which plans qualify and whether it costs extra could not be.
- **Orange Travel's phone number country.** Their Europe plans do include real
  cellular calls and texts and a "European phone number", but they never say
  which country issues it.

## The one that needs a decision

The UK networks price far better per GB than any travel eSIM — SMARTY does 100GB
for £12, which is 12p a GB against Airalo's best of about 60p. Dropped into the
same ranking, UK SIM-only deals would take every top slot on a travel eSIM
comparison site.

That is exactly the editorial point the research made — the best travel eSIM is
often not a travel eSIM — but it needs to be a deliberate choice about what the
homepage is for, not something that happens by accident when the file is loaded.
The `direction` column can split them. Nothing has been loaded into the Sheet.

---

# Preserved rows, not in pounds — do not load

Everything below is a real price read from the provider's own site, in the
currency shown. A second pass from a UK connection needs only to re-check the
price column.

## Nomad — USD

Throttle 2GB a day then 512kbps on all unlimited plans (their own fair use
document; their help centre says 1–2Mbps instead, so they contradict themselves).
Data only. Their Thailand eSIM on DTAC reportedly includes a number with
unlimited calls to local DTAC numbers, but they do not say which plan.

Japan: unlimited 3d $11, unlimited 7d $25, 1GB 7d $4, 5GB 30d $10, 20GB 30d $23.
Europe: unlimited 5d $19, unlimited 10d $34, 1GB 7d $5.50, 5GB 30d $17.50, 20GB 30d $27.
USA: unlimited 3d $11, unlimited 7d $23, 1GB 7d $5, 5GB 30d $16, 20GB 30d $36.
Thailand: unlimited 10d $16, unlimited 30d $33, 1GB 7d $5, 5GB 30d $8, 10GB 30d $10.
Global: 1GB 7d $12, 3GB 30d $25, 5GB 30d $40, 10GB 30d $62, 20GB 30d $103.

## Holafly — USD (global subscriptions in EUR)

Identical ladder for Japan, Europe, USA and Thailand: 3d $11.90, 7d $27.50,
15d $50.50, 30d $73.90. Global unlimited monthly subscription €59.95; Global
Light 25GB monthly €45.95. Throttle unpublished. Hotspot capped at 1GB a day.

## Saily — USD

Full-speed caps are per day: 5GB/day for Japan, USA and Thailand, 3GB/day for
Europe, then 1Mbps. Hotspot unlimited. No unlimited tier on the global plan.
A US phone number is a separate add-on at about $0.99 a month.

Japan: 1GB 7d $3.99, 5GB 30d $10.99, 10GB 30d $17.99, 20GB 30d $24.99, unlimited $48.99.
Europe: 1GB 7d $4.99, 5GB 30d $19.49, 10GB 30d $35.99, 50GB 90d $95.99, unlimited $49.99.
USA: 1GB 7d $3.99, 5GB 30d $13.99, 10GB 30d $22.99, 20GB 30d $36.99, unlimited $45.99.
Thailand: 1GB 7d $2.99, 5GB 30d $7.99, 10GB 30d $10.99, 20GB 30d $19.99, unlimited $38.99.
Global: 1GB 7d $8.99, 5GB 60d $33.99, 10GB 180d $56.99, 20GB 365d $66.99, 50GB 365d $129.99.

## Jetpac — USD, and all promotional

Lowest confidence of the set — their prices are JavaScript-rendered and the 20GB
tier renders above the 30GB tier on every destination, which is almost certainly
a struck-through RRP being picked up. Those rows are omitted. Everything is
marked "September offer, 30–56% off", so it will move. Unlimited plans throttle
at 3GB a day to 1Mbps.

Japan: 5GB $10, 10GB $16, 15GB $21, 30GB $29.99, unlimited 30d $65.99.
Europe: 5GB $16, 10GB $22, 15GB $27, 30GB $29.99, unlimited 30d $65.99.
USA: 5GB $12.99, 10GB $19, 15GB $22, 30GB $29.99, unlimited 30d $67.99.
Thailand: 5GB $7, 10GB $11.50, 15GB $12.50, 30GB $23.99, unlimited 30d $65.99.
Global: unlimited 30d $174, 50GB 365d $249.

## Ubigi — USD

Throttles per plan, not per day. UK unlimited 7d gives 25GB then 2Mbps; 30d gives
60GB then 2Mbps — exactly as the research said. But it is not uniform: Japan's
7-day unlimited throttles at about 15GB to 1Mbps, while Japan's 15-day and 30-day
use the standard 30GB and 60GB at 2Mbps. Ubigi's own listing pages and product
pages also disagree on price, sometimes by 20% (UK unlimited 30d is $55 on one
and $44 on the other). Treat every Ubigi figure as soft.

Japan: 1GB 7d $4, 10GB 30d $17, 25GB 30d $33, unlimited 7d $25 (15GB/1Mbps),
unlimited 15d $39 (30GB/2Mbps), unlimited 30d $65 (60GB/2Mbps).
Europe: 10GB 30d $15, 25GB 30d $29, unlimited 7d $23 (25GB/2Mbps),
unlimited 15d $35 (30GB/2Mbps).
USA: 1GB 7d $5, 10GB 30d $19, 25GB 30d $39, unlimited 7d $25 (25GB/2Mbps),
unlimited 30d $69.
Thailand: 1GB 7d $5, 10GB 30d $20, 25GB 30d $39, unlimited 7d $22.90 (25GB/2Mbps),
unlimited 30d $68.
Global: 1GB 30d $9, 10GB 30d $39, 25GB 90d $59, 100GB 12m $190,
World unlimited monthly $120 (60GB/2Mbps).
UK (inbound): 3GB 30d $5, 10GB 30d $12, 25GB 30d $21, 50GB 30d $39,
unlimited 7d $21 (25GB/2Mbps), unlimited 30d $44 (60GB/2Mbps).

## Orange Travel — EUR

The only provider found with real cellular calls and texts on a travel product.
The Europe range includes unlimited calls and texts and a European phone number,
though Orange never says which country issues it. The plain data tiers on the
Japan, USA, Thailand and UK pages are data-only.

Europe (calls and texts included): 20GB 14d €24.99, 50GB 30d €44.99,
100GB 30d €47.99, 200GB 30d €57.99, 500GB 90d €99.99.
Japan (data only): 3GB 7d €7.99, 10GB 7d €13.99, 20GB 14d €24.99,
50GB 30d €42.99, 100GB 45d €56.99.
USA: Data+Calls+SMS unlimited 5d €15.99, 10d €28.99, 15d €40.99;
data only 10GB 7d €18.99, 50GB 30d €49.99.
Thailand: Data+Calls+SMS unlimited 1d €7.99, 10d €35.99, 30d €72.99;
data only 10GB 7d €10.99, 50GB 30d €28.99.
World: 20GB 30d €29.99 with 15 minutes of calls and 50 texts.
UK (inbound): Data+Calls+SMS unlimited 5d €16.99, 15d €37.99;
data only 10GB 7d €12.99, 20GB 30d €18.99, 50GB 30d €29.99, 200GB 90d €59.99.

## Sim Local — USD

Their Three UK plans include a real +44 number, confirmed. Number provision on
the resold EE and Lycamobile plans could not be confirmed.

Three UK: 20GB 30d $13.50, 100GB $20, 200GB $26.75, unlimited 30d $47,
unlimited 90d $120.50.
EE UK: 30GB $20, 80GB $20, 150GB $26.75, 200GB $40.25, unlimited 30d $53.50,
unlimited 90d $127.25.
Lycamobile: 20GB 15d $13.50, 100GB 15d $26.75.
Sim Local own brand: 20GB 30d $28.50, data only.
