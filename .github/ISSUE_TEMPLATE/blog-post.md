---
name: Blog post from a PR
about: Turn a pull request into a story worth reading
title: "[blog] "
labels: ["blog", "skeleton"]
---

<!--
HOW TO USE THIS

Write in whatever language you think in. Chinese, English, anything.
Do NOT translate for us — translating loses the details that make a post
good, and we localize later anyway.

Write the way you would explain this to a teammate at lunch. Rough is
fine. Fragments are fine. Typos are fine. A writer and a model turn this
into a post; you do not have to write the post.

IN A HURRY? Fill in only the five fields marked [CORE]. That is a real,
usable skeleton and should take about ten minutes.

Do not delete any headings. The pipeline reads them by name. Leave a
heading empty rather than removing it.
-->

```yaml
pr: https://github.com/LMCache/LMCache/pull/
repo: LMCache/LMCache
author:
language: en          # the language YOU wrote this skeleton in: en, zh, ko, ja, de...
post_type: how-to     # how-to | why-to | deep-dive | release-note
reader: # who is this for? e.g. "someone running vLLM in production and hitting TTFT limits"
publish_by: # date, or leave blank
```

## The one-liner

<!-- One sentence. If you told someone in the hallway what this PR does,
what would you say? Not the commit message — the hallway version. -->

## What was wrong before [CORE]

<!-- 2-4 sentences. What was broken, missing, slow, or annoying? How did
it actually show up — an error, a graph going the wrong way, a user
complaint, your own frustration? Be specific about the symptom. -->

## Why it mattered [CORE]

<!-- Who felt this and how much did it cost them? Latency, memory, money,
ops toil, blocked work. Numbers if you have them, honest hand-waving if
you don't ("roughly a third of requests", "every restart"). -->

## What we did [CORE]

<!-- The approach in your own words, not the diff. What is the idea? And
just as important: what else could we have done, and why didn't we? The
road not taken is usually the most interesting paragraph in the post. -->

## The interesting part [CORE]

<!-- THIS IS THE MOST IMPORTANT FIELD. If you fill in one thing at length,
make it this one. Any of these, or all of them:

  - What surprised you?
  - What did you try first that did not work?
  - What constraint made this harder than it looked?
  - What is the thing you would warn the next person about?
  - Was there a moment where you realized the problem was not what you
    thought it was?

Without this, we can only publish a changelog. With it, we can publish
something people send to each other. -->

## Show me the code [CORE]

<!-- Paste the smallest snippet that makes it click. Before/after if that
helps. Paste it — do not describe it. Include the file path. -->

## Numbers

<!-- Benchmarks, before/after, throughput, memory, TTFT. Crucially: under
what conditions do these hold? Hardware, model, batch size, workload
shape. We will not publish a number without its conditions. -->

## Who should care and what should they do [CORE]

<!-- Who should read this, and what is the very next thing they should do
after reading? Upgrade? Set a flag? Try a config? Read a doc? -->

## What is still open

<!-- Known limits, edge cases that do not work yet, follow-up PRs, things
you would like help with. Being honest here earns more trust than any
amount of polish. -->

## Pictures in your head

<!-- When you were working on this, what did you picture? A diagram of the
flow? A before/after of where data sits? A timeline? Describe it plainly
in a sentence or two and we will draw it. "A box for the GPU, a box for
CPU memory, an arrow that used to go both ways and now only goes one
way." -->

## Anything else

<!-- Related PRs and issues, prior art, the discussion thread where this
was argued out, papers, people who should be credited by name. -->

## Notes for the editor

<!-- Not published. Anything we should avoid saying, a customer we should
not name, an embargo date, a competitor comparison you would rather we
did not draw, how to spell your name and what title you want on the
byline. -->
