# Apifox Contracts, Schemas, Examples, And Mocks

Use this reference for endpoints, parameters, request/response bodies, shared schemas, reusable
responses, security schemes, examples, mocks, folders, and contract alignment.

## Authority And Order

- Establish intended behavior from code, IDL, validators, tests, and ratified product requirements.
  Apifox is a maintained contract surface, not evidence that stale behavior is correct.
- Confirm project and branch, read the current endpoint and referenced components, then align semantic
  contract before examples, mocks, or test cases.
- Create reusable schemas, response components, and security schemes before endpoints that reference
  them. Keep environment values out of common parameters.
- Preserve useful descriptions. Replace only incorrect, missing, or structurally broken content.

## Examples And Mocks

- Use request examples only where a body or parameter exists. Keep scalar parameter examples scalar.
- Put stable field examples close to schemas; use deterministic mock rules for IDs, enums, dates, and
  ranges. Use branchy mock scripts only for behavior such as conflict, expiry, authorization, or
  idempotency.
- Prefer visual assertions and field-level mock rules over custom scripts when they express the same
  behavior. Scripts must be deterministic and driven by obvious inputs.
- No-body endpoints must not gain an invented body merely to hold an example.

## Verification

- Re-read each changed endpoint and component in the same project and branch.
- Export a representative OpenAPI slice after non-trivial schema work. Confirm schemas remain objects,
  references resolve, media types are correct, and request/response shapes were not degraded.
- A successful write does not prove export health, client rendering, mock behavior, or runtime tests.
- If a schema is stored as a JSON string or export becomes a plain string body, repair the source model
  before further refactoring. Do not add a downstream adapter that hides the malformed contract.
- Delete a component only after both export references and endpoint-level references prove it unused,
  and only after explicit confirmation.

If the selected MCP surface cannot express an operation, prefer the official CLI. Use raw OpenAPI/API
fallback only for an exact authorized operation and verify it through the normal read surface.
