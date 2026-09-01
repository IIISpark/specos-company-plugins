# Notion Authentication And Diagnostics

Use this reference only for CLI availability, identity, authentication, or health checks.

## Read-Only Checks

1. Run `ntn --version` to establish the local CLI version when it affects diagnosis.
2. Run `ntn whoami` for the active identity, using compact output where useful.
3. Run `ntn doctor` when setup is failing. Summarize the diagnosis; do not paste sensitive paths
   or configuration values.

## Auth Changes

- `ntn login` begins an external authentication flow. Confirm immediately before starting it and
  let the user complete the browser or two-step flow.
- `ntn logout` changes local authentication state. Confirm immediately before it.
- Never run `ntn auth token`, expose a token, or instruct the user to paste a token into chat.
- A missing login is a prerequisite report, not permission to authenticate or configure a workspace.

If identity or workspace selection is ambiguous, stop and ask the user which authorized workspace
to use. Do not infer it from local configuration.
