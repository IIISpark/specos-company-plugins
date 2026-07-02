---
name: ispark-review-risk
description: Use when reviewing code or plans, challenging architecture, assessing security or privacy risk, checking destructive operations, evaluating public contracts, or deciding whether a local patch is hiding a deeper problem.
---

# ISpark Review And Risk

Use this skill to slow down decisions that can create long-term or operational damage.

## Route

- Code review: read `references/code-review.md`.
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
