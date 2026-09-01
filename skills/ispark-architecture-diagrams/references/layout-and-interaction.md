# Layout And Interaction

Choose layout from graph structure and reading task, then treat routing, labels, overlap removal, and navigation as separate decisions.

## Match layout to structure

- Use a tidy tree for rooted ordered trees and decision trees where parent-child depth and sibling order carry meaning.
- Use layered or Sugiyama-style layout for directional workflows, state machines, dependency maps, class hierarchies, ERDs, and most architecture flows.
- Use force or stress layouts for undirected exploration when neighborhood, cluster, or approximate graph distance is the evidence; do not use them for ordered business flow by habit.
- Use radial or circular layout only when distance from a root, hub structure, or cycle order is the actual reading model.
- For a graph too dense to trace, prefer a filtered neighborhood, hierarchy, matrix, clustered overview, or coordinated views before adding more visual effects.

Supply real node sizes, labels, group bounds, lane order, fixed nodes, and port constraints to the layout stage. Choose orthogonal routing for ERDs, block diagrams, schemas, and port-aware topology when it improves connector tracing. Handle crossing reduction, bends, label placement, component packing, and overlap removal explicitly; a layout engine does not solve all of them at once.

Prefer stable layout when readers compare versions, recognize recurring nodes, or manually curate positions. Preserve meaningful source and port order, avoid a fresh random layout after small edits, and keep renderer coordinates as replaceable hints rather than architecture facts.

## Design the explorer state

- Keep semantic data and view state outside the renderer. Model active diagram, search, filter, focused ID, preview, committed selection, expanded groups, layout mode, and viewport explicitly.
- Hover or focus may preview adjacency; click, tap, keyboard action, or an explicit command should create committed selection. Clear selection from an intentional empty-surface or reset action.
- Make durable filters, selected entities, active subview, and drill-down path shareable state when review or collaboration requires it. Define refresh, back/forward, invalid-link, and dataset-version behavior.
- Keep shareable state non-sensitive, compact, allowlisted. Never put credentials, restricted entity names, private notes, raw sensitive data, or arbitrary free text in the URL; use an authorized server-side saved-view reference for protected or large state that is opaque, unpredictable, user/tenant-scoped, short-lived, and revocable. Enforce authorization on every resolve and prevent protected state or reference tokens from leaking through `Referer`, logs, caches, or analytics.
- Pair dense diagrams with a synchronized outline or table so search and keyboard users can reach nodes, edges, states, fields, and relationships without precision panning.
- Keep details from covering the diagram. On mobile, lead with a focused region or outline-to-detail path, provide touch alternatives for hover and drag, and use landscape only when it materially improves tracing.
- Respect reduced-motion for layout transitions and guided steps. Keep a static or stepwise path that preserves the same structure and selected relation.

## Protect legibility

Increase the intrinsic canvas and use an obvious scrollable viewport before shrinking labels below readable size. Start the default viewport on the most important region when the whole model cannot fit. Keep connectors out of table bodies, labels, and lane headers; attach schema relations through stable sides or gutters. Use quiet default edges, medium preview, and strong selected paths so the complete topology remains present without becoming visual noise.

## Protect editing semantics

- Distinguish semantic edits to owned architecture facts from cosmetic layout hints. Renderer coordinates, bends, collapsed groups, and viewport state must not silently become source truth.
- Address semantic nodes and edges through stable source IDs and typed ports. Validate before commit against the source model, ownership boundary, and relationship rules.
- Provide undo and redo for committed edits, expose dirty and save state, and define cancellation and failed-save behavior.
- Detect dataset or document version conflicts before saving. Do not use last-write-wins or any other silent overwrite of newer source facts; require an explicit merge, reload, or conflict decision.
- Keep product interaction design with `$ispark-product-design` and implementation sequencing with `$ispark-dev-workflow`; this skill defines what an architecture edit means and which source owns it.
