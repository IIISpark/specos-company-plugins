# Composition And Advanced Modes

Read this reference when the visualization is a narrative, map-heavy, graph-heavy, synthetic, or unusually
immersive artifact. It adds conditions to the core evidence contract; it does not authorize decorative complexity.

## Compose from the claim

- Write a testable insight or descriptive claim title before choosing a hero view. Give the first viewport one
  focal comparison; use annotations to explain a turning point, mechanism, exception, or uncertainty.
- Keep evidence layers, labels, source notes, and caveats data-bound and editable when the artifact may change.
  Do not use an equal-weight tile gallery, atmospheric background, or generated image to create importance that
  the data does not support.
- Treat a visual reference as a principle to evaluate, not a template to copy. A polished surface still needs a
  clear default reading path, a plain-language summary, and a static continuation.
- If layout, imagery, art direction, or concept selection is the unresolved product decision, hand that approval
  loop to `$ispark-product-design`; keep data labels, evidence, and renderer constraints explicit in the handoff.
- For sensitive, humanitarian, political, or human-impact data, show date, source hierarchy, evidence status,
  uncertainty, denominator, and humane framing. Do not turn people or places into spectacle or false precision.

## Scrollytelling and staged stories

- Decide whether scroll position, an explicit stepper, or a conventional small-multiple view is the clearest
  control. The scene should be a deterministic function of data plus a committed step, not an animation that
  hides the state.
- Define scene enter/exit thresholds, progress-to-state mapping, sticky or non-sticky ownership, media loading,
  and what happens when a scene is skipped, resized, or reached by a deep link. Reserve space before media loads
  so the evidence and focus order do not jump.
- Use native scrolling; do not hijack wheel/touch input or make progress impossible to reverse. Support fast
  scroll, reverse scroll, reload, deep links, resize, keyboard focus, reduced motion, and a narrow/mobile
  stacked or key-frame fallback.
- Keep each scene's claim, source, caveat, and required labels available when the reader lands directly on it.
  Autoplay, parallax, video, and transition effects are optional and must have pause/skip and static paths.

## Maps and spatial evidence

- Record coordinate reference system, units, timestamp/timezone, source geometry, projection, and normalization.
  Check longitude wrapping, antimeridian behavior, and whether projection distorts area, distance, direction, or
  density for the stated claim.
- Keep map layers, marks, labels, hit regions, camera transforms, and fallback/table views in one coordinate
  contract. Use sourced geometry; a schematic map is acceptable only when explicitly labeled and not presented
  as measured geographic precision.
- Record basemap/provider attribution, tile or vector source, rate limits, cache lifetime, offline/failed-tile
  behavior, and a non-map comparison fallback. Define ownership for wheel, pinch, drag, and page scroll so a
  map cannot silently consume the only path through the surrounding document.
- Decide how overlapping points, small regions, missing geometry, and multiscale labels behave (cluster,
  aggregate, offset, or disclose). Do not let a choropleth's palette or area stand in for a denominator.
- For sensitive locations, reduce precision only with an explicit privacy or safety rationale and preserve the
  resulting uncertainty in the caption and data contract.

## Synthetic data, graphs, and schedules

- Label fictional or simulated data in the artifact. Record fixed seed, named assumptions, entity/time/spatial/
  event/outcome layers, derived fields, and invariants; never invent KPI values merely to fill visual space.
- For graphs, preserve stable node/edge IDs and source semantics. Choose a layout for the question (topology,
  flow, dependency, or grouping), and provide a searchable or tabular path when labels overlap. Name the layout
  family and its phases (for example tidy-tree, layered/Sugiyama, stress/force, routing, crossing reduction,
  overlap removal, and component packing); software/system graph semantics route to `$ispark-architecture-diagrams`.
- For timelines or Gantt views, distinguish planned spans, milestones, dependencies, baselines, resources,
  calendars, and actual lifecycle intervals. Keep source IDs, timezone, and ambiguous fields; issue-created or
  issue-closed timestamps are not automatically a planned schedule. If critical path or float is shown, define
  the dependency model and calculation; record import/export format, calendar assumptions, and how missing or
  conflicting spans are surfaced.

## Advanced-mode gate

Escalate to immersive, animated, map-heavy, or staged composition only when the mode exposes evidence that a
simpler view cannot. Require a named fallback, deterministic state, source/caveat continuity, and a verification
plan before implementation; otherwise return to the narrowest truthful chart or table. For each advanced mode,
record an executable contract: entry condition, exit condition, minimum dwell or hysteresis, fallback state,
preserved invariants (claim, units, source, caveat, IDs, and coverage), resource budget, and a deterministic
fixture that exercises entry, steady state, exit, interruption, resize, and recovery. Do not ship a mode whose
thresholds or fallback exist only as prose.
