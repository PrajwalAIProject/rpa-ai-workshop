# Project 1 — Advanced: the company's full trend, with web scraping

## What you'll build

`stock_trend.py`: you type a company name and get its **full trend**:

- **Price trend** from one year of daily prices: change over 1 week, 1 month, 6 months
  and 1 year; 50-day and 200-day averages; 1-year high and low; an
  *uptrend / downtrend / sideways* verdict.
- **Fundamentals, web-scraped** from the company's public page on
  [screener.in](https://www.screener.in): what the company does, key ratios (P/E, ROE,
  market cap…), 10/5/3/1-year growth in sales, profit and share price, the last 4
  quarters of sales and profit, and the site's pros and cons.

It also saves everything to a JSON file. The expert level reuses it.

**Web scraping** means downloading a web page with code (`requests`) and picking the
values out of its HTML (`BeautifulSoup`), the way you'd read them off the page yourself.

## Before you start

- The [basic level](../basic/README.md) done, in the same VS Code folder.
- No API key or AWS account needed.

## Step 1 — Give Copilot this prompt (Agent mode)

```text
Create a Python 3 script called stock_trend.py in this folder. It builds on
company_info.py: use the same company-name search (import or copy find_stock), but show
the company's full trend.

Install: pip install yfinance requests beautifulsoup4

Part A - price trend (yfinance):
- Download 1 year of daily prices with yfinance.Ticker(symbol).history(period="1y").
- Calculate the % change over 1 week (5 trading days), 1 month (21), 6 months (126) and
  1 year; the 50-day and 200-day average closing price; the 1-year high and low.
- Verdict: "Uptrend" if price > 50-day average > 200-day average, "Downtrend" if
  price < 50-day average < 200-day average, otherwise "Sideways / mixed".

Part B - web scraping (screener.in, for companies listed in India):
- If the symbol ends with .NS or .BO, take the part before the dot (INFY.NS -> INFY) and
  download https://www.screener.in/company/INFY/ with requests. Send a normal browser
  User-Agent header, use a 20-second timeout, and make only ONE request per run.
- Parse the page with BeautifulSoup and extract:
  * the About paragraph (".company-profile .about p")
  * the key ratios ("#top-ratios li", each has ".name" and ".nowrap"): Market Cap,
    Current Price, High / Low, Stock P/E, ROE and the rest
  * the growth tables ("table.ranges-table"): Compounded Sales Growth, Compounded Profit
    Growth, Stock Price CAGR, Return on Equity, each with its 10/5/3/1-year values
  * the last 4 quarters of Sales and Net Profit ("section#quarters table")
  * the pros and cons lists (".pros li" and ".cons li")
- If the company is not listed in India, or scraping fails, still show Part A and print
  one line explaining why the fundamentals are missing.

Output:
- Print everything in clear sections: PRICE TREND, ABOUT, KEY RATIOS, LONG-TERM GROWTH,
  LAST 4 QUARTERS, PROS / CONS, and the source URL.
- Save all the data to <SYMBOL>_trend.json, for example INFY_NS_trend.json.
- Put the data collection in a function collect(company_name) that returns a
  dictionary, so another script can reuse it.

Handle errors with clear messages and add short beginner-friendly comments. Then run it
for "Infosys" and for "Apple" and fix any errors.
```

## Step 2 — Approve and run

```bash
python stock_trend.py "Infosys"
python stock_trend.py "Apple"
```

## What correct output looks like

Real output from the reference solution for Infosys (shortened):

```text
============================================================
  Infosys Limited  (INFY.NS, NSE)
  Technology · Information Technology Services
============================================================
  PRICE TREND (last 1 year)
    Last close      : 1,010.05  on 2026-10-06
    1 week / 1 month: -0.53% / -7.12%
    6 months / 1 yr : -20.16% / -29.02%
    50 / 200-day avg: 1,098.81 / 1,229.92
    1-year range    : 980.4 - 1,691.4
    Verdict         : Downtrend (price below its 50-day average, which is below its 200-day average)

  KEY RATIOS (scraped)
    Market Cap      : ₹ 4,09,480 Cr.
    Stock P/E       : 13.2
    ROE             : 35.7 %
    ...
  LONG-TERM GROWTH (scraped)
    Compounded Sales Growth    10 Years: 11%  5 Years: 12%  3 Years: 6%  TTM: 11%
    Stock Price CAGR           10 Years: 7%  5 Years: -10%  3 Years: -12%  1 Year: -31%
  LAST 4 QUARTERS (Rs crore, scraped)
    Sales       Sep 2025: 36,907  Dec 2025: 37,996  Mar 2026: 38,641  Jun 2026: 39,957
  PROS
    + Company is almost debt free.
  CONS
    - Promoter holding is low: 13.8%

  Source: https://www.screener.in/company/INFY/
============================================================
  Saved: INFY_NS_trend.json
```

For **Apple** you get the price trend and the line
`FUNDAMENTALS: not available - Scraping covers Indian listed companies only (screener.in).`
That is correct behaviour.

**Check it yourself:** open `https://www.screener.in/company/INFY/` in a browser and
compare two or three numbers (P/E, ROE, the latest quarter's sales).

## Scrape responsibly

- screener.in's `robots.txt` allows `/company/` pages. Still, make **one request per
  run**, and never loop over hundreds of companies.
- Websites change their HTML. If a section comes back empty one day, the site's
  class names have probably changed. Ask Copilot: *"Open the page HTML and update the
  selectors for the key ratios."* That's a real-world automation skill.

## If Copilot's script is wrong — follow-up prompts

- *"The key ratios come out empty. Print the first 2000 characters of the HTML, find the right selectors, and fix it."*
- *"For Apple it crashes. If the company isn't Indian, skip the scraping and still show the price trend."*
- *"The 1-year change looks wrong. Use the first and last closing price of the 1-year history."*

Reference solution: [`stock_trend.py`](stock_trend.py).

## Common errors and fixes

| You see | Fix |
| ------- | --- |
| `ModuleNotFoundError: No module named 'bs4'` | `pip install beautifulsoup4` (the package name is different from the import name). |
| `HTTP 403` or `429` from screener.in | Too many requests or no browser User-Agent. Wait a minute, keep one request per run, and send the User-Agent header. |
| Every scraped section is empty | The page layout changed, or you got a login/consent page. Print the HTML and update the selectors with Copilot's help. |
| `SSL: CERTIFICATE_VERIFY_FAILED` | Campus or office HTTPS inspection. Try a phone hotspot, or `pip install truststore` and add `import truststore; truststore.inject_into_ssl()` at the top. |
| Growth values show just `%` | Normal for newly listed or demerged companies (e.g. Tata Motors after its 2025 split): there's no 3/5/10-year history yet. |
