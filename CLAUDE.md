# ISpark SpecOS Company Plugins

Shared source repository for the `ispark-company` Codex plugin. It contains Python 3.12-compatible maintenance helpers and Markdown-based company skills.

## Structure

- `skills/`: maintained skill sources.
- `profiles/`: fallback direct-install role profiles.
- `plugins/ispark-company/`: generated marketplace snapshot.
- `tools/`: build, validation, install, and profile-sync helpers.
- `docs/releases/unreleased/`: source release entries for meaningful changes.

## Commands

```powershell
python tools/validate.py
python tools/prepare_publish.py
python tools/sync_profile.py --action dry-run --profile engineer
```

## Decisions

- Edit `skills/` and rebuild the plugin snapshot; never maintain installed caches.
- Keep each `SKILL.md` short and route detailed guidance to `references/`.
- Use descriptions as the discovery index and explicitly allow implicit invocation;
  load full instructions and references only after routing.
- Preserve personal skills: installers manage only `ispark-*` folders.
- Anti-slop is layered: use `ispark-anti-slop` to route, then let writing, academic,
  product-design, browser-QA, dev-workflow, and review-risk skills own their boundaries.
- Chinese pattern inventories load only for explicit anti-slop work; ordinary Chinese
  writing keeps the shorter fact, register, and sentence-relation guidance.
- Tencent Meeting operations use the separately routed `ispark-tmeet` skill; Feishu/Lark
  meeting work remains with `ispark-lark`.
- Notion CLI work uses the separately routed `ispark-notion` skill; it does not share
  Feishu/Lark authentication, page, or data-source semantics.
- Apifox CLI/MCP work uses the separately routed `ispark-apifox` skill; its contract,
  test, import/export, automation, and branch details load only for the selected operation.
- Broad codebase scouting and React/Next performance have narrow entry skills; planning,
  TDD, debugging, review, verification, and subagent methods stay with existing owners.
- Keep reusable skill templates project-neutral: use placeholders for namespaces, hosts,
  paths, headers, and deployment labels; target-repository facts supply real values.

See `README.md`, `docs/anti-ai-slop-integration.md`, and
`docs/candidate-skill-integration.md` for install, validation, and method boundaries.
