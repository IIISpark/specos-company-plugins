# Interaction, Responsive Layout, And State

Interaction should reveal or compare evidence, not compensate for a weak default view.

## Define explicit states

Model the states that can change what the viewer believes:

- default, loading, partial, stale, empty, error, invalid, and offline;
- hovered or focused preview, committed selection, multi-selection, and cleared selection;
- filter, sort, brush, zoom, pan, range, tab, drill-down, comparison, and reset;
- live, paused, reconnecting, delayed, and last-updated time for operational data;
- permission, unavailable layer, unsupported renderer, and fallback mode when relevant.

State belongs outside draw calls so the same inputs render deterministically. A Canvas or WebGL scene must not be the only source of selected IDs, filters, or zoom state.

## Design the first scan

- State what the operator must understand on first scan before touching a control: current condition, the anomaly or change that needs attention, its comparison context, and the next useful detail or action.
- Keep the primary metric or signal in a stable position and encoding across refreshes, filters, and ordinary state changes. Reorder only when ranking is the analytical task, and make that movement legible.
- Keep direct labels and chart-adjacent keys with the evidence they decode. Do not make operators search a remote shared legend while comparing panels.
- Put filters and toggles beside the views they affect. On mobile, keep the main evidence before controls; after Apply, Cancel, Reset, or close, return focus and scroll context to the affected view.
- Treat supporting diagnostics as subordinate. A dashboard should optimize situation awareness and anomaly detection rather than maximize equally weighted tiles.

## Make exploration recoverable

- Hover may preview; click, tap, focus, or an explicit action should commit. Do not hide essential evidence or the only control behind hover.
- Keyboard and touch users need the same analytical path as pointer users, including focus order, selection, reset, details, and escape/cancel behavior.
- Put durable filters, ranges, selections, tabs, drill-down, or zoom in shareable state when revisiting, collaboration, or comparison matters.
- Serialize only non-sensitive, compact, allowlisted fields into shareable state. Never put secrets, credentials, private notes, raw sensitive data, free text, or precise sensitive locations in a URL; use an authorized server-side saved-view reference for protected or large state that is opaque, unpredictable, user/tenant-scoped, short-lived, and revocable. Enforce authorization on every resolve and prevent protected state or reference tokens from leaking through `Referer`, logs, caches, or analytics.
- Back/forward, refresh, copy-link, reset, and invalid-state behavior must be intentional. Avoid restoring stale state against a changed dataset without warning.
- Keep a visible summary of active filters, source date, caveats, and selection when panels collapse.

## Treat mobile as a sibling design

- Define the large-screen and mobile reading paths separately; DOM stacking alone is not a responsive design.
- Keep the main claim, comparison, source, caveat, and primary controls visible at narrow widths. Controls, legends, tooltips, and drawers must not cover the evidence.
- Use container measurement and stable aspect or min/max constraints so labels, loading text, and interaction do not resize the chart unpredictably.
- Adapt label density, orientation, small multiples, table fallback, and interaction mode instead of shrinking the entire desktop chart.
- Give touch targets sufficient size and spacing; replace hover-only detail with tap/focus or persistent disclosure.

## Bound motion and performance

- Animate a transition only when it explains continuity, ordering, a supported causal mechanism, or a state change. Temporal adjacency or visual flow alone is not causal evidence. Preserve the same conclusion with reduced-motion and a static fallback.
- Throttle or batch high-frequency input, virtualize or aggregate when needed, and retain the source count and method. Performance optimization must not silently change the analytical population.
- Budget for data size, update rate, page instance count, layout measurement, labels, hit testing, accessibility overlays, and export rather than timing only the draw call.
- Include battery and thermal pressure, device pixel ratio and GPU memory, bundle and bandwidth limits, offscreen work, background tab behavior, reduced motion, and explicit low-power or low-bandwidth modes in the resource budget.
- For live dashboards, show last successful update, stale thresholds, partial failures, and paused/reconnecting status. A quiet chart must not imply fresh data.
- Classify the feed as stream, snapshot, or polling. Handle event time versus arrival time, duplicate/out-of-order events, reconnect/backoff, and last-known-good data explicitly; alerts need a visible threshold, acknowledgement state, and update cadence.
- For append-only, ordered, or hybrid feeds that expose replay/delta and whose gaps affect accuracy, persist a resumable cursor or checkpoint, make gap detection explicit, and make duplicate delivery safe through stable event identity and idempotent replay. After reconnect or a detected gap, repair with the source-supported verified snapshot-plus-delta boundary or replay window before declaring the feed live again; do not invent a repair API the source does not provide.
- For full snapshots or polling sources without replay/delta semantics, do not invent a cursor. Replace data atomically by a version or timestamp, detect stale/partial responses, and show the last-known-good state until the next complete snapshot is accepted.
- Treat recovery as an explicit state machine: `live -> reconnecting -> repairing -> live` only after the source-supported continuity or complete-snapshot check passes; otherwise remain `stale`/`unavailable`, expose the reason, and require a deliberate retry or operator action. A cursor is valid only when the source documents stable event identity, ordering, and a replay retention boundary; if that boundary is exceeded, fall back to the documented full-snapshot path instead of guessing.

Define a degradation ladder for rising mark count, update rate, simultaneous instances, network pressure, or device limits. Give every step measured entry and exit thresholds, hysteresis or minimum dwell where oscillation is possible, and a tested recovery path to higher fidelity. Budget both per-instance and page-level cost, then prefer aggregation or multi-resolution summaries, batching, culling, lower-frequency updates, or a narrower time window before dropping evidence. Preserve source counts, time coverage, alert semantics, and last-known-good context. Keep the degraded mode visible with its reason and fidelity limit; never let silent decimation look like the full live feed.

## Accessibility continuation

Provide a concise semantic summary, meaningful title/caption, keyboard path, visible focus, sufficient contrast, and a table or downloadable equivalent when the medium permits. Complex views also need a long description that states the claim, data scope, unit, key values, caveats, and interaction state. Keep generated imagery or a contextual substrate separate from the data proof. Announce material state changes without narrating every pointer movement.
