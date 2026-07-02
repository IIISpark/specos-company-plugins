---
name: ispark-release-ops
description: Use when committing, pushing, creating PRs, shipping, deploying, rolling out, checking release health, updating changelogs, or promoting a change through dev and production.
---

# ISpark Release Ops

Use this for real branch closure and deployment work. Release claims need exact evidence.

## Route

- Branch closeout: read `references/branch-closeout.md`.
- Ship or deploy: read `references/deploy.md`.
- Health checks and smoke tests: read `references/health.md`.
- Long-running release checkpoints: read `references/checkpoints.md`.

## Defaults

- Write rollout notes, release summaries, and operator-facing reports in Simplified Chinese unless the repo release format explicitly requires another language.
- Put temporary rollout checklists and evidence bundles under `working-delta/`; raw logs and generated command output go under `.tmp/` or `tmp/`.
- Verify actual repo root before git commands.
- Do not push or deploy without clear user intent.
- Use immutable versions/tags where deployment is involved.
- Report commit, branch, artifact, rollout, and smoke result.
