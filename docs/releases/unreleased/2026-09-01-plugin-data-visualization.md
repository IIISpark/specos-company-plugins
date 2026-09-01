---
type: feature
scope: plugin
audience: developer
summary: 新增按需加载、技术栈中立的数据可视化 skill，覆盖分析语义、统计完整性、renderer 选择与验证。
breaking: false
demo_ready: false
tests:
  - "python -m unittest discover -s tools/tests -p 'test_*.py' -v"
  - "python tools/prepare_publish.py"
  - "git diff --check"
artifacts:
  - "skills/ispark-data-visualization/"
  - "skills/ispark-anti-slop/"
  - "profiles/"
  - "plugins/ispark-company/"
  - "docs/candidate-skill-integration.md"
  - "docs/visualization-skill-pressure-tests.md"
  - "tools/tests/test_validate.py"
---

# What changed

新增 `ispark-data-visualization`，用一个短 discovery entry 和七个按需 reference 覆盖 analytical
question、证据账本、视觉编码、统计完整性、renderer 选择、交互/响应式状态、验证和导出；其中
高密度 Canvas/WebGL reference 规定 backing store/DPR、坐标变换、分层失效、pointer capture、
typed buffers、context loss、资源释放和 non-WebGL fallback。声明式、
科学静态绘图、SVG/D3、Canvas、WebGL/Three.js、地图和 diagram renderer 都是按条件选择的分支，
D3 不再是默认答案。

skill 与 `ispark-product-design`、`ispark-browser-qa`、`ispark-react-performance` 和宿主会话内
visualization 能力之间建立了负向边界，并加入 `dramawork`、`engineer`、`frontend`、`ops`、`product`
和 `research` fallback profiles。跨域 anti-slop 路由也会把明确的数据可视化任务直接交给新 owner。

# Why it matters

Agent 可以从“这组数据用什么图”“审查这张图是否误导”“如何做论文图、地图或 dashboard”等自然
语言任务发现统一方法，却不会在未命中时加载 renderer、统计、交互或测试细节。选中后，数据语义和
证据边界先于技术栈，能够减少 D3-first、隐藏 uncertainty/missing data、hover-only、移动端遮挡、
空白 Canvas/WebGL 和不可复现导出等常见失败。实时恢复只有在源契约支持的连续性或完整快照检查通过后
才可回到 live；高级模式还必须提供 entry/exit、hysteresis、fallback、保留不变量和 deterministic
fixture，避免把关键门禁写成不可执行的宣传语。

# Demo posture / limitations

本条完成 maintainer source、fallback profiles、结构/路由测试、方法来源记录、DASH-01 RED/GREEN/REFACTOR
压力证据和生成 snapshot；发布与本机安装状态以对应 tag、GitHub Release 和安装回读为准。
本轮没有运行任何外部数据、网页或生产系统。静态门禁证明配置允许隐式调用、
职责边界和 source/snapshot 一致，但真实自然语言 discovery 准确率仍需在发布并本机更新后的新会话观察。
Taste、通用产品设计和前端开发 skill 的后续融合不在本轮范围。
