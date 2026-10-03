# AI & RPA Workshop

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Companion code and guided labs for a hands-on, 5-hour **AI & RPA workshop** aimed at
final-year engineering students who already know UiPath **StudioX** from BCG701. The
workshop starts where that syllabus stops and climbs the automation ladder: from the
StudioX desktop canvas into professional UiPath Studio, cloud Orchestrator, Python with
cloud scheduling, and finally an **agentic AI** layer authored with Kiro.

Three projects, three tiers each (**basic → advanced → expert**). Nobody has to hit
"expert" on all three — depth over breadth.

## Who this is for

- **Students** working through the labs — start at [Start here](#start-here).
- **Facilitators** running the session — see [`docs/facilitator-guide.md`](docs/facilitator-guide.md).
- **Faculty** checking how this extends BCG701 — see [`docs/course-alignment.md`](docs/course-alignment.md).
- **Contributors** improving the repo — see [`CONTRIBUTING.md`](CONTRIBUTING.md).

## The learning ladder

```
StudioX  →  UiPath Studio  →  Orchestrator  →  Agentic AI (Kiro)
(desktop,    (professional     (scheduled,       (plain-English specs,
 citizen      IDE: variables,   unattended,       a watcher agent that
 developer)   arguments,        queues, retry/    decides retry / escalate
              reusable flows)   escalate)         / stop)
```

StudioX did the recording, Studio and Orchestrator do the running, and the agent does
the judging. Projects 1 and 2 add the Python, external-API, and cloud-scheduling skills
that sit alongside that ladder.

## Start here

1. Set up your tools once, before the session — see
   [`00-prerequisites/README.md`](00-prerequisites/README.md). It walks you through
   Python 3.11+, a UiPath Automation Cloud (Community) account, an Anthropic API key,
   Kiro, and (only if you host the Project 3 expert watcher on AWS) an AWS account.
2. Pick a project below and open its `basic/` README. Work up through the tiers.
3. All Python tiers share one dependency list:
   [`00-prerequisites/requirements.txt`](00-prerequisites/requirements.txt).

> **Heads-up:** AWS, Kiro, and UiPath change their terms, pricing, and screens often —
> confirm current details on the official pages before the session.

## The three projects

| # | Project | Overview | What it teaches |
| - | ------- | -------- | --------------- |
| 1 | Stock Market Analyzer | [`01-stock-market-analyzer/README.md`](01-stock-market-analyzer/README.md) | Python, external APIs, pandas/matplotlib, SQLite, an LLM commentary step, GitHub Actions scheduling |
| 2 | Morning News Digest | [`02-morning-news-digest/README.md`](02-morning-news-digest/README.md) | RSS parsing, categorization, markdown/HTML rendering, an LLM "what matters" step, email delivery |
| 3 | StudioX to Agentic RPA | [`03-studiox-to-agentic-rpa/README.md`](03-studiox-to-agentic-rpa/README.md) | Professional Studio, Orchestrator, queues and retry/escalate, Kiro specs, a runnable watcher agent |

Each project overview summarizes the basic → advanced → expert progression and links
every tier README. Each tier README follows the same four-part shape: **What you'll
build → Prerequisites → Step-by-step setup → Common errors and fixes.**

## Prerequisites in brief

Everyone needs Python and Git plus an editor. UiPath Automation Cloud (Community) is for
Project 3. The expert AI steps in Projects 1 and 2 need an Anthropic API key. Project 3
expert needs **Kiro** — and **Kiro does not require an AWS account** (sign in with
GitHub, Google, an AWS Builder ID, or AWS IAM Identity Center). You only need an **AWS
account** if you choose to host the Project 3 expert watcher on AWS, and in that case a
**card-free path** (AWS Student Rewards or AWS Educate) is the recommended option for a
classroom — see [`00-prerequisites/aws-free-tier.md`](00-prerequisites/aws-free-tier.md).

The full checklist, decision tree, and per-tool matrix live in
[`00-prerequisites/README.md`](00-prerequisites/README.md).

## Repo map

```
rpa-ai-workshop/
├── README.md                     ← you are here
├── GLOSSARY.md                   ← plain-English definitions of the key terms
├── TROUBLESHOOTING.md            ← consolidated FAQ across setup and projects
├── CONTRIBUTING.md               ← how to contribute
├── CODE_OF_CONDUCT.md            ← community expectations
├── LICENSE                       ← MIT
├── docs/
│   ├── facilitator-guide.md      ← practical instructor guide
│   └── course-alignment.md       ← BCG701 CO-1..CO-5 mapping
├── 00-prerequisites/             ← setup index + focused per-tool guides
├── 01-stock-market-analyzer/     ← basic / advanced / expert
├── 02-morning-news-digest/       ← basic / advanced / expert
├── 03-studiox-to-agentic-rpa/    ← basic / advanced / expert
└── slides/                       ← workshop deck (added later)
```

## More documentation

- [`GLOSSARY.md`](GLOSSARY.md) — plain-English definitions for the terms used across the labs.
- [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) — consolidated fixes for Python, API keys, network, AWS, Kiro, and UiPath.
- [`docs/facilitator-guide.md`](docs/facilitator-guide.md) — running the room: rotation vs deep-dive, timing, pre-session checklist.
- [`docs/course-alignment.md`](docs/course-alignment.md) — how the session extends BCG701 Course Outcomes.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — fork, branch, and PR flow, plus where screenshots go.
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) — the behavior expected of everyone taking part.

## Secrets

API keys and other secrets live only in a local `.env` file, which is git-ignored. Copy
[`.env.example`](.env.example) to `.env` and fill in your own values. **Never commit real
keys.**

## Slides

The workshop deck PDF lands in [`slides/`](slides/) in a later phase.

## Credits and license

Workshop and materials by **Prajwal Gowda H M**. Released under the MIT License — see
[`LICENSE`](LICENSE).
