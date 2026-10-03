# Spec: Orchestrator Watcher Agent

> This is an example **Kiro spec** — a natural-language description of what the agent
> should do. In Kiro you write the behavior in plain English like this, and the
> spec-driven workflow helps generate and refine the implementation
> (`watcher_agent.py` in this folder is the result for the sample-log case).

## Intent

Replace the human who watches the UiPath Orchestrator dashboard. The agent reads the
job log and decides, for each job, whether to **retry**, **escalate** to a person, or
**stop** (nothing to do).

## Inputs

- An Orchestrator job log. During the workshop this is a local JSON file
  (`sample_orchestrator_log.json`); in production it is the Orchestrator **Jobs API**
  response. Each job carries: `job_id`, `process`, `state`, `attempt`, `max_retries`,
  `exception_type`, `error_message`.

## Decision rules

1. If the job **succeeded**, do nothing → **STOP**.
2. If it failed with a **BusinessException** (bad/missing data), a human must fix the
   data; retrying never helps → **ESCALATE**.
3. If it failed with an **ApplicationException** (likely transient: timeout, locked
   file) and **attempts remain**, → **RETRY**.
4. If an **ApplicationException** has **exhausted its retries**, give up automatically
   and alert a human → **ESCALATE**.
5. For any **unrecognized** state, fail safe → **ESCALATE**.

## Output

- A per-job decision (action + human-readable reason) and a summary count of
  RETRY / ESCALATE / STOP.

## Constraints

- Must run standalone against the committed sample log with **no network** and **no
  credentials**.
- Decisions must be **auditable**: every action comes with a plain-English reason.

## Stretch ideas

- Swap the file read for a live Orchestrator Jobs API call.
- Trigger an actual retry via the API, and send escalations to email/Slack.
- Let an LLM summarize the batch of decisions into one morning status line.
