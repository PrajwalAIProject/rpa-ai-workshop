# VS Code, Git, GitHub and GitHub Copilot

In Project 1 you don't type the code yourself. You give **GitHub Copilot** (an AI
assistant inside VS Code) a clear prompt. It writes the Python script, runs it in the
terminal, and fixes its own errors. This guide sets up the four things that needs:

1. A **GitHub account** (free). Copilot is tied to it.
2. **VS Code**, the code editor.
3. **Git**, so VS Code can sign in to GitHub and you can save your work there.
4. **GitHub Copilot**, turned on in VS Code with your GitHub account.

Allow about 20 minutes. Do it **before** the workshop: downloads on college Wi-Fi are slow.

> GitHub changes Copilot's plans and screens often. The facts here were checked in
> October 2026; confirm current details at
> [github.com/features/copilot/plans](https://github.com/features/copilot/plans).

---

## 1. Create a GitHub account

1. Go to [github.com/signup](https://github.com/signup) and sign up with an email you
   check often. Pick a professional username: recruiters will see it.
2. Verify your email.
3. **Recommended for students:** apply for **GitHub Education** at
   [education.github.com/pack](https://education.github.com/pack) with your college
   email or student ID. Approved students get the **Copilot Student** plan, with more
   usage than Copilot Free. Approval can take **1–3 days**, so apply early. Copilot Free
   (step 5) is enough for Project 1 if you're not approved in time.

## 2. Install VS Code

1. Download from [code.visualstudio.com](https://code.visualstudio.com/) and install.
   On Windows, tick **"Add to PATH"** and **"Open with Code"** during setup.
2. Open VS Code → **Extensions** (left bar, or `Ctrl+Shift+X`) → install **Python**
   (by Microsoft).

## 3. Install Git

- **Windows:** download from [git-scm.com/download/win](https://git-scm.com/download/win)
  and run the installer with the defaults.
- **macOS:** run `git --version` once; macOS offers to install it. Or `brew install git`.
- **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install git`.

Then, in a **new** terminal, set your identity once. Use the email of your GitHub account:

```bash
git --version
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## 4. Sign in to GitHub from VS Code

1. In VS Code click the **Accounts** icon (person icon, bottom-left) →
   **Sign in with GitHub to use GitHub Copilot** (or **Sign in to Sync Settings**).
2. Your browser opens. Sign in to GitHub and click **Authorize Visual Studio Code**.
3. Back in VS Code, the Accounts icon shows your GitHub username.

   ![VS Code Accounts menu signed in to GitHub](images/vscode-github-signin.png)
   <br><sub>Screenshot needed — see <a href="images/README.md">images/README.md</a>. Capture: the VS Code Accounts menu showing the signed-in GitHub account.</sub>

## 5. Turn on GitHub Copilot

1. Click the **Copilot icon** in VS Code's title bar (or open **View → Chat**). If
   prompted, choose **Use Copilot for free** / **Sign up for Copilot Free**. Recent
   VS Code versions include Copilot; if asked, install the **GitHub Copilot Chat**
   extension.
2. The **Chat** panel opens. At the bottom of the panel, set the mode drop-down to
   **Agent**. In agent mode Copilot can create files and run terminal commands for you
   (it asks first).

   ![Copilot Chat panel in Agent mode](images/vscode-copilot-agent.png)
   <br><sub>Screenshot needed — see <a href="images/README.md">images/README.md</a>. Capture: the Copilot Chat panel with the mode drop-down set to Agent.</sub>

### What Copilot Free gives you

| Plan | What you get | Cost |
| ---- | ------------ | ---- |
| **Copilot Free** | 2,000 code completions and **50 chat requests a month** (agent mode included) | Free, any GitHub account |
| **Copilot Student** | More chat and agent usage (AI-credit allowance), unlimited completions | Free for verified students (GitHub Education) |

Project 1 needs about **3 prompts plus a few follow-ups**, well inside 50. Don't spend
requests on small talk; each message you send in Chat counts.

Sources: [Copilot plans](https://github.com/features/copilot/plans),
[Copilot Free limits](https://iammeister.de/en/radar/github-copilot-free-limits-en/),
[Copilot for students](https://www.beststudenttools.com/blog/github-copilot-free-student/).

---

## Verify (2 minutes)

1. Make a project folder, e.g. `C:\stock-project`, and open it in VS Code with
   **File → Open Folder**. Click **Yes, I trust the authors** if asked.
2. In Copilot Chat (**Agent** mode) type:

   ```text
   Create hello.py that prints "Copilot works", then run it.
   ```
3. Copilot creates the file and asks to run `python hello.py`. Click **Continue/Allow**.
   The terminal prints `Copilot works`. This also proves VS Code can find Python.

## How to work with Copilot in Project 1

- **Always use Agent mode** and keep the project folder open, so Copilot can create
  files and run them.
- Copilot **asks before running a terminal command**. Read it, then allow it. If you
  don't understand a command, ask: *"What does this command do?"*
- If the output is wrong, describe what you see in plain words ("it picked the US
  listing, I want NSE") and let Copilot fix it.
- **Never paste API keys or passwords into Chat.** Keys go only in the `.env` file.

---

## Common errors and fixes

| You see | Fix |
| ------- | --- |
| `'git' is not recognized` | Close and reopen VS Code / the terminal after installing Git; if it still fails, re-run the Git installer. |
| Sign-in loop / "Authorize Visual Studio Code" never finishes | Make sure the browser is signed in to the same GitHub account, allow pop-ups, then retry from the Accounts icon. On restricted college networks, try a phone hotspot. |
| No Copilot icon or Chat panel | Update VS Code (**Help → Check for Updates**) and install **GitHub Copilot Chat** from Extensions. |
| "You've reached your monthly chat limit" | Copilot Free's 50 chat requests are used up. Use the reference solutions in this repo, or apply for Copilot Student (GitHub Education). |
| Copilot writes code but doesn't run it | You're in **Ask** or **Edit** mode. Switch the Chat mode drop-down to **Agent**. |
| Copilot says `python` isn't found | Install Python with "Add to PATH" ([`python-setup.md`](python-setup.md)), then restart VS Code. |
| GitHub rejects a `git push` | Sign in through VS Code (step 4); VS Code handles the token for you. Don't use your GitHub password on the command line. |
