from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import yaml

from monster_strategy_lab.paper import load_candidate
from monster_strategy_lab.data_sources import resolve_historical_market_data_paths
from monster_strategy_lab.replay import (
    build_bearish_draft_replay_case,
    build_draft_replay_case,
    DiversifiedReplayCandidate,
    discover_events_for_symbol,
    scan_close_below_support_candidates,
    load_replay_case,
    load_replay_discovery_config,
    scan_close_above_resistance_candidates,
    select_date_diversified_candidates,
    select_top_bearish_candidates,
    select_top_candidates,
    write_discovery_constraint_audit,
    write_date_diversified_candidates,
    write_bearish_draft_replay_case,
    write_bearish_manual_review_packet,
    write_close_below_support_csv,
    write_close_below_support_summary,
    write_draft_manual_review_packet,
    write_draft_replay_case,
    write_replay_triage_summary,
)
from monster_strategy_lab.replay.batch import write_replay_evidence_matrix
from monster_strategy_lab.validation import validate_candidate


REPO_ROOT = Path(__file__).resolve().parents[2]


def _write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = "symbol,timeframe,timestamp,open,high,low,close,volume,trade_count,vwap,source,feed,adjustment,downloaded_at\n"
    lines = [header]
    for row in rows:
        lines.append(
            ",".join(
                [
                    row["symbol"],
                    row["timeframe"],
                    row["timestamp"],
                    row["open"],
                    row["high"],
                    row["low"],
                    row["close"],
                    row.get("volume", "1"),
                    row.get("trade_count", "1"),
                    row.get("vwap", row["close"]),
                    row.get("source", "alpaca"),
                    row.get("feed", "iex"),
                    row.get("adjustment", "raw"),
                    row.get("downloaded_at", "2026-01-01T00:00:00+00:00"),
                ]
            )
            + "\n"
        )
    path.write_text("".join(lines))


def test_scanner_finds_close_above_resistance_event_in_fixture(tmp_path: Path):
    repo = tmp_path
    _write_rows(
        repo / "data_refs/google_drive/TEST_5Min_sample.csv",
        [
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:30:00+00:00", "open": "10", "high": "10.5", "low": "9.8", "close": "10.2"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:35:00+00:00", "open": "10.2", "high": "10.6", "low": "10.1", "close": "10.4"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:40:00+00:00", "open": "10.4", "high": "10.9", "low": "10.3", "close": "10.8"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:45:00+00:00", "open": "10.8", "high": "11.2", "low": "10.7", "close": "11.1"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:50:00+00:00", "open": "11.1", "high": "11.6", "low": "11.0", "close": "11.5"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:55:00+00:00", "open": "11.5", "high": "12.0", "low": "11.4", "close": "11.95"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 14:00:00+00:00", "open": "11.95", "high": "12.4", "low": "11.9", "close": "12.35"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 14:05:00+00:00", "open": "12.35", "high": "13.1", "low": "12.3", "close": "13.0"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 14:10:00+00:00", "open": "13.0", "high": "13.2", "low": "12.8", "close": "13.1"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 14:15:00+00:00", "open": "13.1", "high": "13.6", "low": "13.0", "close": "13.5"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 14:20:00+00:00", "open": "13.5", "high": "13.9", "low": "13.4", "close": "13.8"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 14:25:00+00:00", "open": "13.8", "high": "14.2", "low": "13.7", "close": "14.1"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 14:30:00+00:00", "open": "14.1", "high": "14.8", "low": "14.0", "close": "14.7"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 14:35:00+00:00", "open": "14.7", "high": "15.1", "low": "14.6", "close": "15.0"},
        ],
    )

    events = discover_events_for_symbol(repo, "TEST", lookbacks=(12,))
    assert events
    assert any(event.close > event.prior_resistance for event in events)


def test_scanner_does_not_use_current_bar_high_in_prior_resistance(tmp_path: Path):
    repo = tmp_path
    _write_rows(
        repo / "data_refs/google_drive/TEST_5Min_sample.csv",
        [
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:30:00+00:00", "open": "10", "high": "10.5", "low": "9.8", "close": "10.2"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:35:00+00:00", "open": "10.2", "high": "10.6", "low": "10.1", "close": "10.4"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:40:00+00:00", "open": "10.4", "high": "10.9", "low": "10.3", "close": "10.8"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:45:00+00:00", "open": "10.8", "high": "11.2", "low": "10.7", "close": "11.1"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:50:00+00:00", "open": "11.1", "high": "11.6", "low": "11.0", "close": "11.5"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:55:00+00:00", "open": "11.5", "high": "12.0", "low": "11.4", "close": "11.95"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 14:00:00+00:00", "open": "11.95", "high": "12.4", "low": "11.9", "close": "12.35"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 14:05:00+00:00", "open": "12.35", "high": "100.0", "low": "12.3", "close": "12.9"},
        ],
    )

    events = discover_events_for_symbol(repo, "TEST", lookbacks=(7,))
    assert events
    assert events[0].prior_resistance == 12.4


