"""待办任务的核心业务逻辑：数据模型与增删改查操作（纯净，不做 IO）。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Task:
    """单条待办事项。"""

    id: int
    title: str
    done: bool = False


class TodoList:
    """待办清单：维护任务列表，对外提供增删改查操作。"""

    def __init__(self, tasks: list[Task] | None = None) -> None:
        # 转为私有副本，避免外部误改内部状态
        self._tasks = [Task(**item) if isinstance(item, dict) else item for item in (tasks or [])]
        self._next_id = max((t.id for t in self._tasks), default=0) + 1

    def add(self, title: str) -> Task:
        """新增一条待办，返回新任务。"""
        task = Task(id=self._next_id, title=title)
        self._next_id += 1
        self._tasks.append(task)
        return task

    def list(self) -> list[Task]:
        """返回全部任务（调用方不应直接改动其中的对象）。"""
        return list(self._tasks)

    def mark_done(self, task_id: int) -> Task | None:
        """按 id 将任务标记为已完成；不存在返回 None。"""
        task = self._find(task_id)
        if task is None:
            return None
        task.done = True
        return task

    def remove(self, task_id: int) -> bool:
        """按 id 删除任务；成功返回 True，不存在返回 False。"""
        task = self._find(task_id)
        if task is None:
            return False
        self._tasks.remove(task)
        return True

    def _find(self, task_id: int) -> Task | None:
        return next((t for t in self._tasks if t.id == task_id), None)