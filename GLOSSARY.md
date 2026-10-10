# Glossary

Plain-English definitions of the terms used across this workshop, in the context you'll
meet them in the labs. One or two sentences each, alphabetized.

### Agentic AI / agent

Software that doesn't just answer a question but takes goal-directed actions — deciding,
calling tools, and reacting to results, with a human supervising rather than clicking
every step. In Project 3 expert, the watcher agent decides whether to retry, escalate, or
stop a job.

### API

Application Programming Interface — a defined way for one program to request data or
actions from another over the network, instead of a human clicking a UI. The labs call
stock, RSS, and LLM APIs.

### API key

A secret string that identifies and authorizes your calls to an API (like the free Gemini
key the expert levels use). Keep it in your local `.env` and never commit it.

### Attended vs unattended robot

An **attended** robot runs on a person's machine, triggered by them, alongside their
work; an **unattended** robot runs on its own, on a schedule or trigger, with no human
present. Project 3 advanced schedules an unattended robot in Orchestrator.

### AWS Free Tier

Amazon Web Services' entry-level access that lets you use certain services for free up to
set limits. For this workshop AWS is optional — only needed if you host the Project 3
expert watcher on AWS; see [`00-prerequisites/aws-free-tier.md`](00-prerequisites/aws-free-tier.md).

### cron

A time-based scheduling format (and the Unix scheduler that reads it) that runs a command
on a repeating schedule, e.g. every morning at 7. Project 1 expert schedules with a
GitHub Actions cron job; Project 2 can use cron or Task Scheduler.

### Death cross

A bearish chart signal where a shorter moving average (20-day) crosses **below** a longer
one (50-day). The opposite of a golden cross.

### `.env`

A local file that holds your secrets (API keys, SMTP passwords) as `KEY=value` lines,
loaded at runtime so secrets stay out of your code. It is git-ignored; copy `.env.example`
to `.env` and fill in your own values.

### Golden cross

A bullish chart signal where a shorter moving average (20-day) crosses **above** a longer
one (50-day). The opposite of a death cross.

### IAM

Identity and Access Management — AWS's system for creating users and scoping exactly what
each can do. Best practice is to work as a scoped IAM user instead of the all-powerful
root account.

### Kiro

An AI agent IDE (it looks like VS Code) that works spec-first: it writes a plan
(requirements, design, tasks) before it builds. Used at every level of Project 3. It does
**not** require an AWS account: sign in with Google, GitHub or an AWS Builder ID; see
[`00-prerequisites/kiro-install.md`](00-prerequisites/kiro-install.md).

### MCP (Model Context Protocol)

An open standard that lets an AI agent use outside tools. In Project 3 expert, the UiPath
CLI runs as an MCP server (`uip mcp serve`) so Kiro can read and start UiPath jobs.

### LLM

Large Language Model — an AI model trained on large amounts of text that generates and
reasons over natural language. The expert levels call an LLM (Google Gemini, or Groq) to write
the stock report and pick the news that matters.

### MFA

Multi-Factor Authentication — a second proof of identity (such as a phone app code) added
on top of your password. Turn it on for your UiPath and AWS accounts.

### Moving average

The average of a value (here, closing price) over a sliding window of recent periods,
used to smooth out noise and spot trends. Project 1 advanced computes 20-day and 50-day
moving averages.

### Orchestrator

UiPath's cloud control plane for publishing, scheduling, running, and monitoring robots,
including unattended runs and queues. Project 3 advanced uses it.

### Queue

In Orchestrator, a list of work items that robots process one by one, with built-in
retry and exception handling. Project 3 advanced adds a queue with a retry-or-escalate
rule.

### RPA

Robotic Process Automation — software "robots" that carry out explicit, pre-defined steps
across applications and screens, the way a person would click through them. It's what
BCG701 teaches in StudioX.

### RSS feed

A standard, machine-readable feed a site publishes so programs can pull its latest items
(headlines, articles) without scraping the page. Project 2 reads RSS feeds with
`feedparser`.

### SMTP

Simple Mail Transfer Protocol — the standard way programs send email. Project 2 expert
can deliver its digest over SMTP (e.g. Gmail with an app password).

### Spec-driven development

Writing a clear, plain-English specification of what you want, then letting an agentic
tool like Kiro generate or modify the implementation from it, instead of hand-wiring
every step. Project 3 expert authors the watcher agent this way.

### SQLite

A lightweight, file-based SQL database that needs no server — just a single `.db` file.
Project 1 advanced persists price history to SQLite.

### StudioX

UiPath's low-code, citizen-developer design canvas for building automations without
writing code — the tool BCG701 covers. This workshop starts above it.

### Token / rate limit

A **token** is a chunk of text an LLM processes (billing and limits are measured in
tokens); a **rate limit** caps how many requests or tokens you can use in a time window.
Hitting a rate limit on the free API tier is a common, temporary error — wait and retry.

### UiPath Studio (Pro)

UiPath's full professional IDE with variables, arguments, and reusable workflows — the
step up from StudioX. Project 3 basic rebuilds a StudioX exercise here.

### Virtual environment

An isolated Python environment (a `.venv/` folder) that keeps a project's dependencies
separate from the rest of your system. Create and activate one before installing the
shared requirements; see [`00-prerequisites/python-setup.md`](00-prerequisites/python-setup.md).

### Webhook

A URL that another service calls automatically when an event happens, so your code is
"pushed" the event instead of polling for it. Project 1 expert can post its commentary to
a Slack or Telegram webhook.
