# Project 3 — Expert: a watcher agent for the PhoneDeals bot

## What you'll build

Every morning someone opens Orchestrator, looks at the bot's failed jobs and decides what
to do. You replace that person with an **agent** that you build with **Kiro**:

| Loop step | What the watcher does |
| --------- | --------------------- |
| **LOOK** | Reads the PhoneDeals job log (a saved file, or live with `uip or jobs list`) |
| **THINK** | Decides per job: **RETRY**, **ESCALATE** or **STOP**, with a plain-English reason |
| **ACT** | Reruns RETRY jobs with `uip or jobs start`, but only after a person types **y** |
| **CHECK** | Asks a free AI model (Gemini) for a short **morning report** for the team |

Then you go one step further: you connect **Kiro itself** to UiPath through the UiPath
CLI's **MCP server**, so you can ask Kiro in plain English about your bot's jobs.

Time: about **75 minutes**. Kiro free tier: about **6 prompts**.

## Prerequisites

- A finished [advanced level](../advanced/README.md), with `my_jobs.json` saved.
  (No Orchestrator? Use the sample log in this folder; everything except the live steps works.)
- **Kiro** and the **UiPath CLI** (`uip login status` shows your tenant).
- **Python 3.11+**, plus `openai` and `python-dotenv` for the report
  ([`requirements.txt`](../../00-prerequisites/requirements.txt)).
- The free **Gemini key** from Projects 1 and 2 in a `.env` file —
  [`00-prerequisites/free-ai-api-key.md`](../../00-prerequisites/free-ai-api-key.md).

## The decision rules

From [`kiro-specs/watcher-agent.spec.md`](kiro-specs/watcher-agent.spec.md):

| The job… | Decision | Why |
| -------- | -------- | --- |
| succeeded | **STOP** | Nothing to do |
| hit a **robot check (CAPTCHA)** | **ESCALATE** | The site wants a human. Never retry it, never bypass it |
| failed with a **business exception** (no phones, bad input) | **ESCALATE** | Bad data never fixes itself |
| failed with an **application exception**, retries left | **RETRY** | Probably a glitch: slow page, file open in Excel |
| failed with an application exception, **no retries left** | **ESCALATE** | Give up and tell a person |
| anything else | **ESCALATE** | When unsure, ask a person |

---

## Step-by-step setup

### Step 1 — Kiro builds the watcher from the spec

1. Create `C:\PhoneDeals\watcher` and open it in Kiro.
2. Copy [`kiro-specs/watcher-agent.spec.md`](kiro-specs/watcher-agent.spec.md) and
   [`sample_orchestrator_log.json`](sample_orchestrator_log.json) into it.

**Prompt E1 (Kiro, Spec mode)**

```text
Create a spec called "watcher-agent" from watcher-agent.spec.md in this folder.
Then implement it as watcher_agent.py (Python 3.11, standard library only for the core)
that reads sample_orchestrator_log.json, decides RETRY / ESCALATE / STOP for each job
with a plain-English reason, and prints a summary. Put the rules in one pure function
decide(job) so they are easy to test, and write test_watcher_agent.py with plain asserts
for every rule, including the CAPTCHA rule. Run the tests and the script.
```

Expected output on the sample log:

```text
Watcher agent — evaluating 5 job(s) from sample_orchestrator_log.json

  [RETRY   ] J-2001 (PhoneDeals)
             reason: Transient application error; 2 retry attempt(s) remaining.
  [ESCALATE] J-2002 (PhoneDeals)
             reason: Application error persisted after all retries were exhausted; escalate to a human.
  [ESCALATE] J-2003 (PhoneDeals)
             reason: The website asked for human verification (CAPTCHA). Never bypass it; a person decides whether to try later.
  [STOP    ] J-2004 (PhoneDeals)
             reason: Job completed successfully; no action needed.
  [RETRY   ] J-2005 (PhoneDeals)
             reason: Transient application error; 1 retry attempt(s) remaining.

Summary:
  RETRY:    2
  ESCALATE: 2
  STOP:     1
```

Reference solution: [`watcher_agent.py`](watcher_agent.py) and
[`test_watcher_agent.py`](test_watcher_agent.py) in this folder.

### Step 2 — LOOK at your real jobs

The UiPath CLI's job list has its own field names (`State`, `Info`, …), not the ones in
the sample log. That is a perfect small job for Kiro:

