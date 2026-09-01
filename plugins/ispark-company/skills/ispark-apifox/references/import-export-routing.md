# Apifox Import And Export

Use this reference for OpenAPI, Postman, HAR, Swagger, or Apifox-native import/export, migration,
backup, and automatic-import work. Test-scenario step imports belong to `test-scenario`, not here.

## Before Import

1. Search the repository for its maintained OpenAPI or schema generator before writing a route scraper.
2. Preserve the original generated artifact. Parse content as JSON or YAML instead of trusting its
   extension.
3. For OpenAPI, calculate actual `paths`, operations, schemas, write operations, writes with bodies,
   and empty object bodies.
4. Judge completeness in context. Many write operations with few schemas, missing bodies, or empty
   objects indicate a route skeleton; do not import it as the final contract.
5. Check business-oriented tags, readable operation IDs, summaries, descriptions, and preserved
   schemas. Mechanical URL-path tags are not a useful final navigation model.
6. Confirm target project, module strategy, matching/overwrite behavior, and whether a clean temporary
   project is required. Do not trial repeatedly in an established project.

Import and automatic-import change remote state. Preview the source, strategy, expected counts, and
overwrite behavior, then obtain explicit confirmation.

## Native Project Migration

- Default name matching is appropriate only when source module names uniquely identify intended target
  modules. Use explicit module mapping when names are duplicated or placement matters.
- Choose new-module behavior only when the user wants a separate copy. Partial maps must leave a clear
  rule for unmapped modules.
- After import, check module count plus API, schema, case, scenario, WebSocket, Socket.IO, and suite
  references that are in scope. A large ignored count is a risk signal, not ordinary success.

## Export And Verification

- Confirm format, scope, included test assets, destination, and whether export is for migration,
  backup, review, or publication.
- Keep the artifact in `.tmp/` or `working-delta/` unless the repository defines another approved
  location. Do not overwrite an existing artifact without confirmation.
- Verify existence, non-trivial size, parseability, expected counts, and at least one representative
  read and write endpoint. For migration artifacts, test import in an authorized clean project before
  calling them portable.
- Report source, target, actual quality metrics, import/export counts, sampled readback, ignored items,
  module behavior, and remaining risks.
