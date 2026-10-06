"""Project 1 - Basic: look up a company by name and show its stock information.

Reference solution. In the workshop you ask GitHub Copilot to write this file for you
(see README.md for the prompt); compare with this one if yours misbehaves.

Run:
    python company_info.py              # asks for a company name
    python company_info.py "Infosys"    # or pass it directly
"""

import sys
from datetime import datetime

import yfinance as yf


def find_stock(company_name):
    """Turn a company name into a stock symbol using Yahoo Finance search.

    Prefers the NSE listing (symbol ending in .NS) for Indian companies,
    otherwise the first company (equity) result.
    """
    results = yf.Search(company_name, max_results=10).quotes
    equities = [q for q in results if q.get("quoteType") == "EQUITY"]
    if not equities:
        return None
    for quote in equities:
        if quote.get("symbol", "").endswith(".NS"):
            return quote
    return equities[0]


def money(value, currency):
    if value is None:
        return "n/a"
    return f"{currency} {value:,.2f}"


def big_number(value, currency):
    """Show large values (market cap) in words: 4.09 lakh crore / 2.1 trillion."""
    if not value:
        return "n/a"
    if currency == "INR":
        return f"INR {value / 1e7:,.0f} crore"
    for size, word in ((1e12, "trillion"), (1e9, "billion"), (1e6, "million")):
        if value >= size:
            return f"{currency} {value / size:,.2f} {word}"
    return f"{currency} {value:,.0f}"


def main():
    name = " ".join(sys.argv[1:]).strip() or input("Enter a company name: ").strip()
    if not name:
        print("Please type a company name, for example: Infosys")
        return 1

    try:
        quote = find_stock(name)
    except Exception as error:  # network problems, Yahoo changes, etc.
        print(f"Could not search for '{name}': {error}")
        return 1
    if quote is None:
        print(f"No listed company found for '{name}'. Check the spelling and try again.")
        return 1

    symbol = quote["symbol"]
    try:
        info = yf.Ticker(symbol).fast_info
        currency = info["currency"]
        price = info["lastPrice"]
        previous = info["previousClose"]
        day_high, day_low = info["dayHigh"], info["dayLow"]
        year_high, year_low = info["yearHigh"], info["yearLow"]
        market_cap = info["marketCap"]
    except Exception as error:
        print(f"Found {symbol}, but could not download its price: {error}")
        return 1

    change = price - previous
    change_pct = change / previous * 100 if previous else 0
    arrow = "▲" if change >= 0 else "▼"

    print()
    print("=" * 52)
    print(f"  {quote.get('longname') or quote.get('shortname')}")
    print("=" * 52)
    print(f"  Symbol        : {symbol}  ({quote.get('exchDisp', quote.get('exchange'))})")
    print(f"  Sector        : {quote.get('sector', 'n/a')}")
    print(f"  Industry      : {quote.get('industry', 'n/a')}")
    print(f"  Current price : {money(price, currency)}")
    print(f"  Day change    : {arrow} {change:+,.2f} ({change_pct:+.2f}%)")
    print(f"  Day range     : {money(day_low, currency)} - {money(day_high, currency)}")
    print(f"  52-week range : {money(year_low, currency)} - {money(year_high, currency)}")
    print(f"  Market cap    : {big_number(market_cap, currency)}")
    print(f"  Checked at    : {datetime.now():%d %b %Y, %I:%M %p}")
    print("=" * 52)
    print("  Data: Yahoo Finance via yfinance (may be delayed ~15 min)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
