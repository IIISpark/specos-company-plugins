# Worker Topology and Scaling

Use this reference when assessing or normalizing Temporal worker deployment shape, concurrency, probes, metrics, or autoscaling.

## 1. Terminology

- `image`: the packaged artifact. It may contain multiple workflows, activities, and worker roles when dependency and resource profiles are compatible.
- `worker role`: the runtime role selected by config or command, for example `workflow`, `activity-io`, `activity-state`, `activity-heavy`, or `combined-small`.
- `Deployment`: the Kubernetes rollout, replica, resource, probe, and autoscaling unit. Prefer one Deployment per worker role / workload profile.
- `Pod`: a Deployment replica. Multi-container Pods are only justified when roles must share lifecycle, scale, and resource posture.
- `SDK Worker`: the Temporal SDK process that polls one task queue and owns task slots.
- `task queue`: the Temporal routing and isolation surface. Workflow queues express governance and compatibility boundaries; activity queues may express resource, side-effect, rate-limit, or failure-domain boundaries.
- `slot`: the capacity to execute one concurrent Workflow Task, Activity Task, Nexus Task, or Local Activity Task.
- `poller`: the component that long-polls a task queue and feeds available slots.
- `rate limit`: a per-worker, per-task-queue, provider-domain, database, or backing-store protection mechanism.
- `provider capacity source`: the runtime source of truth for provider concurrency/rate/budget. For dynamic LLM/image/audio/video providers, do not require every worker config to maintain static `max_concurrency`; capacity should be estimated by provider-gateway runtime feedback and eventually exposed through provider-gateway metrics or a capacity control plane.
- `fan-out window`: the workflow-owned rollout strategy for how many independent targets/shards are released at once. It is not the same as SDK worker slots, replicas, provider-gateway admission, or upstream provider capacity.
- `provider logical call`: one product-meaningful LLM/model/provider operation, or one bounded homogeneous shard of such operations, with its own target identity, retry value, side-effect/resource profile, and observability identity.

## 2. Default Decision Matrix

Start with the smallest topology that preserves the real resource and failure boundaries.

| Shape | Use when | Avoid when |
| --- | --- | --- |
| one image, one combined worker | local/dev, early bootstrap, low throughput, compatible workflow/activity resource profile | activity work is heavy, provider-limited, DB-bound, or likely to block workflow polling |
| one image, multiple Deployments/commands | dependencies are compatible but workflow/activity or activity subtypes need different scale/resource policies | heavy system dependencies or node placement differ materially |
| split workflow and activity Deployments | workflow orchestration and side-effect execution have different resource, retry, timeout, or scaling needs | the module is still only local/dev and no metrics justify the split |
| split activity queues by profile | IO, state, heavy CPU/GPU, or provider-domain work has different concurrency and rate limits | the split would only rename queues without changing isolation or capacity control |
| multi-container Pod | roles must be co-scheduled and share lifecycle by design | independent scaling is valuable or one role can OOM/block another |
| separate image | dependencies, runtime packages, GPU/CPU profile, security posture, or rollout cadence differ materially | the only reason is to create a scaling unit; use multiple Deployments first |

Do not make "one workflow equals one Pod" the default. The normal production unit is "one worker role equals one Deployment".

## 3. Worker Profiles

### `workflow`

- Owns deterministic orchestration, signals, queries, child workflow/activity scheduling, and small workflow state.
- Must not perform network IO, file IO, database IO, provider calls, FFmpeg/model work, threads, processes, random values, or nondeterministic time.
- Scales on workflow task schedule-to-start, cache pressure, workflow task slots, CPU, and rollout/replay risk.
- Usually keeps a minimum replica count for availability and troubleshooting.

### `activity-io`

- Owns remote API calls, provider task submission/polling, HTTP, object-store IO, and lightweight network-bound work.
- For LLM/provider/model work, activity boundaries should align to one provider logical call or bounded homogeneous shard. Avoid coarse stage activities that bundle many independent long-tail provider calls with different failure, retry, or capacity behavior.
- In fixed-slot deployments, start model/provider call lanes at `16` concurrent activities unless measured provider/backing-store pressure or an explicit project limit says lower. Keep the workflow fan-out window, SDK slots, sync executor, client pool, and deploy config aligned; otherwise the smallest layer silently becomes the real cap.
- Can use higher activity slots when dependency chains are async-safe or when sync executors are sized intentionally.
- Must be constrained by provider-gateway dynamic admission, Temporal-visible retry posture, activity attempt timeout, memory, and connection pools.
- Scales on activity schedule-to-start, backlog, slot saturation, provider 429/5xx/timeout, and execution latency.
- Treat provider quota as dynamic. Worker config may name `provider_domain` / model family for routing and attribution, but should not own per-upstream `max_concurrency`. Provider gateway should infer capacity from 429, first-pending cursors, task pending/completion pace, shared in-flight, and throttle/degraded signals.

