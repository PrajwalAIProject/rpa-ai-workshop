# 00 — Prerequisites

Set this up **before** the workshop. Doing it live eats into lab time, so arrive with
the checklist below ticked.

This folder is an index. Each setup task has its own short guide:

- [`python-setup.md`](python-setup.md) — Python 3.11+ (and an optional virtual environment)
- [`git-and-editor.md`](git-and-editor.md) — **GitHub account, VS Code, Git and GitHub Copilot** (the AI that writes the Project 1 code with you)
- [`free-ai-api-key.md`](free-ai-api-key.md) — a **free** Gemini (or Groq) API key for the Project 1 expert AI report, with no card needed
- [`uipath-cloud.md`](uipath-cloud.md) — UiPath Automation Cloud (Community), Project 3
- [`api-keys.md`](api-keys.md) — Anthropic API key, Project 2 expert
- [`kiro-install.md`](kiro-install.md) and [`aws-free-tier.md`](aws-free-tier.md) — Project 3 expert only (optional)

> **Heads-up:** GitHub, Google and Groq change their plans and screens often. Every
> fact below was checked in October 2026; **confirm current details on the official
> pages linked in each guide before the session.**

---

## Project 1 in one picture

_Project 1 (stock market analyzer) needs Python, VS Code and a GitHub account with
Copilot. The expert level adds one free AI API key._

```mermaid
flowchart TD
    A[Install Python 3.11+] --> B[GitHub account + VS Code + Git]
    B --> C[Sign in to GitHub in VS Code, turn on Copilot - Agent mode]
    C --> D[Basic: company name to stock info]
    D --> E[Advanced: full trend with web scraping]
    E --> F{Doing the expert level?}
    F -->|No| G[Done]
    F -->|Yes| H[Get a free Gemini API key - no card]
    H --> I[Expert: AI-written stock report]
```

---

## Checklist

**Everyone:**

- [ ] **Python 3.11 or newer** installed and on your PATH: `python --version` works.
      See [`python-setup.md`](python-setup.md).
- [ ] A **GitHub account**. Students: also apply for **GitHub Education** (Copilot
      Student). It can take 1–3 days. See [`git-and-editor.md`](git-and-editor.md).
- [ ] **VS Code** and **Git** installed, VS Code **signed in to GitHub**, and
      **Copilot Chat** working in **Agent** mode (the `hello.py` test in
      [`git-and-editor.md`](git-and-editor.md) passes).
- [ ] An empty project folder, e.g. `C:\stock-project`, opened in VS Code.

**Project 1 expert (AI report):**

- [ ] A free **Gemini API key** (or Groq) in a `.env` file in your project folder. See
      [`free-ai-api-key.md`](free-ai-api-key.md).

**Project 2 expert:** an Anthropic API key, see [`api-keys.md`](api-keys.md).

**Project 3:** a free **UiPath Automation Cloud (Community)** account, see
[`uipath-cloud.md`](uipath-cloud.md).

---

## Which tool does each project need?

| Project / level | Python | VS Code + GitHub Copilot | Free AI key (Gemini/Groq) | UiPath Cloud | Anthropic key |
| --------------- | :----: | :----------------------: | :-----------------------: | :----------: | :-----------: |
| **1** Stock — basic | ✅ | ✅ | — | — | — |
| **1** Stock — advanced (web scraping) | ✅ | ✅ | — | — | — |
| **1** Stock — expert (AI report) | ✅ | ✅ | ✅ | — | — |
| **2** News — basic / advanced | ✅ | ✅ | — | — | — |
| **2** News — expert | ✅ | ✅ | — | — | ✅ |
| **3** RPA — basic / advanced | ✅ | — | — | ✅ | — |
| **3** RPA — expert (agentic) | ✅ | — | — | ✅ | — |

**No AWS account and no credit card are needed for Project 1.**

**Python packages:** in Project 1, Copilot installs what each script needs (it runs
`pip install ...` and asks you first). To install everything up front instead, run
`pip install -r 00-prerequisites/requirements.txt`; see [`python-setup.md`](python-setup.md).

---

## Order to do it in

1. [Python](python-setup.md)
2. [GitHub account → VS Code → Git → Copilot](git-and-editor.md) (apply for GitHub Education early)
3. [Free AI API key](free-ai-api-key.md), for the Project 1 expert level
4. [UiPath Cloud](uipath-cloud.md) (Project 3), [Anthropic key](api-keys.md) (Project 2 expert)

Secrets (the Gemini/Groq key, the Anthropic key, SMTP passwords) go **only** in a local
`.env` file, which is git-ignored. Copy [`.env.example`](../.env.example) to `.env` and
fill in your own values. **Never commit real keys and never paste them into Copilot Chat.**
