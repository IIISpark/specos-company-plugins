# Verification And Handoff

Before claiming work is complete:

- map each material claim to the command, rendered state, response, or diff that proves it
- show the exact changed files or surfaces
- run fresh focused diagnostics/tests/typechecks and inspect their exit status and failure count
- mention any skipped verification and why
- self-review for hidden assumptions, blast radius, style drift, and unrelated changes
- compare the delivered result against the acceptance criteria, not only the test suite

For handoff:

- current goal and status
- decisions already made
- files changed
- verification already run
- remaining blockers and stop rules

Do not say "fixed", "complete", or "ready" without evidence from the current run.
An agent report, old command output, passing linter, or partial test is evidence only for
what it directly observed. Distinguish local correctness, design acceptance, demo
readiness, deployment readiness, and production authorization.
