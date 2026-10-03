"""Project 1 — Expert: compute indicators, then let Claude explain them.

Pipeline:
  1. Download recent prices for a ticker with ``yfinance``.
  2. Compute simple indicators (last price, day change, 20/50-day moving averages,
     and any golden/death cross).
  3. Send those numbers to Anthropic Claude via the official ``anthropic`` SDK and
     ask for a 2-3 sentence, plain-English commentary.
  4. Print the commentary (and optionally POST it to a webhook).

The API key is read from the ``ANTHROPIC_API_KEY`` environment variable via
python-dotenv. It is NEVER hardcoded. See ``.env.example`` at the repo root.

Run it:
    python ai_commentary_agent.py            # defaults to AAPL
    python ai_commentary_agent.py MSFT

Stretch (low-confidence flag): the prompt asks the model to say so explicitly when
the signal is weak or the data is thin, instead of always sounding certain.
"""

import os
import sys

import yfinance as yf
from dotenv import load_dotenv

# Load variables from a local .env file if present (safe no-op if it is missing).
load_dotenv()

MODEL = "claude-3-5-sonnet-20241022"
HISTORY_PERIOD = "6mo"


def gather_indicators(ticker: str) -> dict:
    """Return a small dict of indicators for the given ticker.

    Raises ValueError when there is no usable price data.
    """
    history = yf.Ticker(ticker).history(period=HISTORY_PERIOD)
    if history.empty:
        raise ValueError(f"No price data returned for '{ticker}'.")

    close = history["Close"]
    last_price = float(close.iloc[-1])
    prev_close = float(close.iloc[-2]) if len(close) > 1 else last_price
    change_pct = ((last_price - prev_close) / prev_close * 100) if prev_close else 0.0

    ma20 = close.rolling(window=20).mean()
    ma50 = close.rolling(window=50).mean()
    ma20_last = float(ma20.iloc[-1]) if ma20.notna().any() else None
    ma50_last = float(ma50.iloc[-1]) if ma50.notna().any() else None

    cross = "none"
    both = history.assign(ma20=ma20, ma50=ma50).dropna(subset=["ma20", "ma50"])
    if len(both) >= 2:
        prev, last = both.iloc[-2], both.iloc[-1]
        if prev["ma20"] <= prev["ma50"] and last["ma20"] > last["ma50"]:
            cross = "golden"
        elif prev["ma20"] >= prev["ma50"] and last["ma20"] < last["ma50"]:
            cross = "death"

    return {
        "ticker": ticker.upper(),
        "last_price": round(last_price, 2),
        "day_change_pct": round(change_pct, 2),
        "ma20": round(ma20_last, 2) if ma20_last is not None else None,
        "ma50": round(ma50_last, 2) if ma50_last is not None else None,
        "cross": cross,
        "days_of_data": int(len(close)),
    }


def build_prompt(indicators: dict) -> str:
    """Turn the indicator dict into a plain-text instruction for the model."""
    return (
        "You are a careful financial assistant for students. Given these computed "
        "indicators, write a 2-3 sentence plain-English commentary a beginner can "
        "understand. Do not give buy/sell advice. If the signal is weak, mixed, or "
        "the data is thin, explicitly flag that your confidence is low.\n\n"
        f"Indicators: {indicators}"
    )


def get_commentary(indicators: dict) -> str:
    """Call Claude and return its commentary text.

    Raises RuntimeError with a clear message if the key is missing or the SDK call
    fails, so main() can report it without a traceback.
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
            max_tokens=200,
            messages=[{"role": "user", "content": build_prompt(indicators)}],
        )
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Anthropic API call failed: {exc}") from exc

    # The SDK returns a list of content blocks; concatenate the text ones.
    return "".join(block.text for block in message.content if block.type == "text").strip()


def maybe_post_to_webhook(text: str) -> None:
    """POST the commentary to WEBHOOK_URL if one is configured; otherwise skip."""
    url = os.environ.get("WEBHOOK_URL")
    if not url:
        return
    try:
        import requests

        requests.post(url, json={"text": text}, timeout=10)
        print("Posted commentary to webhook.")
    except Exception as exc:  # noqa: BLE001
        print(f"Could not post to webhook: {exc}")


def main() -> int:
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"

    try:
        indicators = gather_indicators(ticker)
    except ValueError as exc:
        print(f"Could not gather indicators: {exc}")
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"Network or API error while fetching '{ticker}': {exc}")
        return 1

    print(f"Indicators for {indicators['ticker']}:")
    for key, value in indicators.items():
        print(f"  {key}: {value}")

    try:
        commentary = get_commentary(indicators)
    except RuntimeError as exc:
        print(f"\nCommentary unavailable: {exc}")
        return 1

    print("\nAI commentary:")
    print(f"  {commentary}")
    maybe_post_to_webhook(commentary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
