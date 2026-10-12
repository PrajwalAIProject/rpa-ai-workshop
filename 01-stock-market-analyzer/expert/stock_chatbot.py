"""Project 1 - Expert: a company chatbot, using a FREE AI API.

Reference solution. In the workshop you ask GitHub Copilot to write this file for you
(see README.md for the prompt); compare with this one if yours misbehaves.

It combines everything you built:
  basic     today's price snapshot (yfinance fast_info)
  advanced  the 1-year price trend + fundamentals scraped from screener.in (collect())
  expert    the latest company news (Google News RSS) + a free AI model you can chat with

Then it opens a chat. Ask anything about the company in plain English:
  "What does this company do?"   "How has the share done this year?"
  "Is profit growing?"           "What is in the news this week?"
The AI answers ONLY from the data and headlines it was given, and says "not available"
when the answer is not there. Chat commands:
  /news            show the headlines it is using
  /report          write a 5-section report and save it as <SYMBOL>_report.md
  /company <name>  switch to another company
  /quit            leave

Setup (see 00-prerequisites/free-ai-api-key.md) - a .env file next to this script:
    LLM_PROVIDER=gemini
    GEMINI_API_KEY=<your key>
    # or:  LLM_PROVIDER=groq  and  GROQ_API_KEY=<your key>

Run:
    python stock_chatbot.py "Infosys"
    python stock_chatbot.py "Infosys" --ask "Is profit growing?"   # one question, then exit
    python stock_chatbot.py "Infosys" --dry-run                    # show what the AI gets
"""

import json
import os
import sys
from pathlib import Path
from urllib.parse import quote_plus

import feedparser
import requests
import yfinance as yf
from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, OpenAI

HERE = Path(__file__).resolve().parent
# Reuse the advanced tier. In your own project folder all the files sit together;
# in this repo the advanced tier lives next door.
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "advanced"))
from stock_trend import HEADERS, collect  # noqa: E402

load_dotenv(HERE / ".env")
load_dotenv(HERE.parent.parent / ".env")  # repo-root .env, if you keep it there

# provider -> (API address, name of the key in .env, default model)
PROVIDERS = {
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai/",
               "GEMINI_API_KEY", "gemini-flash-latest"),
    "groq": ("https://api.groq.com/openai/v1",
             "GROQ_API_KEY", "openai/gpt-oss-20b"),
}
MAX_TURNS = 8  # keep the last 8 questions and answers, so the chat stays inside free limits

RULES = """You are a friendly stock-market assistant for engineering students in India.
You answer questions about ONE company, using ONLY the DATA and NEWS below.
Rules:
- Use only numbers and facts that appear in DATA or NEWS. If the answer is not there,
  say "That is not in my data" and suggest what to check instead.
- When you use a headline, name its source and date, for example (Moneycontrol, 10 Oct).
- Explain any finance word the first time you use it (P/E, ROE, CAGR...).
- Never tell the user to buy, sell or hold. If asked, explain what to look at instead.
- Answer in simple English, in at most 120 words, unless the user asks for more detail.
"""

REPORT_REQUEST = """Write a short report with exactly these 5 sections:
1. Company in one line  2. Recent price trend  3. Business health (growth, P/E, ROE,
pros and cons)  4. In the news (2-3 headlines and why they matter)  5. One-line summary.
Under 350 words. End with: "This is a learning exercise, not financial advice." """


# ---------------------------------------------------------------- data
def snapshot(symbol):
    """Basic level: today's price, day change, 52-week range and market cap."""
    info = yf.Ticker(symbol).fast_info
    last, prev = info.last_price, info.previous_close
    return {
        "currency": info.currency,
        "price": round(last, 2) if last else None,
        "day_change_pct": round((last - prev) / prev * 100, 2) if last and prev else None,
        "week52_high": round(info.year_high, 2) if info.year_high else None,
        "week52_low": round(info.year_low, 2) if info.year_low else None,
        "market_cap": int(info.market_cap) if info.market_cap else None,
    }


def company_news(company, limit=8):
    """Latest headlines about the company from Google News RSS (free, no key).

    Download with requests (with a timeout), then parse with feedparser:
    feedparser.parse(url) on its own can hang forever on a slow network.
    """
    url = ("https://news.google.com/rss/search?q=" + quote_plus(f'"{company}" share OR stock')
           + "&hl=en-IN&gl=IN&ceid=IN:en")
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    items = []
    for entry in feedparser.parse(response.content).entries[:limit]:
        source = entry.get("source", {}).get("title", "")
        title = entry.get("title", "")
        if source and title.endswith(" - " + source):
            title = title[: -len(source) - 3]  # Google adds " - Source" to every title
        items.append({"title": title, "source": source,
                      "date": entry.get("published", "")[:16], "link": entry.get("link", "")})
    return items


def gather(company):
    """Everything about one company: advanced data + basic snapshot + news."""
    data = collect(company)  # raises LookupError if no company is found
    try:
        data["today"] = snapshot(data["symbol"])
    except Exception as error:
        data["today_error"] = str(error)
    try:
        news = company_news(data["company"] or company)
    except Exception as error:
        news, data["news_error"] = [], f"News could not be downloaded: {error}"
    return data, news


def system_prompt(data, news):
    return (RULES + "\nDATA (JSON):\n" + json.dumps(data, ensure_ascii=False)
            + "\n\nNEWS (latest headlines, JSON):\n" + json.dumps(news, ensure_ascii=False))


