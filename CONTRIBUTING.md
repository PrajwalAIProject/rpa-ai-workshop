# Contributing

Thanks for helping improve the AI & RPA Workshop. Fixes to the docs, clearer setup steps,
and the screenshots the guides are waiting on are all welcome.

## How to contribute

1. **Fork** this repository to your own account.
2. Create a **branch** off `main` with a short, descriptive name
   (e.g. `fix-python-setup-typo` or `add-uipath-signup-screenshot`).
3. Make your change, keeping it focused — one topic per branch.
4. Open a **pull request** against `main`. Describe what you changed and why, and link any
   issue it addresses.

## Where to add screenshots

The setup guides reference screenshots that still need capturing. Add them to
[`00-prerequisites/images/`](00-prerequisites/images/) using the **exact filenames** in
the capture checklist at
[`00-prerequisites/images/README.md`](00-prerequisites/images/README.md) — the matching
image link in each guide then resolves automatically. **Never include a real secret in a
screenshot:** blur or omit API key values, account numbers, and anything you wouldn't
paste in chat.

## Coding conventions

- **Python:** keep the sample scripts simple and readable — they're teaching material.
  Match the existing style; prefer clear names and small functions.
- **Secrets:** keep every secret in a local `.env` only (it is git-ignored). **Never
  commit API keys, SMTP passwords, or tokens.** Copy `.env.example` to `.env` for your own
  values.
- **Docs:** match the student-friendly voice — second person, short sentences, wrapped
  prose. Cross-link instead of duplicating other docs. Use backtick-wrapped relative links
  like [`00-prerequisites/README.md`](00-prerequisites/README.md).

## Reporting issues

Open a **GitHub issue** describing what you expected, what happened, and the steps to
reproduce it. Screenshots or exact error messages help a lot.
