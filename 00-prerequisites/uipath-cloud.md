# UiPath Automation Cloud (Community) and UiPath Studio

Project 3 uses UiPath at every level: Studio to build the PhoneDeals bot, Orchestrator to
run it on a schedule. The free **Community** plan gives you everything the workshop needs.

## What you'll set up

- A free **UiPath Automation Cloud (Community)** account.
- MFA turned on for safety.
- **UiPath Studio** on your laptop, with the browser extension for Chrome or Edge.

The Community plan includes **Studio**, **StudioX**, **Orchestrator**, and
**1 Attended + 1 Unattended** robot — enough for the whole project. **No credit card is
required.**

### Good things to know about the Community plan

Content was rephrased for compliance with licensing restrictions.

- **No time limit.** The underlying 12-month license **auto-renews**, so the expiry date
  keeps moving forward — the plan does not simply run out mid-course.
- **Orchestrator is limited to 1 machine per user** on Community, which is fine for this
  workshop.
- The **Community Edition was rebuilt in August 2026** around **AI agents, coding
  agents, and APIs**.
- A **"Small Business"** — an organization and its affiliates under roughly
  **USD $5M annual revenue** — may use Community for **internal commercial** work, and
  **students doing coursework are fine**.
- UiPath changes its terms and plans often — **confirm the current details** on the
  official pages before the session.

Sources:
[UiPath Community plan docs](https://docs.uipath.com/automation-cloud/automation-cloud/latest/admin-guide/community-plan)
and [UiPath pricing](https://www.uipath.com/pricing).

---

## Steps

1. Go to [cloud.uipath.com](https://cloud.uipath.com/) and choose **Sign up** / create a
   **Community** account. You can sign up with Google, Microsoft, or an email address.

   ![UiPath Automation Cloud sign-up page](images/uipath-signup.png)
   <br><sub>Screenshot needed — see <a href="images/README.md">images/README.md</a>. Capture: the UiPath Automation Cloud sign-up page showing the Community sign-up options.</sub>
2. Verify your email if prompted, then let UiPath finish provisioning your Community
   tenant (this takes a minute the first time).
3. Once in, you'll land on the Automation Cloud home with **Orchestrator** and
   **Studio/StudioX** available in the left navigation.
4. Turn on **MFA**: open your profile / account settings and enable
   **multi-factor authentication**.
5. **Install UiPath Studio on your laptop** (Windows 10/11 only). Do this at home: the
   installer is large.
   1. Download **UiPathStudioCommunity.msi**: in Automation Cloud use **Download Studio**
      (home page or Resource Center), or the direct link
      <https://download.uipath.com/UiPathStudioCommunity.msi>.
   2. Run it and choose **Quick** install (installs for your user only, no admin rights
      needed).
   3. When Studio opens, **sign in** with the same Community account. If asked for a
      profile, choose **UiPath Studio** (not StudioX). You can switch later in
      **Home → Settings → License and Profile**.
   4. Studio connects to your Orchestrator tenant automatically.
6. **Install the browser extension** (Project 3 automates a website). In Studio:
   **Home → Tools → UiPath Extensions → Chrome** (or **Edge**) → Install. Then open the
   browser and make sure the **UiPath** extension is **enabled**. Restart the browser.
7. **Then install the UiPath CLI**: [`uipath-cli.md`](uipath-cli.md).

*(On macOS/Linux there is no desktop Studio. Tell your instructor before the workshop:
you can pair with a Windows laptop for Project 3, or do Projects 1–2.)*

---

## Verify

1. You can sign in at [cloud.uipath.com](https://cloud.uipath.com/) and see your
   Orchestrator tenant.
2. **Studio**, **StudioX**, and **Orchestrator** are all visible in the portal.
3. MFA is enabled on your account.
4. **UiPath Studio** opens on your laptop and shows you signed in (top-right of Studio)
   with your Community account.
5. The **UiPath** extension shows as enabled in Chrome or Edge.

---

## Common errors and fixes

- **Sign-up seems stuck** — First-time tenant provisioning can take a minute or two.
  Refresh after a short wait before retrying.
- **Can't find Studio to download** — Studio is downloaded/launched from within
  Automation Cloud; look under the Studio/StudioX area of the portal rather than
  searching the public site.
- **Community limits reached** — The Community plan allows 1 Attended + 1 Unattended
  robot, which is enough here. If a robot slot appears "in use," make sure a previous
  session isn't still connected.

- **The bot can't attach to the browser** — The UiPath extension is missing or disabled.
  Install it again from **Home → Tools → UiPath Extensions**, enable it, and restart the
  browser.

Deploying to Orchestrator, schedules and retries are in the Project 3 advanced guide:
[`03-studiox-to-agentic-rpa/advanced/README.md`](../03-studiox-to-agentic-rpa/advanced/README.md).
