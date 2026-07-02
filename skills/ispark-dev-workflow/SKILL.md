---
name: ispark-dev-workflow
description: Use when implementing code, planning multi-step development, choosing a worktree strategy, deciding test scope, updating architecture safely, preparing handoffs, or verifying before claiming engineering work is complete.
---

# ISpark Dev Workflow

Use this for normal engineering work. Keep the task scoped, read local project facts first, and verify each meaningful unit before expanding the change.

## Route

- Planning or task brief: read `references/planning.md`.
- Implementation and tests: read `references/testing.md`.
- Worktree or branch isolation: read `references/worktrees.md`.
- Architecture or refactor decisions: read `references/architecture.md`.
- Completion evidence or handoff: read `references/verification.md`.

## Defaults

- Write user-facing plans, briefs, reviews, docs, and handoff notes in Simplified Chinese unless the user, repo, or target artifact explicitly requires another language.
- Put temporary analysis, plans, and working documents under the repo's `working-delta/` when present; use `.tmp/` or `tmp/` for disposable command output. Do not create Superpowers, hidden assistant, or arbitrary home-directory document paths.
- Prefer local README/docs/config/code over generic assumptions.
- Make the smallest implementation that satisfies the stated outcome.
- Do not change public contracts, schemas, auth, privacy, deploy, or destructive behavior without explicit approval.
- Preserve unrelated user changes.
- Report exact verification commands and results.