def test_wick_only_break_is_not_close_above_resistance(tmp_path: Path):
    repo = tmp_path
    _write_rows(
        repo / "data_refs/google_drive/TEST_5Min_sample.csv",
        [
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:30:00+00:00", "open": "10", "high": "10.5", "low": "9.8", "close": "10.2"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:35:00+00:00", "open": "10.2", "high": "10.6", "low": "10.1", "close": "10.4"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:40:00+00:00", "open": "10.4", "high": "10.9", "low": "10.3", "close": "10.8"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:45:00+00:00", "open": "10.8", "high": "11.2", "low": "10.7", "close": "11.1"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:50:00+00:00", "open": "11.1", "high": "11.6", "low": "11.0", "close": "11.5"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:55:00+00:00", "open": "11.5", "high": "12.0", "low": "11.4", "close": "11.95"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 14:00:00+00:00", "open": "11.95", "high": "12.4", "low": "11.9", "close": "12.0"},
        ],
    )

    events = discover_events_for_symbol(repo, "TEST", lookbacks=(6,))
    assert not events


def test_scanner_finds_close_below_support_event_in_fixture(tmp_path: Path):
    repo = tmp_path
    _write_rows(
        repo / "data_refs/google_drive/TEST_5Min_sample.csv",
        [
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:30:00+00:00", "open": "10.5", "high": "10.7", "low": "10.0", "close": "10.4"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:35:00+00:00", "open": "10.4", "high": "10.6", "low": "10.1", "close": "10.2"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:40:00+00:00", "open": "10.2", "high": "10.3", "low": "10.0", "close": "10.1"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:45:00+00:00", "open": "10.1", "high": "10.2", "low": "9.95", "close": "10.0"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:50:00+00:00", "open": "10.0", "high": "10.1", "low": "9.9", "close": "10.05"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:55:00+00:00", "open": "10.05", "high": "10.08", "low": "9.98", "close": "10.02"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 14:00:00+00:00", "open": "10.02", "high": "10.03", "low": "9.7", "close": "9.8"},
        ],
    )

    events = scan_close_below_support_candidates(repo, symbols=("TEST",), lookbacks=(6,))
    assert events
    assert events[0].close < events[0].prior_support
    assert events[0].did_price_reclaim_above_support is False


def test_bearish_draft_packet_includes_required_sections(tmp_path: Path):
    repo = tmp_path
    _write_rows(
        repo / "data_refs/google_drive/TEST_1Day_sample.csv",
        [
            {"symbol": "TEST", "timeframe": "1Day", "timestamp": "2023-05-16 04:00:00+00:00", "open": "10", "high": "10.6", "low": "9.8", "close": "10.4"},
            {"symbol": "TEST", "timeframe": "1Day", "timestamp": "2023-05-17 04:00:00+00:00", "open": "10.4", "high": "10.8", "low": "9.6", "close": "9.9"},
        ],
    )
    _write_rows(
        repo / "data_refs/google_drive/TEST_5Min_sample.csv",
        [
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:30:00+00:00", "open": "10.5", "high": "10.7", "low": "10.0", "close": "10.4"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:35:00+00:00", "open": "10.4", "high": "10.6", "low": "10.1", "close": "10.2"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:40:00+00:00", "open": "10.2", "high": "10.3", "low": "10.0", "close": "10.1"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:45:00+00:00", "open": "10.1", "high": "10.2", "low": "9.95", "close": "10.0"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:50:00+00:00", "open": "10.0", "high": "10.1", "low": "9.9", "close": "10.05"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:55:00+00:00", "open": "10.05", "high": "10.08", "low": "9.98", "close": "10.02"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 14:00:00+00:00", "open": "10.02", "high": "10.03", "low": "9.7", "close": "9.8"},
        ],
    )

    event = scan_close_below_support_candidates(repo, symbols=("TEST",), lookbacks=(6,))[0]
    draft = build_bearish_draft_replay_case(repo, event, "HR-007", "PTC-007")
    case_path = write_bearish_draft_replay_case(repo, draft)
    packet_path = write_bearish_manual_review_packet(repo, draft)

    assert case_path.exists()
    assert "classification: candidate_for_manual_review" in case_path.read_text()
    text = packet_path.read_text()
    assert "## Downside follow-through rows" in text
    assert "## Manual promotion workflow" in text


