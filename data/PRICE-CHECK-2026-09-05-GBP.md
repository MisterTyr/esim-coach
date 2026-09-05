# UK price re-check, 5 September 2026

Second pass on the prices that came back in dollars and euros on 4 September.
Read from Marty's own browser on a UK connection, so every figure below is the
price a British buyer actually sees. Provider websites only, no roundups.

Verified rows: `data/verified/2026-09-05-travel-esims-gbp.csv` — 229 rows across
Nomad, Holafly, Saily, Ubigi, Jetpac and Sim Local. **Nothing has been loaded
into the Sheet.**

## The five things that matter

**1. Four of the six were never a connection problem.** Ubigi, Jetpac and Sim
Local all show a British visitor dollars by default, and keep doing it until the
visitor finds the currency switcher themselves. That is a fact about those
products, not about how we checked them, and it belongs on their rows.

**2. Orange shows pounds but charges euros.** In their own small print: "Prices
converted at the rate in effect on Aug 25, 2026. Payment will be made in Euro."
So the pound figure is an estimate and the card gets an FX rate plus whatever the
bank adds. **Orange has been left out of the verified CSV** — we do not have a
sterling price for them, we have a sterling guess. Their rows are written up in
full below for when we decide how to handle it.

**3. The old dollar list cannot be converted, it has to be replaced.** Nomad's
catalogue has changed since Tuesday — new tiers, new durations. Holafly has
scrapped its price ladder entirely and now sells by trip length, any number of
days from 1 to 90, at the same price for every destination.

**4. Two prices are cheap enough to be suspicious.** Nomad's Thailand 50GB for 10
days at £8.85 is 18p a GB. Orange's Japan 1GB for 7 days is 99p. Both need
opening in a browser before they go anywhere near the site.

**5. Discounts are creating rows that make no sense.** Jetpac's 20GB pack costs
more than its 30GB and 40GB packs, because it is the only tier without a discount.
Orange's Japan 100GB for 30 days is cheaper than its 50GB. Whatever the ranking
does, it should not present those silently as though they were sensible.

---

## Nomad — real GBP, confirmed

The site now sits at `nomadesim.com` (the old `getnomad.app` links 404) and it
prices in pounds automatically on a UK connection. No currency switch needed.

**The catalogue has changed since the first check.** There are tiers here that
did not exist in the dollar pass — 3GB and 50GB on most destinations, 14 and 21
day unlimited on Japan, six unlimited lengths on the USA. So this is not a
straight currency conversion of the old list, and the old list should be thrown
away rather than converted.

Full-speed cap 2GB a day then 512kbps on unlimited plans, per Nomad's own fair
use document. Data only.

Prices marked **sale** show a struck-through higher price on the page. They will
move, so they need a check before they go in the Sheet.

### Japan
| Plan | Validity | Price |
|---|---|---|
| Unlimited | 3 days | £8.12 |
| Unlimited | 7 days | £18.45 |
| Unlimited | 14 days | £30.25 |
| Unlimited | 21 days | £36.16 |
| 1GB | 7 days | £2.95 |
| 3GB | 30 days | £5.17 |
| 5GB | 30 days | £7.38 |
| 10GB | 30 days | £11.81 (sale, was £13.28) |
| 20GB | 30 days | £16.97 (sale, was £19.19) |
| 50GB | 30 days | £25.83 |

### Europe (35-country plan; a 36-country plan is a separate tab)
| Plan | Validity | Price |
|---|---|---|
| Unlimited | 5 days | £14.02 |
| Unlimited | 10 days | £25.09 |
| 1GB | 7 days | £4.06 |
| 3GB | 30 days | £8.85 |
| 5GB | 30 days | £12.91 |
| 10GB | 30 days | £16.97 |
| 20GB | 30 days | £19.92 (sale, was £27.30) |
| 50GB | 30 days | £25.83 (sale, was £35.42) |

Also on the Europe page: **Nomad Pass**, £2.21 a month auto-renewing, which
includes 1GB of Europe data a month and takes 15% off other Europe plans. It is a
subscription, not a travel pack, so it does not belong in the same ranking.

### USA
| Plan | Validity | Price |
|---|---|---|
| Unlimited | 3 days | £8.12 |
| Unlimited | 5 days | £11.81 |
| Unlimited | 7 days | £16.97 |
| Unlimited | 10 days | £23.61 |
| Unlimited | 15 days | £32.47 |
| Unlimited | 20 days | £38.37 |
| 1GB | 7 days | £3.69 |
| 3GB | 30 days | £7.38 |
| 5GB | 30 days | £11.81 |
| 10GB | 30 days | £18.45 |
| 20GB | 30 days | £26.56 (sale, was £28.04) |
| 50GB | 30 days | £30.25 (sale, was £44.27) |
| 75GB | 180 days | £65.67 |
| 100GB | 365 days | £88.55 |

