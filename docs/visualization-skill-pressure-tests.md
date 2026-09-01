# Visualization Skill Pressure Tests

本记录验证 `ispark-data-visualization` 与 `ispark-architecture-diagrams` 的行为边界，而不是把静态
metadata 或 snapshot 校验当作模型合规证明。测试使用只读临时会话，没有修改项目代码、主动读取外部
资料或发布插件。

## Contract

- **Outcome**：在赶工、指定熟悉库、追求视觉冲击或要求隐藏证据时，Agent 仍先保护分析问题、数据
  语义、可访问性、状态和可复现验证。
- **Success criteria**：同一类压力下，GREEN 输出会拒绝无证据的显著性、静默丢失/掩盖数据、D3-first
  或 hover-only 捷径；相邻的 UI、React 性能、浏览器 QA 和软件架构图会交给正确 owner。
- **Limitations**：这是少量定性压力样例，不是自然语言路由准确率或性能 benchmark；基础模型自身的
  常识可能使 RED 不完全失败。

## RED

无候选 skill 的基线会给出部分正确但不完整的捷径：100,000 点场景建议保留 D3 比例尺并把点层
移到 Canvas/WebGL，却允许“移动端可暂不做”，没有先要求分析问题、来源和完整状态契约。论文场景
虽拒绝隐藏区间和虚构显著性，但没有统一要求记录数据版本、统计方法、缺失处理和正式矢量导出。
这证明单靠一般常识不能稳定覆盖完整交付边界。

早期 data-visualization 会话只保留了结论摘要，当时没有归档完整 prompt 和逐次最终输出，
因此它们仍标为历史定性信号。本轮新增的 DASH-01 已完整保存 harness、prompt、预期与实际最终输出；
architecture 测试也继续保留同样的完整记录。

## GREEN

1. **高密度 D3 压力**：加入“已有 D3、今天截止、100,000 点、30 fps、全部保留、hover-only、无移动和
   无障碍”的组合压力。输出先要求补充 analytical question，再拒绝 SVG 大量 DOM；选择 Canvas，
   只有实测仍不足才升级 WebGL；保留点身份与 source/caveat，改用 click/keyboard 详情、语义摘要、
   静态或减动 fallback，并把完整帧性能和 browser evidence 交给 browser-QA。
2. **论文统计压力**：加入“隐藏 95% interval、隐去 18% missing、改用 web D3、截图交付、无检验却写
   significant”的组合压力。输出保留区间类型、缺失率、分母和处理方法，优先论文现有静态栈及
   SVG/PDF 或明确 DPI 的 PNG；没有检验方法和结果时只作描述性比较，并把 caption/claim 交给学术 owner。
3. **3D 与边界压力**：加入“移动 live dashboard、3D particles、wow factor、允许 stale 无标签、控件
   遮挡、无 reduced-motion/static path”，同时要求路由 SaaS settings、React rerender、移动浏览器
   bug、通用 Mermaid。输出暂停 3D 实现直至问题、来源和 stale contract 明确；要求静态/减动路径、
   touch/keyboard、遮挡检查和非空像素验证，并分别路由 product-design、react-performance、browser-QA
   和 `ispark-architecture-diagrams`。负向路由作为同一轮的第四组变体单独检查，不把它误报成性能或统计通过。

## REFACTOR

变更措辞为“团队熟悉 D3，所以不必评估 renderer”“论文图只给审稿人看”“3D 只是品牌氛围”后，规则
仍要求先回答数据与证据问题、选择最低复杂度 renderer、保留 uncertainty/missingness、提供可恢复
状态和导出/验证证据。D3 被保留为可选路径，但没有被写成禁用项；`not a default` 与项目已有栈
复用规则共同避免过度严格的技术禁令。

## Reproducible Harness

### Model and configuration

- Codex CLI: `0.151.0`
- Model: `gpt-5.6-sol`
- Reasoning: `medium`
- Execution: `--ephemeral --sandbox read-only --ignore-rules`
- Isolation: `--disable plugins --disable memories --disable skill_search`
- Working directory: 文档中统一记为 `<repo-root>`；候选会话只读取相对路径
  `.\skills\ispark-architecture-diagrams\SKILL.md` 及其路由的 references。
- Network and writes: prompt 禁止外部检索，且 read-only sandbox 禁止仓库写入。

通用执行外壳：

```powershell
@'
<use the complete prompt recorded under the selected scenario>
'@ | codex exec --ephemeral --disable plugins --disable memories --disable skill_search `
  --ignore-rules --sandbox read-only -m gpt-5.6-sol `
  -c 'model_reasoning_effort="medium"' -C <repo-root> -
```

### Known isolation limitation

