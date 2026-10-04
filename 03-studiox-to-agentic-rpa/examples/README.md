# Example UiPath projects

Real, working UiPath automations you can open in **UiPath Studio** to see how a finished
workflow is put together — a useful reference when you rebuild your own BCG701 exercise
in Studio (see [`../basic/README.md`](../basic/README.md)).

> These are **third-party projects** by their original authors, not written for this
> workshop. Each is credited below. Respect each project's own license.

---

## Included here

### `input-forms-rpa-challenge/` — RPA Challenge: Excel → dynamic web forms

A complete UiPath workflow that reads data from a spreadsheet and types it into a web
form whose fields **move position after every submission** — a classic exercise in
robust selectors and `For Each` loops over a `DataTable`.

- **Author:** Maxine Xiong
- **Source:** <https://github.com/MaxineXiong/Input-Forms-RPA-Challenge>
- **License:** MIT (see [`input-forms-rpa-challenge/LICENSE`](input-forms-rpa-challenge/LICENSE)) — © 2023 Maxine Xiong
- **Open it:** launch UiPath Studio → **Open a Local Project** → select
  `input-forms-rpa-challenge/project.json`.
- **Good for:** seeing selectors, `Read Range`, `For Each Row`, and type-into activities
  in a real project.

---

## Referenced (clone it yourself)

### LearningRPA — 13+ beginner UiPath processes

A collection of small, focused processes that line up almost one-to-one with the BCG701
syllabus: Excel read/write/append, email, notepad automation, web scraping, loops,
if/else, exception handling, PDF text extraction, and more.

- **Author:** sidchigo
- **Source:** <https://github.com/sidchigo/LearningRPA>
- **License:** **none specified.** Because the repo has no license, the author retains
  all rights and we do **not** redistribute its files inside this (MIT) repo. Clone it
  directly from the author instead:

  ```bash
  git clone https://github.com/sidchigo/LearningRPA.git
  ```

  Then open any `.xaml` (or `project.json`) in UiPath Studio.
- **Good for:** the closest match to what you already built in StudioX, now as full
  Studio projects.

---

## How to open a UiPath project

1. Install / sign in to **UiPath Studio** — see
   [`../../00-prerequisites/uipath-cloud.md`](../../00-prerequisites/uipath-cloud.md).
2. In Studio: **Open a Local Project** and pick the project's `project.json`.
3. Studio restores the dependencies listed in `project.json`, then you can open
   `Main.xaml` and run or step through it.

> Attribution matters. If you reuse any of these workflows in your own public work, keep
> the original author's credit and license. Content references were kept minimal for
> compliance with licensing restrictions.
