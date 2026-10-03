# Project 1 — Basic: Stock Price

## What you'll build

A one-file Python script that fetches a single stock's current price and day change
and prints it to the terminal: ticker, last price, percent change, and a timestamp.

## Prerequisites

- Python 3.11+ and the shared dependencies installed (see
  [`00-prerequisites/README.md`](../../00-prerequisites/README.md)).
- No API key needed for this tier.

## Step-by-step setup

1. From the repo root, create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows (PowerShell): .venv\Scripts\Activate.ps1
   # macOS / Linux:        source .venv/bin/activate
   ```
2. Install the dependencies:
   ```bash
   pip install -r 00-prerequisites/requirements.txt
   ```
3. Run the script:
   ```bash
   cd 01-stock-market-analyzer/basic
   python stock_price.py          # defaults to AAPL
   python stock_price.py MSFT     # or any ticker
   ```
4. Expected output (prices will differ):
   ```
   AAPL as of 2025-01-15 09:30:00
     Last price:     $234.40
     Day change:     ▲ +1.20 (+0.51%)
   ```

## Common errors and fixes

- **`ModuleNotFoundError: No module named 'yfinance'`** — The virtual environment
  isn't active or dependencies aren't installed. Re-activate and re-run
  `pip install -r 00-prerequisites/requirements.txt`.
- **"Network or API error..."** — You're offline or the data source throttled you.
  The script catches this and exits cleanly; wait a moment and retry.
- **"Could not fetch a quote: No price data returned"** — The ticker symbol is wrong
  or delisted. Double-check the symbol (e.g. `AAPL`, not `APPLE`).
