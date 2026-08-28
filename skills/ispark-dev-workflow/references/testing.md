# Testing

Use test scope proportional to risk.

## Testing process rules

For a skill or agent instruction that constrains behavior, test the process itself, not only its prose. Run a RED baseline without the instruction and record the agent's concrete failure or rationalization. Add the smallest rule that addresses it, run a GREEN pressure scenario with the instruction, then REFACTOR by closing new loopholes and re-running the scenario. Use at least three combined pressures when the rule trades speed for discipline, such as deadline, sunk cost, and incomplete evidence. Static metadata checks prove packaging, not behavioral compliance.

- Behavior change: default to a red-green-refactor loop. Add the smallest test that
  expresses one observable behavior, run it, and confirm that it fails for the intended
  reason before changing production code. Make the smallest implementation pass, then
  refactor only while the focused test remains green.
- Bug fix: first add or identify a regression test that fails for the observed bug when feasible.
- Feature: test normal path, edge path, and important error path.
- Refactor: run focused tests around the touched boundary before broad tests.
- Frontend behavior: do not rely on code review only; use `ispark-browser-qa`.

Do not count a test as useful merely because it failed. A setup error, stale fixture,
wrong assertion, or unrelated failure does not establish the intended red state. Prefer
testing public behavior and state transitions over mocks that only restate an
implementation.

When strict test-first is impractical, be explicit:

- why test-first is not the right fit
- what focused verification replaces it
- what residual risk remains

Common justified alternatives include documentation-only edits, generated artifacts,
configuration with a stronger deterministic validator, a throwaway prototype, or a
legacy boundary with no viable harness in the current scope. Existing implementation is
not by itself a reason to skip a regression test.

Avoid broad expensive test runs as the first move when a focused command can validate the touched surface.
