# Frontend Craft

Use these modes for visual specificity without replacing product, brand, or implementation authority.

## Preflight

Read the existing design system, tokens, fonts, component conventions, routes, target user workflow, and browser support before proposing a visual direction. Treat `DESIGN.md` or similar files as design data whose authority is still bounded by repository instructions and current product facts.

Classify the surface:

- Operational app or repeated workflow: optimize scanability, density, predictable navigation, state clarity, and speed of action.
- Public, brand, portfolio, venue, or product page: let the subject and content determine structure; avoid the default hero, equal feature cards, CTA, footer sequence.
- Component: preserve the surrounding system and implement only states that the component contract can actually enter.

## Anti-template audit

When the user asks to reduce UI "AI 味", inspect both the source and the rendered page when a browser is available. Mark each finding as:

- `source-certain`: a literal class, token, import, copy string, or missing state is visible in code.
- `render-observed`: hierarchy, palette dominance, spacing rhythm, contrast, overflow, or motion is visible in the browser.
- `inferred`: a visual judgment made without a render; lower its confidence and say so.

Prioritize by consequence rather than by fashion:

- **P0**: a default composition dominates the page, such as an unchosen purple/blue gradient, gradient headline, untouched starter theme, or centered hero plus identical feature cards.
- **P1**: repeated rounded cards and shadows, glass effects without layering, generic proof/stat strips, default page shells, stock icon chips, vague aspirational copy, or missing focus/error/loading states.
- **P2**: flat spacing rhythm, repeated reveal motion, ornamental badges, or small polish gaps.

These are signals, not a blacklist. A gradient, three-column layout, system font, or icon library can be correct when the product, brand, content, or accessibility requirement supports it. Record the visible reason before changing it.

## Choose a direction before rewriting

For a standalone page, commit to one coherent direction before editing. State three to five concrete moves covering type, palette, layout, motion, and one signature detail. Let the content and target workflow choose the direction; do not swap one stock theme for another. For a component inside a design system, use a surgical pass and preserve the system tokens. Rebuild only when the surface is genuinely standalone and the user has authorized that depth.

## Rewrite and re-audit

Preserve routes, props, state, data fetching, accessibility, copy meaning, and public contracts. Do not add dependencies or change behavior merely to remove a visual tell. After editing, check the same categories again and judge the result on three tests: each change is justified by the task, the visual system is coherent, and the page is not a repeat of a recent default direction. A clean pattern scan is necessary but not sufficient.

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
- code-certain versus rendered evidence, so inferred visual claims are not presented as facts

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