def test_generated_draft_case_remains_not_verified_and_cannot_promote(tmp_path: Path):
    repo = tmp_path
    _write_rows(
        repo / "data_refs/google_drive/TEST_1Day_sample.csv",
        [
            {"symbol": "TEST", "timeframe": "1Day", "timestamp": "2023-05-16 04:00:00+00:00", "open": "9", "high": "10", "low": "8.5", "close": "9.5"},
            {"symbol": "TEST", "timeframe": "1Day", "timestamp": "2023-05-17 04:00:00+00:00", "open": "9.5", "high": "12", "low": "9.2", "close": "11.8"},
        ],
    )
    _write_rows(
        repo / "data_refs/google_drive/TEST_5Min_sample.csv",
        [
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:30:00+00:00", "open": "10", "high": "10.5", "low": "9.8", "close": "10.2"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:35:00+00:00", "open": "10.2", "high": "10.6", "low": "10.1", "close": "10.4"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:40:00+00:00", "open": "10.4", "high": "10.9", "low": "10.3", "close": "10.8"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:45:00+00:00", "open": "10.8", "high": "11.2", "low": "10.7", "close": "11.1"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:50:00+00:00", "open": "11.1", "high": "11.6", "low": "11.0", "close": "11.5"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:55:00+00:00", "open": "11.5", "high": "12.0", "low": "11.4", "close": "11.95"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 14:00:00+00:00", "open": "11.95", "high": "12.4", "low": "11.9", "close": "12.35"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 14:05:00+00:00", "open": "12.35", "high": "12.9", "low": "12.3", "close": "12.8"},
        ],
    )

    event = discover_events_for_symbol(repo, "TEST", lookbacks=(6,))[0]
    draft = build_draft_replay_case(repo, event, "HR-004", "PTC-004")
    case_path = write_draft_replay_case(repo, draft)
    packet_path = write_draft_manual_review_packet(repo, draft)

    case = load_replay_case(case_path)
    assert case.replay_status == "NOT_VERIFIED"
    assert packet_path.exists()
    assert "Not verified replay evidence" in packet_path.read_text()

    candidate = {
        "schema": "paper_trade_candidate_v1",
        "candidate_id": "PTC-004",
        "related_phase_3_1_rule_candidate": "RC-001",
        "evidence_links": [{"link": "EX-001", "supports": "direction-model only"}],
        "replay_case_links": [{"replay_case": str(Path("replay/cases/HR-004.md")), "replay_status": "NOT_VERIFIED", "replay_outcome": "insufficient"}],
        "symbol": "TEST",
        "direction": "long",
        "timeframe_context": "1D + 5m",
        "setup_timeframe": "1D",
        "execution_timeframe": "5m",
        "support_level": 9.0,
        "resistance_level": 10.5,
        "target_price": 11.5,
        "entry_candidate_price": 10.6,
        "room_to_target": 0.9,
        "invalidation_level": 8.7,
        "confirmation_behavior": "wait",
        "confirmation_type": "close_above_resistance",
        "higher_timeframe_context": "context",
        "higher_timeframe_obstacle_check": "unknown",
        "target_already_hit_check": "unknown",
        "no_trade_filters": [{"id": "NTF-001", "status": "pass"}],
        "risk_notes": "paper-only",
        "boundary": "Paper validation only",
    }
    candidate_path = repo / "candidate.yaml"
    candidate_path.write_text(yaml.safe_dump(candidate, sort_keys=False))
    result = validate_candidate(load_candidate(candidate_path), repo_root=repo)
    assert result.paper_readiness_status != "READY_FOR_PAPER_REVIEW"
    assert result.broker_action_allowed is False


def test_date_diversified_selector_avoids_cluster_when_possible():
    selected = select_date_diversified_candidates(
        [
            DiversifiedReplayCandidate(
                replay_id="",
                symbol="AAPL",
                side="bullish",
                timestamp="2023-05-16 13:45:00+00:00",
                event_type="close_above_resistance",
                prior_level=10.0,
                breakout_or_breakdown_amount=1.0,
                lookback_bars=12,
            ),
            DiversifiedReplayCandidate(
                replay_id="",
                symbol="AAPL",
                side="bullish",
                timestamp="2023-06-20 13:45:00+00:00",
                event_type="close_above_resistance",
                prior_level=11.0,
                breakout_or_breakdown_amount=1.2,
                lookback_bars=24,
            ),
            DiversifiedReplayCandidate(
                replay_id="",
                symbol="MSFT",
                side="bearish",
                timestamp="2023-07-20 13:45:00+00:00",
                event_type="close_below_support",
                prior_level=12.0,
                breakout_or_breakdown_amount=0.8,
                lookback_bars=48,
            ),
        ],
        existing_case_dates=[date(2023, 5, 16)],
        min_calendar_days_between_cases=30,
        max_cases_per_symbol_per_month=1,
        avoid_existing_replay_windows=True,
    )

    assert {candidate.timestamp[:10] for candidate in selected} == {"2023-06-20", "2023-07-20"}


def test_date_diversified_selector_respects_min_calendar_days_between_cases():
    selected = select_date_diversified_candidates(
        [
            DiversifiedReplayCandidate(
                replay_id="",
                symbol="SPY",
                side="bullish",
                timestamp="2023-06-01 13:45:00+00:00",
                event_type="close_above_resistance",
                prior_level=10.0,
                breakout_or_breakdown_amount=1.0,
                lookback_bars=12,
            ),
            DiversifiedReplayCandidate(
                replay_id="",
                symbol="QQQ",
                side="bearish",
                timestamp="2023-06-15 13:45:00+00:00",
                event_type="close_below_support",
                prior_level=11.0,
                breakout_or_breakdown_amount=0.6,
                lookback_bars=24,
            ),
        ],
        existing_case_dates=[],
        min_calendar_days_between_cases=30,
        max_cases_per_symbol_per_month=1,
        avoid_existing_replay_windows=False,
    )

    assert len(selected) == 1
    assert selected[0].timestamp.startswith("2023-06-01")


