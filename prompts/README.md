# eSIM Sorted — prompt pack

Copy-paste prompts to get the site live fast. Each one is self-contained: paste
it into any chat assistant, fill the `[BRACKETS]`, run. They're written to be
token-light — short instructions, tight output formats, no re-explaining context
each time.

## Order to run them
1. `01-configure-brand.md` — set name, domain, colours (mostly done already).
2. `02-collect-plan-data.md` — build your real `data/sample_plans.csv`.
3. `03-affiliate-signup.md` — get your affiliate links, drop them in.
4. `07-deploy.md` — push live (do this early with sample data, then iterate).
5. `04-blog-post.md` — add articles for SEO, one at a time.
6. `05-seo-metadata.md` — tighten titles and descriptions.
7. `06-email-and-social.md` — content for the list and socials.

## Keeping token use low
- **Batch, don't chat.** Ask for the full CSV or full article in one go. Every
  back-and-forth re-sends the whole conversation.
- **Use a cheap model for bulk work.** Data extraction, social captions and first
  drafts don't need a frontier model. On Claude, Haiku is the cheap tier; reserve
  a bigger model for final polish only.
- **Give the exact output format.** These prompts specify columns and structure so
  the answer drops straight into a file with no cleanup round-trips.
- **Reuse, don't regenerate.** Once a prompt gives good output, save the output —
  don't re-run it to get the same thing.

## The one rule that matters
The pipeline reads `data/sample_plans.csv`, ranks it, and rebuilds every page.
Everything else is content. Get real data into that CSV and you have a real site.
