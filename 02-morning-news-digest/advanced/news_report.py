"""Project 2 - Advanced: a categorised morning news page (HTML) from many feeds.

Reference solution. In the workshop you ask GitHub Copilot to write this file for you
(see README.md for the prompt); compare with this one if yours misbehaves.

What it does:
  1. Downloads 8 public RSS feeds (Indian + world news, markets, tech, cricket) with a timeout.
  2. Keeps only stories from the last 24 hours and removes duplicates.
  3. Puts each story in a category - India, World, Business, Tech, Sports - using the
     feed it came from plus keywords in the headline.
  4. Writes a clean, readable digest.html (opens in any browser) and digest.json
     (the expert level reuses it), and prints a short summary.

Run:
    python news_report.py            # writes digest.html and digest.json
    python news_report.py --open     # ...and opens the page in your browser
"""

import html
import json
import re
import sys
import webbrowser
from datetime import datetime, timedelta, timezone
from pathlib import Path
from time import mktime

import feedparser
import requests

# feed name -> (url, the category its stories usually belong to)
FEEDS = {
    "The Hindu": ("https://www.thehindu.com/feeder/default.rss", "India"),
    "Times of India": ("https://timesofindia.indiatimes.com/rssfeedstopstories.cms", "India"),
    "NDTV": ("https://feeds.feedburner.com/ndtvnews-top-stories", "India"),
    "Hindustan Times": ("https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml", "India"),
    "BBC World": ("https://feeds.bbci.co.uk/news/world/rss.xml", "World"),
    "ET Markets": ("https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms", "Business"),
    "ET Tech": ("https://economictimes.indiatimes.com/tech/rssfeeds/13357270.cms", "Tech"),
    "ESPNcricinfo": ("https://www.espncricinfo.com/rss/content/story/feeds/0.xml", "Sports"),
}
CATEGORIES = ["India", "World", "Business", "Tech", "Sports"]
# A headline containing one of these WHOLE words moves to that category, whatever feed it
# came from. Whole words matter: "odi" must not match "Modi", "app" must not match "happened".
KEYWORDS = {
    "Tech": ["ai", "artificial intelligence", "software", "startup", "app", "apps", "google",
             "microsoft", "apple", "chip", "chips", "semiconductor", "isro", "smartphone", "openai"],
    "Business": ["sensex", "nifty", "rupee", "rbi", "gdp", "inflation", "stock market", "shares",
                 "ipo", "budget", "economy", "q1", "q2", "q3", "q4"],
    "Sports": ["cricket", "ipl", "t20", "odi", "football", "hockey", "olympic", "olympics",
               "kabaddi", "tennis", "chess", "world cup", "asian games"],
}
KEYWORD_PATTERNS = {category: re.compile(r"\b(" + "|".join(map(re.escape, words)) + r")\b", re.I)
                    for category, words in KEYWORDS.items()}
HOURS = 24
PER_CATEGORY = 6
HERE = Path(__file__).resolve().parent


def fetch_feed(source, url, default_category):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (news-digest workshop)"}, timeout=10)
    response.raise_for_status()
    stories = []
    for entry in feedparser.parse(response.content).entries:
        published = entry.get("published_parsed") or entry.get("updated_parsed")
        summary = html.unescape(entry.get("summary", ""))
        if "<" in summary:  # some feeds put HTML in the summary; keep the text only
            summary = " ".join(part.split(">")[-1] for part in summary.split("<"))
        stories.append({
            "source": source,
            "title": html.unescape(entry.get("title", "")).strip(),
            "summary": " ".join(summary.split())[:240],
            "link": entry.get("link", ""),
            "time": datetime.fromtimestamp(mktime(published), tz=timezone.utc) if published else None,
            "category": default_category,
        })
    return stories


def categorise(story):
    for category, pattern in KEYWORD_PATTERNS.items():
        if pattern.search(story["title"]):
            return category
    return story["category"]


