"""Project 2 — Basic: print the top 5 headlines from a few RSS feeds.

Uses ``feedparser`` instead of scraping news homepages. Feeds are stable, structured,
and don't break when a site changes its layout — the same reliability lesson as
Project 1.

Run it:
    python news_digest.py
"""

import feedparser

# A small, well-known set of public RSS feeds. Swap in your own if you like.
FEEDS = {
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "NPR": "https://feeds.npr.org/1001/rss.xml",
    "Reuters": "https://feeds.reuters.com/reuters/topNews",
}

TOP_N = 5


def fetch_headlines() -> list[dict]:
    """Return a flat list of {source, title, link} dicts across all feeds.

    Any feed that fails to parse is skipped with a note rather than crashing the run.
    """
    headlines: list[dict] = []
    for source, url in FEEDS.items():
        try:
            parsed = feedparser.parse(url)
        except Exception as exc:  # noqa: BLE001
            print(f"  (could not read {source}: {exc})")
            continue

        if getattr(parsed, "bozo", False) and not parsed.entries:
            # bozo=1 with no entries usually means the feed didn't load at all.
            print(f"  (no entries from {source})")
            continue

        for entry in parsed.entries:
            headlines.append(
                {
                    "source": source,
                    "title": entry.get("title", "(no title)"),
                    "link": entry.get("link", ""),
                }
            )
    return headlines


def main() -> int:
    headlines = fetch_headlines()
    if not headlines:
        print("No headlines could be fetched. Check your network connection.")
        return 1

    print("Morning headlines (top 5)")
    print("=========================")
    for i, item in enumerate(headlines[:TOP_N], start=1):
        print(f"{i}. [{item['source']}] {item['title']}")
        if item["link"]:
            print(f"   {item['link']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
