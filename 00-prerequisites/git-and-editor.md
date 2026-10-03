# Git and a code editor

You'll clone the workshop repo, run the scripts, and (in Project 1 expert) push to
GitHub so a scheduled Action can run. For that you need Git and a code editor.

## What you'll set up

- **Git** installed and configured with your name and email.
- A **code editor** — VS Code for the Python tiers (Kiro for the Project 3 expert tier).

---

## Steps

### 1. Install Git

- **Windows:** download from [git-scm.com/download/win](https://git-scm.com/download/win)
  and run the installer. The defaults are fine; accepting them also installs **Git
  Bash**, a handy terminal.
- **macOS:** `brew install git`, or just run `git --version` once — macOS offers to
  install the developer tools that include Git.
- **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install git`.

### 2. Verify Git

```bash
git --version
```

You should see something like `git version 2.x.x`.

### 3. Set your identity (one time)

Git stamps every commit with a name and email. Set them once:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Use the **email tied to your GitHub account** if you'll push to GitHub in Project 1
expert.

### 4. Install a code editor

**VS Code** is the recommended editor for the Python tiers:

1. Download from [code.visualstudio.com](https://code.visualstudio.com/).
2. Install the **Python** extension (by Microsoft) from the Extensions panel — it gives
   you run buttons, linting, and virtual-environment detection.

> **Expert-tier note:** Kiro (installed in [`kiro-install.md`](kiro-install.md)) is
> itself a **VS Code-based editor**. If you're doing the Project 3 expert tier, you can
> use Kiro as your everyday editor and skip a separate VS Code install — your VS Code
> extensions and keybindings carry over.

---

## Verify

1. `git --version` prints a version.
2. `git config --global user.name` and `git config --global user.email` print your
   values.
3. Your editor opens the `rpa-ai-workshop` folder and can open a `.py` file.

---

## Common errors and fixes

- **`'git' is not recognized`** (Windows) — Close and reopen your terminal after
  installing so it picks up the new PATH; if it still fails, re-run the Git installer.
- **Commits show the wrong author** — Re-run the `git config --global user.name/email`
  commands above with the correct values.
- **GitHub rejects your push with an authentication error** — Modern GitHub needs a
  **personal access token** or SSH key, not your account password. Follow GitHub's
  [authentication guide](https://docs.github.com/en/authentication) if you reach the
  Project 1 expert push step.
