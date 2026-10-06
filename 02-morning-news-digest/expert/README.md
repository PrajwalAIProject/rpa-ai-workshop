# Project 2 — Expert: an AI news editor (free AI API) + email

## What you'll build

`ai_news_briefing.py`: it collects the last 24 hours of headlines with the advanced
level, then asks a **free AI model** (Google **Gemini** by default, or **Groq**) to act as
an **editor**:

- **TOP 5 TODAY:** the most important stories, each with "Why it matters".
- **QUICK HITS:** three more stories worth knowing.
- **FOR ENGINEERING STUDENTS:** the story that matters most for a tech career.

It prints the briefing, saves `briefing.md`, and with `--email` sends it to your inbox.

**Why AI here?** The advanced level sorts with keyword rules; it can't tell which story
*matters*. Deciding importance is judgment, which is what AI adds. It's the same "RPA is
the hands, AI is the judgment" idea from the talk.

## Before you start

- The [advanced level](../advanced/README.md) done, in the same folder
  (`news_report.py` must be there).
- A free **Gemini key** (or Groq) in `.env`, the same key as Project 1. See
  [`free-ai-api-key.md`](../../00-prerequisites/free-ai-api-key.md):

  ```text
  LLM_PROVIDER=gemini
  GEMINI_API_KEY=AIza...your key...
  ```

## Step 1 — Give Copilot this prompt (Agent mode)

```text
Create a Python 3 script called ai_news_briefing.py in this folder. It uses collect()
from news_report.py to get today's headlines, then asks a free AI model to edit them
into a short morning briefing.

Install: pip install openai python-dotenv

1. Load settings from .env with python-dotenv: LLM_PROVIDER ("gemini" by default, or
   "groq"), GEMINI_API_KEY, GROQ_API_KEY, optional LLM_MODEL. Never print a key.
2. Use the openai library for both (they are OpenAI-compatible):
   gemini: base_url "https://generativelanguage.googleapis.com/v1beta/openai/",
           default model "gemini-flash-latest"
   groq:   base_url "https://api.groq.com/openai/v1", default model "openai/gpt-oss-20b"
3. Turn the headlines into one line each: "[category] source: title".
4. Prompt: "You are the editor of a short morning news briefing for engineering students
   in India." Ask for three sections: TOP 5 TODAY (a short neutral title, the source, and
   one line "Why it matters"), QUICK HITS (3 one-liners), FOR ENGINEERING STUDENTS (the
   story that matters most for a tech career). Rules: use only these headlines, don't
   invent facts, stay neutral on politics, under 300 words.
5. Call client.chat.completions.create(model=..., messages=[...], temperature=0.3),
   print the result, save it to briefing.md, and print the model and token counts.
   If the model is not found (404), pick a current one from client.models.list()
   ("flash" for Gemini, "gpt-oss" for Groq) and retry.
6. --dry-run prints the prompt without calling the AI.
7. --email sends the briefing with smtplib using SMTP_HOST, SMTP_PORT (587),
   SMTP_USERNAME, SMTP_PASSWORD and EMAIL_TO from .env (starttls, then login). If those
   are missing, print how to set them instead of crashing; if login fails, say "for Gmail
   use an App Password".
8. Helpful one-line hints for: missing key, invalid key (Gemini 400 / Groq 401),
   429 free limit (wait or switch LLM_PROVIDER), no internet.

Then run it with --dry-run. If my .env is set up, run it for real.
```

## Step 2 — Run it

```bash
python ai_news_briefing.py --dry-run     # see exactly what goes to the AI (no key needed)
python ai_news_briefing.py               # the real briefing
python ai_news_briefing.py --email       # also email it (see below)
```

## What correct output looks like

The AI's words change every run. Check:

- Three sections in order: **TOP 5 TODAY**, **QUICK HITS**, **FOR ENGINEERING STUDENTS**.
- Every story it mentions is really in the headlines list (`--dry-run` shows the list).
  Pick two and check. If it mentions something that isn't there, that's a hallucination;
  tighten the prompt.
- Compare with the advanced level: did the AI pick more important stories than "newest
  first"? Did it handle the stories the keyword rules put in the wrong category?
- The last line looks like `Saved: briefing.md   (model: gemini-flash-latest, tokens in/out: 1200/400)`.

## Optional — email it to yourself (Gmail)

Gmail won't accept your normal password from a script. Use an **App Password**:

1. Turn on **2-Step Verification** for your Google account (myaccount.google.com → Security).
2. Open **myaccount.google.com/apppasswords**, create one named `news-digest`, and copy the 16 characters.
3. Add to `.env`:

   ```text
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=you@gmail.com
   SMTP_PASSWORD=the-16-character-app-password
   EMAIL_TO=you@gmail.com
   ```
4. Run `python ai_news_briefing.py --email`.

Delete the App Password after the workshop if you don't need it. Never commit `.env`.

**Stretch:** schedule it every morning with Task Scheduler (see the advanced README).
Then it's a real "morning briefing in my inbox" agent.

## If Copilot's script is wrong — follow-up prompts

- *"Run it with --dry-run and show me the prompt. Shorten each headline line if it's long."*
- *"The briefing mentions a story that isn't in the headlines. Add the rule: only use the given headlines."*
- *"Email fails with authentication error. Explain Gmail App Passwords and update the error message."*
- *"Add a --topic option so the briefing only covers, for example, technology."*

Reference solution: [`ai_news_briefing.py`](ai_news_briefing.py). In this repo it imports
`news_report.py` from `../advanced/`; in your own folder all files sit together.

## Common errors and fixes

| You see | Fix |
| ------- | --- |
| `GEMINI_API_KEY is not set` | `.env` missing, named `.env.txt`, or not in the folder you run from. |
| `400 ... valid API key` (Gemini) / `401` (Groq) | Copy the key again, no quotes, no spaces. |
| `429` / quota exceeded | Free limit reached. Wait a minute, or switch `LLM_PROVIDER`. |
| `413` / request too large (Groq) | Too many headlines for Groq's free 8,000 tokens/min. Use Gemini. |
| `Email failed: login refused` | Use a Gmail **App Password** (2-Step Verification must be on), not your normal password. |
| `ModuleNotFoundError: No module named 'news_report'` | Run from the folder that contains `news_report.py`. |
| Certificate / SSL error | Campus HTTPS inspection: phone hotspot, or `truststore` (see the basic README). |
