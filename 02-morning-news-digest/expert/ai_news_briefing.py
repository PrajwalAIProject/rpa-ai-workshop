"""Project 2 - Expert: an AI morning briefing, using a FREE AI API.

Reference solution. In the workshop you ask GitHub Copilot to write this file for you
(see README.md for the prompt); compare with this one if yours misbehaves.

What it does:
  1. Collects the last 24 hours of headlines with the advanced level (news_report.collect).
  2. Sends them to a free AI model (Google Gemini by default, or Groq) and asks it to act
     as an editor: pick the 5 most important stories, say in one line why each matters,
     and add one "for engineering students" note. The rules in the keyword version
     can't judge importance; the AI can.
  3. Prints the briefing, saves it as briefing.md, and (optional) emails it to you.

Setup (see 00-prerequisites/free-ai-api-key.md) - the same .env as Project 1:
    LLM_PROVIDER=gemini
    GEMINI_API_KEY=<your key>
Optional email (Gmail needs an App Password, see README.md):
    SMTP_HOST=smtp.gmail.com  SMTP_PORT=587  SMTP_USERNAME=  SMTP_PASSWORD=  EMAIL_TO=

Run:
    python ai_news_briefing.py
    python ai_news_briefing.py --dry-run    # show the prompt, don't call AI
    python ai_news_briefing.py --email      # also email the briefing
"""

import os
import smtplib
import sys
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, OpenAI

HERE = Path(__file__).resolve().parent
# Reuse the advanced level. In your own project folder all files sit together;
# in this repo the advanced level lives next door.
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "advanced"))
from news_report import collect  # noqa: E402

load_dotenv(HERE / ".env")
load_dotenv(HERE.parent.parent / ".env")  # repo-root .env, if you keep it there

PROVIDERS = {
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai/",
               "GEMINI_API_KEY", "gemini-flash-latest"),
    "groq": ("https://api.groq.com/openai/v1",
             "GROQ_API_KEY", "openai/gpt-oss-20b"),
}

INSTRUCTIONS = """You are the editor of a short morning news briefing for engineering
students in India. Below are today's headlines, one per line, as
[category] source: headline.

Write the briefing in simple English, using ONLY these headlines:

TOP 5 TODAY
For the 5 most important stories (importance for India and for young people, not
celebrity gossip): a short, neutral title of your own, then one line "Why it matters: ...".
Mention the source in brackets.

QUICK HITS
One line each for 3 more stories worth knowing.

FOR ENGINEERING STUDENTS
One or two lines on the story that matters most for a technology career, and why.

Rules: do not invent facts that are not in the headlines; stay neutral on politics;
keep it under 300 words; no markdown tables.

HEADLINES:
"""


def ask_ai(prompt, provider, model):
    """Send the prompt to the chosen free AI model. Returns (text, model_used, usage)."""
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
        wanted = "flash" if provider == "gemini" else "gpt-oss"
        names = [m.id.removeprefix("models/") for m in client.models.list()]
        replacement = next((n for n in names if wanted in n and "image" not in n and "tts" not in n), None)
        if not replacement:
            raise
        print(f"Model '{model}' not found; using '{replacement}' instead.")
        model = replacement
        reply = client.chat.completions.create(model=model, messages=messages, temperature=0.3)
    return reply.choices[0].message.content, model, reply.usage


def send_email(subject, body):
    """Email the briefing with SMTP settings from .env. Returns a status message."""
    host, user, password = os.getenv("SMTP_HOST"), os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD")
    to = os.getenv("EMAIL_TO") or user
    if not (host and user and password and to):
        return "Email skipped: set SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD and EMAIL_TO in .env."
    message = EmailMessage()
    message["Subject"], message["From"], message["To"] = subject, os.getenv("EMAIL_FROM") or user, to
    message.set_content(body)
    try:
        with smtplib.SMTP(host, int(os.getenv("SMTP_PORT", "587")), timeout=20) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(message)
        return f"Emailed to {to}."
    except smtplib.SMTPAuthenticationError:
        return "Email failed: login refused. For Gmail use an App Password, not your normal password."
    except Exception as error:
        return f"Email failed: {error}"


def main():
    dry_run, want_email = "--dry-run" in sys.argv, "--email" in sys.argv
    provider = os.getenv("LLM_PROVIDER", "gemini").strip().lower()
    if provider not in PROVIDERS:
        print(f"LLM_PROVIDER must be one of {', '.join(PROVIDERS)} (got '{provider}').")
        return 1
    model = os.getenv("LLM_MODEL") or PROVIDERS[provider][2]

    print("Collecting today's headlines...")
    digest = collect()
    lines = [f"[{category}] {s['source']}: {s['title']}"
             for category, items in digest["categories"].items() for s in items]
    if not lines:
        print("No fresh headlines could be downloaded. Check your internet connection.")
        return 1
    prompt = INSTRUCTIONS + "\n".join(lines)

    if dry_run:
        print(prompt)
        print(f"\n(dry run: would call {provider} model {model}; {len(lines)} headlines, "
              f"{len(prompt):,} characters)")
        return 0

    print(f"Asking the AI editor ({provider}, {model})...")
    try:
        briefing, model, usage = ask_ai(prompt, provider, model)
    except APIStatusError as error:
        hints = {401: "The API key is wrong. Copy it again into .env (no quotes, no spaces).",
                 404: "Model not found. Remove LLM_MODEL from .env to use the default.",
                 413: "The prompt is too big for this model's free limit. Use Gemini.",
                 429: "Free-tier limit reached. Wait a minute, or switch LLM_PROVIDER."}
        hint = hints.get(error.status_code, "See the README troubleshooting table.")
        if "api key" in str(error).lower():  # Gemini reports a bad key as 400
            hint = hints[401]
        print(f"AI error {error.status_code}: {str(error)[:300]}\nHint: {hint}")
        return 1
    except APIConnectionError as error:
        print(f"Could not reach the AI service: {error}. Check your internet connection.")
        return 1

    title = f"Morning Briefing · {datetime.now():%d %b %Y}"
    print("\n" + "=" * 64 + f"\n  {title}\n" + "=" * 64 + "\n")
    print(briefing)
    (HERE / "briefing.md").write_text(f"# {title}\n\n_Edited by {provider} / {model} from "
                                      f"{len(lines)} headlines_\n\n{briefing}\n", encoding="utf-8")
    tokens = f"{usage.prompt_tokens}/{usage.completion_tokens}" if usage else "n/a"
    print(f"\nSaved: briefing.md   (model: {model}, tokens in/out: {tokens})")
    if want_email:
        print(send_email(title, briefing))
    return 0


if __name__ == "__main__":
    sys.exit(main())
