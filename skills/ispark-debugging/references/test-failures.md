# Test Failures

For a failing test:

- run the smallest failing command first
- read the failure message and assertion site
- inspect fixtures and setup before changing production code
- identify whether the test, code, environment, or contract is stale

Do not "fix" by weakening assertions unless the expected behavior changed and the new contract is documented.

When a test suite is noisy:

- isolate the changed surface
- record unrelated failures separately
- avoid claiming repo-wide health if only focused tests passed

