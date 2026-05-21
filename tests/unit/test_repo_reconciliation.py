from __future__ import annotations

from pathlib import Path

import csv
import yaml

from monster_strategy_lab.validation.paper_journal import write_paper_watch_journal, write_paper_watch_journal_template
from monster_strategy_lab.validation.paper_review import write_paper_review_plan, write_paper_review_queue


REPO_ROOT = Path(__file__).resolve().parents[2]
FULL_ARTIFACT_ROOT = "/home/scott/projects/openclaw-historical-market-data-extraction/artifacts/published/monster_historical_data_strategy_lab_1d_5m_v1.0"
READY_CANDIDATES = ["PTC-004", "PTC-005", "PTC-009", "PTC-017", "PTC-019"]
BLOCKED_CANDIDATES = ["PTC-001", "PTC-002", "PTC-003", "PTC-006", "PTC-008", "PTC-016", "PTC-018"]
EXPECTED_SYMBOLS = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "AVGO", "IWM"]


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def test_artifact_index_points_to_full_11_symbol_handoff_and_not_smoke() -> None:
    path = REPO_ROOT / "data_refs/historical_market_data/artifact_index.yaml"
    data = yaml.safe_load(path.read_text())

    assert data["artifact_root"] == FULL_ARTIFACT_ROOT
    assert "monster_historical_data_smoke_v1.0" not in data["artifact_root"]
    assert data["symbols"] == EXPECTED_SYMBOLS
    assert data["timeframes"] == ["1Day", "5Min"]
    assert data["allowed_for_replay"] == ["1Day", "5Min"]
    assert data["blocked_for_replay"] == ["1Min"]
    assert all(item["timeframe"] in {"1Day", "5Min"} for item in data["items"])
    assert all("sample" not in item["path"] for item in data["items"])
    assert any("deprecated" in note.lower() or "sample" in note.lower() for note in data["notes"])


def test_replay_discovery_config_uses_full_handoff_and_blocks_1min() -> None:
    path = REPO_ROOT / "configs/replay_discovery.yaml"
    data = yaml.safe_load(path.read_text())

    assert data["replay_data_root"] == FULL_ARTIFACT_ROOT
    assert data["handoff_manifest_path"] == f"{FULL_ARTIFACT_ROOT}/strategy_lab_handoff.yaml"
    assert data["symbols"] == EXPECTED_SYMBOLS
    assert data["required_timeframes"] == ["1Day", "5Min"]
    assert data["blocked_timeframes"] == ["1Min"]
    assert data["deprecated_sample_sources"] == ["data_refs/google_drive"]


def test_paper_review_queue_includes_ready_candidates_and_excludes_blocked() -> None:
    case_paths = sorted((REPO_ROOT / "replay/cases").glob("HR-*.md"))
    md_path, csv_path, queue_rows = write_paper_review_queue(REPO_ROOT, case_paths)
    for row in queue_rows:
        write_paper_review_plan(REPO_ROOT, row)

    rows = _read_csv_rows(csv_path)
    text = md_path.read_text()

    assert len(rows) == 5
    assert [row["candidate_id"] for row in rows] == READY_CANDIDATES
    assert all(row["paper_review_status"] == "pending_human_approval" for row in rows)
    assert all(row["broker_action_allowed"] == "false" for row in rows)
    for candidate_id in READY_CANDIDATES:
        assert candidate_id in text
        assert (REPO_ROOT / "runs/paper_review" / f"{candidate_id}-paper-review-plan.md").exists()
    for candidate_id in BLOCKED_CANDIDATES:
        assert candidate_id not in text


def test_paper_watch_journal_index_matches_queued_candidates_and_keeps_broker_action_false() -> None:
    case_paths = sorted((REPO_ROOT / "replay/cases").glob("HR-*.md"))
    md_path, csv_path, _, journal_rows = write_paper_watch_journal(REPO_ROOT, case_paths)
    for row in journal_rows:
        write_paper_watch_journal_template(REPO_ROOT, row)

    rows = _read_csv_rows(csv_path)
    text = md_path.read_text()

    assert len(rows) == 5
    assert [row["candidate_id"] for row in rows] == READY_CANDIDATES
    assert all(row["watch_status"] == "pending" for row in rows)
    assert all(row["broker_action_allowed"] == "false" for row in rows)
    for candidate_id in READY_CANDIDATES:
        assert candidate_id in text
        assert (REPO_ROOT / "runs/paper_journal" / f"{candidate_id}-journal.md").exists()
    for candidate_id in BLOCKED_CANDIDATES:
        assert candidate_id not in text
