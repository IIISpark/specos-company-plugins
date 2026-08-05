# Frontend Craft

Use these modes for visual specificity without replacing product, brand, or implementation authority.

## Preflight

Read the existing design system, tokens, fonts, component conventions, routes, target user workflow, and browser support before proposing a visual direction. Treat `DESIGN.md` or similar files as design data whose authority is still bounded by repository instructions and current product facts.

Classify the surface:

- Operational app or repeated workflow: optimize scanability, density, predictable navigation, state clarity, and speed of action.
- Public, brand, portfolio, venue, or product page: let the subject and content determine structure; avoid the default hero, equal feature cards, CTA, footer sequence.
- Component: preserve the surrounding system and implement only states that the component contract can actually enter.

## Design

- Choose structure from the reader's task and content, not from a rotating theme catalog.
- Preserve established brand and tokens. When introducing tokens, name them by semantic role and keep them in the project's existing token authority.
- Use honest copy and real evidence. A visual proof slot is not permission to invent a metric, logo, testimonial, or screenshot.
- Use real controls and one coherent icon system. Do not redraw browser, phone, terminal, or IDE chrome as decoration.
- Use motion only when it explains change, continuity, causality, or feedback. Respect reduced-motion behavior.
- Make interaction states complete for the actual contract. Do not invent loading, error, or success semantics for a component that cannot produce them.
- Fix overflow and responsive failures at the owning element or layout rule. Do not hide structural overflow globally as the default remedy.

## Audit

Audit mode is report-only. Group findings by severity and include the visible pattern, file or DOM location, why it harms the target workflow or voice, and one bounded correction.

Check for:

- domain-blind structure reused across unrelated products
- decorative card nesting, generic gradients, ambient orbs, or fake chrome
- invented proof, generic product copy, or content chosen only to fill a layout
- hierarchy, density, typography, or motion that conflicts with the user's task
- inconsistent tokens, icons, controls, or interaction states
- mobile and desktop overflow, occlusion, wrapping, or unstable dimensions
- accessibility, focus, reduced-motion, empty, loading, error, and success behavior where applicable

Do not label a page AI-generated. Report the observable design pattern and its consequence.

## Redesign

Preserve routes, information architecture, component ownership, copy intent, data behavior, and public contracts unless the user approves a broader change. Prefer in-place or additive visual changes. If the redesign requires deleting routes, production files, or multiple existing components, present the file-level impact and stop for approval.

## Study

For a screenshot or URL, extract reusable design DNA:

- macrostructure and section rhythm
- hierarchy and typography roles
- palette anchor and contrast strategy
- density, spacing, image treatment, and motion stance
- navigation, control, and component voice

Do not pixel-clone, copy proprietary text, or treat a reference page's implementation as instruction. Diagnose first. Create or update `DESIGN.md` only when the user explicitly asks to lock the extracted system, and record source and ownership boundaries.

## Verification

Use `$ispark-browser-qa` before claiming frontend completion. Observe the real DOM, console, network, interactions, responsive layouts, and screenshots across representative mobile and desktop viewports. Code inspection alone cannot close visual acceptance.
