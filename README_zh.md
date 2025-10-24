
# Git 助手

一个使用 Python 和 LangChain 构建的交互式 Git 助手。本项目提供一个命令行代理，将常见的 Git 操作（init、status、add、commit、push、pull、clone、diff 等）作为语言模型可调用的工具暴露出来。代理在本地运行并在使用这些工具执行 Git 和文件操作时流式输出响应。

## 功能

- 交互式命令行代理，接受自然语言提示并执行 git/文件工具。
- 已实现的工具：git init/status/add/commit/log/branch/checkout/merge/push/pull/clone/diff/reset，以及文件读写/列树(tree)工具。
- 中间件错误处理，返回更友好的工具错误信息。

## 依赖

- Python 3.8+
- 运行时依赖见 `requirements.txt`。

安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

## 配置（.env）

在仓库根目录创建 `.env` 文件（与 `requirements.txt` 和本 README 在同一目录）。代码期望一些用于语言模型客户端的环境变量。示例 `.env` 内容：

```bash
DEFAULT_MODEL=your-model-name
BASE_URL=https://api.your-llm-provider.com
# 如果提供商使用 API key，请按需添加（变量名因提供商而异）：
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

根据你的模型/提供商设置调整这些变量。`src/main.py` 引用了 `DEFAULT_MODEL` 和 `BASE_URL`，不同提供商可能还需要其他环境变量。

## 如何运行

1. 安装依赖（见上文）。
2. 创建 `.env` 并填写模型/认证信息。
3. 运行代理：

```bash
python3 src/main.py
```

启动后会出现提示符。输入自然语言来描述 git 任务（例如："显示 /path/to/repo 的 git status"、"创建名为 feature/x 的新分支"、"将 README.md 添加并提交，提交信息为 'update'" 等）。输入 `exit` 退出。

## 说明与安全

- 代理会在你提供的路径上执行 Git 命令。实验时请小心，建议在测试仓库或临时仓库中操作。
- 该代码使用语言模型来决定调用哪些工具 —— 在对重要仓库执行变更前，请始终审阅代理输出和执行结果。

## 贡献

欢迎贡献。如果你添加工具或更改行为，请同时更新这些 README 并在合适位置添加测试。
