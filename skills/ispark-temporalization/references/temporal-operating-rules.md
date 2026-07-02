# Temporal Operating Rules

## Mode Selection

### Assess

Use this mode when the immediate need is to evaluate a module, freeze boundaries, compare against Temporal guidance, or propose the next safe change set without coding yet.

Do this:

1. identify the module role, current entrypoints, and current contracts
2. compare the current shape with the target architecture and official Temporal guidance
3. freeze recommended `config/contracts/services/infra/bootstrap/temporal` boundaries plus workflow/activity/test seams
4. produce a gap list, risk list, and suggested next sequence
5. avoid speculative scaffolding unless the user explicitly wants it
6. structure the assessment with the standardized sections from `references/review-checklist-and-output-template.md`

### Initialize

Use this mode when the module does not exist yet or only exists as an idea.

Do this:

1. define the module role in the product chain
2. freeze initial workflow, activity, worker kind, and default queue boundaries
3. scaffold `config / contracts / services / infra / bootstrap / temporal` and the test layers
4. document the local development path and the verification path
5. keep the first version small; do not prebuild every future queue, profile, or deployment split

### Refactor

Use this mode when the module already runs locally, even if messy or tightly coupled to local files.

Do this:

1. audit current entrypoints, compat layers, and runtime coupling
2. identify the real stable core
3. remove duplicated orchestration or misleading structure when safe
4. extract `infra/ports`, adapters, and shared services
5. add or clean the `bootstrap` and Temporal-facing workflow/activity/worker layers
6. formalize the five test layers
7. keep local development ergonomic without inventing a second orchestrator unless it is justified
8. run an explicit cleanup/tree-audit pass before calling the refactor structurally done
9. explicitly review repo surface, architecture surface, and module contract surface against the standardized checklist before closing the round

### Normalize

Use this mode when the module already follows the pattern but later edits made it drift.

Do this:

1. diff the current module against the target architecture
2. fix drift incrementally instead of rewriting
3. restore queue naming, worker entry, test layering, direct-import surfaces, and docs
4. remove stale dual-entry assumptions unless the module still has a justified local-only orchestration path
5. run an explicit cleanup/tree-audit pass before calling the module normalized
6. explicitly review repo surface, architecture surface, and module contract surface against the standardized checklist before closing the round

## Cleanup / Tree Audit

Before closing a meaningful refactor or normalize round, do a cleanup/tree-audit pass:

1. remove runtime caches and irrelevant generated residue when safe, for example `__pycache__`
2. print or inspect the active source tree, not just individual edited files
3. classify suspicious items into:
   - delete
   - keep but rename/reposition
   - keep and materialize instead of leaving as an empty shell
4. explicitly look for:
  - low-value re-export layers, especially `__init__.py` package aggregators
   - misplaced modules
   - empty directories or empty shells
   - compat wrappers that no longer serve a real contract
   - misleading names that still say compatibility when they are now stable surfaces
   - partially decoupled adapters that still leak old storage/provider semantics
5. after cleanup, rerun tests, type checks, export checks, and doc synchronization

## Non-Negotiable Rules

