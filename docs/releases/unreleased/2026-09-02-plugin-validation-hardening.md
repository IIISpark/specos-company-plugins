---
type: fix
scope: plugin
audience: developer
summary: 修复 skill frontmatter 的分发阻断并强化 snapshot 与 payload 隐私门禁。
breaking: false
demo_ready: false
tests:
  - "python -m unittest discover -s tools/tests -p 'test_*.py' -v"
  - "python tools/prepare_publish.py"
  - "python -X utf8 <codex-skill-root>/skill-creator/scripts/quick_validate.py <all source and snapshot skills>"
  - "git diff --check"
artifacts:
  - "skills/*/SKILL.md"
  - "plugins/ispark-company/skills/"
  - "tools/validate.py"
  - "tools/tests/test_validate.py"
  - "docs/releases/unreleased/2026-09-02-plugin-validation-hardening.md"
---

# What changed

修复 `ispark-apifox`、`ispark-notion`、`ispark-tmeet` 和 `ispark-react-performance` description 中未引用
冒号造成的 YAML frontmatter 解析错误，并从 source 重新生成 marketplace snapshot。仓库 validator 现在会
解析 frontmatter、检查必需字符串字段和允许的键；在没有 PyYAML 时保留保守的无依赖语法 fallback。

payload 隐私门禁改为扫描所有可分发的 UTF-8 文本文件，而不是依赖有限的扩展名列表；二进制资源仍跳过。
分享视图引用的 skill 规则补充了不可猜测、按用户/租户限定、短时有效、可撤销、逐次授权和 Referer/日志/缓存/分析
泄漏控制。6 个历史上过长的 discovery description 也被压缩到统一的 280 字符预算，详细规则继续留在
按需 reference；数据可视化发布说明同步反映 `ops` fallback profile。

# Why it matters

入口 frontmatter 是宿主发现和加载 skill 的前置契约。之前的正则门禁会把四个不可解析的入口误判为有效，导致
source 与已安装 snapshot 同时出现“看起来存在、实际不可加载”的分发风险。新的 parser gate、统一入口预算、全量 snapshot
重建和全量 quick validation 将这类问题前移到发布前。

# Demo posture / limitations

本条只记录 source、生成 snapshot、验证器、测试和发布说明；发布与本机安装状态以对应 tag、GitHub Release
和安装回读为准。本轮没有执行任何外部 API、浏览器或生产系统操作。隐私扫描是已知模式门禁，不是对任意产品名、设备标识或二进制 metadata
的完整保密证明；发布前仍需人工审查 staged diff 和公开 maintainer metadata。
