---
name: Blog post from an existing draft
about: You already wrote the whole post. Skip the drafting lanes and go straight to review.
title: "[blog][draft] "
labels: ["blog", "draft"]
---

<!--
USE THIS ONE ONLY IF THE POST IS ALREADY WRITTEN.

If you have notes, an idea, or a PR you want written up, you want "Blog post
from a PR" instead. That one takes about ten minutes and someone else does
the writing.

This template exists because a finished post should not go back through
drafting. Your card skips Idea, Claimed, and Drafting and lands directly in
the review lane you pick below.

Most of this is one line per section. The one that takes real thought is
"Where your claims come from" — read that one before you start.

Do not delete any headings. The pipeline reads them by name. Leave a heading
empty rather than removing it.
-->

```yaml
draft:                # link to the doc, or attach the file to this issue
entry_lane: editorial # editorial | technical | translations
author:
language: en          # the language the DRAFT is written in: en, zh, ko, ja, de...
post_type: how-to     # how-to | why-to | deep-dive | release-note
placement: lmcache    # lmcache | tensormesh — see "Placement" below
pr:                   # if it is about a PR; leave blank if not
repo: LMCache/LMCache
reader: # who is this for? e.g. "someone running vLLM in production and hitting TTFT limits"
publish_by: # date, or leave blank
```

## Where the draft is [CORE]

<!-- A link, or say "attached" and drag the file onto this issue. Google Doc,
markdown file, HTML, Notion page — whatever you have. If it is a doc, share
it so anyone at Tensormesh with the link can comment.

If the draft lives in more than one place, say which one is authoritative.
Two versions of a finished post is the most expensive kind of confusion
here. -->

## What it says in one sentence [CORE]

<!-- The hallway version. Used for title candidates and the meta
description, and it tells a reviewer what they are about to read. -->

## Which lane it should enter [CORE]

<!-- Set `entry_lane` above and say why in a sentence.

  editorial    — written and you are happy with it, nobody has edited it.
                 This is the normal choice. Goes to Editorial review.
  technical    — an editor has already been through it for structure and
                 register, and what it needs is a correctness check.
                 Goes to Technical review.
  translations — it has been through editorial AND technical somewhere
                 else, e.g. published on another site first, and all it
                 needs is localizing. Goes to Translations.

Claiming a later lane than the draft has earned costs more time than it
saves — it gets sent back, and the round trip is slower than the review you
skipped. When you are unsure, pick editorial. -->

## Who has already reviewed it

<!-- Names and what they looked at. "Nobody" is a fine answer and is the
common one. If a reviewer's comments are in the doc, say so — that saves
the next reviewer from re-raising the same points. -->

## Where your claims come from [CORE]

<!-- THIS IS THE FIELD THAT MATTERS MOST HERE, and it is the one thing this
path needs that a generated draft gets for free.

A generated draft arrives with a claims ledger: every factual assertion that
did not come from the author's skeleton or the PR diff, listed with a pointer
to where it appears. Technical review then just checks the ledger. Your draft
does not have one, so without this section a reviewer has to re-verify the
whole piece from scratch, and that is what turns "already written" into the
slowest path instead of the fastest.

So: for each non-obvious factual claim in the post, where did it come from?
A PR or commit, an issue, a benchmark you ran, a doc, a paper, a
conversation. Bullet list is perfect. Link where you can.

Flag anything you are unsure of. "I think this is right but I did not verify
it" is genuinely useful to a reviewer and costs you nothing. -->

## Numbers and their conditions

<!-- Every benchmark or measurement in the draft, and the conditions it
holds under: hardware, model, batch size, workload shape. We will not
publish a number without its conditions, so if the draft has a number whose
conditions are not written down next to it, this is where you supply them.

If the draft has no numbers in it, say "none" and move on. -->

## Images and assets

<!-- Do you have diagrams, screenshots, or charts? Attach them or link them,
and say whether they are final or want redrawing. If a diagram needs
redrawing, describe what it should show in a sentence or two and we will draw
it. -->

## Who should care and what should they do [CORE]

<!-- Who should read this, and what is the very next thing they should do
after reading? Upgrade? Set a flag? Try a config? Read a doc? If the draft
already ends with this, just say "in the draft". -->

## What is still open

<!-- Known limits, edge cases that do not work yet, follow-up PRs, anything
you would like a reviewer to push back on. -->

## Placement

<!-- Is this LMCache-canonical or Tensormesh? Set `placement` above.

LMCache content is published as LMCache's. Tensormesh does not originate
LMCache content — so if you are unsure, say so here rather than guessing,
and it gets settled before anything is scheduled. -->

## Notes for the editor

<!-- Not published. Anything we should avoid saying, a customer we should
not name, an embargo date, a competitor comparison you would rather we did
not draw, how to spell your name and what title you want on the byline.

Also: how much editing are you comfortable with? Some people want a light
copy-edit only. Say so and we will respect it. -->
