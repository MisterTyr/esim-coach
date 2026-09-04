# Prompt 01 — Configure brand

**When:** first, once. **Edits:** `data/config.json`, `assets/styles.css`.

Most of this is already set (brand "eSIM Sorted", domain esim-sorted.co.uk). Use this
prompt only if you want to change the name, tagline, regions, or colours.

---

PASTE THIS:

```
I have a JSON config for a static eSIM comparison site. Update it with these
values and return the complete file, nothing else:

- brand: [eSIM Sorted]
- tagline: [Find your best-value eSIM in seconds.]
- base_url: [https://esim-sorted.co.uk]
- one-sentence meta description: [DESCRIPTION]
- regions to show as filters: [Europe, North America, Asia, South America, Oceania, Africa, Global]

Current file:
[paste the contents of data/config.json]
```

To change colours, open `assets/styles.css` and edit the `:root` block at the
top (`--accent` is the green button/highlight, `--bg` the page background). Ask
an assistant: "Give me a `:root` block using [BRAND COLOUR] as the accent on a
dark background, same variable names."

After any change, rebuild:

```
python3 scripts/update_plans.py && python3 scripts/build_static.py
```
