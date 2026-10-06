# Free AI API key (expert levels of Projects 1 and 2)

The expert levels send data to an AI model and get text back: the stock report in Project 1,
the morning news briefing in Project 2. You need **one free API key** for both. **No credit card, no AWS account, no payment.**

> **Copilot vs. an API key.** GitHub Copilot is the AI that *helps you write the code*
> in VS Code. When your finished script runs, it calls an AI model on its own, and that
> needs its own key. Both are free. (GitHub's own model API, GitHub Models, was retired
> in July 2026, so we use Gemini or Groq.)

> Free tiers change often. The limits below were checked in October 2026; confirm
> current numbers on the provider's page if something looks different.

## Pick one (Gemini is the default)

| | **Google Gemini** (recommended) | **Groq** (backup) |
|---|---|---|
| Sign in with | Any Google account | Email, Google or GitHub |
| Get the key at | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) | [console.groq.com/keys](https://console.groq.com/keys) |
| Model the script uses | `gemini-flash-latest` (always the current Flash model) | `openai/gpt-oss-20b` |
| Free limits (approx.) | ~10–15 requests/min, ~1,000+ requests/day | 30 requests/min, 1,000/day, 8,000 tokens/min |
| Card needed | No | No |
| Good to know | Free-tier prompts may be used by Google to improve its products. Fine for public stock data; never send personal data. | Very fast. The 8,000 tokens/min limit means about one report at a time. |

One report uses one request, so either limit is far more than a workshop needs. Each
student uses their **own** key, so a full lab doesn't share one limit.

Sources: [Gemini API free tier](https://tinkerllm.com/blog/gemini-api-free-tier-limits-rate-quotas/),
[Groq free tier](https://klymentiev.com/blog/groq-pricing),
[Gemini OpenAI compatibility](https://ai.google.dev/gemini-api/docs/openai).

---

## Steps — Google Gemini

1. Open [aistudio.google.com/apikey](https://aistudio.google.com/apikey) and sign in with
   your Google account. Accept the terms if asked (Google requires you to be 18+).
2. Click **Create API key**. If asked for a project, let it create one for you.
3. **Copy the key** (it starts with `AIza`).

   ![Google AI Studio Create API key](images/gemini-api-key.png)
   <br><sub>Screenshot needed — see <a href="images/README.md">images/README.md</a>. Capture: the AI Studio API keys page with the Create API key button. Do not show a real key.</sub>
4. In your VS Code project folder (the one with `stock_trend.py`), create a file named
   exactly `.env` containing:

   ```text
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=paste-your-key-here
   ```

## Steps — Groq (backup)

1. Open [console.groq.com](https://console.groq.com/) and sign up (email, Google or GitHub).
2. Go to **API Keys** → **Create API Key**, give it a name such as `workshop`, and
   **copy the key** (it starts with `gsk_`). It's shown only once.

   ![Groq console Create API key](images/groq-api-key.png)
   <br><sub>Screenshot needed — see <a href="images/README.md">images/README.md</a>. Capture: the Groq console API Keys page with Create API Key. Do not show a real key.</sub>
3. Your `.env` then looks like:

   ```text
   LLM_PROVIDER=groq
   GROQ_API_KEY=paste-your-key-here
   ```

You can keep both keys in `.env` and switch with the `LLM_PROVIDER` line. That's useful
if one service is slow or blocked on the college network.

> **Keep keys secret.** No quotes and no spaces around `=`. Never commit `.env` to
> GitHub (it's in this repo's `.gitignore`), never paste a key into Copilot Chat or a
> screenshot, and if one leaks, delete it on the provider's page and make a new one.

---

## Check it works

From your project folder:

```bash
pip install openai python-dotenv
python ai_stock_report.py "Infosys"
```

A report printed with a `model: ... tokens in/out` line means it works. (No script yet?
Run the reference one from the repo root: `python 01-stock-market-analyzer/expert/ai_stock_report.py "Infosys"`,
with the `.env` in `01-stock-market-analyzer/expert/` or the repo root.)

## Common errors and fixes

| You see | Fix |
| ------- | --- |
| `GEMINI_API_KEY is not set` / `GROQ_API_KEY is not set` | `.env` is missing, misnamed (`.env.txt`), or not in the folder you run the script from. In Windows Explorer, turn on **View → File name extensions** to check. |
| `400 ... Please pass a valid API key` (Gemini) or `401 Invalid API Key` (Groq) | Copy the key again; no quotes, no spaces. |
| `429` / "quota exceeded" | Free-tier limit hit. Wait a minute, or switch `LLM_PROVIDER` to the other service. |
| `404` / model not found | The script picks a current model automatically. If it still fails, delete any `LLM_MODEL=` line from `.env`. |
| `413` / request too large (Groq) | The prompt is over Groq's free 8,000 tokens/min. Use Gemini, or wait a minute. |
| `403` / "not available in your region" | Rare in India; switch provider, or try another network. |
| Certificate / SSL error | College or office HTTPS inspection. Use a phone hotspot, or `pip install truststore` and add `import truststore; truststore.inject_into_ssl()` as the first line of the script. |
