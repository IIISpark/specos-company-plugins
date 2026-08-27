---
type: feature
scope: plugin
audience: developer
summary: 将去模板化质量门按普通写作、学术撰写、网页设计和代码审查分层纳入公司插件。
breaking: false
demo_ready: false
tests:
  - "python tools/prepare_publish.py"
  - "python -m unittest discover -s tools/tests -p 'test_*.py' -v"
  - "python -X utf8 C:/Users/nmg_w/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/ispark-anti-slop"
  - "python -X utf8 C:/Users/nmg_w/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/ispark-academic-writing"
  - "python tools/sync_profile.py --action dry-run --profile research"
  - "git diff --check"
artifacts:
  - "skills/ispark-anti-slop/"
  - "skills/ispark-academic-writing/"
  - "skills/ispark-writing/"
  - "skills/ispark-product-design/"
  - "skills/ispark-dev-workflow/"
  - "skills/ispark-review-risk/"
  - "profiles/research.yml"
  - "docs/anti-ai-slop-integration.md"
  - "plugins/ispark-company/"
---

# What changed

新增 `ispark-anti-slop` 作为显式“去 AI 味”请求的跨域路由入口，并新增 `ispark-academic-writing` 保护论文中的 citation、公式、变量、术语、段落功能、限定条件和 claim strength。普通写作补充了生成前质量底线、生成后审计、体裁判断、`rewordable` / `hollow` 分流、最多三轮聚焦自审和可选的项目本地 voice profile。

前端设计规则增加 source/render/inference 证据区分、P0/P1/P2 审计、单一设计方向和 surgical/rebuild 深度选择；工程与风险审查规则要求新增 fallback、retry、default、compat 或 wrapper 时给出调用路径、契约或失败证据，同时保留真正需要的安全、兼容和故障恢复边界。

新增 `research` direct-install fallback profile；学术 skill 不再注入无关岗位 profile。插件 draft 版本提升为 `0.3.1+codex.20260827`，生成 snapshot 包含 14 个公司 skill。

# Why it matters

一个通用 humanizer 容易把学术限定条件、UI 状态、代码失败语义和普通文风混为一谈。本轮把共同底线限制为目的、具体性、事实保真、克制和证据，再由各领域 owner 决定可改内容与验收方式，因此能减少模板化输出而不牺牲公共契约、可访问性、安全检查或研究证据。

外部项目只提供经提交与许可核对的方法启发；插件不引入 detector、词表、主题包或第三方运行时，也不把 pattern hit 当作作者判断。来源和 non-vendoring 边界见 `docs/anti-ai-slop-integration.md`。

# Demo posture / limitations

本轮完成 maintainer source、生成 snapshot、profiles、文档和本地验证；本机 local marketplace 当前指向该 source 并由 `codex plugin list` 报告 installed/enabled，但没有推送或团队发布，旧的同名缓存未被直接修改。现有运行中的 Codex 会话不会自动加载这份 draft；发布或本机重装后仍需新开会话验证 discovery。该能力不承诺绕过 AI detector，也不会在没有授权样本时生成或持久化个人 voice profile；真实网页验收仍需要浏览器渲染证据，学术事实仍以原始论文和项目证据协议为准。