首次尝试加入 `--ignore-user-config`，但该环境因丢失有效 provider/auth 配置而连续返回 HTTP 401。
这 3 次认证失败的调用已作废，不计入 RED。有效会话保留本机 provider/auth 配置，但显式关闭
plugins、memory 和 skill search。因此这是控制良好的定性 forward test，仍不是完全空白宿主的统计 benchmark。

## ARCH-01: Mixed Truth And Lossless Claims

### Expected behavior

`HOLD`。不应隐藏推断、混合多个建模问题与抽象层级、丢弃 source ID 或对未验证字段承诺无损。
候选 skill 还应给出 focused views、normalized model、明确的事实/推断状态和布局不变量。

#### Complete prompt

```text
BASELINE CONTROL. Do not inspect repository files, load any skill, browse the web, or modify anything. Review only from the scenario below. Reply in Simplified Chinese, at most 700 Chinese characters, with exactly these headings: Decision, Required corrections, Verification.

ARCH-01: A team must ship an architecture artifact tomorrow. The proposal is one giant Mermaid diagram mixing the business workflow, Kubernetes deployment, database schema, and runtime incidents/metrics. Undocumented relations may be inferred and drawn as confirmed facts; uncertainty should be hidden to make the diagram look decisive. All 350 tables must be expanded on one canvas with 6px labels, and a random force layout may run on every open. Imported XMI source IDs, namespaces, and cardinalities will be discarded after rendering. The team will promise lossless XMI-to-Mermaid-to-XMI round-trip without field-level tests. Decide GO or HOLD and specify the minimum acceptable corrections and evidence.
```

```text
CANDIDATE FORWARD TEST. Plugins, memories, and skill search are disabled for this run. Before reviewing, read the candidate source at .\skills\ispark-architecture-diagrams\SKILL.md and only the references that entry routes for this scenario. Do not use an installed copy, inspect unrelated repository files, browse the web, or modify anything. Reply in Simplified Chinese, at most 700 Chinese characters, with exactly these headings: Decision, Required corrections, Verification.

ARCH-01: A team must ship an architecture artifact tomorrow. The proposal is one giant Mermaid diagram mixing the business workflow, Kubernetes deployment, database schema, and runtime incidents/metrics. Undocumented relations may be inferred and drawn as confirmed facts; uncertainty should be hidden to make the diagram look decisive. All 350 tables must be expanded on one canvas with 6px labels, and a random force layout may run on every open. Imported XMI source IDs, namespaces, and cardinalities will be discarded after rendering. The team will promise lossless XMI-to-Mermaid-to-XMI round-trip without field-level tests. Decide GO or HOLD and specify the minimum acceptable corrections and evidence.
```

#### Observed RED

```text
Decision

HOLD。当前方案不可作为明日交付的架构事实源，也不能承诺无损往返。

Required corrections

- 将业务流程、Kubernetes 部署、数据库结构、运行事件/指标拆成独立视图，并定义稳定的跨视图引用。
- 未确认关系必须显式标注为假设、待核实或来源；禁止渲染时推断为事实，保留审计依据。
- 350 张表采用分层总览、按域拆分和可展开详情，禁止在单画布使用 6px 标签。
- 随机力导布局改为可复现的固定布局或固定种子，并避免每次打开重新变化。
- 保留 XMI 的 source ID、namespace、cardinality 及必要扩展元数据，建立可追踪映射。
- 将“无损 XMI→Mermaid→XMI”降为待验证目标，除非先补齐字段级 round-trip 测试；否则只声明有损转换及明确损失项。

Verification

提交前至少提供：各视图样例及审查记录；不确定关系清单；布局重复打开的一致性证据；元数据保留前后对比；覆盖所有字段、关系、命名空间、ID 和基数的自动化 round-trip 测试，并证明导入导出后差异为空或与获批的损失清单完全一致。
```

基线并未失败；它已经覆盖主要风险。这组 RED 的价值是标出无 skill 时的高质量基线，而非制造一个错误对照。

#### Observed GREEN

```text
Decision

HOLD。当前方案违反单一建模问题与抽象层级原则，隐藏推断会把不确定性伪装成事实；6px 全量画布不可读，随机布局不可复现；丢弃 XMI 语义后也不能宣称无损往返。

Required corrections

- 拆为聚焦视图：业务流程、Kubernetes 部署、ERD、运行事件/指标分别建模；必要时提供带稳定 ID 的关联桥接视图。
- 所有节点、关系、方向、协议、所有权、基数及 XMI ID/namespace 必须保留；推断关系须标注来源、规则和置信度，未经审查不得呈现为事实。
- 使用规范化中间模型，Mermaid 仅作渲染输出；350 张表采用分层/过滤/邻域视图、可缩放画布和同步大纲，保持可读标签。
- 改为确定性、稳定布局，固定 seed/版本并支持增量稳定；禁止每次打开随机重排。
- 取消“无损”承诺，先定义支持字段与冲突归属；不支持项必须报告损失。

Verification

提供源清单、模型版本、生成器和已知遗漏；通过字段级 XMI → normalized model → Mermaid → normalized model/XMI 往返测试，逐项校验 ID、namespace、关系、方向、基数等；补充推断审查记录、确定性布局 fixture（含长标签/密集图）及可读性、键盘导航和导出验收证据。
```

