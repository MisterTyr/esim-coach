# eSIM Coach — 7-day launch plan

The build is done. This is the path from "files on disk" to "live, earning site"
in a week. Each day is an hour or two. Prompt files referenced are in `prompts/`.

## Day 1 — Deploy the skeleton (with sample data)
Get it live first; polish later. Push the folder to a GitHub repo, connect
Cloudflare Pages (`prompts/07-deploy.md`), point esim.coach at it. You now have a
working site with sample plans. Confirm the homepage, filters, and pages load.

## Day 2 — Real plan data
Run `prompts/02-collect-plan-data.md` once per provider (Airalo, Nomad, Holafly,
Saily to start). Paste rows into `data/sample_plans.csv`, rebuild, push. Verify a
few prices against the providers' live sites — don't trust generated prices blind.

## Day 3 — Affiliate links
Apply to the affiliate programs (`prompts/03-affiliate-signup.md`). Approvals can
take a day or two, so start early. As each comes through, swap the `product_url`
values to your affiliate links and rebuild. Test one link end-to-end.

## Day 4 — Content for SEO
Publish 2-3 articles with `prompts/04-blog-post.md` — start with destination
guides for high-traffic spots (Japan, Europe, USA, Thailand). Add each to
`content.py` and to the sitemap list in `update_plans.py`. Rebuild, push.

## Day 5 — SEO polish + Search Console
Tighten every title and description (`prompts/05-seo-metadata.md`). Set up Google
Search Console, verify the domain, submit `sitemap.xml`. Add a privacy-friendly
analytics tag if you want traffic numbers.

## Day 6 — Email + social presence
Load the 4-email welcome sequence (`automation/email-sequence.md`) into your email
tool and add a signup form. Create the social accounts and queue a week of
captions (`prompts/06-email-and-social.md`).

## Day 7 — Automate and check
Confirm the daily GitHub Action ran and committed a refresh (Actions tab). Walk
the whole site once as a visitor: every link, every page, mobile view. Fix
anything rough. You're live.

## After launch (keeps running itself)
- The daily cron refreshes rankings with no input from you.
- Add an article a week (Day-4 loop) to grow search traffic.
- Point `data/config.json` at a Google Sheet or provider API when you outgrow the
  CSV, so prices update from a real source.

## Where the money comes from
Affiliate commissions on outbound clicks. The ranking is honest (pure value maths),
which is what earns repeat visitors — and repeat visitors are what actually pays.
