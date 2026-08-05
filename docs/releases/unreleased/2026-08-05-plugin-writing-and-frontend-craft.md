---
type: feature
scope: plugin
audience: developer
summary: 新增公司级写作能力，并把 Hallmark 的反默认模式方法分别纳入写作与前端设计边界。
breaking: false
demo_ready: false
tests:
  - "python -m unittest discover -s tools/tests -p 'test_*.py' -v"
  - "python tools/validate.py"
  - "python tools/prepare_publish.py"
  - "git diff --check"
artifacts:
  - "skills/ispark-writing/"
  - "skills/*/agents/openai.yaml"
  - "skills/ispark-product-design/references/frontend-craft.md"
  - "profiles/*.yml"
  - "plugins/ispark-company/skills/"
  - "tools/build_plugin_snapshot.py"
  - "tools/validate.py"
  - "tools/tests/test_validate.py"
  - "README.md"
---

# What changed

新增 `ispark-writing`，提供 draft、rewrite、audit、adapt 四种模式，并按需加载事实保真、写作反模式、中文写作、文体适配和 Hallmark 归属说明。`ispark-docs-issues`、`ispark-product-design`、`ispark-lark` 和 `ispark-release-ops` 只增加职责路由，不复制写作规则；全部 fallback profiles 均可安装新 skill。

`ispark-product-design` 新增前端 craft reference，用于反模板设计、只读视觉审计、受边界约束的 redesign 和截图/URL design study。Hallmark 基线固定为 `0a0f706bc0289fef76a07fb854a6a5b031c57901`，MIT notice 随两个派生 skill 的 plugin snapshot 分发。

全部 12 个公司 skill 现在显式允许 implicit invocation。`tools/validate.py` 同时校验 skill 直接引用、调用策略，以及 source 和 plugin snapshot 的相对路径与字节内容；回归测试覆盖同名 skill 的陈旧 snapshot、缺失/多余文件和构建忽略项。

# Why it matters

公司此前有文档结构、产品设计、协作和发布 skill，但缺少跨文体的 prose-quality 事实源。新增入口把“怎么写”与“事实由谁拥有、文档放哪里、动作由谁执行”分开，并把去 AI 默认模式定义为具体性、证据边界和读者适配，而不是统一文风或检测规避。

显式 invocation policy 和内容级 snapshot 校验把“可被自动发现”与“实际分发的是当前源码”分别变成可审查、可回归的仓库契约，避免依赖平台默认值或只比较 skill 名称。

# Demo posture / limitations

本轮会推送 `0.2.0+codex.20260805` 并完成 maintainer 本机安装验证，但不代表已经向所有成员完成升级、公开发布或 GA。该 skill 不是 AI 文本检测器，不通过故意添加错误或口语噪声模拟人类写作，也不会自动同步 Hallmark 上游。前端方法不包含 Hallmark 主题目录、`.hallmark/` 状态、源码 stamp 或特定工具假设。
