# 第 2 周练习报告 (Write-up)

提示：要预览此 markdown 文件

- 在 Mac 上，按 `Command (⌘) + Shift + V`
- 在 Windows/Linux 上，按 `Ctrl + Shift + V`

## 要求说明

请填写此文件中所有的 `TODO`。

## 提交信息

姓名： **jkd**
SUNet ID： **123**
引用来源： **None**

这份作业花了我大约 **1** 小时完成。

## 您的回答

对于每一个练习，除了生成回答的位置，还请写下您用于生成回答的提示词（prompts）。请务必在代码中加入清晰的注释，说明哪些部分是由 AI 生成的代码。

### 练习 1：搭建新功能

提示词 (Prompt):

```
分析 week2/app/services/extract.py 中现有的 extract_action_items() 函数，该函数目前使用预定义的启发式规则来找寻并提取待办事项。

您的任务是实现一个由 大语言模型（LLM）驱动 的替代方案 extract_action_items_llm()，利用 Ollama 让大语言模型执行待办事项提取任务。

一些提示：

要生成结构化输出（即字符串类型的 JSON 数组），请参阅此文档：https://ollama.com/blog/structured-outputs
目前可用的llama模型有：mistral-nemo:12b 和 llama3.1:8b
```

生成的代码片段 (Generated Code Snippets):

```
修改的文件：`week2/app/services/extract.py`

相关行号：
- 第 90 - 129 行：追加了核心的新功能替代函数 `extract_action_items_llm(text: str) -> List[str]`。
  - 包含了对输入文本为空的安全拦截 (`if not text.strip()`)。
  - 使用设计好的 system_prompt（强制返回 `"action_items"` JSON 对象机制）。
  - 调用 `ollama chat` 获取 Llama 的结果并启用了 `format="json"` 保证结构化输出。
  - 使用 `try-except` 包裹 JSON 的反序列化 `json.loads` 以及异常兜底设计防止应用崩溃。
```

### 练习 2：添加单元测试

提示词 (Prompt):

```
在 week2/tests/test_extract.py 中为 extract_action_items_llm() 编写单元测试，需涵盖多种输入情况（例如：带有项目符号的列表，带有指定关键字前缀的单行，甚至空输入）。
```

生成的代码片段 (Generated Code Snippets):

```
修改的文件：`week2/tests/test_extract.py`

相关行号：
- 第 4 行：修改导入语句，导入我们新编写的 `extract_action_items_llm` 函数。
  `(修改前: from ..app.services.extract import extract_action_items -> 修改后: from ..app.services.extract import extract_action_items, extract_action_items_llm)`
- 第 18 - 48 行：追加了 3 个全新的测试用例：
  - `test_extract_action_items_llm_empty()` (18-24行): 测试输入空文本和多空格环境是否会安全地返回空数组。
  - `test_extract_action_items_llm_bullets()` (27-38行): 测试常见的复选框标记（`- [ ]` 等）及加粗类待办项，并使用更具韧性的关键词检测匹配。
  - `test_extract_action_items_llm_keywords()` (41-48行): 测试各种带有 `TODO:`, `action:`, `next:` 关键词标识的首行缩进识别提取。
```

### 练习 3：重构现有代码以提高清晰度

提示词 (Prompt):

```
TODO
```

生成/修改的代码片段 (Generated/Modified Code Snippets):

```
修改的文件：
1. `week2/app/schemas.py` （新文件）
2. `week2/app/routers/action_items.py`
3. `week2/app/routers/notes.py`
4. `week2/app/main.py`
5. `week2/app/db.py`

重构详情与相关行号：
- 定义良好的 API 契约/数据模式（Schemas）：
  新创建了 `app/schemas.py` 文件（第 1-32 行）。在其中通过继承 Pydantic 的 `BaseModel` 为后端 API 的请求 (Request) 和响应 (Response) 设计了严谨的验证模型（例如：`NoteCreate`, `ActionItemResponse`, `ExtractRequest` 等），消除了之前满天飞且不安全的 `Dict[str, Any]`。
- 重构路由层引用：
  在 `app/routers/action_items.py`（第 16 - 72 行）和 `app/routers/notes.py`（第 13 - 42 行）引入了新的 Schema 类型，并将 FastAPI 端点的返回值强制锁定到了 `response_model` 类型上。
- 应用程序生命周期/配置重构：
  在 `app/main.py` (第 13 - 18 行)，将原本在模块顶层直接粗暴调用的的 `init_db()` 改写成了 FastAPI 现代生命周期管理（Lifespan Events） `@asynccontextmanager async def lifespan(app: FastAPI)`，使得数据库的加载仅在服务器真正安全启动的阶段才执行，更加纯粹可控。
- 错误处理：
  为 `action_items.py` 和 `notes.py` 的数据库写入或读取过程增添了 `try-except` 包裹（例如捕捉到 `Exception` 后规范地抛出 HTTP 状态码 500）。
- 清理数据库连接层：
  在 `app/db.py` (第 16 - 25 行) 改造了原先无资源释放设计的 `get_connection`。我使用了 `@contextmanager` 装饰器对连接进行改造（`yield conn ... finally: conn.close()`），保证不管 SQL 执行成败，每一笔请求过后数据库连接都会被安全地关闭释放，杜绝了底层泄漏的隐患。
```

