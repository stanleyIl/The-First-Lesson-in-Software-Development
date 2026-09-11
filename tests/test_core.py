"""core.TodoList 的单元测试。"""

from todo_cli.core import Task, TodoList


def test_add_assigns_incrementing_id():
    todo = TodoList()
    a = todo.add("买菜")
    b = todo.add("写报告")
    assert a.id == 1
    assert b.id == 2


def test_list_returns_insertion_order():
    todo = TodoList()
    todo.add("第一")
    todo.add("第二")
    assert [t.title for t in todo.list()] == ["第一", "第二"]


def test_new_task_is_not_done():
    todo = TodoList()
    task = todo.add("学习")
    assert task.done is False


def test_mark_done_flips_status():
    todo = TodoList()
    task = todo.add("锻炼")
    assert todo.mark_done(task.id).done is True


def test_mark_done_missing_id_returns_none():
    assert TodoList().mark_done(99) is None


def test_remove_deletes_task():
    todo = TodoList()
    a = todo.add("临时任务")
    todo.add("保留任务")
    assert todo.remove(a.id) is True
    assert [t.title for t in todo.list()] == ["保留任务"]


def test_id_stays_stable_after_removal():
    # 删除后 id 不回退：新增自增 id 应跳过已删除的编号
    todo = TodoList()
    a = todo.add("first")
    todo.remove(a.id)
    new = todo.add("second")
    assert new.id == 2


def test_init_from_existing_tasks_resumes_next_id():
    existing = [Task(id=1, title="旧任务", done=True)]
    todo = TodoList(existing)
    new = todo.add("新任务")
    assert new.id == 2