#!/usr/bin/env python3
"""Fallback profile sync for direct skill-root installs."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILES_ROOT = REPO_ROOT / "profiles"
SKILLS_ROOT = REPO_ROOT / "skills"
STATE_ROOT = Path.home() / ".ispark-codex-plugin"
LOCK_PATH = STATE_ROOT / "lock.json"
IGNORE_NAMES = {".git", ".hg", ".svn", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def default_target_root() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "skills"
    return Path.home() / ".codex" / "skills"


def read_profile(profile: str) -> list[str]:
    profile_path = PROFILES_ROOT / f"{profile}.yml"
    if not profile_path.exists():
        raise SystemExit(f"Profile not found: {profile_path}")
    skills: list[str] = []
    for line in profile_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            skills.append(stripped[2:].strip())
    if not skills:
        raise SystemExit(f"Profile has no skills: {profile_path}")
    return skills


def find_skill_source(skill_name: str) -> Path:
    matches = [path for path in SKILLS_ROOT.rglob(skill_name) if path.is_dir() and path.name == skill_name and (path / "SKILL.md").exists()]
    if not matches:
        raise SystemExit(f"Skill source not found: {skill_name}")
    if len(matches) > 1:
        raise SystemExit(f"Multiple skill sources found for {skill_name}: {matches}")
    return matches[0]


def repo_revision() -> str:
    try:
        output = subprocess.check_output(["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL)
    except (OSError, subprocess.CalledProcessError):
        return "local-draft"
    return output.strip() or "local-draft"


def status() -> int:
    if LOCK_PATH.exists():
        print(LOCK_PATH.read_text(encoding="utf-8"))
    else:
        print(f"No ISpark skill lock found at {LOCK_PATH}")
    return 0


def sync(action: str, profile: str, target_root: Path, clean: bool) -> int:
    skills = read_profile(profile)
    resolved = [(name, find_skill_source(name), target_root / name) for name in skills]

    print(f"Profile: {profile}")
    print(f"TargetRoot: {target_root}")
    print("Skills:")
    for name, _, _ in resolved:
        print(f"  - {name}")

    if action == "dry-run":
        print("Dry run only. No files changed.")
        return 0

    target_root.mkdir(parents=True, exist_ok=True)
    for _, source, target in resolved:
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(
            source,
            target,
            ignore=shutil.ignore_patterns(*sorted(IGNORE_NAMES), "*.pyc", "*.pyo"),
        )

    if clean:
        wanted = set(skills)
        for path in target_root.glob("ispark-*"):
            if path.is_dir() and path.name not in wanted:
                shutil.rmtree(path)

    STATE_ROOT.mkdir(parents=True, exist_ok=True)
    lock = {
        "profile": profile,
        "target_root": str(target_root),
        "repo_root": str(REPO_ROOT),
        "revision": repo_revision(),
        "installed_at": datetime.now(timezone.utc).isoformat(),
        "skills": skills,
    }
    LOCK_PATH.write_text(json.dumps(lock, indent=2), encoding="utf-8")
    print(f"Installed {len(skills)} ISpark skills.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["dry-run", "sync", "status"], default="status")
    parser.add_argument("--profile", default="engineer")
    parser.add_argument("--target-root", type=Path, default=default_target_root())
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()

    if args.action == "status":
        return status()
    return sync(args.action, args.profile, args.target_root, args.clean)


if __name__ == "__main__":
    raise SystemExit(main())
