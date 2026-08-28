# React And Next.js Performance

## Establish facts

Identify the supported React/Next.js versions, App or Pages Router, server/client
component boundary, data-fetch path, hydration model, and the metric or symptom being
improved. Capture a comparable baseline when making a performance claim.

For a Web Interface Guidelines review, also inspect accessibility, focus, keyboard,
loading/error/empty states, responsive overflow, and interaction feedback. Keep those
findings separate from performance findings and report the exact file or rendered
location. Fetch a current external guideline only when the user requests that source;
otherwise use the repository's design authority and browser evidence.

## Work by expected impact

1. **Waterfalls:** start independent work early and await it together; defer awaits until
   the branch actually needs them. Use streaming or Suspense only where loading and
   error behavior remain coherent.
2. **Bundle cost:** inspect the build output before changing imports. Lazy-load heavy,
   optional UI; defer non-critical third-party code; prefer analyzable imports when a
   package's barrel materially expands the bundle.
3. **Server/client boundary:** keep secrets, authorization, and privileged actions on
   the server. Send the smallest serializable client payload, avoid mutable request state
   at module scope, and use the project's supported request-deduplication/cache model.
4. **Client data and events:** deduplicate shared requests and global listeners using the
   existing project library. Version persisted browser state and keep it minimal.
5. **Rerenders:** derive state during render when possible, keep effect dependencies
   accurate, use lazy initialization for expensive initial state, and move interaction
   logic into the event that causes it. Add memoization only when work is expensive or
   measurement shows a benefit and inputs can remain stable.
6. **Composition:** when a component has real behavioral modes, prefer explicit variants
   or a coherent compound-component API over growing boolean switches. Do not introduce
   a provider, render prop, or abstraction for a single simple call site.

Treat React-version-specific advice as conditional. For example, verify React 19 support
before replacing established ref or context APIs. Preserve framework security checks,
cache semantics, loading/error states, and accessibility while optimizing.

Also check high-impact interface rules that commonly accompany performance work: avoid
barrel imports that expand bundles, use dynamic imports for heavy optional UI, defer
analytics and non-critical third parties, avoid module-level mutable request state, use
passive global listeners where appropriate, use `content-visibility` for genuinely long
lists, and use explicit conditional rendering when falsy values can leak into the UI.
These are review prompts, not blanket rewrites; confirm the supported framework and
measure before changing them.

## Verify

Run focused unit or component tests, typecheck, and the production build where relevant.
For user-visible changes, inspect the real page with browser tooling: DOM, console,
network requests, bundle/load behavior, interactions, and representative viewports.
Compare the same route and conditions against the baseline; do not infer a speedup from
code shape alone.
