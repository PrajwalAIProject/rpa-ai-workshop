# Troubleshooting

A consolidated FAQ for the whole workshop. Each entry is **symptom → cause → fix**. For
deeper, tool-specific help, follow the cross-links into each prerequisite guide's "Common
errors and fixes" section and the per-tier READMEs rather than reading everything here.

> **Heads-up:** AWS, Kiro, and UiPath change their terms, pricing, and screens often —
> confirm current details on the official pages before the session. Content was rephrased
> for compliance with licensing restrictions.

## Python / virtual environment

See the full guide: [`00-prerequisites/python-setup.md`](00-prerequisites/python-setup.md).

- **`'python' is not recognized` / wrong version** — Python isn't on your PATH, or an old
  version shadows it. Reinstall with "Add python.exe to PATH" ticked, open a **new**
  terminal, and verify with `python --version` (or `py --version` on Windows).
- **`ModuleNotFoundError` for `yfinance` / `feedparser` / `pandas`** — Your virtual
  environment isn't active, or dependencies aren't installed. Activate the venv and run
  `pip install -r 00-prerequisites/requirements.txt`.
- **PowerShell blocks `Activate.ps1` (execution policy)** — Windows blocks the activation
  script by default. In that PowerShell session run
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`, then activate again.
- **`pip install` fails with an SSL / certificate error on college wifi** — A filtering
  proxy is intercepting HTTPS. Try a different/tethered network, or ask IT for the
  proxy's trusted certificate; avoid disabling TLS verification.

## API keys

**Projects 1 and 2 expert (free Gemini / Groq key):** see
[`00-prerequisites/free-ai-api-key.md`](00-prerequisites/free-ai-api-key.md) and the error
table in [Project 1 expert](01-stock-market-analyzer/expert/README.md). The usual fixes:
the `.env` must sit next to the script (not `.env.txt`), the key must be pasted without
quotes, and on a `429` (free limit) wait a minute or switch `LLM_PROVIDER`.

**GitHub Copilot (Project 1):** sign-in, Agent mode and monthly-limit fixes are in
[`00-prerequisites/git-and-editor.md`](00-prerequisites/git-and-editor.md).

**Project 2 email (Gmail):** `login refused` means you need a Gmail **App Password**
(2-Step Verification on), not your normal password. See the
[Project 2 expert](02-morning-news-digest/expert/README.md) README.

## Network

- **"Network or API error" / "No headlines could be fetched" / yfinance returns nothing**
  — You're offline, or the data source throttled you. The scripts catch this and exit
  cleanly — check your connection and retry. See
  [Project 1 basic](01-stock-market-analyzer/basic/README.md) and
  [Project 2 basic](02-morning-news-digest/basic/README.md).
- **One RSS feed is empty but others work** — Normal; a single feed may be down. The
  script skips it and uses the rest.
- **"No listed company found for ..."** (Project 1) — The company name didn't match a
  listed stock. Type the full name ("Tata Consultancy Services") and check the spelling.
- **Scraped sections come back empty** (Project 1 advanced) — screener.in changed its
  page layout, or returned a block page. See the
  [Project 1 advanced](01-stock-market-analyzer/advanced/README.md) README.

## AWS

AWS is **optional** — only needed if you host the Project 3 expert watcher on AWS. See
the full guide: [`00-prerequisites/aws-free-tier.md`](00-prerequisites/aws-free-tier.md).

- **Card declined or a verification hold appears at signup** — The card must support
  international online charges. Use a different card, or avoid the card entirely with a
  **card-free path** — AWS Student Rewards (no card ever; ~12 months premium training, up
  to $30 in AWS credits, a $100 certification exam voucher) or AWS Educate (email-only, no
  card, learners 13+).
- **Worried about a surprise bill** — Set up a budget alert. AWS Budgets gives 62
  budget-days per month free, so one monthly cost budget is free; create a zero-spend
  budget right after signup and stay on always-free limits.
- **Account auto-closes or free access ends** — On the Free account plan, usage is capped
  to your credits and always-free limits; follow the cost-safety and teardown steps in the
  guide to keep the account at zero cost.

## Kiro

Used in Project 3 expert. See the full guide:
[`00-prerequisites/kiro-install.md`](00-prerequisites/kiro-install.md).

- **Not sure whether you need an AWS account** — You do **not** need an AWS account to use
  Kiro. Sign in with GitHub, Google, an AWS Builder ID, or AWS IAM Identity Center.
- **Sign-in fails / agent features greyed out** — Confirm you signed in with one of the
  supported providers above and that your network allows the sign-in flow; sign out and
  back in if needed.
- **"Out of credits"** — The free tier is 50 credits per month (perpetual) with Claude
  Sonnet 4.5 plus open-weight models, subject to rate limits. Wait for the monthly reset;
  the free tier is all this workshop needs. Confirm current terms at
  [kiro.dev/pricing](https://kiro.dev/pricing/).

## UiPath

Used in Project 3 basic and advanced. See the full guide:
[`00-prerequisites/uipath-cloud.md`](00-prerequisites/uipath-cloud.md).

- **Only StudioX opens, not Studio** — Studio and StudioX are separate profiles in the
  same installer; pick "Studio" on first launch or switch from the home screen. See
  [Project 3 basic](03-studiox-to-agentic-rpa/basic/README.md).
- **Orchestrator "robot unavailable" / machine limit** — The Community plan limits
  Orchestrator to **1 machine per user**. Make sure your robot is connected and you're not
  trying to register a second machine. See
  [Project 3 advanced](03-studiox-to-agentic-rpa/advanced/orchestrator_setup_guide.md).
- **Queue items retry forever** — Your retry rule has no escalate/stop path. Add a
  retry-or-escalate rule so exhausted items escalate instead of looping.
