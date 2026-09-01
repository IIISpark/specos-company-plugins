---
name: ispark-tmeet
description: "Use for Tencent Meeting `tmeet` CLI tasks: OAuth status, scheduling, meeting lookup, recordings, participant reports, in-meeting control, and scoped troubleshooting. Contact lookup is allowed only to invite or call someone into a meeting, never for standalone people search."
---

# ISpark Tencent Meeting

Use this for Tencent Meeting CLI operations. Do not use it for Feishu/Lark meetings,
generic contact lookup, or non-meeting calendar work.

## Route

- Authentication, CLI availability, and safe status output: read `references/auth-routing.md`.
- Create, change, cancel, find meetings, or manage invitees: read `references/meetings-routing.md`.
- Find recordings, minutes, transcripts, playback, or request recording access: read `references/recordings-routing.md`.
- Read participants, waiting-room records, or export attendee details: read `references/reports-routing.md`.
- Resolve a person only for a pending invitation or in-meeting call: read `references/contacts-routing.md`.
- Call, remove, or move people in a live meeting: read `references/live-control-routing.md`.
- Export local diagnostics or prepare platform feedback: read `references/troubleshooting-routing.md`.

## Defaults

- Write user-facing meeting summaries, confirmations, and error explanations in Simplified Chinese.
- Use `tmeet --help` and the selected subcommand's `--help` for current flags; do not invent
  CLI parameters or install packages automatically. If `tmeet` is unavailable, state the
  missing prerequisite and wait for the user to authorize installation.
- Keep temporary, user-approved exports and local diagnostic artifacts under `working-delta/`
  or `.tmp/`; do not upload, attach, or expose them without explicit approval.
- Never print credentials, raw tokens, internal IDs, phone numbers, email addresses, or raw
  command JSON. Keep internal identifiers in tool calls only; summarize meetings to users with
  the meeting code and necessary public fields.
- For read commands, request compact output when the CLI supports it. Paginate only when the
  user asks for all results or explicitly asks to continue after the first page.
- Ask for missing required information and disambiguate multiple matches. Do not select a
  person or a meeting from several candidates on the user's behalf.
- Require a new, explicit user confirmation before cancellation, material meeting changes,
  invitee changes, calls, removals, waiting-room moves, logout, recording-access submission,
  log upload, or platform feedback. Show the intended effect first; never self-confirm.

Use `$ispark-lark` for Feishu/Lark meeting records and `$ispark-release-ops` for release
operations unrelated to Tencent Meeting.
