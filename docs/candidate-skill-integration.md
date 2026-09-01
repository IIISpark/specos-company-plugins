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
| OpenAI `build-web-data-visualization` | package `0.1.21` / cache revision `1e285826` | plugin manifest：MIT | 新增技术栈中立的 `ispark-data-visualization` 与 `ispark-architecture-diagrams`；将 React/Next 集成和 TypeScript 契约合入现有 owner，不复制 18 个 specialist、宿主协议或固定 D3/CDN 方案。 |
| OpenAI bundled `visualize` | package `1.0.23` | plugin manifest：Proprietary | 仅用于划清会话内互动可视化的宿主边界；不复制正文、fragment/CSP 协议、样式变量或运行时。 |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | `a218edadbc3361672f5e5e2cd72a8212b0b3fbb8` | 根 `LICENSE`：MIT | 暂缓。未来 community-research skill 必须使用已授权工具并显式记录来源/日期覆盖，不导入 cookie、账号或 source-adapter 运行时。 |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | `773a52944ba4747a18bd4ae9ade53fff041adcbc` | 根 `LICENSE`：MIT | 暂缓整套导入。证据账本和实验协议以后可进入学术 owner；不采用自治循环、cron 和无许可持续执行。 |

## 最终归属

- `ispark-dev-workflow`：工程 spec、domain/module design、TDD、最小代码、新鲜完成证据，以及按需加载的 TypeScript visualization 数据/renderer 契约。
- `ispark-debugging`：症状复现、跨边界追踪、竞争假设和已验证的根因修复。
- `ispark-review-risk`：审计上下文、findings-first diff review、安全/契约和有边界的行为保持简化。
- `ispark-agent-tools`：skill 合并决策，以及并行 Agent ownership 与复核规则。
- `ispark-codebase-understanding`：大型陌生代码库的 read-first 映射。
- `ispark-react-performance`：React/Next 实现性能、组件 API 与按需加载的 visualization 集成边界；视觉设计与渲染验收仍由独立 owner 负责。
- `ispark-data-visualization`：数据与证据可视化的分析语义、编码、renderer、交互状态、验证与导出；不接管通用 UI 设计、浏览器验收或框架性能。
- `ispark-architecture-diagrams`：UML、C4、ERD、BPMN、sequence/state、依赖图和软件架构图的建模语义、source/model、布局、交互、验证与导出；不替代架构或 schema 决策。
- `ispark-tmeet`：腾讯会议 CLI 的认证、会议、录制、报告、通讯录受限解析、会中控制和排障反馈；不与 `ispark-lark` 合并。

## 加载边界

专业 skill 在路由前只暴露名称和可区分的 description；短入口在选中后只加载当前决策所需的
最窄 reference，任务跨越边界时才追加第二个。现有 owner 的新增方法也都位于 references，
因此普通任务不会无条件加载 TDD、audit-context、subagent、React、TypeScript visualization、
data visualization 或 architecture diagram 细节。
所有 discovery description 统一控制在 280 字符内，并保留正向触发词、相邻 owner 的负向边界和 fallback。
这些专业 skill 均允许 implicit invocation，fallback profiles 则继续按岗位收窄。

## 细节吸收校正

后续维护不得把“选择性吸收”误读成只保留标题。已纳入的细节包括：

- skill 规则本身的 RED/GREEN/REFACTOR 压力测试和 rationalization 记录；
- 中文高频对照、递进、因果和总结骨架的上下文审查；
- 领域模型变更时的 glossary、具体场景和 ADR 触发条件；
- diff review 的相邻实现、variant/edge 追踪和失败可见性；
- React 性能与 Web guideline 可用性/状态审查的职责分离。
- AGENTS.md/CLAUDE.md 的单一事实源、精简注入和 exact command/path 校验。
- 学术研究的证据账本、实验协议、baseline、版本和来源追踪；不引入自治循环或定时任务。

仍然不导入外部仓库的自治运行时、issue tracker、dashboard 宿主或状态后端、token、词表和检测器。

## 腾讯会议 Skill 吸收

`tmeet-skill` 的功能面与安全约束在 2026-08-30 重新整理为独立的 `ispark-tmeet`：入口只保留
触发条件、模块路由和跨模块门槛，命令细节拆到 `references/`。保留会议查询的 list/search 分流、
服务端游标分页、录制权限 `prepare -> 用户确认 -> commit`、通讯录只服务邀请/呼叫、踢人目标
必须来自参会人报告、异步导出轮询、脱敏反馈和所有高风险写操作二次确认。

没有吸收自动安装 `@tencentcloud/tmeet@latest`、自动写入 agent/model 环境变量、后台 OAuth、
原始 token/内部 ID 回显或将通讯录作为通用人员查询接口的做法。具体 CLI 参数以本机 `tmeet --help`
和对应子命令 help 为准，避免固定版本说明漂移。

## Notion CLI Skill 吸收

本机 `ntn 0.22.8` 安装中发现 OpenClaw 的 `notion` skill（OpenClaw 为 MIT）；它覆盖 Notion
页面、数据库、块和 API，但采用直接 token、原始 curl 与固定 API 版本的写法。2026-08-31 将其
任务边界重写为独立的 `ispark-notion`，不复制上游正文，不引入 token、环境变量、硬编码版本或
原始 API 响应的处理规则。

入口按认证、页面、数据源、文件、原始 API 和 workspace 级命令拆分，只有选中的分支读取对应参考。
保留窄范围读取、游标继续须经用户请求、歧义对象不得代选，以及创建、编辑、归档、上传、logout 和
任意 API 写入都需紧邻执行时二次确认的约束。`ntn auth token` 被明确禁止；`ntn login`、`ntn update`
和 Notion-as-code/worker 写入不因缺失前置条件而自动执行。

