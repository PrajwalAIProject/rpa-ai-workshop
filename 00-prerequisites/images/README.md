# Prerequisite screenshots — capture checklist

The setup guides in `00-prerequisites/` reference the images below. Each one is linked
from a guide but the PNG itself still needs to be captured and dropped into this folder.
Until a real PNG exists, the image link renders as a broken image on GitHub — that's
expected, and the caption under each link points here.

**How to use this list:** capture each screenshot, save it in this folder with the
**exact filename** shown, and the link in the matching doc will resolve automatically.
The repo's `.gitignore` ignores `*.png` in general but allows
`00-prerequisites/images/*.png`, so these screenshots can be committed.

**Before you capture:** never include a real secret in a screenshot. Blur or omit API
key values, account numbers, and anything you wouldn't paste in chat.

| Filename | Used in | What the screenshot should show |
| -------- | ------- | ------------------------------- |
| `python-add-to-path.png` | [`python-setup.md`](../python-setup.md) | The Python installer's first screen with the **"Add python.exe to PATH"** box ticked. |
| `uipath-signup.png` | [`uipath-cloud.md`](../uipath-cloud.md) | The UiPath Automation Cloud **sign-up page** showing the Community sign-up options (Google / Microsoft / email). |
| `anthropic-create-key.png` | [`api-keys.md`](../api-keys.md) | The Anthropic Console **"Create Key"** dialog with a key name filled in. Do **not** reveal a real key value. |
| `aws-create-account-button.png` | [`aws-free-tier.md`](../aws-free-tier.md) | The AWS homepage with the top-right **"Create an AWS Account"** button in view. |
| `aws-plan-selection.png` | [`aws-free-tier.md`](../aws-free-tier.md) | The AWS plan-selection step with the **Free account plan** selected / highlighted. |
| `aws-budgets-create.png` | [`aws-free-tier.md`](../aws-free-tier.md) | The AWS Budgets **"Create budget"** screen with the **Zero spend budget** template chosen. |
| `kiro-download.png` | [`kiro-install.md`](../kiro-install.md) | The **kiro.dev** download / getting-started page showing the Windows installer download. |
