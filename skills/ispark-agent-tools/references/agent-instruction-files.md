# Agent Instruction Files

Maintain the smallest durable instruction surface. Inspect manifests, commands, docs,
CI, and existing instruction files before writing. Keep one authoritative file per
scope; do not maintain divergent `AGENTS.md` and `CLAUDE.md` copies. Use repo-relative
paths and exact commands, link to detailed docs instead of duplicating them, and omit
installed-skill inventories, generic quality slogans, and historical work logs.

Use a root file for repo-wide behavior and a nested file only when that subtree has a
real different command or boundary. Verify every referenced path and command. Keep
the file short enough to be injected on every task; move architecture, API, release,
and security detail into `docs/`.
