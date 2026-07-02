# Review Checklist and Output Template

Use this reference whenever the temporalization task is primarily a review, assessment, normalization audit, or pre-refactor gap analysis.

The goal is to keep reviews aligned across modules so they converge on the same standard instead of only sounding generally "Temporal-ready".

## 1. Review Scope

Every meaningful review should explicitly check these three surfaces:

1. repo surface
2. architecture surface
3. module contract surface

Do not stop at repo hygiene if the module contract is still fuzzy.
Do not stop at module contract if the repo surface still cannot support repeatable delivery.

Use checklist statuses consistently:

- `pass`: evidence exists in code, config, docs, tests, or live deploy facts
- `gap`: the rule is relevant and not yet satisfied
- `n/a`: the rule is genuinely out of scope for this workflow
- `blocked`: review cannot finish without owner decision, missing fact source, or unsafe access

Every `gap` or `blocked` item should name the file/area and the next owner action. Do not mark a workflow "fully temporalized" when any relevant Workflow Conformance Checklist item is still `gap` or `blocked`.

## 2. Repo Surface Checklist

Check at least these items:

- `pyproject.toml` exists and reflects the active Python/tooling baseline
- package manager and install path are explicit, for example `uv`
- `.gitignore` is sane for Python/Temporal work
- repo surface matches the declared template authority as closely as the repo's explicit exceptions allow
- package tree matches the expected `config / contracts / services / infra / bootstrap / temporal` layering rather than a near-miss variant
- worker runtime entry is explicit
- `run` and optional `verify` entry shape are explicit
- repo or module README explains the active entrypoints
- repo-local docs keep project facts, while generic Temporal guidance stays in the skill
- repo-local docs main tree only keeps current facts; temporary assessments, requirement drafts, and active runbooks live under `working-delta/` when present, with disposable outputs under `.tmp/` or `tmp/`; only stabilized facts are promoted into `docs/`
- repo-local facts are checked against any declared central docs tree instead of drifting into a repo-only interpretation
- tests are present and intentionally layered where the module is mature enough
- GitHub Actions CI surface is explicit:
  - `ci`
  - `codeql`
  - image build/publish workflow when containerized
- Dockerfile exists when the module is intended to run as a containerized worker
- deploy manifests exist when the module is already container-first
- release-note path and TODO conventions are honored

Common findings for this section:

- missing `verify` path
- no replay gate
- drifted `pyproject.toml`
- no CodeQL/image workflow while claiming production readiness
- docs still describe a local-only flow after Temporalization

## 3. Architecture Surface Checklist

Check at least these items:

- there is one canonical Temporal orchestration path
- core services are SDK-free
- storage/provider/model details stay out of core logic
- `bootstrap` assembly layer exists when the module needs environment-specific config loading, local run, or worker startup
- package-level `__init__.py` files are not being used as default re-export surfaces
- workflow code is thin and deterministic
- activity boundaries make sense by retry/side-effect/resource profile
- queue naming and worker kind naming are explicit
- local Temporal validation defaults to one queue unless the repo has a documented reason not to
- local-only unsandboxed workflow runner, if present, is explicit and justified rather than accidental drift
- signal/query/update use is intentional
- public progress surface distinguishes:
  - outward `signal`
  - outward `query`
  - internal `heartbeat/log`
- provider/LLM logical calls or shards have internal observability identity:
  - target ID
  - activity name
  - attempt/shard index
  - provider request ID or operation ID when available
  - trace context
- large payload strategy is `document ref / artifact ref` first
- configuration layering is explicit:
  - worker static config
  - public workflow options
  - internal execution strategy
