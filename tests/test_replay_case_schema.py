from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


REQUIRED_TEMPLATE_SECTIONS = [
    "## Replay ID",
    "## Linked Example ID",
    "## Symbol",
    "## Date window",
    "## Data files",
    "## Data quality status",
    "## Timeframes used",
    "## Concepts labeled",
    "## Phase 3.1 candidates tested",
    "## Replay labels",
    "## Replay outcome",
    "## Contradiction notes",
    "## Phase 6 impact",
    "## Boundary",
]


def _assert_contains_in_order(text: str, phrases: list[str]) -> None:
    pos = 0
    for phrase in phrases:
        next_pos = text.find(phrase, pos)
        assert next_pos != -1, phrase
        pos = next_pos + len(phrase)


def test_replay_case_template_and_case_stubs_have_required_sections():
    template = (REPO_ROOT / "replay/cases/OPEN-HR-template.md").read_text()
    _assert_contains_in_order(template, REQUIRED_TEMPLATE_SECTIONS)
    assert "No trade signal" in template
    assert "No profitability claim" in template
    assert "No execution readiness" in template

    hr_001 = (REPO_ROOT / "replay/cases/HR-001.md").read_text()
    assert hr_001.startswith("---")
    assert "evidence_type: real_market_replay" in hr_001
    assert "real_market_evidence: true" in hr_001
    assert "data_quality_status: PASSED" in hr_001
    assert "## Notes" in hr_001

    fixture = (REPO_ROOT / "tests/fixtures/replay_cases/verified_sample.md").read_text()
    assert fixture.startswith("---")
    assert "evidence_type: synthetic_fixture" in fixture
    assert "real_market_evidence: false" in fixture
    assert "## Notes" in fixture


def test_contradiction_template_stays_aligned_with_replay_boundary_language():
    template = (REPO_ROOT / "replay/contradiction_cases/HC-template.md").read_text()
    case = (REPO_ROOT / "replay/contradiction_cases/HC-001.md").read_text()

    assert "## Candidate being challenged" in template
    assert "## Decision impact" in template
    assert "## Boundary" in template
    assert case.startswith("# HC-001")
    assert "Placeholder contradiction case." in case
