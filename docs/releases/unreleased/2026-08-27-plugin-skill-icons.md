---
type: fix
scope: plugin
audience: developer
summary: 为全部已发布 skill 补齐可验证的图标元数据和图标资产。
breaking: false
demo_ready: false
tests:
  - "python -m unittest discover -s tools/tests -p 'test_*.py' -v"
  - "python tools/prepare_publish.py"
  - "git diff --check"
artifacts:
  - "skills/*/agents/openai.yaml"
  - "skills/ispark-academic-writing/assets/icon.svg"
  - "skills/ispark-anti-slop/assets/icon.svg"
  - "skills/ispark-hiring/assets/icon.svg"
  - "skills/ispark-writing/assets/icon.svg"
  - "tools/validate.py"
---

# What changed

为先前缺失图标的 `ispark-academic-writing`、`ispark-anti-slop`、
`ispark-hiring` 和 `ispark-writing` 增加 `icon_small`、`icon_large`、品牌色与
独立 SVG 图标。发布校验现在要求每个已发布 source skill 都同时声明并提供两个图标
资产，防止未来新 skill 在市场界面中退化为无标识条目。

# Why it matters

图标让技能在插件选择器中更易扫描和区分；校验将这一要求从人工检查变成发布门禁，
确保 source 与生成 snapshot 的展示元数据保持一致。

# Demo posture / limitations

本条目随 `0.3.5+codex.20260827` 发布。图标只影响插件展示，不改变 skill 的触发条件、
内容、执行权限或下游项目行为。