- parallel fan-out uses bounded/windowed release when appropriate
- window size is a configurable rollout strategy, not a hidden workflow constant
- worker slots, replicas, provider-gateway capacity, rate limits, and autoscaling own throughput instead of provider concurrency being hardcoded into workflow code
- successful targets/shards are durably committed or staged before aggregate failure is reported
- reruns skip already successful targets through durable refs, stable child workflow IDs, provider-gateway idempotency keys, or equivalent target state
- single shard/item failure does not cancel unrelated siblings
- timeout and wait boundaries are intentional:
  - public workflow / child workflow run timeout is omitted by default or documented as a wide guardrail
  - activity timeout protects one retryable attempt, not provider queue time or total business wait
  - provider / LLM queued or running waits use workflow durable timer / sleep / query state
  - provider/model SDK and HTTP clients do not hide internal retries or generation-time timeout budgets
  - any unavoidable transport timeout is documented as connection hygiene, not provider generation wait
- shared-key mutation has an explicit coordination model when needed
- test layers are real or explicitly listed as gaps:
  - `unit`
  - `activity`
  - `workflow`
  - `replay`
  - `e2e`
- rollout safety is explicit:
  - replay
  - worker versioning / patching stance
  - DTO compatibility stance

## 3.1 Worker Topology and Scaling Checklist

Check at least these items:

- worker roles are explicit:
  - `workflow`
  - `activity-io`
  - `activity-state`
  - `activity-heavy`
  - `combined-small`
  - `replay/verify` when present
- task queue boundaries have a clear reason:
  - workflow queues are governance/compatibility/replay boundaries
  - activity queues can split by resource profile, side effect, rate-limit domain, or failure domain
- topology decision is explicit:
  - combined worker
  - split workflow/activity Deployments
  - split heavy activity queue
  - multi-container Pod
  - one image with multiple Deployments/commands
  - separate image only when dependency/resource profile requires it
- SDK concurrency is explicit:
  - `max_concurrent_workflow_tasks`
  - `max_concurrent_activities`
  - local activity / Nexus concurrency if used
  - executor sizing for sync activities
- slot strategy is explicit:
  - fixed slots
  - resource-based/custom WorkerTuner
  - no mixed use of WorkerTuner and legacy `max_concurrent_*` style controls
- poller strategy is explicit:
  - simple maximum
  - autoscaling poller behavior
- autoscaling posture is explicit:
  - manual replicas, HPA, KEDA, or disabled
  - min/max replicas
  - scaling metric
  - cooldown or scale-down stabilization
  - provider/backing-store protection
  - current phase, next phase, and final target are stated separately when autoscaling is not yet mature
- capacity formula is stated when tuning matters:
  - effective capacity is bounded by replicas, task slots, executor size, poller behavior, rate limits, dynamic upstream capacity, and pod resources
- metrics are available or listed as gaps:
  - queue backlog
  - workflow/activity schedule-to-start
  - worker slots used/available
  - activity retry/failure/timeout
  - provider estimated allowed concurrency / cluster in-flight / first-pending cursor / throttle / 429 / 5xx
  - DB/backing-store pressure where the project boundary allows DB in that worker role
  - pod CPU/memory/OOM/restarts
- rollout guardrails are explicit:
  - baseline metrics first
  - one capacity knob per rollout
  - rollback thresholds
  - replay/verify before behavior changes
- timeout metrics are available or listed as gaps:
  - activity p99/p99.5 execution latency
  - activity timeouts and retries
  - late completion / "activity not found on completion" style logs
  - workflow completions close to run/execution timeout
- activity profiles are classified by boundary rather than by module name. Video generation and video evaluation can contain both IO-bound provider calls and CPU/memory-heavy media processing activities.
- LLM/provider/model activities align to one logical provider call or bounded homogeneous shard when retry value, resource profile, or side effects differ.
- Coarse "stage" activities do not wrap multiple independent long-tail provider calls just to simplify the workflow graph.
- project-specific data boundaries are enforced. For DramaWork, algo workers must not add DB access; business workflow/worker owns business DB writes.

Common findings for this section:

- duplicated local orchestrator and Temporal orchestrator with no real product reason
- workflow code doing IO
- activities split by file shape instead of retry boundary
- queue names still accidental or copied from earlier experiments
- no replay path before claiming rollout safety

