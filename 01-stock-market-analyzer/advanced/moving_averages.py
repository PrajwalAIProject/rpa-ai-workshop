"""Project 1 — Advanced: moving averages, SQLite persistence, golden/death cross.

For a basket of tickers this script:
  * downloads daily closing prices with ``yfinance``,
  * persists the history to a local SQLite database (so repeated runs accumulate),
  * computes 20-day and 50-day simple moving averages with pandas,
  * flags a golden cross (20-day crossing above 50-day) or death cross (below),
  * plots price + both averages with matplotlib and saves a PNG per ticker.

Run it:
    python moving_averages.py
    python moving_averages.py AAPL MSFT    # override the default basket
"""

import sqlite3
import sys
from pathlib import Path

import pandas as pd

try:
    import matplotlib

    matplotlib.use("Agg")  # headless backend: no display needed, just saves PNGs
    import matplotlib.pyplot as plt
except Exception:  # noqa: BLE001
    plt = None  # plotting is optional; computation still works without it

import yfinance as yf

DEFAULT_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
DB_PATH = Path(__file__).with_name("stock_history.db")
HISTORY_PERIOD = "6mo"  # enough days to compute a 50-day average


def init_db(conn: sqlite3.Connection) -> None:
    """Create the price history table if it does not already exist."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS prices (
            ticker TEXT NOT NULL,
            date   TEXT NOT NULL,
            close  REAL NOT NULL,
            PRIMARY KEY (ticker, date)
        )
        """
    )
    conn.commit()


def save_history(conn: sqlite3.Connection, ticker: str, history: pd.DataFrame) -> None:
    """Upsert each (ticker, date, close) row so re-runs stay idempotent."""
    rows = [
        (ticker, idx.strftime("%Y-%m-%d"), float(close))
        for idx, close in history["Close"].items()
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO prices (ticker, date, close) VALUES (?, ?, ?)",
        rows,
    )
    conn.commit()


def load_history(conn: sqlite3.Connection, ticker: str) -> pd.DataFrame:
    """Read a ticker's stored closes back out, oldest first."""
    frame = pd.read_sql_query(
        "SELECT date, close FROM prices WHERE ticker = ? ORDER BY date",
        conn,
        params=(ticker,),
        parse_dates=["date"],
    )
    return frame.set_index("date")


def compute_averages(frame: pd.DataFrame) -> pd.DataFrame:
    """Add 20-day and 50-day simple moving averages to the frame."""
    frame = frame.copy()
    frame["ma20"] = frame["close"].rolling(window=20).mean()
    frame["ma50"] = frame["close"].rolling(window=50).mean()
    return frame


def detect_cross(frame: pd.DataFrame) -> str:
    """Return 'golden', 'death' or 'none' based on the latest MA crossover."""
    valid = frame.dropna(subset=["ma20", "ma50"])
    if len(valid) < 2:
        return "none"  # not enough history yet to decide

    prev, last = valid.iloc[-2], valid.iloc[-1]
    if prev["ma20"] <= prev["ma50"] and last["ma20"] > last["ma50"]:
        return "golden"
    if prev["ma20"] >= prev["ma50"] and last["ma20"] < last["ma50"]:
        return "death"
    return "none"


def plot_ticker(ticker: str, frame: pd.DataFrame) -> Path | None:
    """Save a price + MA chart as a PNG. Returns the path, or None if skipped."""
    if plt is None:
        print("  (matplotlib unavailable — skipping chart)")
        return None

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(frame.index, frame["close"], label="Close", linewidth=1.2)
    ax.plot(frame.index, frame["ma20"], label="20-day MA", linewidth=1.0)
    ax.plot(frame.index, frame["ma50"], label="50-day MA", linewidth=1.0)
    ax.set_title(f"{ticker} — price and moving averages")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    fig.autofmt_xdate()

    out_path = Path(__file__).with_name(f"{ticker}_moving_averages.png")
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    return out_path


def process_ticker(conn: sqlite3.Connection, ticker: str) -> None:
    """Download, persist, compute and plot one ticker, printing a short summary."""
    print(f"\n{ticker}")
    try:
        history = yf.Ticker(ticker).history(period=HISTORY_PERIOD)
    except Exception as exc:  # noqa: BLE001
        print(f"  Network or API error: {exc}")
        return

    if history.empty:
        print("  No price data returned — skipping.")
        return

    save_history(conn, ticker, history)
    stored = load_history(conn, ticker)
    frame = compute_averages(stored)

    latest_close = frame["close"].iloc[-1]
    cross = detect_cross(frame)
    cross_label = {
        "golden": "GOLDEN CROSS (bullish)",
        "death": "DEATH CROSS (bearish)",
        "none": "no fresh crossover",
    }[cross]

    print(f"  Latest close:   ${latest_close:.2f}")
    print(f"  Signal:         {cross_label}")

    chart = plot_ticker(ticker, frame)
    if chart is not None:
        print(f"  Chart saved:    {chart.name}")


def main() -> int:
    tickers = sys.argv[1:] or DEFAULT_TICKERS

    conn = sqlite3.connect(DB_PATH)
    try:
        init_db(conn)
        for ticker in tickers:
            process_ticker(conn, ticker.upper())
    finally:
        conn.close()

    print(f"\nHistory stored in {DB_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
