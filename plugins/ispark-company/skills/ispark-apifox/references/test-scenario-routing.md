# Apifox Test Scenarios

Use this reference for multi-step workflows, imported endpoint/case steps, scenario references,
conditions, loops, waits, scripts, databases, variables, assertions, and cleanup.

## Model Before Writing

1. Define the business goal, success condition, failure behavior, and cleanup.
2. Confirm project, branch, environment, endpoints, cases, data, and external dependencies.
3. Read a similar scenario and current create/update schemas when available.
4. Draft a small step graph with each step's input, output, dependency, assertion, error policy, and
   cleanup before producing JSON.

Scenario creation may save metadata without steps. Do not call an empty scenario complete. Prefer the
CLI's high-level step import or scenario-reference commands over hand-written binding internals. Imported
steps and referenced scenarios have different synchronization semantics; confirm which the user wants.

## Data And Structure

- Base cross-step references on observed response paths and stable step numbers. Recheck every reference
  after inserting, deleting, or reordering steps.
- Preserve runtime placeholders exactly. In scripts, use the runtime's supported variable API rather
  than embedding unresolved template syntax.
- Use containers for nested conditions and loops; keep children nested and set explicit loop bounds,
  wait limits, and failure behavior. Do not assume list ordering when selecting an element.
- Use current schemas for processors, assertions, scripts, delays, custom HTTP steps, and scenario refs.
  Do not guess field names or copy backend-generated relation IDs from another scenario.
- Prefer visual assertions and existing endpoint contract checks. Add business assertions only where
  they add distinct coverage; custom scripts are a last resort.

## Side Effects And Verification

- Database, external-program, and write-endpoint steps require a known non-production environment and
  explicit execution authorization. Include cleanup that can still run after a main-path failure.
- Before update, retrieve the complete scenario with case detail. Validate, confirm, update once, then
  read back the full step tree and bound HTTP details.
- Readback and schema validation do not prove runnability or client rendering. Run only when requested
  or necessary for approved delivery, then inspect step-level report failures.
- Do not repeatedly overwrite a business scenario while debugging. Use a clearly scoped temporary or
  versioned scenario when isolation is necessary and obtain confirmation before creating it.
