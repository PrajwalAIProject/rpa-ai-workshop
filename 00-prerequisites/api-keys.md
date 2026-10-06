# API keys (Anthropic Claude) — Project 2 expert only

The **Project 2 expert** level asks Claude to pick the top news stories. That needs an
**Anthropic API key**. (Project 1's expert level uses a **free Gemini or Groq key**
instead; see [`free-ai-api-key.md`](free-ai-api-key.md).)

## What you'll set up

- An **Anthropic API key** from the Anthropic Console.
- The key stored **only** in a local `.env` file (git-ignored), never in code.

> This is a **paid** API (usage costs a small amount per request). Treat the key like a
> password. In a classroom setting, your **instructor may provide one shared key** so
> students don't each have to add billing — follow whatever your instructor says here.

---

## Steps

1. Sign up or sign in at the
   [Anthropic Console](https://console.anthropic.com/).
2. Go to **API Keys** (under settings) and **Create Key**. Give it a name like
   `rpa-workshop`.

   ![Anthropic Console Create Key dialog](images/anthropic-create-key.png)
   <br><sub>Screenshot needed — see <a href="images/README.md">images/README.md</a>. Capture: the Anthropic Console "Create Key" dialog with a key name filled in (do not reveal a real key value).</sub>
3. **Copy the key immediately** — the console shows the full value only once. It looks
   like `sk-ant-...`.
4. In the **repo root**, copy the example env file to a real one (the real `.env` is
   git-ignored):

   ```powershell
   # Windows (PowerShell):
   Copy-Item .env.example .env
   ```

   ```bash
   # macOS / Linux:
   cp .env.example .env
   ```
5. Open `.env` and paste your key on the `ANTHROPIC_API_KEY` line, with no quotes and no
   trailing spaces:

   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

The reference template is [`.env.example`](../.env.example), which also lists the
optional webhook (Project 1) and SMTP email (Project 2) settings.

---

## Verify

1. `.env` exists in the repo root and contains your `ANTHROPIC_API_KEY=` line.
2. Running `git status` does **not** list `.env` as a change to commit — it is ignored
   by [`.gitignore`](../.gitignore).
3. The Project 2 expert script runs without an "ANTHROPIC_API_KEY is not set" error.

---

## Keep the key safe

- **Never commit `.env`.** It is already in `.gitignore` (the pattern `.env` with an
  exception only for `.env.example`).
- Don't paste the key into chat, screenshots, or source files.
- If a key leaks, **revoke it** in the Anthropic Console and create a new one.
- If you ever run a script from GitHub Actions, store the key as a **repository
  secret**, never in the workflow file.

---

## Common errors and fixes

- **"ANTHROPIC_API_KEY is not set"** — The key is missing from `.env`, or `.env` isn't
  in the repo root. Add it and re-run.
- **Authentication failed / 401** — The key is wrong or revoked. Create a new key in the
  console and update `.env`.
- **Rate limit / overloaded** — The free/low tiers have tight limits; wait a few seconds
  and retry.
- **Key accidentally committed** — Revoke it immediately in the console, create a new
  one, and remove it from the file. Rotating the key is the only real fix once it's been
  pushed.