## 3.2 Workflow Conformance Checklist

Use this section as the canonical per-workflow review checklist. It is more specific than the repo/architecture/module surfaces above and should be applied to every public workflow and every long-lived internal workflow that can appear in production histories.

### A. Workflow Identity and Public Boundary

Check these items:

- workflow name is stable, explicit, and not an accidental class/function name
- public workflows are distinguished from helper/internal workflows
- child workflow IDs are stable, replay-safe, and derived from durable business identity rather than current time, random values, local paths, provider IDs, or retry attempt noise
- workflow input has a schema-bearing DTO, preferably Pydantic, with explicit `schema_version` when it crosses repo, rollout, or workflow-history windows
- public workflow input carries `progress_target_workflow_id` when the module can report progress upward
- public workflow input does not expose worker static config, ConfigMap paths, Secret names, local paths, or deployment topology as caller-controlled fields
- workflow output is a compact typed result that points to durable refs/packages instead of embedding large documents, full provider responses, media, prompts, or high-cardinality child arrays
- public workflow options are stable capability-level intent, not one provider's private parameter names
- business-owned IDs such as run/target/attempt/workflow-node IDs are consumed and propagated, not minted inside algo modules
- workflow code has a replay/versioning stance before rollout when scheduling order, branching, activity names, child workflow IDs, DTO semantics, or durable state transitions changed

Common findings:

- workflow ID includes a full upstream execution string and later breaks progress/event ID length
- helper workflow accidentally becomes part of the public Business -> Algo contract
- input DTO accepts loose `dict[str, Any]` and silently tolerates incompatible shapes

### B. Determinism and Workflow-Code Safety

Check these items:

- workflow code does not perform network IO, file IO, database IO, object-store IO, subprocesses, thread/process creation, non-Temporal sleeps, current-time reads, random ID generation, or ad hoc UUID generation
- workflow code only orchestrates ordering, branching, durable waits, timers, child workflows, signals/queries/updates, and activity calls
- workflow imports are sandbox-safe; provider/storage/HTTP/SDK/runtime imports are passed through or kept outside workflow import paths
- package `__init__.py` files do not pull heavy runtime dependencies into workflow import graphs unless there is a documented compatibility reason
- signal/query/update handlers are intentional, and shared mutable workflow state is protected when concurrent handlers can run
- public `Query` handlers are read-only and synchronous
- `Update` exists only for acknowledged state-changing controls with a frozen contract
- local smoke tests do not replace replay or sandbox validation for deployment safety

Common findings:

- workflow module imports a service package that imports boto3/OpenAI/httpx at import time
- workflow uses a local helper that reads config files or environment variables
- query handler mutates progress state

### C. Activity Boundary Rules

Check these items:

- every activity boundary is justified by retry value, side-effect boundary, resource profile, scheduling value, or durable state transition
- provider/LLM/model/asset generation activities contain at most one external logical call or one bounded homogeneous shard with the same retry/resource profile
- coarse stage activities do not hide multiple independent long-tail provider calls, fallback calls, or per-item retry loops
- model/provider activity lifecycle is explicit: deterministic input preparation/context import, one logical external call, parse/validation/acceptance, then durable success
- hidden in-activity regeneration after validation failure is documented as an exception and does not loop over multiple targets or mutate durable state before acceptance
- activity retries are owned by Temporal retry policy for retryable external failures such as gateway 429/5xx, transient network errors, and activity-attempt timeout
- SDK/client/service helper retries are disabled by default for provider/model calls; any unavoidable transport timeout is documented as connection hygiene, not generation wait
- provider queued/running waits are durable workflow state with timer/sleep/query/finalize activities, not activity worker-slot blocking loops
- activity attempt timeout protects one non-durable attempt; it is not the total business SLA, provider queue budget, or multi-shard batch duration
- if activity tail latency approaches attempt timeout, the review considers shard split, durable partial success, or separate heavy/IO queues before simply raising timeout
- sync vs async activity choice is deliberate:
  - sync `def` activity for sync SDKs, file IO, boto3, CPU-heavy code, subprocesses, or blocking libraries
  - async activity only when every hot dependency is non-blocking
  - `asyncio.to_thread()` / executor bridges are bounded and documented exceptions