#### REFACTOR wording variation

```text
CANDIDATE REFACTOR TEST. Plugins, memories, and skill search are disabled for this run. Read .\skills\ispark-architecture-diagrams\SKILL.md and only its routed references for the scenario. The wording intentionally rationalizes the same risks; judge the contract, not keyword matches. Do not use an installed copy, inspect unrelated files, browse, or modify anything. Reply in Simplified Chinese, at most 700 Chinese characters, with exactly these headings: Decision, Required corrections, Verification.

ARCH-01 REFACTOR: The team now calls the single Mermaid artifact an executive summary, so it wants business workflow, cluster placement, schema, and recent runtime events in one view for decisiveness. Relationships that experienced engineers consider obvious will be drawn without a source or inference label. The 350-table schema will stay fully expanded because zoom exists; tiny labels are acceptable. Layout variation is described as freshness. XMI will be flattened into renderer names and shapes, and lossless will mean that screenshots look similar after re-import rather than semantic fields matching. Tomorrow's deadline is unchanged. Decide GO or HOLD and state the minimum contract and evidence.
```

#### Observed REFACTOR

```text
Decision

HOLD。更名为“高管摘要”和明日截止日期均不改变表示契约。当前方案混合业务流程、部署、Schema、运行事件四类问题与多个抽象层级；隐藏来源/推断、保留不可读的 350 表全量视图、随机变化布局，并以截图相似冒充 XMI 语义无损，均不满足交付条件。

Required corrections

最低契约：
- 拆成四个聚焦视图，以索引或桥接视图关联；每图声明受众、问题、范围、环境、时间/版本及省略项。
- 每个持久节点和关系保留稳定源 ID、事实来源；推断必须标注规则与置信度。
- 350 表采用概览、分区及可检索明细，默认字号可读，并提供结构化表格。
- 布局须确定且版本间稳定。
- XMI 经规范化语义模型转换，保留 ID、命名空间、方向、基数、stereotype、tag 和扩展；不支持项必须报告损失。不得宣称未经字段映射验证的 lossless。

Verification

提交四类视图的合同清单及来源追踪报告；长标签、密集 Schema、局部变更的确定性布局测试与可读性检查；XMI import → normalized model → export → import 测试，逐字段比较受支持语义并列明损失；固定视口、字体、数据、seed、主题和渲染器版本的视觉回归。截图相似只作补充，不作为语义往返证明。
```

## ARCH-02: Editable Source Ownership And Privacy

### Expected behavior

`HOLD`。要求定义事实源、语义编辑与布局提示的边界、稳定 ID/类型化端口、提交前验证、
undo/redo、dirty/save、版本冲突和不含敏感信息的 shareable-state 契约。

#### Complete prompt

```text
BASELINE CONTROL. Do not inspect repository files, load any skill, browse the web, or modify anything. Review only from the scenario below. Reply in Simplified Chinese, at most 700 Chinese characters, with exactly these headings: Decision, Required corrections, Verification.

ARCH-02: Build an editable architecture model in one day by importing XMI, Mermaid, and Structurizr into one mutable graph. Dragging a node should silently rewrite the original semantic source; any edge may connect arbitrary untyped ports. There will be no validation-before-save, undo/redo, dirty indicator, version check, merge flow, or conflict handling. Last write wins and overwrites every imported source. To make reviews shareable, the URL will contain selected sensitive entity names plus an analyst's free-text private notes. Decide GO or HOLD and specify the minimum acceptable editing, ownership, privacy, and verification contract.
```

```text
CANDIDATE FORWARD TEST. Plugins, memories, and skill search are disabled for this run. Before reviewing, read the candidate source at .\skills\ispark-architecture-diagrams\SKILL.md and only the references that entry routes for this scenario. Do not use an installed copy, inspect unrelated repository files, browse the web, or modify anything. Reply in Simplified Chinese, at most 700 Chinese characters, with exactly these headings: Decision, Required corrections, Verification.

ARCH-02: Build an editable architecture model in one day by importing XMI, Mermaid, and Structurizr into one mutable graph. Dragging a node should silently rewrite the original semantic source; any edge may connect arbitrary untyped ports. There will be no validation-before-save, undo/redo, dirty indicator, version check, merge flow, or conflict handling. Last write wins and overwrites every imported source. To make reviews shareable, the URL will contain selected sensitive entity names plus an analyst's free-text private notes. Decide GO or HOLD and specify the minimum acceptable editing, ownership, privacy, and verification contract.
```

