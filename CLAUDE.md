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

See `README.md` for install, update, validation, and maintainer workflows.
