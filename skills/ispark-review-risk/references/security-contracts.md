# Security And Contracts

Stop for explicit confirmation when a change touches:

- auth, permission, tenant isolation, privacy, secret handling
- database schema or migration
- public API, OpenAPI/APIFox contract, SDK contract
- provider billing or paid external side effects
- production deploy, data repair, or destructive maintenance

Do not hardcode tokens. Do not print secrets. Do not widen access to make a task easier.

