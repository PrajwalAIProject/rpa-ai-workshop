# Install Kiro — Project 3

**Kiro** is an AI agent IDE (it looks like VS Code). Its special trick is **spec-driven
development**: before writing anything, Kiro writes a plan you can read and fix, then
builds from it. In Project 3 Kiro is your teammate at every level:

| Level | Kiro… |
| ----- | ----- |
| Basic | writes the PhoneDeals spec, explains each Studio step, writes `check_phones.py`, runs the bot with the UiPath CLI and checks the result |
| Advanced | updates the spec, writes `deploy.ps1`, explains Workflow Analyzer errors, reads your failed jobs |
| Expert | builds the watcher agent from its spec, adapts it to your real jobs, and talks to UiPath through MCP |

Allow about **10 minutes**. **No AWS account and no credit card needed.**

> Kiro changes its plans and screens often. These facts were checked on
> [kiro.dev](https://kiro.dev/) in October 2026; confirm current details at
> [kiro.dev/pricing](https://kiro.dev/pricing/) before the session.

---

## 1. Download and install (Windows)

1. Go to [kiro.dev/downloads](https://kiro.dev/downloads/) and download the **Windows**
   installer (x64; ARM64 if your laptop has an ARM chip).
2. Run it and keep the default location
   (`C:\Users\<YourName>\AppData\Local\Programs\Kiro`). If SmartScreen warns you, check
   the file came from kiro.dev, then **More info → Run anyway**.
3. Launch **Kiro**.

macOS and Linux builds are on the same page.

![kiro.dev download page](images/kiro-download.png)
<br><sub>Screenshot needed — see <a href="images/README.md">images/README.md</a>. Capture: the kiro.dev downloads page with the Windows installer.</sub>

## 2. Sign in

On first launch, sign in with **Google**, **GitHub** or an **AWS Builder ID**. Any of
them works; an AWS account is **not** needed. Signing in turns on the agent.

**Next:** install the UiPath CLI with its one-line installer
([`uipath-cli.md`](uipath-cli.md#quick-install-recommended-one-command)). It finds Kiro and
adds **UiPath skills** to it, so Kiro knows the UiPath commands.

## 3. The free tier is enough

| Plan | Price | Credits a month |
| ---- | ----- | --------------- |
| **Free** | $0 | **50** (Claude Sonnet 4.5 and open-weight models such as Qwen3 Coder) |
| Pro | $20 | 1,000 |

Project 3 uses about **6 prompts per level**. To save credits:

- Use **Vibe** chat for small questions and **Spec** only to create or update a spec.
- Write one clear prompt instead of many small ones (the prompts in the READMEs are ready
  to paste).
- Don't ask Kiro to rewrite files that already work.

Source: [kiro.dev/pricing](https://kiro.dev/pricing/).

## 4. Learn the three Kiro features Project 3 uses

| Feature | What it is | Where it lives |
| ------- | ---------- | -------------- |
| **Specs** | A plan in three files: `requirements.md` (what), `design.md` (how) and `tasks.md` (steps). Start one from the Kiro panel → **Spec**. | `.kiro/specs/<name>/` |
| **Steering** | Project rules Kiro reads before every answer ("this is a UiPath project, use VB.NET…") | `.kiro/steering/*.md` |
| **MCP servers** | Tools Kiro can use, such as the UiPath CLI (`uip mcp serve`) | `.kiro/settings/mcp.json` |

Kiro also has **agent hooks** (automatic actions, for example "on save, run the
analyzer"), stored in `.kiro/hooks/`. The advanced level shows one.

Docs: [specs](https://kiro.dev/docs/specs/) · [steering](https://kiro.dev/docs/steering/) ·
[MCP](https://kiro.dev/docs/mcp/configuration/) · [hooks](https://kiro.dev/docs/hooks/).

## 5. Verify (3 minutes)

1. **File → Open Folder** → any empty folder.
2. Open the **Kiro** panel, choose **Vibe**, and type:

   ```text
   Create hello.py that prints "Kiro works", then run it.
   ```
3. Kiro writes the file and asks before running `python hello.py`. Allow it. The terminal
   prints `Kiro works`.

Kiro **asks before every terminal command**. Read each one before you allow it. If you
don't understand a command, ask: *"What does this command do?"*

## Common errors and fixes

| You see | Fix |
| ------- | --- |
| Sign-in loops or the agent stays greyed out | Sign out and in again with Google, GitHub or AWS Builder ID. Allow pop-ups. On college Wi-Fi, try a phone hotspot. |
| "Out of credits" | The 50 free credits reset every month. Use the reference files in the repo for the rest of the lab. |
| Kiro can't run `python` or `uip` | Install them, then **restart Kiro** so it sees the new PATH. |
| Kiro invents a UiPath activity that doesn't exist | Add the steering file from the basic README; it tells Kiro to say "not sure" instead of guessing. Check activity names in Studio. |
| An old Kiro version stops connecting | Update Kiro (**Help → Check for Updates**). Very old versions stop working in November 2026. |
