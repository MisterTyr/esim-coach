# Reference: the eSIMDB pipeline (disabled)

This is the September 2026 eSIMDB ingestion pipeline, kept for its logic and not to be run.
eSIMDB's terms (last updated 17 June 2026) forbid scraping, bulk access, and using
their plan database to build or run a competing product. So the entry point raises
on start, and every scraped plan was deleted on 5 November 2026.

The code is ours, and the useful parts are being reused by our own collectors:

- `parse.py`: unlimited detection, daily caps parsed from plan names, throttle speeds, telephony
- `build.py`: plan types, and coverage stored as one plan with many countries
- `changes.py`: change detection between runs
- `verify.py`: quality flags and the checking queue
- `links.py`: affiliate link rules (`affiliate` / `provider_site` / `none`)

The test fixture was left out on purpose, because it was trimmed eSIMDB data.
`ESIMDB-PIPELINE-README.md` is the original write-up.
