# Action Item Extractor (Week 2)

## 📌 项目概述 (Project Overview)

Action Item Extractor 是一个基于 FastAPI 和 SQLite 构建的全栈 Web 应用程序。它的主要功能是从用户输入的自由格式笔记（会议记录、备忘录等）中自动提取“待办事项” (Action Items)。
该项目支持两种提取模式：

1. **基于启发式规则 (Heuristics-based)**：利用正则表达式和关键词匹配快速提取待办项。
2. **基于大语言模型 (LLM-powered)**：利用本地部署的 Ollama (`llama3.1:8b`) 通过 AI 语义理解来精准提取待办任务。

前端使用极简的 HTML + 原生 JavaScript 实现，提供交互式提取、笔记查阅以及勾选完成任务的 Web 界面。

## 🚀 环境配置与运行 (Setup & Run)

### 1. 环境准备

项目依赖于 Python、Poetry 以及 Conda 虚拟环境。为了使用大语言模型提取功能，你需要确保本地已经安装并运行了 [Ollama](https://ollama.com/) 且拉取了相关模型。

```bash
# 激活 Conda 虚拟环境
conda activate cs146s

# （可选）拉取用于提取的本地大模型
ollama pull llama3.1:8b
```

### 2. 启动服务器

在项目根目录下，使用 Poetry 运行 Uvicorn 开发服务器：

```bash
poetry run uvicorn week2.app.main:app --reload
```

启动成功后，控制台会提示服务器已运行在端口 `8000`。

### 3. 访问应用

- **Web 界面**: 在浏览器中打开 http://127.0.0.1:8000/
- **交互式 API 文档 (Swagger UI)**: 在浏览器中打开 http://127.0.0.1:8000/docs

## 🖧 API 接口说明 (API Endpoints)

FastAPI 自动处理了请求与响应的数据校验 (Pydantic Schemas)。以下是后端提供的主要 RESTful API 列表：

### 笔记 (Notes) 相关

- `POST /notes`
  - **说明**: 将用户传入的纯文本保存为一条新笔记记录。
- `GET /notes`
  - **说明**: 获取数据库中保存的所有历史笔记列表（根据时间倒序排列）。
- `GET /notes/{note_id}`
  - **说明**: 根据指定的 ID 获取单条笔记的详细内容。

### 待办事项 (Action Items) 相关

- `POST /action-items/extract`
  - **说明**: 接收文本并使用“启发式规则”提取待办事项。可以选择是否同步保存原始文本为笔记。返回该笔记 ID 及提取到的待办列表。
- `POST /action-items/extract-llm`
  - **说明**: 接收文本并利用本地 LLM (Ollama) 智能识别和提取待办事项。自动过滤掉冗余信息以保持极高的数据结构化准度。
- `GET /action-items`
  - **说明**: 获取存储的待办事项。可以通过附带 `note_id` 查询参数来筛选属于某一条特定笔记的待办事项。
- `POST /action-items/{action_item_id}/done`
  - **说明**: 标记某个特定的待办事项为“已完成 (Done)”，参数传入 `{"done": true}` 或 `{"done": false}` 控制勾选状态。

## 🧪 运行测试套件 (Testing)

项目使用 `pytest` 编写了单元测试（位于 `week2/tests/` 目录），涵盖了对于不同格式文本（空文本、复选框文本、关键词前缀文本等）在传统规则提取和 LLM 提取下的可用性验证。

在项目根目录下打开终端，确保激活虚拟环境后运行以下命令执行全量测试：

```bash
poetry run pytest week2/tests/test_extract.py -s
```

_注：`-s` 参数用于关闭输出捕获，你可以直观地在终端中看到测试时记录的具体控制台信息。_
