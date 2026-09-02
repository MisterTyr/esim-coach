# Prompt 02 — Collect real plan data

**When:** before launch, then whenever you add providers. **Edits:** `data/sample_plans.csv`.

This is the one that turns a demo into a real site. You need real plans in the
exact CSV schema the pipeline expects. Do one provider per run so the model
stays accurate, then paste the rows together.

The CSV columns (header row already in the file):
`provider,plan_name,region,country,data_gb,validity_days,price,product_url,timestamp`

- `data_gb`: a number, or the word `unlimited`
- `price`: number only, no symbol (in the site's display currency — GBP by default; set in `data/config.json`)
- `product_url`: the plan's page (you'll swap in your affiliate link in prompt 03)
- `timestamp`: today's date as `YYYY-MM-DDT09:00:00Z`

---

PASTE THIS (once per provider):

```
You are building a CSV of travel eSIM plans for comparison. Return ONLY CSV
rows (no header, no commentary) for [PROVIDER, e.g. Airalo]'s most popular
travel data plans across these regions: [Europe, North America, Asia, ...].

Columns in this exact order:
provider,plan_name,region,country,data_gb,validity_days,price,product_url,timestamp

Rules:
- One row per plan. 3-6 plans per region max, the popular sizes.
- data_gb is a number or the word unlimited. price is a number, no symbol.
- region must be one of: Europe, North America, Asia, South America, Oceania, Africa, Global.
- product_url = the plan's public page on the provider's site.
- timestamp = [TODAY]T09:00:00Z for every row.
- If unsure of a current price, leave that plan out rather than guess.
```

> Prices change constantly and models can be out of date. Treat generated
> prices as a starting point and verify against the provider's live site before
> you rely on them. For accuracy at scale, pull from a provider API or a shared
> Google Sheet (see `data/config.json` sources) instead of generating prices.

Paste all rows under the header in `data/sample_plans.csv`, then rebuild:

```
python3 scripts/update_plans.py && python3 scripts/build_static.py
```
