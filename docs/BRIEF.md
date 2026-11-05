# eSIM Sorted — rebuild brief

Phase 1 of the rebuild. Written 5 November 2026. Everything marked **[Marty]**
is a proposal waiting for your decision; nothing here is built yet.

## Why rebuild

The old site was a ranked table of hand-typed plans. Three things were wrong
with it, in your words: the concept, the data, and the look and content.

- **Concept.** A table ranked on price per GB answers a question few people
  ask. People ask "I'm going to Japan for ten days, what do I buy?"
- **Data.** A hand-kept Sheet of about 200 rows was two months stale before it
  ever went live.
- **Look and content.** It read like a template. Nothing about it said why to
  trust it over Airalo's own site or any roundup.

## The idea

**Tell us your trip. We'll tell you which eSIM to buy, and what the catch is.**

Headline price is rarely what goes wrong with a travel eSIM. The small print
is. Everything we found in September is that kind of problem:

- "Unlimited" usually means 2–5GB a day at full speed, then slow.
- Holafly publishes no throttle figure at all, and caps hotspot at 1GB a day.
- Nomad's cheapest Thailand plan starts its clock when you *install* it, not
  when you land.
- Orange shows pounds and charges euros.
- Ubigi, Jetpac and Sim Local show a British visitor dollars by default.
- EE's UK Travel eSIM cannot call 999.
- eSIM.dog's breakout IP is in France or the Netherlands, so some UK services
  won't see a UK address.

No comparison site prints these next to the price. We will. **The catch is
the product.**

## Who it's for

1. **UK travellers going abroad.** The bulk of the traffic, and the bulk of
   the affiliate programmes.
2. **Visitors coming to the UK.** Smaller, but it's where a UK-run site has a
   real edge. It means comparing travel eSIMs against the UK networks
   themselves: Three, O2, SMARTY, giffgaff and EE. No travel-eSIM site does
   that.

One site, two front doors. The picker's first question decides which one.

### A question nobody else asks: do you need one at all? — agreed 5 Nov, in at launch

A lot of UK travellers already have roaming. It's free on some plans, and a
daily charge on others. For a weekend in Spain, the honest answer is
sometimes "use what you've got". The picker should be able to say that. It
costs us a click, and it's what makes people trust everything else we say.
Your home network's roaming terms become a baseline row, alongside the eSIMs.

## The product

### The picker (the homepage)

There are four questions, and each one takes a single tap:

1. **Where are you going?** A country, a region, or "the UK".
2. **For how long?** In days.
3. **How do you use your phone?** "Maps and messages", "Normal: some
   social, some video", "Heavy: streaming, hotspot for a laptop". Each
   answer maps to a daily GB figure that we publish, so nobody has to guess
   how many gigabytes they need.
4. **Do you need calls, texts or a phone number?** Inbound visitors also get
   asked whether they need a UK number.

You get **one to three recommendations**. Each one shows:
- the price, in the currency you'll actually be charged
- why it fits your trip, in one sentence
- **the catch**, in one sentence, in the same size type as the price
- when the price was last checked, against the provider's own site

Then a single link: "see every plan for Japan". That's where the full
filterable table lives, for people who want to dig.

The picker runs in the browser from a published JSON file. There's no
server, nothing to log in to, and nothing tracked.

### Guides (the SEO, AEO and GEO surface)

- **Destination hubs.** About 15 at launch. Each one opens with a dated,
  quotable answer ("For 10 days in Japan, most people need about 15GB. The
  best value on 5 November was…"), with the picker embedded and preset to
  that destination. Then what's different about that place: networks, 5G,
  VoIP rules, whether your UK roaming already covers it.
- **The UK visitor hub.** Travel eSIMs against the UK networks, a real +44
  number, 999, and buying before you land.
- **Provider pages.** A short, dated review of each provider we list:
  catches, currency, refunds, hotspot.
- **Explainers.** What "unlimited" actually means, how much data you need,
  checking whether your phone takes an eSIM, and installing one before you
  fly.

**Rule: no page without real data behind it.** No "best eSIM for [every
country]" pages generated from a template. Google penalises thin pages built
at scale, AI answer engines don't quote them, and we would be making claims
we hadn't checked.

### Optimising for search, answer engines and AI (SEO, AEO, GEO)

Every page gets:
- **The answer first.** One or two sentences that work when quoted out of
  context, with a date in them.
- **Its sources visible.** Every price and every catch links to the
  provider's own page, with the date we checked it. AI answer engines prefer
  sources that cite their own sources, and so do people.
- **Structured data:** `FAQPage` on the guides, `Product` and `Offer` on each
  plan, `ItemList` for the recommendations, `Organization`, and
  `BreadcrumbList`.
