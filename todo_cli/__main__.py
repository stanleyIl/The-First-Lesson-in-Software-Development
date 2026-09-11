"""交互式命令行菜单入口：`python -m todo_cli`（或安装后执行 `todo`）。

用户通过输入数字选择操作：添加、查看、标记完成、删除、编辑、清空、统计、退出。
"""

from __future__ import annotations

import sys
from pathlib import Path

from .core import PRIORITIES, Task, TodoList
from .storage import load, save

# 数据文件默认存放在项目根目录下的 data/tasks.json
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "tasks.json"

MENU = """
--- 个人待办清单 ---
1. 添加待办事项
2. 查看所有待办事项
3. 标记某项为已完成
4. 删除某项待办
5. 编辑某项内容
6. 清空所有已完成事项
7. 查看统计信息
8. 退出程序
请选择操作："""


class _Exit(BaseException):
    """用户主动退出（正常退出或收到 EOF/Ctrl+C）。"""


def prompt(text: str) -> str:
    """读取用户输入；Ctrl+D/Ctrl+C 时抛出 _Exit 让程序优雅退出。"""
    try:
        return input(text)
    except (EOFError, KeyboardInterrupt):
        raise _Exit


def main() -> None:
    try:
        todos = TodoList(load(DATA_FILE))
    except Exception as exc:
        # 数据文件损坏时给出友好提示，而不是静默清空用户数据
        print(f"无法读取数据文件 {DATA_FILE}：{exc}")
        sys.exit(1)

    try:
        run(todos)
    except _Exit:
        # 用户以 EOF/Ctrl+C 退出，静默结束
        pass
    finally:
        print("再见！")


def run(todos: TodoList) -> None:
    """主循环，按数字选择分发操作。"""
    while True:
        choice = prompt(MENU).strip()
        if choice == "1":
            add_task(todos)
        elif choice == "2":
            show_list(todos.list())
        elif choice == "3":
            change_task(todos, mark_done=True)
        elif choice == "4":
            change_task(todos, mark_done=False, delete=True)
        elif choice == "5":
            edit_task(todos)
        elif choice == "6":
            clear_done(todos)
        elif choice == "7":
            show_stats(todos)
        elif choice == "8":
            return
        else:
            print("无效选项，请输入 1-8 之间的数字。")


def add_task(todos: TodoList) -> None:
    """添加待办：读取内容与优先级，写入并保存。"""
    title = prompt("请输入待办内容：").strip()
    if not title:
        print("内容不能为空，未添加。")
        return
    priority = prompt(f"请输入优先级({'/'.join(PRIORITIES)}，回车默认中)：").strip()
    if not priority:
        priority = "中"
    if priority not in PRIORITIES:
        print(f"无效优先级，已使用默认「中」。")
        priority = "中"
    task = todos.add(title, priority)
    save(todos.list(), DATA_FILE)
    print(f"已添加：{task.title}（优先级：{task.priority}）")


def change_task(todos: TodoList, mark_done: bool, delete: bool = False) -> None:
    """根据编号对某条任务执行「标记完成」或「删除」。"""
    tasks = todos.list()
    show_list(tasks)
    task = pick_task(tasks)
    if task is None:
        return
    if delete:
        todos.remove(task.id)
        action = "已删除。"
    else:
        todos.mark_done(task.id)
        action = "已标记完成。"
    save(todos.list(), DATA_FILE)
    print(action)


def edit_task(todos: TodoList) -> None:
    """编辑某条待办的内容。"""
    tasks = todos.list()
    show_list(tasks)
    task = pick_task(tasks)
    if task is None:
        return
    new_title = prompt("请输入新的内容：").strip()
    if not new_title:
        print("内容不能为空，未修改。")
        return
    todos.edit(task.id, new_title)
    save(todos.list(), DATA_FILE)
    print("已修改。")


def clear_done(todos: TodoList) -> None:
    """清空所有已完成事项。"""
    count = todos.clear_done()
    if count:
        save(todos.list(), DATA_FILE)
    print(f"已清空 {count} 条已完成事项。")


def show_stats(todos: TodoList) -> None:
    """打印任务总数、已完成与待办数。"""
    stats = todos.stats()
    print(
        f"共 {stats.total} 条："
        f"已完成 {stats.done} 条，待办 {stats.pending} 条。"
    )


def show_list(tasks: list[Task]) -> None:
    """打印全部任务（带序号、完成状态与优先级）。"""
    if not tasks:
        print("当前没有待办事项。")
        return
    status_marks = {True: "✓", False: "  "}
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. [{status_marks[task.done]}] [{task.priority}] {task.title}")


def pick_task(tasks: list[Task]) -> Task | None:
    """让用户按展示序号选择一条任务；无效输入返回 None。"""
    value = prompt("请输入任务编号：").strip()
    if not value.isdigit():
        print("请输入有效数字编号。")
        return None
    seq = int(value)
    if not 1 <= seq <= len(tasks):
        print("未找到该任务。")
        return None
    return tasks[seq - 1]


if __name__ == "__main__":
    main()