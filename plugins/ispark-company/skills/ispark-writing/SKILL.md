---
name: ispark-writing
description: Use when drafting, rewriting, editing, adapting, or auditing reader-facing prose where clarity, specificity, evidence boundaries, voice, or AI-generated sameness matters, including company documents, PRDs, decision memos, reports, release notes, announcements, Lark messages, and product/UI copy. Do not use for code-only changes, mechanical data transforms, or artifact structure/transport alone.
---

# ISpark Writing

Use this for prose quality. Keep artifact authority, operational actions, and domain facts with their owning skill or repository.

## Route

- Draft, rewrite, adapt, or choose the minimum missing question: read `references/writing-method.md`.
- Audit for observable AI-slop patterns without editing: read `references/anti-slop.md`.
- Write or edit Simplified Chinese: also read `references/chinese-writing.md`.
- Match a PRD, technical note, decision memo, release note, collaboration message, hiring artifact, product copy, or public announcement: also read `references/artifact-modes.md`.
- Maintain or redistribute the Hallmark-derived material: read `references/upstream-hallmark.md`.

## Modes

- `draft`: turn supplied facts and intent into new prose.
- `rewrite`: improve existing prose while preserving its fact ledger and claim strength.
- `audit`: return ranked findings and concrete directions; do not edit unless the user separately asks.
- `adapt`: change audience, channel, length, or tone without changing the underlying facts.

## Defaults

- Write company-facing prose in Simplified Chinese unless the target artifact, audience, or user requires another language.
- Put temporary drafts and writing audits under `working-delta/`; use `.tmp/` or `tmp/` for disposable generated output. Do not write into hidden assistant or personal archive paths.
- Separate verified facts, inference, and unknowns before improving style.
- Preserve names, commands, dates, metrics, citations, modality, and explicit uncertainty unless an authoritative source supports a change.
- Prefer concrete nouns and verbs, reader-relevant structure, and the shortest wording that keeps the needed meaning.
- Do not fabricate specificity, add fake warmth, imitate human mistakes, or optimize for AI-detector evasion.
- Ask only for information whose absence would materially change facts, audience, action, or publication risk; otherwise state the bounded assumption and proceed.

When available, pair with `$ispark-docs-issues` for durable artifact structure and fact placement, `$ispark-product-design` for product and visual decisions, `$ispark-lark` for Feishu/Lark operations, and `$ispark-release-ops` for release evidence and shipping state. Keep this skill usable on its own when a fallback profile does not install those companions.
