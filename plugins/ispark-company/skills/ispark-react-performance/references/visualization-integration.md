# React And Next.js Visualization Integration

Use this reference after the visualization or architecture-diagram owner has defined the semantic model. It covers framework ownership, hydration, lifecycle, and measurable delivery cost rather than chart choice or visual direction.

## Split ownership cleanly

- React owns structure, container layout, surrounding controls, application state, routing, persistence, and committed selection summaries.
- The renderer owns geometry, scales, layout, picking, and its narrowly scoped draw lifecycle. Keep its boundary close to the SVG, Canvas, WebGL, or diagram surface.
- Do not let React and D3 or another imperative renderer mutate the same nodes. Let React render the subtree or give the renderer an isolated root; do not alternate ownership by update type.
- Separate data loading, semantic normalization, derived view models, renderer configuration, drawing, and interaction state. A chart component should not become the data client and product shell at once.
- Keep preview state such as hover local to the render boundary. Commit selected IDs, filters, ranges, or drill-down state to React only when the surrounding application needs them.

## Keep the Next.js boundary narrow

- Keep secrets, authorization, and privileged actions server-only. Send the smallest serializable client payload and follow the project's cache and request-deduplication semantics.
- Use Server Components for authorized data loading, deterministic transformation, framing content, and layout when the repository supports them.
- Put measurement, pointer input, browser-only APIs, imperative renderers, and GPU resources in a narrow Client Component. Do not move the whole route client-side because one chart needs the browser.
- Initialize server and client from the same normalized data and URL state. Do not derive first-render dimensions, IDs, timestamps, locale output, or random layout differently during hydration.
- Use a dynamic import for a heavy optional or browser-only renderer when it is not required for the initial reading path. Confirm the actual route and bundle before claiming a saving.
- Reserve dimensions or an aspect constraint before the client renderer loads so fallback, hydration, and final marks do not shift surrounding content.
- Verify the repository's React/Next.js versions, router mode, caching model, and supported loading API before adopting version-specific patterns.

## Bound high-frequency work

- Keep high-frequency pointer positions, animation frames, camera updates, and transient draw state out of broad React context or route state. Use renderer-local state, refs, or a measured external store, then publish meaningful committed changes.
- Avoid rebuilding scales, layout engines, parsed DSLs, buffers, textures, or renderer instances for unrelated parent rerenders. Use stable data/version inputs and memoize only work shown to be material.
- Scope effects to real external synchronization. Clean up `ResizeObserver`, `IntersectionObserver`, native listeners, timers, `requestAnimationFrame` loops, workers, and renderer instances when ownership changes or the component unmounts.
- For WebGL, define initialization, resize, context loss and restoration, animation pause, and GPU resource disposal inside the client boundary.
- Pause or reduce offscreen, route-hidden, background-tab, and reduced-motion work without changing the represented data or committed state.

## Budget and verify

State the expected simultaneous instance count and measure per-instance and page-level bundle, initialization, update, memory, and interaction cost. Share immutable transforms or resources only when ownership and invalidation remain explicit; do not add a global chart manager for a single surface.

Use focused component tests for ownership and cleanup, typecheck and production build for framework integration, and `$ispark-browser-qa` for real DOM, console, network, responsive, interaction, and nonblank Canvas/WebGL evidence. `$ispark-data-visualization` owns chart semantics; `$ispark-architecture-diagrams` owns diagram semantics; this reference owns their React/Next.js integration cost.
