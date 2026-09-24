# Moving this repository to the LMCache organization

Written while preparing the move, so the steps are the ones that were actually
verified rather than the ones that sounded right.

The repository is **transfer-ready**: nothing in the code names an owner any
more. What follows is what a human still has to do, in order, and what will
break if a step is skipped.

## What GitHub moves for you

Confirmed against GitHub's own documentation:

- **Issues, pull requests, wiki, stars, and watchers** come along.
- **All links to the old location redirect** to the new one — including `git
  remote` URLs, so nobody's clone breaks.
- **Webhooks, secrets, and deploy keys stay associated** after the transfer.
  This one is easy to assume otherwise; `PROJECT_TOKEN` survives.
- Git history, forks, and LFS objects are preserved.

## What does not move, and will silently break

**The project board.** A GitHub Projects V2 board belongs to a *user or an
organization*, never to a repository. Transferring the repo leaves the board
exactly where it is. The cards keep pointing at the issues, and the workflow
keeps writing to the old board, because as far as it is concerned nothing
happened.

This is the one that bites, because nothing errors.

## Before the transfer

1. **Karsten needs membership in the LMCache org with permission to create
   repositories.** GitHub requires create-repo rights in the *target* org to
   transfer into it. Without it the transfer cannot be initiated at all — this
   is a hard blocker, not a formality.
2. Decide who ends up with **admin** on the repo afterwards. A transfer makes
   the receiving org's owners admins; confirm the humans who need it have it.

## The transfer

Initiated by the source owner, from Settings → General → Danger Zone →
Transfer, or:

```bash
gh api -X POST repos/quaid/lmcache-blogs/transfer -f new_owner=LMCache
```

## After the transfer, in order

1. **Create the board in the org.** A new Projects V2 board under `LMCache`,
   with the seven columns in order:

   ```
   Idea → Claimed → Drafting → Editorial review → Technical review → Translations → Published
   ```

   The names must match exactly — the router looks them up by name and raises
   rather than guessing if one is missing.

2. **Set `BOARD_NUMBER`** (Settings → Secrets and variables → Actions →
   Variables) to the new board's number. Leave `BOARD_OWNER` unset; it defaults
   to the repository owner, which is now `LMCache`.

3. **Replace `PROJECT_TOKEN` with a narrower one.** This is the upgrade the
   move unlocks. A user-owned board could only be reached by a *classic* token
   with `project` scope, which cannot be narrowed below "every project this
   account can touch". An **org-owned** board can be reached by a **fine-grained
   PAT with the org-level `Projects` permission scoped to this one repository**,
   or by a GitHub App. Swap it, then revoke the old classic token.

4. **Move the two open issues' cards**, or just let the hourly sweep do it — it
   routes any open issue that is not already on the board.

5. **Dry-run before trusting it:**

   ```bash
   gh workflow run content-board.yml --repo LMCache/lmcache-blogs -f dry_run=true
   ```

   Read the run summary. Both current issues are `pipeline`-labelled, so the
   correct outcome is that they stay **off** the board with no triage flag. If
   the dry run wants to file them under `Idea`, the routing table and the board
   disagree about something — fix that before a real run.

6. **Re-point local clones** (optional; the redirect handles it):

   ```bash
   git remote set-url origin git@github.com:LMCache/lmcache-blogs.git
   ```

## Decisions the move forces

Neither is mechanical, and neither should be made by whoever happens to run the
transfer.

**The dual sign-off convention.** `AGENTS.md` requires two `Signed-off-by`
trailers, on the reasoning that this repo sits in two contexts at once — a
personal namespace holding LMCache content produced for Tensormesh. Once the
repo is owned by LMCache that justification no longer holds: there is one
context, and the convention collapses to a single sign-off under the
LMCache/Tensormesh identity. The rule is left as-is here so nothing changes
mid-move. Revisit it deliberately afterwards.

**Where Code of Conduct and security reports go.** `CODE_OF_CONDUCT.md` and
`SECURITY.md` currently route to `karsten@tensormesh.ai`, which was right for a
personal repo. An LMCache-owned repository should route to whatever the project
uses, so that enforcement does not depend on one person's mailbox.

## What is still not built

Unchanged by the move, listed so it is not mistaken for transfer damage:

- Nothing moves a card *forward*; routing sets the entry column only.
- No stall detection, though the process doc promises a nudge at two days.
- No closed-issue policy — whether "closed" means published or abandoned is
  [an open question](../../../issues).
