# Project 3 — Advanced: Orchestrator (scheduled, unattended)

> The full tier walkthrough lives in
> [`orchestrator_setup_guide.md`](orchestrator_setup_guide.md). This README is a short
> index into it, following the standard four-part tier shape.

## What you'll build

Run your Studio bot the way a company actually runs one: publish it to **UiPath
Orchestrator**, schedule it **unattended**, add a **queue**, and build a **deliberate
failure case** with a **retry-or-escalate** rule. See the guide for the step-by-step.

## Prerequisites

- A completed [basic tier](../basic/README.md) Studio project.
- A UiPath **Automation Cloud Community** account with Orchestrator (included free).
- One **Unattended** robot (the Community plan includes one).

## Step-by-step setup

Follow the six numbered steps in
[`orchestrator_setup_guide.md`](orchestrator_setup_guide.md): publish the package,
create a process, schedule it unattended, add a queue, add a deliberate failure with a
retry-or-escalate rule, and confirm the whole loop. Captured images go in the
[`screenshots/`](screenshots/) folder.

## Common errors and fixes

See the "Common errors and fixes" section at the end of
[`orchestrator_setup_guide.md`](orchestrator_setup_guide.md) — it covers an unavailable
robot, a package not visible after publish, a trigger that never fires, and items that
retry forever.
