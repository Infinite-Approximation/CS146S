# 第 2 周 – 待办事项提取器

本周，我们将扩展一个极简的 FastAPI + SQLite 应用程序，将其用于把自由格式的笔记转换为带编号的待办事项。

**_我们建议在开始操作之前完整阅读本篇文档。_**

提示：要预览此 markdown 文件

- 在 Mac 上，按 `Command (⌘) + Shift + V`
- 在 Windows/Linux 上，按 `Ctrl + Shift + V`

## 准备开始

### Cursor 设置

按照以下说明设置 Cursor 并打开您的项目：

1. 兑换您的一年免费 Cursor Pro：https://cursor.com/students
2. 下载 Cursor：https://cursor.com/download
3. 要启用 Cursor 命令行工具，请打开 Cursor，Mac 用户按 `Command (⌘) + Shift+ P`（非 Mac 用户按 `Ctrl + Shift + P`）打开命令面板。输入：`Shell Command: Install 'cursor' command`。选中它并按回车。
4. 打开一个新的终端窗口，导航到您的项目根目录，然后运行：`cursor .`

### 当前应用程序

您可以按以下方法运行当前的初始应用程序：

1. 激活您的 conda 环境。

```bash
conda activate cs146s
```

2. 从项目根目录运行服务器：

```bash
poetry run uvicorn week2.app.main:app --reload
```

3. 打开 Web 浏览器并导航到 http://127.0.0.1:8000/。
4. 熟悉应用程序的当前状态。确保您可以成功输入笔记并生成提取出的待办事项清单。

## 练习

对于每个练习，请使用 Cursor 帮助您实现对当前待办事项提取器应用程序的指定优化改进。

在您完成作业的过程中，请使用 `writeup.md` 记录您的进度。请务必附上您使用的提示词（prompts），以及您或 Cursor 所做的任何更改。我们将根据您的报告（write-up）内容进行评分。也请在代码中添加关键注释来记录您的更改。

### TODO 1: 搭建新功能

分析 `week2/app/services/extract.py` 中现有的 `extract_action_items()` 函数，该函数目前使用预定义的启发式规则来找寻并提取待办事项。

您的任务是实现一个由 **大语言模型（LLM）驱动** 的替代方案 `extract_action_items_llm()`，利用 Ollama 让大语言模型执行待办事项提取任务。

一些提示：

- 要生成结构化输出（即字符串类型的 JSON 数组），请参阅此文档：https://ollama.com/blog/structured-outputs
- 要浏览可用的 Ollama 模型，请参阅此文档：https://ollama.com/library。请注意，越大的模型将越耗费系统资源，因此请从较小的模型开始测试。拉取并运行命令示例：`ollama run {MODEL_NAME}`

### TODO 2: 添加单元测试

在 `week2/tests/test_extract.py` 中为 `extract_action_items_llm()` 编写单元测试，需涵盖多种输入情况（例如：带有项目符号的列表，带有指定关键字前缀的单行，甚至空输入）。

### TODO 3: 重构现有代码以提高清晰度

重构后端处的代码，重点关注这几项：定义良好的 API 接口契约/数据模式（schemas）、数据库层清理、应用程序生命周期/配置，以及错误处理机制。

### TODO 4: 使用 Agentic 模式自动执行自动化小任务

1. 将大语言模型（LLM）驱动的提取功能集成为一个新的 API 接口。并更新前端页面，去加入一个“Extract LLM”的按钮，被点击时，该前端就能调用新接口触发后台的大语言模型提取过程。

2. 增加并开放最后一个用以获取所有已记录笔记的 API 接口。更新前端页面，加入一个“List Notes”按钮，点击时就会去获取并显示所有的笔记资料。

### TODO 5: 从代码库生成 README 说明

**_学习目标：_**
_学生们将了解人工智能如何检查、反省给定的代码库去自动生成软件文档与说明文档。同时也展现 Cursor 工具理解代码上下文并将其转换为人便读形式文档的强大能力。_

使用 Cursor 审查与分析当前的代码库，以此去自动生成一个结构良好的 `README.md` 文件。你的要求是该 README 文件至少必须包括：

- 项目的简要说明/概述
- 如何建立和配置、运行此项目
- 各 API 接口列表及对应的说明介绍
- 关于如何运行测试套件机制的使用说明

## 交付物

请对照上述的提示与要求去独立或辅助填好 `week2/writeup.md` 中需要汇报记录的详情。一定要确保在代码库中也完整记下了你的变更足迹。

## 评估标准（总分 100 分）

- 1-5 各个部分单独评估占 20 分（成功生成有效代码占 10 分，每一个对应好的 prompt / 提示词占 10 分）。