### Thailand
| Plan | Validity | Price |
|---|---|---|
| Unlimited | 10 days | £11.81 (sale, was £14.76) |
| Unlimited | 15 days | £15.50 |
| Unlimited | 30 days | £24.35 |
| 1GB | 7 days | £3.69 |
| 3GB | 30 days | £4.43 |
| 5GB | 30 days | £5.90 |
| 10GB | 30 days | £7.38 |
| 50GB | 10 days | £8.85 |

Thailand 50GB for 10 days at £8.85 is 18p a GB, which undercuts every other
travel eSIM row we hold and most of the UK networks. Worth a second look before
it goes live, in case it is a mispriced page rather than a real offer.

### Global (123 destinations)
| Plan | Validity | Price |
|---|---|---|
| 1GB | 7 days | £8.85 |
| 3GB | 30 days | £18.45 |
| 5GB | 30 days | £29.52 |
| 10GB | 30 days | £45.75 |
| 20GB | 30 days | £76.00 |

No unlimited tier on Global. A cheaper "Global-EX" range (98 destinations, from
£1.90/GB) and several regional packs also exist — APAC from £0.29/GB is the
cheapest per-GB figure Nomad publishes anywhere.

## Holafly — real GBP, confirmed

Prices in pounds automatically on a UK connection (the page carries its own GBP
selector, already set). Verified the connection really is British: their own
analytics tagged the page `ur=GB-GLG`.

**Holafly has thrown the price ladder away.** The six fixed tiers from the first
check (3, 7, 15, 30 days and so on) are gone. You now pick trip dates on a
calendar and the price slides with the number of days, 1 to 90. The banner says
"More days, lower the price!" and it is true: day one costs £4, day ninety costs
£1.23.

**The price is identical for every destination.** Japan, Europe, USA and Thailand
all run the same table, pulled from the same list of 90 day-length variants. What
the first check suspected is now confirmed, in pounds.

| Days | Price | Per day |
|---|---|---|
| 1 | £4 | £4.00 |
| 3 | £10 | £3.33 |
| 5 | £16 | £3.20 |
| 7 | £22 | £3.14 |
| 10 | £30 | £3.00 |
| 15 | £41 | £2.73 |
| 20 | £49 | £2.45 |
| 30 | £60 | £2.00 |
| 60 | £86 | £1.43 |
| 90 | £111 | £1.23 |

Every whole number of days from 1 to 90 has its own price, so the Sheet can hold
whichever lengths we want to show rather than whatever Holafly happened to sell.
Suggest we carry 5, 7, 10, 15 and 30 to match the other providers.

Two things that have not changed:

- **No throttle figure is published anywhere.** Searched the destination pages for
  a fair use, throttle, Mbps or Kbps figure and there is nothing. So the card
  saying "the limit is unpublished" is still needed, and a blank `full_speed_gb`
  still cannot be allowed to read as "no limit".
- **Hotspot is 1GB a day**, in their own words on the page: "Share 1 GB of data
  per day with family, friends, or fellow travellers."

### Holafly global subscriptions — real GBP
| Plan | Price |
|---|---|
| Unlimited, global, monthly | £50.95 a month |
| Light, 25GB, global, monthly | £38.95 a month |

Quarterly saves about 10% and yearly about 20%; the page does not show those
figures until you switch tab. Two things worth noting on the Unlimited
subscription that do not apply to the destination eSIMs: it advertises
**unlimited hotspot**, and a **local phone number with SMS**. If we build the
`voice_type` column, this is one of the few travel products that would not be
`none`.

## Saily — real GBP, confirmed

Prices in pounds automatically. Every figure below was cross-checked two ways:
the visible card and the structured product data behind the page, which lists a
price against the same product code the duration menu uses. They agree.

Full-speed caps are **per day**, confirmed again on each page: 5GB a day for
Japan, USA and Thailand, 3GB a day for Europe, then 1Mbps. Hotspot unlimited.

A **US phone number** is a separate add-on paired with a call and text plan —
worth a row of its own if we build `voice_type`, but it is not part of the data
plan.

