# Project 2 — Advanced: Categorized Digest

## What you'll build

A script that pulls several RSS feeds, categorizes each headline by keyword
(business / tech / sports / general), ranks each category by recency, and renders a
formatted **Markdown** digest (with an optional **HTML** version).

## Prerequisites

- Everything from the [basic tier](../basic/README.md).
- The shared dependencies installed from
  [`00-prerequisites/requirements.txt`](../../00-prerequisites/requirements.txt).
- No API key needed for this tier.

## Step-by-step setup

1. Activate your virtual environment and install dependencies:
   ```bash
   pip install -r 00-prerequisites/requirements.txt
   ```
2. Run it:
   ```bash
   cd 02-morning-news-digest/advanced
   python news_digest_categorized.py          # Markdown only
   python news_digest_categorized.py --html   # also writes digest.html
   ```
3. What it produces:
   - prints the digest to the terminal,
   - writes `digest.md` (and `digest.html` with `--html`) next to the script.
4. To run it every morning, schedule it with your OS scheduler:
   - **Windows:** Task Scheduler → Create Basic Task → run
     `python news_digest_categorized.py`.
   - **macOS / Linux:** a `cron` entry, e.g. `0 7 * * * cd /path && python news_digest_categorized.py`.

   > _Screenshot placeholder: the Windows Task Scheduler "Create Basic Task" wizard._

## Common errors and fixes

- **Everything lands in "general"** — The keyword lists are intentionally small. Add
  terms to `CATEGORY_KEYWORDS` to tune categorization for your feeds.
- **Headlines look out of order** — Some feeds omit a published date; those entries
  sort to the bottom. That's expected.
- **"No headlines could be fetched"** — Offline or all feeds failed. Check your
  connection and retry.
