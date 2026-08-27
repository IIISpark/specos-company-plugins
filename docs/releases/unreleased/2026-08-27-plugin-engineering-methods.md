---
type: feature
scope: plugin
audience: developer
summary: 选择性吸收外部工程方法，并新增陌生代码库理解与 React/Next 性能两个窄触发 skill。
breaking: false
demo_ready: false
tests:
  - "python -m unittest discover -s tools/tests -p 'test_*.py' -v"
  - "python tools/prepare_publish.py"
  - "python tools/sync_profile.py --action dry-run --profile engineer"
  - "python tools/sync_profile.py --action dry-run --profile frontend"
  - "git diff --check"
artifacts:
  - "skills/ispark-codebase-understanding/"
  - "skills/ispark-react-performance/"
  - "skills/ispark-dev-workflow/"
  - "skills/ispark-debugging/"
  - "skills/ispark-review-risk/"
  - "skills/ispark-agent-tools/"
  - "profiles/"
  - "docs/candidate-skill-integration.md"
  - "tools/tests/test_validate.py"
  - "plugins/ispark-company/"
---

# What changed

工程方法没有被拆成一组相互竞争的通用 skill。需求转 spec、domain/module design、TDD 和完成前验证进入 `ispark-dev-workflow`；跨边界根因追踪进入 `ispark-debugging`；audit-context 与 diff-scoped simplification 进入 `ispark-review-risk`；并行 Agent 的 ownership、隔离和独立复核进入 `ispark-agent-tools`。

新增 `ispark-codebase-understanding`，用于大型陌生代码库的 read-first scout；新增 `ispark-react-performance`，用于 React/Next.js waterfall、bundle、server/client boundary、rerender 和 component API。两者均启用 implicit invocation，但通过正向触发、负向边界、单一按需 reference 和 role-scoped fallback profile 控制上下文。

外部来源、pinned commit、许可和拒绝项记录在 `docs/candidate-skill-integration.md`。插件没有复制候选仓库脚本、知识图谱、dashboard、cookie/source adapter、自治循环或 CC BY-SA 文本。

# Why it matters

规划、测试、调试、审查和验证本来就是现有工程 owner 的职责，继续新增同义 skill 会放大路由竞争。把方法放回 owner reference 可以在任务命中后按需加载，同时为两个原先缺失且可明确识别的任务建立独立入口。

这让另一个 Agent 可以从自然语言任务自动发现能力，又不会让普通代码编辑同时加载大型代码库分析、React 性能和安全审计上下文。

# Demo posture / limitations

本轮完成 maintainer source、fallback profiles、测试、文档和生成 snapshot；draft 版本提升为 `0.3.3+codex.20260827`。没有安装、推送、发布、部署、新增第三方依赖或运行外部候选代码。配置和路由测试证明 skill 可被隐式发现且边界被声明，但不等于所有自然语言表述的真实选择准确率已经统计验证；发布或本机重装后仍需在新会话做真实 discovery 观察。React 性能结论仍需要同条件 baseline/build/browser evidence，代码库 scout 也不把自动生成图谱当成事实源。
