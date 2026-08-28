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

For behavior-enforcing skills, use a process RED/GREEN/REFACTOR gate: run pressure
scenarios without the skill, capture the exact failure or rationalization, add the
smallest counter-rule, re-run with the skill, then close newly discovered loopholes.
Three or more combined pressures are required when the skill can be rationalized away.
Passing frontmatter or snapshot validation proves packaging, not behavioral compliance.

When absorbing an external skill collection, decide in this order:

1. Merge the method into an existing owner when the trigger and outcome already belong there.
2. Create a new skill only for a distinct, recurring task with a discriminating description.
3. Keep a source as research-only when its runtime, credentials, license, or autonomous
   behavior would broaden company authority or context cost.

Record provenance and license decisions, but rewrite guidance around ISpark contracts
instead of copying a repository wholesale. Test positive routing, nearby negative
boundaries, reference reachability, and generated snapshot equality.
