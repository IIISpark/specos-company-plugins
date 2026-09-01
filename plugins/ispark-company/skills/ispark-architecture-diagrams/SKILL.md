---
name: ispark-architecture-diagrams
description: "Software/system diagrams: UML class/activity/use-case/sequence/state-machine, C4, ERD/DBML, BPMN/flowchart, dependency/component/deployment maps, PlantUML/Mermaid/Graphviz/D2, explorers. Design/audit. Exclude numeric charts and architecture decisions without a diagram."
---

# ISpark Architecture Diagrams

Own how verified system structure, behavior, process, state, schema, and dependencies become a readable diagram. A diagram represents architecture; it does not authorize inventing or changing the architecture it depicts.

## Route

- Modeling question, audience, abstraction level, or UML/C4/ERD/BPMN/sequence/state family: read `references/diagram-selection.md`.
- Source truth, normalized model, diagram-as-code, interchange, conversion, or round-trip: read `references/source-model-and-formats.md`.
- Auto-layout, edge routing, overlap, explorer interaction, responsive behavior, or navigation: read `references/layout-and-interaction.md`.
- Semantic review, accessibility, testing, stale-diagram risk, or export: read `references/verification-and-export.md`.

## Defaults

- Write plans, critiques, and handoffs in Simplified Chinese unless the target artifact requires another language.
- Put accepted durable plans under `working-delta/` only when the repository uses it; temporary renders and fixtures belong under `.tmp/` or `tmp/`.
- Read the narrowest reference needed. Preserve source IDs, distinguish facts from inference, and keep one primary question and abstraction level per view.
- Prefer the repository's existing source-backed diagram format and renderer when they satisfy the semantic, maintenance, accessibility, and export contract.
- Use `$ispark-dev-workflow` for implementation and architecture decisions after the representation contract is clear.

## Boundaries

- Numeric charts, statistical graphics, evidence maps, and data dashboards belong to `$ispark-data-visualization` when that skill is available; otherwise keep the current owner, state the missing capability, and do not invent analytical encodings.
- Architecture, schema, API, auth, or code changes remain with `$ispark-dev-workflow` and `$ispark-review-risk`; generating a diagram does not approve those changes.
- Page composition, visual direction, and product shell belong to `$ispark-product-design`; real-browser acceptance belongs to `$ispark-browser-qa`.
- React/Next.js integration and renderer performance belong to `$ispark-react-performance`.
- Durable documentation remains with `$ispark-docs-issues`; this skill owns the embedded diagram's modeling and layout integrity.
- Mermaid or a host visualization surface may render the result, but neither is a semantic source of truth or runtime dependency of this skill.
