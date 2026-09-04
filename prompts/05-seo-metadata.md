# Prompt 05 — SEO titles and descriptions

**When:** before launch and after adding pages. **Edits:** `title`/`desc` in
`scripts/content.py` and `data/config.json`.

Titles and meta descriptions are what people see in Google. Tighten them in one
batch.

---

PASTE THIS:

```
Here are page titles and meta descriptions for a travel eSIM comparison site
(brand: eSIM Sorted). Rewrite each pair to be more clickable in search results.

Rules:
- Title: under 60 characters, includes the main keyword, ends with " | eSIM Sorted"
  where it fits.
- Description: 140-160 characters, one benefit + a reason to click. No hype words.
- Return as a simple list: filename -> new title -> new description.

Pages:
[paste each filename with its current title and desc from content.py / config.json]
```

Apply the results by editing the `title` and `desc` fields in
`scripts/content.py` (and the homepage `description` in `data/config.json`),
then rebuild:

```
python3 scripts/build_static.py
```
