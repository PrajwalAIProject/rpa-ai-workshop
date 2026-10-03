# Phase 1 GitHub repo scaffold — AI & RPA Workshop (pass 2)

The scaffold builds out the full nine-tier teaching repo from section 9 of the session plan: three projects (stock analyzer, news digest, StudioX-to-agentic-RPA), each in basic/advanced/expert, plus `00-prerequisites`, a `slides/` placeholder, and root-level `README.md`, `.gitignore`, `.env.example`, and a shared `requirements.txt`. This is the second review pass; its job is to confirm whether the three findings from pass 1 were addressed and to surface anything new. The two blocking findings (a missing sample PNG and a missing project 3 advanced README) are both fixed. The remaining non-blocking git-boundary observation is unchanged but is a downstream push concern rather than a scaffold-content defect.

Watch for: the scaffold directory still has no `.git` of its own — the only repository on the path is at the user's home directory with no commits (confirmed). This does not block the scaffold content but should be resolved before the repo is pushed so the `.gitignore` secret-ignore and sample-PNG carve-out rules take effect.

**Verdict**: APPROVED

## High-level view

The directory tree now matches section 9 exactly. The two files pass 1 flagged as absent are present: `01-stock-market-analyzer/advanced/sample_output.png` is a real 82 KB PNG (verified by its `89 50 4E 47` magic bytes, not a placeholder), and `03-studiox-to-agentic-rpa/advanced/README.md` exists with the required four-part shape. Every project, every tier, the `.github/workflows/daily_run.yml` under project 1 expert, the `kiro-specs/` and `sample_orchestrator_log.json` under project 3 expert, `screenshots/.gitkeep` under project 3 advanced, the `.xaml` stub under project 3 basic, and `slides/.gitkeep` are all accounted for.

The new project 3 advanced README follows "What you'll build → Prerequisites → Step-by-step setup → Common errors and fixes" and indexes into `orchestrator_setup_guide.md` for the depth, which keeps the tier documentation consistent with its siblings rather than duplicating the guide.

The advanced README's claim that "a committed example chart lives at `sample_output.png`" is now accurate — the file is present and is a valid PNG, closing the gap pass 1 called out where the prose asserted a file that did not exist.

The Python tiers, watcher-agent correctness, UiPath stub marking, and secrets posture were verified in pass 1 and are unchanged in this pass; no new concerns surfaced in those areas on spot-check.

The scaffold is still not an independent git repository and has no commit of its own. The only `.git` on the path sits at the user's home directory and reports no commits. This is the one item from pass 1 that remains open; it is non-blocking for the scaffold's content but should be settled before pushing.

<details>
<summary>Issues (1)</summary>

1. **Scaffold not its own git repo / no commit** (non-blocking) — no `.git` exists under `rpa-ai-workshop`; the only repository found is at the user's home directory, which reports no commits. Initialize a dedicated repo (or confirm the intended repo boundary) and make a clean initial commit before pushing, so the `.gitignore` secret-ignore and sample-PNG carve-out rules take effect. Not blocking the scaffold content; the repo boundary and first push are a downstream workflow step.

</details>

<details>
<summary>Details</summary>

### Pass 1 findings — resolution status

Finding 1 (missing `sample_output.png`): **resolved (confirmed).** The file now exists at `01-stock-market-analyzer/advanced/sample_output.png`, is 82,583 bytes, and begins with the PNG signature `89 50 4E 47 0D 0A 1A 0A`, confirming a real image rather than an empty or stub file. The advanced README's reference `[sample_output.png](sample_output.png)` now resolves to a committed file, so the prose no longer over-claims.

Finding 2 (missing project 3 advanced `README.md`): **resolved (confirmed).** The file exists and follows the four-part shape. It is deliberately a short index that defers the step-by-step depth to `orchestrator_setup_guide.md`, with its Prerequisites, Step-by-step setup (the six numbered steps), and Common errors and fixes all pointing into the guide. This satisfies the "exact tree match" criterion and keeps the tier doc consistent with sibling tiers without duplicating content.

Finding 3 (scaffold not its own git repo / no commit): **unchanged (confirmed).** `git rev-parse --show-toplevel` from inside the scaffold resolves to `C:/Users/HMPrajwa`, and that repository reports "your current branch 'master' does not have any commits yet." There is no `.git` under `rpa-ai-workshop`. This remains a non-blocking observation: the scaffold's files are correct and complete, but until the directory is its own committed repository the ignore rules and sample-file carve-outs are not actually in force. The intended repository boundary and the first push are a downstream workflow concern, which is why this does not gate approval of the scaffold content.

### Directory tree against section 9

With the two added files, the filesystem tree lines up with section 9 on every structural element the task calls out:

```
rpa-ai-workshop/
├── README.md, .gitignore, .env.example
├── 00-prerequisites/{README.md, requirements.txt}
├── 01-stock-market-analyzer/
│   ├── basic/{stock_price.py, README.md}
│   ├── advanced/{moving_averages.py, sample_output.png, README.md}   ← png now present
│   └── expert/{ai_commentary_agent.py, .github/workflows/daily_run.yml, README.md}
├── 02-morning-news-digest/{basic, advanced, expert}/...
├── 03-studiox-to-agentic-rpa/
│   ├── basic/{excel_automation_studio.xaml, README.md}
│   ├── advanced/{orchestrator_setup_guide.md, README.md, screenshots/.gitkeep}  ← README now present
│   └── expert/{watcher_agent.py, sample_orchestrator_log.json, kiro-specs/watcher-agent.spec.md, README.md}
└── slides/.gitkeep
```

### Carried forward from pass 1 (unchanged, re-confirmed)

The Python tiers are complete, runnable programs with graceful network/API failure handling and student-level docstrings; the `watcher_agent.py` produces a correct retry/escalate/stop decision against the committed sample log (RETRY 2 / ESCALATE 2 / STOP 1) matching the README's recorded output; the `.xaml` is clearly marked a stub; `requirements.txt` is the exact union (yfinance, pandas, matplotlib, feedparser, anthropic, python-dotenv, requests); `.env.example` carries empty placeholders; `.gitignore` covers `.venv`, `__pycache__`, `*.pyc`, `.env`/`.env.*`, `*.db`/`*.sqlite`, and OS cruft; and no real API key is committed. These were verified in pass 1 and are untouched; this pass did not re-run the suites, consistent with the review instructions.

</details>
