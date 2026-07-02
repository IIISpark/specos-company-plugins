---
name: ispark-debugging
description: Use when investigating bugs, stack traces, failed tests, unexpected behavior, performance regressions, broken workflows, suspicious data drift, or unclear root cause before proposing a fix.
---

# ISpark Debugging

Debugging is evidence-first. Reproduce or localize the symptom before changing code.

## Route

- Root-cause loop: read `references/root-cause-loop.md`.
- Test failures: read `references/test-failures.md`.
- Performance or production-style regressions: read `references/performance.md`.

## Defaults

- Write investigation notes and user-facing reports in Simplified Chinese unless the target artifact explicitly requires another language.
- Put temporary repro notes, logs, traces, and scratch outputs under `working-delta/`, `.tmp/`, or `tmp/` according to repo convention; do not invent assistant-specific document folders.
- Anchor on the exact observed symptom, path, id, status, timestamp, or error.
- Compare intended contract against actual evidence.
- Instrument or inspect upstream before adding downstream tolerance.
- After 2-3 failed attempts, stop and report the evidence instead of looping.
