# Project 2 — Expert: AI News Agent

## What you'll build

A script that pulls morning headlines, passes them to Anthropic Claude, and asks it to
pick the **3 most significant** stories with a one-line "why it matters" for each. The
result is delivered by **email (SMTP)** when SMTP is configured, or printed otherwise —
all environment-driven.

## Prerequisites

- Everything from the [advanced tier](../advanced/README.md).
- An Anthropic API key in your `.env` (`ANTHROPIC_API_KEY=...`). See
  [`00-prerequisites/api-keys.md`](../../00-prerequisites/api-keys.md).
- (Optional) SMTP settings in `.env` if you want email delivery. Leave `SMTP_HOST`
  blank to just print.

## Step-by-step setup

1. Activate your virtual environment and install dependencies:
   ```bash
   pip install -r 00-prerequisites/requirements.txt
   ```
2. Make sure `.env` has your `ANTHROPIC_API_KEY`.
3. Run it:
   ```bash
   cd 02-morning-news-digest/expert
   python ai_news_agent.py
   ```
   With no SMTP set, it prints the top-3 digest. To email it instead, fill in the
   `SMTP_*` and `EMAIL_*` values in `.env`:
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=you@example.com
   SMTP_PASSWORD=your-app-password
   EMAIL_FROM=you@example.com
   EMAIL_TO=you@example.com
   ```

   > _Screenshot placeholder: an email client showing the delivered digest._

   > Tip: for Gmail, use an **app password**, not your account password.

## Common errors and fixes

- **"ANTHROPIC_API_KEY is not set"** — Add your key to `.env` at the repo root.
- **"Could not send email: ... authentication"** — Wrong SMTP username/password. For
  Gmail, generate an app password and enable 2-step verification first.
- **Email never arrives but no error** — Check spam, and that `EMAIL_TO` is correct.
- **Rate limit / overloaded** — Retry after a short wait; the free API tier is tight.
