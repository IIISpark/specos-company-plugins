# Unsupported Or Workspace-Level Notion CLI Work

Use this reference for `ntn notion-as-code`, `ntn workers`, `ntn update`, or a command absent from
the routed references.

- First run the selected command's `--help` and identify whether it changes remote content, local
  configuration, credentials, generated files, or CLI version.
- `ntn update` changes local software and requires explicit authorization. Do not update merely to
  obtain a feature.
- Notion-as-code and workers can change managed workspace state or generate local artifacts. Keep
  any proposal bounded to the user-specified workspace and await explicit confirmation before an
  apply, publish, or generation that overwrites files.
- If the CLI's current behavior is unclear, report the missing fact and stop rather than relying on
  an older command guide or calling an arbitrary API.

For repeatable repository documentation, use the repository's normal docs workflow; Notion is not
the source of truth unless the user explicitly says so.
