Files changed:
- runs/replay/HR-020_031_manual_review_decision_sheet.md
- runs/replay/HR-020_031_triage_summary.md
- .openclaw-mailbox/outbox/2026-05-22-005-prepare-hr020-031-manual-review-response.md

Decision sheet path:
- runs/replay/HR-020_031_manual_review_decision_sheet.md

Review priority order:
- Review first: HR-021, HR-022, HR-024
- Review second: HR-020, HR-023, HR-025, HR-027, HR-028, HR-029, HR-031
- Review later: HR-026, HR-030

Cases that look strongest:
- HR-021
- HR-022
- HR-024

Cases that look weakest:
- HR-026
- HR-030

Confirmation:
- HR-020 through HR-031 remain NOT_VERIFIED / pending / broker_action_allowed false.

Final test result:
- PYTHONPATH=src pytest -q → 88 passed
