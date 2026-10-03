# Project 3 — Advanced: Orchestrator Setup Guide

## What you'll build

You'll run your Studio bot the way a company actually runs one — not from a laptop.
You'll publish the Studio project to **UiPath Orchestrator**, schedule it to run
**unattended**, add a **queue**, and build a **deliberate failure case** with a
**retry-or-escalate** rule. That retry/escalate judgment is the single most
interview-relevant RPA skill there is.

## Prerequisites

- A completed [basic tier](../README.md) Studio project.
- A UiPath **Automation Cloud Community** account with Orchestrator (included free).
- One **Unattended** robot (the Community plan includes one).

## Step-by-step setup

### 1. Publish the project to Orchestrator

1. In Studio, click **Publish**. Target your Orchestrator tenant's package feed.

   > _Screenshot placeholder: the Studio "Publish" dialog pointing at Orchestrator._
2. In Orchestrator, confirm the package appears under **Automations → Packages**.

### 2. Create a process

1. Go to **Automations → Processes → Add process** and select your published package.
2. Pick the environment/machine with your Unattended robot.

   > _Screenshot placeholder: the Orchestrator "Add process" wizard._

### 3. Schedule it unattended

1. Open **Automations → Triggers → Add trigger (Time)**.
2. Set a cron-style schedule (e.g. every weekday at 07:00) and point it at your process.

   > _Screenshot placeholder: the Orchestrator time-trigger configuration._

### 4. Add a queue

1. Create a queue under **Automations → Queues → Add queue** (e.g. `InvoiceQueue`).
2. In your workflow, use **Add Queue Item** to enqueue work and **Get Transaction
   Item** to process items one at a time.

### 5. Add a deliberate failure + retry-or-escalate rule

This is the core exercise. Introduce a controlled failure and handle it:

1. **Create the failure.** Enqueue an item that will fail — e.g. a missing required
   field, or a locked/absent file the workflow expects.
2. **Retry automatically.** On the queue, set **Auto Retry** with a small **Max # of
   retries** (e.g. 2). Transient failures (a briefly locked file) then self-heal.
3. **Escalate on give-up.** When retries are exhausted, mark the transaction as a
   **business exception** vs. an **application exception**:
   - *Application exception* (unexpected/technical): let it fail, log it, and raise an
     alert so a human looks.
   - *Business exception* (bad data): don't retry; route it for correction.
4. **Escalation channel.** Send an email or Orchestrator alert on final failure so
   someone is notified rather than the job silently dying.

   > _Screenshot placeholder: a queue item showing retries exhausted and the escalation alert._

### 6. Confirm the whole loop

Trigger the schedule (or run on demand), watch the queue process items, see the
deliberate failure retry and then escalate, and confirm the alert fires.

## Common errors and fixes

- **Robot shows "Unavailable"** — The Unattended robot/machine isn't connected. Check
  the machine key and that the robot service is running.
- **Package not visible after Publish** — Studio published to a different feed. Re-publish
  to the Orchestrator tenant feed, then refresh Packages.
- **Trigger never fires** — Confirm the trigger is **enabled** and the time zone is what
  you expect; Orchestrator triggers use the tenant time zone.
- **Everything retries forever** — You set retries on an item that always fails. Cap
  **Max # of retries** and classify permanent data problems as **business exceptions**
  so they are not retried.

See the [`screenshots/`](screenshots/) folder for where captured images go.
