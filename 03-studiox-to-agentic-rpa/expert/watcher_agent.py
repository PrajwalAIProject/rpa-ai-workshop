"""Project 3 — Expert: a runnable "watcher" agent for Orchestrator job logs.

This is the agentic layer from Hour 1's thesis: StudioX did the recording, Studio +
Orchestrator does the running, and this agent does the JUDGING. Instead of a human
staring at an Orchestrator dashboard, the agent reads the job log and decides, per
job, whether to RETRY, ESCALATE, or STOP.

It is deliberately self-contained: it reads a LOCAL sample JSON log (standing in for
a real Orchestrator API response) so it runs with NO network and NO credentials. In
production you would swap read_log() for a call to the Orchestrator Jobs API.

Decision rules (simple, auditable — the point is the judgment, not cleverness):
  * Successful job                       -> STOP  (nothing to do)
  * BusinessException (bad data)         -> ESCALATE (a human must fix the data;
                                            retrying will never help)
  * ApplicationException, attempts left  -> RETRY (likely transient: timeout, lock)
  * ApplicationException, retries used up -> ESCALATE (give up automatically, alert
                                            a human)
  * Anything unrecognized                -> ESCALATE (fail safe toward a human)

Run it:
    python watcher_agent.py                         # uses sample_orchestrator_log.json
    python watcher_agent.py path/to/other_log.json  # or point at another log
"""

import json
import sys
from pathlib import Path

DEFAULT_LOG = Path(__file__).with_name("sample_orchestrator_log.json")

# Decision constants, so a typo becomes an error rather than a silent wrong branch.
RETRY = "RETRY"
ESCALATE = "ESCALATE"
STOP = "STOP"


def read_log(path: Path) -> dict:
    """Load the Orchestrator job log from a JSON file.

    Raises FileNotFoundError or ValueError (on bad JSON) with a clear message so the
    caller can report it cleanly instead of dumping a traceback.
    """
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
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
            }
        )
    return decisions


def main() -> int:
    log_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_LOG

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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