- Keep core services, domain logic, and policies free of direct `temporalio` imports.
- Keep S3/SQL/path/credential/provider details out of core logic.
- Treat `temporalio` as the platform orchestration framework, not as a replaceable infrastructure adapter.
- Default to a single canonical Temporal orchestration. A local orchestrator is optional, not standard.
- Prefer direct imports from concrete modules over package-level re-export surfaces. `__init__.py` should default to docstring-only package markers unless the repo has an explicit compatibility contract.
- Distinguish "abstracted capability" from "independent activity".
- Split activities by retry value, side-effect boundary, scheduling value, and resource profile.
- For LLM/provider/model/asset work, one activity may contain at most one external logical call. Zero-call planning, merge, package, and state-mutation activities may stay aggregated. A provider-native batch HTTP/RPC request counts as one logical call only when the inputs are homogeneous and share the same retry value and resource profile. Do not wrap multiple long-tail LLM/provider/asset operations, fallback loops, or per-item retry calls into one coarse "stage" activity.
- Every activity that owns a model/provider call must still implement the full lifecycle: deterministic input preparation and context import, one logical model/provider generation boundary, then parse/validation/acceptance before durable success is reported. Light preparation and validation may stay inside the same activity; split them out when preparation is heavy, validation/repair is heavy, the prepared payload is reused across flows, or the result becomes a stable intermediate product.
- Before splitting activities, prove the intermediate boundary is safe for distributed workers. Separate activities may run on different machines, so they cannot share local files, scratch directories, process memory, or in-memory caches; Temporal payloads must not carry large prompts, large contexts, binary assets, or full candidate batches. Split only across compact DTOs, durable document/artifact/package refs, or stable IDs that each activity can reload from a repository/object store.
- Prefer Temporal activity retry as the normal regeneration boundary after model/provider failure or output validation failure. Hidden in-activity regeneration after validation failure is a documented exception, not the default; it must not loop over multiple targets, hide fallback model calls, or mutate durable state before acceptance.
- For multi-round dependent model chains, each upstream call must publish an explicit acceptance contract before downstream prompt construction consumes it. If a downstream step proves the upstream output violated that contract, model it as a visible workflow repair/regeneration branch or a clear workflow failure, not as an implicit nested retry inside the downstream activity.
- Treat workflow run/execution timeout as an explicit business guardrail, not a default wrapper around durable orchestration. Public workflows and normal child workflows should omit narrow run/execution timeouts unless the owner, SLA, metrics basis, and adjustment/removal condition are documented.
- Treat activity timeout as a single non-durable attempt guard. It must not represent provider queue time, total business wait, multi-shard batch duration, or an activity-internal long polling loop.
- Keep provider / LLM queued or running waits in workflow durable state with timer/sleep/query fallback. Do not hold an activity worker slot while waiting for upstream generation to finish.
- Do not hide provider/model retry or timeout inside an activity's HTTP client, SDK client, service helper, or parser loop. The normal visible boundary is Temporal activity retry plus the activity attempt timeout.
- Provider/model SDK and HTTP clients should disable internal retries and avoid narrow request timeouts by default. If a transport timeout is unavoidable for connection hygiene, it must be documented as a short connect/transport guard, not as the model generation or provider wait budget.
- If provider/model work can wait for a long time, make that wait visible at the workflow/activity boundary instead of burying it inside a client call. Prefer provider async submit/query/finalize or a narrower activity attempt timeout over hidden in-activity polling.
- If an activity's normal tail latency approaches its attempt timeout, or the worker later reports completion after Temporal timed it out, prefer splitting activity/shard boundaries and persisting partial success over simply raising the timeout.
- Freeze worker kind and default task queue before adding complex routing.
- Every assessment or normalization must state the worker topology and scaling stance:
  - whether one image runs multiple Deployments/commands
  - whether workflow and activity roles share a Deployment/Pod/task queue or split by role
  - whether capacity uses fixed SDK concurrency, WorkerTuner/slot suppliers, poller autoscaling, or manual defaults
  - which signals drive scaling: schedule-to-start, queue backlog, worker slots, provider/backing-store pressure, and pod CPU/memory
- Prefer one worker role per Deployment for production-like topology. Multi-container Pods are only justified when roles must share lifecycle and scale.
- Do not classify an entire module as CPU-heavy or IO-heavy when its activities differ. Provider task submission/polling can be IO-heavy while post-success download/decode/transcode/upload is heavy CPU+IO.
- For large sets of parallelizable work, prefer windowed fan-out / bounded in-flight over both extremes:
  - do not hardcode a tiny fixed concurrency in workflow code as the long-term scaling model
  - do not enqueue the full backlog at once when the workload can be released gradually
