# Questions and Checkpoints

## 1. Questions to Ask Early

Ask targeted questions when any of these are unclear:

- what the module produces for the product, not just what the code currently does
- which stages are truly in scope for the first platformized version
- whether the repo wants generic methodology in a skill and only project facts in local docs
- which resources are stable product resources versus flexible documents or ephemeral run artifacts
- what the repo's bundle/object governance rules are:
  - package root
  - `sections/` vs `audit/`
  - `_ephemeral/...`
  - local tmp cleanup
- whether a public contract, config shape, queue name, or storage shape is already depended on
- whether a second local orchestrator is truly needed
- whether activity execution should stay sync, become async, or be split by task type
- whether the module needs Signal / Query / Update handlers, and what their concurrency and state-safety rules are
- whether multiple workflows can concurrently mutate the same logical key, and if so what the shared-key coordination model is
- whether deployment safety requires replay gates, worker versioning, or explicit `Pinned` vs `Auto-Upgrade` strategy
- whether the module needs schedule-driven execution and how pause/backfill/update should behave
- whether the module is expected to be containerized and, if so, what the repo-standard Docker/Kubernetes shape already is
- whether workflow/activity DTOs already have version fields and what the backward-compatibility window is

## 2. Questions to Ask During Refactor

Ask before changing:

- public CLI names
- public API shapes
- task queue names already used by deployment
- config keys already referenced by tooling
- storage layout that downstream systems already read
- whether the repo has a declared template authority that this module is expected to match exactly
- whether a workflow history or replay gate is already relied on for deployment safety
- whether public workflows or child workflows set run/execution timeouts, and if so whether those values are real business guardrails or accidental wrappers around normal long-tail execution
- whether any activity timeout is covering provider queue time, long polling, multi-shard batch work, or overall business wait instead of one retryable attempt
- whether provider/model SDK and HTTP clients avoid hidden retries and generation-time timeouts, leaving retry/wait ownership to Temporal activity retry and activity attempt timeout
- whether a proposed parallel fan-out needs windowed release and whether any shared-key mutation lane must serialize across workflows
- whether observability must be wired through client/worker interceptors
- whether large payload handling should stay ref-first or use Temporal external storage for a subset of payloads
- whether payload customization belongs in a Data Converter / Codec / Encryption layer instead of service code
- whether the repo explicitly wants Nexus, or whether normal workflow/activity/module boundaries remain the default
- whether the module needs a repo-standard Dockerfile, healthcheck path, `run/verify` entry pair, or Kubernetes deployment manifest updates
- whether a proposed workflow/activity input or output change is additive or actually a breaking contract change
- whether a breaking contract should become a new workflow/activity name instead of an in-place mutation
- whether a read-only container runtime also has explicit scratch mounts for `/tmp` or cache paths, instead of relying on accidental filesystem writes
- whether the runtime install path copies a wheelhouse into final image layers when a BuildKit cross-stage mount would keep the image materially smaller

## 3. Incremental Checkpoints

After each meaningful layer:

1. verify tests and type checks
2. inspect package re-export surfaces, docs, and the active source tree
3. update root `TODO.md`
4. add a release note for a meaningful round

Do not defer all verification to the end.

## 4. Closing Checklist

Before considering the round complete:

- core services remain SDK-free
- workflow code is thin and deterministic
- signal/query/update boundaries are intentional where message handlers exist
- worker kind and default queue are frozen
- layered tests exist or explicit gaps are documented
- replay/verify strategy exists for worker rollout
- workflow-code versioning and DTO-schema versioning are both explicitly addressed
- timeout / wait boundaries are explicitly addressed: no narrow workflow run timeout by default, no activity-held provider wait, client timeout classified below activity attempt timeout, and long waits expressed by durable workflow timers
- deployment shape is explicit when the module is containerized
- cleanup/tree-audit has been performed for the active source tree
- stale wrappers, empty shells, misplaced modules, and misleading package re-export surfaces are either removed or explicitly justified
- local tmp and cloud `_ephemeral` cleanup responsibility is explicit and not left to chance
- README and module docs match the new structure
- root `TODO.md` is current
- a release entry exists if the round was meaningful
- repo-local fact docs are updated when project-specific Temporal facts changed
