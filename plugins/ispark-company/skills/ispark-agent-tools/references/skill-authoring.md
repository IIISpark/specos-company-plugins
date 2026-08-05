# Skill Authoring

Company skill rules:

- folder name equals `name`
- use `ispark-` prefix for published company skills
- keep `SKILL.md` short and route to `references/`
- put scripts in `scripts/` and assets in `assets/`
- avoid README/extra docs inside individual skill folders
- no personal paths or secrets
- treat the frontmatter description as the lightweight discovery index: front-load the
  task triggers and ownership boundary
- add `agents/openai.yaml` and set `policy.allow_implicit_invocation: true` explicitly
  for every published company skill; `$skill-name` is an override, not a prerequisite
- keep detailed methods in directly linked `references/` files so they load only after
  skill routing
- validate with `tools/validate.ps1`

Use forward testing for complex or high-risk skills before making them stable.
