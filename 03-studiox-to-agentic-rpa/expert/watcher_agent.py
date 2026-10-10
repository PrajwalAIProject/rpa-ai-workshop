"""Project 3 - Expert: a watcher agent for the PhoneDeals bot's Orchestrator jobs.

Reference solution. In the workshop you build this with Kiro from the spec in
kiro-specs/watcher-agent.spec.md (see README.md for the prompts); compare with this
file if yours misbehaves.

The agent goes round the same loop as every agent:
  LOOK   read the bot's job log (a saved file, or `uip or jobs list ... --output json`)
  THINK  decide per job: RETRY, ESCALATE or STOP, with a plain-English reason
  ACT    --act: rerun the job with the UiPath CLI, after a person says yes
  CHECK  --report: a free AI model writes a short morning report for the team

Decision rules (simple and auditable; the point is the judgment, not cleverness):
  * Successful job                          -> STOP     (nothing to do)
  * Website showed a robot check / CAPTCHA  -> ESCALATE (never retry it, never bypass it)
  * BusinessException (bad or missing data) -> ESCALATE (retrying cannot help)
  * ApplicationException, attempts left     -> RETRY    (likely transient: timeout, locked file)
  * ApplicationException, retries used up   -> ESCALATE (give up, tell a person)
  * Anything unrecognized                   -> ESCALATE (fail safe toward a person)

Run it:
    python watcher_agent.py                          # decisions for sample_orchestrator_log.json
    python watcher_agent.py my_jobs.json             # or another log in the same format
    python watcher_agent.py --act                    # also offer to rerun RETRY jobs (asks first)
    python watcher_agent.py --report                 # also write morning_report.md with free AI
    python watcher_agent.py --report --dry-run       # show the AI prompt, don't call the AI

--act needs the UiPath CLI (00-prerequisites/uipath-cli.md), `uip login`, and the
process key in .env:  UIPATH_PROCESS_KEY=<key from `uip or processes list --folder-path Shared`>
--report needs the free Gemini (or Groq) key in .env, the same one as Projects 1 and 2.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_LOG = HERE / "sample_orchestrator_log.json"

# Decision constants, so a typo becomes an error rather than a silent wrong branch.
RETRY = "RETRY"
ESCALATE = "ESCALATE"
STOP = "STOP"


def read_log(path: Path) -> dict:
    """Load the job log from a JSON file.

    Raises FileNotFoundError or ValueError (on bad JSON) with a clear message so the
    caller can report it cleanly instead of dumping a traceback.
    """
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Log file is not valid JSON: {exc}") from exc


def decide(job: dict) -> tuple[str, str]:
    """Return (action, reason) for a single job entry.

    Pure function: no I/O, easy to test. ``action`` is one of RETRY/ESCALATE/STOP.
    """
    state = job.get("state")
    exception_type = job.get("exception_type")
    attempt = job.get("attempt", 0)
    max_retries = job.get("max_retries", 0)

    if state == "Successful":
        return STOP, "Job completed successfully; no action needed."

    # A robot check means the website wants a human. Never retry it automatically and
    # never try to get around it: a person decides what to do.
    message = (job.get("error_message") or "").lower()
    if "captcha" in message or "robot check" in message:
        return ESCALATE, "The website asked for human verification (CAPTCHA). Never bypass it; a person decides whether to try later."

    if exception_type == "BusinessException":
        return ESCALATE, "Business exception (bad data) — a human must correct it; retrying cannot help."

    if exception_type == "ApplicationException":
        if attempt < max_retries:
            remaining = max_retries - attempt
            return RETRY, f"Transient application error; {remaining} retry attempt(s) remaining."
        return ESCALATE, "Application error persisted after all retries were exhausted; escalate to a human."

    # Unknown / unexpected state: fail safe toward a human.
    return ESCALATE, f"Unrecognized state '{state}' / exception '{exception_type}'; escalating to be safe."


def evaluate_log(log: dict) -> list[dict]:
    """Run decide() over every job and return a list of decision records."""
    decisions = []
    for job in log.get("jobs", []):
        action, reason = decide(job)
        decisions.append(
            {
                "job_id": job.get("job_id", "(unknown)"),
                "process": job.get("process", "(unknown)"),
                "action": action,
                "reason": reason,
                "error": job.get("error_message"),
                "output": job.get("output"),
            }
        )
    return decisions


def act_on_retries(decisions: list[dict]) -> None:
    """ACT: rerun each RETRY job with the UiPath CLI, but only after a person types y."""
    retries = [d for d in decisions if d["action"] == RETRY]
    if not retries:
        print("\nACT: nothing to retry.")
        return
    key = os.getenv("UIPATH_PROCESS_KEY", "").strip()
    command = ["uip", "or", "jobs", "start", key or "<UIPATH_PROCESS_KEY>", "--wait-for-completion"]
    if not shutil.which("uip") or not key:
        print("\nACT (dry run): would run, once per RETRY job:\n  " + " ".join(command))
        print("  To really run it: install the UiPath CLI, run `uip login`, and put "
              "UIPATH_PROCESS_KEY=<key> in .env (see README).")
        return
    for d in retries:
        answer = input(f"\nACT: rerun {d['process']} for {d['job_id']}? [y/N] ").strip().lower()
        if answer != "y":
            print("  Skipped: a person said no.")
            continue
        print("  Running: " + " ".join(command))
        # uip is a .cmd launcher on Windows, so let the shell find it
        result = subprocess.run(command, capture_output=True, text=True, shell=(os.name == "nt"))
        print("  " + (result.stdout or result.stderr).strip().replace("\n", "\n  ")[:800])


REPORT_INSTRUCTIONS = """You are the assistant of a small RPA team in India.
Below are last night's decisions from a watcher agent that monitors a UiPath bot called
PhoneDeals (it lists smartphones under 20,000 rupees from amazon.in into Excel).
Write a morning report in simple English, under 120 words, with exactly these parts:
1. One-line status (how many jobs ran, how many need a person).
2. "Needs a person:" one bullet per ESCALATE job: job id and what the person should do.
3. "Handled by the agent:" one line about the RETRY and STOP jobs.
4. "Phones:" if a successful job has output, one line with how many phones and the cheapest.
Use ONLY the data below. Do not invent numbers. Never suggest bypassing a CAPTCHA.

