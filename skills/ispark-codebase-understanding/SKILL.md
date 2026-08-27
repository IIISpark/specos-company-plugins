---
name: ispark-codebase-understanding
description: Use for onboarding to, mapping, or explaining a large unfamiliar codebase, or for cross-module reconnaissance of architecture, ownership, entrypoints, dependencies, and execution flows before substantial work. Do not use for routine edits, implementation, or findings-led review.
---

# ISpark Codebase Understanding

Build a bounded, evidence-linked map that makes the next engineering decision safer.
Stop when the requested change or explanation has enough context; exhaustive indexing is
not the goal.

## Route

- Repository scout, onboarding map, or cross-module execution trace: read
  `references/scout.md`.

## Defaults

- Write the dossier and user-facing explanation in Simplified Chinese unless the target
  artifact explicitly requires another language.
- Read root and nested instructions, README/docs, manifests, configuration, code, and
  tests before inferring architecture. Identify the owning repository before Git work.
- Keep durable working notes under `working-delta/` when the repository uses it; raw
  inventories and generated output belong under `.tmp/` or `tmp/`.
- Separate verified facts, inference, and open questions, with file or command evidence.
- Start read-only. Do not install analyzers, launch dashboards, request tokens, or create
  a persistent knowledge graph unless the user explicitly asks and approves the cost.
- Hand implementation to `ispark-dev-workflow` and findings-led review to
  `ispark-review-risk`; this skill does not authorize either action by itself.
