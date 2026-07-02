# This file is the canonical annotated template for a Python Temporal worker Dockerfile.
# Use this file itself as the repo template baseline.
# Read this file first when deciding:
# - which placeholders must be replaced
# - which knobs are optional
# - whether this module should derive from the base template instead of copying it unchanged

# syntax=docker/dockerfile:1.7

# REQUIRED TO REPLACE ONLY IF YOUR TEAM STANDARDIZES ON DIFFERENT TOOL VERSIONS:
# - Pin the helper image version.
# - Keep it pinned; do not switch to `latest`.
FROM ghcr.io/astral-sh/uv:0.10.6 AS uvbin

# REQUIRED TO REPLACE:
# - The Python patch/base image line if your repo has a different pinned Python runtime.
# - Keep the image pinned to a concrete version.
FROM python:3.12.12-slim-trixie AS builder

# OPTIONAL:
# - Keep these ARG names stable unless the repo has a stronger package-source convention.
# - Override them at build time for domestic mirrors or private package indexes.
ARG APT_MIRROR_URL=
ARG PIP_INDEX_URL=https://pypi.org/simple
ARG PIP_EXTRA_INDEX_URL=
ARG PIP_TRUSTED_HOST=

# OPTIONAL:
# - If your environment needs a Debian/Ubuntu mirror, rewrite sources before apt install.
# - Keep the mirror injectable; do not hardcode a domestic mirror into the generic template.
RUN if [ -n "${APT_MIRROR_URL}" ]; then \
      sed -i "s|http://deb.debian.org/debian|${APT_MIRROR_URL}|g" /etc/apt/sources.list.d/debian.sources; \
      sed -i "s|http://security.debian.org/debian-security|${APT_MIRROR_URL}|g" /etc/apt/sources.list.d/debian.sources; \
    fi

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_INDEX_URL=${PIP_INDEX_URL} \
    PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL} \
    PIP_TRUSTED_HOST=${PIP_TRUSTED_HOST} \
    UV_DEFAULT_INDEX=${PIP_INDEX_URL} \
    UV_INDEX=${PIP_EXTRA_INDEX_URL} \
    UV_NATIVE_TLS=1

WORKDIR /build

# REQUIRED TO KEEP IN SYNC WITH YOUR PROJECT LAYOUT:
# - If the repo does not use `README.md` or `uv.lock`, adjust this line.
# - If the source root is not `src/`, adjust the copy path.
COPY --from=uvbin /uv /uvx /bin/
COPY pyproject.toml README.md uv.lock ./
COPY src ./src

# OPTIONAL:
# - Keep cache mounts when BuildKit is available.
# - If the repo uses another build backend, adjust this command chain.
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --upgrade pip build

# REQUIRED TO REVIEW:
# - `--all-extras --no-extra dev` matches the current opinionated baseline.
# - If the repo has a dedicated runtime extra set, narrow it here.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv export --frozen --all-extras --no-extra dev --no-editable --no-emit-project -o /tmp/requirements.lock.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip wheel --wheel-dir /tmp/wheels --require-hashes -r /tmp/requirements.lock.txt

RUN python -m build --wheel --outdir /tmp/wheels

# REQUIRED TO REPLACE IF YOUR RUNTIME BASE DIFFERS:
# - Keep runtime image pinned and aligned with the builder ABI unless you know the wheel set is portable.
FROM python:3.12.12-slim-trixie AS runtime

# OPTIONAL BUT RECOMMENDED:
# - Supply these from CI for traceability.
ARG COMMIT_SHA=unknown
ARG BUILD_TIME=unknown
ARG APT_MIRROR_URL=

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    HOME=/home/appuser \
    XDG_CACHE_HOME=/home/appuser/.cache \
    COMMIT_SHA=${COMMIT_SHA} \
    BUILD_TIME=${BUILD_TIME}

# REQUIRED TO REPLACE:
# - Title/description should reflect the real module or org template name if you publish images externally.
LABEL org.opencontainers.image.title="Python Temporal Worker" \
      org.opencontainers.image.description="Generic multi-stage Python Temporal worker runtime image" \
      org.opencontainers.image.revision="${COMMIT_SHA}" \
      org.opencontainers.image.created="${BUILD_TIME}"

# OPTIONAL TO EXTEND:
# - Keep `ca-certificates` and `tini` in the default baseline.
# - Add more packages only when the worker truly needs them.
# DERIVE INSTEAD OF COPYING if you need heavy system dependencies such as:
# - Playwright/Chromium
# - FFmpeg/ImageMagick
# - OCR engines
# - CUDA/GPU stacks
RUN if [ -n "${APT_MIRROR_URL}" ]; then \
      sed -i "s|http://deb.debian.org/debian|${APT_MIRROR_URL}|g" /etc/apt/sources.list.d/debian.sources; \
      sed -i "s|http://security.debian.org/debian-security|${APT_MIRROR_URL}|g" /etc/apt/sources.list.d/debian.sources; \
    fi

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates tini \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# REQUIRED TO REVIEW:
# - If the module does not ship `conf/` defaults, remove or replace that copy.
# - Prefer BuildKit cross-stage mounts for `/tmp/requirements.lock.txt` and `/tmp/wheels`.
# - Do not `COPY` the wheelhouse into the runtime image unless your builder/runtime cannot use mount-based installs.
# - Mounting builder artifacts for install typically saves more runtime image size than switching to a slightly smaller Debian base.
COPY conf ./conf

# REQUIRED TO REPLACE:
# - `your_module-*.whl` must match the project wheel name.
# - Prefer a real package name, not the import path guess.
RUN --mount=type=bind,from=builder,source=/tmp/requirements.lock.txt,target=/tmp/requirements.lock.txt,ro \
    --mount=type=bind,from=builder,source=/tmp/wheels,target=/tmp/wheels,ro \
    python -m pip install --no-cache-dir --no-compile --no-index --find-links=/tmp/wheels --require-hashes -r /tmp/requirements.lock.txt \
    && python -m pip install --no-cache-dir --no-compile --no-index --no-deps /tmp/wheels/your_module-*.whl

# OPTIONAL:
# - UID 10001 is the current generic baseline.
# - Change it only if your cluster policy requires another fixed UID.
RUN useradd --create-home --home-dir /home/appuser --shell /usr/sbin/nologin --uid 10001 appuser \
    && mkdir -p /work/output /app/tls /home/appuser/.cache \
    && chown -R appuser:appuser /app /work /home/appuser

USER appuser
WORKDIR /work

# REQUIRED TO REPLACE:
# - Module name
# - Config path if your repo uses a different runtime config location
# OPTIONAL:
# - Add `--check-temporal`, `--check-artifacts`, or similar flags only if the repo intentionally extends the baseline
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
  CMD ["python", "-m", "your_module", "--config", "/app/conf/config.yaml", "--healthcheck"]

# REQUIRED TO REPLACE:
# - Module name
# OPTIONAL:
# - Switch `CMD` to the repo-standard default such as `--config /app/conf/config.yaml`
# - Keep the annotated template on `--help` if you want the most neutral baseline.
ENTRYPOINT ["tini", "--", "python", "-m", "your_module"]
CMD ["--help"]
