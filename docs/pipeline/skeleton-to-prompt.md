# Skeleton → prompt

How a filled skeleton becomes the prompt that generates a "story of a PR"
post. This is the pipeline-facing half of the template pair.

The skeleton it parses lives at
[`.github/ISSUE_TEMPLATE/blog-post.md`](../../.github/ISSUE_TEMPLATE/blog-post.md)
(canonical) and [`../templates/blog-post-skeleton.md`](../templates/blog-post-skeleton.md)
(the downloadable copy). Its `##` headings are this document's schema: change
one there and the parse contract below changes in the same PR, or the parser
silently drops a field.

## Why the skeleton is markdown and not a YAML issue form

GitHub's YAML issue forms give you cleaner parsing. We are not using them,
on purpose.

There are three intake surfaces — issue body, attached `.md` file, exported
Google Doc — and a YAML form only works on one of them. A markdown skeleton
with stable `##` headings is the same artifact on all three, which means one
parser, one prompt assembler, one thing to maintain. The headings are the
schema.

Cost of this choice: nothing enforces that a heading is filled in, so the
parser has to handle empty sections gracefully (see "Empty required field"
below). That is a cheap problem. Three divergent formats is an expensive one.

If we later want form validation, the upgrade path is to add a YAML form
that *emits* this exact markdown as the issue body. The downstream pipeline
does not change.

## Parse contract

Split the document on `^## ` headings. Strip HTML comments — they are
instructions to the human, never input to the model. Front matter is the
fenced `yaml` block at the top.

A skeleton that arrives as an attached `.md` file (path C) also carries a
`---`-delimited block above that fenced block: GitHub issue-template metadata
(`name`, `about`, `title`, `labels`). It is not skeleton content. Discard it.
It is absent when the skeleton arrives as an issue body, because GitHub
consumes it when creating the issue.

**Strip the ` [CORE]` suffix before matching a heading against the table below.**
Five headings carry it — it tells a contributor in a hurry which fields to fill
in first, and it is part of the literal heading text a splitter returns. So the
raw heading is `What was wrong before [CORE]` and the field name is
`What was wrong before`. Match on the stripped name; a parser that matches the
raw text will silently drop exactly the five fields that carry the post.

| Skeleton field | Machine key | Required |
|---|---|---|
| front matter | `meta.*` | `pr`, `author`, `language`, `post_type` |
| The one-liner | `oneliner` | no |
| What was wrong before | `problem` | **yes** |
| Why it mattered | `stakes` | **yes** |
| What we did | `approach` | **yes** |
| The interesting part | `story` | **yes** |
| Show me the code | `code` | **yes** |
| Numbers | `numbers` | no |
| Who should care and what should they do | `cta` | **yes** |
| What is still open | `open` | no |
| Pictures in your head | `imagery` | no |
| Anything else | `refs` | no |
| Notes for the editor | `editor_notes` | no — **never rendered** |

## Hydration

Before the prompt is assembled, the bundle is enriched from the PR named in
front matter:

- PR title, description, merge date, author, reviewers
- Full diff, plus a file-level summary (paths, lines changed)
- Linked issues and their bodies
- Review conversation, if any (this is often where `story` material hides
  when the author left that field thin)

## Field → function in the post

The generator is told what each field is *for*, not just that it exists.
This is what stops the output reading like a changelog.

- `oneliner` → title candidates, meta description, and the lede
- `problem` → the opening. The hook is the symptom, not the solution
- `stakes` → the paragraph that earns the reader's next two minutes; also
  drives SEO framing and keyword selection
- `approach` → the first body section, including the road not taken
- `story` → **the narrative spine.** At least one section is built around
  this, and the author's specific phrasing is preserved where it is
  colorful. This is the difference between a post and a release note
- `code` → rendered verbatim with the file path, plus explanation. Never
  reformatted, never "improved"
- `numbers` → results section. Every figure carries its conditions in the
  same sentence or the adjacent one
- `cta` → a "who this is for" line near the top, and the closing action
- `open` → an honest limitations section, kept as a section rather than
  softened into an aside
- `imagery` → image prompts, routed to the whitePrint style; not rendered
  as prose
- `refs` → inline links and credits
- `editor_notes` → constraints on the generator. Never appears in output

## Output contract

The generator returns:

1. Three title options, marked for SEO weight
2. Slug and meta description
3. Target keywords, with the primary one named
4. The post, in markdown, with the PR linked in the first two paragraphs
5. Image prompt list — one per idea in `imagery`, plus at most one the
   generator proposes itself, clearly marked as proposed
6. **Claims ledger** (see below)
7. `QUESTION FOR AUTHOR` blocks, if any

## The claims ledger

The reliability mechanism. Every factual assertion in the draft that did not
come from the skeleton, the diff, or a linked issue gets listed at the end
with a pointer to where it appears in the post.

Technical review then becomes a bounded task — check the ledger — instead of
re-reading the whole piece hunting for invention. This is the single thing
that most reduces edit time per piece, which is the number we are reporting
upward.

## Rules the generator is given

- Do not invent numbers. Not one. If `numbers` is empty, the post has no
  benchmarks in it
- Do not state a number without its conditions
- Do not claim a capability the diff does not show
- Preserve the author's voice in `story`. If they wrote something vivid,
  keep their words rather than smoothing them into house style
- House style applies to structure, register, and clarity — not to the
  author's specific descriptions
- Write for someone who has the problem, not for someone admiring the fix
- Second person. Present tense. No "revolutionary", no "seamlessly", no
  "in today's fast-paced world"
- The post must be useful even to a reader who never adopts the change

## Empty required field

Do not fabricate and do not silently proceed. Emit:

```
QUESTION FOR AUTHOR — [field]
[the specific question, referencing what the diff appears to show]
```

The pipeline posts these as a comment on the issue and moves the card back
to the author's column. A draft with open questions never advances to
editorial.

## Prompt skeleton (assembled)

```
You are drafting a technical blog post for the LMCache project.

HOUSE STYLE
{house_style_block}

WHAT YOU ARE WRITING
A "story of a PR" post: type {meta.post_type}, for this reader:
{meta.reader}. The narrative spine is the author's account in THE
INTERESTING PART. Build the piece around it.

The author wrote this skeleton in {meta.language}. Write the post in
English. Preserve their specific descriptions and examples; do not
flatten their voice into generic technical prose.

AUTHOR'S SKELETON
{all populated fields, labeled, verbatim}

THE PULL REQUEST
{pr_metadata}
{file_summary}
{diff}
{linked_issues}
{review_conversation}

CONSTRAINTS FROM THE EDITOR
{editor_notes}

RULES
{rules_block}

RETURN
{output_contract}
```

## Human feedback loops

Every edit made downstream is signal. Three capture points, per the
pipeline design:

1. **Drafting** — diffs between generated draft and author-revised draft
2. **Editorial** — diffs between author-revised and editor-approved
3. **Localization** — idiomatic changes a localizing reviewer makes

Store the diff, the field it traces back to, and the reason if the editor
gives one. These feed prompt revisions and few-shot examples, and they are
how the edit-minutes number comes down over time.
