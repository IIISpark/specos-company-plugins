# Apifox Endpoint Test Cases

Use this reference for a test case bound to one endpoint, its category, test data, request content,
processors, assertions, extractors, and direct execution. Multi-step workflows belong to test scenarios.

## Create Or Update

1. Confirm project, branch, endpoint, environment, and intended side effects.
2. Resolve a valid category through the current category command. A valid category is required for
   reliable client visibility; do not invent one.
3. Read a similar case when available, then obtain the current create/update schema.
4. Build a complete case rather than a name-only shell. On update, start from full readback because
   update is not JSON Patch and arrays may be replaced rather than merged by ID.
5. Validate structure, preview the mutation, confirm, write once, and read the case back.

## Content Rules

- Keep request body content in the representation required by the current schema. Preserve multiline
  formatting for client readability without changing runtime semantics.
- Use the current flat processor shape and stable processor IDs. Do not revive older nested formats.
- Prefer visual assertions for status, JSON fields, and text checks. Use custom scripts only for logic
  the visual assertion model cannot express, and wrap script assertions in the supported test API.
- Do not copy test-scenario step references, loops, or cross-step variables into a single-endpoint case.
- Do not treat an endpoint response example as a test assertion.

## Verification

- Readback proves persistence, not execution. Verify that request content, processors, assertions, and
  extractors are present at the expected level.
- Run a case only when the user authorizes execution and the environment is known. Prefer an explicit
  non-production environment and a local structured report.
- Uploading a report is a separate remote side effect requiring confirmation.
- If CLI readback exists but the client does not show the case, check project, branch, endpoint,
  category, filters, and saved structure before rebuilding it.
