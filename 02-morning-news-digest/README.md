# Project 2 — Morning News Digest

The "hit something in the morning and get my briefing" idea, built in three passes. You
pull headlines from RSS feeds, shape them into a digest, and eventually let an LLM pick
what actually matters and deliver it. Like Project 1, it builds **Python, API, and
scheduling** skills outside the UiPath toolkit.

Work up through the tiers. Each tier is a complete, runnable deliverable on its own.

## The three tiers

### Basic — [`basic/README.md`](basic/README.md)

A one-file script that pulls headlines from a few **RSS feeds** with `feedparser` and
prints the top five. RSS instead of scraping homepages, so a site restyle doesn't break
your run. No API key needed. **Done** when you see a clean top-five list from your feeds.

### Advanced — [`advanced/README.md`](advanced/README.md)

Categorize headlines by keyword (business / tech / sports / general), rank each category
by recency, and render a formatted **Markdown** digest (with an optional **HTML**
version), ready to schedule with cron or Task Scheduler. No API key needed. **Done** when
you have a `digest.md` (and optionally `digest.html`) grouped and ranked the way you
want.

### Expert — [`expert/README.md`](expert/README.md)

Pass the raw headlines to **Anthropic Claude**, ask it to pick the **3 most significant**
with a one-line "why it matters" for each, and deliver by **email (SMTP)** or print.
**Done** when the script produces the top-three digest and (if SMTP is configured) emails
it to you.

## Prerequisites

- Python 3.11+ and the shared dependencies — see
  [`00-prerequisites/python-setup.md`](../00-prerequisites/python-setup.md) and
  [`00-prerequisites/requirements.txt`](../00-prerequisites/requirements.txt).
- Git and a code editor — see
  [`00-prerequisites/git-and-editor.md`](../00-prerequisites/git-and-editor.md).
- **Expert tier only:** an Anthropic API key in a local `.env` — see
  [`00-prerequisites/api-keys.md`](../00-prerequisites/api-keys.md). Email delivery also
  needs SMTP settings in `.env` (optional).

New to any term here? Check the [`GLOSSARY.md`](../GLOSSARY.md). Stuck on setup or a run?
See [`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md).
