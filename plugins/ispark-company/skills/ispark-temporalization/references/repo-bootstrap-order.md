# Repo Bootstrap Order

Use this when a Python Temporal worker repo is being initialized from scratch or normalized back to the standard.

The goal is to avoid building deployment or workflow layers before the repo surface and verification path are stable.

## Recommended Order

1. Freeze repo surface
   - `pyproject.toml`
   - `.gitignore`
   - module/package name
   - Python version
   - lint/type/test baseline

2. Freeze runtime entry shape
   - worker CLI entry
   - config loading path
   - default queue / worker kind naming
   - `run` and optional `verify` entry shape

3. Freeze code structure
   - `config / contracts / services / infra / bootstrap / temporal`
   - direct-import surfaces instead of package-level re-export layers
   - `infra/ports` and adapters
   - Temporal workflows/activities/worker runtime
   - tests layout

4. Freeze CI verification surface
   - GitHub Actions CI workflow
   - test / lint / typecheck jobs
   - security scan job
   - build artifact job
   - CodeQL workflow when GitHub Actions is the repo standard
   - repo variables / secrets naming aligned with the shared convention

5. Freeze image build surface
   - Dockerfile
   - image build/publish workflow
   - registry / repository coordinates
   - APT / PIP / UV mirror and index coordinates
   - trigger policy for PR, branch push, release tag, and manual publish
   - tagging policy
   - provenance / attestation policy

6. Freeze deployment surface
   - compose file for local integration when needed
   - Kubernetes Deployment manifest when container-first
   - healthcheck path
   - resource requests/limits

7. Freeze rollout verification
   - replay / verify strategy
   - smoke path
   - release note path
   - TODO / README sync

## What Not To Do

- Do not start with Kubernetes manifests before the repo has a stable worker entry.
- Do not add image publishing before the Dockerfile and dependency baseline are stable.
- Do not add complex queue splits before the default worker kind and default queue are frozen.
- Do not treat CI as optional cleanup; it is part of the standard repo surface.

## Minimal Template Set

For a new Python Temporal repo, the minimum standardized template set is:

- `worker.pyproject.toml`
- `worker.gitignore`
- `worker.gha-ci.yaml`
- `worker.gha-codeql.yaml`

Add these when the repo is containerized:

- `worker.Dockerfile`
- `worker.gha-image.yaml`
- `worker.compose.yaml`
- `worker.deployment.yaml`

## Normalization Check

When normalizing an existing repo, confirm that these layers still align in the same order:

- repo surface
- runtime entry
- code structure
- CI verification
- image publishing
- deployment
- rollout verification
