# Docs

Three documents, three audiences. Start with whichever describes you.

| Document | Who it is for |
|---|---|
| [`blog-submission-process.md`](blog-submission-process.md) | **A contributor who landed a PR.** The three intake paths, and what happens to your card after you submit. Start here. |
| [`templates/blog-post-skeleton.md`](templates/blog-post-skeleton.md) | **The skeleton itself**, as a file you can download and fill in for intake path C. Byte-identical to the issue template. |
| [`pipeline/skeleton-to-prompt.md`](pipeline/skeleton-to-prompt.md) | **Whoever is building or debugging the pipeline.** Parse contract, PR hydration, prompt assembly, output contract, claims ledger — plus the two smaller contracts for already-written posts. |

## The one-paragraph version

LMCache merges more good PRs than anyone has time to write up. So contributors do not write
posts — they write a **skeleton**: rough notes, in their own language, about what was broken
and what was interesting about fixing it. The pipeline hydrates that skeleton with the PR's
own metadata and diff, assembles a prompt, and generates a draft. A human editor and the
original author review it before it goes out.

The exception is a post that is already written. Those take one of the other two templates
and skip the drafting lanes entirely — see paths D and E in the process doc, and templates
two and three in the parse contract.

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

## The three issue templates

| Template | For | Enters at | Technical review? |
|---|---|---|---|
| `blog-post.md` | notes about a PR; someone else writes the post | Drafting | yes |
| `blog-post-draft.md` | written, but the technical content still needs checking | Editorial or Technical review | **yes — that is the point** |
| `blog-post-complete.md` | written *and* already technically sound | Editorial review | **no — skips to Translations** |

The last two both take an already-written post, and the **only** thing separating them is
whether the technical content still needs checking. Most already-written submissions are the
third kind: a post by the person who built the thing, or one from another org that already
reviewed it. Template two is the exception.

Only the first has a downloadable copy under `templates/`, because only the first hands you a
file to fill in offline. A finished post is already a file.

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