- Let workflow code express dependency and parallelism structure through windowed fan-out, while actual throughput is mainly absorbed by worker topology, poller autoscaling, task slots, replicas, provider-gateway capacity, and activity-level rate limiting.
- Treat window size as a configurable rollout strategy, not a buried constant. Increase or decrease it using measured schedule-to-start latency, worker saturation, and provider/backing-store pressure.
- In parallel fan-out workflows, isolate failures at shard/item level. One failed provider task, child workflow, episode, representation, clip, or micro-batch must not cancel unrelated siblings or prevent successful siblings from finalizing.
- Successful shards must be committed or staged into durable package/resource/audit state before the workflow reports an overall failure. If all shards fail, write a failure audit package when the module has that package surface.
- Retried or rerun workflows must skip already successful targets through durable refs, stable child workflow IDs, provider-gateway idempotency keys, or equivalent target state. Activity retries, current time, random IDs, LLM output, and provider task IDs cannot decide rerun identity.
- Every provider/LLM logical call or shard must carry a locatable observability identity: run ID, target ID when known, attempt ID, workflow/activity name, provider request ID when available, and trace context.
- When a module calls a Provider Gateway create endpoint, send these required audit headers: `X-DW-Project-Id`, `X-DW-Run-Id`, `X-DW-Billing-Subject-Type`, and `X-DW-Billing-Subject-Id`. For Provider Gateway task query/cancel endpoints, do not require callers to repeat create-time audit headers when the task ID can recover the persisted audit facts; still pass any available execution context as optional request context.
- When known, also send the product drilldown headers: `X-DW-Run-Id`, `X-DW-Target-Id`, `X-DW-Attempt-Id`, and `X-DW-Workflow-Node-Id`. These IDs are owned by Business Backend / Business Workflow; algo modules must only consume and pass them through, not mint them locally.
- Keep Temporal runtime facts in separate Provider Gateway headers: `X-DW-Temporal-Workflow-Id` and `X-DW-Temporal-Run-Id`. A workflow may fill them from Temporal context, but they do not replace business IDs and must not participate in create idempotency.
- Keep provider-call diagnostics in explicit headers when available: `X-DW-Workflow-Name`, `X-DW-Activity-Name`, `X-DW-Caller-Service`, `X-DW-Resource-Refs`, `X-DW-Parent-Request-Id`, `traceparent`, and `tracestate`.
- Do not send or rely on retired user compatibility headers for Provider Gateway billing. Billing must be explicit through `X-DW-Billing-Subject-Type` and `X-DW-Billing-Subject-Id`.
- Provider Gateway create idempotency must use `dw:v2:<caller_service>:<create_purpose>:<run_id>:<target_id|run-scope>:<attempt_id>`. Do not introduce operation-based v1 keys in new or migrated modules.
- Use `run-scope` in the v2 idempotency key only when the provider create is genuinely run-scoped and the target count or target identity is not known yet. Once a call belongs to a known target, use the stable target ID.
- Never build Provider Gateway create idempotency from `request_id`, trace/span IDs, Temporal run ID, current time, random IDs, provider IDs, LLM output IDs, filenames, or directories.
- Send `X-DW-Idempotency-Key` only for Provider Gateway create calls. Query, cancel, and finalize calls may carry optional audit context and fresh request identity, but they do not carry create idempotency.
- When a module calls Provider Gateway, carry `traceparent` / `tracestate` from the public workflow input or execution context into provider headers. Keep trace context diagnostic-only: it must not participate in idempotency keys, target identity, retry identity, or resource ownership.
- Keep parent and local request identity separate for Provider Gateway calls: preserve upstream `X-DW-Parent-Request-Id` when available, but still generate a fresh provider-call `X-DW-Request-Id` for each outbound HTTP attempt or logical operation.
- Treat provider/gateway 429, 5xx, transient network errors, and activity-attempt timeouts as retryable external failures owned by Temporal activity retry. Do not add SDK/client retry loops inside the activity, and do not convert these failures into `success=false` business results before the configured retry policy has had a chance to run.
- When multiple workflows can mutate the same logical resource key, do not rely only on per-workflow local ordering. Prefer an explicit shared-key coordination strategy, such as a keyed coordinator/entity workflow or equivalent serialized execution lane, so the same key is serialized across workflows while different keys remain parallel.
- Treat repository/database locks as an implementation detail of the adapter layer when unavoidable, not as the primary workflow-level coordination model.
- Pass large intermediate data by `document ref` or `artifact ref` first.
- Route every durable object read/write through the module's storage boundary. Do not bypass storage adapters with ad hoc OSS/S3 SDK calls from workflows, core services, provider helpers, or package builders. Activity-local temporary files are the narrow exception, and only inside one activity attempt.
- Write OSS objects only under centrally documented storage `data_type` roots and package layouts. Do not invent module-private prefixes, old plural roots, provider folders, `latest` roots, `tmp/cache/output` roots, or raw key conventions unless the central storage table explicitly defines them.
- Do not elevate worker/static environment configuration into public workflow contracts via a `config ref`.
- If a repo already materializes immutable run-preparation metadata, keep it module-owned and internal unless there is a very strong reason to expose it as a stable business object.
- Keep workflows thin and deterministic.
- Never do network IO, file IO, database IO, threads, processes, nondeterministic time, random values, or ad hoc UUID generation inside workflow code.
- For Python sandboxed workflows, make workflow imports sandbox-safe:
  - wrap local imports that transitively load provider, storage, HTTP, SDK, or runtime clients in `workflow.unsafe.imports_passed_through()`
  - keep package `__init__.py` files docstring-only or lazy unless a compatibility contract explicitly requires re-export
  - validate with replay, `SandboxedWorkflowRunner.prepare_workflow`, or real Worker construction; a plain Python import is not enough to prove sandbox safety
