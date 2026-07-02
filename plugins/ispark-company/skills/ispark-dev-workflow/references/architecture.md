# Architecture

Prefer existing project patterns over new abstractions. Add an abstraction only when it removes real complexity, reduces meaningful duplication, or matches an established local pattern.

Root-cause rule:

- Fix the fact source, contract, schema, generator, or upstream output when that is where the defect lives.
- Do not hide a contract failure with wrappers, permissive defaults, `any`, stringly parsing, or caller-side duplicated business rules.
- Temporary workarounds must be labeled with removal conditions and a follow-up owner.

For shared interfaces, database schema, auth, privacy, or deployment contracts: stop and ask before changing.

