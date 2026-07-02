# Target Architecture

## 1. Core Shape

Aim for a single canonical Temporal orchestration with an SDK-free services layer and explicit six-block module boundaries.

```text
module/
  Dockerfile
  deploy/
    deployment.yaml
  src/<module>/
    __main__.py
    cli.py
    config/
      __init__.py
      models.py
      loaders.py
    contracts/
      __init__.py
      refs.py
      package.py
      workflow_io.py
    services/
      __init__.py
      package_builder.py
    infra/
      __init__.py
      ports/
        __init__.py
      adapters/
        __init__.py
    bootstrap/
      __init__.py
      context.py
      assembly.py
      local_request.py
      local_run.py
      healthcheck.py
      worker_entry.py
    temporal/
      __init__.py
      names.py
      worker_main.py
      verify.py
      workflows/
        __init__.py
        run.py
      activities/
        __init__.py
        build_package.py
  tests/
    support/
    unit/
    activity/
    workflow/
    replay/
    e2e/
```

Interpretation:

- `cli.py` owns the single canonical command surface
- `config/` owns static worker/runtime configuration only
- `contracts/` owns structured module I/O and ref envelopes
- `services/` owns SDK-free business logic
- `infra/` owns concrete ports and adapters
- `bootstrap/` assembles config, local run, healthcheck, and worker startup
- `temporal/` owns workflows, activities, worker runtime entry, and verification
- `tests/` are intentionally layered by execution boundary
- `Dockerfile` and `deploy/` express the operational contract when the module is containerized
- the skill ships generic container and Kubernetes templates under `templates/` that can be adapted per repo
- package-level `__init__.py` files should default to docstring-only package markers rather than re-exporting symbols
- when the target repo declares a template authority, this six-block tree should be matched as exactly as practical, not only approximately

## 2. Core Rules

- Keep core services free of direct `temporalio` imports.
- Keep cloud details out of task logic.
- Prefer `bootstrap` assembly plus `infra/ports` over direct SDK calls or hidden package aggregators.
- Do not make the whole core async by default.
- Prefer Pydantic for config models and public workflow/package DTOs instead of loose dicts or lightly typed dataclasses.
- Prefer `pathlib.Path` for local/logical path values that cross storage seams; stringify only at the adapter boundary.

## 3. Workflow Rules

- Workflows stay thin and deterministic.
- Workflow code only orchestrates ordering, retries, branching, signals, and state progression.
- No direct network/file/database IO inside workflows.
- No regular `random`, `uuid.uuid4()`, `datetime.now()`, `time.time()`, threads, or processes inside workflows.
- `Query` handlers stay read-only and synchronous.
- `Update` handlers are for acknowledged state changes.
- `Signal` handlers are for unacknowledged state changes.
- For module public workflow surfaces, prefer `signal + query` as the default outward progress contract and do not expose public `update` unless the module has an explicitly frozen synchronous control action.
- If multiple handlers can mutate shared workflow state, coordinate them explicitly.

## 4. Activity Rules

- Use activities for side effects, external IO, and durable execution boundaries.
- Split activity boundaries by retry value, side-effect/resource profile, and scheduling value; for LLM/provider/model work, prefer one logical provider call or a bounded homogeneous shard per activity.
- Do not hide a batch of unrelated or long-tail LLM/provider calls inside one coarse stage activity. If the calls can fail, retry, timeout, rate-limit, or consume capacity independently, model that independence at activity or shard level.
- Do not put provider/model retry or generation-time timeout policy inside SDK/HTTP clients or service helpers. Disable SDK/client retries by default, avoid narrow request timeouts, and let Temporal activity retry plus activity attempt timeout be the observable boundary.
- Async activities are preferred for high-concurrency IO when the dependency stack supports async well.
- Sync activities are acceptable for sync-only SDKs or low-concurrency tasks.
- CPU-heavy work should not block an async event loop; isolate it by execution model, worker pool, or service boundary when needed.

## 4.1 Parallel Release Rules

- For large parallelizable workloads, prefer windowed fan-out / bounded in-flight release from the workflow.
- Avoid both extremes:
  - do not treat a tiny hardcoded workflow concurrency cap as the final scaling model
  - do not enqueue the entire backlog at once if it can be released gradually
- Let workflows declare dependency and parallelism shape. Let worker capacity absorb throughput.
- Treat the release window as a configurable strategy parameter.
- Use worker topology, replicas, poller autoscaling, task slots, provider-gateway capacity, and activity-level rate limits as the main throughput controls.
- Only add more adaptive feedback loops when measured queue delay, worker saturation, or provider pressure show that a static window is no longer adequate.
- Commit or stage successful targets/shards durably as they complete. Reruns should skip already successful targets, and one failed shard should not cancel or roll back unrelated siblings.

## 4.1.1 Worker Topology and Scaling Rules

