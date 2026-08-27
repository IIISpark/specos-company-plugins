# 候选 Skill 吸收记录

本文记录 2026-08-27 工程方法增强所依据的来源审查。公司插件只选择性吸收方法，
不打包候选仓库、外部运行时代码或其自治执行假设。

## 决策规则

- 已有 skill 拥有相同触发条件和结果责任时，将方法合入现有 owner。
- 只有当任务可重复、职责独立且发现边界明确时，才新增 skill。
- 如果采用会带入凭证、依赖、持久状态、宽泛自治行为或不兼容的许可义务，
  则只保留为研究来源。

所有落地说明都按 ISpark 自身的授权、stop rule、artifact 和验证契约重新编写。
外部仓库是上游参考，不是插件运行时依赖。

## 固定版本审查

| 仓库 | 审查提交 | 许可证据 | ISpark 决定 |
| --- | --- | --- | --- |
| [obra/superpowers](https://github.com/obra/superpowers) | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | 根 `LICENSE`：MIT | 将 TDD、系统化调试、完成前验证和有边界的并行 Agent 方法合入现有 owner；拒绝所有回复前强制分发和无条件流程规则。 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` | 根 `LICENSE`：MIT | 将需求转 spec、domain glossary、module interface 和任务拆解方法合入 `ispark-dev-workflow`；不默认采用依赖 issue tracker 的 Wayfinder。 |
| [Lum1104/Understand-Anything](https://github.com/Lum1104/Understand-Anything) | `ba450c43425f3de6d43daf76526950ad8ca93536` | 根 `LICENSE`：MIT | 新增精简的 `ispark-codebase-understanding` scout；排除 dashboard、token、持久知识图谱、分析器运行时和生成状态。 |
| [trailofbits/skills](https://github.com/trailofbits/skills) | `5eb104e1c5255fe6dad1cdb74a3866113bb311b5` | 根 `LICENSE`：CC BY-SA 4.0 | 为 `ispark-review-risk` 独立重写 audit-context 方法；不复制上游文字、资源、agent 或 workflow。 |
| [getsentry/skills](https://github.com/getsentry/skills) | `c2f99a5b04b4cd992ec3022d7c2c3e23e938d241` | 根 `LICENSE`：Apache-2.0 | 将行为保持、diff 范围内简化和精简 agent instruction 原则合入已有 owner；不新增 skill。 |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | `dd089a8c752c966dee8bf0f27cb625ba193ffd9e` | React skill frontmatter：MIT | 新增 `ispark-react-performance`，只组合有优先级的 React/Next 性能和 composition 决策；不打包其规则全集或构建包。 |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | `a218edadbc3361672f5e5e2cd72a8212b0b3fbb8` | 根 `LICENSE`：MIT | 暂缓。未来 community-research skill 必须使用已授权工具并显式记录来源/日期覆盖，不导入 cookie、账号或 source-adapter 运行时。 |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | `773a52944ba4747a18bd4ae9ade53fff041adcbc` | 根 `LICENSE`：MIT | 暂缓整套导入。证据账本和实验协议以后可进入学术 owner；不采用自治循环、cron 和无许可持续执行。 |

## 最终归属

- `ispark-dev-workflow`：工程 spec、domain/module design、TDD、最小代码和新鲜完成证据。
- `ispark-debugging`：症状复现、跨边界追踪、竞争假设和已验证的根因修复。
- `ispark-review-risk`：审计上下文、findings-first diff review、安全/契约和有边界的行为保持简化。
- `ispark-agent-tools`：skill 合并决策，以及并行 Agent ownership 与复核规则。
- `ispark-codebase-understanding`：大型陌生代码库的 read-first 映射。
- `ispark-react-performance`：React/Next 实现性能和组件 API；视觉设计与渲染验收仍由独立 owner 负责。

## 加载边界

两个新 skill 在路由前只暴露名称和可区分的 description；短入口在选中后各自只加载
一个 reference。现有 owner 的新增方法也都位于 references，因此普通任务不会无条件加载
TDD、audit-context、subagent 或 React 细节。两个新 skill 均允许 implicit invocation，
fallback profiles 则继续按岗位收窄。
