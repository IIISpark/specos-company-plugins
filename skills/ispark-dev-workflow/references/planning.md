# Planning

Start non-trivial work by stating:

- Outcome: facts that should be true when done.
- Success criteria: tests, commands, page state, API response, or review result.
- Constraints: safety, compatibility, scope, style, dependencies, release boundary.
- Non-goals: what not to do in this pass.
- Stop rules: conditions that require pausing for user confirmation.

Use a written brief for complex agentic work:

- context: modules, owners, existing patterns
- integration notes: files and boundaries that must stay stable
- verification plan: commands and artifacts to check
- kill criteria: when to stop rather than keep investing

Do not over-specify implementation steps unless the sequence itself is a requirement or risk control.

## From requirements to an engineering spec

Synthesize the current conversation and local facts before asking questions. Separate:

- confirmed requirements and existing contracts
- assumptions that are safe and reversible
- open questions whose answers change architecture, public behavior, data, or release scope

When enough evidence exists, write the spec directly. Ask only for the smallest missing
decision when multiple reasonable interpretations would materially change the result.

A useful engineering spec states the problem, desired observable behavior, acceptance
criteria, important implementation decisions, testing decisions, and out-of-scope work.
Keep unstable file paths and code snippets in the implementation plan rather than the
durable product or domain spec.

Decompose complex work by independently verifiable behavior or contract boundary. Avoid
plans that are only lists of files to edit, and do not turn an issue tracker or planning
artifact into an authority that overrides repository facts.
