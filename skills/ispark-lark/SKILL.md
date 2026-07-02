---
name: ispark-lark
description: Use when working with Feishu/Lark/Doubao collaboration resources, including docs, drive files, sheets, base, wiki, slides, IM, calendar, tasks, minutes, meetings, mail, approvals, contacts, apps, or Lark OpenAPI gaps.
---

# ISpark Lark

Use this as the company Lark router. Read the narrowest reference before calling Lark tools.

## Route

- Auth, scope, identity: read `references/shared.md`.
- Docs/Drive/Sheets/Base/Wiki/Slides/Markdown: read `references/content.md`.
- IM/Contact/Calendar/Task/VC/Minutes/Note/Mail: read `references/collaboration.md`.
- Apps, events, approvals, attendance, OKR, whiteboard, OpenAPI gaps: read `references/advanced.md`.

## Defaults

- Write generated documents, summaries, meeting notes, and collaboration reports in Simplified Chinese unless the destination document or recipient context explicitly requires another language.
- When exporting or staging local files before upload/import, use the repo's `working-delta/`, `.tmp/`, or `tmp/` conventions instead of assistant-specific document folders.
- Route by URL path, token shape, and requested operation, not domain alone.
- If a resource embeds another resource type, switch references after extracting the token.
- For visible or destructive operations, summarize target and intended effect before acting.
