"""待办任务的核心业务逻辑：数据模型与增删改查、统计、清空操作（纯净，不做 IO）。"""

from __future__ import annotations

from dataclasses import dataclass, field

# 优先级取值：默认"中"，可校验为 高/中/低
PRIORITIES = ("高", "中", "低")


@dataclass
class Task:
    """单条待办事项。"""

    id: int
    title: str
    done: bool = False
    priority: str = "中"


@dataclass
class Stats:
    """待办清单统计数据。"""

    total: int
    done: int

    @property
    def pending(self) -> int:
        return self.total - self.done


class TodoList:
    """待办清单：维护任务列表，对外提供增删改查等操作。"""

    def __init__(self, tasks: list[Task] | None = None) -> None:
        # 转为私有副本，避免外部误改内部状态
        self._tasks = [Task(**item) if isinstance(item, dict) else item for item in (tasks or [])]
        self._next_id = max((t.id for t in self._tasks), default=0) + 1

    def add(self, title: str, priority: str = "中") -> Task:
        """新增一条待办，返回新任务。"""
        task = Task(id=self._next_id, title=title, priority=priority)
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

    def edit(self, task_id: int, new_title: str) -> Task | None:
        """按 id 修改待办内容；不存在返回 None。"""
        task = self._find(task_id)
        if task is None:
            return None
        task.title = new_title
        return task

    def clear_done(self) -> int:
        """移除所有已完成的任务，返回移除数量。"""
        done = [t for t in self._tasks if t.done]
        self._tasks = [t for t in self._tasks if not t.done]
        return len(done)

    def stats(self) -> Stats:
        """统计总数与已完成数。"""
        return Stats(total=len(self._tasks), done=sum(1 for t in self._tasks if t.done))

    def _find(self, task_id: int) -> Task | None:
        return next((t for t in self._tasks if t.id == task_id), None)