- Use `Signal`, `Query`, and `Update` deliberately:
  - `Query` is read-only and should stay synchronous.
  - `Update` is for state-changing requests that need an acknowledged result.
  - `Signal` is for fire-and-forget state changes.
- Coordinate concurrent workflow handlers explicitly, for example with `asyncio.Lock`, when shared workflow state can be mutated by multiple handlers.
- Treat testing as part of the architecture: `unit`, `activity`, `workflow`, `replay`, `e2e`.
- Use `ActivityEnvironment` for isolated activity tests, `WorkflowEnvironment.start_time_skipping()` for most workflow tests, `WorkflowEnvironment.start_local()` or a local Temporal dev server for smoke tests, and replay tests for deployment safety.
- For local Temporal validation, default to a single queue that closes the workflow/activity loop quickly; reserve multi-queue topology for remote or production-like worker modes.
- A local-only unsandboxed workflow runner is acceptable when it is an explicit developer ergonomics choice rather than accidental drift.
- Choose sync vs async mainly at the `activity` and `infra` layers. Keep the core synchronous by default unless async semantics are intrinsic to the domain code.
- Default Temporal activities to synchronous `def` plus the worker `activity_executor` unless the whole dependency chain is async-safe end to end. An `async def` activity that calls synchronous OpenAI, `requests`, `httpx.Client`, `boto3`, local file IO, subprocesses, or CPU-heavy code is a worker event-loop blocking bug.
- Prefer async activities only for high-concurrency IO where every hot path awaits non-blocking clients. Standard choices:
  - OpenAI: use `AsyncOpenAI` in async activities; use `OpenAI` only in sync activities or an explicitly bounded thread bridge.
  - Generic HTTP: use `httpx.AsyncClient` in async activities; keep `requests` and `httpx.Client` inside sync activities.
  - S3 / object storage: prefer `boto3` low-level clients inside sync activities and size `activity_executor` / connection pools deliberately. Use `aioboto3` / `aiobotocore` only after lockfile compatibility, context-manager lifetime, and the specific S3 operations are tested in the target repo.
  - Local file IO: keep it in sync activities unless a repo deliberately adopts and tests an async file adapter.
