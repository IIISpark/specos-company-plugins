---
name: ispark-agent-tools
description: Use when creating, editing, installing, auditing, consolidating, or validating skills/plugins; coordinating subagents; maintaining agent memory/tooling; or managing ISpark skill distribution.
---

# ISpark Agent Tools

Use this for agent infrastructure and company skill maintenance.

## Route

- Skill authoring and validation: read `references/skill-authoring.md`.
- Distribution and profiles: read `references/distribution.md`.
- Subagents and context: read `references/subagents.md`.
- Optional agent tooling: read `references/optional-tooling.md`.

## Defaults

- Write company skill design notes, audits, and handoff docs in Simplified Chinese unless a manifest/schema field or public marketplace text requires another language.
- Put temporary migration notes under `working-delta/` or the governance repo's scoped audit path; use `.tmp/` or `tmp/` for generated validation output. Do not depend on Superpowers archive paths.
- Keep company skills self-contained.
- Do not rely on personal absolute paths.
- Do not overwrite private skills.
- Validate before publishing or syncing.
