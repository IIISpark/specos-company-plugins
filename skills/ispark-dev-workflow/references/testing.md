# Testing

Use test scope proportional to risk.

- Bug fix: first add or identify a regression test that fails for the observed bug when feasible.
- Feature: test normal path, edge path, and important error path.
- Refactor: run focused tests around the touched boundary before broad tests.
- Frontend behavior: do not rely on code review only; use `ispark-browser-qa`.

When strict test-first is impractical, be explicit:

- why test-first is not the right fit
- what focused verification replaces it
- what residual risk remains

Avoid broad expensive test runs as the first move when a focused command can validate the touched surface.

