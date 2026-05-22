from __future__ import annotations

from pathlib import Path

from monster_strategy_lab.validation.paper_review import (
    PAPER_REVIEW_STATUS_PENDING_HUMAN_APPROVAL,
    write_paper_review_plan,
    write_paper_review_queue,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def _case_path(replay_id: str) -> Path:
    return REPO_ROOT / "replay" / "cases" / f"{replay_id}.md"


def test_only_ready_candidates_enter_paper_review_queue():
    case_paths = [
        _case_path("HR-001"),
        _case_path("HR-002"),
        _case_path("HR-003"),
        _case_path("HR-004"),
        _case_path("HR-005"),
        _case_path("HR-009"),
        _case_path("HR-006"),
        _case_path("HR-008"),
        _case_path("HR-016"),
        _case_path("HR-017"),
        _case_path("HR-018"),
        _case_path("HR-019"),
        _case_path("HR-021"),
        _case_path("HR-022"),
        _case_path("HR-024"),
        _case_path("HR-032"),
        _case_path("HR-033"),
        _case_path("HR-034"),
        _case_path("HR-035"),
    ]
    md_path, csv_path, rows = write_paper_review_queue(REPO_ROOT, case_paths)

    assert md_path.exists()
    assert csv_path.exists()
    assert [row.candidate_id for row in rows] == ["PTC-004", "PTC-005", "PTC-009", "PTC-017", "PTC-019", "PTC-021", "PTC-022", "PTC-024", "PTC-032", "PTC-034", "PTC-035"]
    assert all(row.paper_review_status == PAPER_REVIEW_STATUS_PENDING_HUMAN_APPROVAL for row in rows)
    assert all(row.broker_action_allowed is False for row in rows)
    assert all(row.candidate_id not in {"PTC-016", "PTC-018", "PTC-033"} for row in rows)


def test_generated_paper_review_plans_include_boundary_language():
    case_paths = [_case_path(replay_id) for replay_id in ["HR-004", "HR-005", "HR-009", "HR-017", "HR-019", "HR-032", "HR-034", "HR-035"]]
    _, _, rows = write_paper_review_queue(REPO_ROOT, case_paths)
    for row in rows:
        path = write_paper_review_plan(REPO_ROOT, row)
        text = path.read_text().lower()
        assert path.exists()
        assert "no trade signal" in text
        assert "no profitability claim" in text
        assert "no broker action" in text
        assert "no alpaca submission" in text
        assert "broker_action_allowed: false" in text


def test_queue_excludes_blocked_candidates_and_keeps_broker_action_false():
    case_paths = [_case_path(replay_id) for replay_id in ["HR-016", "HR-018", "HR-006", "HR-001", "HR-002", "HR-003", "HR-033"]]
    _, _, rows = write_paper_review_queue(REPO_ROOT, case_paths)
    assert rows == []
