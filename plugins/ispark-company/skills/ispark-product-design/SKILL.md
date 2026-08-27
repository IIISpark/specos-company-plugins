---
name: ispark-product-design
description: Use for product direction, frontend experience, prototypes, UI variants, visual references, redesigns, or visual/product review, including requests to remove generic, template-like, or AI-looking UI patterns. For wording-only edits use ispark-writing.
---

# ISpark Product Design

Use this for creative and product-facing work before or during implementation.

## Route

- Product framing or brainstorming: read `references/product-framing.md`.
- Frontend/UI design: read `references/frontend-design.md`.
- Frontend craft, anti-template or AI-slop audit, redesign, or screenshot/URL design study: read `references/frontend-craft.md`.
- Prototype or variants: read `references/prototype.md`.
- Design QA: read `references/design-qa.md`.
- Maintaining Hallmark-derived guidance: read `references/upstream-hallmark.md`.

## Defaults

- Write product critiques, design notes, PRDs, and prototype handoff text in Simplified Chinese unless the publication target explicitly requires another language.
- Put temporary explorations, variants, and review notes under `working-delta/`; generated images, screenshots, and disposable prototype outputs belong under `.tmp/` or `tmp/` unless the repo has a scoped artifact path.
- Start from target user workflow, not decoration.
- Build the usable experience, not a marketing shell, unless the user asks for a landing page.
- Respect existing brand/design systems before external style references.
- Treat generic gradients, card grids, font choices, badges, icon treatments, and copy as review signals rather than automatic bans; every visual change needs a product or interaction reason.
- Use `$ispark-writing` for product/UI copy drafting, rewriting, tone, or anti-slop prose audit; this skill owns product and visual decisions.
- Validate frontend work through `ispark-browser-qa`.
