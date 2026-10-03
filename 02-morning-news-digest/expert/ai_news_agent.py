"""Project 2 — Expert: let Claude pick the most significant headlines.

Pipeline:
  1. Pull headlines from a few RSS feeds with ``feedparser``.
  2. Send them to Anthropic Claude and ask it to pick the 3 most significant,
     each with a one-line "why it matters".
  3. Deliver the result by email (SMTP) if SMTP is configured, otherwise print it.

Everything is environment-driven. The API key is read from ANTHROPIC_API_KEY via
python-dotenv and is NEVER hardcoded. SMTP settings are optional; leave SMTP_HOST
blank to just print. See ``.env.example`` at the repo root.

Run it:
    python ai_news_agent.py
"""

import os
import smtplib
import sys
from email.message import EmailMessage

import feedparser
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-3-5-sonnet-20241022"

FEEDS = {
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "NPR": "https://feeds.npr.org/1001/rss.xml",
    "Reuters": "https://feeds.reuters.com/reuters/topNews",
}

MAX_HEADLINES = 25  # cap how many we send to the model


def fetch_headlines() -> list[str]:
    """Return a list of 'source: title' strings across all feeds."""
    headlines: list[str] = []
    for source, url in FEEDS.items():
        try:
            parsed = feedparser.parse(url)
        except Exception as exc:  # noqa: BLE001
            print(f"  (could not read {source}: {exc})")
            continue
        for entry in parsed.entries:
            headlines.append(f"{source}: {entry.get('title', '(no title)')}")
    return headlines[:MAX_HEADLINES]


def build_prompt(headlines: list[str]) -> str:
    """Instruction asking the model to pick the top 3 with 'why it matters'."""
    joined = "\n".join(f"- {h}" for h in headlines)
    return (
        "Here are this morning's news headlines. Pick the 3 most significant and, "
        "for each, write a single short line explaining why it matters. Format as a "
        "numbered list: the headline, then 'Why it matters: ...'. Be concise and "
        "neutral.\n\n"
        f"{joined}"
    )


def summarize_with_claude(headlines: list[str]) -> str:
    """Call Claude and return the digest text.

    Raises RuntimeError with a clear message on misconfiguration or API failure.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key."
        )

    try:
        import anthropic
    except ImportError as exc:  # noqa: BLE001
        raise RuntimeError(
            "The 'anthropic' package is not installed. Run: "
            "pip install -r 00-prerequisites/requirements.txt"
        ) from exc

    client = anthropic.Anthropic(api_key=api_key)
    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=400,
            messages=[{"role": "user", "content": build_prompt(headlines)}],
        )
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Anthropic API call failed: {exc}") from exc

    return "".join(block.text for block in message.content if block.type == "text").strip()


def deliver(digest: str) -> None:
    """Email the digest if SMTP is configured; otherwise print it to the terminal."""
    host = os.environ.get("SMTP_HOST")
    if not host:
        print("\nTop stories this morning:\n")
        print(digest)
        print("\n(SMTP_HOST not set — printed instead of emailed.)")
        return

    msg = EmailMessage()
    msg["Subject"] = "Morning News Digest"
    msg["From"] = os.environ.get("EMAIL_FROM", "")
    msg["To"] = os.environ.get("EMAIL_TO", "")
    msg.set_content(digest)

    port = int(os.environ.get("SMTP_PORT", "587"))
    username = os.environ.get("SMTP_USERNAME", "")
    password = os.environ.get("SMTP_PASSWORD", "")

    try:
        with smtplib.SMTP(host, port, timeout=20) as server:
            server.starttls()
            if username:
                server.login(username, password)
            server.send_message(msg)
        print("Digest emailed successfully.")
    except Exception as exc:  # noqa: BLE001
        print(f"Could not send email: {exc}")
        print("\nDigest content:\n")
        print(digest)


def main() -> int:
    headlines = fetch_headlines()
    if not headlines:
        print("No headlines could be fetched. Check your network connection.")
        return 1

    try:
        digest = summarize_with_claude(headlines)
    except RuntimeError as exc:
        print(f"Digest unavailable: {exc}")
        return 1

    deliver(digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
