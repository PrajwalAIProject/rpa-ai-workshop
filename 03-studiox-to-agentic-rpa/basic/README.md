# Project 3 — Basic: StudioX to Studio Pro

## What you'll build

You'll rebuild one of your own **BCG701 Excel-automation** exercises — but this time in
professional **UiPath Studio Pro** instead of StudioX. Same logic, but with proper
variables, arguments, and a reusable workflow structure instead of a flat StudioX
recording. This is the first rung above where your syllabus left off.

> The `.xaml` in this folder is a **stub** — you build the real workflow live in
> Studio. See [`excel_automation_studio.xaml`](excel_automation_studio.xaml).

## Prerequisites

- A free **UiPath Automation Cloud Community** account ([cloud.uipath.com](https://cloud.uipath.com/)).
  See [`00-prerequisites/uipath-cloud.md`](../../00-prerequisites/uipath-cloud.md).
- UiPath Studio (Pro) installed from your Automation Cloud tenant.
- One of your BCG701 Excel exercises handy to rebuild.

## Step-by-step setup

1. Open **UiPath Studio** (not StudioX) and create a new **Process** project.

   > _Screenshot placeholder: the Studio "New Process" dialog._
2. Add the **Excel** activities package if it isn't already present
   (_Manage Packages → UiPath.Excel.Activities_).
3. Rebuild your BCG701 Excel task as a workflow:
   - Use an **Excel Process Scope** / **Use Excel File** activity to open the workbook.
   - Read a range into a **DataTable** variable instead of a recorded click path.
   - Add **arguments** (e.g. `in_FilePath`) so the workflow is reusable, not hardcoded.
   - Do your transformation (filter / sum / write back) using variables.

   > _Screenshot placeholder: the Studio designer with the Excel scope and variables panel._
4. Run it from Studio and confirm the output workbook is correct.
5. Save the project. The real `.xaml` Studio generates replaces the stub in this folder.

## Common errors and fixes

- **Only StudioX opens** — Install/launch **Studio** specifically; they're separate
  profiles in the same installer. Pick "Studio" on first launch, or switch via the
  home screen.
- **Excel activities missing** — Install `UiPath.Excel.Activities` from Manage Packages.
- **"File in use" when opening the workbook** — Close the file in desktop Excel first,
  or set the Excel scope to visible/read-only as appropriate.
- **Workflow isn't reusable** — If paths are hardcoded, promote them to **arguments**
  so the same `.xaml` can run against different files.
