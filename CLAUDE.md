# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this repository.

## Read First

**[AGENTS.md](AGENTS.md)** is the authoritative agent policy for this repo: the standards it
follows, the layout, commit authorship, PR conventions, prose and Python style, the
pipeline-specific rules, and the review checklist. Read it before writing anything.

**[CONTRIBUTING.md](CONTRIBUTING.md)** covers the human-facing flow — how to submit a blog
post, and how to change the pipeline.

This repo adopts the LMCache project standards for agentic contributors, with a small set of
repo-specific bindings (base branch is `main`, not `dev`; no AI co-author trailers). AGENTS.md
has the full table.

## The Two Things Most Likely to Trip You Up

1. **Commits carry two DCO sign-offs and no AI attribution.** Both of Karsten's
   identities sign off — `quaid@iquaid.org` and `karsten@tensormesh.ai` — because the work
   sits in both contexts. `git commit -s` produces only one, so set the trailers explicitly;
   AGENTS.md § Commit Authorship has the command. And no `Co-Authored-By:` trailer naming a
   model, no "generated with" banner, in commits **or PR bodies**.
2. **The skeleton lives in two places and must stay byte-identical.**
   `.github/ISSUE_TEMPLATE/blog-post.md` is canonical; `docs/templates/blog-post-skeleton.md`
   is a copy for intake path C. `tools/check_skeleton_sync.sh` enforces it in pre-commit.

## Docs Map

| Document | What it is |
|---|---|
| [`docs/blog-submission-process.md`](docs/blog-submission-process.md) | Contributor-facing. The three intake paths and what happens to a card. |
| [`docs/pipeline/skeleton-to-prompt.md`](docs/pipeline/skeleton-to-prompt.md) | Machine-facing. Parse contract, hydration, prompt assembly, output contract, claims ledger. |
| [`.github/ISSUE_TEMPLATE/blog-post.md`](.github/ISSUE_TEMPLATE/blog-post.md) | The skeleton itself. Its `##` headings are the parser's schema. |
| [`.github/ISSUE_TEMPLATE/blog-post-draft.md`](.github/ISSUE_TEMPLATE/blog-post-draft.md) | Intake for a post that is already written. Skips the drafting lanes; its `sources` section stands in for the claims ledger. |

When a change touches one of these, check whether it needs to touch the others. The process
doc, the template, and the parse contract are three views of one agreement, and they drift
silently.

## Skills

The PR flow has committed skills — use them rather than improvising:

- **`/pre-pr-check`** — check the branch against this repo's standards and fix what is
  mechanically fixable, before opening a PR.
- **`/create-pr`** — open the PR from an already-pushed branch, using the repo's PR template.

## Working Agreements

- Prose wraps at 80 columns. See AGENTS.md § Writing Prose for the rest of the house style.
- Keep PRs small and focused; one logical change each.
- Upstream `LMCache/LMCache` issues and PRs are read-only reference. Never relabel, assign,
  transition, or close an issue this project does not own.
- Never invent a number, and never state one without its conditions. This applies to docs
  and to anything the pipeline generates.
