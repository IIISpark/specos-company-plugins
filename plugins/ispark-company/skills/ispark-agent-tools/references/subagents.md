# Subagents And Context

Use subagents only when work can be separated cleanly:

- research
- POC
- independent docs
- independent tests
- isolated implementation slices

Do not parallelize tasks that modify the same shared files or adjacent core logic without a stable ownership boundary.

Before dispatching, assign each agent one bounded outcome, owned files or read-only
surface, prohibited side effects, and independent verification evidence. Prefer an
isolated branch or worktree for writers. One agent should own each shared contract and
each file; the primary agent retains architecture decisions and integration responsibility.

Use parallel agents when their results can be reviewed independently and parallelism
reduces elapsed time. Keep work serial when tasks depend on the same evolving facts,
when the merge cost exceeds the work, or when human review capacity is already the
bottleneck.

Do not accept an agent's completion message as proof. Inspect its diff or artifacts and
rerun the relevant check. For higher-risk changes, separate implementation review from
requirements/architecture review so one passing test suite does not answer both questions.

Check-ins should include:

- what changed
- what is next
- risks or blockers
- what is needed from the user
