---
name: create-pr
description: Create a GitHub pull request from the current branch, using the repo's PR template
allowed-tools: Bash, Read, Glob, Grep, Agent, mcp__github__create_pull_request
argument-hint: "[base_branch] [--draft] [--title 'PR title']"
---

# Create Pull Request

Open a pull request from the current branch. This skill only opens the PR — it never
commits, and it never pushes.

Run `/pre-pr-check` first.

## Arguments

`$ARGUMENTS` may contain:
- First positional arg: base branch (default: the repo's default branch, `main`)
- `--draft`: open as a draft
- `--title 'PR title'`: override the generated title

## Steps

### 1. Gather context

Run in parallel:

```bash
git remote -v
git branch -vv --contains HEAD
git status -s
gh api repos/<OWNER>/<REPO> --jq '.default_branch'
```

Determine the remote, the owner/repo, and the base branch (from `$ARGUMENTS`, else the
repo's default branch).

### 2. Check the branch is pushed

Verify the branch exists on the remote. If it does not, **stop and tell the developer to
push it** — do not push on their behalf.

If the working tree is dirty, warn that the uncommitted changes will not be in the PR.

### 3. Verify the commits before drafting anything

```bash
git log --format='%H%n%an <%ae>%n%b%n---' <base>..HEAD
```

Stop and report, rather than opening the PR, if any commit:

- lacks its required `Signed-off-by:` trailers — a commit by the repo owner needs **both**
  `quaid@iquaid.org` and `karsten@tensormesh.ai`; anyone else signs off once, as themselves
- carries a `Co-Authored-By:` trailer naming a model, or a "generated with" banner — this
  repo's commits are authored by humans only (`AGENTS.md` § Commit Authorship)

The same rule binds the PR body you are about to write: no model attribution, no
"generated with" footer. Do not add one.

These are cheap to fix before the PR exists and annoying to fix after.

### 4. Read the PR template

```
Glob: .github/PULL_REQUEST_TEMPLATE.md
Glob: .github/pull_request_template.md
```

### 5. Analyze the changes

```bash
git log --oneline <base>..HEAD
git diff <base>..HEAD --stat
git diff <base>..HEAD          # if the change is small enough to read whole
```

### 6. Draft the PR

- **Title** — `--title` if given, else generate one under 70 characters. It must start with
  a type tag: a bracketed type (`[Doc]`, `[Bugfix]`, `[Core]`, `[CI]`, `[Build]`, `[Test]`,
  `[Misc]`) or a conventional-commit type (`docs:`, `fix:`, `feat:`, `ci:`, `chore:`).
  Name the component when it helps — `[Intake][Doc] ...` or `docs(intake): ...`.
- **Body** — fill in the template's sections. Lead with **why** the change is needed and
  what a reviewer should look at first. Tick the checkboxes that apply, including the
  skeleton-sync and parse-contract ones when the change touches the skeleton. Do not
  enumerate per-file changes; the reviewer can read the diff.
- **Link the issue** — `Fixes #N` to close on merge, `Refs #N` for context only.

Show the drafted title and body and **ask for confirmation before creating the PR.**

### 7. Create it

Use `mcp__github__create_pull_request` with the owner, repo, `head` (the branch), `base`,
title, body, and `draft` if requested.

### 8. Report

Print the PR URL, and remind the developer that opening a PR notifies nobody in particular:
post the link in `#lmcache-content` with a one-line summary so a human knows it is waiting.

## Important Notes

- Never push, never commit. This skill opens PRs from branches that are already pushed.
- Always show the title and body for confirmation first.
- One logical change per PR. If the diff spans unrelated concerns, say so and suggest a
  split rather than opening one big PR.
