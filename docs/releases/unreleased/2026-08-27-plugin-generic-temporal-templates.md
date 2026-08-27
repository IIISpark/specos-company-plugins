---
type: fix
scope: plugin
audience: developer
summary: 将 Temporal worker 模板与审查规则中的项目绑定名称、路径和协议前缀收紧为通用占位符。
breaking: false
demo_ready: false
tests:
  - "python -m unittest discover -s tools/tests -p 'test_*.py' -v"
  - "python tools/prepare_publish.py"
  - "git diff --check"
artifacts:
  - "skills/ispark-temporalization/"
  - "skills/ispark-agent-tools/references/distribution.md"
  - "tools/tests/test_validate.py"
  - "plugins/ispark-company/"
---

# What changed

`ispark-temporalization` 不再包含具体下游项目名、Kubernetes namespace、label domain、
环境变量前缀、Provider Gateway header 前缀、idempotency prefix、私有索引地址、
监控服务地址或项目专用 activity workspace 路径。模板和规则改用
`your-namespace`、`your-org.io`、`<idempotency-prefix>`、`<private-index-host>`、
`<monitoring-namespace>` 与 `<project>` 等占位符。

保留了原有工程语义：算法与业务数据库边界、临时工作目录必须受管、progress event
长度约束、create-only idempotency、审计/诊断 header 分类，以及不把局部路径作为
公共 workflow/package 契约。

新增 source-skill 回归测试，禁止恢复这些已移除的项目绑定标记。

# Why it matters

公司插件应提供可复用的方法和安全边界，而不是把一个下游项目的部署拓扑和协议命名
传播到其他仓库。占位符让 agent 知道需要什么类型的配置或契约，同时要求它从目标
仓库的事实源取得真实名称和地址。

# Demo posture / limitations

本条变更随 `0.3.5+codex.20260827` 发布。没有部署或迁移既有下游项目。已有的
`dramawork` fallback profile 名称和历史 release/documentation 仍保留在 skill 树外，
它们不是本次“skill 内容去项目绑定”的改动对象；若要重命名 profile，需要单独评估
直接安装用户的兼容性。
