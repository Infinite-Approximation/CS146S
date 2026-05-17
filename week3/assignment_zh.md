# 第 3 周 — 构建自定义 MCP 服务器

设计并实现一个模型上下文协议 (MCP) 服务器，以封装真实的外部 API。你可以：

- **本地**运行它（STDIO 传输）并与 MCP 客户端（如 Claude Desktop）进行集成。
- 或者**远程**运行它（HTTP 传输）并通过模型代理或客户端直接调用。这难度较大，但会获得额外加分。

如果添加符合 MCP 授权规范的身份验证机制（API 密钥或 OAuth2），将会获得额外的加分。

## 学习目标

- 理解 MCP 的核心功能：工具 (Tools)、资源 (Resources) 和 提示词 (Prompts)。
- 实现包含带类型参数与健壮错误处理机制的工具定义。
- 遵循日志记录和通讯传输的最佳实践（对于 STDIO 服务器，不可向 stdout 输出任何日志信息）。
- （可选）为 HTTP 传输实现授权验证流程。

## 任务要求

1. 选择一个外部 API，并记录你将使用的接口端点 (endpoints)。例子包括：天气预报、GitHub Issues、Notion 页面、电影/电视数据库、日历、任务管理器、金融/加密货币、旅行、体育比赛数据等。
2. 对外暴露至少两个 MCP 工具 (tools)。
3. 实现基本的容错与容灾机制：
   - 优雅地处理 HTTP 请求失败、超时异常和空数据结果。
   - 尊重并遵守 API 的速率限制 (Rate limits)（例如：实现简单的失败退避策略，或抛出面向用户的警告提示）。
4. 打包与文档准备：
   - 提供清晰的环境设置说明、所需环境变量列表以及运行命令。
   - 包含一份示例调用流程说明（例如：用户在客户端中应输入/点击什么内容来触发这些 MCP 工具）。
5. 选择一种部署运行模式：
   - 本地：运行 STDIO 服务器，可在你的本机运行，并能被 Claude Desktop 或各种 AI IDE（例如 Cursor）发现并对接。
   - 远程：可通过网络访问的 HTTP 服务器，能够由支持 MCP 协议的本地/云端客户端及代理运行时调用。若真实部署了该应用并允许外部网络访问，将获得加分。
6. （可选）额外加分项：身份验证 (Authentication)
   - 通过读取环境变量及客户端侧配置来实现 API 密钥身份验证机制；或者
   - 针对 HTTP 传输方式实现 OAuth2 风格的 Bearer Token，并在请求过程校验 Token 受众，保证严禁向未经授权的上游 API 透传 Token。

## 交付物

- 将源代码保存在 `week3/` 目录下（建议路径为 `week3/server/`，且包含清晰的应用程序入口，如 `main.py` 或 `app.py`）。
- 提交 `week3/README.md`，至少包含：
  - 前置条件、环境设置说明以及项目运行指引（本地环境和/或远程环境均可）。
  - 有关如何配置 MCP 客户端（以调用本地接口的 Claude Desktop 为例）或配置代理服务以调用远程接口的说明。
  - 工具接口文档参考：包括名称、参数、示例输入/输出内容和预期执行行为。

## 评分标准（共计 90 分）

- 功能性 (35分): 至少实现 2 个工具，正确实现了 API 的集成方案，具有合理的返回输出。
- 可靠性 (20分): 包含严谨的输入参数验证、异常捕获错误处理、日志记录方案及遵守 API 调用的速率限制。
- 开发者体验 (20分): 具备清晰的安装配置说明和开发文档，允许轻松在本地启动运行；且项目的目录结构合理有序。
- 代码质量 (15分): 代码具备优秀的可读性，变量/函数命名遵循“见名知意”原则，避免无效嵌套复杂度，以及在适用位置提供了相关类型提示 (type hints)。
- 额外加分项 (计 10 分):
  - +5分：能够通过 OpenAI/Claude SDK 此类代理客户端调用远程暴露的 HTTP MCP 服务器。
  - +5分：正确构建了安全鉴权控制（API 请求前完成鉴权动作或通过了带有鉴权审计性质的 OAuth2 验证）。

## 推荐的参考资料

- MCP 服务器快速入门指引：[modelcontextprotocol.io/quickstart/server](https://modelcontextprotocol.io/quickstart/server)
  _注：严禁直接提交此示例项目作为作业糊弄了事。_
- MCP 对 HTTP 请求鉴权指南：[modelcontextprotocol.io/specification/2025-06-18/basic/authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)
- 在 Cloudflare 上挂载实现远程 MCP 服务器的指引 (Agents)：[developers.cloudflare.com/agents/guides/remote-mcp-server/](https://developers.cloudflare.com/agents/guides/remote-mcp-server/)。在应用发布部署前，你可以利用 MCP 官方 inspector 验证工具进行本地环境调试。
- 部署至 Vercel: [https://vercel.com/docs/mcp/deploy-mcp-servers-to-vercel](https://vercel.com/docs/mcp/deploy-mcp-servers-to-vercel) 如果你选择实践远程 MCP 服务器的拓展项，Vercel 会是一个包含免费套餐配额的极佳之选。
