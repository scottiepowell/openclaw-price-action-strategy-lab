from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

from .status import format_status_report, project_status
from .paper.candidate import load_candidate
from .validation.dry_run import validate_candidate, write_dry_run_report


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="monster_strategy_lab")
    parser.add_argument("--repo-root", default=Path.cwd(), type=Path)
    subparsers = parser.add_subparsers(dest="command")

    paper_dry_run = subparsers.add_parser("paper-dry-run", help="Validate a paper-trade candidate without submitting orders")
    paper_dry_run.add_argument("--candidate", required=True, type=Path)
    paper_dry_run.set_defaults(command_handler=_handle_paper_dry_run)
    return parser


def _handle_paper_dry_run(args) -> int:
    repo_root = args.repo_root
    candidate_path = args.candidate if args.candidate.is_absolute() else repo_root / args.candidate
    candidate = load_candidate(candidate_path)
    result = validate_candidate(candidate, repo_root=repo_root)
    report_path = write_dry_run_report(repo_root, candidate, result)

    print(f"schema_status: {result.schema_status}")
    print(f"evidence_status: {result.evidence_status}")
    print(f"replay_status: {result.replay_status}")
    print(f"strategy_logic_status: {result.strategy_logic_status}")
    print(f"paper_readiness_status: {result.paper_readiness_status}")
    print(f"broker_action_allowed: {str(result.broker_action_allowed).lower()}")
    print(f"Report: {report_path}")
    print("Blocking reasons:")
    if result.blocking_reasons:
        for reason in result.blocking_reasons:
            print(f"- {reason}")
    else:
        print("- none")
    print("Warnings:")
    if result.warnings:
        for warning in result.warnings:
            print(f"- {warning}")
    else:
        print("- none")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if hasattr(args, "command_handler"):
        return args.command_handler(args)
    status = project_status(args.repo_root)
    print(format_status_report(status))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
