# Shared Lark Rules

- Use the configured `lark-cli` identity required by the operation.
- Authentication, scope, permission, and `_notice` handling must be resolved before retrying random commands.
- Do not print secrets or tokens unless they are already user-provided public identifiers.
- For missing permissions, distinguish app scope, document access, tenant policy, and security label restrictions.