- A real "last updated" date that only changes when the facts change.
- Pages that work without JavaScript, with fast load times and a clean
  heading structure.
- An `llms.txt` file and a sitemap, and AI crawlers allowed in `robots.txt`.
- An about page with a named person behind the site, and the methodology
  written out. That's what Google means by experience and trust, and it's
  what an AI checks before quoting a site.

## Data

### What we already have

| Source | What it is | Can we publish it? |
|---|---|---|
| `data/verified/` (4–5 Sep) | 229 travel-eSIM rows in GBP, plus Airalo and the UK networks, checked against providers | Yes. It's our own work. But it's two months old, so it needs re-checking before launch |
| `data/PRICE-CHECK-*.md` | The catches, written up per provider | Yes. This is the backbone of the "catch" copy |
| `MARKET-RESEARCH`, `PROVIDER-SCOUTING` | Market research and the provider shortlist | Yes, as research |
| `../_archive/esimdb/` | 627,826 plans, 223 providers, scraped 6 Sep | **No.** See below |
| `esimdb/data/provider_verification.csv` | eSIM.dog checked against esim.dog, 7 Sep | Yes. It's our own work |

### eSIMDB: what we can and can't use

eSIMDB's terms (last updated 17 June 2026, so they were in force when the
September run was made) forbid scraping, bots and bulk access, and forbid
using their plan database "to build, enrich, benchmark, or operate a
competing product". They also claim database rights, which UK law protects
separately from copyright. A UK comparison site built on their catalogue is
exactly what those clauses describe. I'm not a lawyer, but I don't think this
one needs one.

**So: none of the eSIMDB plan data goes on the site, and we don't run the
scraper again.**

What stays usable:

- **The pipeline code.** All 2,200 lines of it are ours: the schema, unlimited
  parsing, plan types, coverage modelling, change detection, quality flags,
  the verification queue, and the affiliate-link rules. Most of it carries
  straight over to our own collectors. It currently lives only in
  `_archive/esimdb` and **isn't in git anywhere**. It goes into this repo
  first.
- **The schema lessons.** They hold whatever the source. Coverage is a
  plan-to-country table, not one row per country. Unlimited needs a daily cap
  and a throttle speed. Telephony is inbound and outbound for voice and SMS
  separately.
- **The eSIM.dog verification** and the affiliate-network findings: Impact
  covers Airalo, Ubigi, Nomad, Amigo and others, and Awin covers Sim Local and
  SimWallet. We confirmed those on the providers' own sites.

### Building our own provider list — agreed in principle 5 Nov

We use eSIMDB's provider *names and websites* only as a lead list, alongside
other sources: the Impact and Awin marketplaces, app stores and search. Then
we check every provider on its own site. That way no provider is in our
list just because eSIMDB has it. Nothing eSIMDB-specific comes across: not
their "certified" flag, their plan counts, their promo codes (ESIMDB15 and
the like), their ratings or their tracking links. A provider discovery tool
visits each provider's own site, checks `robots.txt`, and records:
- the real site and whether it sells in GBP
- whether there's an affiliate, partner or creator programme, with the page
  that says so
- which network runs it (Impact, Awin, CJ, PartnerStack, Tapfiliate,
  Rewardful, Everflow or in-house), spotted from the signup link
- the published commission and cookie length, where there is one
- the date checked, with a link to the page as evidence

The output is a review list. A person confirms each row before it counts.

**[Marty] Ask eSIMDB for permission anyway.** Their terms allow use "with our prior
written permission", and they cover "partner interfaces". A licensed feed
would give us the breadth that collectors never will. I'd email them this
week. I can draft the email. If they say yes, eSIMDB becomes the catalogue
and our own checks become the layer on top. If they say no, we've lost
nothing.

**[Marty] The 1.1GB of scraped data in `_archive/esimdb/data/`.** I'd delete
the scraped data, keep the code, and keep `provider_verification.csv` and
`provider_links.csv` (our own work). Your call.

### How the data stays current in an hour a week

- **A collector for each provider**, starting with 8–10: Airalo, Nomad, Saily,
  Holafly, Ubigi, Jetpac, Sim Local, eSIM.dog, Orange and Three. Each one
  reads that provider's prices in GBP. Several sites need JavaScript to set
  the currency, so the collectors run a real browser.
- Once the affiliate programmes approve us, **their product feeds replace the
  collectors where they can.** Feeds are licensed and they don't break.
