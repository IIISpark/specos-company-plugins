# ISpark SpecOS Company Plugins

This repository is the shared source of truth for ISpark SpecOS Codex capabilities.
It currently publishes the `ispark-company` Codex plugin, which contains company-level
skills for Agent Harness, engineering workflow, product design, release operations,
writing and editorial quality, Lark collaboration, evidence-based hiring, review,
debugging, browser QA, and Temporal worker work.

`DramaWork` or `短剧大师` may appear in downstream workspaces, but they are not this
repository's identity. The maintainer identity is `ISpark SpecOS`.

## What This Repository Provides

```text
.agents/plugins/        Repo marketplace catalog for Codex
plugins/ispark-company/ Published Codex plugin bundle
skills/                 Source skills copied into the plugin snapshot
profiles/               Fallback direct-install role profiles
tools/*.py              Cross-platform install, update, validation, and publish helpers
tools/*.ps1             PowerShell wrappers for Windows users
```

The plugin path is the default distribution path. The profile sync helper is only a
fallback when plugin installation is unavailable or a teammate explicitly needs direct
skill-root copies.

## Install From GitHub

Use this path after the repository is available at:

```text
https://github.com/IIISpark/specos-company-plugins
```

Install the marketplace and plugin:

```bash
codex plugin marketplace add IIISpark/specos-company-plugins --ref main
codex plugin add ispark-company@ispark-company
```

Then restart Codex or open a new thread.

PowerShell helper:

```powershell
.\tools\install-or-update.ps1 -Action install
```

Cross-platform helper:

```bash
python tools/install_or_update.py --action install
```

## Update

When SpecOS publishes a new version:

```bash
codex plugin marketplace upgrade ispark-company
codex plugin add ispark-company@ispark-company
```

Then restart Codex or open a new thread.

PowerShell helper:

```powershell
.\tools\install-or-update.ps1 -Action update
```

Cross-platform helper:

```bash
python tools/install_or_update.py --action update
```

## Confirm Installation

```bash
codex plugin marketplace list
codex plugin list
```

Expected facts:

- marketplace `ispark-company` is configured
- plugin `ispark-company@ispark-company` is installed and enabled
- a new Codex thread shows `ispark-company:*` skills

Helper:

```bash
python tools/install_or_update.py --action status
```

## Discovery And Loading Model

The company plugin is index-first and uses Codex progressive disclosure:

- after the installed plugin is enabled, its bundled skills become eligible for a new
  chat or CLI session's lightweight name, description, and path index; the host may
  shorten a very large global skill list to fit its context budget
- every published company skill explicitly sets `allow_implicit_invocation: true`, so
  Codex can select it from the task intent; users do not need to type `$skill-name`
- `$skill-name` remains available as an explicit override for testing or precise routing
- Codex loads the selected skill's full `SKILL.md` only after selection, and the skill
  then reads only the references needed for the task

