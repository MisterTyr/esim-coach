# Prompt 03 — Affiliate links

**When:** before you monetise. **Edits:** `product_url` values in `data/sample_plans.csv`.

This is a checklist plus a find-and-replace, not really an AI task. The site
already appends your UTM tags automatically; you just need each provider's
affiliate link format.

## Programs to apply to
Most travel eSIM providers run affiliate programs, usually via a network:
- **Airalo** — Partnerize
- **Nomad** — affiliate program / Impact
- **Holafly** — affiliate program
- **Saily** (NordVPN's eSIM) — via their affiliate network

Apply, get approved, and grab either your affiliate link format or a tracking
parameter (often `?ref=` or a wrapped network URL).

## Dropping links in
In `data/sample_plans.csv`, replace each `product_url` with your affiliate
version of that plan's page. The pipeline adds `utm_source/medium/campaign` on
top, so don't add those yourself.

To rewrite many at once, PASTE THIS:

```
Here are CSV rows with a product_url column. Replace each product_url with the
affiliate format below, keeping every other column identical. Return the full
CSV.

Affiliate format: [e.g. append ?ref=MYID  OR  wrap as https://network.link/xxx?url=ENCODED]

Rows:
[paste the rows]
```

Then rebuild. Check one link in a browser to confirm it tracks before trusting
the rest.
