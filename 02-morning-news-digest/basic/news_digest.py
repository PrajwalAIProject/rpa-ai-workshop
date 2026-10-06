"""Project 2 - Basic: the latest headlines from Indian and world news feeds.

Reference solution. In the workshop you ask GitHub Copilot to write this file for you
(see README.md for the prompt); compare with this one if yours misbehaves.

What it does:
  1. Downloads a few public RSS feeds (each news site publishes one: a list of its
     latest stories in a fixed XML format, so a site redesign doesn't break us).
  2. Optionally keeps only headlines about a topic you type, e.g. "cricket".
  3. Removes duplicates, sorts newest first, and prints the top 10.

Run:
    python news_digest.py              # asks for a topic (press Enter for all news)
    python news_digest.py cricket      # or pass it directly
"""

import sys
from datetime import datetime, timezone
from time import mktime

import feedparser
import requests

FEEDS = {
    "The Hindu": "https://www.thehindu.com/feeder/default.rss",
    "Times of India": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "NDTV": "https://feeds.feedburner.com/ndtvnews-top-stories",
    "BBC World": "https://feeds.bbci.co.uk/news/world/rss.xml",
}
TOP_N = 10


def fetch_feed(source, url):
    """Download one feed with a timeout (feedparser alone can hang) and parse it."""
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (news-digest workshop)"}, timeout=10)
    response.raise_for_status()
    stories = []
    for entry in feedparser.parse(response.content).entries:
        published = entry.get("published_parsed") or entry.get("updated_parsed")
        stories.append({
            "source": source,
            "title": entry.get("title", "").strip(),
            "link": entry.get("link", ""),
            "time": datetime.fromtimestamp(mktime(published), tz=timezone.utc) if published else None,
        })
    return stories


def time_ago(moment):
    if moment is None:
        return "time n/a"
    minutes = int((datetime.now(timezone.utc) - moment).total_seconds() // 60)
    if minutes < 60:
        return f"{max(minutes, 0)} min ago"
    if minutes < 24 * 60:
        return f"{minutes // 60} h ago"
    return f"{minutes // (24 * 60)} days ago"


def main():
    topic = " ".join(sys.argv[1:]).strip()
    if not sys.argv[1:]:
        topic = input("Topic to look for (press Enter for all news): ").strip()

    stories = []
    for source, url in FEEDS.items():
        try:
            stories += fetch_feed(source, url)
        except Exception as error:  # one broken feed must not stop the others
            print(f"  (skipped {source}: {error.__class__.__name__})")
    if not stories:
        print("No headlines could be downloaded. Check your internet connection.")
        return 1

    if topic:
        stories = [s for s in stories if topic.lower() in s["title"].lower()]
        if not stories:
            print(f"No headlines mention '{topic}' right now. Try another word.")
            return 0

    # Remove duplicates (same headline from two feeds), then newest first.
    unique = {s["title"].lower(): s for s in stories if s["title"]}
    stories = sorted(unique.values(),
                     key=lambda s: s["time"] or datetime.min.replace(tzinfo=timezone.utc),
                     reverse=True)

    heading = f"Top {min(TOP_N, len(stories))} headlines" + (f" about '{topic}'" if topic else "")
    print(f"\n{heading} · {datetime.now():%d %b %Y, %I:%M %p}")
    print("=" * 60)
    for number, story in enumerate(stories[:TOP_N], start=1):
        print(f"{number:2}. {story['title']}")
        print(f"    {story['source']} · {time_ago(story['time'])} · {story['link']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
