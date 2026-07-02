# Repo Variables And Secrets

Use this reference when a Python Temporal repo is expected to run through GitHub Actions, build images, or deploy workers.

The goal is to keep variable names stable across repos so templates and automation do not drift.

## Scope Layering

Prefer three configuration layers instead of redefining the same defaults in every repo:

1. organization-level variables/secrets for shared defaults
2. repository-level variables/secrets for repo-specific coordinates and policy
3. environment-level variables/secrets for `staging` / `production` differences

For private repositories, verify what the GitHub plan actually allows before assuming organization-level Actions configuration will flow through. A common failure mode is:

- organization variables/secrets are limited to public repositories
- the target repo is private
- the workflow silently falls back to template defaults because the org-level values are invisible

If the repo is private and org-level private-repo access is unavailable, use:

1. repository-level variables/secrets for stable repo defaults
2. environment-level variables/secrets for deploy-target differences
3. manual dispatch inputs for one-off overrides

When the workflow also exposes manual dispatch inputs, recommended effective precedence is:

1. manual `workflow_dispatch` inputs
2. environment variables / secrets
3. repository variables / secrets
4. organization variables / secrets
5. safe template defaults

If a workflow needs access to environment-level values, the job must explicitly bind:

```yaml
jobs:
  deploy-image:
    environment: production
```

Creating a GitHub Environment in the UI is not enough by itself.

Recommended canonical environment names:

- `dev`
- `production`

Prefer these names consistently across repos and templates so workflow defaults, environment binding, and rollout documentation stay aligned.

For image/release workflows, resolve organization/repository/environment variables inside the bound job rather than only in workflow-level `env:`. Environment-level variables are job-scoped and should be read after the job declares its `environment: ...`.

## Recommended GitHub Actions Variables

Configure these under:

- `Settings -> Secrets and variables -> Actions -> Variables`

### Image publishing

- `IMAGE_REGISTRY`
  - Example: `ghcr.io`, `harbor.example.com`, `123456789.dkr.ecr.us-west-2.amazonaws.com`
- `IMAGE_REPOSITORY`
  - Example: `dramawork/artbook-worker`
- `IMAGE_REGISTRY_USERNAME`
  - Example: `ci-bot`
- `IMAGE_PUBLISH_ON_MAIN`
  - `true` or `false`
- `ENABLE_IMAGE_ATTESTATION`
  - `true` or `false`

### Package source and mirror settings

- `APT_MIRROR_URL`
  - Example: `https://mirrors.ustc.edu.cn/debian`
- `PIP_INDEX_URL`
  - Example: `https://pypi.org/simple`
- `PIP_EXTRA_INDEX_URL`
  - Example: `https://pypi.company.internal/simple`
- `PIP_TRUSTED_HOST`
  - Example: `pypi.company.internal`

## Recommended GitHub Actions Secrets

Configure these under:

- `Settings -> Secrets and variables -> Actions -> Secrets`

### Image publishing

- `IMAGE_REGISTRY_PASSWORD`
  - Registry password or access token for image publishing

## Naming Rules

- Prefer `IMAGE_*` for container registry and publishing controls.
- Prefer `PIP_*` for Python package index settings.
- Prefer `APT_*` for Debian/Ubuntu package mirror settings.
- Keep the exact names stable across repos; treat them as a workspace/organization standard rather than per-repo inventions.
- Do not invent per-repo synonyms like `REGISTRY_HOST`, `DOCKER_REPO`, `PRIVATE_PYPI`, or `APT_SOURCE_URL` unless the repo already has a frozen standard you must keep.

## Defaults And Overrides

Recommended placement:

- organization defaults:
  - `APT_MIRROR_URL`
  - `PIP_INDEX_URL`
  - `PIP_EXTRA_INDEX_URL`
  - `PIP_TRUSTED_HOST`
  - optional `IMAGE_REGISTRY`
- repository overrides:
  - `IMAGE_REPOSITORY`
  - `IMAGE_REGISTRY_USERNAME`
  - `IMAGE_PUBLISH_ON_MAIN`
  - `ENABLE_CODEQL`
  - `ENABLE_IMAGE_ATTESTATION`
- environment overrides:
  - deploy-target-specific registry credentials, namespaces, or release controls

For private repositories where org-level Actions configuration does not reach the repo, move shared defaults down to repository scope and only keep true deploy-target differences in environments.

Recommended precedence:

1. manual `workflow_dispatch` inputs
2. environment variables / secrets
3. repository variables / secrets
4. organization variables / secrets
5. safe template defaults

This allows:

- organization-wide defaults without per-repo duplication
- stable repo-level defaults
- environment-specific release overrides
- one-off override for emergency or release runs
- a working baseline without forcing local mirror assumptions into the template

## Security And Feature Gates

Recommended repo variables:

- `ENABLE_CODEQL`
  - `true` or `false`
- `ENABLE_IMAGE_ATTESTATION`
  - `true` or `false`

Recommended behavior:

- `ENABLE_CODEQL=true` means "attempt CodeQL if the repo is eligible", not "fail red when GitHub Advanced Security is unavailable"
- image attestation should be opt-in unless the organization has already standardized the required GitHub feature set
- image publishing credentials should usually live at repo or environment scope, not org scope, unless the organization has confirmed cross-repo applicability

## Action Pinning

For generic GitHub Actions templates, prefer:

1. a human-readable comment with the reviewed upstream release tag
2. a `uses:` entry pinned to the exact commit SHA behind that release tag

Example:

```yaml
- name: Checkout
  # actions/checkout@v6.0.2
  uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd
```

Why:

- a moving major tag such as `@v6` is convenient but not immutable
- a commit SHA is reproducible and narrows supply-chain drift
- the adjacent release-tag comment keeps the workflow maintainable for humans and upgrade bots

When refreshing templates, verify the SHA from the official GitHub release/tag metadata instead of copying a value from memory or a secondary blog post.

## What Not To Do

- Do not hardcode domestic mirrors or private indexes into generic templates.
- Do not store registry passwords in variables.
- Do not make every repo invent a different name for the same concept.
- Do not push deploy-environment-only values down into organization defaults when they vary by `staging` / `production`.
- Do not couple mirror configuration names to a single cloud vendor unless the repo is permanently vendor-locked.
- Do not assume org-level Actions variables/secrets work for private repos just because they work for public ones.
- Do not read environment-scoped values only from workflow-level `env:`; they are job-scoped after `environment:` binding.
