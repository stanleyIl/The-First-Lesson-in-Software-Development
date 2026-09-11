"""新增功能（优先级/编辑/清空/统计）的单元测试。"""

from todo_cli.core import TodoList


def test_add_with_priority():
    todo = TodoList()
    task = todo.add("重要", priority="高")
    assert task.priority == "高"


def test_add_default_priority_is_medium():
    todo = TodoList()
    assert todo.add("默认").priority == "中"


def test_edit_changes_title():
    todo = TodoList()
    task = todo.add("旧标题")
    todo.edit(task.id, "新标题")
    assert todo.list()[0].title == "新标题"


def test_edit_missing_id_returns_none():
    assert TodoList().edit(99, "x") is None


def test_clear_done_removes_only_completed():
    todo = TodoList()
    a = todo.add("完成的")
    b = todo.add("待办的")
    todo.mark_done(a.id)
    removed = todo.clear_done()
    assert removed == 1
    assert [t.title for t in todo.list()] == ["待办的"]


def test_clear_done_noop_when_none():
    todo = TodoList()
    todo.add("待办")
    assert todo.clear_done() == 0


def test_stats_counts_total_and_done():
    todo = TodoList()
    a = todo.add("一")
    todo.add("二")
    todo.add("三")
    todo.mark_done(a.id)
    stats = todo.stats()
    assert stats.total == 3
    assert stats.done == 1
    assert stats.pending == 2