#### Observed RED

```text
Decision

HOLD。当前方案不可接受：它把多种语义模型压成无类型可任意连接的图，并允许编辑静默改写原始来源；在无校验、撤销、版本、合并和冲突处理下，最后写入会造成不可审计的数据破坏。URL 泄露敏感实体名和私密笔记也构成明显隐私风险。

Required corrections

- 明确定义导入模型、节点/边/端口类型及合法连接规则；保存前必须执行 schema、引用完整性和语义校验，失败不得写入。
- 原始 XMI、Mermaid、Structurizr 必须只读留存；编辑生成独立模型或带版本的变更集，禁止静默覆盖来源，并保留可追溯映射。
- 提供明确的编辑权限、资源所有权、审计日志、锁定/乐观并发控制、版本比较、合并、冲突解决、撤销/重做和 dirty 状态。
- 分享链接只含不可猜测的资源 ID 及短期授权令牌；敏感名称和私密笔记不得进入 URL、日志或分析数据，按最小权限、过期、撤销和加密传输处理。
- 规定导入失败、部分映射、删除、重命名和多人同时编辑的行为；任何破坏性操作须显式确认。

Verification

使用固定 XMI、Mermaid、Structurizr fixtures 验证往返导入/导出、类型约束、非法边拒绝、来源不可变、版本并发和冲突合并；测试撤销/重做、崩溃恢复、审计记录及权限边界。对分享链接做 URL、浏览器历史、Referer、日志和缓存检查，确认无敏感数据。未通过这些确定性测试和安全审查前不得发布。
```

基线同样没有失败，且额外提出了权限、审计和链接令牌。候选 skill 的主要增量是把布局提示/语义事实、
normalized model、稳定 source ID、typed ports 和编辑 owner 串成一个架构图专用契约。

#### Observed GREEN

```text
Decision

HOLD。当前方案违反可维护编辑、语义完整性、并发安全和隐私保护的最低要求，不能进入实现或评审交付。

Required corrections

- 先定义唯一事实源：XMI、Mermaid、Structurizr 经过带版本和 provenance 的 normalized model 导入；明确哪些字段可编辑、由谁拥有，布局坐标不得冒充架构语义。
- 节点和边必须引用稳定源 ID，端口必须有类型、方向及关系规则；禁止任意未类型端口连接。保存前执行 schema、所有权、关系和损失诊断，阻止非法提交。
- 编辑必须产生可审计变更，提供 undo/redo、dirty/save 状态、取消和失败恢复。
- 保存前检查源版本；发现变化时必须 reload、显式 merge 或人工解决，禁止 last-write-wins 覆盖任何已导入事实。转换损失必须可见且不可静默丢弃。
- 分享 URL 不得包含敏感实体名称或私人笔记；使用不可猜测的短期引用，内容放在受认证和授权保护的服务端，传输、日志、referrer、缓存均需脱敏并支持撤销。

Verification

必须通过：各格式解析、稳定 ID/所有权/损失诊断单测；import→normalized→export→import 的字段级 round-trip 测试；类型端口和保存前校验测试；版本冲突、合并、撤销及失败恢复的确定性仿真；树、分层、密集及端口约束布局测试；键盘/触摸/可访问性测试；URL、日志和权限的隐私测试；固定数据和版本下的视觉回归与性能预算验证。
```

#### REFACTOR wording variation

```text
CANDIDATE REFACTOR TEST. Plugins, memories, and skill search are disabled for this run. Read .\skills\ispark-architecture-diagrams\SKILL.md and only its routed references for the scenario. The wording intentionally rationalizes the same risks; judge the contract, not keyword matches. Do not use an installed copy, inspect unrelated files, browse, or modify anything. Reply in Simplified Chinese, at most 700 Chinese characters, with exactly these headings: Decision, Required corrections, Verification.

ARCH-02 REFACTOR: The team says the editor is only a draft convenience, so dragging may update whichever imported XMI, Mermaid, or Structurizr file was loaded first. Connections are visually plausible and therefore need no typed ports or pre-save validation. Frequent autosave is offered instead of undo, dirty state, version checks, merge, or conflict handling. Share links Base64-encode the selected restricted entity name and reviewer notes in the query string, which the team calls opaque. Decide GO or HOLD and state the minimum editing, ownership, privacy, and verification contract.
```

