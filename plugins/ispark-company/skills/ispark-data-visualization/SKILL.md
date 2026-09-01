---
name: ispark-data-visualization
description: "Evidence charts/maps/dashboards, statistical graphics, timelines/Gantt, scrollytelling, data-bearing diagrams; D3/SVG, Canvas/WebGL, live-data fidelity/degradation, uncertainty/accessibility, interaction/export. Exclude UI-only shells/QA and unrelated framework performance"
---

# ISpark Data Visualization

Own the analytical truth, encoding, and renderer decision for charts, maps, dashboards, statistical graphics, and evidence-bearing diagrams. Start with what the viewer must understand or decide; visual novelty is not a substitute for a supported claim.

## Route

- Analytical question, audience, data shape, chart family, source, or claim: read `references/task-and-evidence.md`.
- Encoding, scale, aggregation, missingness, uncertainty, labels, or color: read `references/encoding-and-statistical-integrity.md`.
- Library, renderer, scientific plotting, SVG/D3, Canvas, WebGL, map, or diagram choice: read `references/renderer-selection.md`.
- Dense Canvas/WebGL/Three rendering, pointer math, GPU lifecycle, or high-frequency redraw: read `references/high-density-rendering.md`.
- Interaction, responsive layout, state, live data, or accessibility behavior: read `references/interaction-responsive-and-state.md`.
- Scrollytelling, concept-led composition, maps with sensitive geometry, synthetic data, graph layout, or schedule semantics: read `references/composition-and-advanced-modes.md`.
- Correctness, browser evidence, visual regression, critique, or export: read `references/verification-and-export.md`.

## Defaults

- Write plans, critiques, and handoffs in Simplified Chinese unless the target artifact requires another language.
- Put durable accepted plans under `working-delta/` when the repository uses it; temporary data, screenshots, renders, and exports belong under `.tmp/` or `tmp/`.
- Read the narrowest reference needed for the current decision; add a second only when the task crosses that boundary.
- Preserve the repository's existing charting stack when it can meet the semantic, accessibility, performance, and export contract.
- Prefer the simplest truthful view and keep units, source, caveats, and essential evidence visible without hover.
- Use `$ispark-dev-workflow` for implementation sequencing and tests after the visualization contract is clear.

## Boundaries

- General page layout, UI styling, product experience, or visual direction belongs to `$ispark-product-design`.
- Real-page DOM, console, network, screenshot, responsive, and interaction acceptance belongs to `$ispark-browser-qa`.
- React/Next.js waterfalls, rerenders, bundles, and component API performance belong to `$ispark-react-performance`.
- For a generic in-conversation explanation, non-evidence simulator, or diagram, use the host's bundled `visualize` capability when available; this skill is for data or evidence semantics and does not depend on that plugin.
- UML, C4, ERD, BPMN, software architecture, and generic Mermaid system diagrams belong to `$ispark-architecture-diagrams` when that skill is available; otherwise keep the current owner, state the missing capability, and do not invent diagram semantics.
- Document, slide, PDF, and academic owners keep their artifact and prose contracts; this skill owns the embedded visualization's integrity.