DATA (JSON):
"""


def write_report(decisions: list[dict], dry_run: bool) -> int:
    """CHECK / report: ask a free AI model (Gemini or Groq) for a short morning report."""
    prompt = REPORT_INSTRUCTIONS + json.dumps(decisions, ensure_ascii=False, indent=1)
    if dry_run:
        print("\n--- AI prompt (dry run, not sent) ---\n" + prompt)
        return 0

    from dotenv import load_dotenv
    from openai import APIConnectionError, APIStatusError, OpenAI

    load_dotenv(HERE / ".env")
    load_dotenv(HERE.parent.parent / ".env")  # repo-root .env, if you keep it there
    providers = {  # provider -> (API address, name of the key in .env, default model)
        "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai/", "GEMINI_API_KEY", "gemini-flash-latest"),
        "groq": ("https://api.groq.com/openai/v1", "GROQ_API_KEY", "openai/gpt-oss-20b"),
    }
    provider = os.getenv("LLM_PROVIDER", "gemini").strip().lower()
    if provider not in providers:
        print(f"LLM_PROVIDER must be one of {', '.join(providers)} (got '{provider}').")
        return 1
    base_url, key_name, model = providers[provider]
    model = os.getenv("LLM_MODEL") or model
    api_key = os.getenv(key_name)
    if not api_key:
        print(f"{key_name} is not set. Put {key_name}=<your key> in .env (see 00-prerequisites/free-ai-api-key.md).")
        return 1

    print(f"\nAsking the AI for the morning report ({provider}, {model})...")
    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        reply = client.chat.completions.create(model=model, temperature=0.2,
                                               messages=[{"role": "user", "content": prompt}])
    except APIStatusError as error:
        hint = "Check the key in .env." if error.status_code in (400, 401, 403) else \
               "Free-tier limit reached; wait a minute." if error.status_code == 429 else \
               "Remove LLM_MODEL from .env to use the default." if error.status_code == 404 else ""
        print(f"AI error {error.status_code}: {str(error)[:200]} {hint}")
        return 1
    except APIConnectionError as error:
        print(f"Could not reach the AI service: {error}. Check your internet connection.")
        return 1

    report = reply.choices[0].message.content.strip()
    print("\n" + "=" * 60 + "\n  MORNING REPORT · PhoneDeals bot\n" + "=" * 60 + "\n" + report)
    (HERE / "morning_report.md").write_text(f"# Morning report: PhoneDeals bot\n\n_Written by {provider} / {model}_\n\n{report}\n",
                                            encoding="utf-8")
    print("\nSaved: morning_report.md")
    return 0


def main() -> int:
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    log_path = Path(paths[0]) if paths else DEFAULT_LOG

    try:
        log = read_log(log_path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Could not read the log: {exc}")
        return 1

    decisions = evaluate_log(log)
    if not decisions:
        print("No jobs found in the log — nothing to evaluate.")
        return 0

    print(f"Watcher agent — evaluating {len(decisions)} job(s) from {log_path.name}\n")
    counts = {RETRY: 0, ESCALATE: 0, STOP: 0}
    for d in decisions:
        counts[d["action"]] = counts.get(d["action"], 0) + 1
        print(f"  [{d['action']:<8}] {d['job_id']} ({d['process']})")
        print(f"             reason: {d['reason']}")

    print("\nSummary:")
    print(f"  RETRY:    {counts.get(RETRY, 0)}")
    print(f"  ESCALATE: {counts.get(ESCALATE, 0)}")
    print(f"  STOP:     {counts.get(STOP, 0)}")

    if "--act" in flags:
        act_on_retries(decisions)
    if "--report" in flags:
        return write_report(decisions, dry_run="--dry-run" in flags)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
