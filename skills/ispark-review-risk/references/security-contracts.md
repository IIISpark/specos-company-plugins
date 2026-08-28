# Security And Contracts

Stop for explicit confirmation when a change touches:

- auth, permission, tenant isolation, privacy, secret handling
- database schema or migration
- public API, OpenAPI/APIFox contract, SDK contract
- provider billing or paid external side effects
- production deploy, data repair, or destructive maintenance

Do not hardcode tokens. Do not print secrets. Do not widen access to make a task easier.

Before approving a security-sensitive diff, verify authentication and authorization
(including tenant/object scope), input/output encoding, state-changing request protection,
rate/resource limits, secure error behavior, auditability, and rollback or recovery. Keep
the checklist evidence-linked to changed files and lines; do not substitute a generic
security score for a path-specific review.