- `asyncio.to_thread()` / `loop.run_in_executor()` are bridge tools, not the default Temporal architecture. Use them only when an activity must stay `async def` for other awaited work, and guard them with explicit bounds, timeouts, cancellation expectations, and client thread-safety review. If the whole activity body is blocking, make the activity synchronous instead.
- Treat CPU-heavy tasks as a separate execution problem; do not block an async event loop with long CPU work. If CPU work is substantial, put it in a sync heavy activity queue, a process pool, or a dedicated worker role with resource limits.
- Use `16` as the normal fixed-concurrency starting point for model/provider activity-io lanes when the project has no stronger measured cap. Align the workflow fan-out window, Temporal `max_concurrent_activities`, sync `activity_executor` size, HTTP/client pool, and deploy config so the cap is real. Do not apply this model-call cap to mixed queues that also run FFmpeg, decode/transcode, package assembly, or other CPU/memory-heavy work; split those activities into a low-concurrency heavy role first.
- Model failures intentionally:
  - use typed business errors
  - use `ApplicationError` when you need explicit retry semantics
  - mark non-retryable failures deliberately instead of relying on vague exception behavior
  - in Python public workflows, every deliberate terminal business failure must raise `ApplicationError(message, type=<stable_type>, non_retryable=True)` or a local helper that builds the same failure
  - in Python public workflows, `@workflow.defn(...)` must explicitly include `failure_exception_types=(ApplicationError,)`; otherwise later workflow-thrown plain exceptions can degrade into repeated workflow task failures instead of a closed workflow execution
  - do not add broad `ValueError`, `RuntimeError`, or `Exception` to `failure_exception_types`; catch workflow input validation at the boundary and convert it to `invalid_workflow_input`
  - default cross-repo workflow failure types are `invalid_workflow_input`, `workflow_all_items_failed`, `workflow_dependency_failed`, `workflow_output_contract_violation`, and root-level fallback `workflow_failed`
- Treat `document ref / artifact ref` as the default payload strategy.
- Treat `DocumentRef` / `ArtifactRef` as structured envelope objects, not raw strings or bare S3 keys.
- Treat durable object roots as bundle/object-family semantics instead of one-file-per-data-type assumptions.
- Default logical object paths to `path_segments: list[str]`; platform adapters may join them into local paths, S3 keys, or serving URLs.
- Default `package_ref` to the bundle-root `package.json`.
- Default package-internal canonical members to `sections/` and retained audit members to `audit/`.
- Keep human-readable `.txt` sidecars and similar convenience exports out of canonical contract unless the repo explicitly freezes them as public outputs.
- Make `progress_target_workflow_id` mandatory on every module public workflow input so upward progress communication can be added without later breaking the contract.
- For outward progress signals, separate progress event identity from Temporal execution identity: `event_id` is a scoped idempotency key, not a workflow/run identity.
- Outward progress `event_id` must stay stable and short. In DramaWork-compatible modules it must satisfy `event_id <= 64`.
- Never build outward progress `event_id` from a full `workflow_id`, `source_workflow_id`, Temporal run ID, object-store key, long request namespace, provider payload field, current time, or random value.
- Preserve full execution identity in dedicated fields such as `workflow_id`, `source_workflow_id`, `temporal_workflow_id`, `temporal_run_id`, execution context, or correlation links.
- Add at least one production-shaped workflow ID regression test for progress emitters, using a long legacy shape such as `project-run:workspace:<project_id>:operation:<operation_id>:<module>`, and assert the emitted `event_id` is short while the full execution identity remains available elsewhere.
- Do not keep generic `summary_ref / component_refs` as default public outputs; promote only explicitly named stable refs.
- If the main `document ref` already carries stable scope such as `project_id`, do not repeat the same field in module public input unless the caller has no authoritative main ref.
- Treat `manifest/index` as explicitly named embedded package sections, not as a third ref kind or a default parallel public output.
- For high-cardinality outputs, prefer a single `package_ref` whose package JSON embeds named `manifest/index` sections instead of large child-ref arrays in public workflow outputs.
- Allow the business layer to create staging/adaptor packages between modules; do not force a downstream module to always consume the raw upstream package shape.
- Treat downstream stage inputs as stable snapshots/hard copies by default; later downstream edits should not silently mutate upstream canonical products.
- The main exception is globally shared canonical resources such as asset registries and asset artifacts, which may continue to be referenced live across stages.
- Force each persisted object into one of these lifecycle positions:
  - canonical durable truth
  - durable package-local audit members
  - ephemeral staging/tmp/debug/rebuildable intermediates
