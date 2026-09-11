"""交互式命令行菜单入口：`python -m todo_cli`。

用户通过输入数字选择操作：添加、查看、标记完成、删除、退出。
"""

from __future__ import annotations

import sys
from pathlib import Path

from .core import Task, TodoList
from .storage import load, save

# 数据文件默认存放在项目根目录下的 data/tasks.json
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "tasks.json"

MENU = """
--- 个人待办清单 ---
1. 添加待办事项
2. 查看所有待办事项
3. 标记某项为已完成
4. 删除某项待办
5. 退出程序
请选择操作："""


def main() -> None:
    try:
        todos = TodoList(load(DATA_FILE))
    except Exception as exc:
        # 数据文件损坏时给出友好提示，而不是静默清空用户数据
        print(f"无法读取数据文件 {DATA_FILE}：{exc}")
        sys.exit(1)

    while True:
        choice = input(MENU).strip()
        if choice == "1":
            title = input("请输入待办内容：").strip()
            if not title:
                print("内容不能为空，未添加。")
                continue
            task = todos.add(title)
            save(todos.list(), DATA_FILE)
            print(f"已添加：{task.title}")
        elif choice == "2":
            show_list(todos.list())
        elif choice == "3":
            tasks = todos.list()
            show_list(tasks)
            target = pick_task(tasks)
            if target is None:
                continue
            todos.mark_done(target.id)
            save(todos.list(), DATA_FILE)
            print("已标记完成。")
        elif choice == "4":
            tasks = todos.list()
            show_list(tasks)
            target = pick_task(tasks)
            if target is None:
                continue
            todos.remove(target.id)
            save(todos.list(), DATA_FILE)
            print("已删除。")
        elif choice == "5":
            print("再见！")
            break
        else:
            print("无效选项，请输入 1-5 之间的数字。")


def show_list(tasks: list[Task]) -> None:
    """打印全部任务（带序号和完成状态）。"""
    if not tasks:
        print("当前没有待办事项。")
        return
    status_marks = {True: "✓", False: "  "}
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. [{status_marks[task.done]}] {task.title}")


def pick_task(tasks: list[Task]) -> Task | None:
    """让用户按展示序号选择一条任务；无效输入返回 None。"""
    value = input("请输入任务编号：").strip()
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