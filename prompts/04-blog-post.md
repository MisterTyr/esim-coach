# Prompt 04 — Blog / guide post

**When:** ongoing, for SEO. **Edits:** adds an entry to `scripts/content.py`.

Every article is one entry in the `PAGES` dict in `scripts/content.py`. The
builder wraps it in the site's header/footer automatically, so you only write
the body. Good targets: destination guides ("Best eSIM for Japan"), comparisons
("Airalo vs Holafly"), and how-tos.

---

PASTE THIS:

```
Write the BODY of a web article titled "[TITLE, e.g. Best eSIM for Japan in 2026]"
for a travel eSIM comparison site. Audience: travellers who want data abroad
without roaming fees.

Output HTML only, no <html>/<head>/<body>, no <h1> (the site adds it). Use:
- an opening paragraph (no heading)
- 3-5 <h2> sections with <p> paragraphs
- one <p> at the end linking to the homepage: <a href="/">compare plans</a>

Constraints:
- 400-600 words. Plain, useful, no fluff or hype.
- Concrete and specific. No invented prices; talk value, coverage, trade-offs.
- One internal link to /how-to-install-esim.html where it fits naturally.

Also return, on the first line only: a 150-char meta description.
```

## Adding it to the site
Open `scripts/content.py` and add an entry to `PAGES`:

```python
"best-esim-japan.html": {
    "title": "Best eSIM for Japan in 2026",
    "desc": "PASTE THE META DESCRIPTION",
    "body": """PASTE THE HTML BODY""",
},
```

Then rebuild and it appears as a real page:

```
python3 scripts/build_static.py
```

Add new pages to the sitemap list in `scripts/update_plans.py` (the `pages`
array in `write_sitemap`) so search engines find them.
