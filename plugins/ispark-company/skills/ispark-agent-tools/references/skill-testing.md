# Skill Behavior Testing

Use this for any skill whose rules can be rationalized away, especially TDD, review,
verification, privacy, release, or anti-slop guidance.

1. **RED**: construct at least three combined pressures, run the scenario without the
   skill, and record the exact shortcut, omission, or rationalization.
2. **GREEN**: add only the rule needed to block the observed failure; rerun the same
   scenario with the skill and verify the agent follows it while preserving the task.
3. **REFACTOR**: vary the wording and pressure, look for a new loophole, add a narrowly
   scoped counter-rule, and rerun until the rule remains clear without a giant checklist.
4. **Evidence**: keep scenario input, expected behavior, observed output, and unresolved
   risk under `working-delta/` or the repository's equivalent. Metadata, snapshots, and
   a passing static validator prove packaging only; they do not prove compliance.

Do not test authorship detection or detector evasion. For a pure reference skill with no
behavioral rule to violate, use reachability, example correctness, and negative-boundary
tests instead.
