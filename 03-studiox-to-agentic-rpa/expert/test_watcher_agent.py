"""Quick checks for the watcher's decision rules. Run: python test_watcher_agent.py"""

from watcher_agent import ESCALATE, RETRY, STOP, decide, evaluate_log, read_log, DEFAULT_LOG

app = {"state": "Faulted", "exception_type": "ApplicationException", "max_retries": 3}

assert decide({"state": "Successful"})[0] == STOP
assert decide({**app, "attempt": 1})[0] == RETRY
assert decide({**app, "attempt": 3})[0] == ESCALATE                      # retries used up
assert decide({**app, "attempt": 1, "error_message": "Robot check page"})[0] == ESCALATE  # never retry a CAPTCHA
assert decide({"state": "Faulted", "exception_type": "BusinessException"})[0] == ESCALATE
assert decide({"state": "Weird"})[0] == ESCALATE                         # unknown -> a person

actions = [d["action"] for d in evaluate_log(read_log(DEFAULT_LOG))]
assert actions == [RETRY, ESCALATE, ESCALATE, STOP, RETRY], actions
print("All watcher checks passed.")
