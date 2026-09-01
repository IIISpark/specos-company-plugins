---
type: feature
scope: plugin
audience: developer
summary: 新增按需路由的 Apifox CLI/MCP skill，吸收官方 CLI skill 的契约、测试、导入导出和分支规则。
breaking: false
demo_ready: false
tests: python tools/prepare_publish.py; python -m unittest discover -s tools/tests -p 'test_*.py' -v
artifacts: skills/ispark-apifox; profiles; plugins/ispark-company/skills/ispark-apifox
---

## What changed

新增 `ispark-apifox`，将官方 8 个 Apifox CLI skill 的可复用方法和现有 APIFox 文档治理能力合并为一个
短入口及 9 个按需参考文件，并同步到全部 fallback profile。

## Why it matters

Agent 能自动识别 Apifox 任务，同时只加载当前契约、导入导出、测试、自动化或分支所需的细节。官方的
schema/帮助优先、回读验证、AI 分支隔离、报告边界和导入质量门禁得到保留，写操作不会被隐式执行。

## Demo posture / limitations

本次不代表已安装或登录 Apifox CLI，也不代表访问、导入、运行或修改任何 Apifox 项目。官方仓库当前无
LICENSE 文件，skill 文本为基于公开规则的独立重写；CLI 参数始终以实际环境的 `apifox --help` 为准。