- CPU/memory-heavy work is separated from high-concurrency provider IO when resource profiles differ
- activities heartbeat or log long-running progress where useful, without treating heartbeat as business progress

Common findings:

- one `generate_all` activity does provider submit, polling, download, transcode, upload, package, and DB/state mutation
- activity wraps OpenAI/HTTP retries inside the client while Temporal also retries the activity
- async activity calls sync boto3 or `requests`, blocking the worker event loop

### D. Activity Local Workspace Rules

Check these items:

- worker deployment declares `DRAMAWORK_ACTIVITY_TMPDIR` or the repo's canonical equivalent
- activity local work is created under an explicit managed tmp root, preferably one per activity attempt
- local workspace creation is run-scoped or attempt-scoped enough to avoid collisions across concurrent attempts
- local workspace cleanup uses `try/finally` / context manager semantics and best-effort cleanup on success/failure
- stale local workspace cleanup or janitor strategy exists when process crash or pod eviction can leave residue
- local files, process memory, scratch directories, and in-memory caches are never used as cross-activity, cross-workflow, or cross-pod handoff
- separate activities exchange compact DTOs, durable refs/packages, or stable IDs that can be reloaded from storage
- cross-activity temporary cloud objects use reserved `_ephemeral/...` style roots with owner cleanup plus TTL safety net when the project standard requires it
- TTL is longer than maximum workflow runtime, retry window, and manual recovery window
- canonical durable outputs are written under stable data-type/package roots, not tmp/cache/scratch roots
- package-local canonical members and retained audit members are separated, for example `sections/` and `audit/`
- `package_ref` points to the bundle root, usually `package.json`
- local path refs are rejected at public workflow/package boundaries unless the module is explicitly local-only
- for DramaWork-compatible algo workers, active deploy/config does not depend on bare `/scratch`; activity-local storage lives under `/var/tmp/dramawork/activity-workspaces`

Common findings:

- activity A returns `/tmp/foo.json` and activity B reads it
- config points `work_root` to a path that is not mounted in live pods
- package builder publishes local adapter paths into public package refs

### E. Storage Authority and OSS Layout Rules

Check these items:

- all durable object reads/writes go through the repo's storage port/adapter/service boundary, not direct ad hoc SDK calls from workflow code, service logic, provider helpers, or package builders
- workflow code never touches object storage directly
- core/domain services do not import S3/OSS SDKs, read storage credentials, or assemble deploy-specific endpoints
- activity-local temporary files are the only accepted bypass of durable storage, and they stay inside the single activity attempt boundary
- any data that crosses activity, workflow, pod, process, or retry-attempt boundaries is persisted through the storage adapter as structured refs/packages
- OSS object keys follow the central storage data-type table, not module-private prefixes, old plural names, provider-specific folders, or convenience paths invented in the worker
- the first object-key segment is a registered global `data_type` unless the central docs explicitly define another reserved root such as `_ephemeral/{data_type}/...`
- each writer can point to the exact central `data_type`, path rule, package layout, producer, consumer, permanence, and retention/GC row it implements
- new `data_type` values are not introduced locally without updating the central table and explaining why an existing type cannot be reused
- long-lived outputs write to the durable canonical shape `{data_type}/{project_id}/{owner_id}/{snapshot_id}/{path_segments...}` or the exact row-specific variant from the central table
- temporary cross-activity/cloud handoff writes to `_ephemeral/{data_type}/{project_id}/{owner_id}/{snapshot_id}/{path_segments...}` only when central docs allow that lifecycle
- package roots contain canonical machine members under the documented layout, and retained debug/audit members stay in documented `audit/` or provider-debug surfaces
- provider raw artifacts, raw requests/responses, thumbnails, previews, text sidecars, and legacy exports are not promoted to canonical roots unless the central table explicitly names them
- storage refs are structured envelopes with data type/root/member semantics, not raw OSS keys or signed URLs passed through the workflow contract
- public/business-facing refs do not expose bucket names, endpoints, credentials, temporary signed URLs, local paths, or adapter-specific path separators
- compatibility readers for old OSS paths are explicitly documented with removal conditions and metrics/logging; new writers do not continue writing legacy roots
- tests or audit scripts prove current writers do not emit legacy prefixes and reject local-path/raw-key refs at public boundaries

