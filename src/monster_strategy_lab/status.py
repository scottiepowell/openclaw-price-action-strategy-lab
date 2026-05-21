from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class TodoItem:
    text: str
    checked: bool


CHECKBOX_RE = re.compile(r"^\s*- \[( |x|X)\]\s+(.*\S)\s*$")


def parse_todo(text: str) -> list[TodoItem]:
    items: list[TodoItem] = []
    for line in text.splitlines():
        match = CHECKBOX_RE.match(line)
        if match:
            items.append(TodoItem(text=match.group(2), checked=match.group(1).lower() == "x"))
    return items


def load_todo_items(path: Path) -> list[TodoItem]:
    return parse_todo(path.read_text())


def next_open_items(items: list[TodoItem], limit: int = 3) -> list[TodoItem]:
    return [item for item in items if not item.checked][:limit]


def count_items(items: list[TodoItem]) -> tuple[int, int]:
    open_count = sum(1 for item in items if not item.checked)
    done_count = sum(1 for item in items if item.checked)
    return open_count, done_count


def project_status(repo_root: Path) -> dict[str, object]:
    todo_path = repo_root / "TODO.md"
    items = load_todo_items(todo_path)
    open_count, done_count = count_items(items)
    return {
        "repo_root": repo_root,
        "todo_path": todo_path,
        "items": items,
        "open_count": open_count,
        "done_count": done_count,
        "next_items": next_open_items(items, 3),
    }


def format_status_report(status: dict[str, object]) -> str:
    open_count = status["open_count"]
    done_count = status["done_count"]
    next_items = status["next_items"]

    lines = [
        f"Project status for {status['repo_root']}",
        f"Open TODOs: {open_count}; done: {done_count}",
        "Next up:",
    ]

    if next_items:
        for idx, item in enumerate(next_items, 1):
            lines.append(f"{idx}. {item.text}")
    else:
        lines.append("- no open TODO items found")

    return "\n".join(lines)
