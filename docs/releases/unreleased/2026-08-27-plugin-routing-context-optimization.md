---
type: fix
scope: plugin
audience: developer
summary: 优化 skill 自动路由的短路规则和领域负向边界，减少无关上下文加载。
breaking: false
demo_ready: false
tests:
  - "python tools/prepare_publish.py"
  - "python -m unittest discover -s tools/tests -p 'test_*.py' -v"
  - "python -X utf8 C:/Users/nmg_w/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/ispark-anti-slop"
  - "git diff --check"
artifacts:
  - "skills/ispark-anti-slop/"
  - "skills/ispark-writing/SKILL.md"
  - "skills/ispark-product-design/SKILL.md"
  - "skills/ispark-dev-workflow/SKILL.md"
  - "skills/ispark-review-risk/SKILL.md"
  - "skills/ispark-anti-slop/references/routing.md"
  - "tools/tests/test_validate.py"
---

# What changed

跨域 `ispark-anti-slop` 新增 single-domain short circuit：单一领域任务直接交给 owner，不再加载跨域 routing reference 或第二个领域 skill；混合任务限制为当前决策所需的最多两个 owner。写作、产品设计、工程实现和风险审查的 description 也补上互斥边界，减少相邻 skill 竞争。

路由 reference 新增 loading order 和 negative boundaries，并用测试锁定短路和 owner 分工。

# Why it matters

隐式调用的成本不只在是否命中，还在命中后加载了多少无关规则。短路和负向边界把“发现入口”和“继续加载上下文”分开，保留自动调用能力，同时减少普通写作、UI 文案、代码实现和 review 任务之间的上下文串扰。

# Demo posture / limitations

本轮是本地 source/snapshot 的路由优化，插件 draft 版本为 `0.3.2+codex.20260827`，不代表模型在所有自然语言中的选择准确率已被统计证明；当前 `codex plugin list` 仍登记已安装版本 `0.3.1`，需要显式重装后才会刷新安装登记，再用新会话观察真实 discovery。没有新增运行时 detector、外部依赖、公共 API 或团队发布动作。
