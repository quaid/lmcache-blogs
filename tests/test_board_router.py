# SPDX-License-Identifier: Apache-2.0
"""Tests for the content-board routing decision.

These exercise the public contract of :func:`route` and
:func:`parse_entry_lane` — the pure half of the router. The board writes are
not tested here; they are I/O against a live project and are covered by running
the workflow in dry-run mode.

The test that matters most is :func:`test_route_is_total`, which asserts the
property the router exists to guarantee: no combination of labels goes
unhandled.
"""

# Future
from __future__ import annotations

# Standard
from pathlib import Path
import itertools
import sys

# Third Party
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

# Third Party
from board_router import (  # noqa: E402
    COLUMN_DRAFTING,
    COLUMN_EDITORIAL,
    COLUMN_IDEA,
    COLUMN_TECHNICAL,
    TEMPLATE_LABELS,
    Decision,
    parse_entry_lane,
    route,
)

ALL_LABELS = (*TEMPLATE_LABELS, "blog", "pipeline", "bug", "documentation")


def decide(*labels: str, entry_lane: str | None = None) -> Decision:
    """Route a set of labels, for brevity in the tests below.

    Args:
        *labels: Label names on the hypothetical issue.
        entry_lane: Declared lane, if any.

    Returns:
        The routing decision.
    """
    return route(frozenset(labels), entry_lane)


class TestSkeletonPath:
    """Intake paths A, B, and C — a skeleton someone else writes up."""

    def test_skeleton_enters_drafting(self) -> None:
        result = decide("blog", "skeleton")
        assert result.column == COLUMN_DRAFTING
        assert not result.needs_triage

    def test_entry_lane_is_ignored(self) -> None:
        """A stray entry_lane on a skeleton does not divert it."""
        assert decide("blog", "skeleton", entry_lane="technical").column == (
            COLUMN_DRAFTING
        )


class TestDraftPath:
    """Intake path D — written, technical content still needs checking."""

    def test_editorial_lane(self) -> None:
        result = decide("blog", "draft", "needs-tech-review", entry_lane="editorial")
        assert result.column == COLUMN_EDITORIAL
        assert not result.needs_triage

    def test_technical_lane(self) -> None:
        result = decide("blog", "draft", "needs-tech-review", entry_lane="technical")
        assert result.column == COLUMN_TECHNICAL
        assert not result.needs_triage

    def test_missing_lane_defaults_to_editorial_without_triage(self) -> None:
        """An absent lane is the documented default, not an error."""
        result = decide("blog", "draft", "needs-tech-review", entry_lane=None)
        assert result.column == COLUMN_EDITORIAL
        assert not result.needs_triage

    @pytest.mark.parametrize("lane", ["translations", "publish", "", "editoral"])
    def test_invalid_lane_routes_but_flags(self, lane: str) -> None:
        """An unrecognised lane is a validation error, never a silent guess.

        It still lands somewhere — leaving the card off the board would be the
        worse failure — but it is flagged so a human confirms the lane.
        """
        result = decide("blog", "draft", "needs-tech-review", entry_lane=lane)
        assert result.column == COLUMN_EDITORIAL
        assert result.needs_triage
        assert lane in result.reason or "not a valid lane" in result.reason


class TestCompletePath:
    """Intake path E — written and already technically verified."""

    def test_enters_editorial_not_technical(self) -> None:
        result = decide("blog", "complete", "tech-verified")
        assert result.column == COLUMN_EDITORIAL
        assert not result.needs_triage

    def test_never_routes_to_technical_review(self) -> None:
        """Skipping Technical review is the whole point of path E."""
        for lane in (None, "editorial", "technical", "nonsense"):
            assert decide("blog", "tech-verified", entry_lane=lane).column != (
                COLUMN_TECHNICAL
            )


