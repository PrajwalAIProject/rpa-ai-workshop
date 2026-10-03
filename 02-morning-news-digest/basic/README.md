# Project 2 — Basic: News Digest

## What you'll build

A one-file script that pulls headlines from a few RSS feeds with `feedparser` and
prints the top five. RSS instead of scraping homepages, for the same reliability
reason as Project 1 — feeds don't break when a site restyles its front page.

## Prerequisites

- Python 3.11+ and the shared dependencies installed (see
  [`00-prerequisites/README.md`](../../00-prerequisites/README.md)).
- No API key needed for this tier.

## Step-by-step setup

1. Activate your virtual environment and install dependencies:
   ```bash
   pip install -r 00-prerequisites/requirements.txt
   ```
2. Run it:
   ```bash
   cd 02-morning-news-digest/basic
   python news_digest.py
   ```
3. Expected output (headlines will differ):
   ```
   Morning headlines (top 5)
   =========================
   1. [BBC] Some headline here
      https://www.bbc.co.uk/news/...
   ...
   ```

## Common errors and fixes

- **`ModuleNotFoundError: No module named 'feedparser'`** — Activate the venv and
  re-run `pip install -r 00-prerequisites/requirements.txt`.
- **"No headlines could be fetched"** — You're offline, or every feed URL failed.
  The script catches this and exits cleanly; check your connection and retry.
- **One feed is empty but others work** — Normal; a single feed may be down. The
  script just skips it and uses the rest.
