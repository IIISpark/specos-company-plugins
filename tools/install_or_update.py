#!/usr/bin/env python3
"""Install or update the ISpark SpecOS Codex plugin from a marketplace source."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys


DEFAULT_SOURCE = "IIISpark/specos-company-plugins"
DEFAULT_REF = "main"
DEFAULT_MARKETPLACE = "ispark-company"
DEFAULT_PLUGIN = "ispark-company"


def run(command: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    print("+ " + " ".join(command))
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result


def resolve_codex() -> str:
    candidates = ["codex.cmd", "codex"] if os.name == "nt" else ["codex"]
    for candidate in candidates:
        path = shutil.which(candidate)
        if path:
            return path
    raise SystemExit("codex CLI was not found on PATH.")


def require_codex() -> str:
    codex = resolve_codex()
    if not codex:
        raise SystemExit("codex CLI was not found on PATH.")
    return codex


def marketplace_names(codex: str) -> set[str]:
    result = run([codex, "plugin", "marketplace", "list"], check=False)
    names: set[str] = set()
    for line in result.stdout.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("MARKETPLACE"):
            continue
        names.add(stripped.split()[0])
    return names


def add_marketplace(codex: str, source: str, ref: str | None) -> None:
    command = [codex, "plugin", "marketplace", "add", source]
    if ref:
        command.extend(["--ref", ref])
    run(command)


def install_plugin(codex: str, plugin: str, marketplace: str) -> None:
    run([codex, "plugin", "add", f"{plugin}@{marketplace}"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--action", choices=["install", "update", "status"], default="install")
    parser.add_argument("--source", default=DEFAULT_SOURCE)
    parser.add_argument("--ref", default=DEFAULT_REF)
    parser.add_argument("--marketplace", default=DEFAULT_MARKETPLACE)
    parser.add_argument("--plugin", default=DEFAULT_PLUGIN)
    args = parser.parse_args()

    codex = require_codex()

    if args.action == "status":
        run([codex, "plugin", "marketplace", "list"])
        run([codex, "plugin", "list"])
        return 0

    names = marketplace_names(codex)
    if args.marketplace not in names:
        add_marketplace(codex, args.source, args.ref)
    elif args.action == "update":
        run([codex, "plugin", "marketplace", "upgrade", args.marketplace])
    else:
        print(f"Marketplace already configured: {args.marketplace}")

    install_plugin(codex, args.plugin, args.marketplace)
    print("Done. Restart Codex or open a new thread before testing newly installed skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
