from __future__ import annotations

from pathlib import Path
from datetime import date

import yaml

from monster_strategy_lab.replay import load_replay_case
from monster_strategy_lab.validation.paper_readiness import (
    BLOCKED_BY_AMBIGUITY,
    BLOCKED_BY_FAILED_RECLAIM,
    BLOCKED_BY_INSUFFICIENT_DATA,
    BLOCKED_BY_NO_TRIGGER,
    BLOCKED_BY_TARGET_NOT_HIT,
    READY_FOR_PAPER_REVIEW,
    assess_replay_case,
    write_paper_readiness_matrix,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def _case_path(replay_id: str) -> Path:
    return REPO_ROOT / "replay" / "cases" / f"{replay_id}.md"


def _write_case(path: Path, data: dict, body: str = "# temp\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\n" + yaml.safe_dump(data, sort_keys=False).rstrip() + "\n---\n" + body)


def _load_and_assess(replay_id: str):
    return assess_replay_case(load_replay_case(_case_path(replay_id)))


def test_confirmed_breakout_and_breakdown_are_ready_for_paper_review():
    for replay_id in ["HR-004", "HR-005", "HR-009", "HR-017", "HR-019", "HR-032", "HR-034", "HR-035"]:
        result = _load_and_assess(replay_id)
        assert result.readiness_status == READY_FOR_PAPER_REVIEW
        assert result.eligible_for_paper_review is True
        assert result.broker_action_allowed is False


def test_target_not_hit_confirmation_blocks_paper_review():
    result = _load_and_assess("HR-033")
    assert result.replay_status == "VERIFIED"
    assert result.replay_outcome == "insufficient"
    assert result.classification == "confirmed_breakdown_no_target_hit"
    assert result.readiness_status == BLOCKED_BY_TARGET_NOT_HIT
    assert result.eligible_for_paper_review is False
    assert result.broker_action_allowed is False


def test_ambiguous_failed_reclaim_target_not_hit_and_watch_cases_block_paper_review():
    expectations = {
        "HR-016": BLOCKED_BY_AMBIGUITY,
        "HR-018": BLOCKED_BY_FAILED_RECLAIM,
        "HR-008": BLOCKED_BY_FAILED_RECLAIM,
        "HR-006": BLOCKED_BY_TARGET_NOT_HIT,
        "HR-001": BLOCKED_BY_NO_TRIGGER,
        "HR-002": BLOCKED_BY_NO_TRIGGER,
    }
    for replay_id, expected in expectations.items():
        result = _load_and_assess(replay_id)
        assert result.readiness_status == expected
        assert result.eligible_for_paper_review is False
        assert result.broker_action_allowed is False


def test_not_verified_and_insufficient_block_paper_review():
    for replay_id in ["HR-001", "HR-003"]:
        result = _load_and_assess(replay_id)
        assert result.readiness_status in {BLOCKED_BY_NO_TRIGGER, BLOCKED_BY_INSUFFICIENT_DATA}
        assert result.broker_action_allowed is False


def test_synthetic_fixture_cannot_reach_paper_review(tmp_path: Path):
    case = load_replay_case(_case_path("HR-017"))
    data = dict(case.raw)
    data.update(
        {
            "replay_id": "HR-synth",
            "related_candidate_id": "PTC-synth",
            "evidence_type": "synthetic_fixture",
            "real_market_evidence": False,
            "replay_status": "VERIFIED",
            "replay_outcome": "confirmed",
            "classification": "confirmed_breakout",
            "manual_review_status": "completed",
            "manual_review_outcome": "confirmed",
            "manual_review_classification": "confirmed_breakout",
            "manual_reviewer_notes": "synthetic fixture only",
            "broker_action_allowed": False,
        }
    )
    path = tmp_path / "replay/cases/HR-synth.md"
    _write_case(path, data)
    result = assess_replay_case(load_replay_case(path))
    assert result.readiness_status == BLOCKED_BY_INSUFFICIENT_DATA
    assert result.broker_action_allowed is False


def test_ready_matrix_marks_broker_action_false(tmp_path: Path):
    paths = [
        _case_path("HR-004"),
        _case_path("HR-005"),
        _case_path("HR-009"),
        _case_path("HR-006"),
        _case_path("HR-008"),
        _case_path("HR-016"),
        _case_path("HR-017"),
        _case_path("HR-018"),
        _case_path("HR-019"),
        _case_path("HR-032"),
        _case_path("HR-033"),
        _case_path("HR-034"),
        _case_path("HR-035"),
    ]
    _, _, rows = write_paper_readiness_matrix(tmp_path, paths)
    assert rows
    assert all(row.broker_action_allowed is False for row in rows)
    assert any(row.readiness_status == READY_FOR_PAPER_REVIEW for row in rows)
    ready_ids = {row.replay_id for row in rows if row.readiness_status == READY_FOR_PAPER_REVIEW}
    assert {"HR-032", "HR-034", "HR-035"}.issubset(ready_ids)
    assert "HR-033" not in ready_ids
