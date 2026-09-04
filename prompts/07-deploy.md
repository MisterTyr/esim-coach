# Prompt 07 — Deploy

**When:** early. Deploy with sample data first, then keep editing — it's live in minutes.

The site is plain static files at the repo root (`index.html`, the other
`.html` pages, `plans.json`, `sitemap.xml`, `assets/`). Any static host serves
it with no build step. Pick one.

## Option A — Cloudflare Pages (recommended)
1. Push this folder to a GitHub repo.
2. Cloudflare dashboard → Pages → Connect to Git → pick the repo.
3. Build command: leave empty. Output directory: `/` (root).
4. Deploy. Add your domain (esim-sorted.co.uk) under the Pages project's Custom Domains.

## Option B — Netlify
1. Push to GitHub.
2. Netlify → Add new site → Import from Git → pick the repo.
3. Build command: empty. Publish directory: `.` (root).
4. Deploy, then add the custom domain in Domain settings.

## Option C — GitHub Pages
1. Push to GitHub.
2. Repo → Settings → Pages → Source: deploy from branch `main`, folder `/root`.
3. The `CNAME` file already points at esim-sorted.co.uk — set that domain in Pages settings
   and add the DNS record your host shows you.

## Daily auto-refresh
`.github/workflows/update.yml` re-runs the pipeline every day at 06:17 UTC and
commits the updated `plans.json` and pages. It works out of the box on GitHub.
To point at a live data source instead of the sample CSV, enable the Google
Sheet source in `data/config.json` and set its URL.

## Sanity check after deploy
- Homepage loads, region filter buttons work.
- A "Get this plan" link opens the provider (with your affiliate + UTM tags).
- `/sitemap.xml` and `/robots.txt` load.
- Submit the sitemap in Google Search Console.

---

### Quick assistant prompt if a host errors

```
My static site (plain HTML at repo root, no build step) fails to deploy on
[HOST] with this error: [ERROR]. What's the fix? Keep it to the specific
setting to change.
```