- Prefer a reserved ephemeral prefix such as `_ephemeral/{data_type}/...` for temporary objects instead of mixing them into canonical roots.
- If cross-activity/tmp objects must go to object storage, require both:
  - owner-side best-effort cleanup
  - platform-side TTL safety net
- Keep TTL comfortably longer than maximum runtime, retry window, and manual recovery window; do not use short TTLs that can expire during execution.
- For local worker scratch, require an explicit run-scoped tmp root and janitor strategy instead of assuming process exit will always clean up.
- Keep orphan scan / reachability analysis / delayed GC as a platform concern; modules only need to classify objects correctly and expose canonical roots.
- If an ephemeral staging object exists only to satisfy one downstream call and has no audit/reuse value, let the creating business workflow clean it up after the call completes instead of promoting it to a durable object.
- Separate three configuration layers explicitly:
  - worker static config via config files, ConfigMap, Secret, or startup args
  - public workflow options for light, enumerated caller controls
  - internal execution strategy for retry, timeout, batching, and fan-out details
- Large payload offloading through Temporal external storage is optional and secondary; if used, document durability, retention, and rollout constraints because the Python SDK feature is still pre-release.
- Separate workflow-code versioning from wire-schema versioning:
  - use Worker Versioning, replay, and patching for workflow-code evolution
  - use explicit schema-compatibility rules for workflow/activity input and output DTOs
- Default wire-schema evolution to backward-compatible additive change:
  - adding optional fields with safe defaults is preferred
  - removing, renaming, or redefining field meaning is a breaking change unless an explicit compatibility window exists
- Keep readers more compatible than writers during rollout:
  - new workers should keep reading older payload shapes for at least the active rollout window
  - activity handlers should expect to receive older workflow-emitted inputs while old runs are still alive
- Promote breaking wire changes to explicit contract changes instead of silent mutation:
  - introduce a new activity or workflow name when semantics, retry meaning, side effects, or result shape materially change
  - reserve in-place DTO mutation for clearly compatible changes
- If the module needs schedule-driven execution, prefer Temporal Schedules over ad hoc cron-style conventions and record pause/backfill/update expectations explicitly.
- Treat Data Converter / Payload Codec / Payload Encryption as infrastructure-level customization points. Do not re-invent ad hoc serialization or encryption rules inside business services.
- Treat replay and worker versioning as part of deployment safety, not as optional polish.
- Any workflow code-shape change that changes scheduling order, branching, activity names, child workflow IDs, or durable state transitions needs an explicit replay, patching, or Worker Versioning stance before rollout.
- Prefer a single stable `run` entry plus a `verify` or replay-validation path for worker processes.
- Treat containerization as part of operational shape, not post-processing:
  - prefer pinned multi-stage builds
  - when BuildKit is available, mount the builder wheelhouse and lockfile into the runtime install step instead of copying them into final layers
  - keep runtime images non-root and minimal
  - use a real init such as `tini` when the image runs a long-lived worker process
  - keep config, certificates, and secrets mounted or injected at runtime rather than baked into the image
  - keep domestic mirrors or private package indexes configurable through build args or environment, not hardcoded into the generic template
  - prefer least-privilege runtime defaults such as dropped Linux capabilities, `no-new-privileges`, and explicit writable scratch paths when the runtime platform supports them
- Prefer Kubernetes-oriented worker packaging when the repo is container-first:
  - readiness probes may reuse a real worker healthcheck path when that path is cheap and intentionally dependency-aware
  - liveness probes must be process-local or omitted until a process-local healthcheck exists
  - never put S3/OSS `HeadBucket`, provider calls, database migrations, or other external dependency reachability checks in liveness
  - resource requests/limits and shutdown grace should be explicit
  - image tags should be immutable enough for rollback and replay correlation
  - when feasible, treat SBOM generation and CVE scanning as part of the image release workflow rather than an afterthought
