# First Pass Routing

Read the core references in this order for most Temporalization work:

1. `source-of-truth.md`
2. `task-modes.md`
3. `target-architecture.md`
4. `questions-and-checkpoints.md`
5. `repo-bootstrap-order.md`
6. `repo-variables-and-secrets.md`
7. `review-checklist-and-output-template.md`
8. `worker-topology-and-scaling.md`

If the task changes workflow/activity contracts, DTOs, or versioning behavior, also read `contract-versioning.md`.

If the task includes containerization or Kubernetes delivery, inspect the annotated config, Dockerfile, deployment, and compose templates.

If the task includes worker autoscaling, inspect the KEDA ScaledObject template.

If the task initializes or normalizes a Python module repo surface, inspect the pyproject, gitignore, CI, CodeQL, and image workflow templates.

Use templates only as baselines. Project facts, central docs, and repo-local contracts remain authoritative.
