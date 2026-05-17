# 第 4 周 — 现实中的自主编程智能体 (The Autonomous Coding Agent IRL)

> **_我们建议在开始之前通读整篇文档。_**

本周，你的任务是在本代码库的上下文中构建至少 **2 个自动化工作流**，你可以使用以下任意 **Claude Code** 功能的组合：

- 自定义斜杠命令 (slash commands)（被检入到 `.claude/commands/*.md` 路径中）
- 用于代码库或上下文指导的 `CLAUDE.md` 文件
- Claude SubAgents (子智能体)（协同工作的特定角色智能体）
- 集成到 Claude Code 中的 MCP 服务器

你的自动化项目应当能够切实改善开发者的工作流——例如，通过简化测试、自动生成文档、代码重构或数据相关任务。随后，你将使用你创建的自动化工作流，对 `week4/` 中提供的初始应用程序进行功能扩展与提升。

## 学习关于 Claude Code

要深入了解 Claude Code 并探索你的自动化构建选项，请阅读以下两份资源：

1. **Claude Code 最佳实践 (Best practices)：** [anthropic.com/engineering/claude-code-best-practices](https://www.anthropic.com/engineering/claude-code-best-practices)

2. **子智能体概述 (SubAgents overview)：** [docs.anthropic.com/en/docs/claude-code/sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)

## 探索初始应用程序

这是一个旨在作为 **“开发者命令中心 (developer's command center)”** 的极简全栈起步应用。

- 基于 SQLite (SQLAlchemy) 的 FastAPI 后端
- 静态前端 (无需 Node 工具链)
- 极简的测试套件 (pytest)
- Pre-commit 钩子配置 (black + ruff)
- 用于练习由智能体驱动的工作流的各种任务

你可以把这个应用程序作为你的游乐场，来尝试及实验你所构建的 Claude 自动化。

### 目录结构

```text
backend/                # FastAPI 应用
frontend/               # 由 FastAPI 所承载的静态 UI
data/                   # SQLite 数据库 + 初始种子数据
docs/                   # 用于智能体驱动工作流的 TASKS 和指南
```

### 快速起步

1. 激活你的 conda 环境。

```bash
conda activate cs146s
```

2. (可选) 安装 pre-commit 钩子

```bash
pre-commit install
```

3. 运行应用 (在 `week4/` 目录下执行)

```bash
make run
```

4. 打开 `http://localhost:8000` 访问前端界面，打开 `http://localhost:8000/docs` 访问 API 文档。

5. 随手探索一下这个起步应用，以了解它目前包含的特性和功能机制。

### 测试验证

运行测试 (在 `week4/` 目录下执行)

```bash
make test
```

### 代码格式化/代码检查 (Linting)

```bash
make format
make lint
```

## 第一部分：构建你的自动化工作流 (至少选择 2 个)

既然你已经熟悉了初始应用，你的下一步就是构建自动化流程来增强它或扩展它的功能。下面提供了几种自动化方案供你选择，你可以随意搭配各类别进行组装实现。

当你构建自身的自动化时，请记录到 `writeup.md` 文件中。暂时将 _“你如何使用它去增强初始应用程序 (How you used the automation to enhance the starter application)”_ 这一小节留空 —— 在作业的第二部分中才会回到这里补充它。

### A) Claude 自定义斜杠命令 (custom slash commands)

斜杠命令通过读取位于 `.claude/commands/` 下的 Markdown 文件创建可复用的工作流功能，主要用于重复出现的各类工作流程。Claude 可以通过 `/` 来暴露及调用它们。

- 示例 1: 带有代码覆盖率的测试运行器
  - 名称: `tests.md`
  - 意图: 执行 `pytest -q backend/tests --maxfail=1 -x`，如果测试通过变绿，则运行 coverage 覆盖率检测。
  - 输入参数: 可选的 marker 标记或运行路径。
  - 预期输出: 总结失败的错误用例并对下一步操作提出建议。
- 示例 2: 文档同步器
  - 名称: `docs-sync.md`
  - 意图: 读取 `/openapi.json` 获取规范参数，更新 `docs/API.md`，并列举出发生改变的路由增量/减量细节。
  - 预期输出: 提供类 Diff 的摘要和生成的 TODO 任务项。
- 示例 3: 重构助手 (Refactor harness)
  - 名称: `refactor-module.md`
  - 意图: 重命名一个模块 (例如，`services/extract.py` → `services/parser.py`)，重构所涉及的各类引入关系，并运行代码风格检查和单元测试。
  - 预期输出: 被修改文件的复选框核对清单以及检验步骤指南。

> _提示：力求命令保持聚焦与简洁，要懂得使用 `$ARGUMENTS` 变量获取动态数据，并尽量倾向于使执行步骤具有幂等性 (idempotent steps)。考虑将安全的工具列入白名单并通过无头验证环境 (headless mode) 获得良好的工作流可重复性。_

### B) `CLAUDE.md` 指导描述文件

`CLAUDE.md` 是在启动新对话时便会被自动默认读取的文件，使你得以为代码库下发项目级别的结构特有指令、上下文情景介绍或指导方针，以此来影响或规约 Claude 的行为输出。通过在代码库根目录下创建 `CLAUDE.md` (同样也可在其包含的 `week4/` 子目录里进行特定覆盖创建) 将可以大幅改善 AI 在项目环境中的表现。

- 示例 1: 代码导航和应用入口描述
  - 内容包含: 告知 AI 应当如何运行起本应用、相关的请求路由写在了哪里 (`backend/app/routers`)，对应单元测试存放在哪、以及关于如何植入测试 DB 的说明。
- 示例 2: 编码风格约束与安全防范护栏 (safety guardrails)
  - 内容包含: 代码工具期望规范（例如要用 black/ruff 约束格式）、阐明允许运行哪些安全的命令、避免去尝试执行哪些危险的命令、指明使用相关格式检查和测试的准入命令等。
- 示例 3: 固定工作流水线片段
  - 内容包含: “当你被要求新增一个端点接口时，请**先**写一段包含预期的故意失败形式的单元测试，接着再实现接口路由逻辑，最后触发运行 pre-commit 钩子约束检查。”

> _提示：需要把 `CLAUDE.md` 看做在像调试某个提示词 (prompt) 一样去进行迭代，维持长话短说但必须具体体现出“可操作性”。并且请提前为你期望 Claude 能够执行用到的各类自定义脚本进行好文字说明约定。_

### C) SubAgents 子智能体 (角色专长分工化)

SubAgents 是被配置为专门处理特定种类任务领域的专用型 AI 助理助手，它们会挂载了拥有独立设定配置的系统级的提示词 (system prompts)，配备自己特有的工具使用权限、以及独立的上下文追踪。你需要设计出至少两个乃至更多的可相互配合协作的智能体，使它们每一个都在一套自动化流水线流程的个别步骤上拥有清晰独特的任务指责边界。

- 示例 1: 测试智能体 (TestAgent) + 编码智能体 (CodeAgent)
  - 工作流机制: TestAgent 负责因为一项代码改动而去写对应补丁/更新单元测试用例 → CodeAgent 负责根据测试去真正执行能够 pass 通过这些测试的修复代码 → TestAgent 最后再完成验证闭环审核。
- 示例 2: 文档智能体 (DocsAgent) + 编码智能体 (CodeAgent)
  - 工作流机制: CodeAgent 被安排编写一项新的 API 通讯路由逻辑 → DocsAgent 随后跟进自动化更新 `API.md` 和 `TASKS.md`，并在中途随时检查核对自身与 `/openapi.json` 的偏移问题。
- 示例 3: 数据库智能体 (DBAgent) + 重构智能体 (RefactorAgent)
  - 工作流机制: DBAgent 拟定出一项对表模式 Schema 进行改变的方案 (例如对 `data/seed.sql` 做了变更修改) → RefactorAgent 则在收到 Schema 模型修改后，及时跟进完成对对应的 ORM Data 模型、通信参数路由的更改并且去修复任何连带造成的 linting 格式规范违规。

> _提示：可以去设计使用清单/检查任务表 (checklists) 去作为不同 Agent 交接时作为任务追踪的“草稿板”，也要利用在进行不同角色切换扮演之间重置环境语境 (`/clear`) 的策略，对不需要交接上下文串联的流程，甚至可以安排不同的 Agent 对独立的任务流实现并行的处理操作。_

## 第二部分：把你的自动化工作流投入到实际战斗运作里

既然你构建完了 2+ 自动化机制设计了，接下来就是去使用它们的环节了！在 `writeup.md` 文件里前往 _"你如何使用了此自动化工作流来增强初始应用程序的"_ 对应的模块，对其如何协助你扩展出初始应用中新的特性并发挥作用进行描述。

试以刚才讲述例作参考：假如你实现的是自定义斜杠指令 `/generate-test-cases`，在这里说明清楚你是如何去通过操作使用此指令而完成对初始应用的交互与测试构建的。

## 提交内容 (Deliverables)

1. 两个或是以上的自动化策略的运用产出成果，这其中也许能涵盖：
   - 包含在 `.claude/commands/*.md` 里的斜杠运行指令 (Slash commands)
   - 设置完成的项目指引文件 `CLAUDE.md`
   - 对所涉及的所有智能体配置/提示词 (SubAgent prompts) 等脚本配置的记录保存。

2. 提交位于 `week4/` 的记录文件 `writeup.md`，里面须记录包含下述板块：

- 设计理念以及设计从何处借用了创意启发 (如引用之前提过最佳实践链接页面与/或是某段 agent 文档章节)。
- 对个别所选用自动化构建策略的细致设计结构（体现了自身要解决和达成的目标，对应的输出与输出规范格式、具体所操作实现它的全部流程等）。
- 有关要以怎样命令行形式能跑起它的用法文档 (含特定的调用执行全代码步骤)，期盼出现的测试最终输出表象行为、如何规避以及保障安全的失败回退行为记录。
- 用实施使用自动化和单纯手工作坊之间进行的效能成果等前后改进状态对比分析。
- 你是如何实际在这个项目内，利用自身做出的这这套自动化对已有的起始启动应用所做的提升的真实使用体验汇报。

## 提交方式要求 (SUBMISSION INSTRUCTIONS)

1. 确保已把全部完成修改的文件变更皆 PUSH 推送递交至你用作打分的远程仓库节点上。
2. **确保您已将 brentju 和 febielin 添加为您该作业代码库仓库站点的共同协作审阅人。**
3. 务必经由 Gradescope 提供最终的上交申请。