- When performance tuning goes beyond basic queue splits and concurrency caps, explicitly decide whether to adopt newer Temporal worker tuners / slot suppliers / poller autoscaling instead of mixing old and new control styles.
- Keep debugging guidance close to rollout safety: replay, history inspection, and nondeterminism diagnosis are the first tools, not last-resort cleanup.
- Treat Nexus as an advanced integration surface, not the default cross-module boundary, unless the repo explicitly standardizes on it.
- Update README, TODO, release notes, and any repo-local fact docs when the round is meaningful.
- When the repo uses GitHub Actions, keep CI/CD surface explicit:
  - separate test, security scan, and build concerns into distinct jobs or workflows
  - keep permissions minimal by default
  - prefer uploading built artifacts rather than silently discarding them
  - treat CodeQL or equivalent code scanning as a first-class security workflow, not an afterthought
  - prefer `workflow_dispatch` on `ci`, `codeql`, and `image` workflows so operators can rerun or override without fake commits
  - set `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true` in workflow `env` unless the target repo has a pinned lower-runtime constraint
  - when using GitHub Environments, bind `jobs.<job>.environment` explicitly; creating an environment in the UI does not inject vars by itself
  - resolve environment-scoped values inside the bound job `env:` block rather than only at workflow top level
  - for private repositories on GitHub Free or similar restricted plans, do not assume organization-level Actions vars/secrets will flow through; repo-level or environment-level values are the safe default
  - when Advanced Security or artifact attestation may be unavailable, preflight or gate them so the workflow skips cleanly instead of failing red
  - if the repo publishes worker images, keep image build/push as an explicit workflow with configurable registry coordinates, explicit trigger policy, metadata tagging, and provenance/attestation policy
  - prefer pinning GitHub Actions to the exact commit SHA of a reviewed release tag; keep a nearby comment such as `# actions/checkout@v6.0.2` so the intended upstream release remains human-readable
  - prefer immutable dev image tags based on UTC build time, for example `dev-YYYYMMDDHHMMSSmmm`, instead of only `edge` or raw commit SHA tags
  - keep APT/PIP/UV mirror and index URLs configurable through build args, repo variables, or manual dispatch inputs; do not hardcode local acceleration endpoints into the generic template
  - standardize variable names across repos instead of inventing local synonyms; keep mirror defaults at organization scope when possible, repo-specific image coordinates at repository scope, and deploy-target differences at environment scope
- When the repo has a declared template authority, prefer exact alignment on repo surface files such as `conf/`, `.github/workflows/`, `Dockerfile`, `pyproject.toml`, `README.md`, and package tree layout unless the repo has an explicit, documented exception.
- Treat config and public workflow I/O models as schema-bearing surfaces. Prefer Pydantic models over ad hoc dicts or loose dataclasses when the object is part of config loading, workflow I/O, or stable package/reference envelopes.
- Prefer `pathlib.Path` over raw `str` for local/logical path values passed through storage seams; only stringify at the adapter boundary.
- Keep repo-local docs clean: current fact docs in the main tree, temporary assessments/runbooks/design snapshots under `working-delta/`, disposable outputs under `.tmp/` or `tmp/`, and release deltas under the repo's release-note path only when the round is meaningful.

## Deliverables

Produce all of these:

- a short assessment or design note before substantial refactor
- code or scaffolding changes
- synchronized docs
- test additions or an explicit test gap note
- task-tracking updates when the repo uses a shared TODO file
- a `docs/releases/unreleased/` entry when the round is meaningful
- repo-local fact-doc updates when project-specific Temporal facts changed
- when the task is an assessment or review, the note should explicitly report findings across repo surface, architecture surface, and module contract surface, even if some sections have no issues
- when the task is a workflow conformance review, the note should include the per-workflow checklist status table or an equivalent explicit `pass/gap/n/a/blocked` accounting across identity, determinism, activity boundaries, activity workspace, storage authority, payload/ref strategy, error reporting, observability, tests, replay, and rollout evidence
