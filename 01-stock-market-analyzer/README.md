# Project 1 — Stock Market Analyzer

Pull stock data, compute something useful from it, and eventually explain the result in
plain English. This project is deliberately outside the UiPath toolkit — it's where you
pick up **Python, external APIs, and cloud scheduling** that BCG701 doesn't cover.

Work up through the tiers. You don't have to reach expert — each tier is a complete,
runnable deliverable on its own.

## The three tiers

### Basic — [`basic/README.md`](basic/README.md)

A one-file script that fetches a single stock's current price and day change with
`yfinance` and prints the ticker, last price, percent change, and a timestamp. No API
key needed. **Done** when the script prints a clean quote for any ticker you pass it.

### Advanced — [`advanced/README.md`](advanced/README.md)

Track five tickers, persist their history to a local **SQLite** database, compute 20-day
and 50-day moving averages with **pandas**, flag a golden/death cross, and save a
price-plus-averages **matplotlib** chart per ticker. No API key needed. **Done** when you
have a database of prices, a per-ticker chart, and a terminal summary with any cross
signal.

### Expert — [`expert/README.md`](expert/README.md)

Feed the computed indicators to **Anthropic Claude** for a 2-3 sentence plain-English
commentary (prompted to flag low confidence instead of always sounding certain), then
schedule it with a **GitHub Actions** cron job. **Done** when the script prints Claude's
commentary locally and the scheduled Action runs it on its own.

## Prerequisites

- Python 3.11+ and the shared dependencies — see
  [`00-prerequisites/python-setup.md`](../00-prerequisites/python-setup.md) and
  [`00-prerequisites/requirements.txt`](../00-prerequisites/requirements.txt).
- Git and a code editor — see
  [`00-prerequisites/git-and-editor.md`](../00-prerequisites/git-and-editor.md) (the
  expert tier pushes to GitHub for scheduling).
- **Expert tier only:** an Anthropic API key in a local `.env` — see
  [`00-prerequisites/api-keys.md`](../00-prerequisites/api-keys.md).

New to any term here? Check the [`GLOSSARY.md`](../GLOSSARY.md). Stuck on setup or a run?
See [`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md).
