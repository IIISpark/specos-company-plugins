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
- Keep every discovery `description` at or below 280 characters; move detail to on-demand references.
- Use descriptions as the discovery index and explicitly allow implicit invocation;
  load full instructions and references only after routing.
- Preserve personal skills: installers manage only `ispark-*` folders.
- Anti-slop is layered: use `ispark-anti-slop` to route, then let writing, academic,
  architecture-diagrams, data-visualization, product-design, browser-QA, dev-workflow,
  and review-risk skills own their boundaries.
- Chinese pattern inventories load only for explicit anti-slop work; ordinary Chinese
  writing keeps the shorter fact, register, and sentence-relation guidance.
- Tencent Meeting operations use the separately routed `ispark-tmeet` skill; Feishu/Lark
  meeting work remains with `ispark-lark`.
- Notion CLI work uses the separately routed `ispark-notion` skill; it does not share
  Feishu/Lark authentication, page, or data-source semantics.
- Apifox CLI/MCP work uses the separately routed `ispark-apifox` skill; its contract,
  test, import/export, automation, and branch details load only for the selected operation.
- Broad codebase scouting and React/Next performance have narrow entry skills; React
  visualization integration and TypeScript visualization contracts load through on-demand
  references under React performance and dev workflow rather than new overlapping owners.
- Evidence-bearing charts, maps, dashboards, statistical graphics, and data-bearing diagrams
  use `ispark-data-visualization`; product/UI direction, browser acceptance, and React
  performance remain with their existing owners. UML, C4, ERD, BPMN, sequence/state, and
  software architecture views use `ispark-architecture-diagrams`. Details load on demand.
- Keep reusable skill templates project-neutral: use placeholders for namespaces, hosts,
  paths, headers, and deployment labels; target-repository facts supply real values.
- Validate every distributable skill text file for personal homes/emails, concrete internal
  hosts, and downstream project/runtime markers. Manifest author fields are public package
  metadata outside the skill-payload privacy scan.

See `README.md`, `docs/anti-ai-slop-integration.md`, and
`docs/candidate-skill-integration.md` for install, validation, and method boundaries.
