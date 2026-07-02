# Source of Truth

## Read Order

When starting a temporalization task, inspect these sources first if they exist:

1. central/system documentation tree and cross-repo specs
2. declared template authority or repo-surface template
3. repo-level architecture or platform overview docs
4. repo-level project-fact docs for Temporal/runtime/storage
5. target module README and module-specific design docs
6. current config, CLI, worker entry, tests, and deployment files
7. repo TODO / release-note conventions

## What to Find

Build a short fact list before refactoring:

- the module's product role
- whether the repo already declares a central docs tree and a template authority
- current local entrypoints
- whether the repo keeps generic guidance in a skill and project facts in local docs
- current public contracts
- current config keys
- current config layering:
  - worker static config
  - public workflow options
  - internal execution strategy
- current storage split
- current object layout rules:
  - canonical package root
  - package `sections/` vs `audit/`
  - `_ephemeral/...` tmp/staging shape
  - ref/path semantics such as `path_segments`
- existing workflow, activity, queue, and worker naming
- existing test layers and gaps
- existing Dockerfile, healthcheck path, and deployment manifests if the module is already containerized

## If the Repo Has No Local Temporal Docs

If the target repo does not have platform or Temporal fact docs:

- inspect the README, docs, and current module layout
- reconstruct the missing facts from code and tests
- write a short design note before doing a large refactor

## Existing Docs Beat Assumptions

If repo docs, code, and deployment files disagree:

- treat the conflict as an explicit finding
- do not guess silently
- ask targeted questions before changing public contracts

If the repo declares a central docs tree or capability/spec authority:

- treat that declared authority as higher precedence than drifted repo-local prose
- record repo-local drift as a finding instead of silently averaging the two stories
