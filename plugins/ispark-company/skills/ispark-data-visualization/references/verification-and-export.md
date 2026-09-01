# Verification And Export

Verify the visualization at the layer where a failure originates. Passing screenshot review cannot prove data correctness, and correct transforms cannot prove that the rendered result is legible or interactive.

## Verification ladder

1. **Data contract**: test schema, types, units, joins, filters, aggregation, normalization, missing data, uncertainty, scale/domain, and invariants against deterministic fixtures.
2. **Encoding contract**: test domains, ticks, baselines, bins, ordering, labels, color roles, intervals, and annotations with boundary, sparse, empty, and adversarial values.
3. **Component behavior**: test loading, stale, empty, error, selection, reset, keyboard, touch, URL/shareable state, and fallback behavior without relying on real time or random IDs.
4. **Real browser**: hand rendered acceptance to `$ispark-browser-qa`; inspect DOM, console, network, viewport layout, interactions, themes, and runtime failures on the actual page.
5. **Renderer evidence**: for Canvas/WebGL, wait for render-ready state, assert a nonblank pixel region, sample meaningful pixels or scene state, exercise resize/context loss, and verify the static fallback.
6. **Human critique**: inspect semantic truth, encoding, composition, interaction/accessibility, then implementation. Do not collapse these into an unexplained aggregate score.

Use targeted visual regression for stable geometry or critical states. Fix viewport, device scale, theme, locale, timezone, data fixture, random seed, animation, fonts, and network state; mask only truly nondeterministic regions. Avoid screenshotting every state when behavioral assertions are clearer and less brittle.

## Accessibility acceptance

- Check normal text at 4.5:1 contrast, large text at 3:1, and meaningful marks,
  adjacent graphical objects, and state indicators at 3:1 against their
  neighbors. Review dark/light themes, grayscale, and common color-vision
  differences; keep a color-role ledger so selection, warning, forecast, and
  categories do not silently reuse one hue.
- Pair color with position, direct labels, shape, dash, texture, ordering, or a
  table whenever the distinction affects the claim. Keep the title/caption,
  source, units, caveats, key values, active filters, and selection summary
  available without hover, pointer precision, or a permission-gated feature.
- Provide a keyboard path for focus, selection, reset, details, filters, and
  export, plus a concise semantic summary and a long description for complex
  views. Announce material live/stale/partial/error changes without narrating
  every pointer move; pair Canvas/WebGL or diagrams with an outline, table, or
  accessible HTML controls.
- Treat PDF, PNG, slide, and print output as separate acceptance targets. A
  static export must preserve the claim, source, units, caveat, uncertainty,
  and exact-value alternative without hover, autoplay, or network access.

- Mock at the loader/network boundary so transforms and renderer behavior see realistic canonical, edge, and stress fixtures without depending on live services.
- Assert semantic outputs, domains, selected IDs, and accessible state rather than exact SVG path strings, Canvas command logs, or huge DOM snapshots.
- Accept or update a visual baseline only after its data, encoding, fonts, viewport, and intended state have been reviewed; a stable wrong image is still wrong.

## Adversarial checks

- smallest, largest, negative, zero, equal, duplicate, out-of-order, and extreme values;
- long labels, mixed units, sparse groups, all-missing groups, missing intervals, and no-result filters;
- domain changes, truncated axes, log values at or below zero, timezone/DST boundaries, and category churn;
- slow, partial, stale, malformed, or reordered responses;
- keyboard-only, touch-only, reduced-motion, high zoom, grayscale, and narrow mobile layouts;
- many chart instances, rapid updates, large mark counts, export during interaction, and renderer fallback.

## Export contract

Choose outputs from the delivery need, not as an afterthought:

- SVG/PDF for vector editing and print when the renderer and fonts support it;
- PNG at explicit pixel dimensions and high DPI for raster publication;
- accessible HTML/table or source-data download when readers need exact values;
- a static screenshot or key-frame sequence that preserves the claim, source, units, caveats, and uncertainty without hover, autoplay, or network access.

For a scientific figure, record dataset/version, processing and statistical method, random seed where relevant, package versions, font, physical dimensions, color specification, and export command or notebook cell. Check captions and scholarly claims with the academic owner; this skill verifies the figure evidence.

## Completion evidence

Report the data fixtures and tests run, target viewports and themes observed, browser/runtime evidence, export files inspected, known limits, and anything still inferred. A nonblank render is necessary for Canvas/WebGL but does not by itself prove truthful encoding or useful interaction.
