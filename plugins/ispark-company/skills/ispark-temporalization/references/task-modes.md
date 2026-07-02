# Task Modes

## 0. Assess

Use this when the module already exists or is planned, but the immediate goal is analysis rather than code changes.

Output:

- current-shape assessment
- target-shape recommendation
- `config/contracts/services/infra/bootstrap/temporal` boundary proposal
- risk list and rollout suggestion

Use this before large refactors, when repo docs and code disagree, or when the user explicitly wants research and design first.

## 1. Initialize

Use this when the module does not exist yet or only has a rough algorithm idea.

Output:

- initial product role
- initial workflow/activity split
- `config / contracts / services / infra / bootstrap / temporal` skeleton
- default worker kind and task queue plan
- starter docs and starter tests

Keep the first version small. Do not prebuild every future queue, deployment split, or optional local orchestrator.

When bootstrapping a new Python repo surface, also start from the generic skill templates for:

- `pyproject.toml`
- `.gitignore`
- annotated GitHub Actions CI workflow
- annotated GitHub Actions CodeQL workflow
- annotated GitHub Actions worker-image publish workflow

And apply them in the repo-bootstrap order:

- repo surface
- runtime entry
- code structure
- CI verification
- image publishing
- deployment
- rollout verification

## 2. Refactor

Use this when the module already runs locally, even if unstable.

Primary goal:

- keep the real algorithm path alive
- clean obvious structural debt
- extract the core
- move storage/model/metadata concerns behind ports
- add Temporal-facing structure without forcing cloud-only development
- add the standard five test layers

Typical order:

1. audit current entrypoints, compat layers, and runtime coupling
2. remove duplicated or misleading orchestration when safe
3. extract shared services and policies
4. define `infra/ports`, adapters, and `bootstrap` assembly
5. add workflow/activity builders and worker entry
6. add layered tests
7. add an optional local orchestrator only if there is a real non-Temporal need
8. do a cleanup/tree-audit pass to remove stale wrappers, empty shells, misplaced modules, and misleading re-export surfaces

## 3. Normalize

Use this when the module already follows the standard but later changes drifted.

Primary goal:

- restore naming consistency
- restore deterministic workflow boundaries
- restore test layering and verification
- remove stale dual-entry assumptions

Common drift patterns:

- queue names renamed ad hoc
- workflow code grows business logic or IO
- one task has adapters but the others do not
- worker entry exists but verify/replay/docs lag behind
- core service starts depending on `temporalio`
- storage or provider details leak back into core logic

Treat this as targeted repair, not a fresh rewrite.

Closing expectation:

- normalization is not complete until the module tree has been re-audited for stale wrappers, empty shells, misplaced modules, and misleading package re-export surfaces
- normalization should also check whether the repo-surface files such as `pyproject.toml` and `.gitignore` still match the standardized Temporal module baseline
- normalization should also check whether repo-standard CI/CD workflows still separate test, security, and build concerns cleanly
- normalization should also check whether worker-image publishing remains explicit, reproducible, and aligned with the repo-standard Dockerfile and registry policy
