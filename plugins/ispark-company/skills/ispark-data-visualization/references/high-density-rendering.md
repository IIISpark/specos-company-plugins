# High-Density Canvas And WebGL Rendering

Use this reference for dense Canvas2D, WebGL, Three.js, GPU, particle, tiled, or
high-frequency views. It specifies rendering and interaction contracts; the
visualization owner still decides what a mark means and whether the extra
complexity is justified.

## Choose The Smallest Renderer

- Keep HTML/SVG or a declarative grammar when exact labels, native semantics,
  print, editable vector export, or small mark counts dominate.
- Use Canvas2D for flat dense marks, frequent redraw, sparklines, heatmaps, or
  custom hit testing when raster output is acceptable and a DOM companion can
  carry labels and controls.
- Use WebGL or Three.js directly when true depth, terrain, volume, or occlusion
  is part of the evidence. For dense flat 2D, upgrade from Canvas2D when
  instancing, shader logic, GPU picking, blending, or very large layers are the
  measured bottleneck. WebGL is not automatically faster after buffer uploads,
  preprocessing, context pressure, and memory are counted.

## Canvas2D Contract

- Keep a retained semantic scene outside the drawing context: stable IDs, data
  records, scales, world-to-screen transform, mark descriptors, selection, and
  invalidation state. Canvas is a renderer, not the state store.
- Maintain CSS-pixel layout separately from the backing store. Set bitmap size
  to `cssWidth * clampedDevicePixelRatio`, reset with
  `ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0)`, and redraw on CSS-size,
  page-zoom, or DPR changes. Treat pinch zoom separately unless crisp redraw is
  an intentional product behavior.
- Share one transform between marks, HTML/SVG labels, overlays, and hit tests.
  If a parent has a non-uniform CSS transform, invert the full `DOMMatrix`, not
  only `clientX - rect.left`.
- Split static context, primary marks, and interaction/highlight layers when a
  hover or selection should not invalidate the whole scene. Prefer partial
  invalidation, culling, batching, typed arrays, cached geometry, and one
  virtualized/shared surface over hundreds of backing stores.
- Normalize pointer coordinates through `getBoundingClientRect()`, invert the
  active transform, and use pointer capture for drags. End drag state on
  `pointerup`, `pointercancel`, and `lostpointercapture`; define `touch-action`
  and a non-drag keyboard/touch path deliberately.
- Use a spatial index, analytic test, `Path2D` candidate replay, or a picking
  buffer according to mark count and pointer frequency. For color picking,
  document ID encoding, antialiasing/alpha assumptions, invalidation, and the
  `getImageData()` readback cost; use `willReadFrequently` only on readback
  canvases.
- Put axes, labels, legends, tooltips, menus, focus rings, tables, and status in
  HTML/SVG when they need native semantics. Keep a static/table fallback and a
  visible stale or offline overlay instead of blanking the evidence.
- Estimate backing-store memory as
  `width * height * pixelRatio^2 * 4 * layerCount * instanceCount`, then include
  picking buffers, overlays, framework overhead, and browser allocation.
  Cap DPR or quality under mobile memory, battery, or thermal pressure. Move
  aggregation, layout, or rendering to a worker/`OffscreenCanvas` only when the
  transfer and lifecycle cost is measured.

## WebGL And Three.js Contract

- Keep positions, colors, sizes, timestamps, IDs, and selection masks in stable
  typed arrays or binary attributes. Separate static from dynamic attributes;
  use partial buffer updates, textures, or tiles instead of full uploads every
  frame. Minimize draw calls, state changes, texture swaps, and material churn.
- Use `BufferGeometry`, instancing, level of detail, frustum/viewport culling,
  screen-grid aggregation, clustering, or vector tiles before increasing raw
  GPU work. Keep CPU layout and preprocessing off the input path when a worker
  can own it.
- Use one scene clock. Update uniforms or small dynamic buffers for animation;
  do not rebuild CPU objects each frame. Pause hidden, offscreen, background-tab,
  reduced-motion, and route-unmounted work, and dispose buffers, geometries,
  materials, textures, render targets, listeners, and workers.
- Define resize, DPR cap, context loss/restoration, first-frame readiness, and a
  non-WebGL fallback. A screenshot must verify nonblank pixels and scene bounds,
  not only a canvas element. Provide reset/home/focus orientation and a 2D or
  tabular companion when perspective makes exact comparison hard.
- Pick only actionable marks. Use screen-space nearest-mark, a spatial index, or
  GPU picking rather than intersecting decorative glow. Hover previews; click,
  lasso, or brush commits. Keep particle count, speed, opacity, trail length,
  and blending semantics explicit: visual carriers must not imply individual
  records, exact totals, or certainty that the source does not support.
- Use 3D only when depth, volume, terrain, occlusion, trajectory, or a named
  camera comparison carries evidence. A particle, glow, orbit, or ambient loop
  needs an explanatory verb and a reduced-motion/static final state.

## Verification

Before claiming a dense renderer is ready, record visible marks, update cadence,
simultaneous instances, memory, bundle, initialization, frame/input cost, and
fallback thresholds. Test resize/DPR, zoom/pan, selection, pointer cancellation,
hidden-route pause, reduced motion, context loss, nonblank output, keyboard and
screen-reader paths, static export, and source-count preservation after any
aggregation or degradation. Use `$ispark-react-performance` for framework cost,
`$ispark-browser-qa` for real rendered evidence, and `$ispark-dev-workflow` for
implementation tests and deterministic fixtures.
