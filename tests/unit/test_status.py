from pathlib import Path

from monster_strategy_lab.status import count_items, next_open_items, parse_todo, project_status


def test_parse_todo_items_and_next_actions():
    items = parse_todo("""
- [ ] first task
- [x] done task
- [ ] second task
- [ ] third task
- [ ] fourth task
""")

    assert count_items(items) == (4, 1)
    assert [item.text for item in next_open_items(items, 3)] == ["first task", "second task", "third task"]


def test_project_status_uses_todo_file(tmp_path: Path):
    (tmp_path / "TODO.md").write_text("""
- [ ] alpha
- [x] beta
- [ ] gamma
""")

    status = project_status(tmp_path)
    assert status["open_count"] == 2
    assert status["done_count"] == 1
    assert [item.text for item in status["next_items"]] == ["alpha", "gamma"]
