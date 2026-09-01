---
type: feature
scope: plugin
audience: developer
summary: 新增架构图 owner，并补强实时 dashboard、React 可视化集成和 TypeScript renderer 契约。
breaking: false
demo_ready: false
tests:
  - "python -m unittest discover -s tools/tests -p 'test_*.py' -v"
  - "python tools/prepare_publish.py"
  - "python -X utf8 <codex-skill-root>/skill-creator/scripts/quick_validate.py skills/ispark-architecture-diagrams"
  - "python -X utf8 <codex-skill-root>/skill-creator/scripts/quick_validate.py skills/ispark-data-visualization"
  - "git diff --check"
artifacts:
  - "skills/ispark-architecture-diagrams/"
  - "skills/ispark-data-visualization/references/interaction-responsive-and-state.md"
  - "skills/ispark-react-performance/"
  - "skills/ispark-dev-workflow/"
  - "profiles/"
  - "plugins/ispark-company/"
  - "docs/visualization-skill-pressure-tests.md"
  - "tools/validate.py"
  - "tools/tests/test_validate.py"
---

# What changed

新增 `ispark-architecture-diagrams`，以短 discovery entry 和四个按需 reference 覆盖 UML、C4、ERD、
BPMN、sequence/state、依赖图和软件架构图的图型选择、source model、format/interchange、布局、交互、
验证与导出。它保留 source ID 和事实/推断状态，按建模问题选择 tree、layered、force、radial 等布局，
不把 Mermaid、渲染坐标或视觉输出误作架构事实源。

实时 dashboard reference 新增首屏扫描路径、主指标稳定位置、图旁 key、移动端 evidence-first，以及数据率
升高时可见的聚合、降频、缩窗等降级阶梯；对支持重放/增量的 stream 补上 resumable cursor、gap detection、
idempotent replay、snapshot-plus-delta 恢复，full snapshot/polling 则使用版本化完整替换；各路径都带进入/退出
阈值、hysteresis、资源压力和 URL 隐私边界；恢复门禁明确为 `live -> reconnecting -> repairing -> live`，
只有源契约支持的连续性或完整快照检查通过后才能恢复。高级模式还要记录 entry/exit condition、minimum
dwell 或 hysteresis、fallback、保留不变量、资源预算和 deterministic fixture。`ops` fallback profile 现在也包含
data visualization。`ispark-react-performance` 和 `ispark-dev-workflow` 分别新增按需加载的 React/Next renderer 集成和
TypeScript 数据/renderer 契约，保留 server/client 安全基线、finite number 与输入资源上限。

架构图 explorer 新增完整编辑契约：semantic edit 与 layout hint 分离、stable source ID、typed port、
提交前验证、undo/redo、dirty/save、版本冲突和 shareable-state 隐私。仓库验证器现会扫描所有可分发
skill 文本的个人邮箱/家目录、具体内部主机和下游项目/运行时 marker；manifest author 字段保持为公开包元数据。

# Why it matters

Agent 可以从自然语言发现软件架构图方法，而无需让数据可视化 skill 同时承担系统建模。React、TypeScript
和 dashboard 的高频细节只在对应任务命中后加载，普通工程、图表或产品设计任务不会预装这些正文。
source/model/render 分层、稳定状态、资源生命周期和显式降级也降低了图看起来正确但事实不可追溯、页面
不可恢复或高负载时静默改变数据含义的风险。
对所有 skill payload 的通用隐私门禁则把原先依赖已知字符串的检查提升为可持续的分发契约。

# Demo posture / limitations

本条记录 maintainer source、fallback profiles、文档、测试和生成 snapshot；发布与本机安装状态不由实现
条目单独证明，以对应 tag、GitHub Release 和安装回读为准。本轮未修改 Taste/product-design owner。三组 architecture 与一组 data 压力测试完整记录了 RED/GREEN/REFACTOR prompt、
预期、最终输出与配置；它们仍是只读定性回归，不是 discovery benchmark。强模型基线本身已命中主要风险，
因此不把它包装为“无 skill 必然失败”。
真实浏览器性能、可访问性和格式 round-trip 仍须在具体项目中验证。

# Verification evidence

- `python -m unittest discover -s tools/tests -p 'test_*.py' -v`：全量测试通过（测试数以命令输出为准）。
- `python tools/prepare_publish.py`：重建 21 个 skill 的 snapshot，仓库验证通过。
- source 与 snapshot 均为 183 个可分发文件，`tools/validate.py` 字节比较无差异。
- 21 个 source 与 snapshot skill 均通过 skill-creator `quick_validate.py`；architecture-diagrams 与
  data-visualization 也单独复核通过。
- 3 组 architecture 场景和 1 组 data 场景各完成 baseline/GREEN/REFACTOR，共 12 个有效只读会话；
  3 个 `--ignore-user-config` 认证失败会话已明确作废。
- `python -m py_compile tools/validate.py tools/tests/test_validate.py` 与 `git diff --check` 通过。