Common findings:

- package builder constructs `f"{module_name}/{run_id}/..."` directly instead of using the central storage key helper
- provider adapter uploads raw files to `tmp/`, `cache/`, `outputs/`, `artbook/`, `video_generation/`, or `latest/` roots not listed in the central data-type table
- service logic has direct `boto3`/OSS client usage instead of going through `infra/adapters`
- a workflow output returns an OSS key string that downstream code parses by splitting `/`

### F. Temporal Payload and Ref Strategy

Check these items:

- workflow/activity payloads are intentionally small and JSON-serializable through the configured data converter
- large prompts, retrieved context, binary media, raw provider request/response bodies, full candidate batches, and high-cardinality result sets are passed by document/artifact/package refs
- ref objects are structured envelopes, not raw strings, absolute paths, Windows drive paths, or bare S3 keys
- logical paths use structured fields such as `path_segments: list[str]` where the project standard expects them
- public DTO fields distinguish schema version from content version, revision, snapshot ID, or package version
- readers are more compatible than writers during rollout; active workers can read older input shapes while old histories are still alive
- breaking semantic changes use a new workflow/activity name or explicit compatibility window instead of silent in-place mutation
- Temporal payload external storage / codec / encryption is treated as an infrastructure-level decision, not a substitute for ref-first workflow design
- payload size budget is tested or audited for fan-out workflows and target batches
- workflow history does not grow with repeated full prompt/context/provider payload copies

Common findings:

- ref-first package exists, but activity input still embeds the same large package inline
- DTO `schema_version` is used to mean both wire shape and content revision
- batch result arrays grow with target count and are returned directly from the workflow

### G. Error and Failure Reporting Rules

Check these items:

- public workflow declares deliberate workflow terminal failure behavior explicitly
- Python public workflows include `failure_exception_types=(ApplicationError,)` when deliberate `ApplicationError` failures should close workflow execution instead of causing repeated workflow-task failure
- public workflow does not add broad `ValueError`, `RuntimeError`, or `Exception` to `failure_exception_types`
- input validation failures are converted at the workflow boundary to a stable non-retryable type such as `invalid_workflow_input`
- terminal business failures raise `ApplicationError(message, type=<stable_type>, non_retryable=True)` or a local helper that produces the same semantics
- stable failure types are documented and reused. Default cross-repo types are:
  - `invalid_workflow_input`
  - `workflow_all_items_failed`
  - `workflow_dependency_failed`
  - `workflow_output_contract_violation`
  - `workflow_failed`
- retryable external/provider/storage failures are left retryable at activity boundary until Temporal retry policy is exhausted
- provider/gateway 429, 5xx, transient network errors, and activity-attempt timeouts are not prematurely converted to `success=false` business results
- partial failure semantics are explicit:
  - successful shards/targets are committed or staged before aggregate failure is reported
  - one failed shard/item does not cancel unrelated siblings unless contract says all-or-nothing
  - if all shards fail, a failure audit package is written when the module has that surface
