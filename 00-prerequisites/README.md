# 00 — Prerequisites

Set this up once, before the lab. Everything else in the repo assumes it is done.

## 1. Install Python 3.11 or newer

1. Download Python from [python.org/downloads](https://www.python.org/downloads/).
   Any version **3.11 or newer** works.
2. On Windows, tick **"Add python.exe to PATH"** in the installer.
3. Confirm it worked:
   ```bash
   python --version
   ```
   You should see `Python 3.11.x` (or newer).

## 2. Create a virtual environment and install dependencies

A virtual environment keeps this workshop's packages separate from the rest of your
system. Do this from the repo root (`rpa-ai-workshop/`).

```bash
# Create the environment
python -m venv .venv

# Activate it
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (cmd):
.venv\Scripts\activate.bat
# macOS / Linux:
source .venv/bin/activate

# Install every Python dependency used across all projects
pip install -r 00-prerequisites/requirements.txt
```

When the environment is active your prompt is prefixed with `(.venv)`. Run
`deactivate` to leave it.

## 3. Set up secrets

The expert tiers call the Anthropic Claude API, which needs a key.

1. Copy the example file to a real one (git ignores `.env`):
   ```bash
   # Windows (PowerShell):
   Copy-Item .env.example .env
   # macOS / Linux:
   cp .env.example .env
   ```
2. Open `.env` and paste your `ANTHROPIC_API_KEY`. Get a key from the
   [Anthropic Console](https://console.anthropic.com/).
3. Never commit `.env`. It is already in `.gitignore`.

## 4. Sign up for UiPath Automation Cloud (Community plan)

Needed for Project 3. Free, no card required.

1. Go to [cloud.uipath.com](https://cloud.uipath.com/) and create a Community account.
2. This gives you Studio (Pro), StudioX, Orchestrator, and one Attended + one
   Unattended robot.
3. Enable **MFA** on the account.

## 5. Sign up for AWS Educate (expert tier of Project 3 only)

Only needed if you reach Project 3 expert (Kiro + the watcher agent).

1. Prefer [AWS Educate](https://aws.amazon.com/education/awseducate/) with your school
   email — typically no card required, with starter credit.
2. If you use a standard AWS account instead, **set a billing alert at a low
   threshold before launching any compute**, and create a scoped **IAM user** rather
   than using the root account.
3. Enable **MFA**.
4. AWS terms change often — confirm current credit amounts closer to the date.

## 6. Install Kiro

Needed for Project 3 expert.

1. Download and install Kiro, AWS's spec-driven agentic IDE.
2. Sign in with the AWS account from step 5.

## Common errors and fixes

- **`python` not found / wrong version** — On some systems the command is `python3`.
  Reinstall and tick "Add to PATH" (Windows), or use `python3 -m venv .venv`.
- **PowerShell blocks `Activate.ps1`** — Run once in that terminal:
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again.
- **`pip install` fails to build a package** — Upgrade pip first:
  `python -m pip install --upgrade pip`, then retry.
- **`ANTHROPIC_API_KEY` not picked up** — Confirm `.env` is in the repo root and the
  line reads `ANTHROPIC_API_KEY=sk-...` with no quotes or trailing spaces.
