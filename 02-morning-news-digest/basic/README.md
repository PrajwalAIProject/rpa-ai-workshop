# Project 2 — Basic: the latest headlines (with a topic filter)

## What you'll build

`news_digest.py`: it downloads the latest stories from four public news feeds (The
Hindu, Times of India, NDTV, BBC World) and prints the 10 newest, with source, how long
ago and link. Type a topic such as `cricket` or `ISRO` to see only matching headlines.
GitHub Copilot writes the code from the prompt below.

## Before you start

- [Python 3.11+](../../00-prerequisites/python-setup.md) and
  [VS Code with GitHub Copilot](../../00-prerequisites/git-and-editor.md), signed in to GitHub.
- A project folder (for example `C:\news-project`) opened in VS Code.

No API key needed for this level.

## Step 1 — Give Copilot this prompt (Agent mode)

```text
Create a Python 3 script called news_digest.py in this folder.

Goal: show me the latest news headlines from a few Indian and world news sites, and let
me filter them by a topic.

Requirements:
1. Use the requests and feedparser libraries (pip install requests feedparser).
2. Read these RSS feeds:
   The Hindu: https://www.thehindu.com/feeder/default.rss
   Times of India: https://timesofindia.indiatimes.com/rssfeedstopstories.cms
   NDTV: https://feeds.feedburner.com/ndtvnews-top-stories
   BBC World: https://feeds.bbci.co.uk/news/world/rss.xml
3. Download each feed with requests.get (10-second timeout, a browser-like User-Agent
   header) and then parse response.content with feedparser.parse. Do NOT call
   feedparser.parse(url) directly, because it has no timeout and can hang.
4. If one feed fails, print "(skipped <name>)" and carry on with the others.
5. Take a topic from the command line (python news_digest.py cricket), or ask for it with
   input(); an empty topic means all news. Match the topic case-insensitively in the title.
6. Remove duplicate headlines, sort newest first using published_parsed, and print the top
   10 as: number, title, then "source · X min/h ago · link" on the next line.
7. Clear one-line messages when nothing could be downloaded or no headline matches.
8. One file, under 90 lines, with short comments a beginner can follow.

Then install the libraries, run it once with no topic and once with "cricket", and fix any errors.
```

## Step 2 — Run it

```bash
python news_digest.py
python news_digest.py cricket
python news_digest.py "ISRO"
```

## What correct output looks like

Real output from the reference solution (headlines change all day):

```text
Top 10 headlines about 'India' · 06 Oct 2026, 12:58 PM
============================================================
 1. CEC row LIVE updates: Several INDIA bloc MPs detained by police during march to ECI
    The Hindu · 5 h ago · https://www.thehindu.com/news/national/...
 2. Harmanpreet Kaur steps down as captain of India women's team
    ...
```

A line such as `(skipped Times of India: ReadTimeout)` is fine. It means that site was
slow, and the script carried on with the others. That's the point of step 4.

**Check it yourself:** open one of the links. Is the headline really on that site, and
about as recent as the script says?

## If Copilot's script is wrong — follow-up prompts

- *"It hangs and never finishes. Download each feed with requests and a 10-second timeout, then parse the text with feedparser."*
- *"When one site is down the whole script crashes. Skip that feed with a message instead."*
- *"The same headline appears twice. Remove duplicates by title."*
- *"Add a 'Deccan Herald' or 'The Hindu Karnataka' feed."* (Ask Copilot to find the feed address, then check it works.)

Reference solution: [`news_digest.py`](news_digest.py).

## Common errors and fixes

| You see | Fix |
| ------- | --- |
| `ModuleNotFoundError: No module named 'feedparser'` | `pip install requests feedparser` in the VS Code terminal. |
| Script runs forever | It is calling `feedparser.parse(url)` with no timeout. Use `requests.get(url, timeout=10)` first (see the follow-up prompts). |
| `(skipped ...: ReadTimeout)` for every feed | No internet, or the network blocks news sites. Try a phone hotspot. |
| `SSL: CERTIFICATE_VERIFY_FAILED` | Campus or office HTTPS inspection. Use a hotspot, or `pip install truststore` and add `import truststore; truststore.inject_into_ssl()` as the first line. |
| Times show "time n/a" | That feed doesn't publish dates for some stories. Normal; they sort last. |
