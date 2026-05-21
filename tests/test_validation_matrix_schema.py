from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_phase_five_validation_matrix_documents_have_the_expected_gates():
    phase_5 = (REPO_ROOT / "docs/phases/phase-05-validation/PHASE_5_VALIDATION_MATRIX.md").read_text()
    phase_5_1 = (REPO_ROOT / "docs/phases/phase-05-validation/PHASE_5_1_VALIDATION_MATRIX_HISTORICAL_REPLAY_UPDATE.md").read_text()
    phase_6 = (REPO_ROOT / "docs/phases/phase-06-rule-refinement/PHASE_6_PAPER_TRADE_READINESS_GATES.md").read_text()
    checklist = (REPO_ROOT / "paper_validation/readiness_gates/promotion_checklist.md").read_text()

    assert "Starter matrix" in phase_5
    assert "Candidate family | Expected focus | Validation output" in phase_5
    assert "Boundary" in phase_5
    assert "not a backtest" in phase_5.lower()
    assert "paper-trade approval" in phase_5.lower()

    assert "Replay requirements" in phase_5_1
    for phrase in [
        "parseable timestamps",
        "known timezone",
        "known symbol",
        "known timeframe",
        "missing bars checked",
        "OHLC sanity checked",
        "market-hours scope known",
    ]:
        assert phrase in phase_5_1

    assert "Minimum gate set" in phase_6
    assert "Promotion rule" in phase_6
    assert "Fail fast conditions" in phase_6
    assert "live-order wording" in phase_6

    assert "candidate definition is explicit" in checklist
    assert "candidate promotion criteria are satisfied" in checklist
    assert "If any box cannot be checked confidently, stop and gather more evidence." in checklist