### Japan
Sized: 1GB 7d £2.99 · 3GB 30d £5.99 · 5GB 30d £8.49 · 10GB 30d £13.99 · 20GB 30d £19.49
Unlimited: 5d £14.49 · 7d £20.99 · 10d £26.99 · 15d £37.49 · 20d £45.99 · 25d £50.99 · 30d £55.49

### Europe (35 countries)
Sized: 1GB 7d £3.99 · 3GB 30d £9.49 · 5GB 30d £14.99 · 10GB 30d £27.49 · 50GB 90d £73.99
Unlimited: 7d £20.99 · 10d £27.49 · 15d £38.49 · 20d £45.99 · 25d £50.99 · 30d £55.49
No 5-day unlimited on Europe. Full-speed cap is 3GB a day here, not 5.

### USA
Sized: 1GB 7d £2.99 · 3GB 30d £6.99 · 5GB 30d £10.99 · 10GB 30d £17.49 · 20GB 30d £28.49
Unlimited: 5d £13.99 · 7d £18.99 · 10d £25.99 · 15d £35.49 · 20d £43.99 · 25d £48.49 · 30d £52.49

### Thailand
Sized: 1GB 7d £2.49 · 3GB 30d £4.49 · 5GB 30d £5.99 · 10GB 30d £8.49 · 20GB 30d £15.49
Unlimited: 5d £11.49 · 7d £15.99 · 10d £23.99 · 15d £29.99 · 20d £33.99 · 25d £36.99 · 30d £37.49

### Global
1GB 7d £6.99 · 2GB 15d £12.49 · 5GB 60d £25.99 · 10GB 180d £43.99 · 20GB 365d £51.49 · 50GB 365d £99.99
Still no unlimited tier on Global.

All Saily plans carry a 180-day activation window, and every purchase earns 3%
back in Saily credits — which is a discount on the next purchase, not on this one,
so it should not come off the price we publish.

## Ubigi — real GBP, confirmed

**Ubigi does not follow the connection.** On a UK browser it still opens in
dollars. There is a currency switcher tucked in the header, and picking British
Pound adds `?wmc-currency=GBP` to the address. So the dollar prices in the first
check were not a US-connection problem after all — that is just what Ubigi shows
a British visitor until they change it themselves. Worth a line on the Ubigi rows.

Once switched, the whole catalogue prices in pounds on one page, so these are all
read from the same table rather than page by page.

The plan detail pages carry the throttle figures; the listing does not. The
structural findings from the first check still stand and are not currency
dependent: Ubigi caps the **whole plan**, not the day — 25GB on a 7-day
unlimited, 60GB on a 30-day, then 2Mbps — and their listing and product pages
have been seen to disagree on price. **Every Ubigi figure below comes from the
listing.** Before any of it goes in the Sheet, spot-check two or three against
the plan pages.

### Japan
1GB 3d £3 · 1GB 30d £3.50 · 3GB 15d £6.50 · 5GB 15d £9 · 10GB 7d £12 · 10GB 30d £13.50 · 25GB 30d £27 · 50GB 30d £47
Unlimited: 8d £22 · 15d £34 · 30d £56
Monthly subscriptions: 5GB £7 · 20GB £15 · Unlimited £38

### Europe
500MB 2d £2 · 3GB 30d £6 · 10GB 7d £10 · 10GB 30d £13 · 25GB 30d £24 · 50GB 30d £62
Unlimited: 7d £20 · 15d £30 · 30d £72
Monthly: 5GB £6 · 20GB £16 · Unlimited £42
A separate **Europe Extended** region costs roughly double at every tier.

### USA
500MB 1d £2.50 · 1GB 7d £3.50 · 3GB 15d £6 · 10GB 7d £10 · 10GB 30d £12 · 25GB 30d £27 · 50GB 30d £35
Unlimited: 1d £8 · 7d £22 · 15d £34 · 30d £56
Monthly: 5GB £5 · 20GB £13

### Thailand
1GB 7d £3 · 3GB 15d £4 · 10GB 7d £8 · 10GB 30d £9 · 25GB 30d £21.90
Unlimited: 7d £19 · 15d £30 · 30d £42
Monthly: 5GB £5 · 20GB £10 · Unlimited £31

### UK (inbound)
3GB 30d £4 · 10GB 7d £8 · 10GB 30d £9 · 25GB 30d £19 · 50GB 30d £27
Unlimited: 1d £4 · 7d £18 · 15d £27 · 30d £37
Monthly: 5GB £4 · 20GB £10 · Unlimited £23

**UK unlimited for a day at £4** is the cheapest single-day unlimited anywhere in
this check, Holafly included, and it is the sort of row an inbound page is for.

