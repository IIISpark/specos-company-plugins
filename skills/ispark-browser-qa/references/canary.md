# Canary

Post-deploy canary:

- confirm the intended version is live
- check health endpoint or status page
- exercise one behavior-specific smoke
- inspect logs or console for new errors
- compare with the expected production environment

Do not mutate production data during canary unless the smoke action is approved and reversible.

