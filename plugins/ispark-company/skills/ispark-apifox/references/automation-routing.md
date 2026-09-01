# Apifox Automation, CI, And Reports

Use this reference for suites, scheduled tasks, runners, CI execution, iterations, variable overrides,
timeouts, report files, and report uploads.

## Select The Resource

- Single endpoint case: use the test-case reference.
- Multi-step workflow: use the test-scenario reference.
- Regression collection: use a test suite.
- Scheduled execution: use a scheduled task.
- Private execution capacity: use a runner.

Do not create empty suites or scheduled-task shells unless the user explicitly requests placeholders.
Read current schemas and existing resources before updates; preserve suite members, variables, and run
configuration. Runner creation is a team-level infrastructure action, not a lightweight project edit.

## Execution Gate

Before running, establish project, branch, suite/scenario/case, explicit environment, iteration data,
variable overrides, SSL and timeout behavior, expected external effects, and cleanup. Production or
unknown environments stop execution until the user chooses a safe target.

- Local execution is still capable of remote API side effects and needs confirmation.
- Uploading a report is a separate remote effect; do not add it merely because a cloud report is useful.
- CI credentials belong in the CI secret store, never repository files or command summaries.
- Scheduled tasks and runner changes require a preview of cadence, target, team, and resource usage.

## Evidence

- Use process exit status plus requested local structured reports as the primary CI gate.
- Cloud report lookup applies only when upload was enabled for that run.
- Empty execution should lead to suite/scenario membership readback, not a successful conclusion.
- On failure, locate the exact case and step, then separate request, environment, variable, processor,
  assertion, timeout, and report-transport failures.
