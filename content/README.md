# Content

Where the actual material lives, as opposed to the process that produces it. The process
docs are in [`../docs/`](../docs/).

| Directory | What goes in it |
|---|---|
| `skeletons/` | Filled-in skeletons committed through intake path C, named `<pr-number>.md`. |

## skeletons/

Intake path C lets a contributor commit a filled skeleton alongside their code rather than
pasting it into an issue. Those land here as `content/skeletons/<pr-number>.md` — the PR
number from `LMCache/LMCache`, so `content/skeletons/1234.md`.

Use the template at
[`../docs/templates/blog-post-skeleton.md`](../docs/templates/blog-post-skeleton.md) and
keep the `##` headings exactly as they are: the parser reads them by name.

A skeleton committed here still needs an issue on the content board linking to it. The file
is the working surface; the issue is the tracking record.

## Not here yet

Drafts, published posts, and image assets do not have a home in this repo yet. Where they
land depends on the WordPress publishing service, which is a later phase. Do not invent a
directory for them without an issue agreeing on the layout first.
