## 项目概述
纯命令行（CLI）个人待办清单（To-Do List）工具。用户通过数字菜单选择操作：添加、查看、标记完成、删除待办，数据保存在本地 JSON 文件中，程序重启后不丢失。

## 技术栈
- Python 3.12，仅使用标准库（`dataclasses`、`json`、`pathlib`、`argparse` 等）
- 测试：pytest（开发期依赖）
- 包管理/虚拟环境：uv（项目依赖 `[project.dependencies]`，开发依赖在 `[dependency-groups].dev`）

## 目录结构
```
todo_cli/
  core.py      # Task 模型 + TodoList 业务逻辑（纯净，不做 IO）
  storage.py   # JSON 持久化（加载/保存）
  __main__.py  # 交互式命令行菜单入口（`python -m todo_cli`）
tests/
  test_core.py # 单元测试
data/tasks.json  # 运行时生成的数据文件（gitignore，不提交）
```

## 关键入口 / 核心模块
- 入口：`python -m todo_cli`（交互菜单，输入数字选择操作）
- `core.TodoList`：对外提供 `add()/list()/mark_done()/remove()` 操作
- `storage`：`load(path)` 读 JSON，`save(tasks, path)` 写 JSON；文件不存在时返回空列表
- 任务字段：`id`（自增稳定标识）、`title`（内容）、`done`（完成状态）

## 运行与预览
- 运行：`uv run python -m todo_cli`
- 测试：`uv run pytest -q tests/`
- 本产品为纯 CLI，`preview_enable = "disabled"`（不可预览，无网页/小程序界面），数据文件由程序运行时在 `data/tasks.json` 中生成。

## 用户偏好与长期约束
- 仅依赖 Python 标准库，不引入复杂第三方框架
- 不接入真实用户数据、不处理隐私信息、不用于生产环境（安全要求）
- 数据保存在本地 JSON，重启不丢失
- 关键步骤保留中文注释

## 常见问题和预防
- JSON 文件损坏时 `storage.load` 会选择性失败：读到无效 JSON 时抛出异常，由 `__main__` 捕获并给出友好提示，不静默清空用户数据。
- 删除后任务 id 不回退（用自增 id 保证稳定性，展示序号独立计算）。