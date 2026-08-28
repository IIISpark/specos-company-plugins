# Anti-AI-Slop 吸收方案

## 决策

本轮采用“共同质量底线 + 领域 owner”的结构，不把所有输出交给一个巨型 humanizer：

1. `ispark-anti-slop` 负责识别任务目的、具体性、事实保真和证据置信度，并把请求路由到正确的领域 skill。
2. `ispark-writing` 负责普通读者向 prose 的生成前约束、生成后审计、genre/register 和可选 voice profile。
3. `ispark-academic-writing` 独立负责论文体裁，保护 citation、公式、变量、术语、段落功能和 claim strength。
4. `ispark-product-design` 负责反模板视觉判断；`ispark-browser-qa` 仍是浏览器验收 owner。
5. `ispark-dev-workflow` 与 `ispark-review-risk` 负责代码的根因优先、最小 diff 和过度防御分支审查。

加载策略采用 single-domain short circuit：意图明确时直接加载 owner；只有混合、歧义或跨域审计才读取 `ispark-anti-slop` 的 routing reference，并把本次决策限制在最多两个 owner skill。description 同时写明相邻领域的负向边界，避免写作/视觉、实现/review 双重命中。

“少 AI 味”在这里指减少可观察的泛化、模板化和过度平滑，不指作者识别、检测器规避或故意制造人类错误。

## 来源核对

以下是 2026-08-27 读取的公开仓库入口和 `main` 分支提交。只吸收方法论，不把外部仓库作为运行时依赖，也不把其未核验的统计或效果声明当作公司事实。

| 来源 | 提交 | 许可/处理 | 吸收内容 |
|---|---|---|---|
| [Shirhussain/humanize](https://github.com/Shirhussain/humanize) | `454179265115bea6c2eeb96e6b4191fa8873c4b1` | MIT | 生成前约束、register、引用保护、voice profile、生成后自审 |
| [thekozugroup/humanizer](https://github.com/thekozugroup/humanizer) | `e01b919b776c7df8740e29baebbc394efb772e6e` | MIT | pattern density 和“检测信号不是判决”的思路；不引入 Rust detector |
| [isatimur/de-slop](https://github.com/isatimur/de-slop) | `4349a8af4116d6f02b38d62f4b19e66108c4aada` | MIT | `rewordable`/`hollow` 分流、有限次 self-check、空洞内容不编造 |
| [wdkang123/stop-slop-zh](https://github.com/wdkang123/stop-slop-zh) | `41f853dada499954cf353551cd1e375c0a6ea950` | MIT | 中文八股、名词化、假深度、体裁门控和误报边界 |
| [y10reo/stop-slop-zh](https://github.com/y10reo/stop-slop-zh) | `62896a15200874bb809c52eb3f46bdc856d71d1d` | MIT | 中文场景分类、证据边界和低分时重写的启发；不采用固定分数门槛 |
| [henmuc/codex-academic-humanizer](https://github.com/henmuc/codex-academic-humanizer) | `496d5d897d920d1c8f0d382e31406eeff0f29e45` | MIT | 独立学术入口、修订强度、术语表、citation/notation closure |
| [funboy322/avoid-ai-design](https://github.com/funboy322/avoid-ai-design) | `8337060636a8cf12e32e883eb367becd702aa526` | MIT | source/render 证据分级、P0/P1/P2、单一设计方向和 surgical/rebuild 深度 |
| [AnswerDotAI/skill-plugins](https://github.com/AnswerDotAI/skill-plugins) | `18be134dd175bd6240d2f7c5f21f08282cc80c54` | Apache-2.0 | “写任何面向人的 prose 前先加载规则”的 discovery 触发思想 |
| [aravelo7/codex-agent-skills](https://github.com/aravelo7/codex-agent-skills) | `33ee2ef7236a6fda5bc4df2c6002f505e243c0aa` | 本轮未发现 LICENSE；只吸收公开可观察的最小改动/失败可见性概念，不复制文本 |
| [ch040602/anti-ai-slop](https://github.com/ch040602/anti-ai-slop) | `171db9c7daa0e4507cd22f5ad4e8771343f79e72` | 本轮未发现 LICENSE；只吸收跨域目的/具体性/设计质量三问，不复制文本 |

`hardikpandya/stop-slop`、`blader/humanizer` 和 `ashgreat/humanizer` 作为重叠候选保留在审计记录中；本轮没有足够的边界收益把它们再变成独立入口。外部项目的 star 数、检测分数和“更像人”的营销性表述不作为验收依据。

2026-08-28 重新核对中文清单后，将总分总、排比三件套、空泛开头、抽象主语、解释升格、
商务/报告黑话、伪口语、标题腔和金句收尾整理到
`ispark-writing/references/chinese-ai-patterns.md`。该文件只在明确的中文去 AI 味任务中加载；
命中词句本身不构成问题，必须结合局部密度、语义贡献、关系真实性、体裁和作者声音判断。
硬禁标点、固定句长波动、固定命中次数，以及强行添加观点、数字或口头禅的做法没有吸收。

## 不吸收的内容

- 不 vendor 外部仓库的脚本、Rust/Node/Python 运行时、词表或主题目录。
- 不使用统一的 banned-word list；术语、正式表达、列表、字体、渐变和防御分支必须按上下文判断。
- 不用固定句长、标点数量或模板命中次数模拟“人味”；密度只用于定位复查，不是自动失败门槛。
- 不输出“AI 概率”“人类分数”或绕过检测器的承诺。
- 不把用户的私人写作样本、`sttot-voice` 或其他个人画像写进公司插件；voice profile 只能在用户授权的项目本地维护。
- 不让风格层改变公共 API、数据库 schema、认证权限、学术结果、引用范围、产品状态或 UI 行为。

## 验收口径

- 直接说“去 AI 味”时，能发现并路由到 `ispark-anti-slop`，再进入领域 owner。
- 普通 prose 有生成前质量底线、生成后审计和空洞段落 flag；已经足够好的段落不被强行改写。
- 学术文本能保留引用、公式、变量、术语、数字、条件和段落功能，并把不确定项留给作者确认。
- UI 审计能区分代码事实和像素观察，改动前有明确方向，完成后有真实浏览器证据。
- 代码审查能解释每个新增 fallback、retry、default、compat 或 wrapper 的依据，并保持失败可见。
- source skills 与生成的 `plugins/ispark-company/skills/` snapshot 字节一致；本轮只完成本地 draft，不代表已推送、全员安装或 GA。
