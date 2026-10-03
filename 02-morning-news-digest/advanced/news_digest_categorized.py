"""Project 2 — Advanced: categorize headlines, rank by recency, render a digest.

Builds on the basic tier:
  * pulls several RSS feeds with ``feedparser``,
  * categorizes each headline by keyword (business / tech / sports / general),
  * ranks within each category by recency (newest first),
  * renders a Markdown digest (and an HTML version) and writes them to disk.

Run it:
    python news_digest_categorized.py
    python news_digest_categorized.py --html    # also open-friendly HTML output
"""

import sys
from datetime import datetime, timezone
from pathlib import Path
from time import mktime

import feedparser

FEEDS = {
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "NPR": "https://feeds.npr.org/1001/rss.xml",
    "Reuters": "https://feeds.reuters.com/reuters/topNews",
}

# Simple keyword buckets. First category whose keyword appears wins; else "general".
CATEGORY_KEYWORDS = {
    "business": ["market", "economy", "stocks", "trade", "inflation", "earnings", "bank"],
    "tech": ["ai", "tech", "software", "chip", "google", "apple", "microsoft", "cyber"],
    "sports": ["match", "cup", "league", "olympic", "tournament", "goal", "player"],
}


def categorize(title: str) -> str:
    """Return the first matching category for a headline, or 'general'."""
    lowered = title.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return category
    return "general"


def entry_timestamp(entry) -> datetime:
    """Best-effort published time for an entry; falls back to epoch 0 (very old)."""
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed:
        return datetime.fromtimestamp(mktime(parsed), tz=timezone.utc)
    return datetime.fromtimestamp(0, tz=timezone.utc)


def fetch_entries() -> list[dict]:
    """Return a list of headline dicts with source, title, link, category, time."""
    entries: list[dict] = []
    for source, url in FEEDS.items():
        try:
            parsed = feedparser.parse(url)
        except Exception as exc:  # noqa: BLE001
            print(f"  (could not read {source}: {exc})")
            continue

        for entry in parsed.entries:
            title = entry.get("title", "(no title)")
            entries.append(
                {
                    "source": source,
                    "title": title,
                    "link": entry.get("link", ""),
                    "category": categorize(title),
                    "time": entry_timestamp(entry),
                }
            )
    return entries


def group_and_rank(entries: list[dict]) -> dict[str, list[dict]]:
    """Group entries by category and sort each group newest-first."""
    grouped: dict[str, list[dict]] = {}
    for item in entries:
        grouped.setdefault(item["category"], []).append(item)
    for group in grouped.values():
        group.sort(key=lambda e: e["time"], reverse=True)
    return grouped


def render_markdown(grouped: dict[str, list[dict]]) -> str:
    """Render the grouped headlines as a Markdown digest string."""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"# Morning News Digest — {today}", ""]
    for category in ["business", "tech", "sports", "general"]:
        items = grouped.get(category)
        if not items:
            continue
        lines.append(f"## {category.capitalize()}")
        lines.append("")
        for item in items[:5]:
            link = f" ([link]({item['link']}))" if item["link"] else ""
            lines.append(f"- **[{item['source']}]** {item['title']}{link}")
        lines.append("")
    return "\n".join(lines)


def render_html(markdown_text: str) -> str:
    """Wrap a very small subset of the digest in a minimal HTML page.

    We avoid extra dependencies: this does light line-based conversion of the
    headings and bullet points produced by render_markdown().
    """
    body_lines = []
    for line in markdown_text.splitlines():
        if line.startswith("# "):
            body_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            body_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("- "):
            body_lines.append(f"<li>{line[2:]}</li>")
        elif line.strip():
            body_lines.append(f"<p>{line}</p>")
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>Morning News Digest</title></head><body>"
        + "\n".join(body_lines)
        + "</body></html>"
    )


def main() -> int:
    want_html = "--html" in sys.argv[1:]

    entries = fetch_entries()
    if not entries:
        print("No headlines could be fetched. Check your network connection.")
        return 1

    grouped = group_and_rank(entries)
    markdown_text = render_markdown(grouped)

    md_path = Path(__file__).with_name("digest.md")
    md_path.write_text(markdown_text, encoding="utf-8")
    print(markdown_text)
    print(f"\nMarkdown digest written to {md_path.name}")

    if want_html:
        html_path = Path(__file__).with_name("digest.html")
        html_path.write_text(render_html(markdown_text), encoding="utf-8")
        print(f"HTML digest written to {html_path.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
