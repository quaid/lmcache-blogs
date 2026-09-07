# Board routing

How an issue becomes a card in the right column, and — more to the point — what
happens to the ones that do not fit any rule.

The mechanism is `.github/workflows/content-board.yml` plus
[`tools/board_router.py`](../../tools/board_router.py). The board is
**LMCache Blogs [Editorial Kanban]**, project 5 under `quaid`.

## Setup — one secret, and it is required

**`GITHUB_TOKEN` cannot write to a user-owned Projects V2 board.** There is no
workflow permission that grants it; Projects V2 is outside the repository
permission model. So the workflow needs its own token.

1. Create a fine-grained personal access token with **read and write access to
   your projects**, or a classic token with the **`project`** scope.
2. Add it to this repo as a secret named **`PROJECT_TOKEN`**
   (Settings → Secrets and variables → Actions).

A GitHub App installation token with project permissions works too, and is the
better long-term answer if this ever moves under the LMCache org.

**Until that secret exists, routing does not happen** — and the workflow says so
loudly rather than failing one API call at a time and looking like an outage.
The `preflight` job writes a plain-English notice to the run summary and emits a
warning annotation. Issues still get filed and labelled correctly in the
meantime; they are just not on the board, and the first sweep after the secret
lands will place every one of them.

## The routing table

Routing keys off labels, because a label is visible, editable, and searchable by
a human. Path D is refined by the `entry_lane` value in its YAML block, since
which review a draft has earned is not something a label can express.

| Labels | Column | Triage? |
|---|---|---|
| `skeleton` | Drafting | no |
| `needs-tech-review` + `entry_lane: editorial` | Editorial review | no |
| `needs-tech-review` + `entry_lane: technical` | Technical review | no |
| `needs-tech-review`, no `entry_lane` | Editorial review | no — the documented default |
| `needs-tech-review` + an unrecognised `entry_lane` | Editorial review | **yes** |
| `tech-verified` | Editorial review | no |
| more than one of the three intake labels | Idea | **yes** |
| `blog`, but no intake label | Idea | **yes** |
| `pipeline` | *off the board* | no |
| neither `blog` nor `pipeline` | *off the board* | **yes** |

## Nothing is ignored, and nothing dead-ends

That is the property the router is built for, and it is worth stating exactly
what it does and does not promise.

**Every input produces a decision.** `route()` is total: any set of labels
returns a column, or an explicit and justified decision to stay off the board,
and in every case a one-sentence reason. There is no fall-through branch. The
test suite asserts this exhaustively over every combination of the labels in
play, crossed with valid and invalid lanes — see
[`tests/test_board_router.py`](../../tests/test_board_router.py).

**An issue the router cannot place gets flagged, not dropped.** It receives the
`needs-triage` label *and* a comment naming why, so it is both findable
(`is:issue is:open label:needs-triage`) and self-explanatory when found. The
comment is written once; re-runs do not re-comment.

**Off the board is a decision, never an accident.** Only two cases land there,
and one of them still gets triaged. A `pipeline` issue stays off deliberately —
the board's columns are editorial lanes and "Published" means nothing for a
parser bug — so it lives in the repo's issue list where it belongs. An issue
with neither label is off the board *and* triaged, because nobody has said what
kind of work it is.

**A wrong guess is never silent.** An unrecognised `entry_lane` still gets a
card, because leaving it off the board is the worse failure — but it is triaged,
because every lane is a review and picking one by inference would silently skip
a check on something about to be published.

**Ambiguity beats precedence.** Two intake labels means the author's intent is
unknowable. The router could let one win by branch order; instead it routes to
Idea and triages, because arbitrary precedence is exactly how a card ends up in
the wrong review.

**Late is allowed, absent is not.** The `issues` event handles arrivals. The
hourly `sweep` job walks every open issue and routes any that is not already on
the board — which covers issues that predate the workflow, arrived while it was
broken, or were missed for any reason. `workflow_dispatch` runs it on demand,
with a `dry_run` input that decides and logs without changing anything.

**Labels cannot silently vanish.** GitHub drops an issue-template label that
does not exist in the repository, with no error anywhere — which would leave
every intake issue unlabelled and therefore unroutable. This bit us already: all
seven template labels were missing when the templates were first written. The
`ensure-labels` job now reads whatever the templates declare and creates
anything absent, so the templates are self-healing.

## What this does not do

Named so nobody assumes otherwise:

- **It never moves a card forward.** Routing sets a card's *entry* column. Once
  a human moves it, the router leaves it alone — it only touches issues that are
  not on the board yet. Nothing here advances work through the lanes.
- **No stall detection.** The process doc promises a nudge when a card waits on
  someone for more than two days. That needs Slack and is not built.
- **No closed-issue handling.** A closed issue keeps its card wherever it was.
  Whether "closed" means abandoned or published is a policy question nobody has
  answered yet.

## Running it locally

```bash
export GH_TOKEN=$(gh auth token)
export PROJECT_TOKEN=<a token with project scope>

# What would happen, changing nothing
python tools/board_router.py sweep --repo quaid/lmcache-blogs --dry-run

# One issue
python tools/board_router.py route --repo quaid/lmcache-blogs --issue 12 --dry-run
```

Tests:

```bash
pip install -r requirements/test.txt
pytest tests/ -q
```

## Changing the rules

The routing table above, `route()` in the router, and the `Routing` sections of
the parse contracts are three views of one agreement — the same trap the
templates and the process doc are in. If you change a label, a lane, or a
column:

1. Update `route()` and its tests. A new column must be added to the assertion
   in `test_every_routed_column_is_a_real_column`.
2. Update this table and the parse contract's `Routing` section.
3. Confirm the column exists on the board. The router raises rather than
   guessing if it does not, so a typo fails loudly, but it fails at runtime
   rather than in review.