Editing this repository is not an installed plugin update. Rebuild the plugin snapshot,
bump and publish or otherwise install a distinct plugin version, and start a new chat or
CLI session before judging discovery. A running session may continue using the version
it indexed at startup. This follows OpenAI's
[skill loading model](https://developers.openai.com/codex/skills).

## Private Repository Access

If the GitHub repository is private, the teammate's local Git/Codex environment must be
able to clone `IIISpark/specos-company-plugins`. Resolve GitHub authentication first,
then rerun the install command. Do not put personal tokens in this repository.

## Role And Profile Guidance

Default plugin installation currently installs the shared company plugin as one bundle.
This is the recommended path for most teammates.

Fallback profiles exist for direct skill-root installs:

- `engineer`
- `backend`
- `frontend`
- `ops`
- `product`
- `agent-maintainer`
- `dramawork`

Use fallback sync only when plugin installation is unavailable:

```bash
python tools/sync_profile.py --action dry-run --profile engineer
python tools/sync_profile.py --action sync --profile engineer
python tools/sync_profile.py --action status
```

PowerShell:

```powershell
.\tools\sync-profile.ps1 -Action DryRun -Profile engineer
.\tools\sync-profile.ps1 -Action Sync -Profile engineer
.\tools\sync-profile.ps1 -Action Status
```

The sync helper only manages `ispark-*` folders. It must not edit or delete personal
skills with other names.

If we later need true role-specific plugin subsets, prefer separate plugins or marketplace
entries such as `ispark-specos-engineering`, `ispark-specos-product`, or
`ispark-specos-ops` instead of asking teammates to manually delete bundled skills.

## Writing And Frontend Craft

`ispark-writing` owns reader-facing prose quality across company documents, PRDs,
decision notes, release communication, collaboration messages, and product copy. It
supports draft, fact-preserving rewrite, report-only audit, and audience/channel
adaptation. Artifact structure, source-of-truth placement, release state, collaboration
side effects, and product decisions remain with their existing owning skills.

`ispark-product-design` includes a scoped frontend craft method for anti-template design,
report-only visual audit, bounded redesign, and screenshot/URL design study. Real frontend
acceptance still routes through `ispark-browser-qa`.

Both areas adapt selected methods from Hallmark at pinned upstream commit
`0a0f706bc0289fef76a07fb854a6a5b031c57901`. The distributed skill references include the
MIT notice and ISpark modification boundary. The company plugin does not vendor Hallmark's
theme catalog, `.hallmark/` state, source stamps, or tool assumptions.

## Maintain And Publish

Before sharing a new version:

```bash
python tools/prepare_publish.py
```

PowerShell:

```powershell
.\tools\prepare-publish.ps1
```

This runs:

```bash
python tools/build_plugin_snapshot.py
python tools/validate.py
```

For a narrower manual flow:

```bash
python tools/build_plugin_snapshot.py
python tools/validate.py
```

Validation checks:

- every source skill has valid frontmatter
- every source skill has resolvable direct reference paths
- every source skill has Simplified Chinese output guidance
- every source skill has temporary artifact path guidance
- every source skill explicitly allows implicit invocation
- profile entries reference existing source skills
- plugin snapshot relative paths and byte contents match published source skills
- plugin logo/icon paths exist
- skill UI icon paths exist
- each skill `default_prompt` names its own `$skill`

After a human reviews the diff, commit and push to GitHub. Do not push from a local
draft before review.

## Plugin Scope

This repository may later add:

- MCP server configuration for company systems
- app mappings for internal/external tools
- hooks for lifecycle checks, prompt scanning, validation, or analytics
- assets and UI metadata for better discovery
- helper scripts for repeatable local workflows

Do not use the plugin to silently overwrite a teammate's global `~/.codex/AGENTS.md`.
Company-wide values and taste should be distributed as opt-in guidance, skills, hooks,
repo `AGENTS.md` templates, or explicit onboarding instructions.

## AGENTS.md And Skill Boundaries

Use the smallest durable surface:

- `AGENTS.md`: durable repo or global behavior expectations
- skill: reusable task workflow and domain-specific method
- plugin: installable bundle of skills, MCP, apps, hooks, metadata, and assets
- hook: deterministic lifecycle enforcement
- MCP/app: live external tools and shared data

For SpecOS taste and product judgment, keep the durable principles in product/design
skills, and put repo-specific build/test/release rules in each repo's `AGENTS.md`.

## Troubleshooting

If the plugin does not appear:

1. Run `codex plugin marketplace list`.
2. Confirm `ispark-company` is listed.
3. Run `codex plugin add ispark-company@ispark-company`.
4. Restart Codex or open a new thread.
5. If using a private repo, verify GitHub clone access.

If the installed version did not change:

```bash
codex plugin marketplace upgrade ispark-company
codex plugin add ispark-company@ispark-company
```

If a skill appears stale, verify that `tools/build_plugin_snapshot.py` was run before
publishing.
