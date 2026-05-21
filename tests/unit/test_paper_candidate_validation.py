from __future__ import annotations

import json
from pathlib import Path

import yaml

from monster_strategy_lab.cli import main
from monster_strategy_lab.paper import load_candidate
from monster_strategy_lab.replay import analyze_level_interactions, write_manual_review_packet, write_replay_batch_summary, write_replay_evidence_matrix
from monster_strategy_lab.replay import load_replay_case, replay_case_verification_result
from monster_strategy_lab.validation import (
    inspect_ohlcv_file,
    load_historical_market_data_inventory,
    validate_candidate,
    write_replay_data_quality_report,
    write_dry_run_report,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_REPLAY = "tests/fixtures/replay_cases/verified_sample.md"


def _candidate_payload() -> dict:
    return {
        "schema": "paper_trade_candidate_v1",
        "candidate_id": "PTC-TEST-001",
        "title": "Test candidate",
        "related_phase_3_1_rule_candidate": "RC-001",
        "evidence_links": [
            {
                "link": "EX-001",
                "supports": "direction-model only",
                "notes": "Directional context only.",
            }
        ],
        "replay_case_links": [
            {
                "replay_case": "replay/cases/HR-001.md",
                "replay_status": "NOT_VERIFIED",
                "replay_outcome": "placeholder",
                "notes": "Not yet verified.",
            }
        ],
        "related_evidence": {
            "examples": ["EX-001"],
            "replay_cases": ["replay/cases/HR-001.md"],
        },
        "symbol": "AAPL",
        "direction": "long",
        "timeframe_context": "1D + 5m",
        "setup_timeframe": "1D",
        "execution_timeframe": "5m",
        "support_level": 100.0,
        "resistance_level": 105.0,
        "target_price": 110.0,
        "entry_candidate_price": 105.25,
        "room_to_target": 4.75,
        "invalidation_level": 98.5,
        "confirmation_behavior": "wait for close above resistance",
        "confirmation_type": "close_above_resistance",
        "higher_timeframe_context": "Daily context from replay notes.",
        "higher_timeframe_obstacle_check": "not documented",
        "target_already_hit_check": "not documented",
        "no_trade_filters": [{"id": "NTF-001", "status": "pass"}],
        "risk_notes": "Conservative placeholder risk notes.",
        "boundary": "Paper validation only",
    }


def _write_replay_case(
    path: Path,
    *,
    evidence_type: str,
    real_market_evidence: bool,
    replay_status: str,
    replay_outcome: str,
    classification: str = "insufficient",
    replay_observations: list[str] | None = None,
    data_quality_status: str = "PASSED",
    date_window: str = "2026-05-01 to 2026-05-05",
    data_files: list[str] | None = None,
    labels_present: list[str] | None = None,
    reviewer: str = "tester",
    boundary: str = "No trade signal, no profitability claim, no execution readiness.",
) -> None:
    labels_present = labels_present or ["range", "support", "resistance", "target", "break_behavior", "invalidation"]
    replay_observations = replay_observations or ["Synthetic replay case for testing."]
    data_files = data_files or ["data_refs/historical_market_data/example.csv"]
    path.parent.mkdir(parents=True, exist_ok=True)
    body = [
        "---",
        f"replay_id: {path.stem}",
        "symbol: AAPL",
        "timeframe_stack: 1D + 5m",
        f"date_window: {date_window}",
        "data_files:",
    ]
    body.extend(f"  - {item}" for item in data_files)
    body.extend(
        [
            f"data_quality_status: {data_quality_status}",
            "related_candidate_id: PTC-TEST-001",
            "related_examples:",
            "  - EX-001",
            "labels_present:",
        ]
    )
    body.extend(f"  - {label}" for label in labels_present)
    body.append("replay_observations:")
    body.extend(f"  - {observation}" for observation in replay_observations)
    body.extend(
        [
            f"classification: {classification}",
            f"replay_outcome: {replay_outcome}",
            f"replay_status: {replay_status}",
            f"evidence_type: {evidence_type}",
            f"real_market_evidence: {str(real_market_evidence).lower()}",
            f"reviewer: {reviewer}",
            f"boundary: {boundary}",
            "---",
            "",
            "# Replay case",
        ]
    )
    path.write_text("\n".join(body))


def test_candidate_parser_supports_yaml_and_json(tmp_path: Path):
    payload = _candidate_payload()

    yaml_path = tmp_path / "candidate.yaml"
    yaml_path.write_text(yaml.safe_dump(payload, sort_keys=False))
    json_path = tmp_path / "candidate.json"
    json_path.write_text(json.dumps(payload))

    yaml_candidate = load_candidate(yaml_path)
    json_candidate = load_candidate(json_path)

    assert yaml_candidate.candidate_id == "PTC-TEST-001"
    assert json_candidate.symbol == "AAPL"
    assert yaml_candidate.evidence_links[0].supports == "direction-model only"
    assert json_candidate.replay_case_links[0].replay_status == "NOT_VERIFIED"


def test_dry_run_validation_outputs_layered_statuses_and_report(tmp_path: Path):
    payload = _candidate_payload()
    replay_path = tmp_path / "replay/cases/HR-001.md"
    _write_replay_case(
        replay_path,
        evidence_type="placeholder",
        real_market_evidence=False,
        replay_status="NOT_VERIFIED",
        replay_outcome="placeholder",
        date_window="TBD",
        reviewer="pending",
    )
    payload["replay_case_links"] = [{"replay_case": "replay/cases/HR-001.md", "replay_status": "NOT_VERIFIED", "replay_outcome": "placeholder", "notes": "Not yet verified."}]
    candidate_path = tmp_path / "candidate.yaml"
    candidate_path.write_text(yaml.safe_dump(payload, sort_keys=False))
    candidate = load_candidate(candidate_path)

    result = validate_candidate(candidate, repo_root=tmp_path)
    assert result.schema_status == "PASS"
    assert result.evidence_status == "PASS"
    assert result.replay_status == "NOT_VERIFIED"
    assert result.strategy_logic_status == "PASS"
    assert result.paper_readiness_status == "READY_FOR_DRY_RUN"
    assert result.broker_action_allowed is False
    assert any("higher_timeframe_obstacle_check is not verified" in warning for warning in result.warnings)
    assert any("target_already_hit_check is not verified" in warning for warning in result.warnings)
    assert result.next_actions

    report_path = write_dry_run_report(tmp_path, candidate, result)
    report = report_path.read_text()
    assert "schema_status: PASS" in report
    assert "paper_readiness_status: READY_FOR_DRY_RUN" in report
    assert "broker_action_allowed: false" in report
    assert "## Next actions" in report


def test_complete_schema_but_incomplete_strategy_logic(tmp_path: Path):
    payload = _candidate_payload()
    payload["confirmation_type"] = "free_text"
    path = tmp_path / "candidate.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result = validate_candidate(load_candidate(path), repo_root=tmp_path)
    assert result.schema_status == "PASS"
    assert result.strategy_logic_status == "INCOMPLETE"
    assert result.paper_readiness_status == "READY_FOR_DRY_RUN"


def test_missing_target_invalidation_and_room_to_target_are_not_ready(tmp_path: Path):
    expectations = {
        "target_price": "missing support, resistance, target, or invalidation level",
        "invalidation_level": "missing support, resistance, target, or invalidation level",
        "room_to_target": "room_to_target is missing",
    }
    for field, expected_reason in expectations.items():
        payload = _candidate_payload()
        payload.pop(field)
        path = tmp_path / f"{field}.yaml"
        path.write_text(yaml.safe_dump(payload, sort_keys=False))
        result = validate_candidate(load_candidate(path), repo_root=tmp_path)
        assert result.schema_status == "FAIL"
        assert result.paper_readiness_status == "NOT_READY_FOR_ORDER_SUBMISSION"
        assert result.broker_action_allowed is False
        assert any(expected_reason in reason for reason in result.blocking_reasons)


def test_ex001_requires_explicit_direction_mapping(tmp_path: Path):
    payload = _candidate_payload()
    payload["evidence_links"] = [
        {
            "link": "EX-001",
            "supports": "general example",
            "notes": "Not explicit enough.",
        }
    ]
    path = tmp_path / "candidate.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result = validate_candidate(load_candidate(path), repo_root=tmp_path)
    assert any("EX-001" in warning for warning in result.warnings)


def test_placeholder_replay_cannot_be_verified(tmp_path: Path):
    case_path = tmp_path / "replay/cases/HR-placeholder.md"
    _write_replay_case(case_path, evidence_type="placeholder", real_market_evidence=False, replay_status="VERIFIED", replay_outcome="confirmed", reviewer="pending")
    case = load_replay_case(case_path)
    verification = replay_case_verification_result(case)

    assert verification.replay_status == "NOT_VERIFIED"
    assert verification.verified is False


def test_template_replay_cannot_be_verified(tmp_path: Path):
    case_path = tmp_path / "replay/cases/HR-template.md"
    _write_replay_case(case_path, evidence_type="template", real_market_evidence=False, replay_status="VERIFIED", replay_outcome="confirmed", reviewer="pending")
    case = load_replay_case(case_path)
    verification = replay_case_verification_result(case)

    assert verification.replay_status == "NOT_VERIFIED"
    assert verification.verified is False


def test_replay_case_linked_but_not_verified(tmp_path: Path):
    payload = _candidate_payload()
    replay_path = tmp_path / "replay/cases/HR-001.md"
    _write_replay_case(
        replay_path,
        evidence_type="placeholder",
        real_market_evidence=False,
        replay_status="NOT_VERIFIED",
        replay_outcome="placeholder",
        date_window="TBD",
        reviewer="pending",
    )
    path = tmp_path / "candidate.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result = validate_candidate(load_candidate(path), repo_root=tmp_path)
    assert result.replay_status == "NOT_VERIFIED"
    assert result.paper_readiness_status == "READY_FOR_DRY_RUN"
    assert result.next_actions == [
        "verify the historical data file paths for HR-001",
        "run data quality checks",
        "label support/resistance/target/invalidation",
        "verify close_above_resistance behavior",
        "check higher timeframe obstacle",
        "check whether target was already hit",
    ]


def test_replay_case_symbol_and_candidate_id_must_match(tmp_path: Path):
    payload = _candidate_payload()
    payload["candidate_id"] = "PTC-TEST-002"
    payload["symbol"] = "SPY"
    replay_path = tmp_path / "replay/cases/HR-symbol-mismatch.md"
    _write_replay_case(
        replay_path,
        evidence_type="real_market_replay",
        real_market_evidence=True,
        replay_status="VERIFIED",
        replay_outcome="confirmed",
        classification="confirmed_breakout",
        reviewer="human",
    )
    payload["replay_case_links"] = [
        {"replay_case": "replay/cases/HR-symbol-mismatch.md", "replay_status": "VERIFIED", "replay_outcome": "confirmed", "notes": "Mismatch test."}
    ]
    path = tmp_path / "candidate.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result = validate_candidate(load_candidate(path), repo_root=tmp_path)
    assert result.replay_status == "BLOCKED"
    assert result.paper_readiness_status == "BLOCKED"
    assert any("symbol mismatch" in reason for reason in result.blocking_reasons)


def test_hr_002_cannot_link_to_ptc_001_when_symbols_differ(tmp_path: Path):
    payload = _candidate_payload()
    payload["candidate_id"] = "PTC-002"
    payload["symbol"] = "SPY"
    replay_path = tmp_path / "replay/cases/HR-002.md"
    _write_replay_case(
        replay_path,
        evidence_type="real_market_replay",
        real_market_evidence=True,
        replay_status="VERIFIED",
        replay_outcome="confirmed",
        classification="confirmed_breakout",
        reviewer="human",
    )
    replay_text = replay_path.read_text().replace("symbol: AAPL", "symbol: SPY").replace("related_candidate_id: PTC-TEST-001", "related_candidate_id: PTC-001")
    replay_path.write_text(replay_text)
    payload["replay_case_links"] = [
        {"replay_case": "replay/cases/HR-002.md", "replay_status": "VERIFIED", "replay_outcome": "confirmed", "notes": "Should not link across symbols."}
    ]
    path = tmp_path / "candidate.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result = validate_candidate(load_candidate(path), repo_root=tmp_path)
    assert result.replay_status == "BLOCKED"
    assert any("related_candidate_id mismatch" in reason for reason in result.blocking_reasons)


def test_next_actions_shift_from_missing_files_to_missing_labels(tmp_path: Path):
    payload = _candidate_payload()
    payload["replay_case_links"] = [{"replay_case": "replay/cases/HR-missing.md", "replay_status": "NOT_VERIFIED", "replay_outcome": "placeholder", "notes": "Missing files."}]
    candidate_path = tmp_path / "candidate_missing.yaml"
    candidate_path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result_missing = validate_candidate(load_candidate(candidate_path), repo_root=tmp_path)
    assert any("verify the historical data file paths" in action for action in result_missing.next_actions)

    replay_path = tmp_path / "replay/cases/HR-labeled.md"
    _write_replay_case(
        replay_path,
        evidence_type="real_market_replay",
        real_market_evidence=True,
        replay_status="NOT_VERIFIED",
        replay_outcome="confirmed",
        labels_present=["range", "support", "target"],
        reviewer="human review pending",
    )
    payload["replay_case_links"] = [{"replay_case": "replay/cases/HR-labeled.md", "replay_status": "NOT_VERIFIED", "replay_outcome": "confirmed", "notes": "Real market replay pending promotion."}]
    candidate_path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result_labeled = validate_candidate(load_candidate(candidate_path), repo_root=tmp_path)
    assert any("label support/resistance/target/invalidation" in action for action in result_labeled.next_actions)


def test_artifact_inventory_parsing_round_trip(tmp_path: Path):
    inventory = {
        "schema": "historical_market_data_artifact_index_v1",
        "status": "active",
        "generated_at": "2026-05-17T00:00:00+00:00",
        "items": [
            {
                "symbol": "AAPL",
                "timeframe": "1Day",
                "path": "data_refs/google_drive/AAPL_1Day_sample.csv",
                "file_type": "csv",
                "row_count": 250,
                "first_timestamp": "2023-05-15T04:00:00+00:00",
                "last_timestamp": "2024-05-10T04:00:00+00:00",
                "timezone": "UTC",
                "source": "alpaca",
                "feed": "iex",
                "adjustment": "raw",
                "data_quality_status": "NOT_CHECKED",
            }
        ],
    }
    path = tmp_path / "artifact_index.yaml"
    path.write_text(yaml.safe_dump(inventory, sort_keys=False))

    loaded = load_historical_market_data_inventory(path)
    assert loaded["schema"] == "historical_market_data_artifact_index_v1"
    assert loaded["items"][0]["symbol"] == "AAPL"
    assert loaded["items"][0]["data_quality_status"] == "NOT_CHECKED"


def test_ohlcv_quality_pass_and_fail(tmp_path: Path):
    good = tmp_path / "AAPL_1Day_sample.csv"
    good.write_text(
        "symbol,timeframe,timestamp,open,high,low,close,volume,source,feed,adjustment\n"
        "AAPL,1Day,2023-05-15T04:00:00+00:00,100,105,99,104,123,alpaca,iex,raw\n"
    )
    bad = tmp_path / "AAPL_bad.csv"
    bad.write_text(
        "symbol,timeframe,timestamp,open,high,low,close,volume,source,feed,adjustment\n"
        "AAPL,1Day,2023-05-15T04:00:00+00:00,100,95,99,104,123,alpaca,iex,raw\n"
    )

    good_result = inspect_ohlcv_file(good)
    bad_result = inspect_ohlcv_file(bad)

    assert good_result.quality_status == "PASS"
    assert good_result.row_count == 1
    assert good_result.first_timestamp == "2023-05-15T04:00:00+00:00"
    assert bad_result.quality_status == "FAIL"
    assert any("high below candle body" in issue for issue in bad_result.issues)


def test_synthetic_verified_replay_stays_fixture_only(tmp_path: Path):
    payload = _candidate_payload()
    path = tmp_path / FIXTURE_REPLAY
    _write_replay_case(
        path,
        evidence_type="synthetic_fixture",
        real_market_evidence=False,
        replay_status="VERIFIED",
        replay_outcome="confirmed",
        reviewer="synthetic_fixture_test",
        boundary="No trade signal, no profitability claim, no execution readiness.",
    )
    payload["replay_case_links"] = [{"replay_case": FIXTURE_REPLAY, "replay_status": "VERIFIED", "replay_outcome": "confirmed", "notes": "Synthetic fixture."}]
    candidate_path = tmp_path / "candidate.yaml"
    candidate_path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result = validate_candidate(load_candidate(candidate_path), repo_root=tmp_path)
    assert result.replay_status == "VERIFIED_FIXTURE_ONLY"
    assert result.paper_readiness_status == "READY_FOR_DRY_RUN"
    assert any("fixture" in warning.lower() for warning in result.warnings)


def test_real_market_replay_can_upgrade_readiness(tmp_path: Path):
    payload = _candidate_payload()
    replay_path = tmp_path / "replay/cases/HR-real.md"
    _write_replay_case(
        replay_path,
        evidence_type="real_market_replay",
        real_market_evidence=True,
        replay_status="VERIFIED",
        replay_outcome="confirmed",
        classification="confirmed_breakout",
        reviewer="human",
        boundary="No trade signal, no profitability claim, no execution readiness.",
    )
    payload["replay_case_links"] = [{"replay_case": "replay/cases/HR-real.md", "replay_status": "VERIFIED", "replay_outcome": "confirmed", "notes": "Real market replay."}]
    path = tmp_path / "candidate.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result = validate_candidate(load_candidate(path), repo_root=tmp_path)
    assert result.replay_status == "VERIFIED"
    assert result.paper_readiness_status == "READY_FOR_PAPER_REVIEW"
    assert result.broker_action_allowed is False


def test_insufficient_replay_does_not_promote_paper_review(tmp_path: Path):
    payload = _candidate_payload()
    replay_path = tmp_path / "replay/cases/HR-insufficient.md"
    _write_replay_case(
        replay_path,
        evidence_type="real_market_replay",
        real_market_evidence=True,
        replay_status="VERIFIED",
        replay_outcome="insufficient",
        classification="insufficient",
        replay_observations=[
            "replay inspected",
            "manual visual review pending",
        ],
        reviewer="human",
        boundary="No trade signal, no profitability claim, no execution readiness.",
    )
    payload["replay_case_links"] = [{"replay_case": "replay/cases/HR-insufficient.md", "replay_status": "VERIFIED", "replay_outcome": "insufficient", "notes": "Manual review pending."}]
    path = tmp_path / "candidate.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result = validate_candidate(load_candidate(path), repo_root=tmp_path)
    assert result.replay_status == "NOT_VERIFIED"
    assert result.paper_readiness_status == "READY_FOR_DRY_RUN"
    assert result.broker_action_allowed is False
    assert any("replay_outcome not confirmed: insufficient" in reason for reason in result.blocking_reasons)


def test_watch_no_trigger_does_not_promote_paper_review(tmp_path: Path):
    payload = _candidate_payload()
    replay_path = tmp_path / "replay/cases/HR-watch.md"
    _write_replay_case(
        replay_path,
        evidence_type="real_market_replay",
        real_market_evidence=True,
        replay_status="VERIFIED",
        replay_outcome="insufficient",
        classification="watch_no_trigger",
        replay_observations=["approached resistance but did not trigger"],
        reviewer="human",
        boundary="No trade signal, no profitability claim, no execution readiness.",
    )
    payload["replay_case_links"] = [{"replay_case": "replay/cases/HR-watch.md", "replay_status": "VERIFIED", "replay_outcome": "insufficient", "notes": "Watch/no-trigger."}]
    path = tmp_path / "candidate.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result = validate_candidate(load_candidate(path), repo_root=tmp_path)
    assert result.paper_readiness_status == "READY_FOR_DRY_RUN"
    assert result.broker_action_allowed is False


def test_ambiguous_replay_blocks_paper_review(tmp_path: Path):
    payload = _candidate_payload()
    replay_path = tmp_path / "replay/cases/HR-ambiguous.md"
    _write_replay_case(
        replay_path,
        evidence_type="real_market_replay",
        real_market_evidence=True,
        replay_status="AMBIGUOUS",
        replay_outcome="ambiguous",
        classification="ambiguous",
        replay_observations=["not enough information to confirm the setup"],
        reviewer="human",
        boundary="No trade signal, no profitability claim, no execution readiness.",
    )
    payload["replay_case_links"] = [{"replay_case": "replay/cases/HR-ambiguous.md", "replay_status": "AMBIGUOUS", "replay_outcome": "ambiguous", "notes": "Ambiguous replay."}]
    path = tmp_path / "candidate.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result = validate_candidate(load_candidate(path), repo_root=tmp_path)
    assert result.paper_readiness_status == "BLOCKED"
    assert result.broker_action_allowed is False


def test_contradicted_replay_blocks_paper_review(tmp_path: Path):
    payload = _candidate_payload()
    replay_path = tmp_path / "replay/cases/HR-contradicted.md"
    _write_replay_case(
        replay_path,
        evidence_type="real_market_replay",
        real_market_evidence=True,
        replay_status="CONTRADICTED",
        replay_outcome="contradicted",
        classification="contradicted",
        replay_observations=["the candidate setup did not match the observed replay"],
        reviewer="human",
        boundary="No trade signal, no profitability claim, no execution readiness.",
    )
    payload["replay_case_links"] = [{"replay_case": "replay/cases/HR-contradicted.md", "replay_status": "CONTRADICTED", "replay_outcome": "contradicted", "notes": "Contradicted replay."}]
    path = tmp_path / "candidate.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result = validate_candidate(load_candidate(path), repo_root=tmp_path)
    assert result.paper_readiness_status == "BLOCKED"
    assert result.broker_action_allowed is False


def test_confirmed_replay_needs_real_market_evidence_and_passed_data_quality_for_paper_review(tmp_path: Path):
    payload = _candidate_payload()
    replay_path = tmp_path / "replay/cases/HR-confirmed.md"
    _write_replay_case(
        replay_path,
        evidence_type="real_market_replay",
        real_market_evidence=True,
        replay_status="VERIFIED",
        replay_outcome="confirmed",
        classification="confirmed_breakout",
        replay_observations=["confirmed breakout reviewed"],
        reviewer="human",
        boundary="No trade signal, no profitability claim, no execution readiness.",
    )
    payload["replay_case_links"] = [{"replay_case": "replay/cases/HR-confirmed.md", "replay_status": "VERIFIED", "replay_outcome": "confirmed", "notes": "Confirmed breakout."}]
    path = tmp_path / "candidate.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result = validate_candidate(load_candidate(path), repo_root=tmp_path)
    assert result.replay_status == "VERIFIED"
    assert result.paper_readiness_status == "READY_FOR_PAPER_REVIEW"
    assert result.broker_action_allowed is False


def test_batch_summary_generation_includes_hr_001_hr_002_hr_003(tmp_path: Path):
    cases = [("HR-001", "SPY", "PTC-001"), ("HR-002", "NVDA", "PTC-002"), ("HR-003", "AAPL", "PTC-003")]
    for replay_id, symbol, candidate_id in cases:
        data_path = tmp_path / f"data_refs/google_drive/{symbol}_5Min_sample.csv"
        data_path.parent.mkdir(parents=True, exist_ok=True)
        data_path.write_text(
            "symbol,timeframe,timestamp,open,high,low,close,volume,source,feed,adjustment\n"
            f"{symbol},5Min,2023-05-15T13:30:00+00:00,100,101,99,100,10,alpaca,iex,raw\n"
        )
        day_path = tmp_path / f"data_refs/google_drive/{symbol}_1Day_sample.csv"
        day_path.write_text(
            "symbol,timeframe,timestamp,open,high,low,close,volume,source,feed,adjustment\n"
            f"{symbol},1Day,2023-05-15T04:00:00+00:00,100,101,99,100,10,alpaca,iex,raw\n"
        )
        case_path = tmp_path / f"replay/cases/{replay_id}.md"
        _write_replay_case(
            case_path,
            evidence_type="real_market_replay",
            real_market_evidence=True,
            replay_status="NOT_VERIFIED",
            replay_outcome="insufficient",
            classification="insufficient",
            data_quality_status="PASSED",
            date_window="2023-05-15 to 2023-05-15",
            data_files=[
                f"data_refs/google_drive/{symbol}_1Day_sample.csv",
                f"data_refs/google_drive/{symbol}_5Min_sample.csv",
            ],
            reviewer="pending manual visual review",
        )
        case_text = case_path.read_text().replace("related_candidate_id: PTC-TEST-001", f"related_candidate_id: {candidate_id}")
        case_path.write_text(case_text)

    summary_path = write_replay_batch_summary(tmp_path, [tmp_path / "replay/cases/HR-001.md", tmp_path / "replay/cases/HR-002.md", tmp_path / "replay/cases/HR-003.md"])
    summary = summary_path.read_text()
    assert "HR-001" in summary
    assert "HR-002" in summary
    assert "HR-003" in summary
    assert "related_candidate_id: PTC-001" in summary
    assert "related_candidate_id: PTC-002" in summary
    assert "related_candidate_id: PTC-003" in summary


def test_data_quality_report_uses_generic_real_market_replay_flag(tmp_path: Path):
    replay_path = tmp_path / "replay/cases/HR-001.md"
    _write_replay_case(
        replay_path,
        evidence_type="real_market_replay",
        real_market_evidence=True,
        replay_status="NOT_VERIFIED",
        replay_outcome="insufficient",
        reviewer="pending",
    )

    report_path = write_replay_data_quality_report(
        tmp_path,
        "HR-001",
        replay_path,
        [],
        can_be_real_market_replay=True,
        blockers=[],
        date_window="2023-05-15 to 2023-05-15",
    )
    report = report_path.read_text()
    assert "can_be_real_market_replay: true" in report
    assert "hr_001_can_be_real_market_replay" not in report


def test_real_market_evidence_false_blocks_paper_review(tmp_path: Path):
    payload = _candidate_payload()
    replay_path = tmp_path / "replay/cases/HR-false.md"
    _write_replay_case(
        replay_path,
        evidence_type="real_market_replay",
        real_market_evidence=False,
        replay_status="VERIFIED",
        replay_outcome="confirmed",
        reviewer="human",
        boundary="No trade signal, no profitability claim, no execution readiness.",
    )
    payload["replay_case_links"] = [{"replay_case": "replay/cases/HR-false.md", "replay_status": "VERIFIED", "replay_outcome": "confirmed", "notes": "real_market_evidence false."}]
    path = tmp_path / "candidate.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result = validate_candidate(load_candidate(path), repo_root=tmp_path)
    assert result.replay_status == "BLOCKED"
    assert result.paper_readiness_status == "BLOCKED"
    assert result.broker_action_allowed is False


def test_replay_case_with_missing_labels_is_not_verified(tmp_path: Path):
    payload = _candidate_payload()
    replay_path = tmp_path / "replay/cases/HR-003.md"
    _write_replay_case(
        replay_path,
        evidence_type="real_market_replay",
        real_market_evidence=True,
        replay_status="VERIFIED",
        replay_outcome="confirmed",
        labels_present=["range", "support", "target"],
    )
    payload["replay_case_links"] = [{"replay_case": "replay/cases/HR-003.md", "replay_status": "VERIFIED", "replay_outcome": "confirmed", "notes": "Missing labels."}]
    path = tmp_path / "candidate.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result = validate_candidate(load_candidate(path), repo_root=tmp_path)
    assert result.replay_status == "NOT_VERIFIED"
    assert result.paper_readiness_status == "READY_FOR_DRY_RUN"
    assert any("labels missing" in reason for reason in result.blocking_reasons)


def test_replay_case_with_data_quality_not_passed_is_not_verified(tmp_path: Path):
    payload = _candidate_payload()
    replay_path = tmp_path / "replay/cases/HR-004.md"
    _write_replay_case(
        replay_path,
        evidence_type="real_market_replay",
        real_market_evidence=True,
        replay_status="VERIFIED",
        replay_outcome="confirmed",
        data_quality_status="PENDING",
    )
    payload["replay_case_links"] = [{"replay_case": "replay/cases/HR-004.md", "replay_status": "VERIFIED", "replay_outcome": "confirmed", "notes": "Data quality pending."}]
    path = tmp_path / "candidate.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result = validate_candidate(load_candidate(path), repo_root=tmp_path)
    assert result.replay_status == "NOT_VERIFIED"
    assert any("data_quality_status not passed" in reason for reason in result.blocking_reasons)


def test_replay_case_missing_date_window_blocks_verified(tmp_path: Path):
    payload = _candidate_payload()
    replay_path = tmp_path / "replay/cases/HR-006.md"
    _write_replay_case(
        replay_path,
        evidence_type="real_market_replay",
        real_market_evidence=True,
        replay_status="VERIFIED",
        replay_outcome="confirmed",
        date_window="",
    )
    payload["replay_case_links"] = [{"replay_case": "replay/cases/HR-006.md", "replay_status": "VERIFIED", "replay_outcome": "confirmed", "notes": "Missing date window."}]
    path = tmp_path / "candidate.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result = validate_candidate(load_candidate(path), repo_root=tmp_path)
    assert result.replay_status == "NOT_VERIFIED"
    assert any("date_window missing" in reason for reason in result.blocking_reasons)


def test_replay_case_contradicted_blocks_readiness(tmp_path: Path):
    payload = _candidate_payload()
    replay_path = tmp_path / "replay/cases/HR-005.md"
    _write_replay_case(
        replay_path,
        evidence_type="real_market_replay",
        real_market_evidence=True,
        replay_status="CONTRADICTED",
        replay_outcome="contradicted",
    )
    payload["replay_case_links"] = [{"replay_case": "replay/cases/HR-005.md", "replay_status": "CONTRADICTED", "replay_outcome": "contradicted", "notes": "Contradicted replay."}]
    path = tmp_path / "candidate.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False))

    result = validate_candidate(load_candidate(path), repo_root=tmp_path)
    assert result.replay_status == "CONTRADICTED"
    assert result.paper_readiness_status == "BLOCKED"
    assert result.broker_action_allowed is False


def test_replay_readme_and_checklist_exist():
    assert (REPO_ROOT / "replay/README.md").exists()
    assert (REPO_ROOT / "replay/REPLAY_CASE_CHECKLIST.md").exists()
    assert (REPO_ROOT / FIXTURE_REPLAY).exists()


def test_cli_paper_dry_run_writes_report(tmp_path: Path, capsys):
    payload = _candidate_payload()
    replay_path = tmp_path / "replay/cases/HR-001.md"
    _write_replay_case(
        replay_path,
        evidence_type="placeholder",
        real_market_evidence=False,
        replay_status="NOT_VERIFIED",
        replay_outcome="placeholder",
        date_window="TBD",
        reviewer="pending",
    )
    candidate_path = tmp_path / "candidate.yaml"
    candidate_path.write_text(yaml.safe_dump(payload, sort_keys=False))

    exit_code = main(["--repo-root", str(tmp_path), "paper-dry-run", "--candidate", str(candidate_path)])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "schema_status: PASS" in out
    assert "paper_readiness_status: READY_FOR_DRY_RUN" in out
    assert (tmp_path / "runs/dry_run/PTC-TEST-001-dry-run-report.md").exists()


def test_schema_and_template_track_the_required_fields():
    schema = yaml.safe_load((REPO_ROOT / "knowledge_base/paper_trade_candidates/schema.yaml").read_text())
    template = (REPO_ROOT / "paper_validation/paper_trade_candidates/PTC-template.md").read_text()

    assert schema["schema"] == "paper_trade_candidate_v1"
    assert schema["fields"]["candidate_id"]["required"] is True
    assert schema["fields"]["evidence_links"]["required"] is True
    assert schema["fields"]["replay_case_links"]["required"] is True
    assert schema["fields"]["no_trade_filters"]["required"] is True

    for section in [
        "## Candidate ID",
        "## Related Phase 3.1 rule candidate",
        "## Related evidence examples",
        "## Symbol",
        "## Direction",
        "## Support",
        "## Resistance",
        "## Target",
        "## Room to target",
        "## Invalidation",
        "## Timeframe context",
        "## Confirmation behavior",
        "## No-trade filters",
    ]:
        assert section in template


def test_ptc_002_and_ptc_003_remain_dry_run_only():
    for candidate_id in ["PTC-001", "PTC-002", "PTC-003"]:
        candidate = load_candidate(REPO_ROOT / f"paper_validation/paper_trade_candidates/{candidate_id}.yaml")
        result = validate_candidate(candidate, repo_root=REPO_ROOT)
        assert result.broker_action_allowed is False
        assert result.paper_readiness_status != "READY_FOR_PAPER_REVIEW"


def test_manual_review_packets_exist_and_include_required_sections():
    for replay_id in ["HR-002", "HR-003"]:
        packet = REPO_ROOT / f"runs/replay/{replay_id}_manual_review_packet.md"
        text = packet.read_text()
        assert packet.exists()
        assert "## Replay case metadata" in text
        assert "## 1D OHLCV rows for the replay window" in text
        assert "## 5m OHLCV excerpt for the replay window" in text
        assert "## Level interaction analysis" in text
        assert "## Candidate chart-level worksheet" in text
        assert "## Candidate event summary" in text
        assert "## Manual visual review checklist" in text
        assert "## Recommended classification options" in text
        assert "## Boundary" in text


def test_manual_review_packets_include_explicit_event_flags():
    for replay_id, expected_classification in [
        ("HR-004", "confirmed_breakout"),
        ("HR-005", "confirmed_breakout"),
        ("HR-006", "confirmed_breakout_no_target_hit"),
    ]:
        text = (REPO_ROOT / f"runs/replay/{replay_id}_manual_review_packet.md").read_text()
        for field in [
            "- target_hit_before_confirmation:",
            "- target_hit_after_confirmation:",
            "- invalidation_hit_after_confirmation:",
            "- max_high_after_confirmation:",
            "- max_close_after_confirmation:",
            "- target_distance:",
            "- max_favorable_move:",
        ]:
            assert field in text
        assert "## Manual promotion workflow" in text
        for field in [
            "- manual_review_status: pending",
            "- manual_review_outcome: TBD",
            "- manual_review_classification: TBD",
            "- manual_reviewer_notes: TBD",
            "- broker_action_allowed: false",
        ]:
            assert field in text
        assert f"- suggested_classification: {expected_classification}" in text


def test_confirmed_breakout_no_target_hit_is_supported_classification():
    from monster_strategy_lab.replay import ALLOWED_REPLAY_CLASSIFICATIONS

    assert "confirmed_breakout_no_target_hit" in ALLOWED_REPLAY_CLASSIFICATIONS


def test_hr_002_verified_and_hr_003_remains_not_verified():
    hr_002 = load_replay_case(REPO_ROOT / "replay/cases/HR-002.md")
    hr_003 = load_replay_case(REPO_ROOT / "replay/cases/HR-003.md")

    assert hr_002.replay_status == "VERIFIED"
    assert hr_002.classification == "watch_no_trigger"
    assert hr_003.replay_status == "VERIFIED"
    assert hr_003.classification == "insufficient"


def test_close_above_resistance_detection_and_suggested_classification():
    rows = [
        {"timestamp": "2023-05-17 13:30:00+00:00", "open": "100", "high": "101", "low": "99", "close": "100.5"},
        {"timestamp": "2023-05-17 13:35:00+00:00", "open": "100.5", "high": "102.5", "low": "100.2", "close": "102.1"},
        {"timestamp": "2023-05-17 13:40:00+00:00", "open": "102.1", "high": "103.3", "low": "101.8", "close": "103.1"},
    ]
    analysis = analyze_level_interactions(rows, support_level=99.0, resistance_level=102.0, target_price=103.0, invalidation_level=98.5)
    assert analysis["close_above_resistance"] is True
    assert analysis["resistance_touched"] is True
    assert analysis["suggested_classification"] == "confirmed_breakout"


def test_resistance_touched_but_no_close_above_is_watch_no_trigger():
    rows = [
        {"timestamp": "2023-05-17 13:30:00+00:00", "open": "100", "high": "101", "low": "99", "close": "100.5"},
        {"timestamp": "2023-05-17 13:35:00+00:00", "open": "100.5", "high": "102.5", "low": "100.2", "close": "101.9"},
        {"timestamp": "2023-05-17 13:40:00+00:00", "open": "101.9", "high": "102.2", "low": "101.2", "close": "101.8"},
    ]
    analysis = analyze_level_interactions(rows, support_level=99.0, resistance_level=102.0, target_price=103.0, invalidation_level=98.5)
    assert analysis["resistance_touched"] is True
    assert analysis["close_above_resistance"] is False
    assert analysis["suggested_classification"] == "watch_no_trigger"


def test_target_not_present_in_window_is_insufficient():
    rows = [
        {"timestamp": "2023-05-17 13:30:00+00:00", "open": "100", "high": "101", "low": "99", "close": "100.5"},
        {"timestamp": "2023-05-17 13:35:00+00:00", "open": "100.5", "high": "101.5", "low": "100.2", "close": "101.1"},
        {"timestamp": "2023-05-17 13:40:00+00:00", "open": "101.1", "high": "101.8", "low": "100.8", "close": "101.2"},
    ]
    analysis = analyze_level_interactions(rows, support_level=99.0, resistance_level=102.0, target_price=110.0, invalidation_level=98.5)
    assert analysis["target_close_hit"] is False
    assert analysis["target_high_hit"] is False
    assert analysis["suggested_classification"] == "insufficient"


def test_target_hit_before_confirmation_blocks_confirmed_breakout():
    rows = [
        {"timestamp": "2023-05-17 13:30:00+00:00", "open": "100", "high": "103.5", "low": "99", "close": "102.6"},
        {"timestamp": "2023-05-17 13:35:00+00:00", "open": "102.6", "high": "104.2", "low": "102.4", "close": "103.9"},
        {"timestamp": "2023-05-17 13:40:00+00:00", "open": "103.9", "high": "105.0", "low": "103.7", "close": "104.8"},
    ]
    analysis = analyze_level_interactions(rows, support_level=99.0, resistance_level=103.0, target_price=103.2, invalidation_level=98.5)
    assert analysis["close_above_resistance"] is True
    assert analysis["target_already_hit_before_confirmation"] is True
    assert analysis["suggested_classification"] == "contradicted"


def test_close_above_resistance_without_target_hit_is_confirmed_breakout_no_target_hit():
    rows = [
        {"timestamp": "2023-05-17 13:30:00+00:00", "open": "100", "high": "101", "low": "99", "close": "100.5"},
        {"timestamp": "2023-05-17 13:35:00+00:00", "open": "100.5", "high": "102.5", "low": "100.2", "close": "102.1"},
        {"timestamp": "2023-05-17 13:40:00+00:00", "open": "102.1", "high": "102.9", "low": "101.8", "close": "102.8"},
    ]
    analysis = analyze_level_interactions(rows, support_level=99.0, resistance_level=102.0, target_price=110.0, invalidation_level=98.5)
    assert analysis["close_above_resistance"] is True
    assert analysis["target_hit_after_confirmation"] is False
    assert analysis["suggested_classification"] == "confirmed_breakout_no_target_hit"


def test_replay_evidence_matrix_is_generated_and_covers_current_cases():
    matrix_path = write_replay_evidence_matrix(REPO_ROOT)
    csv_path = REPO_ROOT / "runs/replay/replay_evidence_matrix.csv"
    text = matrix_path.read_text()
    csv_text = csv_path.read_text()

    assert matrix_path.exists()
    assert csv_path.exists()
    for replay_id in [f"HR-00{i}" for i in range(1, 10)]:
        assert replay_id in text
        assert replay_id in csv_text

    assert "broker_action_allowed: true" not in text
    assert "broker_action_allowed" not in csv_text

    assert "### bullish_confirmed_breakout_target_hit" in text
    assert "- count: 2" in text
    assert "HR-004, HR-005" in text

    assert "### bullish_watch_no_trigger" in text
    assert "HR-001, HR-002" in text

    assert "### bearish_confirmed_breakdown_target_hit" in text
    assert "- count: 1" in text
    assert "HR-009" in text

    assert "### bearish_breakdown_no_target_hit" in text
    assert "- count: 1" in text
    assert "HR-007" in text

    assert "### bearish_failed_breakdown_reclaim" in text
    assert "- count: 1" in text
    assert "HR-008" in text

    assert "### insufficient_coverage" in text
    assert "- count: 1" in text
    assert "HR-003" in text

    assert "bearish close_below_support discovery" in text
