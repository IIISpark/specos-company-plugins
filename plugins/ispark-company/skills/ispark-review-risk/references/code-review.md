# Code Review

Prioritize:

- behavioral regressions
- contract/schema/API drift
- missing tests on changed behavior
- security and privacy boundaries
- data loss or migration risk
- deployment or rollback blind spots
- unnecessary abstraction or unrelated refactor

Format:

1. Findings with severity and evidence.
2. Open questions or assumptions.
3. Brief summary only after findings.

If no issues are found, say so and name the remaining test gaps.

After correctness and risk, perform a bounded clarity pass over recently changed code.
Preserve behavior exactly, follow repository conventions, and simplify only where the
diff introduced avoidable indirection, nested control flow, duplicated rules, or a
premature abstraction. Do not turn review into unrelated cleanup, and do not prefer
shorter code when it hides state, errors, or intent.

## Generated-code and over-defensive patterns

When a diff is described as "AI 味" or feels larger than the requirement, inspect for speculative null checks, `|| []`/`|| {}` defaults, swallowed exceptions, unbounded or duplicate retries, silent fallbacks, compatibility branches, wrappers, copied validation, and premature abstractions. These are review signals, not automatic defects.

For every new branch, require one concrete basis: a reproduced failure, a documented contract, a security or data boundary, an existing architecture rule, or a focused test. Check that the branch preserves failure visibility and does not change required-state semantics. Valid input validation, authorization, schema checks, explicit timeouts, bounded recoverable retries, transactions, cleanup, and fail-closed behavior remain good engineering.

Findings should identify the earliest incorrect state and the smallest correction. Do not recommend a downstream default merely because it makes a page or test look successful. If evidence is insufficient, record the uncertainty rather than approving a hypothetical safeguard.

## Diff and attack-surface pass

For a security or public-contract review, enumerate changed inputs, database queries,
authentication and authorization checks, session/state transitions, external calls,
cryptographic operations, and error/logging paths. Check each changed boundary for
injection, XSS, CSRF, IDOR, race/TOCTOU, information disclosure, DoS/resource limits,
business-logic violations, and secret leakage. Confirm suspected issues against callers,
callees, existing tests, and neighboring implementations before assigning severity.

For a differential or variant review, search for equivalent handlers, adapters, and
error branches outside the diff. Compare their invariants and failure behavior. A
missing check is a finding only when the changed path can actually reach the boundary;
an extra check is not a defect merely because it is unfamiliar.