- **Nothing publishes on its own.** A weekly GitHub Action collects, compares
  against last week, and opens a pull request with a plain summary:

  > Saily Japan 10GB £12.99 → £11.49. Nomad dropped its 3GB tier.
  > Holafly unchanged. ⚠ Jetpac collector failed — last good data 29 Oct.

  You read it and approve it. That's the hour. It also closes the old trap of
  pushing straight to `main`.
- **Gates that stop a PR from being mergeable:** a price that moves more than
  40%, a provider losing more than half its plans, a collector failing, or
  any plan older than 21 days still on show.
- **Catches are data, not prose.** These are fields: throttle speed, daily
  cap, hotspot limit, voice and SMS (in and out), number country, can it call
  999, charged currency, when the clock starts, refundable, 5G, KYC. The
  picker reasons with them, and the card copy is generated from them.
- **Our checks override everything.** A provider-and-country table, like
  eSIMDB's `provider_verification.csv`, holds what we checked by hand
  (networks, activation, fair use), and it's joined in on every run.

## Brand

### Voice — agreed 5 Nov

**Plain, straight, on your side.**

- *Plain*: British spelling, short sentences, no jargon left unexplained.
- *Straight*: we say the catch before you find it, and we say "you don't
  need one" when that's true.
- *On your side*: we write like a friend who checked, not a shop.

**It never says** "unlimited" without saying what the limit really is.

### Paid placement — agreed 5 Nov

Honest Mobile's pin is the only paid placement. The rules:

- The picker's recommendations are **never** paid. Merit only. That's the
  promise the whole site rests on.
- Paid placement can appear only as a clearly labelled "Sponsored" slot
  *below* the recommendations, and in the full table, with the same catch
  line as everyone else.
- Wording on the slot: **"Sponsored. Honest Mobile pays to appear here. It
  doesn't change our recommendations."**
- Affiliate links, which earn on a sale but don't change the order, get a
  single sitewide line: "We earn a commission if you buy through our links.
  It never changes what we recommend."

### Look

Keep the logo and palette, with Blue Slate carrying the type and the warm
colours as fills. The rebuild gets proper design time in Phase 3. The picker
should feel like a short, friendly form, not a spreadsheet.

## Launch destinations — agreed 5 Nov

15, chosen for UK outbound traffic, plus the UK visitor hub:

Europe (multi-country), Spain, France, Italy, Portugal, Greece, Turkey, USA,
Canada, Mexico, Japan, Thailand, UAE, Australia, Egypt. **Plus: the UK, for
visitors.**

**Second wave, soon after launch (proposed):** China (blocked apps on local SIMs,
which some eSIMs get around), India (ID check, and many eSIMs don't work there),
Vietnam, Indonesia (Bali), Sri Lanka, Maldives, South Korea, Singapore, Morocco,
South Africa, Dominican Republic and the Caribbean, New Zealand.

## Stack

- **Astro**, building static HTML. Good for search, fast, and there's no
  server to keep alive. The picker is a small island of JavaScript reading
  `plans.json`.
- **Data:** JSON in the repo, changed only through the weekly PR. No
  database.
- **Collectors:** Python, carried over from the eSIMDB pipeline, with
  Playwright for the JavaScript-priced sites. They run in GitHub Actions.
- **Hosting:** Cloudflare Pages, with a preview URL for every branch. The
  domain moves from GitHub Pages at switch-over.
- **Analytics:** Cloudflare Web Analytics. It's free, uses no cookies, and
  needs no consent banner.

## Phases

1. **Brief.** This document, plus your decisions on the [Marty] items.
2. **Data.** Bring the eSIMDB code into the repo. Build the new schema. Build
   collectors for the first 8–10 providers. Build the weekly review PR and its
   gates. Re-check the verified rows.
3. **Picker and design.** Astro scaffold, the picker, plan cards with the
   catch line, and the full tables.
4. **Content.** The 15 destination hubs, the UK visitor hub, provider pages,
   explainers, structured data and `llms.txt`.
5. **Deploy.** Cloudflare Pages, the domain switch, Search Console, analytics,
   affiliate links in place, and the holding page down.

**Start now, alongside the build:** apply to Impact (one account covers
Airalo, Ubigi, Nomad and four more), chase Awin, and apply in-house to Saily
and Jetpac. The domain is live, so nothing is holding these up.

## Decisions needed from you

1. Email eSIMDB for permission? (I'd say yes. I'll draft it.)
2. Delete the scraped eSIMDB data, keep the code?
3. Voice: "plain, straight, on your side", and never "unlimited" without
   the limit?
4. Paid placement: never in the picker, only a labelled sponsored slot?
5. The 15 launch destinations?
6. Should the "do you need one at all?" baseline (your own network's roaming)
   go in at launch?
