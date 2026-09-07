---
name: pre-pr-check
description: Check local changes against this repo's standards and fix what is mechanically fixable, before creating a PR
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, Agent
argument-hint: "[--scope uncommitted|branch|staged] [--fix|--check-only]"
---

# Pre-PR Check

Check the current changes against the standards in `AGENTS.md` and fix what can be fixed
mechanically, so the PR is clean before it is opened.

Run this **before** `/create-pr`.

## Arguments

- `--scope` (default: `branch`)
  - `uncommitted` — unstaged + staged changes vs `HEAD`
  - `staged` — staged changes only
  - `branch` — every commit on this branch not yet in `main` (the full PR diff). Default,
    because it matches what a reviewer sees.
- `--fix` (default) — fix what is mechanically fixable
- `--check-only` — report only, modify nothing

## Workflow

### Step 0 — Load the standard

Read `AGENTS.md`. It is authoritative. Note especially § Commit Authorship, § Writing Prose,
and § Pipeline-Specific Rules for Agents.

### Step 1 — Detect scope

```bash
git status --short
git branch --show-current
```

| Scope | Diff | File list |
|---|---|---|
| `uncommitted` | `git diff HEAD` | `git diff --name-only HEAD` |
| `staged` | `git diff --cached` | `git diff --cached --name-only` |
| `branch` | `git diff main...HEAD` | `git diff --name-only main...HEAD` |

If the scope has no changes, say so and stop.

### Step 2 — Read the changed files

Read the current content of each changed file, not just the diff, so edits are accurate.
For a large change, delegate a per-file summary to the Explore agent first.

### Step 3 — Run the checks

#### A. Mechanical (fix unless `--check-only`)

1. **Prose over 80 columns** in any `.md` file under `docs/`, in `README.md`, or in a
   template. Rewrap. Do not reflow paragraphs you did not otherwise touch — that turns a
   two-line diff into a twenty-line one.
2. **Skeleton drift.** If `.github/ISSUE_TEMPLATE/blog-post.md` changed, re-copy it:
   `cp .github/ISSUE_TEMPLATE/blog-post.md docs/templates/blog-post-skeleton.md`.
   The canonical direction is always `.github/` → `docs/`, never the reverse.
3. **Banned words** in prose or in generator instructions: "leverage", "utilize",
   "seamlessly", "revolutionary", "in today's fast-paced world", "delve", "robust
   solution". Replace with the plain word.
4. **Trailing whitespace, missing final newline, CRLF line endings.**
5. **Missing SPDX header** — `# SPDX-License-Identifier: Apache-2.0` on line 1 of every
   new `.py` file.
6. **Python typing gaps** (`AGENTS.md` § Python): missing type hints, `Any`, bare generics
   (`list` → `list[str]`), `Optional[X]` → `X | None`.
7. **`assert` used for runtime validation** → `if not cond: raise ValueError(...)`.
8. **Lazy imports** → move to the top of the file under the right section heading.

#### B. Docstrings (fix when the content is clear; flag when it is not)

9. **Missing docstring** on a public Python function. If the purpose is obvious from the
   code, write a full one (summary, args, returns, raises). If it is not, write what you can
   and leave a `TODO: confirm` plus a note in the report.
10. **Stale docstring** — a parameter was added or its meaning changed and the docstring
    still describes the old contract.

#### C. Judgment calls (flag; do NOT silently change)

11. **A `##` heading in the skeleton was renamed, reordered, or removed.** This breaks the
    parser. The parse-contract table in `docs/pipeline/skeleton-to-prompt.md` must change in
    the same PR. Report as **error** if it did not.
12. **The intake agreement is out of step.** The issue template,
    `docs/blog-submission-process.md`, and `docs/pipeline/skeleton-to-prompt.md` are three
    views of one agreement. If the diff touches one and the others now describe something
    different, report it.
13. **The skeleton got longer.** If a `[CORE]` section was added or an existing one grew,
    ask what got cut. The five core fields have a ten-minute budget; that budget is the
    whole reason contributors fill it in.
14. **An invented number**, or a number without its conditions (hardware, model, batch size,
    workload shape) in the same sentence or the adjacent one. Report as **error**.
15. **A claim not traceable** to the skeleton, the diff, or a linked issue, missing from the
    claims ledger. Report as **error**.
16. **`Notes for the editor` content leaking** into anything that gets published.
17. **A customer name, embargo date, credential, token, or internal-only URL** anywhere in
    the diff. Report as **error**.
18. **Brand-boundary violation** — Tensormesh originating LMCache-canonical content, or the
    reverse.
19. **Upstream board mutation** — a plan or script that relabels, assigns, transitions, or
    closes an issue in `LMCache/LMCache`. Report as **error**.
20. **New Python without tests**, or a bug fix without a regression test.
21. **PR scope too large** — the diff spans unrelated concerns. Suggest a split.

### Step 4 — Apply fixes

Use `Edit` for precise, minimal changes. Preserve existing voice and formatting. Re-read
after editing to confirm the change applied.

Category C is never auto-fixed. Report it.

### Step 5 — Check the commits

```bash
git log --format='%H%n%an <%ae>%n%b%n---' main..HEAD
```

For every commit on the branch, verify:

- the required `Signed-off-by:` trailers are present (report as **error** if missing). A
  commit by the repo owner needs **both** `quaid@iquaid.org` and `karsten@tensormesh.ai`;
  anyone else signs off once, as themselves. The fix is a rebase, which the developer runs,
  not you
- the author line carries a plain name and no parenthetical handle — `Karsten Wade
  <quaid@iquaid.org>`, not `Karsten Wade (quaid) <...>`, which is what a local `user.name`
  often supplies
- **no** `Co-Authored-By:` trailer naming a model, and no "generated with" banner (report as
  **error**; this repo's authorship stays human — `AGENTS.md` § Commit Authorship). Check the
  PR body too, not just the commits
- the author is a human, not an agent identity

### Step 6 — Final verification

Print these for the developer to run. Do not run them yourself.

```bash
pre-commit run --all-files     # or: uvx pre-commit run --all-files
```

## Output Format

### Summary
- Scope: `<uncommitted|staged|branch>`
- Files changed: `<N>`
- Issues found: `<total>` (auto-fixed: `<N>`, manual: `<N>`)

### Auto-fixed
Grouped by category with `file:line` references.

### Manual review required
Grouped by severity — **error** (must fix before the PR), **warning** (should fix), **info**
(suggestion) — each with `file:line` and a one-line explanation.

### Commands to run next

### Summary table

| Category | Auto-fixed | Manual | Total |
|---|---|---|---|

## Rules

- Only touch files in the selected scope. Do not "improve" unchanged files.
- Never add error handling, validation, or abstraction the task does not require.
- When a fix needs judgment, flag it rather than guessing.
- Never run `git add`, `git commit`, or `git push`. Git is the developer's.
- Never run `pre-commit` yourself; print the command.
- If `AGENTS.md` is missing, stop and ask the developer to pull the latest `main`.
