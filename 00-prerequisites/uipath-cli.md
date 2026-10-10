# UiPath CLI (`uip`) — Project 3

The **UiPath CLI** is UiPath's official command line, called `uip`. It runs, checks, packs
and deploys UiPath projects and starts Orchestrator jobs from a terminal. That matters in
Project 3 because **Kiro** (an AI agent) can type terminal commands, so with `uip` it can
run and test your bot for you.

| Level | You use `uip` to… |
| ----- | ----------------- |
| Basic | run your bot from the terminal: `uip rpa run-file` |
| Advanced | check, pack, deploy and start it: `uip rpa analyze`, `uip rpa pack`, `uip or …` |
| Expert | read failed jobs and rerun them; connect Kiro to UiPath with `uip mcp serve` |

Allow about **10 minutes**. Install **UiPath Studio first** ([`uipath-cloud.md`](uipath-cloud.md)).

> The new `uip` CLI became generally available in July 2026 and replaces the older
> `uipcli` tool. Commands below were checked against the
> [UiPath CLI docs](https://docs.uipath.com/uipath-cli/standalone/latest/user-guide/about-uipath-cli)
> in October 2026. If a command differs on your version, run it with `--help`.

---

## Quick install (recommended): one command

Open **PowerShell** and run UiPath's official installer:

```powershell
# Windows (PowerShell)
irm https://download.uipath.com/uipath-cli/install.ps1 | iex
```

It installs everything the CLI needs and skips anything you already have:
**Node.js**, the **UiPath CLI** (`uip`), the **.NET 8 SDK** (for pack/analyze) and
**Python** (if missing). It also installs **UiPath skills** into AI coding agents it finds
on your PC, such as Kiro, so they know how to work with UiPath.

- Install Kiro **first** ([`kiro-install.md`](kiro-install.md)) so the installer finds it.
  To target Kiro explicitly, download the script and run it with `-Agent kiro`:

  ```powershell
  irm https://download.uipath.com/uipath-cli/install.ps1 -OutFile install-uip.ps1
  .\install-uip.ps1 -Agent kiro
  ```
- Want to see what it would do first? Run `.\install-uip.ps1 -DryRun`.
- It uses **winget** for Node.js, .NET and Python. If a step fails with a permissions
  error, run PowerShell **as Administrator** and try again.

Then **open a new terminal** and go to [step 3, log in](#3-log-in-to-your-uipath-account).
Prefer to install each piece yourself? Follow steps 1 and 2 instead.

## 1. Install Node.js 22 or later (manual install)

The CLI runs on Node.js.

1. Download the **LTS** version (22 or newer) from [nodejs.org](https://nodejs.org/) and
   install it with the default options.
2. In a **new** terminal:

   ```powershell
   node --version     # v22.x or newer
   npm --version
   ```

## 2. Install the UiPath CLI (manual install)

```powershell
npm install -g @uipath/cli
uip --version
```

On Windows the `uip` launcher lives in `%APPDATA%\npm\`. If `uip` is not recognized, close
the terminal and open a new one.

The CLI downloads its tools the first time you use them (for example, the Orchestrator
tool on the first `uip or …` command). To get them now, while the Wi-Fi is quiet:

```powershell
uip tools install rpa
uip tools install or
```

## 3. Log in to your UiPath account

```powershell
uip login --interactive
```

A browser opens. Sign in with the same account as UiPath Studio, then pick your tenant
(usually **DefaultTenant**) in the terminal. Check it:

```powershell
uip login status
```

The session is saved in a local `.uipath/` folder, so you don't log in every time. You
**never** type your UiPath password into a script or into Kiro's chat.

## 4. Verify (2 minutes)

```powershell
uip or folders list
```

You see your Orchestrator folders, including **Shared**. That proves the CLI is
installed, logged in and can reach Orchestrator.

The basic level's first real command, once your bot exists, is:

```powershell
uip rpa run-file --file-path C:\PhoneDeals\Main.xaml
```

It runs the workflow through UiPath Studio on your PC (Windows only). If Studio is not
open, the CLI starts it.

## The commands you'll use

| Command | What it does |
| ------- | ------------ |
| `uip rpa run-file --file-path .\Main.xaml` | Run a workflow on this PC |
| `uip rpa run-file --file-path .\Main.xaml --input-arguments '{"in_MaxPrice": 15000}'` | Run it with input arguments |
| `uip rpa analyze .` | Workflow Analyzer: check the project for errors |
| `uip rpa pack . --output .\dist` | Build a `.nupkg` package |
| `uip or packages upload .\dist\PhoneDeals.1.0.2.nupkg` | Upload the package to Orchestrator |
| `uip or processes create --name "PhoneDeals" --package-key "PhoneDeals" --package-version "1.0.2" --folder-path "Shared" --entry-point "Main.xaml"` | Create the process in folder Shared |
| `uip or processes list --folder-path "Shared"` | List processes and their keys |
| `uip or jobs start <process-key> --wait-for-completion` | Start a job and wait for the result |
| `uip or jobs list --folder-path "Shared" --state Faulted --process-name "PhoneDeals"` | List the failed jobs |
| `uip mcp serve` | Let an AI agent (Kiro) use `uip` as a tool (Project 3 expert) |

Every command has `--help`, for example `uip or jobs start --help`.

## Common errors and fixes

| You see | Fix |
| ------- | --- |
| `'uip' is not recognized` | Open a new terminal. If it still fails, check that `%APPDATA%\npm` is on your PATH, or reinstall with `npm install -g @uipath/cli`. |
| `running scripts is disabled on this system` (PowerShell) | Run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, or use `uip.cmd` instead of `uip`. |
| `npm install` fails on college Wi-Fi | Use a phone hotspot. Behind a proxy, set `HTTPS_PROXY` (the CLI and npm both respect it). |
| `node` is older than 22 | Install the current LTS from nodejs.org and open a new terminal. |
| `uip login` opens no browser | Use `uip login --interactive --no-browser` and open the printed link yourself. |
| "not logged in" / token expired | `uip login --interactive` again. |
| `run-file` can't find Studio | UiPath Studio must be installed on this PC and signed in ([`uipath-cloud.md`](uipath-cloud.md)). |
| `uip rpa pack` / `analyze` complains about .NET | The packaging tools need the .NET 8 runtime. Install the **.NET 8 Desktop Runtime** from [dotnet.microsoft.com](https://dotnet.microsoft.com/download/dotnet/8.0). |
