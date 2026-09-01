---
name: ispark-review-risk
description: "Use for review-only findings on code/diffs, plans, architecture, security/privacy, destructive actions, public contracts, root causes, generated-code risk, and audit context. Implementation: ispark-dev-workflow; unfamiliar-codebase mapping: ispark-codebase-understanding."
---

# ISpark Review And Risk

Use this skill to slow down decisions that can create long-term or operational damage.

## Route

- Code review: read `references/code-review.md`.
- Unfamiliar-code security, threat-model, or architecture audit: first read `references/audit-context.md`.
- Generated-code or over-defensive branch review: also read `references/code-review.md` and inspect the branch evidence.
- Diff, variant, or sharp-edge review: read `references/code-review.md` and map the changed boundary, neighboring implementations, and failure-preserving behavior before findings.
- Plan or product critique: read `references/plan-review.md`.
- Security/privacy/contracts: read `references/security-contracts.md`.
- Destructive or high-side-effect actions: read `references/destructive-actions.md`.

## Defaults

- Write review findings, risk notes, and decision memos in Simplified Chinese unless the target artifact explicitly requires another language.
- Put temporary review notes under `working-delta/`; use `.tmp/` or `tmp/` only for disposable raw outputs. Do not write review artifacts into Superpowers or hidden assistant paths.
- Findings first, ordered by severity.
- Cite file paths, line numbers, commands, or observed evidence.
- Separate confirmed facts from inference.
- Do not approve changes that rely on hidden assumptions or unverified downstream behavior.
