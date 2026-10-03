# Project 3 — Expert: Agentic Layer with Kiro

## What you'll build

The agentic layer on top of Orchestrator. You'll use **Kiro** (AWS's spec-driven,
agentic IDE on Amazon Bedrock) to describe a **watcher agent** in plain English, and
you'll run a self-contained Python watcher that reads an Orchestrator job log and
decides, per job, whether to **retry**, **escalate**, or **stop**. That's the judgment
call that used to be a human watching a dashboard.

This tier is the clearest payoff of Hour 1's thesis: StudioX did the recording, Studio
+ Orchestrator does the running, the agent does the judging.

## Prerequisites

- A completed [advanced tier](../advanced/orchestrator_setup_guide.md) (Orchestrator +
  a queue with retry/escalate).
- An **AWS Educate** account and **Kiro** installed. See
  [`00-prerequisites/README.md`](../../00-prerequisites/README.md) steps 5-6.
- Python 3.11+ (the watcher itself needs **no network and no API key**).

## Step-by-step setup

1. **Read the spec.** Open [`kiro-specs/watcher-agent.spec.md`](kiro-specs/watcher-agent.spec.md).
   This is the natural-language description of the agent — the kind of spec you author
   in Kiro.

   > _Screenshot placeholder: the Kiro spec editor with the watcher spec open._
2. **Run the watcher locally** against the committed sample log (no network needed):
   ```bash
   cd 03-studiox-to-agentic-rpa/expert
   python watcher_agent.py
   ```
   It reads [`sample_orchestrator_log.json`](sample_orchestrator_log.json) and prints a
   retry/escalate/stop decision (with a reason) for each job, plus a summary.
3. **Point it at your own log** (optional):
   ```bash
   python watcher_agent.py path/to/your_log.json
   ```
4. **In Kiro:** use the spec to generate or extend the agent — for example, swap the
   file read for a live Orchestrator **Jobs API** call, or host the watcher on a small
   AWS instance so it runs on a schedule.

### Expected output (verbatim from the sample log)

```
Watcher agent — evaluating 5 job(s) from sample_orchestrator_log.json

  [RETRY   ] J-1001 (InvoiceExtraction)
             reason: Transient application error; 2 retry attempt(s) remaining.
  [ESCALATE] J-1002 (InvoiceExtraction)
             reason: Application error persisted after all retries were exhausted; escalate to a human.
  [ESCALATE] J-1003 (InvoiceExtraction)
             reason: Business exception (bad data) — a human must correct it; retrying cannot help.
  [STOP    ] J-1004 (InvoiceExtraction)
             reason: Job completed successfully; no action needed.
  [RETRY   ] J-1005 (InvoiceExtraction)
             reason: Transient application error; 1 retry attempt(s) remaining.

Summary:
  RETRY:    2
  ESCALATE: 2
  STOP:     1
```

## Common errors and fixes

- **"Could not read the log: Log file not found"** — Run from this `expert/` folder, or
  pass the full path to the JSON file.
- **"Log file is not valid JSON"** — Your custom log has a syntax error. Validate it,
  or compare against `sample_orchestrator_log.json`.
- **Kiro can't reach Bedrock** — Confirm you're signed in with the AWS account from the
  prerequisites and that your region has Bedrock access.
- **Watcher makes a "wrong" call** — The rules are deliberately simple and auditable;
  tune them in `decide()` and update the spec to match.
