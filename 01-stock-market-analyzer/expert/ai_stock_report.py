"""Project 1 - Expert: an AI-written stock report, using a FREE AI API.

Reference solution. In the workshop you ask GitHub Copilot to write this file for you
(see README.md for the prompt); compare with this one if yours misbehaves.

What it does:
  1. Collects the company's data with the advanced tier (stock_trend.collect):
     price trend + scraped fundamentals.
  2. Sends that data to a free AI model and asks for a plain-English report.
     Default: Google Gemini (free API key from aistudio.google.com).
     Backup:  Groq (free API key from console.groq.com).
     Both speak the same "OpenAI-compatible" API, so one library (openai) works
     for both; you switch with one line in .env.
  3. Prints the report and saves it as <SYMBOL>_report.md.

Setup (see 00-prerequisites/free-ai-api-key.md) - a .env file next to this script:
    LLM_PROVIDER=gemini
    GEMINI_API_KEY=<your key>
    # or:  LLM_PROVIDER=groq  and  GROQ_API_KEY=<your key>

Run:
    python ai_stock_report.py "Infosys"
    python ai_stock_report.py "Infosys" --dry-run   # show the prompt, don't call AI
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, OpenAI

HERE = Path(__file__).resolve().parent
# Reuse the advanced tier. In your own project folder all three files sit together;
# in this repo the advanced tier lives next door.
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "advanced"))
from stock_trend import collect  # noqa: E402

load_dotenv(HERE / ".env")
load_dotenv(HERE.parent.parent / ".env")  # repo-root .env, if you keep it there

# provider -> (API address, name of the key in .env, default model)
PROVIDERS = {
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai/",
               "GEMINI_API_KEY", "gemini-flash-latest"),
    "groq": ("https://api.groq.com/openai/v1",
             "GROQ_API_KEY", "openai/gpt-oss-20b"),
}

INSTRUCTIONS = """You are a friendly stock-market teacher for engineering students in India.
Using ONLY the data below, write a short report in simple English with these sections:

1. Company in one line - what the company does.
2. Recent price trend - what the 1-week, 1-month, 6-month and 1-year numbers and the
   50/200-day averages say. Name the trend (up, down or sideways).
3. Business health - sales and profit growth, key ratios (P/E, ROE, debt if given),
   and the most important pros and cons.
4. Things to watch - two or three points a careful investor would check next.
5. One-line summary.

Rules: use only numbers that appear in the data; if something is missing say "not
available"; explain any finance word the first time you use it; do NOT tell the reader
to buy or sell; keep it under 350 words; end with: "This is a learning exercise, not
financial advice."

DATA (JSON):
"""


def pick_fallback_model(client, provider):
    """If the default model name has changed, choose a current one from the provider's list."""
    names = [m.id.removeprefix("models/") for m in client.models.list()]
    wanted = "flash" if provider == "gemini" else "gpt-oss"
    candidates = [n for n in names if wanted in n and "image" not in n and "tts" not in n]
    return candidates[0] if candidates else None


def ask_ai(prompt, provider, model):
    """Send one prompt to the chosen free AI model and return (text, model_used, usage)."""
    base_url, key_name, _ = PROVIDERS[provider]
    api_key = os.getenv(key_name)
    if not api_key:
        raise SystemExit(f"{key_name} is not set. Put {key_name}=<your key> in a .env file "
                         "next to this script (see 00-prerequisites/free-ai-api-key.md).")
    client = OpenAI(api_key=api_key, base_url=base_url)
    messages = [{"role": "user", "content": prompt}]
    try:
        reply = client.chat.completions.create(model=model, messages=messages, temperature=0.3)
    except APIStatusError as error:
        if error.status_code != 404:  # 404 = model name not found -> try a current one
            raise
        replacement = pick_fallback_model(client, provider)
        if not replacement:
            raise
        print(f"Model '{model}' not found; using '{replacement}' instead.")
        model = replacement
        reply = client.chat.completions.create(model=model, messages=messages, temperature=0.3)
    return reply.choices[0].message.content, model, reply.usage


def main():
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry_run = "--dry-run" in sys.argv
    name = " ".join(args).strip() or input("Enter a company name: ").strip()
    if not name:
        print("Please type a company name, for example: Infosys")
        return 1

    provider = os.getenv("LLM_PROVIDER", "gemini").strip().lower()
    if provider not in PROVIDERS:
        print(f"LLM_PROVIDER must be one of {', '.join(PROVIDERS)} (got '{provider}').")
        return 1
    model = os.getenv("LLM_MODEL") or PROVIDERS[provider][2]

    print(f"Collecting data for '{name}'...")
    try:
        data = collect(name)
    except Exception as error:
        print(f"Could not collect data: {error}")
        return 1
    prompt = INSTRUCTIONS + json.dumps(data, ensure_ascii=False)

    if dry_run:
        print(prompt)
        print(f"\n(dry run: would call {provider} model {model}; prompt is {len(prompt):,} characters)")
        return 0

    print(f"Asking the AI ({provider}, {model})...")
    try:
        report, model, usage = ask_ai(prompt, provider, model)
    except APIStatusError as error:
        hints = {
            400: "The request was rejected. Check LLM_MODEL, or remove it to use the default.",
            401: "The API key is wrong. Copy it again into .env (no quotes, no spaces).",
            403: "The key isn't allowed to use this model/region. Create a new key, or switch LLM_PROVIDER.",
            404: "Model not found. Remove LLM_MODEL from .env to use the default.",
            413: "The prompt is too big for this model's free limit. Use Gemini, or send fewer fields.",
            429: "Free-tier limit reached (too many requests). Wait a minute, or switch LLM_PROVIDER.",
        }
        hint = hints.get(error.status_code, "See the README troubleshooting table.")
        if "api key" in str(error).lower():  # Gemini reports a bad key as 400, Groq as 401
            hint = hints[401]
        print(f"AI error {error.status_code}: {str(error)[:300]}\nHint: {hint}")
        return 1
    except APIConnectionError as error:
        print(f"Could not reach the AI service: {error}. Check your internet connection.")
        return 1

    print("\n" + "=" * 64)
    print(f"  AI STOCK REPORT · {data['company']} ({data['symbol']})")
    print("=" * 64 + "\n")
    print(report)
    out_file = HERE / f"{data['symbol'].replace('.', '_')}_report.md"
    out_file.write_text(f"# AI stock report: {data['company']} ({data['symbol']})\n\n"
                        f"_Written by {provider} / {model}_\n\n{report}\n", encoding="utf-8")
    tokens = f"{usage.prompt_tokens}/{usage.completion_tokens}" if usage else "n/a"
    print(f"\nSaved: {out_file.name}   (model: {model}, tokens in/out: {tokens})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
