# Apifox API Lifecycle

Use this only for a request that spans several Apifox domains, such as designing APIs, adding mocks and
tests, exporting documentation, and preparing a branch for merge.

## Delivery Order

1. Confirm authority: project, branch, source facts, delivery scope, environment, and permission model.
2. If source code or documents must become OpenAPI, apply the import/export quality gate before import.
3. Define reusable schemas, responses, security, and environment boundaries before dependent endpoints.
4. Align endpoints, examples, and mocks; read back and perform an export smoke check.
5. Add complete endpoint cases. Add scenarios only for genuine cross-step workflows.
6. Run only the explicitly authorized tests in a known environment and collect local evidence; upload
   reports only when requested.
7. Export or publish only the requested artifact and verify its scope.
8. In an AI branch, preview the merge impact and obtain separate confirmation for MR or merge.

Load only the domain reference for the current step. Do not preload every Apifox reference merely because
the overall request is broad.

## Acceptance

Report saved-resource readback, representative OpenAPI export health, test execution evidence, artifact
scope, branch state, and unresolved risks separately. Do not conflate API-definition success, environment
readiness, test correctness, report upload, client rendering, or merge completion.
