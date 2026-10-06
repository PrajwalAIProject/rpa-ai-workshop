# Project 1 — Basic: company name → stock information

## What you'll build

`company_info.py`: you type a company name, it finds the company's stock and prints its
current price, day change, day and 52-week range, and market cap. GitHub Copilot writes the code
from the prompt below.

## Before you start

- [Python 3.11+](../../00-prerequisites/python-setup.md) installed (`python --version` works).
- [VS Code with GitHub Copilot](../../00-prerequisites/git-and-editor.md), signed in to GitHub.
- A project folder (for example `C:\stock-project`) opened in VS Code with
  **File → Open Folder**.

No API key and no AWS account are needed for this level.

## Step 1 — Give Copilot this prompt

Open Copilot Chat (Copilot icon in the title bar, or **View → Chat**), set the mode to **Agent**, paste the whole prompt, and press Enter.

```text
Create a Python 3 script called company_info.py in this folder.

Goal: I type a company name (for example "Infosys", "Tata Motors" or "Apple") and the
script shows that company's current stock information.

Requirements:
1. Use only the yfinance library (install it with: pip install yfinance).
2. Read the company name from the command line, e.g. python company_info.py "Infosys".
   If no name is given, ask for it with input().
3. Find the stock with yfinance.Search(company_name, max_results=10). Keep only results
   whose quoteType is "EQUITY". If one of them has a symbol ending in ".NS" (NSE India),
   use that one; otherwise use the first one.
4. Get the prices from yfinance.Ticker(symbol).fast_info: lastPrice, previousClose,
   dayHigh, dayLow, yearHigh, yearLow, marketCap and currency. Take the company name,
   exchange, sector and industry from the search result.
5. Print a neat block with: company name, symbol and exchange, sector, industry, current
   price, day change as amount and percent with ▲ or ▼, day range, 52-week range,
   market cap (in crore when the currency is INR), and the time it was checked.
6. Handle errors politely: no company found, no internet, price not available. Print a
   clear one-line message instead of a traceback.
7. Keep it in one file, under 100 lines, with short comments a beginner can follow.

When the file is ready, install yfinance, run the script for "Infosys" and for "Apple",
and fix any errors you see.
```

## Step 2 — Approve and run

Copilot will ask to run `pip install yfinance` and then the script. Click **Continue/Allow** for each command
after reading it. You can also run it yourself in the VS Code terminal (**Terminal → New Terminal**):

```bash
python company_info.py "Infosys"
```

Try a few more: `"Tata Motors"`, `"Reliance Industries"`, `"Apple"`, and a nonsense
name like `"xyzqqq"` (it should print a friendly "not found" message, not crash).

## What correct output looks like

Real output from the reference solution (prices change every day):

```text
====================================================
  Infosys Limited
====================================================
  Symbol        : INFY.NS  (NSE)
  Sector        : Technology
  Industry      : Information Technology Services
  Current price : INR 1,010.00
  Day change    : ▼ -10.50 (-1.03%)
  Day range     : INR 1,007.65 - INR 1,020.50
  52-week range : INR 980.40 - INR 1,728.00
  Market cap    : INR 409,085 crore
  Checked at    : 06 Oct 2026, 10:50 AM
====================================================
```

**Check it yourself:** compare the price with a site such as NSE or Google Finance. It
should match within a few rupees (Yahoo data can be about 15 minutes behind).

## If Copilot's script is wrong — follow-up prompts

- *"It picked the US listing INFY. For Indian companies I want the NSE symbol ending in .NS."*
- *"When I type a wrong name it crashes with a traceback. Print a friendly message instead."*
- *"Show the market cap in crore for INR, like 409,085 crore."*

Still stuck? The reference solution is [`company_info.py`](company_info.py) in this folder.

## Common errors and fixes

| You see | Fix |
| ------- | --- |
| `ModuleNotFoundError: No module named 'yfinance'` | Run `pip install yfinance` in the VS Code terminal (inside your virtual environment if you use one). |
| `AttributeError: module 'yfinance' has no attribute 'Search'` | Old yfinance. Run `pip install --upgrade yfinance`. |
| `SSL: CERTIFICATE_VERIFY_FAILED` or a certificate error | College or office Wi-Fi is inspecting HTTPS. Try a phone hotspot, or `pip install truststore` and add `import truststore; truststore.inject_into_ssl()` as the first line of the script. |
| `401 Unauthorized` / "Invalid Crumb" warnings | Yahoo blocked one request. Run again; if it keeps happening, upgrade yfinance. |
| Wrong company found | Type the full name ("Tata Consultancy Services", not "TCS Ltd"), or ask Copilot to print the top 3 matches and let you choose. |