- dependency failure vs output-contract violation vs provider transient failure are distinguishable in error type/message
- error reports include enough correlation to locate the failing run/target/attempt/activity/provider request without embedding huge payloads
- workflow/application errors propagate to Business or parent workflows through the agreed summary shape rather than only logs
- broad `except Exception` blocks do not swallow failures, hide retryability, or rewrite all failures into one vague message
- cancellation and timeout paths are reviewed separately from ordinary exceptions

Common findings:

- workflow raises `ValueError`, causing endless workflow task retries
- activity catches provider 500 and returns `{success: false}` before Temporal retry can run
- parent workflow sees only "child failed" without stable child failure type, activity name, or target identity

### H. Progress, Observability, and Provider Audit

Check these items:

- public progress is business-meaningful and separated from heartbeat/log/provider noise
- outward progress signal payload has a stable name and typed payload
- outward progress `event_id` is a scoped idempotency key, not Temporal execution identity
- DramaWork-compatible progress `event_id` is `<= 64` and has a production-shaped workflow ID regression test
- `event_id` does not include full `workflow_id`, `source_workflow_id`, Temporal run ID, object-store key, long request namespace, provider payload field, current time, or random value
- full execution identity remains available through dedicated fields such as `workflow_id`, `source_workflow_id`, `temporal_workflow_id`, `temporal_run_id`, execution context, or correlation links
- every provider/LLM logical call or shard carries locatable identity: run ID, target ID when known, attempt ID, workflow/activity name, provider request ID when available, and trace context
- Provider Gateway create calls send required audit headers when available:
  - `X-DW-Project-Id`
  - `X-DW-Run-Id`
  - `X-DW-Billing-Subject-Type`
  - `X-DW-Billing-Subject-Id`
- optional drilldown headers are propagated when known:
  - `X-DW-Target-Id`
  - `X-DW-Attempt-Id`
  - `X-DW-Workflow-Node-Id`
  - `X-DW-Temporal-Workflow-Id`
  - `X-DW-Temporal-Run-Id`
  - `X-DW-Workflow-Name`
  - `X-DW-Activity-Name`
  - `X-DW-Caller-Service`
  - `X-DW-Resource-Refs`
  - `X-DW-Parent-Request-Id`
  - `traceparent`
  - `tracestate`
- provider create idempotency uses the project standard, for DramaWork: `dw:v2:<caller_service>:<create_purpose>:<run_id>:<target_id|run-scope>:<attempt_id>`
- provider create idempotency never uses `request_id`, trace/span IDs, Temporal run ID, current time, random IDs, provider IDs, LLM output IDs, filenames, or directories
- `X-DW-Idempotency-Key` is sent only for create calls, not query/cancel/finalize calls
- logs/metrics/traces include activity retry, timeout, provider status, schedule-to-start, worker saturation, and backing-store pressure where relevant

Common findings:

- provider audit has only request ID and no run/target/attempt identity
- progress event ID is built from full workflow ID
- provider query calls incorrectly reuse create idempotency keys

### I. Tests, Replay, and Rollout Evidence

Check these items:

- unit tests cover SDK-free services, policy, package/ref builders, and DTO validation
- activity tests use `ActivityEnvironment` or equivalent isolation for side effects, retryable errors, local workspace cleanup, and ref materialization
- workflow tests use `WorkflowEnvironment.start_time_skipping()` for orchestration, branching, signal/query, and retry behavior
- replay tests or replay-validation command exist for representative histories before production rollout
- e2e/local smoke uses `WorkflowEnvironment.start_local()` or local Temporal dev server when workflow/activity loop needs proof
- sandbox import / real Worker construction is tested when workflow import safety changed
- failure tests cover invalid input, dependency failure, output contract violation, all-items-failed, cancellation/timeout where relevant, and partial success before aggregate failure
- payload/ref tests prove large payloads are offloaded and public refs reject local paths
- storage authority tests prove durable writers go through storage adapters and emit only central-table data-type roots
- OSS layout audit proves no current writer emits unregistered module-private prefixes or legacy roots
- activity tmpdir tests prove per-attempt local workspace creation and cleanup
- progress tests prove short `event_id` with production-shaped workflow IDs
- provider audit/idempotency tests prove required headers and create-key shape
- worker topology and deploy config are validated when queue/concurrency/tmpdir/probe settings changed
- rollout notes state replay/Worker Versioning/patching stance, DTO compatibility stance, and rollback criteria