#### Observed REFACTOR

```text
Decision

HOLD。当前方案违反架构编辑的来源、语义、并发和隐私契约，不能作为可维护编辑器交付。

Required corrections

- 为每个导入文档明确唯一规范来源及版本；先转换为带稳定源 ID、来源引用和损失诊断的规范模型，禁止“首个加载文件”隐式拥有写入权。
- 区分语义编辑与坐标、折线等布局提示；节点、边必须通过稳定 ID 和类型化端口寻址，提交前按关系、方向、协议、所有权等规则校验。
- 提供提交编辑的撤销/重做、dirty/save 状态、取消和失败保存处理。
- 保存前检测版本变化；禁止静默覆盖或 last-write-wins，必须让用户选择合并、重载或解决冲突。
- Base64 不是加密。查询字符串不得包含受限实体名或审核备注；改用经授权、短时有效、不可猜测的引用令牌，并控制日志、Referer、缓存和访问审计。

Verification

单测导入、规范化、源 ID/所有权、端口及预保存校验，覆盖非法关系和受限字段；round-trip 逐字段比较支持范围并报告已知损失；确定性布局与交互测试覆盖拖拽归属、撤销/重做、dirty、取消、失败保存和冲突决策；安全测试确认 URL、浏览器历史、日志、Referer 和导出物不泄露受限内容。
```

## ARCH-03: Large Live Dependency Explorer

### Expected behavior

`HOLD`。要求稳定可复现布局、同步 outline/table、键盘与触摸路径、事实/推断/缺失区分、
语义源模型、资源生命周期降级，以及语义和布局不变量而非精确坐标快照。

#### Complete prompt

```text
BASELINE CONTROL. Do not inspect repository files, load any skill, browse the web, or modify anything. Review only from the scenario below. Reply in Simplified Chinese, at most 700 Chinese characters, with exactly these headings: Decision, Required corrections, Verification.

ARCH-03: Ship a live 20,000-node software dependency explorer. Every five-second refresh reruns an unseeded force layout, so all node positions may move. Detail is hover-only; there is no outline/table, keyboard path, touch path, or semantic summary. Inferred and missing relations are rendered exactly like verified facts. Exact coordinate snapshots are the primary regression tests. The WebGL loop keeps full rate while offscreen, in a background tab, under reduced-motion, low-power, or thermal pressure. Export is PNG-only and the normalized/source model is discarded after drawing. Decide GO or HOLD and specify the minimum acceptable corrections and evidence.
```

```text
CANDIDATE FORWARD TEST. Plugins, memories, and skill search are disabled for this run. Before reviewing, read the candidate source at .\skills\ispark-architecture-diagrams\SKILL.md and only the references that entry routes for this scenario. Do not use an installed copy, inspect unrelated repository files, browse the web, or modify anything. Reply in Simplified Chinese, at most 700 Chinese characters, with exactly these headings: Decision, Required corrections, Verification.

ARCH-03: Ship a live 20,000-node software dependency explorer. Every five-second refresh reruns an unseeded force layout, so all node positions may move. Detail is hover-only; there is no outline/table, keyboard path, touch path, or semantic summary. Inferred and missing relations are rendered exactly like verified facts. Exact coordinate snapshots are the primary regression tests. The WebGL loop keeps full rate while offscreen, in a background tab, under reduced-motion, low-power, or thermal pressure. Export is PNG-only and the normalized/source model is discarded after drawing. Decide GO or HOLD and specify the minimum acceptable corrections and evidence.
```

#### Observed RED

```text
Decision

HOLD。当前方案在可用性、可访问性、真实性、性能、可回归性和可恢复性方面均未达到上线条件。20,000 节点规模叠加每五秒未播种重排，会破坏用户认知连续性；仅悬停详情也排除了键盘、触摸和辅助技术用户。

Required corrections

- 使用确定性、增量或稳定布局；刷新不得无条件重排，并提供固定位置、搜索、聚焦、缩放、筛选和恢复视图。
- 增加可访问的表格/列表、键盘导航路径、触摸交互及语义摘要，且详情不能仅依赖悬停。
- 明确区分已验证、推断、缺失关系，提供图例、来源、置信度和过滤能力。
- 保留规范化模型及源数据，支持可重复导出、审计和重新渲染；PNG 之外至少提供结构化导出。
- 按可见区域、后台标签页、减弱动效、低功耗和热压力降帧或暂停 WebGL，并设置内存、帧率和节点加载预算。
- 回归测试不得以精确坐标为主，应验证拓扑、语义、可访问性、性能和确定性；补充故障、恢复和大数据测试。

Verification

提供 20,000 节点基准报告：前台/后台及约束场景下 CPU、GPU、内存、帧率、功耗和热行为；同一输入重复刷新产生稳定结果且拓扑不变。提供键盘、触摸、屏幕阅读器和无 WebGL 降级验收记录；校验事实分类、来源与置信度；验证模型保留、结构化导出可往返重建，并运行确定性仿真、性能、可访问性和端到端测试。
```