- Default to one image with multiple Deployments or commands when dependency and resource profiles are compatible.
- Split images only when dependency, runtime package, security, node placement, GPU, or heavy system resource profiles differ materially.
- Prefer one worker role per Deployment in production-like environments. A worker role should have a coherent queue, resource, probe, and scaling stance.
- Workflow queues are governance, compatibility, and replay boundaries; do not use them as CPU/GPU/IO capacity labels.
- Activity queues may split by resource profile, side-effect boundary, provider domain, DB/backing-store limit, or failure domain.
- A combined worker is acceptable for local/dev/bootstrap mode. Split workflow and activity roles when side effects, heavy work, provider limits, or resource pressure can block workflow polling.
- Do not default to one workflow per Pod. The normal production shape is one worker role per Deployment.
- Model capacity explicitly:
  - workflow slots handle deterministic Workflow Task throughput
  - activity slots handle side-effect/IO/CPU concurrency
  - pollers handle task ingestion from task queues
  - replicas handle horizontal fleet size
  - task queue, provider, and backing-store rate limits protect shared systems
- Treat provider quota as dynamic capacity. Static worker config may name the provider domain / model family, but should not require per-upstream `max_concurrency`; live concurrency/rate/budget should be inferred by provider-gateway runtime feedback and exposed through provider-gateway metrics or a capacity control plane when available.
- Obey project DB boundaries. In DramaWork, algo workers do not access DB; `activity-state` in algo means package/manifest/registry/object-store state, while business workflow/worker owns business DB writes.
- Tune in order: fan-out window, worker slots/executor, poller behavior, rate limits, replicas/autoscaler, then adaptive feedback loops.
- Do not mix WorkerTuner/resource-based slot suppliers with legacy `max_concurrent_*` style limits in the same worker.
- Do not raise activity slots or replicas without checking provider/backing-store pressure.
- Classify activities by boundary, not by module. For video generation, provider submission/polling is usually IO-bound, while download/decode/transcode/upload after success is heavy CPU+IO; video evaluation may follow the same pattern.

## 4.2 Shared-Key Mutation Rules

- If multiple workflows can update the same logical key, do not assume per-workflow ordering is enough.
- Prefer a keyed coordinator/entity-workflow style coordination point when the same key must be serialized across workflows.
- Keep the coordination key as small and stable as possible, for example a canonical family key before introducing finer-grained locks.
- Different keys should stay parallel; only the same key should serialize.
- Treat database or cache locks as adapter-level fallback mechanisms, not as the primary orchestration design.

## 5. Testing Rules

Use all five layers:

- `unit`: core services, policies, domain logic
- `activity`: `ActivityEnvironment`
- `workflow`: `WorkflowEnvironment.start_time_skipping()`
- `replay`: replay existing histories before rollout
- `e2e`: `WorkflowEnvironment.start_local()` or local Temporal dev server smoke tests

## 5.1 Deployment Safety Rules

- Keep a replay path for representative histories.
- Prefer worker processes that support both `run` and `verify` style execution.
- If the repo uses worker versioning, explicitly record whether workflows are expected to be `Pinned` or `Auto-Upgrade`.

## 6. Data and Contract Rules

Use:

- `document ref`
- `artifact ref`

Do not pass large JSON or binary payloads through workflow history by default.
Treat refs as structured envelope objects, not raw strings or bare S3 keys.
Default ref/path envelopes to structured fields, including `path_segments: list[str]` for logical member paths, instead of raw slash-joined strings.
Default package refs to the bundle-root `package.json`.
Within a package, prefer relative member references; only include full root identity for cross-bundle references.

Temporal external storage can be used selectively for large payloads, but ref-first design is still the default architectural choice.

Treat configuration as three separate layers:

- worker static config
  - mounted or injected at runtime
  - for endpoints, credentials, default routing, and worker/process settings
- public workflow options
  - light, enumerated caller controls such as `model_name`, `backend_profile`, `dry_run`, or range selection
- internal execution strategy
  - retry, timeout, batching, fan-out windows, and provider rate-limit handling

