# Documentation

Use docs for durable facts:

- architecture and decisions
- API or workflow contracts
- operator procedures
- release notes
- module usage and examples

Keep index docs short. Move details to scoped documents. Do not write achievement logs into index files.

When changing behavior, update nearby docs and release notes if users, operators, or future agents need that fact.

Language and path defaults:

- Write company-facing docs, PRDs, reports, release notes, and issue plans in Simplified Chinese unless the user, repo, or publication channel requires another language.
- Use `working-delta/` for temporary audits, plans, draft decisions, and migration notes.
- Use `.tmp/` or `tmp/` for disposable generated files, logs, screenshots, exports, or command output.
- Promote only stabilized facts into `docs/`, README, release notes, or other durable fact sources.
- Do not write documents into Superpowers, hidden assistant, arbitrary home-directory, or personal archive paths.