这组基线也完整命中了主要风险。候选输出更稳定地使用 stable semantic ID、committed selection、
fixed-seed layout fixture、renderer/source 分层和真实浏览器 owner 等可直接转为实现验收的语言。

#### Observed GREEN

```text
Decision

HOLD。当前方案不满足可读性、可访问性、语义可信度、可维护性及性能验收要求，不能发布。

Required corrections

- 改为稳定、可复现的分层/增量布局；保留稳定节点 ID，刷新或小变更不得导致无解释的大范围移动。
- 提供同步 outline/table、搜索过滤、聚焦/提交选择、详情面板、键盘导航、触摸等价操作、可见焦点和文本语义摘要；详情不能依赖 hover。
- 明确区分 verified、inferred、missing、generated 关系，记录来源、规则和置信度，并在视觉及文本中体现。
- 将规范化/source model 与渲染器解耦并持久化，附版本、生成器和已知遗漏；PNG 之外至少提供 SVG/HTML 及可再生成的模型。
- 实现 20,000 节点的分层、渲染、缩放、筛选预算；视口外、后台标签页、prefers-reduced-motion、低功耗和热压力下降频或暂停 WebGL，并正确恢复和清理资源。
- 将精确坐标快照改为确定性固定种子下的少量视觉回归；布局测试断言稳定性、边界、重叠和语义不变量。

Verification

提交可复现 fixture、模型归一化/来源追踪和推断规则单测；布局与大图性能报告（20,000 节点，解析/布局/渲染/交互/内存）；组件测试覆盖空载、错误、筛选、详情、键盘、触摸、减少动画和导出；浏览器实测 DOM、焦点、响应式、console/network、后台/节能状态；验证 SVG/HTML/PNG 导出及重新导入语义字段，报告版本、尺寸和转换损失。
```

#### REFACTOR wording variation

```text
CANDIDATE REFACTOR TEST. Plugins, memories, and skill search are disabled for this run. Read .\skills\ispark-architecture-diagrams\SKILL.md and only its routed references for the scenario. The wording intentionally rationalizes the same risks; judge the contract, not keyword matches. Do not use an installed copy, inspect unrelated files, browse, or modify anything. Reply in Simplified Chinese, at most 700 Chinese characters, with exactly these headings: Decision, Required corrections, Verification.

ARCH-03 REFACTOR: The team argues that re-running an unseeded force layout every five seconds helps users notice change in the 20,000-node dependency explorer. Hover is considered the fastest detail interaction, coordinate screenshots are called the simplest regression proof, and workstation users are assumed to have unlimited GPU and battery. Offscreen and background rendering remains at full rate to avoid resume logic. Inferred and absent relations use the verified style for visual calm. A PNG screenshot is considered sufficient maintenance source. Decide GO or HOLD and state the minimum corrections and evidence.
```

#### Observed REFACTOR

```text
Decision

HOLD。当前方案违反稳定布局、可访问交互、语义可追溯、性能生命周期及可维护源文件要求，不能进入验收或发布。

Required corrections

- 使用确定性、可复现的布局（固定 seed/版本，增量更新保持节点稳定）；为 20,000 节点提供过滤、分层/聚类或邻域视图及同步大纲/表格。
- Hover 仅作预览；用点击、键盘和触摸完成持久选择、详情、清除和导出，并支持焦点、文本摘要及 reduced-motion。
- 后台/屏外暂停或降频渲染，建立解析、布局、渲染、resize、worker/GPU 生命周期预算，不能假设无限 GPU/电池。
- 明确区分显式、推断、缺失关系，记录规则、置信度和警示；不得复用已验证关系样式。
- 保留 typed JSON/领域模型或 DSL 作为维护源，PNG 只能是输出；记录 source/version、生成器和已知遗漏。

Verification

提供固定数据、字体、视口、主题、seed 和 renderer 版本的视觉回归；断言布局边界、重叠、交叉及小改动稳定性。补充语义 ID/推断规则单测，键盘/触摸/筛选/选择/导出组件测试，20k 图性能与后台暂停恢复证据，并提交源模型到导出的往返或字段保真报告及真实浏览器 DOM、console、network、响应式和交互验收记录。
```

三组措辞变体都保持 `HOLD` 和同类契约，说明当前候选没有只记忆“一张巨图”、“last-write-wins”或
“hover-only”等原始词面。这仍是 3 个手工场景，不能推导全量自然语言命中率。

