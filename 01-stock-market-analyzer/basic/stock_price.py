"""Project 1 — Basic: fetch and print one stock's current price and day change.

Uses the ``yfinance`` library instead of scraping raw HTML. Scraping breaks the
moment a target site changes its markup — a bad failure mode in front of a class.
``yfinance`` teaches the same skill (pull external data, handle a failed request)
without that fragility.

Run it:
    python stock_price.py            # defaults to AAPL
    python stock_price.py MSFT       # or pass any ticker
"""

import sys
from datetime import datetime

import yfinance as yf


def fetch_quote(ticker: str) -> dict:
    """Return last price, previous close, percent change and a timestamp.

    Raises ``ValueError`` if the ticker is unknown or no price data comes back,
    so the caller can print a clean message instead of a stack trace.
    """
    stock = yf.Ticker(ticker)

    # ``fast_info`` is the quickest way to a current price. Different yfinance
    # versions expose slightly different keys, so we read defensively.
    info = stock.fast_info
    last_price = info.get("last_price") or info.get("lastPrice")
    prev_close = info.get("previous_close") or info.get("previousClose")

    if last_price is None or prev_close is None:
        # Fall back to the most recent daily close from history.
        history = stock.history(period="2d")
        if history.empty:
            raise ValueError(f"No price data returned for '{ticker}'.")
        last_price = float(history["Close"].iloc[-1])
        prev_close = float(history["Close"].iloc[0])

    last_price = float(last_price)
    prev_close = float(prev_close)
    change = last_price - prev_close
    percent_change = (change / prev_close * 100) if prev_close else 0.0

    return {
        "ticker": ticker.upper(),
        "last_price": last_price,
        "change": change,
        "percent_change": percent_change,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def main() -> int:
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"

    try:
        quote = fetch_quote(ticker)
    except ValueError as exc:
        # Expected, user-facing problem (bad ticker / empty data).
        print(f"Could not fetch a quote: {exc}")
        return 1
    except Exception as exc:  # noqa: BLE001 - keep the classroom demo robust
        # Network down, API throttled, etc. Fail with a clear message, no traceback.
        print(f"Network or API error while fetching '{ticker}': {exc}")
        return 1

    arrow = "▲" if quote["change"] >= 0 else "▼"
    print(f"{quote['ticker']} as of {quote['timestamp']}")
    print(f"  Last price:     ${quote['last_price']:.2f}")
    print(f"  Day change:     {arrow} {quote['change']:+.2f} ({quote['percent_change']:+.2f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
