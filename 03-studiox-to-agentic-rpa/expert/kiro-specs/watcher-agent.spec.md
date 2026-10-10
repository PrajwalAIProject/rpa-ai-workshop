# Spec: PhoneDeals watcher agent

> An example **Kiro spec**: a plain-English description of what the agent must do. In
> Kiro you start a spec from text like this (Prompt E1), and Kiro turns it into
> requirements, a design and tasks, then writes the code. `watcher_agent.py` in this
> folder is the reference result.

## Intent

Replace the person who checks the PhoneDeals bot's jobs in UiPath Orchestrator every
morning. The agent reads the job log and decides, for each job, whether to **retry**,
**escalate** to a person, or **stop** (nothing to do), and explains every decision.

## Inputs

- A job log in JSON. During the workshop: `sample_orchestrator_log.json`, or your own
  jobs from `uip or jobs list --folder-path Shared --process-name PhoneDeals --all-fields`
  converted to the same format. Each job has: `job_id`, `process`, `state`, `attempt`,
  `max_retries`, `exception_type`, `error_message`, and optionally `output`.

## Decision rules (in this order)

1. The job **succeeded** → **STOP**.
2. The error mentions a **robot check** or **CAPTCHA** → **ESCALATE**. Never retry it and
   never try to get around it.
3. **BusinessException** (no phones found, bad input) → **ESCALATE**; retrying never helps.
4. **ApplicationException** with **attempts left** (`attempt < max_retries`) → **RETRY**.
5. **ApplicationException** with **no attempts left** → **ESCALATE**.
6. Anything **unrecognized** → **ESCALATE** (fail safe toward a person).

## Actions

- `--act`: for each RETRY job, ask the person "rerun? [y/N]" and only on **y** run
  `uip or jobs start <process key> --wait-for-completion`. The process key comes from
  `UIPATH_PROCESS_KEY` in `.env`. Without the CLI or the key, print the command instead.
  ESCALATE and STOP jobs are never rerun.
- `--report`: send the decisions to a free AI model (Gemini by default, Groq as backup,
  key in `.env`) and save a short morning report as `morning_report.md`.
  `--report --dry-run` prints the prompt without calling the AI.

## Constraints

- The decisions come from the rules above, never from the AI. The AI only writes the report.
- Every decision has a plain-English reason (auditable).
- The core runs with no network and no credentials on the sample log.
- No passwords, keys or secrets in code or in chat.

## Tests

- One assert per rule, including the CAPTCHA rule, and one test that the sample log gives
  RETRY, ESCALATE, ESCALATE, STOP, RETRY.

## Stretch ideas

- A daily limit on automatic reruns (for example, 3 a day).
- Send ESCALATE jobs to email or Teams instead of printing them.
- Run the watcher every morning at 09:30, after the 09:00 bot run.