def test_scanner_does_not_use_current_bar_low_in_prior_support(tmp_path: Path):
    repo = tmp_path
    _write_rows(
        repo / "data_refs/google_drive/TEST_5Min_sample.csv",
        [
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:30:00+00:00", "open": "10.5", "high": "10.7", "low": "10.0", "close": "10.4"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:35:00+00:00", "open": "10.4", "high": "10.6", "low": "10.1", "close": "10.2"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:40:00+00:00", "open": "10.2", "high": "10.3", "low": "10.0", "close": "10.1"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:45:00+00:00", "open": "10.1", "high": "10.2", "low": "9.95", "close": "10.0"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:50:00+00:00", "open": "10.0", "high": "10.1", "low": "9.9", "close": "10.05"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 13:55:00+00:00", "open": "10.05", "high": "10.08", "low": "9.98", "close": "10.02"},
            {"symbol": "TEST", "timeframe": "5Min", "timestamp": "2023-05-17 14:00:00+00:00", "open": "10.02", "high": "99.0", "low": "0.1", "close": "9.8"},
        ],
    )

    events = scan_close_below_support_candidates(repo, symbols=("TEST",), lookbacks=(6,))
    assert events
    assert events[0].prior_support == 9.9


def test_matrix_warns_when_cases_are_date_clustered():
    path = write_replay_evidence_matrix(REPO_ROOT)
    text = path.read_text()
    assert "clustered_windows_warning:" in text
    assert "active artifact index now points at the full 11-symbol 1Day + 5Min handoff" in text


def test_date_diversified_report_uses_full_handoff_config_and_keeps_1min_blocked():
    config = load_replay_discovery_config(REPO_ROOT)
    assert len(config.symbols) == 11
    assert config.required_timeframes == ["1Day", "5Min"]

    for symbol in ["SPY", "QQQ", "META", "NVDA"]:
        paths = resolve_historical_market_data_paths(REPO_ROOT, symbol)
        assert set(paths) == {"1Day", "5Min"}
        assert all(path.suffix == ".parquet" for path in paths.values())
        assert all("sample" not in str(path) for path in paths.values())
        assert all("1Min" not in str(path) for path in paths.values())


def test_selector_prefers_different_symbols_when_available():
    selected = select_date_diversified_candidates(
        [
            DiversifiedReplayCandidate("", "AAPL", "bullish", "2023-01-03T13:30:00+00:00", "close_above_resistance", 10.0, 1.0, 12),
            DiversifiedReplayCandidate("", "AAPL", "bullish", "2023-02-06T13:30:00+00:00", "close_above_resistance", 11.0, 1.1, 12),
            DiversifiedReplayCandidate("", "MSFT", "bullish", "2023-03-10T13:30:00+00:00", "close_above_resistance", 20.0, 1.2, 12),
            DiversifiedReplayCandidate("", "MSFT", "bullish", "2023-04-12T13:30:00+00:00", "close_above_resistance", 21.0, 1.3, 12),
            DiversifiedReplayCandidate("", "QQQ", "bullish", "2023-05-15T13:30:00+00:00", "close_above_resistance", 30.0, 1.4, 12),
            DiversifiedReplayCandidate("", "QQQ", "bullish", "2023-06-19T13:30:00+00:00", "close_above_resistance", 31.0, 1.5, 12),
        ],
        existing_case_dates=[],
        min_calendar_days_between_cases=30,
        max_cases_per_symbol_per_month=1,
        max_cases_per_symbol_total=2,
        avoid_existing_replay_windows=False,
    )

    assert len({candidate.symbol for candidate in selected[:3]}) == 3
    assert len(selected) >= 3


