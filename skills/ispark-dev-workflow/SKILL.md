---
name: ispark-dev-workflow
description: "Use for engineering specs and implementation: plans, TDD/tests, worktrees, safe module changes, minimal refactors, and verification. Docs-only: ispark-docs-issues; review-only: ispark-review-risk; unfamiliar-codebase mapping: ispark-codebase-understanding."
---

# ISpark Dev Workflow

Use this for normal engineering work. Keep the task scoped, read local project facts first, and verify each meaningful unit before expanding the change.

## Route

- Requirement clarification, engineering spec, or task brief: read `references/planning.md`.
- Implementation, regression tests, or TDD: read `references/testing.md`.
- Worktree or branch isolation: read `references/worktrees.md`.
- Domain terminology, module interface, architecture, or refactor decisions: read `references/architecture.md`.
- TypeScript visualization data or renderer contracts: read `references/typescript-visualization.md`.
- Minimal implementation and over-defensive-code review: read `references/code-minimalism.md`.
- Completion evidence or handoff: read `references/verification.md`.

## Defaults

- Write user-facing plans, briefs, reviews, docs, and handoff notes in Simplified Chinese unless the user, repo, or target artifact explicitly requires another language.
- Put temporary analysis, plans, and working documents under the repo's `working-delta/` when present; use `.tmp/` or `tmp/` for disposable command output. Do not create Superpowers, hidden assistant, or arbitrary home-directory document paths.
- Prefer local README/docs/config/code over generic assumptions.
- Make the smallest implementation that satisfies the stated outcome.
- Treat speculative null checks, defaults, retries, fallbacks, compatibility branches, wrappers, and abstractions as review candidates. Keep a branch only when a reproduced failure, documented contract, security boundary, or focused test justifies it.
- Do not change public contracts, schemas, auth, privacy, deploy, or destructive behavior without explicit approval.
- Preserve unrelated user changes.
- Report exact verification commands and results.