### 练习 4：使用 Agentic 模式自动执行一项自动化小任务

提示词 (Prompt):

```
1. 将大语言模型（LLM）驱动的提取功能集成为一个新的 API 接口。并更新前端页面，去加入一个“Extract LLM”的按钮，被点击时，该前端就能调用新接口触发后台的大语言模型提取过程。

2. 增加并开放最后一个用以获取所有已记录笔记的 API 接口。更新前端页面，加入一个“List Notes”按钮，点击时就会去获取并显示所有的笔记资料。xxxxxxxxxx 1. 将大语言模型（LLM）驱动的提取功能集成为一个新的 API 接口。并更新前端页面，去加入一个“Extract LLM”的按钮，被点击时，该前端就能调用新接口触发后台的大语言模型提取过程。2. 增加并开放最后一个用以获取所有已记录笔记的 API 接口。更新前端页面，加入一个“List Notes”按钮，点击时就会去获取并显示所有的笔记资料。TODO
```

生成的代码片段 (Generated Code Snippets):

```
修改的文件与相关行号：

1. `week2/app/routers/action_items.py`
   - 第 4-6 行：修改了导入，引入了新依赖的 `extract_action_items_llm` 函数。
   - 第 43-69 行：新增了 `@router.post("/extract-llm")` 的端点。实现了接收请求、保存原始文本笔记，并将文本传递给大模型后端来提取、持久化和返回。

2. `week2/app/routers/notes.py`
   - 第 14-25 行：新增了 `@router.get("")` 处理列出所有笔记的端点 `list_all_notes()`，它将通过调用底层的 `db.list_notes()` 获取所有项目返回封装。

3. `week2/frontend/index.html`
   - 第 26-28 行：在 DOM 中并添加了两个新的核心按钮控件：`<button id="extractLlm">Extract LLM</button>`和 `<button id="listNotesBtn">List Notes</button>`。
   - 第 32-33 行：加入了标记用来呈现新列表的数据容器 `<h2>Notes Directory</h2>` 与 `<div class="items" id="notesList"></div>`。
   - 第 38-40 行：定义和声明并抓取了页面上对应的 `llmBtn` 与 `listNotesBtn` 对象与存放节点。
   - 第 42-56 行：将原有硬编码的 extract 事件逻辑重构成更加泛用的功能函数 `performExtract(endpoint)`，支持向新旧两个不同的后端端点发送 `POST` 解析数据。
   - 第 80-81 行：应用重构后的绑定，分别给两个 extract 按钮配置正确的调用 URL 端点。
   - 第 83-102 行：补全针对 List Notes 按钮所绑定的完整的 fetch 事件、DOM 更新等一整套前端交互，并且对列表内的排版进行简易渲染设定样式处理。
```

### 练习 5：从代码库生成 README 说明

提示词 (Prompt):

```
对week2的项目审查与分析，以此去自动生成一个结构良好的 README.md 文件。你的要求是该 README 文件至少必须包括：

项目的简要说明/概述
如何建立和配置、运行此项目
各 API 接口列表及对应的说明介绍
关于如何运行测试套件机制的使用说明
```

生成的代码片段 (Generated Code Snippets):

```
创建的文件：`week2/README.md`

主要生成内容覆盖：
- 概述了这是一个基于 FastAPI + SQLite 带有两种不同逻辑双引擎（正则匹配和本地 Ollama 提取）驱动的 Action Item 全栈项目。
- 配置运行说明中提到了 `conda activate cs146s`、拉取模型的 `ollama pull` 以及使用 Poetry 拉起服务器的命令 `poetry run uvicorn week2.app.main:app --reload`。
- API 接口列出了分为 Notes 以及 Action Items 的详细端点（重点描述了新增的 `extract-llm` 和获取相关记录的接口）。
- 测试套件说明给出了完整的 `poetry run pytest` 测试验证命令及其参数含义。
```

## 提交说明

1. 按 `Command (⌘) + F`（或 `Ctrl + F`）去查找此文件中是否还残留着 `TODO`。如果找不到了，恭喜——您已经填好了所有必填的字段。
2. 确保您已将所有的更改提交（push）到您远端的 Git 仓库以便评审打分。
3. 请通过 Gradescope 进行提交通知。
