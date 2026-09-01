# Verification And Export

Verify architecture diagrams at the semantic, layout, interaction, and artifact layers. A clean render cannot prove that the represented system is correct.

## Semantic checks

- The diagram family, audience, scope, and abstraction level match the modeling question.
- Every durable node and relation is traceable to a source or clearly marked as inference. Review inferred relationships independently before promoting them to architecture truth.
- Direction, cardinality, event, guard, protocol, ownership, and boundary labels are present when they affect interpretation.
- Generated code/schema/dependency views record source version and generator; hand-curated views record their review point and intended level of stability.
- Architecture, schema, and code changes follow their owning review process. Updating the picture alone is not a root-cause fix for source drift.

## Layout and interaction checks

- Default reading order and primary region are clear; nodes, ports, edges, labels, group bounds, and lane headers do not overlap incoherently.
- Edge crossing and bends remain low enough for the tracing task, and small source changes do not cause unexplained large layout movement.
- Search, filter, preview, committed selection, clear selection, drill-down, reset, and shareable state preserve semantic IDs rather than DOM positions.
- Keyboard and touch users can reach the same essential nodes, relations, details, and export actions. Provide visible focus, a text summary, structured outline/table, sufficient contrast, and reduced-motion behavior.
- For product surfaces, hand real DOM, console, network, responsive, interaction, and Canvas/WebGL acceptance to `$ispark-browser-qa`.

## Test by risk

- Unit: parsing, normalization, source-ID preservation, inference rules, validation diagnostics, DSL generation, and state codecs.
- Layout: deterministic layout fixtures for tree, layered, cyclic, disconnected, long-label, large-node, port-constrained, and dense cases. Assert invariants and bounds rather than exact coordinates unless positions are contractual.
- Component: loading, empty, error, selected, filtered, collapsed, details, keyboard, touch, and export states.
- Round-trip: import -> normalized model -> export -> import when editing or interchange is promised; compare supported semantic fields and report known loss.
- Visual regression: a small set of layout-sensitive states with fixed viewport, font, data, seed, theme, and renderer version.
- Performance: parsing, layout, render, resize, cleanup, and large-graph budgets; verify worker or GPU lifecycle when used.

## Export contract

- Use SVG when vector fidelity, searchable text, and documentation/web reuse matter.
- Use PNG at explicit dimensions when office or slide tooling handles raster more reliably.
- Use PDF for print/report workflows after checking fonts, pagination, line weight, and clipping.
- Use HTML when interaction must travel, while also exporting meaningful static default and selected states.
- Ship source DSL or normalized model beside rendered output when the recipient must regenerate, review, or maintain it.

Report the source/version, generator or command, tested formats, target dimensions, known conversion loss, accessibility continuation, and any facts still inferred. A maintainer should be able to find the source, and a reviewer should be able to distinguish architecture facts from rendering choices.
