# Apifox CLI, Auth, And Write Gate

Use this reference for CLI setup, identity, project selection, command discovery, and the shared
write protocol.

## Establish Runtime Facts

1. Check `apifox --version` and `apifox --help` without credentials.
2. Read the selected command and subcommand help. Treat it as authoritative over examples, cached
   skill text, or `agentHints` that mention unavailable flags.
3. Confirm the authorized project and branch. If several candidates exist, present safe labels and
   let the user choose; do not infer a target from an unrelated workspace.
4. Prefer structured output. Respect `success`, exit status, and returned diagnostics over optimistic
   summary text.

If `apifox` is unavailable, state that fact and stop. Installation, upgrading, login, account
switching, private-deployment configuration, or local config writes require explicit authorization.
Never ask the user to paste a token into chat or pass a token in a command that could be logged.

## Structured Write Protocol

For create or update operations:

1. Read the current resource when it exists.
2. Read the command's current JSON schema with `cli-schema` when supported.
3. Build the smallest complete payload under `.tmp/` or `working-delta/`.
4. Run `cli-schema validate`; validation proves structure only, not UI or runtime behavior.
5. Show project, branch, resource, changed fields, side effects, and verification plan.
6. Obtain a new explicit confirmation immediately before the write.
7. Execute once, then use the matching `get` or `list` in the same branch to verify persistence.

Do not repeat a failed write unchanged. Use current help, schema, readback, and structured error fields
to locate the mismatch. AI write-permission failures require the user's choice between direct-edit
permission and an AI branch; never switch strategies automatically.
