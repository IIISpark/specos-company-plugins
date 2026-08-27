---
name: ispark-writing
description: Use for drafting, rewriting, adapting, or auditing reader-facing prose such as company docs, PRDs, reports, release notes, messages, and product copy, including requests to humanize or reduce robotic wording. For scholarly manuscripts use ispark-academic-writing; for visual or interaction changes use ispark-product-design. Exclude code-only and mechanical transforms.
---

# ISpark Writing

Use this for prose quality. Keep artifact authority, operational actions, and domain facts with their owning skill or repository.

## Route

- Draft, rewrite, adapt, or choose the minimum missing question: read `references/writing-method.md`.
- Apply the generation/rewrite/audit loop and register check: read `references/quality-loop.md`.
- Audit for observable AI-slop patterns without editing: read `references/anti-slop.md`.
- Write or edit Simplified Chinese: also read `references/chinese-writing.md`.
- Calibrate to an authorized author sample or project profile: read `references/voice-profile.md`.
- Match a PRD, technical note, decision memo, release note, collaboration message, hiring artifact, product copy, or public announcement: also read `references/artifact-modes.md`.
- Maintain or redistribute the Hallmark-derived material: read `references/upstream-hallmark.md`.

## Modes

- `draft`: turn supplied facts and intent into new prose, applying the quality floor before sentence generation.
- `rewrite`: improve existing prose while preserving its fact ledger and claim strength.
- `audit`: return ranked findings and concrete directions; do not edit unless the user separately asks.
- `adapt`: change audience, channel, length, or tone without changing the underlying facts.

## Defaults

- Write company-facing prose in Simplified Chinese unless the target artifact, audience, or user requires another language.
- Put temporary drafts and writing audits under `working-delta/`; use `.tmp/` or `tmp/` for disposable generated output. Do not write into hidden assistant or personal archive paths.
- Separate verified facts, inference, and unknowns before improving style.
- Preserve names, commands, dates, metrics, citations, modality, and explicit uncertainty unless an authoritative source supports a change.
- Detect the register and genre before applying a style rule; a report, message, product label, and essay should not share one default voice.
- Prefer concrete nouns and verbs, reader-relevant structure, and the shortest wording that keeps the needed meaning.
- Treat pattern hits as candidates, not verdicts: judge whether the paragraph has a real claim, then classify it as `rewordable` or `hollow`. Flag hollow content instead of inventing substance.
- Run at most three focused rewrite/self-check passes and leave already-strong prose alone. Do not fabricate specificity, add fake warmth, imitate human mistakes, or optimize for AI-detector evasion.
- Never edit direct quotes or required literals merely to lower a pattern count.
- Ask only for information whose absence would materially change facts, audience, action, or publication risk; otherwise state the bounded assumption and proceed.

When available, pair with `$ispark-docs-issues` for durable artifact structure and fact placement, `$ispark-product-design` for product and visual decisions, `$ispark-lark` for Feishu/Lark operations, and `$ispark-release-ops` for release evidence and shipping state. Keep this skill usable on its own when a fallback profile does not install those companions.
