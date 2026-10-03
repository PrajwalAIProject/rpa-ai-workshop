# UiPath Automation Cloud (Community)

Project 3 (basic and advanced tiers) uses UiPath to build and run RPA automations. The
free **Community** plan gives you everything the workshop needs.

## What you'll set up

- A free **UiPath Automation Cloud (Community)** account.
- MFA turned on for safety.

The Community plan includes **Studio (Pro)**, **StudioX**, **Orchestrator**, and
**1 Attended + 1 Unattended** robot — enough for the whole project. **No credit card is
required.**

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

---

## Verify

1. You can sign in at [cloud.uipath.com](https://cloud.uipath.com/) and see your
   Orchestrator tenant.
2. **Studio**, **StudioX**, and **Orchestrator** are all visible in the portal.
3. MFA is enabled on your account.

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

The detailed Orchestrator wiring (queues, retry/escalate) lives in the Project 3
advanced guide:
[`03-studiox-to-agentic-rpa/advanced/orchestrator_setup_guide.md`](../03-studiox-to-agentic-rpa/advanced/orchestrator_setup_guide.md).
