---
type: feature
scope: plugin
audience: developer
summary: 将腾讯会议 tmeet CLI 以独立按需加载 skill 纳入 SpecOS。
breaking: false
demo_ready: false
tests:
  - "python -m unittest discover -s tools/tests -p 'test_*.py' -v"
  - "python tools/prepare_publish.py"
  - "git diff --check"
artifacts:
  - "skills/ispark-tmeet/"
  - "plugins/ispark-company/skills/ispark-tmeet/"
  - "profiles/*.yml"
  - "docs/candidate-skill-integration.md"
---

# What changed

新增 `ispark-tmeet`，将腾讯会议 CLI 的认证、会议、录制、报告、通讯录、会中控制和排障反馈按
操作拆分为按需 reference。入口保持短小并允许 implicit invocation；高风险写操作、隐私字段、
分页、录制权限申请和通讯录用途边界均保留。

# Why it matters

腾讯会议能力不会与 Feishu/Lark 或通用人员检索混路由。未唤醒时只增加一条轻量 skill 描述，
选中后才加载对应模块细节；不自动安装 CLI、不自动登录、不回显 token 或内部会议标识。

# Demo posture / limitations

本轮完成 maintainer source、marketplace snapshot、fallback profile 和结构回归测试；未执行任何
腾讯会议 API、登录、邀请、会议变更、录制下载或日志上传。CLI 参数以本机实际 `tmeet --help`
为准；本条目不代表腾讯会议账号已授权或任何会议动作已完成。
