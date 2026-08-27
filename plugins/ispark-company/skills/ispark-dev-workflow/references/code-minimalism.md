# Minimal Code And Failure Visibility

Use this reference when reviewing or changing generated code, especially when the complaint is that the implementation has an "AI 味": too many helpers, wrappers, defaults, retries, or compatibility branches.

## First locate the real defect

Inspect the smallest relevant call path, contract, configuration, and tests. Identify the exact failure or requirement, where the invalid state first appears, and which component owns that state. Fix that source before adding tolerance downstream.

## Valid safeguards versus speculative branches

Keep safeguards that enforce a real boundary: input validation, authentication and authorization, tenant isolation, schema validation, explicit timeouts, bounded retries for documented recoverable failures, transactions, cleanup, concurrency controls, and fail-closed security behavior.

Treat each new `try/catch`, null check, default, retry, fallback, legacy branch, wrapper, `return []`, `return {}`, or exception-to-success conversion as a decision that needs evidence. Ask:

1. Which observed failure or contract requires it?
2. What would the caller observe without it?
3. Does it hide an upstream defect or change public semantics?
4. Is the branch covered by a focused test?

If the answer is hypothetical, do not add the branch. Do not turn missing identity, invalid configuration, persistence failure, or a violated invariant into an anonymous user, empty result, or success response.

## LLM and external boundaries

Validate model and third-party output against an explicit schema. Reject or visibly degrade invalid output according to the existing contract. Do not guess missing fields, fabricate tool results, retry authentication or deterministic validation failures, or let an optional sidecar change the primary business result.

## Completion report

After implementation, report the root cause, exact modified scope, failure policy, every new defensive branch with its justification, and the checks that exercised it. Explicitly state when no speculative safeguards, unrelated refactor, new configuration, dual write, or deployment action was added. Write handoff material in Simplified Chinese by default; keep temporary notes under `working-delta/` and disposable output under `.tmp/` or `tmp/`.