**Prompt E2 (Kiro, Vibe mode)**

```text
Copy my_jobs.json from the advanced level into this folder. It is the output of
"uip or jobs list --folder-path Shared --process-name PhoneDeals --all-fields".
Add a function that converts it into the same format as sample_orchestrator_log.json
(job_id, process, state, attempt, max_retries, exception_type, error_message), using the
real field names you find in the file. Business exceptions and robot checks must map to
exception_type "BusinessException"; other failures to "ApplicationException". Use
max_retries 3. Then run: python watcher_agent.py my_jobs.json
```

Now the watcher's decisions are about **your** bot's real failures.

### Step 3 — ACT, with a person in the loop

1. Get the process key: `uip or processes list --folder-path "Shared"` and put it in
   `.env` as `UIPATH_PROCESS_KEY=<key>` (a key is not a password, but keep it out of chat
   anyway).
2. Run:

   ```powershell
   python watcher_agent.py my_jobs.json --act
   ```

   For each RETRY job it asks `rerun PhoneDeals for J-2001? [y/N]` and only then runs
   `uip or jobs start <key> --wait-for-completion`. ESCALATE jobs are **never** rerun.
   Without the CLI or the key, it shows the command it *would* run (a safe dry run).

> This is **human-in-the-loop**: the agent proposes, a person approves anything that
> changes the real world. A real company would add a daily limit too (for example, at most
> 3 automatic reruns a day), so the agent can never hammer the website.

### Step 4 — CHECK: the AI morning report

```powershell
python watcher_agent.py my_jobs.json --report --dry-run   # see the prompt first
python watcher_agent.py my_jobs.json --report             # Gemini writes morning_report.md
```

The AI only *writes* the report. The decisions come from the rules, which you can read and
test. That is the safe way to add an LLM: let it summarize, not decide risky things.

**Prompt E3 (Kiro, Vibe mode, optional)**

```text
Improve the morning report: also read PhonesUnder20K.xlsx (sheet "Phones") if it exists
and add the 3 cheapest phones to the AI's data. Keep --dry-run working.
```

### Step 5 — Connect Kiro to UiPath (MCP)

The UiPath CLI can run as an **MCP server**, so an AI agent such as Kiro can use your
Orchestrator as a tool.

1. In Kiro: **Ctrl+Shift+P → "Kiro: Open workspace MCP config (JSON)"** and paste:

   ```json
   {
     "mcpServers": {
       "uipath": {
         "command": "uip",
         "args": ["mcp", "serve"]
       }
     }
   }
   ```

   Save. The server needs you to be logged in (`uip login`) first.
2. **Prompt E4 (Kiro, Vibe mode)**

   ```text
   Using the uipath MCP tool, list the PhoneDeals jobs in folder Shared from today.
   For each faulted one, say what failed and what the watcher rules would decide.
   Do not start, stop or change anything.
   ```

Kiro now runs `uip` commands itself (it asks you before each one). Notice the last line of
the prompt: **you** set the limits of what the agent may do.

## Done when

- `python test_watcher_agent.py` prints **All watcher checks passed.**
- `python watcher_agent.py my_jobs.json` gives a decision and a reason for each of your
  real jobs.
- `--act` reruns a RETRY job only after you type **y**, and the job ends Successful.
- `morning_report.md` exists and matches the decisions.
- Kiro answers Prompt E4 using the uipath MCP server.

## Common errors and fixes

| You see | Fix |
| ------- | --- |
| "Could not read the log: Log file not found" | Run from the folder with the JSON file, or pass the full path. |
| "Log file is not valid JSON" | `my_jobs.json` also caught a warning line. Run the `uip or jobs list` command again, or ask Kiro to clean the file. |
| Every job says "Unrecognized state" | The converter (Step 2) didn't map the field names. Show Kiro one job from `my_jobs.json`. |
| `--act` only prints a dry run | Install the CLI, run `uip login`, and set `UIPATH_PROCESS_KEY` in `.env`. |
| `GEMINI_API_KEY is not set` | Put the key in `.env` next to the script or in the repo root (same key as Projects 1–2). |
| Kiro doesn't show the uipath MCP server | Check the JSON, save the file, and make sure `uip --version` works in a new terminal. Search Settings for "MCP" and make sure MCP is enabled. |
| The watcher "made a wrong call" | The rules are deliberately simple. Change `decide()`, update the spec to match, and add a test first. |
