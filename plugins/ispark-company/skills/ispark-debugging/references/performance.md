# Performance

For performance regressions:

- establish baseline and current measurement using the same path
- separate cold start, cache, network, DB, browser, and provider effects
- avoid optimizing before identifying the dominant cost
- verify the changed path after the fix

For live systems, prefer read-only checks first. Do not mutate production just to gather evidence unless approved.