### World and Best World
Best World: 500MB 30d £4 · 1GB 30d £8 · 3GB 30d £16 · 10GB 30d £34 · 25GB 90d £50 ·
50GB 180d £86 · 100GB 12m £165 · 200GB 12m £251 · unlimited 8d £42 / 15d £70 / 30d £92
World: 500MB 30d £6 · 1GB 30d £12 · 3GB 30d £23 · 10GB 30d £50 · 25GB 90d £86 ·
50GB 180d £165 · 100GB 360d £251 · 200GB 360d £337 · monthly unlimited £105

## Jetpac — real GBP, confirmed

Like Ubigi, **Jetpac shows a British visitor dollars until they change it
themselves.** The switcher is in the header. Once set to British Pound it sticks
across pages.

**Everything is still on offer**, and the discounts are deeper than in the first
check — 56% off the unlimited packs. Treat every Jetpac price as a September
number that will move.

**The 20GB-above-30GB oddity is real, not a rendering fault.** The first check
guessed a struck-through price was being picked up by mistake. It is not: the
20GB pack is the only tier with no discount applied, so it genuinely costs more
than the discounted 30GB and 40GB packs sitting below it. On Japan, 20GB is £33
while 40GB is £29. Anyone buying 20GB from Jetpac this month is being had, and
that is worth saying rather than quietly dropping the row.

Full-speed cap in Jetpac's own words: **first 3GB every 24 hours at standard
speed, then up to 1Mbps until the next 24-hour cycle.** So `per_day`, 3GB.

Data only, no SMS. Calls are a separate voice pack used through the Jetpac app —
`app_voip` if we build the voice column, not `none` and certainly not `native`.

All figures below are the 30-day validity tab. Shorter 7, 4 and 1-day tabs exist
and are cheaper; not captured this pass.

| Pack | Japan | Europe | USA | Thailand |
|---|---|---|---|---|
| 5GB | £8.50 | £13.50 | £11 | £6 |
| 10GB | £13.50 | £18.50 | £16 | £9.50 |
| 15GB | £17.50 | £22.50 | £18.50 | £10.50 |
| 20GB | £33 | £33 | £29 | £23 |
| 30GB | £25 | £25 | £25 | £20 |
| 40GB | £29 | £29 | £29 | £25 |
| Unlimited 30d | £54.50 | £54.50 | £56 | £54.50 |

Global: unlimited 30 days £143; 50GB 365 days £204.50. Both a long way above
everyone else's global pricing.

Jetpac's lounge perk (SmartDelay, register through their app) is still advertised
on every destination page.

## Orange Travel — pounds shown, euros charged

Orange prices in pounds on a UK connection, but there is a line in small print at
the top of every page:

> Prices converted at the rate in effect on Aug 25, 2026. Payment will be made in Euro.

**So the pound figure is an estimate, not the price.** The card is charged in
euros at whatever the rate is on the day, plus whatever the buyer's bank adds for
a foreign currency transaction. Orange is the only provider in this check that
does that. If we list them, the row needs to say so — a price that is right on
the page and wrong on the statement is exactly the kind of thing this site exists
to catch.

The figures below are the pounds Orange showed on 5 September.

**A correction to the first check: only Europe gets unlimited calls and texts.**
Everywhere else the Data+Calls+SMS plans are metered, and some of the allowances
are small — the USA 20GB plan gives 15 minutes and 50 texts. The first check read
"Data+Calls+SMS unlimited" on the USA page; that "unlimited" was the data tab.

### Europe — Data + Calls + SMS (unlimited calls and texts, genuinely)
20GB 14d £21.99 · 50GB 30d £38.99 · 100GB 30d £41.99 (was £58.99) ·
200GB 30d £49.99 (was £76.99) · 500GB 90d £85.99 (was £145.99)

### Japan — data only
1GB 7d £0.99 · 3GB 7d £6.99 · 5GB 7d £8.99 · 10GB 7d £11.99 · 10GB 14d £12.99 ·
20GB 14d £21.99 · 20GB 30d £11.99 (was £22.99) · 50GB 30d £36.99 ·
100GB 30d £23.99 (was £47.99) · 100GB 45d £48.99

**Japan 1GB for seven days at 99p** is the cheapest single row anywhere in this
check. Either a loss-leader or a mistake, and worth opening before it goes live.
Note also that 100GB for 30 days at £23.99 costs less than 50GB at £36.99 — the
same discount-only-on-some-tiers problem Jetpac has.

