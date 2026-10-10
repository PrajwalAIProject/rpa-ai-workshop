# Get your laptop ready

Do this **at home, 2–3 days before the workshop**. It takes about **1 hour**, plus a
few days' wait for GitHub Education approval. College Wi-Fi is slow when 60 laptops
download at once, so don't leave it for the day.

Work through the steps **in order**. Each step ends with a **check**. When every check
passes, your laptop is ready.

| Step | What you do | Time | Needed for |
| :--: | ----------- | :--: | ---------- |
| 1 | [Check your laptop](#step-1--check-your-laptop) | 5 min | Everything |
| 2 | [Create free accounts](#step-2--create-free-accounts) | 15 min | Everything |
| 3 | [Install the software](#step-3--install-the-software) | 45 min | Everything |
| 4 | [Get the workshop repo](#step-4--get-the-workshop-repo) | 2 min | Everything |
| 5 | [Install the Python packages](#step-5--install-the-python-packages) | 3 min | All projects |
| 6 | [Add your free AI key](#step-6--add-your-free-ai-key) | 5 min | Expert level of every project |
| 7 | [Run the night-before test](#step-7--run-the-night-before-test) | 5 min | Everything |

> Everything here is **free** and needs **no credit card**. You do **not** need an AWS
> account for any project.

---

## Step 1 — Check your laptop

- [ ] **Windows 10 or 11 (64-bit)**. UiPath Studio (Project 3) runs only on Windows.
      Projects 1 and 2 also work on macOS or Linux.
- [ ] At least **8 GB RAM** and **10 GB free disk space**.
- [ ] You can **install software** (administrator rights). College-managed laptops
      often block this, so check early.
- [ ] Windows is **up to date**.
- [ ] On the day, bring your **charger** (the session is 5 hours) and your **phone**
      (sign-in codes, and a mobile hotspot if the lab network blocks something).

## Step 2 — Create free accounts

| Account | Used for | Sign up at | Note |
| ------- | -------- | ---------- | ---- |
| **GitHub** | Signing in to VS Code and GitHub Copilot, saving your code | [github.com/signup](https://github.com/signup) | Pick a professional username. Recruiters will see it. |
| **GitHub Education** *(recommended)* | The **Copilot Student** plan, with more AI usage than Copilot Free | [education.github.com/pack](https://education.github.com/pack) | Apply with your college email or ID card. **Approval takes 1–3 days**, so apply first. Copilot Free is enough if you're not approved in time. |
| **Google** | The free Gemini AI key (Step 6) | [accounts.google.com](https://accounts.google.com/) | Your normal Gmail account works. |
| **UiPath Automation Cloud (Community)** | UiPath Studio and Orchestrator (Project 3) | [cloud.uipath.com](https://cloud.uipath.com/) | Choose the free **Community** plan. Turn on MFA. Details: [`uipath-cloud.md`](uipath-cloud.md) |
| **Kiro** | The AI agent IDE for Project 3 | Sign in inside Kiro (Step 3) | No new account: use your **Google** or **GitHub** login. |
| **Groq** *(optional)* | A backup free AI key | [console.groq.com](https://console.groq.com/) | Only if Gemini doesn't work for you. |

**Check:** you can sign in to GitHub, Google and UiPath Cloud, and your GitHub
Education application is submitted.

## Step 3 — Install the software

Install in this order. Open a **new** terminal after each install so it sees the change.

| # | Install | Download | Don't miss | Check (in a new terminal) | Full guide |
| :-: | ------- | -------- | ---------- | ------------------------- | ---------- |
| 1 | **Python 3.11 or newer** | [python.org/downloads](https://www.python.org/downloads/) | Tick **"Add python.exe to PATH"** on the first installer screen | `python --version` shows 3.11 or higher | [`python-setup.md`](python-setup.md) |
| 2 | **VS Code** | [code.visualstudio.com](https://code.visualstudio.com/) | Tick **"Add to PATH"** and **"Open with Code"**. Then install the **Python** extension (by Microsoft) | `code --version` | [`git-and-editor.md`](git-and-editor.md#2-install-vs-code) |
| 3 | **Git** | [git-scm.com/download/win](https://git-scm.com/download/win) | Keep the default options. Then set your name and email (see below) | `git --version` | [`git-and-editor.md`](git-and-editor.md#3-install-git) |
| 4 | **GitHub Copilot** (inside VS Code) | Built into VS Code | Sign in with GitHub (Accounts icon, bottom left), open **Chat**, and set the mode to **Agent** | Copilot Chat answers you | [`git-and-editor.md`](git-and-editor.md#4-sign-in-to-github-from-vs-code) |
| 5 | **UiPath Studio** (desktop, Windows only) | [UiPathStudioCommunity.msi](https://download.uipath.com/UiPathStudioCommunity.msi) (or **Download Studio** in cloud.uipath.com) | Choose **Quick** install, sign in, pick the **Studio** profile, then install the **UiPath browser extension** for Chrome/Edge. The installer is large, so do this at home | Studio opens and shows you signed in | [`uipath-cloud.md`](uipath-cloud.md#steps) |
| 6 | **Kiro** (AI agent IDE) | [kiro.dev/downloads](https://kiro.dev/downloads/) | Sign in with Google or GitHub. The free tier (50 credits a month) is enough. Install it **before** the UiPath CLI | Kiro writes and runs `hello.py` | [`kiro-install.md`](kiro-install.md) |
| 7 | **UiPath CLI** (`uip`), with Node.js and .NET 8 | In PowerShell: `irm https://download.uipath.com/uipath-cli/install.ps1 \| iex` | One command installs Node.js, the CLI, .NET 8 and UiPath skills for Kiro. Then open a new terminal and run `uip login --interactive` | `uip login status` shows your tenant | [`uipath-cli.md`](uipath-cli.md#quick-install-recommended-one-command) |

After installing Git, set your identity once. Use your GitHub account's email:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

**Check, Copilot:** in VS Code, open an empty folder (for example `C:\stock-project`),
open Copilot Chat in **Agent** mode, and type:

```text
Create hello.py that prints "Copilot works", then run it.
```

Allow it to run the command. The terminal should print `Copilot works`.

**Check, Kiro (Project 3):** open an empty folder in Kiro, choose **Vibe** in the Kiro
panel, and type the same request with `"Kiro works"`. It should print `Kiro works`.

## Step 4 — Get the workshop repo

In VS Code: **View → Command Palette → Git: Clone**, paste the address below, choose a
folder (a short path such as `C:\dev` works best) and open it.

```text
https://github.com/PrajwalAIProject/rpa-ai-workshop.git
```

Or in a terminal:

```bash
git clone https://github.com/PrajwalAIProject/rpa-ai-workshop.git
```

No Git yet? On the GitHub page click **Code → Download ZIP** and unzip it.

**Check:** VS Code shows the `rpa-ai-workshop` folder with `00-prerequisites`,
`01-stock-market-analyzer`, `02-morning-news-digest` and `03-studiox-to-agentic-rpa`.

## Step 5 — Install the Python packages

In VS Code, open the repo folder, then **Terminal → New Terminal**, and run:

```bash
python -m pip install --upgrade pip
pip install -r 00-prerequisites/requirements.txt
```

This installs everything the Python scripts in all three projects use:

| Package | What it does |
| ------- | ------------ |
| `yfinance` | Finds a company's stock symbol and downloads its prices |
| `requests` | Downloads web pages and news feeds |
| `beautifulsoup4` | Reads values out of a web page (web scraping) |
| `feedparser` | Reads RSS news feeds |
| `openai` | Talks to the free AI service (Gemini or Groq) |
| `python-dotenv` | Loads your secret key from the `.env` file |
| `openpyxl` | Reads the Excel file your UiPath bot writes (Project 3) |

*(Optional: create a virtual environment first, so these packages stay separate. See
[`python-setup.md`](python-setup.md#3-create-and-activate-a-virtual-environment).)*

**Check:** this prints `all imports OK`:

```bash
python -c "import yfinance, requests, bs4, openai, dotenv, feedparser, openpyxl; print('all imports OK')"
```

## Step 6 — Add your free AI key

The **expert** levels of all three projects call an AI model, which needs one free key
(in Project 3, the watcher agent's morning report).

1. Open [aistudio.google.com/apikey](https://aistudio.google.com/apikey), sign in with
   Google, click **Create API key** and copy it (it starts with `AIza`).
2. In the repo folder, copy `.env.example` to a new file named exactly **`.env`**.
3. Paste your key after `GEMINI_API_KEY=`:

   ```text
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=paste-your-key-here
   ```

Full guide, plus the Groq backup: [`free-ai-api-key.md`](free-ai-api-key.md).

> **Keep your key secret.** It goes **only** in `.env` (Git ignores that file).
> Never paste it into Copilot Chat, WhatsApp or a screenshot, and never commit it.

**Check:** the expert dry run in Step 7 prints an AI prompt without errors.

## Step 7 — Run the night-before test

Open the repo folder in VS Code, open a terminal (**Terminal → New Terminal**) and run
these one at a time:

| Run this | You should see |
| -------- | -------------- |
| `python --version` | `Python 3.11` or higher |
| `git --version` | A Git version number |
| `python 01-stock-market-analyzer/basic/company_info.py "Infosys"` | Infosys stock details (symbol, price) |
| `python 01-stock-market-analyzer/expert/ai_stock_report.py "Infosys" --dry-run` | The AI prompt the script would send |
| `python 02-morning-news-digest/basic/news_digest.py cricket` | Today's cricket headlines |
| Copilot Chat (Agent mode): *"Create hello.py that prints Copilot works, then run it."* | `Copilot works` in the terminal |
| `python 03-studiox-to-agentic-rpa/expert/test_watcher_agent.py` | `All watcher checks passed.` |
| `uip --version` and `uip login status` *(Project 3)* | A version number, and your tenant name |
| Kiro (Vibe): *"Create hello.py that prints Kiro works, then run it."* *(Project 3)* | `Kiro works` in Kiro's terminal |

**All of these work? Your laptop is ready.** (Doing only Projects 1–2? The first six are enough.) If one fails, open the guide for that step or
[`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md), and message your instructor **before**
the workshop day.

---

## What each project needs

| Project and level | Python | VS Code + Copilot | UiPath Studio + Cloud | UiPath CLI | Kiro | Free AI key |
| ----------------- | :----: | :---------------: | :-------------------: | :--------: | :--: | :---------: |
| **1** Stock analyzer: basic and advanced | ✅ | ✅ | — | — | — | — |
| **1** Stock analyzer: expert (AI report) | ✅ | ✅ | — | — | — | ✅ |
| **2** News digest: basic and advanced | ✅ | ✅ | — | — | — | — |
| **2** News digest: expert (AI editor) | ✅ | ✅ | — | — | — | ✅ |
| **3** PhoneDeals: basic (phones under ₹20K → Excel) | ✅ | — | ✅ | ✅ | ✅ | — |
| **3** PhoneDeals: advanced (deploy + schedule) | ✅ | — | ✅ | ✅ | ✅ | — |
| **3** PhoneDeals: expert (watcher agent) | ✅ | — | ✅ | ✅ | ✅ | ✅ |

**Optional extras:**

- **Gmail App Password**: only to email the Project 2 briefing to yourself. See the
  [Project 2 expert README](../02-morning-news-digest/expert/README.md).
- **An AWS account is not needed.** [`aws-free-tier.md`](aws-free-tier.md) is only for
  students who want to host the Project 3 watcher in the cloud on their own.

## Quick fixes

| Problem | Fix |
| ------- | --- |
| `'python' is not recognized` | Re-run the Python installer, choose **Modify**, and tick **"Add python.exe to PATH"**. Or use `py` instead of `python`. Then open a new terminal. |
| `'git' is not recognized` | Close and reopen VS Code after installing Git. |
| `pip install` fails on college Wi-Fi | Use your phone's hotspot, and run `python -m pip install --upgrade pip` first. |
| `CERTIFICATE_VERIFY_FAILED`, `SSLError`, or "No headlines could be downloaded" | The network is inspecting secure traffic (common on office and some college networks). Switch to your phone's hotspot. Or run `pip install truststore` and add `import truststore; truststore.inject_into_ssl()` as the first line of the script. |
| No Copilot icon or Chat panel | Update VS Code (**Help → Check for Updates**) and install **GitHub Copilot Chat** from Extensions. |
| Copilot writes code but doesn't run it | Switch the Chat mode drop-down to **Agent**. |
| "You've reached your monthly chat limit" | Copilot Free gives 50 chat requests a month. Save them for the lab, and apply for GitHub Education. |
| UiPath Studio opens as StudioX | Choose the **Studio** profile when it starts, or switch profiles in its settings. |
| `'uip' is not recognized` | Open a new terminal after `npm install -g @uipath/cli`. See [`uipath-cli.md`](uipath-cli.md). |
| PowerShell: "running scripts is disabled" when you run `uip` | Run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, or type `uip.cmd`. |
| Kiro says "out of credits" | The 50 free credits reset monthly. Use the reference files in the repo. |

More fixes: [`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md).

> Plans and screens for GitHub, Google, Groq and UiPath change often. These details were
> checked in October 2026; if a screen looks different, follow the official page.