class TestAmbiguousAndUnclassified:
    """The cases that would otherwise become dead ends."""

    @pytest.mark.parametrize("pair", list(itertools.combinations(TEMPLATE_LABELS, 2)))
    def test_conflicting_intake_labels_are_triaged(self, pair: tuple[str, str]) -> None:
        """Two intake labels means the author's intent is unknowable.

        Precedence would let one label win arbitrarily, which silently picks a
        review path. Triage instead.
        """
        result = decide("blog", *pair)
        assert result.needs_triage
        assert result.column == COLUMN_IDEA
        for label in pair:
            assert label in result.reason

    def test_all_three_intake_labels_are_triaged(self) -> None:
        assert decide("blog", *TEMPLATE_LABELS).needs_triage

    def test_blog_without_intake_label_is_triaged_not_dropped(self) -> None:
        """A hand-made blog issue still gets a card, plus a flag."""
        result = decide("blog")
        assert result.column == COLUMN_IDEA
        assert result.needs_triage

    def test_pipeline_stays_off_board_without_triage(self) -> None:
        """Pipeline work is classified, just not editorial. Not a dead end."""
        result = decide("pipeline")
        assert result.column is None
        assert not result.needs_triage
        assert result.reason

    def test_pipeline_bug_stays_off_board(self) -> None:
        result = decide("pipeline", "bug")
        assert result.column is None
        assert not result.needs_triage

    def test_unclassified_issue_is_triaged(self) -> None:
        """A blank issue with neither label is the case most likely to rot."""
        result = decide()
        assert result.column is None
        assert result.needs_triage

    def test_unrelated_labels_alone_are_triaged(self) -> None:
        assert decide("documentation", "bug").needs_triage


class TestTotality:
    """The property the router exists to provide."""

    @pytest.mark.parametrize("size", [0, 1, 2, 3])
    def test_route_is_total(self, size: int) -> None:
        """Every label combination yields a decision with a reason.

        This is the guarantee that nothing is ignored. Any input either lands in
        a real column, or is explicitly and justifiably left off the board, and
        in every case carries a human-readable reason. Nothing returns an empty
        decision and nothing raises.
        """
        lanes: list[str | None] = [None, "editorial", "technical", "bogus"]
        for combo in itertools.combinations(ALL_LABELS, size):
            for lane in lanes:
                result = route(frozenset(combo), lane)
                assert result.reason, f"no reason for {combo} lane={lane}"
                assert result.column is None or isinstance(result.column, str)
                # Off-board without triage must be a deliberate classification.
                if result.column is None and not result.needs_triage:
                    assert "pipeline" in combo

    @pytest.mark.parametrize("size", [0, 1, 2, 3])
    def test_every_routed_column_is_a_real_column(self, size: int) -> None:
        """The router never names a column that does not exist on the board.

        The seven live columns are asserted against in the workflow itself;
        here we pin the four this router can ever produce.
        """
        allowed = {COLUMN_IDEA, COLUMN_DRAFTING, COLUMN_EDITORIAL, COLUMN_TECHNICAL}
        for combo in itertools.combinations(ALL_LABELS, size):
            column = route(frozenset(combo), None).column
            assert column is None or column in allowed


class TestParseEntryLane:
    """Reading entry_lane out of an issue body."""

    def test_reads_from_yaml_block(self) -> None:
        body = "```yaml\ndraft: http://x\nentry_lane: technical\nauthor: kw\n```"
        assert parse_entry_lane(body) == "technical"

    def test_strips_trailing_comment(self) -> None:
        assert parse_entry_lane("entry_lane: editorial # editorial | technical") == (
            "editorial"
        )

    def test_lowercases(self) -> None:
        assert parse_entry_lane("entry_lane: Editorial") == "editorial"

    def test_tolerates_leading_whitespace(self) -> None:
        assert parse_entry_lane("  entry_lane:   technical  ") == "technical"

    def test_missing_returns_none(self) -> None:
        assert parse_entry_lane("no yaml here at all") is None

    def test_empty_body_returns_none(self) -> None:
        assert parse_entry_lane("") is None

    def test_blank_value_returns_none(self) -> None:
        """An author who deleted the value gets the documented default."""
        assert parse_entry_lane("entry_lane:\nauthor: kw") is None
