# Docs

Three documents, three audiences. Start with whichever describes you.

| Document | Who it is for |
|---|---|
| [`blog-submission-process.md`](blog-submission-process.md) | **A contributor who landed a PR.** The three intake paths, and what happens to your card after you submit. Start here. |
| [`templates/blog-post-skeleton.md`](templates/blog-post-skeleton.md) | **The skeleton itself**, as a file you can download and fill in for intake path C. Byte-identical to the issue template. |
| [`pipeline/skeleton-to-prompt.md`](pipeline/skeleton-to-prompt.md) | **Whoever is building or debugging the pipeline.** Parse contract, PR hydration, prompt assembly, output contract, claims ledger. |

## The one-paragraph version

LMCache merges more good PRs than anyone has time to write up. So contributors do not write
posts — they write a **skeleton**: rough notes, in their own language, about what was broken
and what was interesting about fixing it. The pipeline hydrates that skeleton with the PR's
own metadata and diff, assembles a prompt, and generates a draft. A human editor and the
original author review it before it goes out.

## These three documents are one agreement

The issue template, the process doc, and the parse contract describe the same thing from
three angles, and they drift silently:

- The skeleton's `##` headings are the **parser's schema**. Renaming, reordering, or
  deleting one is a breaking change.
- The process doc promises contributors a specific set of fields and a ten-minute budget for
  the five marked `[CORE]`.
- The parse contract says which fields are required, and what each one is *for* in the
  finished post.

Change one, check the other two. A PR that touches a heading without touching the parse
contract table will be sent back — see the checklist in [`../AGENTS.md`](../AGENTS.md).

## Where the skeleton lives

`.github/ISSUE_TEMPLATE/blog-post.md` is **canonical** — GitHub's template chooser only
reads that directory. `docs/templates/blog-post-skeleton.md` is a byte-identical copy,
because intake path C needs a file a contributor can download and attach, and a symlink does
not survive `raw.githubusercontent.com`. `tools/check_skeleton_sync.sh` fails pre-commit if
the two drift. Edit the canonical one, then:

```bash
cp .github/ISSUE_TEMPLATE/blog-post.md docs/templates/blog-post-skeleton.md
```

## Not here yet

Named in the pipeline plan, still to be written:

- The **whitePrint style definition** the image stage depends on.
- The **Google Doc** copy of the skeleton for intake path B, and its link in the process doc.
- The **parser** implementing the parse contract, across all three intake surfaces.
- The **prompt assembler**: hydration, claims ledger, `QUESTION FOR AUTHOR` emission.
