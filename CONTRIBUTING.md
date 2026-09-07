# Contributing

There are two different things people come here to do, and they have almost nothing in
common. Pick your half.

- **You want a blog post written** about a PR you landed, or an idea you have.
  → [Submitting a blog post](#submitting-a-blog-post). You will not write the post.
- **You want to change the pipeline** — the template, the docs, the tooling.
  → [Changing the pipeline](#changing-the-pipeline).

---

## Submitting a blog post

Read **[`docs/blog-submission-process.md`](docs/blog-submission-process.md)**. It has three
intake paths; pick whichever is least annoying for you.

The short version: open a new issue and choose the **Blog post from a PR** template, fill in
the five sections marked `[CORE]`, and submit. Ten minutes is a normal amount of time to
spend. A draft comes back to you within a day, and you review it before it goes out.

Two things worth repeating, because they are the ones people get wrong:

- **Write in whatever language you think in.** Do not translate for us. Translating on the
  way in loses the details that make a post good, and we localize on the way out anyway.
- **Rough is fine.** Fragments, typos, and lunch-table explanations are exactly right. The
  skeleton is notes, not prose.

---

## Changing the pipeline

This repo follows the **LMCache project standards for agentic contributors**, because what it
produces flows upstream into `LMCache/LMCache`. The full standard, including the small set of
repo-specific bindings, is in **[`AGENTS.md`](AGENTS.md)** — it applies to humans and agents
alike, and it is the document a reviewer will hold your PR against.

### 1. Before you write

For anything beyond a typo, open an issue first and say what you intend to change. The
template, the process doc, and the parse contract are three views of one agreement; a change
to any of them usually implies a change to the others, and that is worth agreeing on before
you start.

Keep each PR small and focused on one logical change.

### 2. Branch and commit

The default branch is `main`. Base all new branches and pull requests against `main`.

```bash
git switch main
git pull
git switch -c docs/my-change
```

Branch names are `<type>/<short-slug>` — `docs/`, `chore/`, `feat/`, `fix/`, `ci/`.

Every commit must carry a `Signed-off-by` trailer certifying that you agree to the
[Developer Certificate of Origin](DCO). Use `-s` and git adds it for you:

```bash
git commit -s -m "[Doc] Describe the change"
```

If you forget, `git commit --amend -s` fixes the last commit and `git rebase --signoff main`
fixes a whole branch.

**Maintainer note:** commits by the repo owner carry **two** sign-offs rather than one,
because this repo sits in two contexts at once — a personal namespace holding LMCache
content produced on behalf of Tensormesh. `git commit -s` cannot emit both; see
[`AGENTS.md` § Commit Authorship](AGENTS.md#commit-authorship) for the command. If you are
not the repo owner, sign off once, as yourself.

**Commits are authored by a human, never by an AI.** If you used an agent — and you are
encouraged to — the commit still carries your name and no model attribution: no
`Co-Authored-By:` trailer naming a model, no "generated with" banner, in the commit message
**or the PR body**. This repo publishes editorial content under a human byline, so authorship
stays human all the way down. (This is a deliberate divergence from LMCache upstream, which
does ask for an agent co-author trailer.)

### 3. Check your work locally

```bash
pre-commit run --all-files

# or, without installing anything
uvx pre-commit run --all-files
```

That runs whitespace and end-of-file hygiene, YAML/JSON/TOML validation, `codespell`, and the
skeleton-sync check. Once there is Python in the repo it also runs the SPDX-header check,
`ruff`, `isort`, and `mypy`.

If you changed the skeleton, remember it lives in two places and they must stay
byte-identical:

```bash
cp .github/ISSUE_TEMPLATE/blog-post.md docs/templates/blog-post-skeleton.md
```

`AGENTS.md` explains why it is a copy and not a symlink.

### 4. Open the pull request

Push the branch and open a PR against `main`.

- **Title** — start with a type tag, matching LMCache practice. Either a bracketed type
  (`[Doc]`, `[Bugfix]`, `[Core]`, `[CI]`, `[Build]`, `[Test]`, `[Misc]`) or a
  conventional-commit type (`docs:`, `fix:`, `feat:`, `ci:`, `chore:`, `refactor:`, `test:`).
  Naming the component as well helps a reviewer — `[Intake][Doc] ...` or `docs(intake): ...`.
- **Description** — fill in the [PR template](.github/PULL_REQUEST_TEMPLATE.md): what the PR
  does and why it is needed, and anything a reviewer should look at first.
- **Link the issue** — `Fixes #12` closes it on merge; `Refs #12` links it for context
  without closing.
- **Open it as a draft** if you want early feedback, and mark it ready when it is done.

### 5. Review

Reviewers work from the checklist at the end of [`AGENTS.md`](AGENTS.md). Reading it first
tells you what they will look for. Address feedback by pushing more commits to the same
branch, each one signed off — merges are squashed, so there is no need to tidy your history.

---

## Working with agents in this repo

Agents are first-class contributors here, and the repo is configured for them:

- **[`AGENTS.md`](AGENTS.md)** — the cross-agent policy file (Claude Code, Copilot, Cursor,
  Gemini). Human-owned: an agent should report guidance it thinks is missing rather than
  edit the file.
- **[`CLAUDE.md`](CLAUDE.md)** — Claude Code's entry point, pointing at the above.
- **`.claude/skills/`** — committed skills for the PR flow: `/pre-pr-check` before you open
  a PR, `/create-pr` to open it.

The pipeline-specific rules in `AGENTS.md` are the load-bearing ones — never invent a number,
never state one without its conditions, every unsourced claim goes in the claims ledger,
`Notes for the editor` is never published. Those exist because a post that gets one of them
wrong has to be retracted, not edited.

---

## Code of Conduct

Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).

## Who to ask

Karsten, in `#lmcache-content`. If the pipeline produces something wrong, say so in the
issue rather than fixing it silently — the corrections are how it gets better.
