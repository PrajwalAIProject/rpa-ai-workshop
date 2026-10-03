# Project 1 — Expert: AI Commentary Agent

## What you'll build

A script that computes stock indicators (last price, day change, 20/50-day moving
averages, golden/death cross) and then asks Anthropic Claude to write a 2-3 sentence
plain-English commentary on them. A GitHub Actions cron job runs it on a schedule, and
the model is prompted to **flag low confidence** instead of always sounding certain.

## Prerequisites

- Everything from the [advanced tier](../advanced/README.md).
- An Anthropic API key in your `.env` file (`ANTHROPIC_API_KEY=...`). See
  [`00-prerequisites/README.md`](../../00-prerequisites/README.md) step 3.
- The `anthropic` and `python-dotenv` packages (in the shared requirements).

## Step-by-step setup

1. Activate your virtual environment and install dependencies:
   ```bash
   pip install -r 00-prerequisites/requirements.txt
   ```
2. Make sure `.env` exists at the repo root with your key:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```
3. Run it locally:
   ```bash
   cd 01-stock-market-analyzer/expert
   python ai_commentary_agent.py AAPL
   ```
   It prints the computed indicators, then Claude's commentary.
4. Schedule it on GitHub Actions:
   - Copy [`.github/workflows/daily_run.yml`](.github/workflows/daily_run.yml) to the
     **repository root** `.github/workflows/` folder (GitHub only discovers workflows
     there).
   - Add `ANTHROPIC_API_KEY` as a repository secret under
     _Settings → Secrets and variables → Actions_.

     > _Screenshot placeholder: the GitHub Actions "New repository secret" screen._
   - The job runs on the cron schedule and can also be triggered manually from the
     Actions tab.

### Stretch: low-confidence flag

The prompt in `get_commentary()` explicitly asks the model to say when its confidence
is low (weak/mixed signal or thin data) rather than overstating certainty.

## Common errors and fixes

- **"ANTHROPIC_API_KEY is not set"** — The key is missing from `.env`, or `.env` isn't
  at the repo root. Add it and re-run.
- **"Anthropic API call failed: ... authentication"** — The key is wrong or revoked.
  Generate a new one in the [Anthropic Console](https://console.anthropic.com/).
- **Workflow never runs on GitHub** — The YAML must be in the repo-root
  `.github/workflows/`, not the project subfolder. GitHub ignores workflows elsewhere.
- **Rate limit / overloaded errors** — Retry after a short wait; the free tier has
  tight limits.
