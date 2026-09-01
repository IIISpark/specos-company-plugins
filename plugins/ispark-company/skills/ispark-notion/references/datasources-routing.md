# Notion Data Sources

Use this reference for `ntn datasources resolve` and `ntn datasources query`.

## Scope The Query

- Resolve a data source from an exact ID, database ID, or Notion URL supplied by the user.
- Before querying, identify the authorized data source, required properties, filter, sort order,
  and small result limit. Do not explore unrelated databases to discover candidates.
- Fetch the first useful page of results. Continue with a cursor only when the user asks for all
  records or explicitly requests the next page.

## Handle Results Carefully

- Data-source rows may contain private people, project, or operational data. Summarize only the
  requested fields and do not print raw JSON or internal IDs.
- If filters could produce materially different interpretations, ask for the missing criterion
  rather than selecting a broad default.
- `ntn datasources` is read-oriented in the local CLI. Route record creation or mutation through
  the exact supported command or the authorized API reference; do not invent an update command.

Use `$ispark-lark` for Feishu Base or Sheets, which are separate systems.
