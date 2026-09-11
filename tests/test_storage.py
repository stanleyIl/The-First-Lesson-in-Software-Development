"""storage 持久化的单元测试：往返一致、中文、缺文件、损坏数据。"""

import json

import pytest

from todo_cli.core import Task
from todo_cli.storage import load, save


def test_save_load_roundtrip(tmp_path):
    path = tmp_path / "tasks.json"
    tasks = [
        Task(id=1, title="买菜", done=True, priority="高"),
        Task(id=2, title="写报告", done=False, priority="中"),
    ]
    save(tasks, path)
    loaded = load(path)
    assert [(t.id, t.title, t.done, t.priority) for t in loaded] == [
        (1, "买菜", True, "高"),
        (2, "写报告", False, "中"),
    ]


def test_load_missing_file_returns_empty(tmp_path):
    assert load(tmp_path / "nope.json") == []


def test_save_creates_parent_directory(tmp_path):
    nested = tmp_path / "a" / "b" / "tasks.json"
    save([Task(id=1, title="x")], nested)
    assert nested.exists()


def test_json_is_utf8_readable(tmp_path):
    # 中文应以可读形式写入，而不是 unicode 转义
    path = tmp_path / "tasks.json"
    save([Task(id=1, title="中文待办")], path)
    raw = path.read_text(encoding="utf-8")
    assert "中文待办" in raw


def test_load_corrupt_json_raises(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text("{ this is not valid json", encoding="utf-8")
    with pytest.raises(Exception):
        load(path)


def test_load_backward_compatible_without_priority(tmp_path):
    # 旧版本数据没有 priority 字段，应能正常加载（使用默认值）
    path = tmp_path / "tasks.json"
    path.write_text(json.dumps([{"id": 1, "title": "旧任务", "done": False}]), encoding="utf-8")
    tasks = load(path)
    assert tasks[0].priority == "中"