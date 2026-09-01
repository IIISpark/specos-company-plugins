# TypeScript Visualization Contracts

Use this reference when a TypeScript implementation needs reliable chart, map, timeline, simulation, or architecture-diagram data and renderer boundaries. The visualization owner chooses the semantics and encoding; this reference keeps those decisions intact in code.

## Validate the boundary

- Validate external data at the loader boundary. Treat parsed JSON, CSV rows, URL parameters, persisted state, DSL input, and untrusted or undocumented external callback payloads as `unknown` until a runtime schema or explicit parser establishes the contract.
- Require finite numbers rather than accepting `NaN` or `Infinity`. Enforce row, node, edge, string, and nesting limits from explicit product and resource budgets; reject, aggregate, or enter a visible degraded mode when structurally valid input exceeds them.
- Preserve source IDs, units, denominator, timezone, missingness, uncertainty, provenance, and version fields when they affect interpretation. Do not replace missing, stale, suppressed, invalid, or not-applicable values with one nullable number.
- Use discriminated unions for states with different valid payloads, such as observed versus estimated values, loading versus stale data, or preview versus committed selection.
- Reject or visibly report invalid source data according to the product contract. Type assertions, default objects, and `any` do not repair an invalid upstream payload.

## Keep a traceable pipeline

Separate raw source rows, a normalized semantic model, pure transformations, scales/domains or layout inputs, derived marks, renderer adapters, interaction state, and export state. Each layer should retain enough identity to trace a visible mark or diagram edge back to its source.

- Keep transformations deterministic and independently testable. Inject clocks and use a fixed seed when time, sampling, simulation, or layout randomness is part of the result.
- Keep renderer-specific coordinates, handles, scene objects, and DOM/GPU references out of the canonical semantic model.
- Add a renderer adapter only at a real boundary, such as two maintained renderers, an export target, or an external library model. Do not create a generic chart framework for hypothetical future backends.
- For architecture diagrams, model nodes, edges, groups, ports, labels, source references, inference status, and layout hints before adapting to a DSL or interactive renderer.

## Type durable and ephemeral state separately

Define a canonical view-state codec when filters, ranges, selected entities, active views, camera bounds, or drill-down paths are shareable or persisted. The codec must parse, validate, normalize defaults, serialize in stable order, and migrate or reject stale schema versions.

Limit shareable state to non-sensitive, compact, allowlisted fields. Never serialize secrets, credentials, private notes, raw sensitive data, arbitrary free text, or precise sensitive locations into a URL; use an authorized server-side saved-view reference for protected or large state that is opaque, unpredictable, user/tenant-scoped, short-lived, and revocable. Enforce authorization on every resolve and prevent protected state or reference tokens from leaking through `Referer`, logs, caches, or analytics.

Keep ephemeral interaction state such as hover, pointer position, drag-in-progress, animation frame, temporary camera velocity, and open tooltip out of saved URLs and durable workspace payloads. Define precedence among incoming URL state, saved state, repository defaults, and renderer-local state so hydration and refresh do not invent a transient view.

## Verify the contract

Test schema rejection, normalization, units, missing and uncertain values, stable IDs, transform invariants, state-codec round trips, stale-version policy, and deterministic fixtures before renderer snapshots. Test public behavior and semantic outputs rather than exact SVG paths, Canvas command logs, or library-internal objects. Use `$ispark-browser-qa` for rendered behavior and the relevant visualization owner for evidence or diagram correctness.