### `activity-state`

- Owns DB writes, registry/apply logic, package/manifest state updates, and idempotent durable mutations.
- Concurrency must align with DB pool, lock/key strategy, transaction shape, and write ordering.
- Scales only when backing-store pressure confirms it is safe.
- Obey project-specific DB boundaries. In DramaWork, algo workers must not access DB; algo `activity-state` means package/manifest/registry/object-store state, while business workflow/worker owns DB writes.

### `activity-heavy`

- Owns FFmpeg, decoding, transcoding, image/video/audio processing, GPU/model inference, large local files, or high memory tasks.
- Uses low in-process concurrency by default and explicit CPU/memory/GPU requests. Start around `2-4` per worker, or lower when one activity can consume most of a pod's CPU, and scale by replicas or a dedicated node pool only after CPU/RSS/disk metrics support it.
- Often deserves its own Deployment, node pool, and sometimes its own image.

### `combined-small`

- Acceptable for local/dev or low-risk low-throughput modules.
- Must be documented as a bootstrap/simple mode, not as the long-term production shape for heavy or provider-limited work.

Do not classify an entire module by name. Classify each activity boundary. For example, video generation provider submission/polling is usually `activity-io`, while download/decode/transcode/upload after success is `activity-heavy` plus storage IO. Video evaluation can have the same split.

## 4. Capacity Model

Effective activity capacity is bounded by all of these at once:

```text
replicas
  * per-worker activity slots
  * executor capacity for sync activities
  * poller ability to ingest tasks
  * task queue or worker rate limit
  * provider/backing-store dynamic capacity
  * pod CPU/memory/GPU and local disk pressure
```

Workflow capacity has a different bottleneck set:

```text
replicas
  * workflow task slots
  * workflow task executor/cache capacity
  * workflow task poller behavior
  * workflow history size/replay cost
```

Increasing only Kubernetes replicas is not a complete capacity model. Increasing only SDK slots can also fail if the executor, provider, DB, object store, or pod memory cannot absorb the work.

For provider-backed work, the quota source should be explicit:

| Stage | Source of truth | Worker posture |
| --- | --- | --- |
| current | provider-gateway adaptive runtime feedback: 429, first-pending cursors, pending/completion pace, timeout/5xx, shared in-flight | set fixed slots and low max replicas; do not scale without gateway admission control |
| next | provider-gateway metrics per domain/model family | combine backlog/schedule-to-start with provider `estimated_allowed_concurrency`, `cluster_in_flight`, `first_pending_cursor`, throttle and error metrics |
| final | provider gateway or capacity control plane | cap workflow fan-out, activity slots, and autoscaler max replicas from dynamic capacity |

For DB-backed business work, a transaction-level pool can allow more connection concurrency, but it does not remove transaction, row-lock, idempotency, and write-order limits.

Keep provider-gateway signal ownership explicit:

- Pod-local signals such as DNS failure, TLS/connect timeout, network interruption, upstream unreachable, or AZ-specific network quality belong to the gateway pod's in-memory routing state and guide only that pod's local target choice.
- Cluster-wide signals such as 429, first-pending cursor, accepted/pending pace, shared in-flight, rate-window remaining, upstream throttle, and upstream degraded describe upstream availability for the whole gateway cluster. They should be shared across gateway pods and can be published as quota/capacity view for worker scaling and dashboards.
- A pod-local adaptive target window is a defensive selector state, not a worker autoscaling fact source. The first autoscaling guard should consume cross-pod provider pressure records or a shared capacity snapshot that preserves provider/account/internal-model/upstream-model scope.

## 5. Tuning Order

Tune one knob at a time.

1. Confirm workflow fan-out/windowing and shared-key serialization.
2. Set per-worker fixed slots or WorkerTuner strategy.
3. Align sync activity executor size with activity slots.
4. Set poller behavior.
5. Add provider/backing-store/task queue rate limits or admission control.
6. Increase replicas manually or through HPA/KEDA.
7. Add adaptive feedback loops only after metrics show static windows and slots are insufficient.

Do not mix WorkerTuner/resource-based slot suppliers with legacy `max_concurrent_*` style limits in the same worker. Pick one slot strategy per worker.

Keep the layers separate:

- workflow fan-out windows express release structure and rollout risk
- SDK activity slots and sync executors express per-worker execution capacity
- replicas and pollers express fleet ingestion and horizontal capacity
- provider gateway/admission expresses external provider capacity
- task-queue or provider-domain rate limits protect shared systems

