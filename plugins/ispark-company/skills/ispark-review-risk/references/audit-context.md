# Audit Context Before Findings

Use this pass before vulnerability hunting, threat modeling, or a deep architecture
review of unfamiliar code. Its purpose is to establish what the system assumes,
guarantees, trusts, and changes. Do not name vulnerabilities, assign severity, or propose
fixes until this context pass is complete enough to support those claims.

Start from authoritative docs and externally reachable entry points. Map:

- identities, trust boundaries, privileged operations, and external dependencies
- important state, ownership, and lifecycle transitions
- validation and authorization points
- error, retry, rollback, and partial-failure behavior
- callers and callees that carry an invariant across a module boundary

For each critical function or handler, record evidence for:

- inputs and facts it assumes
- outputs and state changes it guarantees
- state and configuration it reads or writes
- external calls and their failure semantics
- constraints inherited from callers or imposed on callees
- unresolved questions and uninspected paths

Keep the dossier under `working-delta/`; raw extracts belong under `.tmp/` or `tmp/`.
Treat generated graphs and automated summaries as navigation aids, not semantic truth.
Once the context is sufficient, begin a separate findings pass so confirmed defects are
not mixed with preliminary suspicion.
