# Apifox CLI Troubleshooting

Use this reference when a command reports success but a resource, step, report, or client view is missing,
or when current help, hints, and observed behavior disagree.

## Evidence Ladder

1. Record the redacted command shape, CLI version/path, project, branch, environment, resource type,
   resource ID kept internal, and whether a private deployment endpoint is in use.
2. Read current command help. Do not use hidden aliases or update the CLI merely because an old example
   differs.
3. Inspect structured success, exit status, and diagnostics. A success-sounding summary cannot override
   `success=false` or a failing exit status.
4. Use the matching `list/get` with the same project and branch. Check module, folder, category, and UI
   filters before recreating anything.
5. For tests, separate saved structure from runtime behavior and local reports from uploaded reports.

## Common Separations

- A saved endpoint can still export incorrectly.
- A saved case can still be invisible due to category or branch and can still fail at runtime.
- A scenario can exist with no steps; complete readback is needed.
- A local run has no cloud report unless upload was requested.
- A test failure can be caused by Mock or environment configuration without invalidating the saved API.

If a required public flag is absent, report the installed version and missing capability. Updating the
CLI requires explicit authorization. After two materially different failed attempts at the same issue,
stop with the evidence and likely ownership boundary instead of continuing speculative writes.
