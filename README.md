# todo-cli

一个纯命令行（CLI）的个人待办清单（To-Do List）工具。通过数字菜单即可添加、查看、标记完成、编辑、删除待办事项，数据保存在本地 JSON 文件中，**重启程序后数据不丢失**。

## 功能

- ✅ 添加待办事项（支持优先级 高/中/低）
- 🔍 查看所有事项（显示序号、完成状态、优先级）
- ✔️ 标记某项为已完成
- 🗑️ 删除某项待办
- ✏️ 编辑某项内容
- 🧹 清空所有已完成事项
- 📊 查看统计信息（总数 / 已完成 / 待办）
- 🚪 退出程序

## 技术栈

- Python 3.10+，**仅使用标准库**（`dataclasses`、`json`、`pathlib`）
- 测试：`pytest`
- 包管理与虚拟环境：`uv`

## 快速开始

```bash
# 1) 安装依赖并创建虚拟环境
uv sync

# 2) 运行（方式一：模块）
uv run python -m todo_cli

# 3) 运行（方式二：安装后的命令，二选一）
uv run todo
```

运行后按提示输入数字即可操作。

## 运行测试

```bash
uv run pytest -q
```

## 数据存储

任务保存于项目根目录下的 `data/tasks.json`（运行后自动生成，已在 `.gitignore` 中忽略）。文件不存在时自动初始化为空；若文件损坏，程序会给出友好提示而**不会静默清空你的数据**。

## 目录结构

```
todo_cli/
  core.py      # Task 模型 + TodoList 业务逻辑（增删改查、统计、清空）
  storage.py   # JSON 持久化（加载/保存）
  __main__.py  # 交互式命令行菜单入口
tests/
  test_core.py        # 核心逻辑测试
  test_storage.py     # 持久化测试
  test_features.py    # 增强功能测试
data/tasks.json       # 运行时生成的数据文件
```

## 许可证

[MIT](./LICENSE)