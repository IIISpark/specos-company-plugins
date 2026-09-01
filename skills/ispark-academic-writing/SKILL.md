---
name: ispark-academic-writing
description: "Use for Chinese/English theses, papers, abstracts, methods, results, discussions, conclusions, or rebuttals: draft, revise, adapt, audit, humanize while preserving citations, equations, terminology, evidence, uncertainty, claim strength, and voice. Exclude general prose."
---

# ISpark Academic Writing

Use this skill for academic prose. Its goal is disciplined authorial judgment and readable argumentation, not casual tone, authorship claims, or detector evasion.

## Route

- General workflow, section roles, and revision intensity: read `references/academic-method.md`.
- Chinese academic patterns and false-positive boundaries: read `references/chinese-patterns.md`.
- Citation, notation, and claim-preservation checks: read `references/verification.md`.

## Modes

- `draft`: write from supplied research facts and an explicit argument boundary.
- `rewrite`: revise supplied prose without changing its claims or evidence.
- `audit`: report ranked issues only; do not rewrite.
- `adapt`: change audience, language, or density while retaining academic scope.

Use `light`, `medium` (default), or `deep` revision intensity. A deeper rewrite may change sentence structure and paragraph cohesion, but never adds unsupported research content.

## Non-negotiables

- Preserve citations and their scope, BibTeX keys, formulas, variables, units, figure/table labels, section references, dataset/model names, markup, and required terminology.
- Preserve modality and conditions: `may`, `suggests`, association, tested population, denominator, and stated limitations do not become stronger claims.
- Do not add literature, results, examples, mechanisms, novelty, causal explanations, or future implications that are absent from the source.
- Keep method, result, discussion, and conclusion functions distinct. Flag ambiguous or inconsistent source material instead of silently repairing it.

## Workflow

1. Identify language, section type, audience, intensity, and the manuscript's existing register.
2. Build a preservation ledger for literals, evidence, claim strength, terminology, and paragraph roles.
3. Diagnose surface patterns and substance separately. A smooth sentence with no supported claim is a flag, not an invitation to invent one.
4. Rewrite only where the source supports the sharper wording. Prefer concrete research actions and results over stock background, abstract noun chains, and promotional endings.
5. Compare source and revision for new facts, changed citation scope, notation drift, omitted caveats, and altered argument order.
6. Return the requested revision; for a normal rewrite, include concise material-change notes. For audit mode, return findings only.

## Defaults

- Use Simplified Chinese for reports about the editing work unless the target manuscript requires another language.
- Put temporary comparison tables and audit notes under `working-delta/`; put disposable exports under `.tmp/` or `tmp/`.
- Keep a terminology map for long documents. Do not rotate synonyms merely to avoid repetition when a term names a fixed construct.
- The canonical manuscript, evidence protocol, and domain expert remain authoritative over this skill.
