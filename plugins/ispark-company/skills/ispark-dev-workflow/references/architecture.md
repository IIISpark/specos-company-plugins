# Architecture

Prefer existing project patterns over new abstractions. Add an abstraction only when it removes real complexity, reduces meaningful duplication, or matches an established local pattern.

Root-cause rule:

- Fix the fact source, contract, schema, generator, or upstream output when that is where the defect lives.
- Do not hide a contract failure with wrappers, permissive defaults, `any`, stringly parsing, or caller-side duplicated business rules.
- Temporary workarounds must be labeled with removal conditions and a follow-up owner.

For shared interfaces, database schema, auth, privacy, or deployment contracts: stop and ask before changing.

## Domain model and module depth

Keep three artifacts distinct:

- domain language defines business concepts and their relationships without encoding
  current implementation details
- an engineering spec defines desired behavior and acceptance
- an ADR records a consequential architecture decision and its tradeoffs

Challenge vague terms with concrete scenarios and cross-check them against both the
authoritative docs and code. Record an ADR sparingly; routine implementation choices do
not need permanent decision records.

When the task changes a business concept, relationship, lifecycle, or overloaded term,
switch into domain-modeling mode: update the repository's domain glossary (often
`CONTEXT.md`) and record the concrete scenario that resolved the ambiguity. Keep that
glossary free of implementation details, temporary notes, and delivery specs. Write an
ADR only when the decision is hard to reverse, surprising without context, and based on
a documented tradeoff. If any condition is absent, keep the decision in the working plan.

A module interface includes more than a type signature: callers may also depend on
invariants, ordering, error behavior, configuration, and performance characteristics.
Prefer a small, stable interface that hides meaningful complexity. Do not manufacture a
wrapper or shallow abstraction merely to make the directory tree look modular.