Common findings:

- tests only cover services and never instantiate workflow sandbox
- no regression test for large payload or local-path ref leak
- deployment changed queues or activity names without replay stance

## 4. Module Contract Surface Checklist

This is the most important section when aligning modules with a proven sample such as `artbook`.

Check at least these items:

- the module's product role is clearly stated
- public entry workflows are explicit
- internal-only workflows are distinguished from public ones
- public input contract is explicit
- public input/output model files are explicitly located, for example `contracts/workflow_io.py` or an equivalent schema-bearing surface
- config and workflow I/O surfaces use schema-bearing models rather than loose dicts; prefer Pydantic for config/public DTOs
- public input/result DTOs have explicit `schema_version` fields when they cross rollout windows, workflow history, or repo boundaries
- stored package/document schemas have their own version fields; content revisions use separate `content_version`, `revision`, or `snapshot_id` semantics instead of overloading the DTO schema version
- `progress_target_workflow_id` is mandatory on every module public workflow input
- public output/ref contract is explicit
- refs are treated as structured envelope objects instead of raw strings
- refs/path members use structured logical paths such as `path_segments: list[str]`, not adapter-specific raw strings
- large content, large prompts, high-cardinality collections, media assets, and provider raw responses are kept in document/artifact/package refs rather than inline workflow input/output fields
- public workflow options and output requirements express stable capability-level intent, not provider/model-specific parameter names
- generic `summary_ref / component_refs` are not used as default public outputs
- if the main ref already carries stable scope such as `project_id`, module public input does not repeat the same field without a clear fallback reason
- high-cardinality outputs use a single `package_ref`, with explicitly named `manifest/index` sections embedded inside the package JSON instead of large child-ref arrays
- package refs default to the bundle-root `package.json`
- package-local canonical members are clearly separated from retained audit members, for example `sections/` vs `audit/`
- the review distinguishes direct upstream package consumption from business-side staging/adaptor packages instead of assuming they are always the same object
- downstream stage data is treated as a stable snapshot/hard copy by default, with explicit exceptions called out for globally shared canonical resources
- storage split is explicit:
  - canonical document/package members
  - retained audit members
  - artifact/object families
  - projection/read model
  - ephemeral run artifact
- lifecycle split is explicit:
  - `durable` canonical and audit roots are separated from `ephemeral` staging/tmp/debug objects
  - temporary objects use a reserved ephemeral prefix instead of canonical roots
- local/tmp handling is explicit:
  - run-scoped local scratch root
  - best-effort cleanup owner
  - janitor or periodic cleanup path
- cross-activity cloud tmp handling is explicit:
  - `_ephemeral/...` shape
  - best-effort cleanup owner
  - TTL safety net long enough for runtime/retry/manual recovery windows
- orphan scan / delayed GC responsibility stays at the platform layer rather than being re-invented in each module
- if ephemeral staging objects are created only for one downstream call, cleanup responsibility is assigned to the creating business workflow instead of being left implicit
- config contract is explicit
  - worker/static config is not leaked as a public workflow ref
