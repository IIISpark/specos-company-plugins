---
type: fix
scope: plugin
audience: developer
summary: 补齐外部 skill 方法的中文模板审查、行为压力测试、领域模型、安全 diff、React guideline 与研究证据细节。
breaking: false
demo_ready: false
tests:
  - "python -m unittest discover -s tools/tests -p 'test_*.py' -v"
  - "python tools/prepare_publish.py"
  - "codex exec --ephemeral --sandbox read-only (Chinese compound-pattern pressure scenario)"
  - "git diff --check"
artifacts:
  - "CLAUDE.md"
  - "skills/ispark-writing/references/chinese-writing.md"
  - "skills/ispark-writing/references/chinese-ai-patterns.md"
  - "skills/ispark-dev-workflow/references/testing.md"
  - "skills/ispark-agent-tools/references/skill-testing.md"
  - "skills/ispark-dev-workflow/references/architecture.md"
  - "skills/ispark-review-risk/references/code-review.md"
  - "skills/ispark-react-performance/references/react-performance.md"
  - "skills/ispark-academic-writing/references/academic-method.md"
---

# What changed

补充中文高频对照、递进、因果和总结骨架的上下文审查，明确“不是……而是……”等句式
不是禁词；新增仅在明确去 AI 味请求时加载的中文模式簇，覆盖总分总、三件套、抽象主语、
商务黑话、伪口语、报告腔和金句收尾，并以局部密度、语义贡献、体裁和误伤例外决定是否改写；
增加 skill 规则的 RED/GREEN/REFACTOR 压力测试 reference；补充领域 glossary、
具体场景与 ADR 触发条件；扩展安全 diff/variant/攻击面审查；补充 React bundle、监听器、
长列表和 Web guideline 状态检查；为学术写作加入来源、数据集、协议、baseline 和结果
追踪字段；增加 AGENTS.md/CLAUDE.md 单一事实源维护规则。

# Why it matters

这些约束把此前只保留在摘要层的方法细节变成可路由、可检查、可复核的 owner guidance，
同时维持按需加载，不引入外部仓库的自治 runtime、账号或检测器。

# Demo posture / limitations

本轮发布版本为 `0.3.6+codex.20260828`。已完成 source/snapshot 校验、23 项回归测试和
中文复合模板压力复测；本条目不代表任何业务服务部署或生产环境变更。