## Apifox 官方 Skill 吸收

官方仓库 `apifox/apifox-cli-skills` 在提交 `8a98f5f17b80689d3b11ce18e8cfda80e1e86f57` 提供 8 个
skill：CLI 总入口、checkup、branch、import/export、test-case、test-scenario、test-automation 和
API lifecycle。仓库当前未包含 LICENSE 文件，且 `apifox-cli` npm 包标记为 `UNLICENSED`，因此没有复制
上游正文或把它作为可再分发依赖；仅根据官方公开内容独立重写方法。

它们已合并为单一 `ispark-apifox`：官方的 `--help`/schema/agentHints 事实优先、项目/分支一致性、
AI 分支 pick-to、导入前 OpenAPI 质量指标、空壳 case/scenario 防护、本地/云端报告区分、测试清理、
分支合并门禁，以及现有 APIFox skill 的契约、Mock、共享模型和导出回读规则都保留在按需 references。
安装、更新、登录、token、导入、写入、运行、报告上传、分支和合并均不会因 skill 被选中而自动执行。

## Visualization Skill 吸收

OpenAI curated `build-web-data-visualization` 0.1.21 的 plugin manifest 声明 MIT。审查时该包包含
18 个 specialist、138 个 Markdown、约 688KB 内容；直接分发会扩大 discovery 竞争和维护面。
本仓库没有发布这 18 个 specialist：数据与证据语义收敛为一个 `ispark-data-visualization` 入口和
七个按需 reference；软件/系统图收敛为一个 `ispark-architecture-diagrams` 入口和四个按需
reference；其中高密度 Canvas/WebGL renderer 作为 data owner 的第七个按需 reference；React/Next
集成与 TypeScript 工程契约分别进入现有 owner。全部按 ISpark 的 owner、
artifact、stop rule 和验证契约独立重写。

纳入的方法包括：先定义 analytical question、受众、数据形态、claim 和证据账本；先审查单位、
分母、尺度、聚合、missing data 与 uncertainty，再选择视觉编码；根据 mark 密度、更新频率、
交互、可访问性、维护和导出来选择声明式图表、科学静态绘图、SVG/D3、Canvas、WebGL、地图或
diagram renderer；显式设计 loading/stale/empty/error、selection、shareable state、移动端、键盘、
触控、reduced-motion 和 static fallback；实时 dashboard 还要求 first scan、稳定主指标位置、
chart-adjacent key、移动端证据优先；对支持重放/增量且缺口影响准确性的 stream 才要求 resumable cursor、gap
repair 和源契约支持的 snapshot-plus-delta 或 replay window，full snapshot/polling 则采用版本化完整替换与
stale/partial 处理，并在 `live -> reconnecting -> repairing -> live` 的恢复门禁通过前保持 stale/unavailable；最后分层
验证数据契约、浏览器渲染和导出。所有 degradation ladder 都带进入/退出阈值、hysteresis 和恢复路径。

本次补上原 Web-focused 包较弱的科学绘图路径，包括 Matplotlib、Seaborn、Altair、ggplot2 等
静态或可复现方案，但它们同样只是条件分支。fallback 只覆盖常态进行可视化设计、实现或研究的
`dramawork`、`engineer`、`frontend`、`ops`、`product` 和 `research`；`backend` 与
`agent-maintainer` 仍可在完整 plugin 中按需发现。`ops` 加入 fallback 是为了覆盖运维 dashboard 的默认工作面，
不改变完整 plugin 的索引优先加载模型。

架构图 owner 保留一问一图、一层 abstraction、稳定 source ID、explicit/inferred 区分、normalized
model、format/interchange 损失、tree/layered/force/radial layout、routing/crossing/overlap/stability、
explorer state、accessibility、round-trip 和 export 方法。它加入除 `research` 外的 fallback profiles；
research 仍可在完整 plugin 中按需发现，不把工程图方法预装为科研默认。
可编辑 explorer 额外区分 semantic edit 与 layout hint，要求 stable source ID、typed port、提交前校验、
undo/redo、dirty/save 和显式版本冲突；shareable state 只允许紧凑非敏感 allowlist 字段。

React 补充只处理 React 与 renderer 的 ownership、窄 Client Component、hydration、dynamic import、
lifecycle cleanup 和 per-instance/page-level cost。TypeScript 补充只处理 runtime validation、
normalized semantic model、derived marks、renderer adapter、view-state codec 和 deterministic transform；
React 路由保留 server-only secret/authorization、最小可序列化 client payload 与项目 cache/dedup 语义；
TypeScript 边界还检查 finite number 和行/节点/边/字符串/嵌套预算。两者都不会重新决定可视化或架构图语义。

高级 scrollytelling、地图、图和 Gantt 模式还必须把 entry/exit condition、minimum dwell 或 hysteresis、
fallback、保留不变量、资源预算和 deterministic fixture 写成可执行验收；阈值不能只存在于描述性文案。

没有吸收 18 个 specialist 全文、固定 D3 版本或 CDN、
Codex fragment/CSP 宿主协议、固定 React/Next/GSAP 版本或专用 API recipe、出版物风格模板或概念图审批工作流、厂商 Gantt 字段或任何
项目专用路径。bundled `visualize` 1.0.23 为 Proprietary，只作为宿主能力边界参考，没有复制或
再分发；company skill 在它不可用时仍可独立完成分析和实现指导。
