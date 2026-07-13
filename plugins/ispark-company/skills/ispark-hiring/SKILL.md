---
name: ispark-hiring
description: Use when Codex needs to define hiring context or roles, build evidence rubrics, screen candidate batches, prepare candidate-specific interview runbooks, analyze interview records or transcripts, draft post-interview evaluations and human decision records, or review hiring-process quality.
---

# ISpark Hiring

Use this skill to run an evidence-based hiring loop from organizational need through human-owned decision and process review.

## Required Reference

Read `references/hiring-loop.md` before creating, comparing, or evaluating any hiring artifact. It contains the canonical state machine, evidence rules, privacy boundaries, templates, and stop conditions.

## Workflow

1. Identify the current hiring state and the human owners for the role and HR process.
2. Confirm the authorized sources, current Role Brief version, and current Evidence Rubric version.
3. If an upstream artifact is missing, list the missing fields and stop before ranking or evaluating people.
4. Use the matching canonical template for the current state.
5. Separate verified fact, candidate claim, Agent inference, counterevidence, and `Unknown`.
6. Map every material judgment back to a predefined role dimension and a locatable source.
7. Return the next gate, human owner, unresolved risks, and any action that requires authorization.

## Hard Boundaries

- Keep final hiring, rejection, compensation, background-check, candidate-contact, and publication decisions human-owned.
- Do not infer ability or stability from protected, sensitive, or job-irrelevant personal traits or proxies.
- Do not upload candidate PII, resumes, interview transcripts, or private evaluations to unauthorized external tools.
- Do not copy private founder notes or candidate dossiers into company methodology.
- Do not treat missing evidence as a low score; preserve `Unknown` explicitly.
- Do not change the rubric for one candidate without versioning it and rechecking the affected batch.
- Stop when source permissions, role constraints, decision authority, or material facts are unclear.

## Output And Artifact Rules

- Write company-facing artifacts in Simplified Chinese unless the target team or channel requires another language.
- Lead with the current fact and recommended next gate, then show supporting evidence.
- Store durable artifacts in the authorized hiring or team documentation space.
- Put temporary extraction, draft, and analysis files under `working-delta/`, `.tmp/`, or `tmp/`; never make them the candidate fact source.
- Keep raw candidate materials separate from generated analysis and reference them through a controlled source index.