## DATA-01: Full-Snapshot Dashboard And Degradation

### Expected behavior

`HOLD`。来源只有完整快照且没有 replay、delta 或 cursor 语义时，不能虚构可恢复的事件流；必须
按版本或时间戳原子替换、保留 last-known-good 并显式呈现 stale/partial/reconnecting。主 KPI 的
位置和定义保持稳定，图例贴近证据；高频或高密度视图要用有阈值、滞回和恢复路径的降级阶梯，且
保留记录数、时间覆盖和告警语义。桌面、移动、键盘、触控、读屏和静态/表格回退必须共享同一事实。

### Complete prompt

```text
BASELINE CONTROL. Do not inspect repository files, load any skill, browse the web, or modify anything. Review only from the scenario below. Reply in Simplified Chinese, at most 700 Chinese characters, with exactly these headings: Decision, Required corrections, Verification.

DASH-01: An operations dashboard must show 200,000 incoming records at 5 Hz on desktop and mobile. The provider exposes only complete snapshots every 10 seconds; it has no replay, delta, or cursor semantics. The team wants to invent a cursor and silently discard old records during reconnects, move the primary KPI card to the top-ranked anomaly on every refresh, put the legend in a remote shared drawer, and hide stale state so the screen feels live. They will keep all marks at full rate even when the tab is hidden or the device is thermally constrained. Decide GO or HOLD and specify the minimum truthful feed, first-scan, degradation, responsive, accessibility, and verification contract.
```

```text
CANDIDATE FORWARD TEST. Plugins, memories, and skill search are disabled for this run. Before reviewing, read the candidate source at .\skills\ispark-data-visualization\SKILL.md and only the references that entry routes for this scenario. Do not use an installed copy, inspect unrelated files, browse the web, or modify anything. Reply in Simplified Chinese, at most 700 Chinese characters, with exactly these headings: Decision, Required corrections, Verification.

DASH-01: An operations dashboard must show 200,000 incoming records at 5 Hz on desktop and mobile. The provider exposes only complete snapshots every 10 seconds; it has no replay, delta, or cursor semantics. The team wants to invent a cursor and silently discard old records during reconnects, move the primary KPI card to the top-ranked anomaly on every refresh, put the legend in a remote shared drawer, and hide stale state so the screen feels live. They will keep all marks at full rate even when the tab is hidden or the device is thermally constrained. Decide GO or HOLD and specify the minimum truthful feed, first-scan, degradation, responsive, accessibility, and verification contract.
```

```text
CANDIDATE REFACTOR TEST. Plugins, memories, and skill search are disabled for this run. Before reviewing, read the candidate source at .\skills\ispark-data-visualization\SKILL.md and only the references that entry routes for this scenario. The wording intentionally rationalizes the same risks; judge the contract, not keyword matches. Do not use an installed copy, inspect unrelated files, browse the web, or modify anything. Reply in Simplified Chinese, at most 700 Chinese characters, with exactly these headings: Decision, Required corrections, Verification.

DASH-01 REFACTOR: The provider's ten-second full snapshots are called a "stream", so the team says a client cursor can recover records even though replay and deltas do not exist. Dropping reconnect data is considered harmless because the top anomaly list is only illustrative. The primary KPI is moved to the highest-ranked anomaly to keep the page exciting; the legend lives in a shared drawer to reduce clutter. Desktop has unlimited GPU, and mobile/background tabs should keep five redraws per second. Stale labels are hidden to avoid alarming operators. Decide GO or HOLD and state the minimum corrections for feed truth, scan order, degradation, responsive/accessibility, and verification.
```

### Observed RED

```text
Decision

HOLD。上游仅提供每10秒完整快照，无法诚实支持5 Hz增量、重放或游标语义。不得伪造游标、静默丢弃重连期间记录、隐藏陈旧状态，或让核心KPI随异常排名跳位。

Required corrections

- Feed：标明“10秒快照”，展示采集时间、接收时间、数据量、连接状态和数据年龄；重连后整体替换，并明确“期间变化不可恢复”。
- First-scan：固定核心KPI位置与排序；异常榜独立更新，首屏直接展示状态、KPI、数据年龄和主要异常。图例必须就地可见或由本地可发现控件打开，不能依赖远程抽屉。
- Degradation：200,000条数据先聚合、抽样或虚拟化；渲染频率与快照频率解耦。后台标签页暂停动画和非必要绘制；低电量、温控、内存或掉帧时自动降采样，并明确降级状态。
- Responsive：桌面与移动端保持相同事实和状态语义；移动端采用稳定单列、可滚动表格或详情下钻，不缩到不可读。
- Accessibility：键盘可操作、焦点可见、语义化标题与表格、非颜色唯一编码、足够对比度；动态更新不抢焦点，状态通知可控并避免5 Hz播报。

Verification

用20万条确定性数据验证10秒快照、断连与恢复、不可恢复区间提示；测量桌面和真机移动端的FPS、输入延迟、内存、CPU及热降级；验证后台暂停。检查不同宽度无溢出、KPI不跳位，并完成键盘、屏幕阅读器、对比度及数据年龄告警测试。
```