# ---------------------------------------------------------------- AI
def make_client(provider):
    base_url, key_name, _ = PROVIDERS[provider]
    api_key = os.getenv(key_name)
    if not api_key:
        raise SystemExit(f"{key_name} is not set. Put {key_name}=<your key> in a .env file "
                         "next to this script (see 00-prerequisites/free-ai-api-key.md).")
    return OpenAI(api_key=api_key, base_url=base_url)


def pick_fallback_model(client, provider):
    """If the default model name has changed, choose a current one from the provider's list."""
    names = [m.id.removeprefix("models/") for m in client.models.list()]
    wanted = "flash" if provider == "gemini" else "gpt-oss"
    candidates = [n for n in names if wanted in n and "image" not in n and "tts" not in n]
    return candidates[0] if candidates else None


def chat_once(client, provider, model, messages):
    """Send the conversation, return (answer, model actually used)."""
    try:
        reply = client.chat.completions.create(model=model, messages=messages, temperature=0.3)
    except APIStatusError as error:
        if error.status_code != 404:  # 404 = model name not found -> try a current one
            raise
        replacement = pick_fallback_model(client, provider)
        if not replacement:
            raise
        print(f"(Model '{model}' not found; using '{replacement}' instead.)")
        model = replacement
        reply = client.chat.completions.create(model=model, messages=messages, temperature=0.3)
    return reply.choices[0].message.content.strip(), model


def explain(error):
    """A one-line hint for the common API errors."""
    if isinstance(error, APIConnectionError):
        return "Could not reach the AI service. Check your internet connection."
    code = getattr(error, "status_code", None)
    if code in (400, 401) and "key" in str(error).lower() or code == 401:
        return "The API key is wrong. Copy it again into .env (no quotes, no spaces)."
    hints = {403: "This key can't use this model. Create a new key or switch LLM_PROVIDER.",
             404: "Model not found. Remove LLM_MODEL from .env.",
             413: "Too much data for this model's free limit. Use Gemini.",
             429: "Free-tier limit reached. Wait a minute, or switch LLM_PROVIDER."}
    return f"AI error {code}: {hints.get(code, str(error)[:200])}"


# ---------------------------------------------------------------- chat
def show_header(data, news):
    t, today = data.get("price_trend", {}), data.get("today", {})
    print("\n" + "=" * 64)
    print(f"  {data['company']} ({data['symbol']}) · chat ready")
    if today.get("price"):
        print(f"  Price {today['currency']} {today['price']:,}  ({today['day_change_pct']:+}% today)"
              f" · 1 year {t.get('change_1_year_pct')}%")
    print(f"  Data: price trend, {'fundamentals' if data.get('fundamentals') else 'no fundamentals'},"
          f" {len(news)} news headlines")
    print("  Ask anything. Commands: /news  /report  /company <name>  /quit")
    print("=" * 64)


def save_report(data, text, provider, model):
    out = HERE / f"{data['symbol'].replace('.', '_')}_report.md"
    out.write_text(f"# Company report: {data['company']} ({data['symbol']})\n\n"
                   f"_Written by {provider} / {model} from the collected data and news_\n\n{text}\n",
                   encoding="utf-8")
    return out.name


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    question = None
    if "--ask" in args:
        i = args.index("--ask")
        question = " ".join(args[i + 1:i + 2])
        del args[i:i + 2]
    company = " ".join(a for a in args if a != "--dry-run").strip() or input("Company name: ").strip()
    if not company:
        print("Please type a company name, for example: Infosys")
        return 1

    provider = os.getenv("LLM_PROVIDER", "gemini").strip().lower()
    if provider not in PROVIDERS:
        print(f"LLM_PROVIDER must be one of {', '.join(PROVIDERS)} (got '{provider}').")
        return 1
    model = os.getenv("LLM_MODEL") or PROVIDERS[provider][2]

    print(f"Collecting data and news for '{company}'...")
    try:
        data, news = gather(company)
    except Exception as error:
        print(f"Could not collect data: {error}")
        return 1
    system = system_prompt(data, news)

    if dry_run:
        print(system)
        print(f"\n(dry run: would chat with {provider} model {model}; "
              f"context is {len(system):,} characters, {len(news)} headlines)")
        return 0

    client = make_client(provider)
    history = []

    def ask(text):
        nonlocal model
        messages = [{"role": "system", "content": system}] + history[-2 * MAX_TURNS:] + \
                   [{"role": "user", "content": text}]
        answer, model = chat_once(client, provider, model, messages)
        history.extend([{"role": "user", "content": text}, {"role": "assistant", "content": answer}])
        return answer

    if question:  # one question, then exit (handy for testing)
        try:
            print("\n" + ask(question))
        except (APIStatusError, APIConnectionError) as error:
            print(explain(error))
            return 1
        return 0

    show_header(data, news)
    while True:
        try:
            text = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not text:
            continue
        if text in ("/quit", "/exit", "quit", "exit"):
            break
        if text == "/news":
            for n in news or [{"title": data.get("news_error", "No headlines found."), "source": "", "date": ""}]:
                print(f"  - {n['title']}  ({n['source']}, {n['date']})")
            continue
        if text.startswith("/company"):
            name = text[len("/company"):].strip() or input("Company name: ").strip()
            print(f"Collecting data and news for '{name}'...")
            try:
                data, news = gather(name)
            except Exception as error:
                print(f"Could not collect data: {error}")
                continue
            system, history = system_prompt(data, news), []
            show_header(data, news)
            continue
        try:
            if text == "/report":
                report = ask(REPORT_REQUEST)
                print("\n" + report + f"\n\nSaved: {save_report(data, report, provider, model)}")
            else:
                print("\nBot: " + ask(text))
        except (APIStatusError, APIConnectionError) as error:
            print(explain(error))
    print("Bye! (This chat is a learning exercise, not financial advice.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