def collect():
    """Download, filter, de-duplicate and group the news. Returns a dictionary."""
    stories, skipped = [], []
    for source, (url, category) in FEEDS.items():
        try:
            stories += fetch_feed(source, url, category)
        except Exception as error:  # one broken feed must not stop the rest
            skipped.append(f"{source} ({error.__class__.__name__})")

    cutoff = datetime.now(timezone.utc) - timedelta(hours=HOURS)
    fresh = {}
    for story in stories:
        if not story["title"] or (story["time"] and story["time"] < cutoff):
            continue
        key = story["title"].lower()[:80]          # same headline from two feeds -> keep one
        fresh.setdefault(key, story)

    grouped = {c: [] for c in CATEGORIES}
    for story in fresh.values():
        story["category"] = categorise(story)
        grouped.setdefault(story["category"], []).append(story)
    for items in grouped.values():
        items.sort(key=lambda s: s["time"] or cutoff, reverse=True)
        del items[PER_CATEGORY:]

    return {
        "generated": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "hours": HOURS,
        "skipped_feeds": skipped,
        "categories": {c: [{**s, "time": s["time"].isoformat() if s["time"] else None}
                           for s in items] for c, items in grouped.items() if items},
    }


def render_html(digest):
    cards = []
    for category, items in digest["categories"].items():
        rows = "".join(
            f'<li><a href="{html.escape(s["link"])}" target="_blank" rel="noopener">{html.escape(s["title"])}</a>'
            f'<span class="meta">{html.escape(s["source"])}</span>'
            + (f'<p>{html.escape(s["summary"])}</p>' if s["summary"] else "") + "</li>"
            for s in items)
        cards.append(f'<section><h2>{category} <small>{len(items)}</small></h2><ul>{rows}</ul></section>')
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Morning News Digest</title>
<style>
 body{{margin:0;font:16px/1.5 system-ui,sans-serif;background:#f4f6f8;color:#0f1222}}
 header{{background:#0a5c64;color:#fff;padding:22px 24px}} header h1{{margin:0;font-size:26px}}
 header p{{margin:4px 0 0;opacity:.85}} main{{max-width:1100px;margin:0 auto;padding:20px;
 display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(min(320px,100%),1fr))}}
 a,li p{{overflow-wrap:anywhere}}
 section{{background:#fff;border-radius:12px;padding:16px 18px;box-shadow:0 1px 3px #0002}}
 h2{{margin:0 0 8px;font-size:19px;color:#0a5c64}} h2 small{{color:#64748b;font-weight:500}}
 ul{{list-style:none;margin:0;padding:0}} li{{padding:9px 0;border-top:1px solid #e2e8f0}}
 li:first-child{{border-top:0}} a{{color:#0f1222;font-weight:600;text-decoration:none}}
 a:hover{{color:#0a5c64;text-decoration:underline}} .meta{{display:block;font-size:13px;color:#64748b}}
 li p{{margin:3px 0 0;font-size:14px;color:#334155}}
</style></head><body>
<header><h1>Morning News Digest</h1><p>{digest["generated"]} · last {digest["hours"]} hours</p></header>
<main>{''.join(cards)}</main></body></html>"""


def main():
    digest = collect()
    if not digest["categories"]:
        print("No fresh headlines could be downloaded. Check your internet connection.")
        return 1

    (HERE / "digest.json").write_text(json.dumps(digest, indent=1, ensure_ascii=False), encoding="utf-8")
    page = HERE / "digest.html"
    page.write_text(render_html(digest), encoding="utf-8")

    print(f"\nMorning News Digest · {digest['generated']} · last {digest['hours']} h")
    print("=" * 60)
    for category, items in digest["categories"].items():
        print(f"\n{category.upper()} ({len(items)})")
        for story in items[:3]:
            print(f"  - {story['title']}  [{story['source']}]")
    if digest["skipped_feeds"]:
        print(f"\n(skipped: {', '.join(digest['skipped_feeds'])})")
    print(f"\nSaved: {page.name} and digest.json")
    if "--open" in sys.argv:
        webbrowser.open(page.as_uri())
    return 0


if __name__ == "__main__":
    sys.exit(main())
