# Install Kiro (Project 3 expert only)

The Project 3 expert tier uses **Kiro** to describe the watcher agent as a spec in plain
English. You only need this for that tier.

> AWS and Kiro update their terms, pricing, and screens often. The facts below were
> accurate at the time of writing — **confirm current details on
> [kiro.dev](https://kiro.dev/) before the session.** Kiro facts are attributed to
> [kiro.dev](https://kiro.dev/). Content was rephrased for compliance with licensing
> restrictions.

## What you'll set up

- **Kiro** installed on your machine.
- Signed in so the agent features are active.

**What Kiro is:** AWS's AI-powered, **agentic, spec-driven IDE** — a **VS Code-based
fork**, powered by Claude. It went **GA in May 2026** and is the successor to Amazon Q
Developer. Downloading it is **free**.

---

## Before you start

Do the [AWS Free Tier setup](aws-free-tier.md) first — you'll sign in to Kiro with an
AWS identity.

### System requirements

- **macOS** (Intel and Apple Silicon)
- **Windows 10/11** on **x64 or ARM64**
- **Linux**: Ubuntu 24+, Debian 13+, Fedora 40+, Arch, or Mint 22+ (x86_64 / ARM64)

---

## Steps (Windows)

1. Go to the official site **[kiro.dev](https://kiro.dev/)** and open the
   getting-started / installation page. Download the **Windows installer**.

   > _(screenshot placeholder: kiro.dev download page)_
2. Run the installer.
3. Accept the **AWS Customer Agreement / license** when prompted.
4. Choose the install location, or keep the default
   (`C:\Users\<YourName>\AppData\Local\Programs\Kiro`).
5. Finish the installer and **launch Kiro**.

**macOS / Linux:** download the matching build from
[kiro.dev](https://kiro.dev/) and follow its platform installer.

### First launch / sign-in

1. On first launch, **sign in to authenticate**. Kiro supports **AWS Builder ID**, an
   **AWS account**, or supported **SSO**.
2. Signing in activates the agent features.

> **Credits/usage:** downloading Kiro is free, but **AI agent usage consumes credits**.
> There is a perpetual **Kiro Free tier with a limited monthly credit allocation**, and
> agent requests draw from it. The **free tier is all you need** for this workshop.

Full official docs: [kiro.dev/docs](https://kiro.dev/docs).

---

## Verify

1. Kiro opens and you are **signed in** (agent features available).
2. Create a trivial spec to confirm the agent works: start a new spec, type a one-line
   request (for example, "a function that adds two numbers"), and confirm Kiro responds.
3. You can open the repo's existing spec at
   [`03-studiox-to-agentic-rpa/expert/kiro-specs/watcher-agent.spec.md`](../03-studiox-to-agentic-rpa/expert/kiro-specs/watcher-agent.spec.md).

---

## Common errors and fixes

- **Sign-in fails / agent features greyed out** — Confirm you're signed in with the AWS
  identity from the [AWS setup](aws-free-tier.md) and that your region is supported.
- **Agent requests stop working** — You may have used up the free monthly credit
  allocation; check your usage. The free tier resets monthly.
- **Installer blocked by Windows SmartScreen** — Confirm you downloaded from
  **kiro.dev**, then choose **More info → Run anyway**.
- **Can't reach the Claude backend** — Check your network/proxy (college Wi-Fi often
  needs a proxy) and that you're signed in.
