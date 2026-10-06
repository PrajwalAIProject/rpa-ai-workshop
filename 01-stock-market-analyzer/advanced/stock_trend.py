"""Project 1 - Advanced: the full trend of a company, using web scraping.

Reference solution. In the workshop you ask GitHub Copilot to write this file for you
(see README.md for the prompt); compare with this one if yours misbehaves.

What it does:
  1. Finds the company's stock symbol from its name (Yahoo Finance search).
  2. Price trend from one year of daily prices (yfinance): 1 week / 1 month /
     6 months / 1 year change, 50- and 200-day averages, and an
     "uptrend / downtrend / sideways" verdict.
  3. Web scraping: downloads the company's public page on screener.in with
     requests and reads it with BeautifulSoup - about the company, key ratios,
     long-term growth (sales, profit, share price), recent quarterly sales and
     profit, and the site's pros and cons. (Screener covers companies listed in
     India; for other companies only step 2 is shown.)
  4. Prints it all and saves it to <SYMBOL>_trend.json (the expert tier reuses it).

Run:
    python stock_trend.py "Infosys"
"""

import json
import sys
import time

import requests
import yfinance as yf
from bs4 import BeautifulSoup

HEADERS = {
    # Identify as a normal browser; some sites refuse the default python-requests agent.
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/126.0 Safari/537.36",
}


# ---------------------------------------------------------------- 1. find the stock
def find_stock(company_name):
    """Company name -> best matching stock (prefers the NSE listing in India)."""
    results = yf.Search(company_name, max_results=10).quotes
    equities = [q for q in results if q.get("quoteType") == "EQUITY"]
    if not equities:
        return None
    for quote in equities:
        if quote.get("symbol", "").endswith(".NS"):
            return quote
    return equities[0]


# ---------------------------------------------------------------- 2. price trend
def pct_change(prices, days_back):
    if len(prices) <= days_back:
        return None
    old, new = prices.iloc[-1 - days_back], prices.iloc[-1]
    return round((new - old) / old * 100, 2)


def price_trend(symbol):
    history = yf.Ticker(symbol).history(period="1y")
    if history.empty:
        raise ValueError(f"no price history for {symbol}")
    close = history["Close"]
    last = float(close.iloc[-1])
    avg50 = float(close.tail(50).mean())
    avg200 = float(close.tail(200).mean())

    if last > avg50 > avg200:
        verdict = "Uptrend (price above its 50-day average, which is above its 200-day average)"
    elif last < avg50 < avg200:
        verdict = "Downtrend (price below its 50-day average, which is below its 200-day average)"
    else:
        verdict = "Sideways / mixed (the averages do not agree)"

    return {
        "last_close": round(last, 2),
        "date": str(close.index[-1].date()),
        "change_1_week_pct": pct_change(close, 5),
        "change_1_month_pct": pct_change(close, 21),
        "change_6_months_pct": pct_change(close, 126),
        "change_1_year_pct": pct_change(close, len(close) - 1),
        "average_50_day": round(avg50, 2),
        "average_200_day": round(avg200, 2),
        "high_1_year": round(float(history["High"].max()), 2),
        "low_1_year": round(float(history["Low"].min()), 2),
        "verdict": verdict,
    }


# ---------------------------------------------------------------- 3. web scraping
def scrape_screener(symbol):
    """Scrape screener.in/company/<CODE>/ for an Indian listed company.

    robots.txt on screener.in allows /company/ pages. Be polite: one request
    per run, no loops over hundreds of companies.
    """
    code = symbol.split(".")[0]
    url = f"https://www.screener.in/company/{code}/"
    response = requests.get(url, headers=HEADERS, timeout=20)
    if response.status_code != 200:
        raise ValueError(f"{url} returned HTTP {response.status_code}")
    page = BeautifulSoup(response.text, "html.parser")

    def text(element):
        return element.get_text(" ", strip=True) if element else None

    about = text(page.select_one(".company-profile .about p") or page.select_one(".about p"))

    # Key ratios box: Market Cap, Current Price, High / Low, Stock P/E, ROE ...
    ratios = {}
    for item in page.select("#top-ratios li"):
        name, value = item.select_one(".name"), item.select_one(".nowrap")
        if name and value:
            ratios[text(name)] = text(value)

    # Growth tables: Compounded Sales Growth, Compounded Profit Growth, Stock Price CAGR, ROE
    growth = {}
    for table in page.select("table.ranges-table"):
        rows = table.select("tr")
        if not rows:
            continue
        title = text(rows[0])
        growth[title] = {text(r.select("td")[0]).rstrip(":"): text(r.select("td")[1])
                         for r in rows[1:] if len(r.select("td")) == 2}

    # Last four quarters of sales and net profit
    quarters = {}
    table = page.select_one("section#quarters table")
    if table:
        headers = [text(th) for th in table.select("thead th")][1:]
        for row in table.select("tbody tr"):
            cells = [text(td) for td in row.select("td")]
            label = (cells[0] or "").replace("+", "").strip()
            if label in ("Sales", "Revenue", "Net Profit"):
                quarters[label] = dict(zip(headers[-4:], cells[-4:]))

    return {
        "source": url,
        "about": about,
        "key_ratios": ratios,
        "long_term_growth": growth,
        "last_4_quarters": quarters,
        "pros": [text(li) for li in page.select(".pros li")],
        "cons": [text(li) for li in page.select(".cons li")],
    }


