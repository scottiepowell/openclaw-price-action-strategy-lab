from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_source_manifests_and_example_cards_are_structured():
    manifests = {
        "transcript": REPO_ROOT / "evidence/source_manifests/transcript_manifest.yaml",
        "snapshot": REPO_ROOT / "evidence/source_manifests/snapshot_manifest.yaml",
        "historical": REPO_ROOT / "evidence/source_manifests/historical_data_manifest.yaml",
    }

    for path in manifests.values():
        data = yaml.safe_load(path.read_text())
        assert data["schema"].endswith("_v1")
        assert data["status"] == "placeholder"
        assert data["items"] == []
        assert data["notes"]

    ex_001 = yaml.safe_load((REPO_ROOT / "knowledge_base/examples/EX-001.yaml").read_text())
    ex_002 = yaml.safe_load((REPO_ROOT / "knowledge_base/examples/EX-002.yaml").read_text())

    assert ex_001["schema"] == "example_card_v1"
    assert ex_001["example_id"] == "EX-001"
    assert ex_001["candidate_family"] == [
        "current_range_identification",
        "current_range_context",
        "current_range_target_relationship",
        "current_range_invalidation",
    ]
    assert ex_001["source_refs"]["transcript"].endswith("WHAT ARE CURRENT RANGES LESSON [awsgn46dne].txt")
    assert ex_001["replay_refs"] == ["replay/cases/HR-001.md"]

    assert ex_002["schema"] == "example_card_v1"
    assert ex_002["example_id"] == "EX-002"
    assert "78_close_break_candidate" in ex_002["candidate_family"]
    assert len(ex_002["source_refs"]["snapshots"]) == 3
    assert ex_002["replay_refs"] == ["tests/fixtures/replay_cases/verified_sample.md"]


def test_candidate_registry_points_to_existing_families():
    registry = yaml.safe_load((REPO_ROOT / "knowledge_base/rule_candidates/candidate_index.yaml").read_text())
    families = {item["id"]: item["path"] for item in registry["families"]}

    assert set(families) == {
        "direction",
        "current_range",
        "support_resistance",
        "target_activation",
        "no_trade_filters",
        "paper_trade_readiness",
    }

    for path in families.values():
        assert (REPO_ROOT / path).exists()
