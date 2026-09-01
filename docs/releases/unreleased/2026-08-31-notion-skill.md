---
type: feature
scope: plugin
audience: developer
summary: 新增按需路由的 Notion ntn CLI skill，并收紧认证、读取与写入边界。
breaking: false
demo_ready: false
tests: python tools/prepare_publish.py; python -m unittest discover -s tools/tests -p 'test_*.py' -v
artifacts: skills/ispark-notion; profiles; plugins/ispark-company/skills/ispark-notion
---

## What changed

新增 `ispark-notion`，将 Notion CLI 工作按认证、页面、数据源、文件、原始 API 和 workspace 级命令
拆为按需加载的参考文件，并同步加入全部 fallback profile。

## Why it matters

Agent 能从任务意图自动选择 Notion 工作流，却不会为其他任务加载命令细节。读取范围保持收窄，写操作
在实际执行前仍需明确确认，且不会暴露凭证、原始内部标识或完整私有响应。

## Demo posture / limitations

本次不代表已经登录、读取或修改任何 Notion workspace，也不代表已发布或安装新的插件版本。CLI 参数以
实际环境中的 `ntn --help` 为准。