- signal/query contract is explicit if the module reports progress outward
- public progress granularity is business-meaningful, not provider/scene/attempt noise
- helper workflows and activities do not accidentally become public progress surfaces
- provider request IDs, operation IDs, attempt indexes, shard indexes, and trace context are retained for diagnostics without becoming public workflow progress fields unless the product contract explicitly requires them
- outward progress `event_id` is treated as a scoped idempotency key, not Temporal execution identity
- outward progress `event_id` length is bounded by the downstream Business contract; for DramaWork-compatible modules this means `event_id <= 64`
- outward progress `event_id` does not contain full `workflow_id`, `source_workflow_id`, Temporal run ID, object-store key, long request namespace, provider payload field, current time, or random value
- full execution identity remains available through dedicated fields such as `workflow_id`, `source_workflow_id`, `temporal_workflow_id`, `temporal_run_id`, execution context, or correlation links
- progress emitters have production-shaped workflow ID tests proving the emitted `event_id` is short and does not embed full execution identity
- public update is absent by default and only appears when a synchronous control action is explicitly frozen
- business-layer integration boundary is explicit:
  - what the upper layer passes in
  - what the upper layer listens to
  - what remains internal to the module
- business-to-module child workflow calls have contract fixtures or tests that validate the real child input shape, not only broad mocks
- breaking public DTO changes have an explicit migration plan, compatibility window, and either compatibility readers/adapters or a new workflow/activity contract name
- internal activity DTO changes are additive by default; if retry value, side-effect semantics, resource profile, or result shape changes materially, the review recommends a new activity name rather than silent in-place mutation
- stable product resources are distinguished from flexible documents and run-scoped artifacts
- if the module claims S3/local dual support, that boundary is configuration-driven rather than scattered through task logic

Common findings for this section:

- "Temporalized" but still no stable module contract
- repo structure looks clean while storage/config/progress contracts remain implicit
- the repo looks “roughly template-shaped” but still drifts in exactly the places that later block maintenance
- package/object governance is still file-by-file instead of bundle-first
- `.txt` convenience outputs are still being treated as canonical machine contracts
- business layer would still need to read module-private JSON layout directly
- progress exists but has no stable signal name/payload shape
- the module still passes large inline payloads through workflow inputs
- public input/result files exist but are treated as local DTOs instead of general API contracts
- provider-specific knobs such as a single model's audio switch leak into public workflow input instead of a stable capability field
- schema versioning exists for workflow code but not for wire DTOs or stored package documents

## 5. Output Template

Use this shape for assessment/review output.

### A. Module role and current state

- one short paragraph on what the module produces in the product chain
- one short paragraph on current entrypoints and current deployment/runtime reality

### B. Findings

Organize findings under:

- repo surface
- architecture surface
- module contract surface
- workflow conformance checklist, when reviewing a concrete workflow

For each finding, prefer:

- severity or priority
- concise statement of the gap
- why it matters
- affected files or areas

For concrete workflow reviews, also include a compact checklist table with at least these columns:

- area
- status: `pass`, `gap`, `n/a`, or `blocked`
- evidence
- required next action

The area rows should correspond to the Workflow Conformance Checklist sections:

- workflow identity and public boundary
- determinism and workflow-code safety
- activity boundary rules
- activity local workspace rules
- storage authority and OSS layout rules
- Temporal payload and ref strategy
- error and failure reporting rules
- progress, observability, and provider audit
- tests, replay, and rollout evidence

### C. Frozen recommendations

State what should be frozen next:

- worker/queue names
- worker topology and role split
- task queue matrix
- concurrency, slot, and poller defaults
- autoscaling metric and rollout tuning sequence
- workflow/activity boundaries
- storage/ref strategy
- config surface
- signal/query surface
- rollout/replay strategy

### D. Suggested next sequence

Prefer a short ordered list of the next safe steps.

Typical order:

1. freeze docs and contracts
2. normalize repo/runtime surface
3. fix core architecture drift
4. add replay/tests/CI/deploy gaps
5. only then expand features

### E. Explicit non-goals

State what is intentionally not being done in this round so the review does not silently imply more completion than actually exists.

## 6. Closing Rule

If a module review does not explicitly cover repo surface, architecture surface, and module contract surface, treat it as incomplete.
If it does not also state template-alignment status, central-doc alignment status, and bundle/tmp governance status, treat it as incomplete for repos that declare those authorities.
