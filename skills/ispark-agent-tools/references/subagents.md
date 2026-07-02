# Subagents And Context

Use subagents only when work can be separated cleanly:

- research
- POC
- independent docs
- independent tests
- isolated implementation slices

Do not parallelize tasks that modify the same shared files or adjacent core logic without a stable ownership boundary.

Check-ins should include:

- what changed
- what is next
- risks or blockers
- what is needed from the user

