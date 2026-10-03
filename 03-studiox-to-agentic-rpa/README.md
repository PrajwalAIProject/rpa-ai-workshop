# Project 3 — From StudioX to Agentic RPA

The centerpiece track. Every tier assumes you already know **StudioX** from BCG701 and
starts past it, climbing the ladder: professional **UiPath Studio**, cloud
**Orchestrator**, and an **agentic AI** layer authored with **Kiro**. StudioX did the
recording, Studio and Orchestrator do the running, and the agent does the judging.

Work up through the tiers. Each tier is a complete, runnable deliverable on its own.

## The three tiers

### Basic — [`basic/README.md`](basic/README.md)

Move from the StudioX citizen-developer canvas into the full **UiPath Studio Pro** IDE by
rebuilding one of your own BCG701 Excel-automation exercises — same logic, but with
variables, arguments, and a reusable workflow structure instead of a flat recording.
**Done** when your Studio workflow runs and produces the correct output workbook.

### Advanced — [`advanced/README.md`](advanced/README.md)

Run the bot the way a company actually runs one. Publish the Studio project to
**Orchestrator**, schedule it **unattended**, add a **queue**, and build a deliberate
failure case with a **retry-or-escalate** rule — the single most interview-relevant RPA
skill there is. The full walkthrough is in
[`advanced/orchestrator_setup_guide.md`](advanced/orchestrator_setup_guide.md). **Done**
when the job runs unattended on a schedule and the queue correctly retries or escalates
the failure case.

### Expert — [`expert/README.md`](expert/README.md)

Add the agentic layer. Use **Kiro** (a spec-driven, agentic IDE) to describe a **watcher
agent** in plain English, and run a self-contained Python watcher that reads an
Orchestrator job log and decides, per job, whether to **retry**, **escalate**, or
**stop**. **Done** when the watcher prints a correct decision and reason for each job in
the sample log, and you can author or extend the agent from its spec in Kiro.

## Prerequisites

- Python 3.11+ and the shared dependencies — see
  [`00-prerequisites/python-setup.md`](../00-prerequisites/python-setup.md).
- Git and a code editor — see
  [`00-prerequisites/git-and-editor.md`](../00-prerequisites/git-and-editor.md).
- **Basic and advanced tiers:** a free **UiPath Automation Cloud (Community)** account —
  see [`00-prerequisites/uipath-cloud.md`](../00-prerequisites/uipath-cloud.md).
- **Expert tier:** **Kiro** installed and signed in — see
  [`00-prerequisites/kiro-install.md`](../00-prerequisites/kiro-install.md). Kiro does
  **not** require an AWS account. You only need an **AWS account** if you choose to host
  the watcher on AWS — see
  [`00-prerequisites/aws-free-tier.md`](../00-prerequisites/aws-free-tier.md).

New to any term here? Check the [`GLOSSARY.md`](../GLOSSARY.md). Stuck on setup or a run?
See [`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md).
