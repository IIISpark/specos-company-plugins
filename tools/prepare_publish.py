#!/usr/bin/env python3
"""Prepare the repository for publishing the company plugin."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    print("+ " + " ".join(command))
    result = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, check=False)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def maybe_git_status() -> None:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "status", "--short"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        print("Git status skipped: repository metadata is not available.")
        return
    print("Git status:")
    print(result.stdout.rstrip() or "  clean")


def main() -> int:
    run([sys.executable, str(REPO_ROOT / "tools" / "build_plugin_snapshot.py")])
    run([sys.executable, str(REPO_ROOT / "tools" / "validate.py")])
    maybe_git_status()
    print("Publish preparation complete. Do not push until a human reviews the diff.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
