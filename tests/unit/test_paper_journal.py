from __future__ import annotations

from pathlib import Path

from monster_strategy_lab.validation.paper_journal import (
    WATCH_STATUS_PENDING,
    write_paper_watch_journal,
    write_paper_watch_journal_template,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def _case_path(replay_id: str) -> Path:
    return REPO_ROOT / "replay" / "cases" / f"{replay_id}.md"


def test_only_paper_review_queued_candidates_get_journal_templates():
    case_paths = [_case_path(replay_id) for replay_id in ["HR-001", "HR-002", "HR-003", "HR-004", "HR-005", "HR-006", "HR-008", "HR-009", "HR-016", "HR-017", "HR-018", "HR-019", "HR-021", "HR-022", "HR-024", "HR-032", "HR-033", "HR-034", "HR-035"]]
    md_path, csv_path, readme_path, rows = write_paper_watch_journal(REPO_ROOT, case_paths)

    assert md_path.exists()
    assert csv_path.exists()
    assert readme_path.exists()
    assert [row.candidate_id for row in rows] == ["PTC-004", "PTC-005", "PTC-009", "PTC-017", "PTC-019", "PTC-021", "PTC-022", "PTC-024", "PTC-032", "PTC-034", "PTC-035"]
    assert all(row.watch_status == WATCH_STATUS_PENDING for row in rows)
    assert all(row.broker_action_allowed is False for row in rows)
    assert all(row.candidate_id not in {"PTC-016", "PTC-018", "PTC-033"} for row in rows)

    for row in rows:
        path = write_paper_watch_journal_template(REPO_ROOT, row)
        assert path.exists()


def test_blocked_candidates_do_not_get_journal_rows():
    case_paths = [_case_path(replay_id) for replay_id in ["HR-001", "HR-002", "HR-003", "HR-006", "HR-008", "HR-016", "HR-018", "HR-033"]]
    _, _, _, rows = write_paper_watch_journal(REPO_ROOT, case_paths)
    assert rows == []


def test_journal_readme_and_templates_include_manual_only_boundary():
    case_paths = [_case_path(replay_id) for replay_id in ["HR-004", "HR-005", "HR-009", "HR-017", "HR-019", "HR-032", "HR-034", "HR-035"]]
    _, _, readme_path, rows = write_paper_watch_journal(REPO_ROOT, case_paths)
    readme = readme_path.read_text().lower()
    assert "manual paper-watch tracking only" in readme
    assert "no broker action" in readme
    assert "no alpaca submission" in readme
    assert "no position sizing" in readme

    for row in rows:
        text = write_paper_watch_journal_template(REPO_ROOT, row).read_text().lower()
        assert "no trade signal" in text
        assert "no profitability claim" in text
        assert "no broker action" in text
        assert "no alpaca submission" in text
        assert "broker_action_allowed: false" in text


def test_no_alpaca_or_broker_dependency_is_introduced():
    module_text = (REPO_ROOT / "src/monster_strategy_lab/validation/paper_journal.py").read_text().lower()
    assert "from monster_strategy_lab.alpaca" not in module_text
    assert "import alpaca" not in module_text
    assert "submit_order" not in module_text
    assert "broker_api" not in module_text
