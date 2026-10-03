# AI & RPA Workshop

Starter code and guided labs for a hands-on AI + RPA workshop aimed at final-year
engineering students who already know UiPath **StudioX** from BCG701. The workshop
climbs from StudioX into professional UiPath Studio, cloud Orchestrator, Python +
cloud scheduling, and an agentic AI layer on top.

Three projects, three tiers each (**basic → advanced → expert**). Nobody has to hit
"expert" on all three — depth over breadth.

## The three projects

| # | Project | What it teaches |
| - | ------- | --------------- |
| 1 | [Stock Market Analyzer](01-stock-market-analyzer/) | Python, external APIs, pandas/matplotlib, SQLite, an LLM commentary step, GitHub Actions scheduling |
| 2 | [Morning News Digest](02-morning-news-digest/) | RSS parsing, categorization, markdown/HTML rendering, an LLM "what matters" step, email delivery |
| 3 | [StudioX to Agentic RPA](03-studiox-to-agentic-rpa/) | Professional Studio, Orchestrator, queues & retry/escalate, Kiro specs, a runnable watcher agent |

Each project folder has `basic/`, `advanced/`, and `expert/` subfolders. Every tier
has its own README following the same four-part shape:

1. **What you'll build**
2. **Prerequisites**
3. **Step-by-step setup** (with screenshot placeholders where relevant)
4. **Common errors and fixes**

## How to use this repo

1. Start with [`00-prerequisites/`](00-prerequisites/) — install Python, create your
   UiPath Automation Cloud and AWS Educate accounts, and install Kiro.
2. Pick a project and open its `basic/` README. Work up through the tiers.
3. The Python tiers all share one dependency list:
   [`00-prerequisites/requirements.txt`](00-prerequisites/requirements.txt).

## Prerequisites

See [`00-prerequisites/README.md`](00-prerequisites/README.md) for the full,
numbered setup (Python 3.11+, UiPath Automation Cloud Community, AWS Educate, Kiro).

## Secrets

API keys and other secrets live only in a local `.env` file, which is git-ignored.
Copy [`.env.example`](.env.example) to `.env` and fill in your own values. Never
commit real keys.

## Slides

The workshop deck PDF lands in [`slides/`](slides/) in a later phase.
