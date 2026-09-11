"""待办任务的 JSON 持久化：加载与保存。"""

from __future__ import annotations

import json
from pathlib import Path

from .core import Task

# 任务序列化的字段顺序，写入 JSON 时保持一致
_FIELDS = ("id", "title", "done", "priority")


def load(path: Path) -> list[Task]:
    """从 JSON 文件加载任务列表；文件不存在时返回空列表。"""
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return [Task(**item) for item in data]


def save(tasks: list[Task], path: Path) -> None:
    """把任务列表写入 JSON 文件（自动创建父目录）。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [{field: getattr(t, field) for field in _FIELDS} for t in tasks]
    # ensure_ascii=False 保持中文可读；indent=2 便于人工查看
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)