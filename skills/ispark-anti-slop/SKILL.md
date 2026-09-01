---
name: ispark-anti-slop
description: Use only when a user explicitly asks to reduce AI-like, generic, template-like, or over-smoothed output across multiple or unclear artifact domains. Route clear prose, academic, UI, or code tasks directly to their owner. Do not perform authorship detection or detector evasion.
---

# ISpark Anti-Slop

Use this as a cross-domain quality gate when the request is about "AI 味"、模板感、泛化输出或过度润色。它识别可观察的质量风险，不判断作者，也不承诺绕过检测器。

## Quality floor

Before changing an artifact, establish:

- **Purpose**: the reader or user needs to decide, understand, act, or use something.
- **Specificity**: names, actors, actions, constraints, tradeoffs, and evidence that make the result fit this context.
- **Fidelity**: facts, scope, uncertainty, contracts, and required format remain intact.
- **Restraint**: no invented substance, fake personality, decorative complexity, or success state.
- **Evidence**: distinguish what was observed in source/code from what was observed in a render or inferred from appearance.

## Route by artifact

Read the narrowest owning skill before editing:

- Reader-facing prose, Chinese prose, reports, or copy -> `$ispark-writing`.
- Thesis, paper, abstract, method, results, discussion, or rebuttal -> `$ispark-academic-writing`.
- UML, C4, ERD/schema, BPMN, sequence/state, dependency, or software architecture diagrams -> `$ispark-architecture-diagrams` when available; architecture decisions and source changes remain with `$ispark-dev-workflow` and `$ispark-review-risk`, and a missing target must be reported rather than silently guessed.
- Data charts, maps, statistical graphics, evidence-bearing timelines/scrollytelling, or data-bearing diagrams whose encoding supports a claim -> `$ispark-data-visualization` when available; software/system diagrams use `$ispark-architecture-diagrams`, and UI-only dashboard shells/product direction use `$ispark-product-design`, with `$ispark-browser-qa` for rendered acceptance. If a target is unavailable, keep the current owner and state the gap.
- Frontend, UI, visual system, or page redesign -> `$ispark-product-design`, then `$ispark-browser-qa` for rendered acceptance.
- Code, PR, bug fix, generated implementation, or over-defensive branch -> `$ispark-dev-workflow` and, when reviewing risk, `$ispark-review-risk`.
- Durable docs, release notes, or issue artifacts -> `$ispark-docs-issues` plus `$ispark-writing`; release state remains with `$ispark-release-ops`.

The routed skill owns its facts, public contracts, design system, security boundary, and artifact format. This skill does not override those authorities.

## Short circuit

If the task clearly belongs to one domain, hand off to that owner immediately. Do not
load this skill's routing reference or a second domain skill. For mixed artifacts,
ambiguous requests, or cross-domain audits, read `references/routing.md` and load no
more than the two owner skills needed for the current decision.

## Review loop

1. Classify the artifact, audience, register, and requested mode (`draft`, `rewrite`, or `audit`).
2. Identify visible patterns and label confidence: source-certain, render-observed, or inference.
3. Fix the smallest confirmed problem at its owning layer. If the substance is missing, flag it instead of inventing it.
4. Re-check function, evidence, contracts, and reader fit in the artifact's real medium.
5. Report the change, evidence, unresolved items, and any deliberately unmade edits. Never call a style pattern proof of AI authorship.

## Defaults

- Prefer Simplified Chinese for plans and reports unless the target requires another language.
- Put temporary audits and drafts under `working-delta/`; put disposable renders and scan output under `.tmp/` or `tmp/`.
- A clean surface scan is not proof of good writing, design, or code. Keep semantic review and domain review separate.
- Do not use a universal banned-word list. A term, layout, safeguard, or formal convention may be correct when the context earns it.
- Do not trigger this cross-domain gate merely because the task contains prose, UI, or code; use the narrow owner directly when no anti-slop intent is present.
