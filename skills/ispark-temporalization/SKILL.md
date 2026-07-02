---
name: ispark-temporalization
description: Assess, initialize, refactor, and normalize Python modules into ISpark's Temporal-ready worker structure with canonical orchestration, explicit `config/contracts/services/infra/bootstrap/temporal` boundaries, layered tests, object-reference payloads, rollout safety, and synchronized docs/release-note updates. Use for Python workers, workflows, activities, queue naming, provider gateway audit/idempotency, object storage boundaries, and Temporal deployment readiness.
---

# Temporalization

## Overview

Use this skill to take a Python module through one of four jobs:

- assess an existing module or planned module before writing code
- initialize a new module skeleton
- refactor an existing local-only or partially platformized module
- normalize a drifted module back to the standard

The default target is:

- one canonical Temporal workflow/activity orchestration for distributed execution
- explicit `config / contracts / services / infra / bootstrap / temporal` layering
- SDK-free services and policy logic
- `infra/ports` plus concrete adapters for storage/model/metadata access
- `bootstrap` assembly for config loading, local run, healthcheck, and worker entry
- layered tests for local development and deployment safety
- container-friendly worker packaging with explicit rollout verification paths

Do not assume every module needs a second local orchestrator. Add one only when the module has a real non-Temporal product or research path that justifies it.
If the target repo declares both a central documentation tree and a template authority, treat both as hard review inputs rather than optional style references.

## Output And Path Defaults

- Write assessments, design notes, review findings, rollout notes, and user-facing reports in Simplified Chinese unless the target repo, publication channel, or user explicitly requires another language.
- Put temporary assessments, gap lists, design deltas, and audit notes under the repo's `working-delta/` when present.
- Put disposable generated output, raw logs, test exports, and one-off script results under `.tmp/` or `tmp/`.
- Promote only stabilized facts into `docs/`, repo-local README files, release notes, or contract documents.
- Do not write artifacts into Superpowers, hidden assistant, arbitrary home-directory, or personal archive paths.

## First Pass

Start by classifying the job as `assess`, `initialize`, `refactor`, or `normalize`; then read the narrow references for that job. Use `references/first-pass-routing.md` for the full reading order and template-selection map.

Before coding:

- inspect the target repo or module docs and current structure
- inspect any declared central docs tree and template authority
- write a short gap list
- identify public contract, storage, queue, and runtime risks
- for assessment/review/normalization work, use the standardized checklist in `references/review-checklist-and-output-template.md`
- for implementation or closing work, read `references/temporal-operating-rules.md`

## Detailed Operating Rules

Read `references/temporal-operating-rules.md` before coding, scaffolding, refactoring, normalizing, or closing a Temporalization task. It contains mode-specific procedure, cleanup/tree audit, non-negotiable architecture rules, and deliverables.

## References

- Read [references/task-modes.md](references/task-modes.md) for the four operating modes.
- Read [references/first-pass-routing.md](references/first-pass-routing.md) for the conditional reference and template map.
- Read [references/target-architecture.md](references/target-architecture.md) for the expected module shape.
- Read [references/source-of-truth.md](references/source-of-truth.md) to find the repo facts to inspect first.
- Read [references/questions-and-checkpoints.md](references/questions-and-checkpoints.md) before asking questions or closing a round.
- Read [references/review-checklist-and-output-template.md](references/review-checklist-and-output-template.md) to standardize review scope and report shape.
