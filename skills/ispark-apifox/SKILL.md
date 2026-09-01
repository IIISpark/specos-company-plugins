---
name: ispark-apifox
description: Use for Apifox CLI or MCP work: API contracts, schemas, examples, mocks, imports, exports, test cases, scenarios, automation, reports, branches, and API lifecycle governance. Do not use for generic API implementation or prose-only docs.
---

# ISpark Apifox

Use this for Apifox project work through the current `apifox` CLI or an authorized Apifox
MCP/OpenAPI surface. Do not use it for generic API implementation or prose-only documentation.

## Route

- CLI availability, authentication, project selection, schemas, and safe writes: read `references/cli-routing.md`.
- Endpoints, shared schemas, examples, mocks, folders, and contract alignment: read `references/contracts-routing.md`.
- OpenAPI/Postman/Apifox import, export, migration, or quality gates: read `references/import-export-routing.md`.
- Single-endpoint test cases and test data: read `references/test-case-routing.md`.
- Multi-step test scenarios, variables, processors, and cleanup: read `references/test-scenario-routing.md`.
- Suites, scheduled tasks, runners, CI execution, and reports: read `references/automation-routing.md`.
- Branches, AI branches, pick-to, merge, or merge requests: read `references/branches-routing.md`.
- Success-but-missing resources, version drift, display, or report failures: read `references/troubleshooting-routing.md`.
- End-to-end delivery across several of these domains: read `references/lifecycle-routing.md`, then only the referenced domain files needed for the current step.

## Defaults

- Write user-facing summaries, confirmations, and failures in Simplified Chinese.
- Treat current `apifox <command> --help`, `cli-schema`, structured result fields, and readback as
  runtime facts. Do not invent flags, payloads, hidden aliases, project IDs, branches, or environments.
- If the CLI is absent, report the prerequisite. Do not install, update, log in, switch accounts,
  write local configuration, or request a token unless the user explicitly authorizes that action.
- Never print credentials, raw internal IDs, private deployment addresses, complete payloads, or full
  project responses. Keep approved generated specs and reports under `working-delta/` or `.tmp/`.
- Reads must stay within the user-authorized project and branch. Paginate only when the user asks for
  all results or explicitly continues after the first page.
- Before any write, establish project, branch, resource, exact effect, and verification. Validate
  structured payloads when supported, show a compact preview, then obtain a new explicit confirmation.
- Require separate confirmation for create/update/delete/archive, import, test execution with side
  effects, report upload, runner or scheduled-task changes, branch creation/pick-to, merge, and MR actions.

Use `$ispark-dev-workflow` for source-code implementation and `$ispark-docs-issues` for durable local docs.
