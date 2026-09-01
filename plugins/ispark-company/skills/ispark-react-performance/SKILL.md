---
name: ispark-react-performance
description: "Use for React or Next.js performance, visualization integration, and scalable component APIs: waterfalls, bundles, server/client boundaries, hydration, rerenders, or boolean-prop proliferation. Do not use for visual design, non-React work, or browser acceptance alone."
---

# ISpark React Performance

Prioritize structural, observable React and Next.js performance improvements over
blanket memoization or framework folklore. Preserve behavior, accessibility, and the
repository's supported versions.

## Route

- React/Next.js performance or component-composition work: read
  `references/react-performance.md`.
- React/Next.js visualization integration, renderer lifecycle, hydration, or chart bundle cost:
  read `references/visualization-integration.md`.

## Defaults

- Write plans, reviews, and handoffs in Simplified Chinese unless the target artifact
  explicitly requires another language.
- Confirm React/Next.js versions, router/rendering mode, existing data library, and build
  configuration before using version-specific APIs.
- Keep benchmark captures and bundle reports under `.tmp/` or `tmp/`; place a durable
  accepted plan under `working-delta/` only when the repository uses that convention.
- Prefer measured bottlenecks and high-impact architecture over low-impact syntax tweaks.
- Use `ispark-dev-workflow` for implementation/testing, `ispark-product-design` for
  visual intent, and `ispark-browser-qa` for DOM, network, responsive, and interaction
  acceptance. Do not claim performance improvement without comparable evidence.
