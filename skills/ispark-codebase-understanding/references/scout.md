# Bounded Codebase Scout

## Establish scope and authority

Restate the question the map must answer. Locate the workspace/repository root, nested
instruction files, authoritative design docs, build manifests, and the owner of the
target behavior. In a workspace of repositories, do not assume the outer root is the
implementation repository.

## Build the smallest useful map

Trace only the paths needed for the task:

1. top-level repositories or modules and their responsibilities
2. runtime, build, test, and deployment entry points relevant to the question
3. one or two critical request, event, state, or data flows from entry to side effect
4. public and internal interfaces, persistence, queues, external systems, and trust boundaries
5. existing tests, fixtures, observability, and commands that can verify a future change
6. ownership conflicts, stale documents, generated files, and unresolved facts

Use search and static tooling as navigation aids. Validate important relationships by
reading the referenced code and tests. A generated dependency graph, AI summary, or
directory name is not proof of runtime semantics.

## Deliverable

Report:

- scope and authoritative sources
- concise system/module map
- critical execution or data flow
- likely change surface and boundaries that must remain stable
- verification entry points
- open questions and the next smallest read or probe

Avoid narrating every file. Do not modify production code during a scout unless the user
also authorized implementation and the ownership boundary is already clear.
