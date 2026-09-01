# Renderer Selection

Choose a renderer after the analytical and encoding contract. Respect the project's current dependencies and supported versions when they can satisfy the job. Do not migrate a working chart merely because another library is fashionable or more familiar.

D3 is one renderer path, not a default. Do not pin a CDN, framework version, or package command in this skill; verify the target repository's actual toolchain before implementation.

## Decision matrix

| Workload | Reasonable paths | Strengths | Costs and required fallback |
| --- | --- | --- | --- |
| Precise small dataset | semantic HTML table, CSS, existing design-system primitives | accessible lookup, copy, print | add a visual only when it improves pattern detection |
| Standard interactive chart | declarative Vega-Lite, Altair, Observable Plot, ECharts, Plotly, or the existing chart library | concise reproducible specification, common interactions | inspect generated accessibility, bundle, theme, and export behavior |
| Static or scientific figure | Matplotlib, Seaborn, Altair, plotnine, ggplot2, Makie, PGFPlots, or the established notebook/report stack | batch rendering, reproducibility, print control | record versions, fonts, dimensions, method, and vector/high-DPI export |
| Custom vector chart | SVG with native APIs or D3 for scales, shapes, layout, and interaction | precise geometry, labels, annotations, DOM inspection, vector export | DOM cost grows with marks; preserve semantics and avoid a D3-first rewrite |
| Dense flat marks or frequent redraw | Canvas with DOM controls and accessible summary | high mark throughput and flexible drawing | externalize state, hit testing, focus, labels, and static fallback |
| GPU-scale marks or real 3D | WebGL through Three.js, deck.gl, PixiJS, regl, Cesium, or the existing engine | large data, picking, terrain, depth, particles | verify context loss, nonblank pixels, reduced-motion, static fallback, and analytical need |
| Product map | MapLibre, Leaflet, deck.gl, or the existing map SDK | projection, tiles, pan/zoom, geographic layers | source geometry and tiles; pair with non-map comparison when location is not the only question |
| Network or editable graph | Cytoscape, Sigma, React Flow, ELK, Graphviz, or a domain component | layout and topology tooling | label density, deterministic layout, keyboard path, and tabular alternative |
| Software or system documentation diagrams | Mermaid, PlantUML, Graphviz, D2, or Structurizr | text-source diffs and reproducible layout | route semantics to `$ispark-architecture-diagrams`; the document owner retains the surrounding artifact and prose contract |

Names in the table are examples, not required dependencies. Prefer a proven project-local library over adding a parallel stack when it meets correctness, accessibility, performance, and export needs.

## Escalation questions

Choose the lowest-complexity path that passes all relevant questions:

1. How many marks are visible, how often do they update, and how many instances share the page?
2. Are custom geometry, labels, projections, brushing, picking, drag, zoom, or editing essential?
3. Must the output remain accessible, searchable, printable, editable, or exportable as SVG/PDF?
4. Is deterministic server, notebook, CI, or batch rendering required?
5. Does the team already maintain the renderer, and can the repository test it reliably?
6. Can a simpler static or declarative view communicate the same evidence?

Use Canvas for dense 2D drawing, not as the application state store. Use WebGL, Three, particles, animation, or 3D only when depth, motion, scale, or simulation carries analytical meaning. Provide a reduced-motion or static fallback that preserves the claim and caveats.

For evidence maps, use sourced geometry and a projection appropriate to the claim. A clearly labeled schematic map may simplify or distort space intentionally, but must not imply measured geographic precision. For diagrams, prefer a model-aware or text-source renderer before bespoke geometry unless custom spatial reasoning is the feature.
