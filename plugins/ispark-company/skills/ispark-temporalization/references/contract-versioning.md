# Contract Versioning

## 1. Purpose

Use this reference when a temporalization task touches any of these:

- workflow input or workflow result DTOs
- activity input or activity result DTOs
- `document ref` or `artifact ref` envelopes
- Data Converter / Codec evolution
- rollout compatibility between older runs and newer workers

This file is about business-wire compatibility, not deterministic workflow branching. For deterministic workflow branching and rollout safety, also use replay, Worker Versioning, and patching.

Treat public workflow input/output files as API contracts. They should describe stable caller intent and result shape, not the current provider SDK request body or a local implementation DTO.

Activity DTOs can be internal, but they still cross workflow history and worker rollout windows. Treat their compatibility deliberately, especially when a DTO represents an LLM/provider/model call or shard.

## 2. Separate the Four Version Axes

Do not collapse these into a single vague "version" concept:

1. workflow code version
2. wire schema version
3. stored-object schema version
4. business content version

Recommended ownership:

- workflow code version:
  - replay
  - Worker Versioning
  - patching
- wire schema version:
  - workflow/activity DTO compatibility policy
- stored-object schema version:
  - `schema_version`
- business content version:
  - `content_version`, `revision`, or equivalent domain concept

## 3. Default Compatibility Policy

Default to additive, backward-compatible change for wire DTOs.

Preferred changes:

- add optional fields
- add metadata fields with safe defaults
- widen readers to accept older representations

Treat these as breaking unless there is an explicit transition window:

- removing a field
- renaming a field
- changing the semantic meaning of a field
- changing enum meaning
- changing retry or timeout meaning that callers rely on
- changing result shape in a way old readers cannot safely interpret

## 4. Reader/Writer Rule

During rollout:

- new readers should accept old payloads
- new writers may emit the new shape only when downstream readers can safely consume it

Practical rule:

- readers must be more compatible than writers

This matters even for activities:

- activities are not replay-determinism sensitive in the same way workflows are
- but a new activity worker can still receive input emitted by an older workflow run

## 5. When to Introduce a New Contract Name

Prefer a new activity or workflow name instead of in-place mutation when:

- input meaning changes materially
- output meaning changes materially
- side-effect timing changes materially
- retry behavior changes materially
- activity resource profile or provider-call granularity changes materially
- a coarse stage activity is split into provider logical calls or bounded shards
- old runs would keep sending payloads the new code cannot safely interpret

Examples:

- `GeneratePromptV2Activity`
- `materialize_v2`
- `TaskBWorkflowV2`

Reserve in-place DTO evolution for clearly compatible changes.

Internal activity DTO changes should still be additive by default. Adding optional diagnostic fields such as `target_id`, `shard_index`, `traceparent`, or a nullable provider request/operation ID is compatible when old handlers can ignore them and new handlers can tolerate absence.

Do not silently redefine activity DTO identity fields. Target identity, shard identity, idempotency key, provider operation identity, and retry classification affect rerun behavior and observability; changing their meaning requires an explicit compatibility window or a new activity name.

## 5.1 Provider-Specific Knobs vs Stable Capabilities

Do not promote provider/model-specific parameter names into public workflow DTOs unless the provider itself is the stable product contract.

Prefer stable capability-level fields that adapters can map to provider-specific parameters.

Example:

- avoid `vidu_q3_enable_audio`
- prefer an output requirement such as `video_audio = "disallow" | "allow_generated" | "require_generated"`

The public field should answer what the caller is asking the product to permit or require. The adapter decides how, whether, or with what warning that maps to Vidu, Veo, MiniMax, or another backend.

When a provider-specific option is genuinely experimental, put it behind a namespaced, ignorable extension with an explicit expiry or promotion plan. Do not let `extra: dict[str, Any]` become the long-term contract.

## 6. Recommended Envelope Fields

### 6.1 Workflow and Activity DTOs

For long-lived or rollout-sensitive DTOs, prefer an explicit envelope:

```json
{
  "schema_version": "1.2",
  "payload": {
    "...": "..."
  }
}
```

Use `schema_version` when:

- the DTO crosses workflow/activity boundaries
- the DTO may survive a rollout window
- the DTO will be read by more than one worker build over time

If meaning can evolve independently of shape, add `content_version`:

```json
{
  "schema_version": "1.2",
  "content_version": 7,
  "payload": {
    "...": "..."
  }
}
```

### 6.2 Object References

For `document ref` / `artifact ref`, prefer:

```json
{
  "kind": "artifact_ref",
  "schema_version": "1.0",
  "content_version": 3,
  "data_type": "example_package",
  "project_id": "p1",
  "owner_id": "r1",
  "snapshot_id": "01HXYZ...",
  "path_segments": ["sections", "output.json"],
  "retention_class": "durable"
}
```

Recommended meanings:

- `kind`:
  - identifies the envelope family
- `schema_version`:
  - how to parse the envelope
- `content_version`:
  - which revision of the underlying content this refers to
- `path_segments`:
  - logical member path, kept adapter-neutral instead of hardcoding a slash-joined storage key
- `retention_class`:
  - lifecycle expectation such as `durable` or `ephemeral`

Do not model worker/static environment configuration as a public object ref by default.
If a repo persists immutable run-preparation metadata, treat it as a module-owned internal document unless it is explicitly promoted to a stable business object with clear reader/writer ownership.

## 7. Recommended Transition Pattern

For a breaking DTO change:

1. widen reader first
2. keep old reader path alive through rollout
3. introduce new writer path
4. drain old runs
5. remove old reader later

For a breaking workflow branching change:

1. protect determinism with patching or Worker Versioning
2. replay old histories
3. roll out new workers
4. retire old code path only after the protected window closes

For workflow code-shape changes around LLM/provider fan-out:

1. identify whether scheduling order, activity names, child workflow IDs, windowing state, or durable shard commit state changes
2. choose patching, Worker Versioning, or a separate workflow name before rollout
3. replay histories that include partial success, shard failure, retry, and rerun/skip paths
4. keep old activity handlers available while older runs can still schedule them

## 8. Data Converter and Codec Changes

Treat Data Converter / Payload Codec changes like infrastructure compatibility changes.

Do not assume a converter upgrade is safe just because DTO code compiles.

Before changing converters/codecs:

- verify old histories can still be decoded
- verify replay still passes
- record whether old payloads remain readable

If the converter or codec change is not backward-readable, treat it as a rollout blocker.

## 9. Questions to Answer Before Merging

- Is this a workflow-code change, a DTO-schema change, or both?
- Is the change additive or breaking?
- Can new workers still read payloads emitted by old runs?
- Should this become a new activity/workflow contract name?
- Does this change activity retry value, side-effect/resource profile, provider-call granularity, or durable shard identity?
- Does replay cover fan-out windowing, partial success commit, failure isolation, and rerun skip behavior?
- Do these DTOs need explicit `schema_version` and `content_version`?
- Does replay cover the workflow-code part of the change?
