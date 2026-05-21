from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[1]


def _todo_items(text: str) -> list[tuple[str, bool]]:
    items: list[tuple[str, bool]] = []
    for line in text.splitlines():
        match = re.match(r"^\s*- \[( |x|X)\]\s+(.*\S)\s*$", line)
        if match:
            items.append((match.group(2), match.group(1).lower() == "x"))
    return items


def test_repo_scope_and_remaining_blockers_are_explicit():
    readme = (REPO_ROOT / "README.md").read_text()
    brief = (REPO_ROOT / "PROJECT_BRIEF.md").read_text()
    todo = _todo_items((REPO_ROOT / "TODO.md").read_text())

    assert "not a live trading bot" in readme
    assert "not a live trading bot" in brief

    open_items = [text for text, checked in todo if not checked]
    assert open_items == [
        "Do not copy large OHLCV files into this repo unless explicitly required.",
        "Do not commit real API keys.",
        "Do not use live account keys.",
        "Do not implement real order submission until explicitly approved.",
    ]

    assert sum(1 for _, checked in todo if checked) > 0