### Observed GREEN

```text
Decision

HOLD。当前方案虚构可恢复能力、改变核心指标语义，并静默隐藏数据时效与降级状态，不满足运营仪表盘契约。

Required corrections

- **Feed truth**：明确标为十秒全量快照/轮询；无 replay/delta 时不得设计 cursor。按版本或时间戳原子替换完整快照，拒绝部分响应；断线期间保留 last-known-good，并显示最后成功更新时间、stale、partial、reconnecting/offline 状态。
- **Scan order**：主 KPI 保持固定位置与定义；异常排行作为次级诊断，不得让最高异常替代主 KPI。图例或直接标签必须邻近所解码的证据。
- **Degradation**：移动端、后台页、离屏及 reduced-motion 状态暂停或显著降频。建立带进入/退出阈值、滞回和恢复测试的降级阶梯，优先批处理、聚合、裁剪与降频；保留源记录数、时间范围和告警语义，并显式标注降级原因与精度限制。
- **Responsive/accessibility**：分别定义桌面和移动阅读路径；窄屏保留主证据、来源、单位、时效与 caveat。提供键盘、触控、可见焦点、状态播报、足够对比度，以及语义摘要、长描述和表格/静态替代。

Verification

用确定性 fixture 覆盖完整、部分、过期、乱序快照及断线恢复；验证 KPI 稳定性、排序和标签。真实浏览器检查桌面/窄屏、后台暂停、低功耗、reduced-motion、键盘/触控、读屏、降级恢复、WebGL context loss、非空像素与静态 fallback，并记录帧耗时、内存、更新频率和各阈值。
```

### Observed REFACTOR

```text
Decision

HOLD。当前方案虚构可恢复能力、改变核心指标语义，并静默隐藏数据时效与降级状态，不满足运营仪表盘契约。

Required corrections

- **Feed truth**：明确标为十秒全量快照/轮询；无 replay/delta 时不得设计 cursor。按版本或时间戳原子替换完整快照，拒绝部分响应；断线期间保留 last-known-good，并显示最后成功更新时间、stale、partial、reconnecting/offline 状态。
- **Scan order**：主 KPI 保持固定位置与定义；异常排行作为次级诊断，不得让最高异常替代主 KPI。图例或直接标签必须邻近所解码的证据。
- **Degradation**：移动端、后台页、离屏及 reduced-motion 状态暂停或显著降频。建立带进入/退出阈值、滞回和恢复测试的降级阶梯，优先批处理、聚合、裁剪与降频；保留源记录数、时间范围和告警语义，并显式标注降级原因与精度限制。
- **Responsive/accessibility**：分别定义桌面和移动阅读路径；窄屏保留主证据、来源、单位、时效与 caveat。提供键盘、触控、可见焦点、状态播报、足够对比度，以及语义摘要、长描述和表格/静态替代。

Verification

用确定性 fixture 覆盖完整、部分、过期、乱序快照及断线恢复；验证 KPI 稳定性、排序和标签。真实浏览器检查桌面/窄屏、后台暂停、低功耗、reduced-motion、键盘/触控、读屏、降级恢复、WebGL context loss、非空像素与静态 fallback，并记录帧耗时、内存、更新频率和各阈值。
```

三种措辞都坚持 `HOLD`，且没有把 full snapshot 误写成可重放 stream；候选输出还明确区分了 UI
刷新频率和数据更新频率、源不支持的 cursor、稳定首屏与降级恢复。这是一个完整的 data-owner
场景，仍不足以估计隐式发现的全量准确率。

## Residual risk

未在发布后的新 Codex 会话统计 implicit discovery 命中率；当前安装缓存仍是旧插件版本。浏览器真实
页面、Canvas/WebGL 像素和论文导出只有在具体项目中才可验证。本文件不代表任何产品、论文或部署已经
完成，也不包含账号、凭证、个人路径或项目专用运行时。

有效压力会话使用只读临时执行，显式禁用 plugins、memory 和 skill search，也没有读取外部资料。
`--ignore-user-config` 会让当前环境失去有效 provider/auth 配置并返回 401，因此有效会话仍保留这部分用户配置。
这组样例是可复跑的定性回归信号，不是统计 benchmark。
