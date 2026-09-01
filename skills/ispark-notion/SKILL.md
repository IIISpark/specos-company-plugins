---
name: ispark-notion
description: Use for Notion `ntn` CLI tasks: authentication checks, scoped page or data-source reads, page edits, file uploads, diagnostics, and authorized API calls. Do not use for Feishu/Lark, generic web browsing, or unrelated documentation work.
---

# ISpark Notion

Use this for Notion work through the local `ntn` CLI. Do not use it for Feishu/Lark,
generic web browsing, or prose-only documentation work.

## Route

- Authentication state, login, logout, or diagnostics: read `references/auth-routing.md`.
- Read, create, edit, or archive a page: read `references/pages-routing.md`.
- Resolve or query a data source: read `references/datasources-routing.md`.
- Inspect or upload a Notion file: read `references/files-routing.md`.
- Call an API endpoint not covered by a dedicated command: read `references/api-routing.md`.
- Notion-as-code, workers, CLI updates, or unsupported commands: read `references/workspace-routing.md`.

## Defaults

- Write user-facing summaries, confirmations, and failures in Simplified Chinese.
- Use `ntn --help` and the selected subcommand's `--help` for current flags. Do not install,
  update, log in, or configure `ntn` unless the user explicitly authorizes that operation.
- Never print credentials, session material, raw internal identifiers, complete API responses, or
  private page content beyond the user's stated scope. Do not run `ntn auth token`.
- Keep user-approved local exports and diagnostics under `working-delta/` or `.tmp/`; do not
  upload, attach, or expose them without explicit approval.
- For reads, request the smallest useful result. Paginate only when the user asks for all results
  or explicitly asks to continue after the first page. Disambiguate multiple page or data-source
  matches rather than choosing one.
- Require a new, explicit confirmation immediately before page creation or editing, archiving,
  file upload, arbitrary API mutation, logout, or any action that changes Notion or local auth
  state. State the exact intended effect first; never self-confirm.

Use `$ispark-lark` for Feishu/Lark resources and `$ispark-writing` for prose-only drafting or revision.
