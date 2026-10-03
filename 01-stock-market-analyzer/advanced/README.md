# Project 1 — Advanced: Moving Averages

## What you'll build

A script that tracks five tickers, persists their price history to a local SQLite
database, computes 20-day and 50-day moving averages with pandas, flags any
golden/death cross, and saves a price + averages chart as a PNG for each ticker.

## Prerequisites

- Everything from the [basic tier](../basic/README.md).
- The shared dependencies (includes `pandas` and `matplotlib`) installed from
  [`00-prerequisites/requirements.txt`](../../00-prerequisites/requirements.txt).
- No API key needed for this tier.

## Step-by-step setup

1. Activate your virtual environment and make sure dependencies are installed:
   ```bash
   pip install -r 00-prerequisites/requirements.txt
   ```
2. Run the script:
   ```bash
   cd 01-stock-market-analyzer/advanced
   python moving_averages.py                 # default basket of 5 tickers
   python moving_averages.py AAPL MSFT       # or your own list
   ```
3. What it produces:
   - `stock_history.db` — SQLite file with accumulated closing prices (git-ignored).
   - `<TICKER>_moving_averages.png` — one chart per ticker (git-ignored by default).
   - A terminal summary with the latest close and any cross signal.

   > _Screenshot placeholder: a sample `AAPL_moving_averages.png` chart._

   A committed example chart lives at [`sample_output.png`](sample_output.png) so you
   can see the expected shape before running anything yourself.

## Common errors and fixes

- **Charts not produced** — matplotlib may be missing; the script prints a note and
  still computes the numbers. Re-install dependencies to enable charts.
- **"Signal: no fresh crossover"** — Normal. A cross is only flagged when the 20-day
  line actually crosses the 50-day between the last two sessions.
- **SQLite "database is locked"** — Another process (or a stale run) holds the file.
  Close it, or delete `stock_history.db` to start fresh.
- **Network error** — The script catches it per-ticker and keeps going with the rest.
