# Worktrees

Use a separate branch or worktree when:

- the task is long-running
- multiple agents may work in parallel
- the change may conflict with local user edits
- release work needs isolation from experiments

Before creating isolation:

- inspect current repo root and status
- identify whether the current directory is a workspace shell or actual git repo
- preserve uncommitted user changes

Do not use destructive cleanup such as reset, checkout, or recursive delete unless the user explicitly requested it and the target path is verified.

