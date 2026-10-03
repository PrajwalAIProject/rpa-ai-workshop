# Facilitator guide

A practical guide for running the 5-hour AI & RPA workshop — not a minute-by-minute
script. It assumes students already know UiPath **StudioX** from BCG701, so the session
starts above that and climbs the ladder (StudioX → Studio → Orchestrator → agentic AI).

## Two ways to run the room

| Option | Structure | Best when |
| ------ | --------- | --------- |
| **Rotation** | ~70 min per project, all three in sequence, with a ~30 min buffer and wrap-up | The group is fairly even in skill — everyone touches all three, at least at basic |
| **Deep dive** | Students pick one project at the start and push it toward expert over the full 4 hours | Mixed skill — stronger students reach the agentic/Kiro layer while others consolidate fundamentals |

Because every student already has a StudioX foundation, a **deep dive on Project 3** is
often the stronger default: they skip past what BCG701 already taught and spend real time
in Studio Pro, Orchestrator, and Kiro. Projects 1 and 2 work well as the rotation option
for students who want Python/cloud breadth.

## Suggested timing

- **Hour 1 — briefing:** what AI is, how it differs from the RPA they've built, the tools
  landscape, and a short agentic-RPA demo clip, ending with a preview of the afternoon.
- **Hours 2–5 — hands-on lab:** roughly 70 minutes per project under rotation, or one
  project driven toward expert under deep dive. State the clock out loud at the start of
  each block — "you have 70 minutes, here's what done looks like" — so setup doesn't eat
  the lab.

## Pre-session checklist

- [ ] Confirm the room has **reliable internet for 40+ laptops** hitting UiPath Cloud,
      GitHub, AWS, and an LLM API at the same time.
- [ ] Send **signup links at least 2 days ahead**: UiPath Automation Cloud (Community),
      the Anthropic API key steps, the Kiro download, and — only for students hosting the
      watcher on AWS — a card-free AWS path (Student Rewards or Educate). Point everyone at
      [`00-prerequisites/README.md`](../00-prerequisites/README.md) so setup is done
      before the session, not live in the room.
- [ ] Prepare a **backup**: a pre-recorded run of the expert tier, in case live Kiro or
      AWS provisioning lags on the day.
- [ ] Have the [`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md) open — it covers the common
      Python, API-key, network, AWS, Kiro, and UiPath snags.

## What "done" looks like per project tier

Share the "done" bar at the start of each block so students know when to stop and help a
neighbor. The exact criteria live in each project overview and tier README:

- **Project 1** — [`01-stock-market-analyzer/README.md`](../01-stock-market-analyzer/README.md)
- **Project 2** — [`02-morning-news-digest/README.md`](../02-morning-news-digest/README.md)
- **Project 3** — [`03-studiox-to-agentic-rpa/README.md`](../03-studiox-to-agentic-rpa/README.md)

## Close the loop

- Run a **5-minute anonymous feedback form** at the end — what landed, what didn't, what
  they'd want next time — and share it back with the faculty, not just collect it.
- If the department supports it, hand out a **certificate of participation**. It's small,
  but it's what makes the session citable on a resume.
- Leave a way to keep learning (a discussion thread or group) — much of the real learning
  happens in the week after students start tinkering on their own.

For how the session maps onto BCG701 Course Outcomes when you brief the faculty, see
[`course-alignment.md`](course-alignment.md).