def test_selector_warns_when_all_selected_cases_are_same_symbol(tmp_path: Path):
    repo = tmp_path
    artifact_root = repo / "published" / "monster_historical_data_smoke_v1.0"
    full_1day = artifact_root / "symbols" / "TEST" / "1Day" / "TEST_1Day_2024.parquet"
    full_5min = artifact_root / "symbols" / "TEST" / "5Min" / "TEST_5Min_2024.parquet"
    full_1day.parent.mkdir(parents=True, exist_ok=True)
    full_5min.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([
        {"symbol": "TEST", "timeframe": "1Day", "timestamp": "2024-02-01T05:00:00+00:00", "open": 10, "high": 11, "low": 9, "close": 10.5, "volume": 1, "trade_count": 1, "vwap": 10.4, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        {"symbol": "TEST", "timeframe": "1Day", "timestamp": "2024-02-02T05:00:00+00:00", "open": 10.5, "high": 11.5, "low": 10, "close": 11, "volume": 1, "trade_count": 1, "vwap": 10.8, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        {"symbol": "TEST", "timeframe": "1Day", "timestamp": "2024-02-03T05:00:00+00:00", "open": 11, "high": 12, "low": 10.5, "close": 11.8, "volume": 1, "trade_count": 1, "vwap": 11.5, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
    ]).to_parquet(full_1day, index=False)
    start = datetime(2024, 2, 1, 14, 30, tzinfo=timezone.utc)
    rows = [
        {"symbol": "TEST", "timeframe": "5Min", "timestamp": (start + timedelta(minutes=0)).isoformat(), "open": 10.0, "high": 10.5, "low": 9.8, "close": 10.2, "volume": 1, "trade_count": 1, "vwap": 10.2, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        {"symbol": "TEST", "timeframe": "5Min", "timestamp": (start + timedelta(minutes=5)).isoformat(), "open": 10.2, "high": 10.6, "low": 10.1, "close": 10.4, "volume": 1, "trade_count": 1, "vwap": 10.4, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        {"symbol": "TEST", "timeframe": "5Min", "timestamp": (start + timedelta(minutes=10)).isoformat(), "open": 10.4, "high": 10.9, "low": 10.3, "close": 10.8, "volume": 1, "trade_count": 1, "vwap": 10.8, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        {"symbol": "TEST", "timeframe": "5Min", "timestamp": (start + timedelta(minutes=15)).isoformat(), "open": 10.8, "high": 11.2, "low": 10.7, "close": 11.1, "volume": 1, "trade_count": 1, "vwap": 11.1, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        {"symbol": "TEST", "timeframe": "5Min", "timestamp": (start + timedelta(minutes=20)).isoformat(), "open": 11.1, "high": 11.6, "low": 11.0, "close": 11.5, "volume": 1, "trade_count": 1, "vwap": 11.5, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        {"symbol": "TEST", "timeframe": "5Min", "timestamp": (start + timedelta(minutes=25)).isoformat(), "open": 11.5, "high": 12.0, "low": 11.4, "close": 11.95, "volume": 1, "trade_count": 1, "vwap": 11.95, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        {"symbol": "TEST", "timeframe": "5Min", "timestamp": (start + timedelta(minutes=30)).isoformat(), "open": 11.95, "high": 12.4, "low": 11.9, "close": 12.35, "volume": 1, "trade_count": 1, "vwap": 12.35, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        {"symbol": "TEST", "timeframe": "5Min", "timestamp": (start + timedelta(minutes=35)).isoformat(), "open": 12.35, "high": 13.1, "low": 12.3, "close": 13.0, "volume": 1, "trade_count": 1, "vwap": 13.0, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        {"symbol": "TEST", "timeframe": "5Min", "timestamp": (start + timedelta(minutes=40)).isoformat(), "open": 13.0, "high": 13.2, "low": 12.8, "close": 13.1, "volume": 1, "trade_count": 1, "vwap": 13.1, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        {"symbol": "TEST", "timeframe": "5Min", "timestamp": (start + timedelta(minutes=45)).isoformat(), "open": 13.1, "high": 13.6, "low": 13.0, "close": 13.5, "volume": 1, "trade_count": 1, "vwap": 13.5, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        {"symbol": "TEST", "timeframe": "5Min", "timestamp": (start + timedelta(minutes=50)).isoformat(), "open": 13.5, "high": 13.9, "low": 13.4, "close": 13.8, "volume": 1, "trade_count": 1, "vwap": 13.8, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        {"symbol": "TEST", "timeframe": "5Min", "timestamp": (start + timedelta(minutes=55)).isoformat(), "open": 13.8, "high": 14.2, "low": 13.7, "close": 14.1, "volume": 1, "trade_count": 1, "vwap": 14.1, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        {"symbol": "TEST", "timeframe": "5Min", "timestamp": (start + timedelta(minutes=60)).isoformat(), "open": 14.1, "high": 14.8, "low": 14.0, "close": 14.7, "volume": 1, "trade_count": 1, "vwap": 14.7, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        {"symbol": "TEST", "timeframe": "5Min", "timestamp": (start + timedelta(minutes=65)).isoformat(), "open": 14.7, "high": 15.1, "low": 14.6, "close": 15.0, "volume": 1, "trade_count": 1, "vwap": 15.0, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
    ]
    pd.DataFrame(rows).to_parquet(full_5min, index=False)

    (repo / "configs").mkdir(parents=True, exist_ok=True)
    (repo / "configs" / "replay_discovery.yaml").write_text(
        "artifact_index_path: data_refs/historical_market_data/artifact_index.yaml\n"
        f"replay_data_root: {artifact_root}\n"
        f"handoff_manifest_path: {artifact_root / 'strategy_lab_handoff.yaml'}\n"
        "symbols:\n"
        "  - TEST\n"
        "lookback_bars: [12]\n"
        "min_calendar_days_between_cases: 30\n"
        "max_cases_per_symbol_per_month: 1\n"
        "max_cases_per_symbol_total: 3\n"
        "avoid_existing_replay_windows: true\n"
        "preferred_sides:\n"
        "  - bullish\n"
        "  - bearish\n"
        "required_timeframes:\n"
        "  - 1Day\n"
        "  - 5Min\n"
        "deprecated_sample_sources:\n"
        "  - data_refs/google_drive\n"
    )
    (artifact_root / "strategy_lab_handoff.yaml").write_text(
        "artifact_version: v1.0\n"
        "artifact_root: artifacts/published/monster_historical_data_smoke_v1.0\n"
        "allowed_for_replay:\n"
        "  - 1Day\n"
        "  - 5Min\n"
        "blocked_for_replay:\n"
        "  - 1Min\n"
        "symbols:\n"
        "  - TEST\n"
        "full_data_paths:\n"
        "  TEST:\n"
        "    1Day:\n"
        f"      - {full_1day}\n"
        "    5Min:\n"
        f"      - {full_5min}\n"
        "sample_data_paths:\n"
        "  - data_refs/google_drive/TEST_1Day_sample.csv\n"
        "  - data_refs/google_drive/TEST_5Min_sample.csv\n"
    )
    md_path, csv_path, _ = write_date_diversified_candidates(repo)
    assert md_path.exists()
    assert csv_path.exists()
    assert "symbol diversity warning: all selected cases are TEST" in md_path.read_text()


def test_triage_summary_includes_hr_010_through_hr_015():
    path = write_replay_triage_summary(
        REPO_ROOT,
        [REPO_ROOT / "replay/cases" / f"HR-{idx:03d}.md" for idx in range(10, 16)],
    )
    text = path.read_text()
    for idx in range(10, 16):
        assert f"HR-{idx:03d}" in text


def test_mixed_batch_uses_multiple_symbols_when_candidates_exist():
    config = load_replay_discovery_config(REPO_ROOT)
    selected = select_date_diversified_candidates(
        [
            DiversifiedReplayCandidate("", "SPY", "bullish", "2023-08-09T16:30:00+00:00", "close_above_resistance", 446.37, 0.19, 12),
            DiversifiedReplayCandidate("", "META", "bearish", "2023-09-19T13:30:00+00:00", "close_below_support", 311.13, 0.12, 12),
            DiversifiedReplayCandidate("", "QQQ", "bullish", "2023-10-30T14:30:00+00:00", "close_above_resistance", 350.0, 0.8, 24),
            DiversifiedReplayCandidate("", "NVDA", "bearish", "2023-11-29T15:30:00+00:00", "close_below_support", 470.0, 1.0, 24),
        ],
        existing_case_dates=[],
        min_calendar_days_between_cases=30,
        max_cases_per_symbol_per_month=1,
        max_cases_per_symbol_total=2,
        avoid_existing_replay_windows=False,
    )
    assert len(selected) == 4
    assert len({candidate.symbol for candidate in selected}) >= 2
    assert {candidate.symbol for candidate in selected}.issubset(set(config.symbols))
    assert {candidate.side for candidate in selected} == {"bullish", "bearish"}
    assert all(candidate.replay_id == "" for candidate in selected)


def test_handoff_manifest_and_generated_cases_are_not_verified_and_block_broker_action():
    config = load_replay_discovery_config(REPO_ROOT)
    assert config.symbols == ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "AVGO", "IWM"]
    assert config.required_timeframes == ["1Day", "5Min"]

    bullish_case = load_replay_case(REPO_ROOT / "replay/cases/HR-010.md")
    bearish_case = load_replay_case(REPO_ROOT / "replay/cases/HR-013.md")
    for case in (bullish_case, bearish_case):
        assert case.replay_status == "NOT_VERIFIED"
        assert case.manual_review_status == "pending"
        assert case.broker_action_allowed is False
        assert case.evidence_type == "real_market_replay"
        assert case.real_market_evidence is True


def test_hr_020_through_hr_031_cases_reflect_promotion_where_applicable_and_keep_broker_action_false():
    promoted = {21, 22, 24}
    for idx in range(20, 32):
        case = load_replay_case(REPO_ROOT / "replay/cases" / f"HR-{idx:03d}.md")
        if idx in promoted:
            assert case.replay_status == "VERIFIED"
            assert case.manual_review_status == "completed"
            assert case.replay_outcome == "confirmed"
            assert case.classification == "confirmed_breakout"
        else:
            assert case.replay_status == "NOT_VERIFIED"
            assert case.manual_review_status == "pending"
        assert case.broker_action_allowed is False
        assert case.evidence_type == "real_market_replay"
        assert case.real_market_evidence is True


def test_new_batch_triage_summary_and_evidence_matrix_include_hr_020_through_hr_031():
    case_paths = [REPO_ROOT / "replay/cases" / f"HR-{idx:03d}.md" for idx in range(20, 32)]
    triage_path = write_replay_triage_summary(
        REPO_ROOT,
        case_paths,
        filename="HR-020_031_triage_summary.md",
        title="HR-020 through HR-031 Triage Summary",
    )
    triage_text = triage_path.read_text()
    for idx in range(20, 32):
        assert f"HR-{idx:03d}" in triage_text

    matrix_path = write_replay_evidence_matrix(REPO_ROOT)
    matrix_text = matrix_path.read_text()
    for idx in range(20, 32):
        assert f"HR-{idx:03d}" in matrix_text


def test_old_sample_files_are_not_used_when_full_handoff_index_is_present(tmp_path: Path):
    repo = tmp_path
    full_root = repo / "full"
    full_root.mkdir(parents=True)
    full_1day = full_root / "symbols" / "TEST" / "1Day" / "TEST_1Day_2024.parquet"
    full_5min = full_root / "symbols" / "TEST" / "5Min" / "TEST_5Min_2024.parquet"
    full_1day.parent.mkdir(parents=True, exist_ok=True)
    full_5min.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        [
            {"symbol": "TEST", "timeframe": "1Day", "timestamp": "2024-02-01T05:00:00+00:00", "open": 10, "high": 11, "low": 9, "close": 10.5, "volume": 1, "trade_count": 1, "vwap": 10.4, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
            {"symbol": "TEST", "timeframe": "1Day", "timestamp": "2024-02-02T05:00:00+00:00", "open": 10.5, "high": 11.5, "low": 10, "close": 11, "volume": 1, "trade_count": 1, "vwap": 10.8, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        ]
    ).to_parquet(full_1day, index=False)
    rows = []
    start = datetime(2024, 2, 1, 14, 30, tzinfo=timezone.utc)
    for idx in range(12):
        ts = start + timedelta(minutes=5 * idx)
        rows.append({"symbol": "TEST", "timeframe": "5Min", "timestamp": ts.isoformat(), "open": 10, "high": 10.5, "low": 9.8, "close": 10.2, "volume": 1, "trade_count": 1, "vwap": 10.2, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"})
    rows.append({"symbol": "TEST", "timeframe": "5Min", "timestamp": (start + timedelta(minutes=60)).isoformat(), "open": 10.2, "high": 12, "low": 10.1, "close": 11.9, "volume": 1, "trade_count": 1, "vwap": 11.5, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"})
    pd.DataFrame(rows).to_parquet(full_5min, index=False)

    sample_dir = repo / "data_refs" / "google_drive"
    sample_dir.mkdir(parents=True, exist_ok=True)
    (sample_dir / "TEST_1Day_sample.csv").write_text(
        "symbol,timeframe,timestamp,open,high,low,close,volume,trade_count,vwap,source,feed,adjustment,downloaded_at\n"
        "TEST,1Day,2023-05-15T04:00:00+00:00,10,11,9,10.5,1,1,10.4,alpaca,iex,raw,2026-05-19T00:00:00+00:00\n"
    )
    (sample_dir / "TEST_5Min_sample.csv").write_text(
        "symbol,timeframe,timestamp,open,high,low,close,volume,trade_count,vwap,source,feed,adjustment,downloaded_at\n"
        "TEST,5Min,2023-05-15T13:30:00+00:00,10,10.5,9.8,10.2,1,1,10.2,alpaca,iex,raw,2026-05-19T00:00:00+00:00\n"
        "TEST,5Min,2023-05-15T13:35:00+00:00,10.2,10.6,10.1,10.4,1,1,10.4,alpaca,iex,raw,2026-05-19T00:00:00+00:00\n"
    )

    artifact_index = {
        "schema": "historical_market_data_artifact_index_v1",
        "status": "active",
        "artifact_root": str(full_root),
        "symbols": ["TEST"],
        "timeframes": ["1Day", "5Min"],
        "allowed_for_replay": ["1Day", "5Min"],
        "blocked_for_replay": [],
        "items": [
            {"symbol": "TEST", "timeframe": "1Day", "path": str(full_1day), "file_type": "parquet", "artifact_kind": "full"},
            {"symbol": "TEST", "timeframe": "5Min", "path": str(full_5min), "file_type": "parquet", "artifact_kind": "full"},
        ],
    }
    index_path = repo / "data_refs" / "historical_market_data" / "artifact_index.yaml"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(yaml.safe_dump(artifact_index, sort_keys=False))

    events = discover_events_for_symbol(repo, "TEST", lookbacks=(12,))
    assert events
    assert events[0].timestamp.startswith("2024-02")
    assert all(not event.timestamp.startswith("2023-05") for event in events)


def test_handoff_manifest_is_respected_and_blocks_1min_and_sample_exports(tmp_path: Path):
    repo = tmp_path
    artifact_root = repo / "published" / "monster_historical_data_smoke_v1.0"
    full_1day = artifact_root / "symbols" / "TEST" / "1Day" / "TEST_1Day_2024.parquet"
    full_5min = artifact_root / "symbols" / "TEST" / "5Min" / "TEST_5Min_2024.parquet"
    blocked_1min = artifact_root / "symbols" / "TEST" / "1Min" / "TEST_1Min_2024.parquet"
    full_1day.parent.mkdir(parents=True, exist_ok=True)
    full_5min.parent.mkdir(parents=True, exist_ok=True)
    blocked_1min.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(
        [
            {"symbol": "TEST", "timeframe": "1Day", "timestamp": "2024-02-01T05:00:00+00:00", "open": 10, "high": 11, "low": 9, "close": 10.5, "volume": 1, "trade_count": 1, "vwap": 10.4, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
            {"symbol": "TEST", "timeframe": "1Day", "timestamp": "2024-02-02T05:00:00+00:00", "open": 10.5, "high": 11.5, "low": 10, "close": 11, "volume": 1, "trade_count": 1, "vwap": 10.8, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
            {"symbol": "TEST", "timeframe": "1Day", "timestamp": "2024-02-03T05:00:00+00:00", "open": 11, "high": 12, "low": 10.5, "close": 11.8, "volume": 1, "trade_count": 1, "vwap": 11.5, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        ]
    ).to_parquet(full_1day, index=False)

    rows = []
    start = datetime(2024, 2, 1, 14, 30, tzinfo=timezone.utc)
    for idx in range(7):
        ts = start + timedelta(minutes=5 * idx)
        rows.append({"symbol": "TEST", "timeframe": "5Min", "timestamp": ts.isoformat(), "open": 10, "high": 10.5 + idx * 0.1, "low": 9.8, "close": 10.2 + idx * 0.15, "volume": 1, "trade_count": 1, "vwap": 10.2, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"})
    rows.append({"symbol": "TEST", "timeframe": "5Min", "timestamp": (start + timedelta(minutes=35)).isoformat(), "open": 10.9, "high": 12.0, "low": 10.8, "close": 11.95, "volume": 1, "trade_count": 1, "vwap": 11.6, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"})
    pd.DataFrame(rows).to_parquet(full_5min, index=False)
    pd.DataFrame(
        [
            {"symbol": "TEST", "timeframe": "1Min", "timestamp": "2024-02-01T14:30:00+00:00", "open": 10, "high": 10.1, "low": 9.9, "close": 10.05, "volume": 1, "trade_count": 1, "vwap": 10.0, "source": "alpaca", "feed": "iex", "adjustment": "raw", "downloaded_at": "2026-05-19T00:00:00+00:00"},
        ]
    ).to_parquet(blocked_1min, index=False)

    (repo / "data_refs" / "google_drive").mkdir(parents=True, exist_ok=True)
    (repo / "data_refs" / "google_drive" / "TEST_1Day_sample.csv").write_text(
        "symbol,timeframe,timestamp,open,high,low,close,volume,trade_count,vwap,source,feed,adjustment,downloaded_at\n"
        "TEST,1Day,2023-05-15T04:00:00+00:00,10,11,9,10.5,1,1,10.4,alpaca,iex,raw,2026-05-19T00:00:00+00:00\n"
    )
    (repo / "data_refs" / "google_drive" / "TEST_5Min_sample.csv").write_text(
        "symbol,timeframe,timestamp,open,high,low,close,volume,trade_count,vwap,source,feed,adjustment,downloaded_at\n"
        "TEST,5Min,2023-05-15T13:30:00+00:00,10,10.5,9.8,10.2,1,1,10.2,alpaca,iex,raw,2026-05-19T00:00:00+00:00\n"
        "TEST,5Min,2023-05-15T13:35:00+00:00,10.2,10.6,10.1,10.4,1,1,10.4,alpaca,iex,raw,2026-05-19T00:00:00+00:00\n"
    )

    (repo / "configs").mkdir(parents=True, exist_ok=True)
    (repo / "configs" / "replay_discovery.yaml").write_text(
        "artifact_index_path: data_refs/historical_market_data/artifact_index.yaml\n"
        f"replay_data_root: {artifact_root}\n"
        f"handoff_manifest_path: {artifact_root / 'strategy_lab_handoff.yaml'}\n"
        "symbols:\n"
        "  - TEST\n"
        "lookback_bars: [6]\n"
        "min_calendar_days_between_cases: 30\n"
        "max_cases_per_symbol_per_month: 1\n"
        "avoid_existing_replay_windows: true\n"
        "preferred_sides:\n"
        "  - bullish\n"
        "  - bearish\n"
        "required_timeframes:\n"
        "  - 1Day\n"
        "  - 5Min\n"
        "deprecated_sample_sources:\n"
        "  - data_refs/google_drive\n"
    )
    (artifact_root / "strategy_lab_handoff.yaml").write_text(
        "artifact_version: v1.0\n"
        "artifact_root: artifacts/published/monster_historical_data_smoke_v1.0\n"
        "allowed_for_replay:\n"
        "  - 1Day\n"
        "  - 5Min\n"
        "blocked_for_replay:\n"
        "  - 1Min\n"
        "symbols:\n"
        "  - TEST\n"
        "full_data_paths:\n"
        "  TEST:\n"
        "    1Day:\n"
        f"      - {full_1day}\n"
        "    5Min:\n"
        f"      - {full_5min}\n"
        "    1Min:\n"
        f"      - {blocked_1min}\n"
        "sample_data_paths:\n"
        "  - data_refs/google_drive/TEST_1Day_sample.csv\n"
        "  - data_refs/google_drive/TEST_5Min_sample.csv\n"
    )

    paths = resolve_historical_market_data_paths(repo, "TEST")
    assert set(paths) == {"1Day", "5Min"}
    assert all("sample" not in str(path) for path in paths.values())

    events = discover_events_for_symbol(repo, "TEST", lookbacks=(6,))
    assert events
    assert events[0].timestamp.startswith("2024-02")

    config = load_replay_discovery_config(repo)
    md_path, csv_path, selected = write_date_diversified_candidates(repo, config)
    assert md_path.exists()
    assert csv_path.exists()
    assert selected
    assert all(candidate.symbol == "TEST" for candidate in selected)
    assert all(not candidate.timestamp.startswith("2023-05") for candidate in selected)


def test_discovery_constraint_audit_is_generated_and_reports_key_counts():
    md_path, csv_path = write_discovery_constraint_audit(REPO_ROOT)
    assert md_path.exists()
    assert csv_path.exists()

    text = md_path.read_text()
    assert "| raw candidates | 898 | 261 | 1159 |" in text
    assert "| final selected candidates | 6 | 6 | 12 |" in text
    assert "HR-020..HR-031" in text
    assert "avoid-existing-window" in text or "avoid_existing_replay_windows" in text

    csv_text = csv_path.read_text()
    assert "row_type,side,symbol,timestamp" in csv_text
    assert "near_miss" in csv_text


def test_discovery_constraint_audit_preserves_broker_action_false_in_existing_hr_cases():
    write_discovery_constraint_audit(REPO_ROOT)
    for idx in range(20, 32):
        case = load_replay_case(REPO_ROOT / "replay/cases" / f"HR-{idx:03d}.md")
        assert case.broker_action_allowed is False