Do not bury provider concurrency in workflow constants. A workflow can choose the next bounded window, but workers and provider gateway should absorb and protect throughput.

## 5.1 Timeout and Wait Boundary

Review timeout as part of topology, not as a local constant.

- Workflow run/execution timeout is not the normal way to express business waiting. Omit it by default, or keep it as a very wide guardrail with owner, SLA meaning, metrics basis, and adjustment/removal condition.
- Workflow task timeout only protects one deterministic workflow task. It does not protect provider calls because provider calls do not belong in workflow code.
- Activity `start_to_close_timeout` protects one activity attempt and one worker slot. It should fit a short submit/query call, bounded finalize/download/upload window, or one bounded shard of work.
- Activity `schedule_to_close_timeout` must not be used as "provider maximum generation time" for queued/running upstream tasks.
- Provider/model SDK and HTTP clients should not own hidden retry or generation-time timeout budgets. Disable SDK/client retries by default and avoid narrow request timeouts; let Temporal activity retry and activity attempt timeout be the visible retry/wait boundary.
- If a transport timeout is unavoidable, keep it limited to short connection/transport hygiene and document why it cannot be represented by the activity attempt timeout. Do not use it as the provider generation wait budget.
- Provider / LLM queued/running waits must be durable workflow state plus timer/sleep/query fallback, or a provider async submit/query/finalize activity split.
- When normal p99/p99.5 execution approaches timeout, or late completion logs appear after Temporal already timed the activity out, split the work or persist shard-level progress before increasing the timeout.

## 6. Metrics Checklist

Capture a baseline before tuning:

- workflow/activity `schedule_to_start` latency
- task queue backlog/count
- worker slots used/available
- poll success/failure and poller count
- workflow sticky cache size and workflow active threads when available
- activity execution latency, failures, retries, timeouts, and heartbeats
- late activity completion / "activity not found on completion" style logs
- workflow completions close to run/execution timeout
- per-provider-call or per-shard identity coverage: target ID, activity name, attempt/shard index, trace context, and provider request/operation ID when available
- provider 429/5xx/timeouts
- provider estimated allowed concurrency, cluster in-flight requests/jobs, first-pending cursor, throttle/degraded state
- DB pool wait, transaction duration, lock wait, transaction failure, deadlock/retry when the project allows DB in that worker role
- object-store latency/errors
- pod CPU, memory RSS, OOM, restarts, local disk/tmp usage
- GPU/model utilization when relevant

## 7. Rollout Checklist

- Record baseline metrics before changing slots, windows, or replicas.
- Change one capacity knob per rollout.
- Define rollback thresholds such as provider error spikes, DB pool wait, OOM/restarts, or schedule-to-start not improving.
- Run replay/verify before deployment when workflow code, activity names, task queues, or DTOs changed.
- If a rollout changes workflow windowing, scheduling order, child workflow IDs, activity names, or durable shard state transitions, state the replay, patching, or Worker Versioning plan before deployment.
- Keep minimum replicas for workflow/control queues unless scale-to-zero has been explicitly reviewed.
- Configure termination grace and scale-down stabilization for long activities.
- State the autoscaling phase in the review: current manual posture, first KEDA/Temporal backlog pilot, later Prometheus/HPA multi-metric posture, and final dynamic provider-capacity posture.
- For KEDA pilots on provider-backed activity queues, combine Temporal backlog with a Provider Gateway global pressure guard as one composite metric. Do not let independent triggers scale up on backlog when the provider guard says the upstream is already pressured.

## 8. Anti-patterns

- Treating Pod replicas as the only capacity model.
- Hiding long-term concurrency in workflow constants.
- Treating the workflow fan-out window as the sole throughput control instead of a rollout strategy.
- Wrapping many independent LLM/provider calls in one coarse stage activity.
- Emitting provider request/operation IDs as public progress noise instead of internal observability.
- Putting worker/static capacity settings in public workflow input.
- Using multi-container Pods for roles that need independent scaling.
- Running CPU-heavy activities on an async event loop.
- Raising activity slots without provider-gateway admission control or backing-store protection.
- Treating provider quota as a static worker/module config constant.
- Allowing an algo worker to add DB access when the project boundary reserves DB writes for business workers.
- Tuning without schedule-to-start, slot, retry, and resource metrics.
- Using workflow run timeout as a near-normal business deadline for durable provider-heavy workflows.
- Using long activity timeouts to hide provider queueing, LLM generation, or multi-shard batch work.
- Moving every worker role to a separate image when multiple Deployments with one image would preserve the boundary.
