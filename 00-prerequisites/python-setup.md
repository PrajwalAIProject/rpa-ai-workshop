# Python setup

Every project in this workshop runs on Python. Set this up once; all three projects
share the same virtual environment and dependency list.

## What you'll set up

- Python **3.11 or newer**.
- A **virtual environment** (`.venv`) so this workshop's packages stay separate from the
  rest of your system.
- All the Python packages the projects use, installed from
  [`requirements.txt`](requirements.txt).

---

## Steps

### 1. Install Python 3.11 or newer

**Windows (this is what the lab machines run):**

1. Go to [python.org/downloads](https://www.python.org/downloads/) and download the
   latest **Windows installer (64-bit)**. Any version **3.11 or newer** is fine.
2. Run the installer. On the **first screen**, tick the box
   **"Add python.exe to PATH"** at the bottom — this is the single most common thing
   people forget, and skipping it causes the "python is not recognized" error later.

   ![Python installer first screen with Add python.exe to PATH checked](images/python-add-to-path.png)
   <br><sub>Screenshot needed — see <a href="images/README.md">images/README.md</a>. Capture: the Python installer's first screen with the "Add python.exe to PATH" box ticked.</sub>
3. Click **Install Now** and let it finish.

**macOS:** download the macOS installer from the same page and run it, **or** use
Homebrew: `brew install python@3.11`.

**Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install python3 python3-venv python3-pip`.

### 2. Verify the install

Open a **new** terminal (PowerShell on Windows) so it picks up the updated PATH, then:

```powershell
# Windows — either of these should print 3.11 or newer:
python --version
py --version
```

```bash
# macOS / Linux — the command is often python3:
python3 --version
```

You should see `Python 3.11.x` (or newer). If not, see
[Common errors and fixes](#common-errors-and-fixes).

### 3. Create and activate a virtual environment

Do this from the **repo root** (`rpa-ai-workshop/`).

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If activation is blocked with a message about scripts being disabled, run this **once**
for your user account, then activate again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

(That allows locally created scripts to run. You only ever need to do it once per
machine. A per-terminal alternative is `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.)

**Windows (cmd):**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

When the environment is active your prompt is prefixed with `(.venv)`. Run `deactivate`
to leave it.

### 4. Install the dependencies

With the virtual environment **active**, from the repo root:

```bash
pip install -r 00-prerequisites/requirements.txt
```

That installs everything used across all three projects.

---

## What each package is for

| Package | Used by | One-line purpose |
| ------- | ------- | ---------------- |
| `yfinance` | Project 1 | Downloads stock price data. |
| `pandas` | Project 1 | Holds and crunches the data in tables (moving averages). |
| `matplotlib` | Project 1 | Draws the price/MA charts and saves them as PNGs. |
| `feedparser` | Project 2 | Reads RSS news feeds. |
| `anthropic` | Projects 1 & 2 (expert) | Official client for the Claude API. |
| `python-dotenv` | Projects 1 & 2 (expert) | Loads secrets from your local `.env` file. |
| `requests` | Project 1 (expert) | Makes HTTP calls (e.g. posting commentary to a webhook). |

---

## Verify

1. Virtual environment active (prompt shows `(.venv)`).
2. `python --version` (or `py --version`) prints 3.11+.
3. `pip list` shows `yfinance`, `pandas`, `matplotlib`, `feedparser`, `anthropic`,
   `python-dotenv`, and `requests`.
4. Quick smoke test (should print nothing and exit cleanly):

   ```bash
   python -c "import yfinance, pandas, matplotlib, feedparser, anthropic, dotenv, requests; print('all imports OK')"
   ```

---

## Common errors and fixes

- **`'python' is not recognized`** (Windows) — Python isn't on your PATH. Re-run the
  installer, choose **Modify**, and ensure **"Add python.exe to PATH"** is ticked; or
  use the `py` launcher instead of `python`. On macOS/Linux the command is usually
  `python3`.
- **PowerShell blocks `Activate.ps1`** ("running scripts is disabled on this system") —
  Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then activate again.
- **`pip install` fails with SSL / proxy errors on college Wi-Fi** — Campus networks
  often sit behind a proxy or TLS-inspection firewall. Try a phone hotspot, or ask IT
  for the proxy settings and set `HTTP_PROXY` / `HTTPS_PROXY`. As a last resort for a
  trusted mirror only, your instructor may give you a `--trusted-host` flag. Also run
  `python -m pip install --upgrade pip` first — an old pip causes many install failures.
- **A package fails to build / "Microsoft Visual C++ required"** — Upgrade pip
  (`python -m pip install --upgrade pip`) and retry; the pinned versions ship prebuilt
  wheels, so a fresh pip usually avoids any compiler step.
- **Windows "path too long" errors during install** — Enable long paths: in an
  **admin** PowerShell run
  `Set-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' -Name LongPathsEnabled -Value 1`,
  then reboot. Also keep the repo in a short path like `C:\dev\rpa-ai-workshop` rather
  than deep under Documents.
