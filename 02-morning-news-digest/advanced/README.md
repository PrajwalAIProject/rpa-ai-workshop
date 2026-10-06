# Project 2 — Advanced: a categorised news page from 8 feeds

## What you'll build

`news_report.py`: it reads 8 news feeds (Indian and world news, markets, tech, cricket),
keeps only the **last 24 hours**, removes duplicates, sorts every story into **India,
World, Business, Tech or Sports**, and writes a clean **`digest.html`** news page you
open in the browser. It also saves `digest.json`, which the expert level reuses.

Sorting works by **rules**: each feed has a default category, and keywords in the
headline can move a story (for example, "Sensex" moves it to Business). You'll see where
rules work well and where they make mistakes. The expert level fixes that with AI.

## Before you start

- The [basic level](../basic/README.md) done, in the same VS Code folder.
- No API key needed.

## Step 1 — Give Copilot this prompt (Agent mode)

```text
Create a Python 3 script called news_report.py in this folder. It builds on
news_digest.py (same safe download: requests with a 10-second timeout, then feedparser),
but makes a categorised news page.

1. Read these feeds; each has a default category:
   The Hindu https://www.thehindu.com/feeder/default.rss -> India
   Times of India https://timesofindia.indiatimes.com/rssfeedstopstories.cms -> India
   NDTV https://feeds.feedburner.com/ndtvnews-top-stories -> India
   Hindustan Times https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml -> India
   BBC World https://feeds.bbci.co.uk/news/world/rss.xml -> World
   ET Markets https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms -> Business
   ET Tech https://economictimes.indiatimes.com/tech/rssfeeds/13357270.cms -> Tech
   ESPNcricinfo https://www.espncricinfo.com/rss/content/story/feeds/0.xml -> Sports
2. Keep only stories from the last 24 hours, and remove duplicate headlines.
3. Keyword rules that override the feed's category, matched as WHOLE words with a regular
   expression (\b...\b) so "odi" does not match "Modi":
   Tech: ai, software, startup, app, google, microsoft, apple, chip, semiconductor, isro, openai
   Business: sensex, nifty, rupee, rbi, gdp, inflation, shares, ipo, budget, economy
   Sports: cricket, ipl, t20, odi, football, hockey, olympic, kabaddi, tennis, chess, world cup
4. In each category keep the 6 newest stories (title, source, link, a short summary
   without HTML tags).
5. Put the work in a function collect() that returns a dictionary, so another script can
   reuse it. Save it as digest.json.
6. Write digest.html: a simple, clean page with a coloured header (title, date and time,
   "last 24 hours") and one white card per category, each story a clickable headline that
   opens in a new tab, with the source and summary underneath. The cards must sit in a
   responsive grid that works on a phone. Escape all text with html.escape.
7. Print a short summary (3 headlines per category) and the names of any skipped feeds.
   With --open, open digest.html in the browser using webbrowser.
8. Clear error messages; short beginner-friendly comments.

Then run it with --open and fix any errors.
```

## Step 2 — Run it

```bash
python news_report.py --open
```

## What correct output looks like

The terminal shows a summary like this (real output, shortened), and your browser opens
the news page:

```text
Morning News Digest · 06 Oct 2026, 01:03 PM · last 24 h
============================================================
INDIA (6)
  - 'Best ever September': Auto retail sales surge 32% year-on-year  [The Hindu]
BUSINESS (6)
  - Viceroy Hotels shares rise 2% as Zerodha founders ... pick 6.72% stake  [ET Markets]
TECH (6)
  - DeepSeek to raise at least $12 billion in Tencent-backed funding  [ET Tech]
SPORTS (6)
  - Harmanpreet Kaur steps down as India captain  [ESPNcricinfo]

Saved: digest.html and digest.json
```

**Check it yourself, and look for rule mistakes.** Find two stories in the wrong
category. Why did the rules put them there? (For example, a story about Israel from The
Hindu lands in "India" because that is The Hindu feed's default.) Keep these examples:
the expert level shows how AI handles them.

## Stretch — make it a real morning digest

Ask Copilot: *"Show me how to run news_report.py every morning at 7:00 with Windows
Task Scheduler, step by step, and explain each setting."* (On macOS/Linux: `cron`.) A
script that runs by itself on a schedule is one of the things employers look for.

## If Copilot's script is wrong — follow-up prompts

- *"'India Mobile Congress' with PM Modi went into Sports. Match keywords as whole words with \\b in a regex."*
- *"The summaries show HTML tags like &lt;p&gt;. Strip the tags and keep plain text."*
- *"The page scrolls sideways on my phone. Make the grid responsive."*

Reference solution: [`news_report.py`](news_report.py).

## Common errors and fixes

| You see | Fix |
| ------- | --- |
| A category is missing from the page | No fresh stories matched it in the last 24 hours, or its feed was skipped. Normal on quiet days. |
| Stories in the wrong category | Expected with keyword rules. Adjust the keyword lists, and note the examples for the expert level. |
| Page shows strange symbols like `&amp;` | Unescape feed text with `html.unescape` before `html.escape` when writing the page. |
| `--open` does nothing | Open `digest.html` from the project folder by double-clicking it. |
| All feeds skipped | Internet or network block. Try a phone hotspot. |
