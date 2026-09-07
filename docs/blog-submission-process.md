# How to get a blog post written

Three ways in. All three end in the same place: a card on the board with a
skeleton attached. Pick whichever is least annoying for you.

**You do not write the post.** You write a skeleton — rough notes in your
own language — and the pipeline plus an editor turn it into a post. You
review it before it goes out.

**Write in your own language.** Do not translate for us. Translating on the
way in loses the details that make a post good, and we localize on the way
out anyway.

---

## Path A — Issue template (default, start here)

Best for: most people, most of the time. Fastest path if you are already in
GitHub.

1. Go to the content board and [open a new
   issue](https://github.com/quaid/lmcache-blogs/issues/new/choose). Choose
   **Blog post from a PR**.
2. Fill in the YAML block at the top — the PR link and your name are the
   only ones that matter.
3. Fill in the five `[CORE]` sections. Ten minutes is a normal amount of
   time to spend. Leave the rest blank if you are busy.
4. Submit. Your card lands in **Drafting** automatically.
5. Within a day you get a Slack DM with a generated draft attached to the
   issue.
6. Read it. If there are `QUESTION FOR AUTHOR` blocks, answer them in a
   comment — the card comes back to you until they are cleared.
7. Comment "looks right" or push corrections. Card moves to **Editorial
   review**.
8. You get one more look at technical review before it publishes.

---

## Path B — Google Doc

Best for: you would rather write in a doc, you want a colleague to help you
fill it in, or you are drafting on a phone.

1. Open the **Blog Post Skeleton** template in Drive and make a copy.
   (File → Make a copy. Do not edit the template itself.)
2. Fill it in the same way as Path A. Keep the headings — do not delete or
   rename them.
3. Share the copy so anyone at Tensormesh with the link can comment.
4. Open a blank issue on the content board, title it `[blog] <your one-liner>`,
   and paste the doc link as the whole body.
5. The pipeline reads the doc, pulls the fields, and rewrites the issue body
   with the parsed skeleton and the right labels.
6. From here it is identical to Path A, step 5 onward. Edits continue in the
   doc — the issue is the tracking record, the doc is the working surface.

---

## Path C — Attach a markdown file

Best for: you already wrote notes somewhere, you live in your editor, or you
want this in the same PR as your code.

1. Grab the skeleton from this repo — [`docs/templates/blog-post-skeleton.md`](templates/blog-post-skeleton.md),
   or download it straight from
   [raw](https://raw.githubusercontent.com/quaid/lmcache-blogs/main/docs/templates/blog-post-skeleton.md)
   — or write plain markdown using the same `##` headings.
2. Fill it in.
3. Either:
   - drag the `.md` file onto a new blank issue on the content board, or
   - commit it to `content/skeletons/<pr-number>.md` in a PR and open an
     issue linking to it.
4. Title the issue anything. You do not need to fill in the body.
5. The pipeline reads the attachment, derives the metadata from the front
   matter, and **rewrites the issue title, body, and labels to match**. You
   do not have to keep them in sync by hand.
6. From here it is identical to Path A, step 5 onward.

---

## If you already wrote the whole post

Open an issue, attach or link it, and say so. It skips the idea and drafting
columns and drops straight into **Editorial review**, or into **Translations**
if it is already been through editorial elsewhere.

## If it is not about a PR

The skeleton still works — leave `pr:` blank and set `post_type` to `why-to`.
`What was wrong before` and `The interesting part` are still the two fields
that carry the piece.

## What happens to your card

```
Idea → Claimed → Drafting → Editorial review → Technical review → Translations → Published
```

You get a Slack DM when your card moves and when something needs you. If a
card sits waiting on you for more than two days, you get a nudge.

## Who to ask

Karsten, in `#lmcache-content`. If the pipeline produces something wrong,
say so in the issue rather than fixing it silently — the corrections are how
it gets better.