### USA — data only
Unlimited 5d £13.99 (was £17.99) · 1GB 7d £5.99 · 3GB 7d £7.99 · 5GB 7d £9.99 ·
10GB 7d £16.99 · 10GB 14d £17.99 · 20GB 14d £25.99 · 20GB 30d £16.99 (was £33.99) ·
50GB 30d £42.99 · 100GB 30d £27.99 (was £55.99) · 100GB 45d £59.99

### USA — Data + Calls + SMS (metered)
2GB 7d £8.99 (15 texts, 15 min) · 5GB 7d £17.99 (30 texts, 30 min) ·
10GB 14d £25.99 (100 texts, 60 min) · 20GB 30d £20.99 (50 texts, 15 min) ·
50GB 30d £35.99 (50 texts, 15 min) · 100GB 30d £41.99 (50 texts, 60 min)

### Thailand — data only
Unlimited 1d £6.99 · 3GB 7d £5.99 · 5GB 7d £7.99 · 10GB 7d £9.99 · 10GB 14d £10.99 ·
20GB 14d £17.99 · 20GB 30d £8.99 (was £17.99) · 30GB 30d £23.99 · 50GB 30d £24.99 ·
100GB 30d £19.99 (was £39.99) · 100GB 45d £40.99

### UK inbound — data only
Unlimited 5d £14.99 (was £20.99) · 1GB 7d £3.99 · 3GB 7d £5.99 · 5GB 7d £7.99 ·
10GB 7d £11.99 · 10GB 14d £11.99 · 20GB 14d £15.99 · 20GB 30d £16.99 ·
50GB 30d £25.99 · 100GB 30d £29.99 · 100GB 45d £30.99 · 200GB 45d £51.99 ·
500GB 90d £79.99

### UK inbound — Data + Calls + SMS (metered)
1GB 7d £4.99 (200 texts, 60 min) · 3GB 7d £7.99 (200/60) · 5GB 7d £9.99 (200/60) ·
10GB 7d £13.99 (500 texts, 120 min) · 10GB 14d £14.99 · 20GB 14d £18.99 ·
20GB 30d £19.99 · 50GB 30d £30.99 (1000 texts, 180 min) ·
100GB 30d £35.99 · 100GB 45d £36.99 · 200GB 45d £61.99 (1000 texts, 300 min)

These UK inbound calls-and-texts rows are the strongest thing found for the
inbound cluster. A visitor gets real minutes and real texts, which is exactly
what EE's Travel eSIM cannot give them.

**Still unanswered: which country issues the number.** Searched again, and Orange
still will not say. Until they do, the inbound rows cannot claim a +44 number.

## Sim Local — real GBP, confirmed

Another one that shows a British visitor dollars by default. The switcher is
under Language / Currency; picking GBP sticks.

Sim Local resells other networks' plans rather than running its own, so what
matters here is that these are **real UK network plans with calls, texts and a
number** — the thing the travel eSIM providers mostly cannot offer.

### UK inbound — all Data / Calls / SMS
| Network | Plan | Duration | Price |
|---|---|---|---|
| Three UK | 20GB | 30 days | £10 |
| Three UK | 100GB | 30 days | £15 |
| Three UK | 200GB | 30 days | £20 |
| Three UK | Unlimited | 30 days | £35 |
| Three UK | Unlimited | 90 days | £90 |
| EE UK | 30GB / 80GB | 30 days | £15 |
| EE UK | 100GB / 150GB | 30 days | £20 |
| EE UK | Unlimited | 30 days | £40 |
| Lycamobile | 20GB | 15 days | £10 |
| Lycamobile | 100GB | 15 days | £20 |

The Three rows carry roaming; the EE rows carry unlimited local SMS. Three UK
plans through Sim Local include a real +44 number — confirmed in the first check.
Number provision on the EE and Lycamobile rows is still unconfirmed.

Note the EE plans are listed as two data figures ("30 GB eSIM | 80 GB eSIM"),
which is a promotional double-data offer rather than a choice. Worth opening one
before publishing a figure.

**These are the same networks Sim Local resells, and the direct prices are often
better** — Three's own PAYG £10 pack gives 40GB against Sim Local's 20GB for the
same money. Sim Local's advantage is that a visitor can buy before they arrive.

### Japan — data only, on AU (KDDI)
Unlimited 4d £9.50 · 7d £14.00 · 10d £19.25 · 15d £28.75 · 30d £57.25

No sized packs on Japan any more. The 4-day at £9.50 and 7-day at £14 both
undercut Holafly for the same lengths.