# ---------------------------------------------------------------- 4. put it together
def collect(company_name):
    """Everything about one company as a dictionary (used by the expert tier too)."""
    quote = find_stock(company_name)
    if quote is None:
        raise LookupError(f"No listed company found for '{company_name}'.")
    symbol = quote["symbol"]
    data = {
        "company": quote.get("longname") or quote.get("shortname"),
        "symbol": symbol,
        "exchange": quote.get("exchDisp", quote.get("exchange")),
        "sector": quote.get("sector"),
        "industry": quote.get("industry"),
        "price_trend": price_trend(symbol),
        "fundamentals": None,
        "fetched_at": time.strftime("%Y-%m-%d %H:%M"),
    }
    if symbol.endswith((".NS", ".BO")):
        try:
            data["fundamentals"] = scrape_screener(symbol)
        except Exception as error:
            data["fundamentals_error"] = str(error)
    else:
        data["fundamentals_error"] = "Scraping covers Indian listed companies only (screener.in)."
    return data


def show(data):
    t = data["price_trend"]
    def pct(v):
        return "n/a" if v is None else f"{v:+.2f}%"

    print("\n" + "=" * 60)
    print(f"  {data['company']}  ({data['symbol']}, {data['exchange']})")
    print(f"  {data['sector'] or ''} · {data['industry'] or ''}")
    print("=" * 60)
    print("  PRICE TREND (last 1 year)")
    print(f"    Last close      : {t['last_close']:,}  on {t['date']}")
    print(f"    1 week / 1 month: {pct(t['change_1_week_pct'])} / {pct(t['change_1_month_pct'])}")
    print(f"    6 months / 1 yr : {pct(t['change_6_months_pct'])} / {pct(t['change_1_year_pct'])}")
    print(f"    50 / 200-day avg: {t['average_50_day']:,} / {t['average_200_day']:,}")
    print(f"    1-year range    : {t['low_1_year']:,} - {t['high_1_year']:,}")
    print(f"    Verdict         : {t['verdict']}")

    f = data.get("fundamentals")
    if not f:
        print(f"\n  FUNDAMENTALS: not available - {data.get('fundamentals_error')}")
    else:
        if f["about"]:
            print("\n  ABOUT")
            print(f"    {f['about'][:300]}")
        print("\n  KEY RATIOS (scraped)")
        for name, value in f["key_ratios"].items():
            print(f"    {name:<16}: {value}")
        print("\n  LONG-TERM GROWTH (scraped)")
        for title, periods in f["long_term_growth"].items():
            row = "  ".join(f"{p}: {v}" for p, v in periods.items())
            print(f"    {title:<26} {row}")
        if f["last_4_quarters"]:
            print("\n  LAST 4 QUARTERS (Rs crore, scraped)")
            for label, values in f["last_4_quarters"].items():
                print(f"    {label:<11} " + "  ".join(f"{q}: {v}" for q, v in values.items()))
        if f["pros"] or f["cons"]:
            print("\n  PROS")
            for p in f["pros"][:3]:
                print(f"    + {p}")
            print("  CONS")
            for c in f["cons"][:3]:
                print(f"    - {c}")
        print(f"\n  Source: {f['source']}")
    print("=" * 60)


def main():
    name = " ".join(sys.argv[1:]).strip() or input("Enter a company name: ").strip()
    if not name:
        print("Please type a company name, for example: Infosys")
        return 1
    try:
        data = collect(name)
    except Exception as error:
        print(f"Could not get the trend for '{name}': {error}")
        return 1
    show(data)
    out_file = f"{data['symbol'].replace('.', '_')}_trend.json"
    with open(out_file, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
    print(f"  Saved: {out_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