Do not expose worker/static environment config through a public `config ref`.
If a module persists immutable run-preparation metadata, keep that as an internal module artifact unless it is intentionally promoted to a stable business object.
Make `progress_target_workflow_id` mandatory on every module public workflow input so upward progress communication can be added later without breaking the public contract.
For outward progress signals, keep progress event identity separate from Temporal execution identity:
- `event_id` is a scoped idempotency key in the run / target / attempt context, not a workflow execution identity.
- In DramaWork-compatible modules, outward progress `event_id` must be stable and `<= 64` characters.
- Do not include full `workflow_id`, `source_workflow_id`, Temporal run ID, object-store key, long request namespace, provider payload field, current time, or random value in `event_id`.
- Put full execution identity in dedicated fields such as `workflow_id`, `source_workflow_id`, `temporal_workflow_id`, `temporal_run_id`, execution context, or correlation links.
- Progress emitters need production-shaped workflow ID tests that prove `event_id` stays short and does not embed the full execution identity.
Do not keep generic `summary_ref / component_refs` as default public outputs; only expose explicitly named stable refs that downstream modules truly consume.
If the authoritative main `document ref` already carries `project_id` or equivalent scope, do not repeat that same scope field again in the module public input unless the caller is using an explicit-ID fallback path.
Treat `manifest/index` as explicitly named embedded package sections, not a third ref kind or a default parallel public output.
When a stage produces a high-cardinality set, expose a single `package_ref` and embed named `manifest/index` sections inside the package JSON rather than emitting a large child-ref array or parallel manifest refs through workflow I/O.
Allow the business layer to create staging/adaptor packages between modules; do not force a downstream module to always consume the raw upstream package shape.
Treat downstream stage inputs as stable snapshots/hard copies by default so later downstream edits do not silently mutate upstream canonical products.
The main exception is globally shared canonical resources such as asset registries and asset artifacts, which may continue to be referenced live across stages.
Classify persisted objects into only two lifecycle classes:
- `durable` for canonical truth and retained audit members
- `ephemeral` for staging/tmp/debug/rebuildable intermediates
Within durable package roots, distinguish canonical `sections/` from retained audit `audit/`.
Prefer a reserved ephemeral prefix such as `_ephemeral/{data_type}/...` instead of mixing temporary objects into canonical roots.
Do not make each module invent its own orphan-scan or GC flow; platform-level reachability scan and delayed cleanup should own that.
If an ephemeral staging object exists only to satisfy one downstream call and has no audit/reuse value, let the creating business workflow clean it up after the call completes instead of promoting it to a durable object.
For local worker scratch, define an explicit tmp root and janitor/cleanup path instead of relying on process exit.

## 6.0 Schema-Evolution Rules

- Treat workflow-code evolution and DTO-schema evolution as separate concerns.
- Use replay, Worker Versioning, and patching for workflow-code changes that change scheduling order, branching, activity names, child workflow IDs, durable state transitions, or otherwise risk nondeterminism.
- Use explicit compatibility policy for workflow/activity inputs and outputs.
- Default DTO evolution to additive, backward-compatible change:
  - new optional fields with defaults are preferred
  - field removal, field rename, or semantic redefinition should be treated as breaking
- Keep readers more compatible than writers during rollout.
- Prefer explicit DTO version fields such as `schema_version`, and add `content_version` when payload meaning can evolve independently from shape.
- Introduce a new workflow name or activity name instead of mutating the existing contract in place when:
  - the semantic meaning of inputs or outputs changes materially
  - retry or timeout meaning changes materially
  - side-effect timing or durability meaning changes materially
  - old runs would keep emitting payloads that the new handler cannot safely interpret
  - an internal activity DTO change changes retry value, side-effect boundary, resource profile, or result shape rather than only adding compatible optional fields

## 6.1 Observability Rules

- Keep tracing/logging/metrics wiring outside core business logic.
- If the repo adopts Temporal interceptors, keep them in client/worker bootstrap layers rather than in service code.
- Keep progress/observability split explicit:
  - outward business-facing milestones go through workflow `signal/query`
  - long activity liveness and fine-grained execution stay in `heartbeat + structured logs`
  - do not assume heartbeat alone is a sufficient business-facing progress surface
- Give every provider/LLM logical call or bounded shard a locatable observability identity: target ID, activity name, attempt/shard index, provider request ID or operation ID when available, and trace context.
- Do not expose provider-call noise as public progress. Public progress should stay business-meaningful; provider request IDs and shard attempts belong in logs, metrics, traces, audit packages, or internal diagnostics.

## 6.2 Schedule and Payload-Customization Rules

- If the module needs recurring execution, prefer Temporal Schedules and define pause/backfill/update semantics explicitly.
- Keep payload transformation concerns in Data Converter / Payload Codec / Payload Encryption layers, not in service logic.

## 6.3 Debugging and Advanced-Integration Rules

- Keep replay and history inspection as the primary debugging path for nondeterminism and rollout regressions.
- Do not introduce Nexus as a default module boundary unless the repo has explicitly chosen it.

## 6.4 Containerization and Deployment Rules

- Treat worker containerization as part of the target architecture once the module is intended to run outside a developer laptop.
- Prefer pinned multi-stage builds.
- When BuildKit is available, prefer cross-stage mounts for wheelhouse/lockfile installation so builder artifacts do not become permanent runtime layers.
- Keep runtime images minimal, non-root, and long-lived-process friendly.
- Keep configuration, TLS material, and secrets external to the image.
- Prefer a real healthcheck command that can be reused by Docker and Kubernetes probes.
- Keep `run` and `verify` style entrypaths available when rollout safety depends on replay or validation gates.
- If the repo is Kubernetes-first, treat Deployment shape, probes, security context, and resource settings as part of the module contract rather than ad hoc ops glue.
- If the runtime uses read-only root filesystems, define the minimal writable scratch surface explicitly, for example `/tmp` and cache mounts, instead of silently depending on rootfs writes.

## 7. Local-Orchestrator Rule

Do not add `local_pipeline.py` by default.

Only add a dedicated local orchestrator when:

- the module must run outside Temporal as a real product or research path
- benchmark or offline dataset workflows need a sustained non-Temporal orchestration surface
- there is an explicit non-Temporal caller that should remain first-class
