#!/usr/bin/env python3
"""Build the plugin skill snapshot from the source skills tree."""

from __future__ import annotations

import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOTS = [REPO_ROOT / "skills"]
PLUGIN_SKILLS_ROOT = REPO_ROOT / "plugins" / "ispark-company" / "skills"
IGNORE_NAMES = {".git", ".hg", ".svn", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def find_skill_dirs() -> list[Path]:
    """Return source skill directories that contain `SKILL.md`."""

    skill_dirs: list[Path] = []
    for root in SOURCE_ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.iterdir()):
            if path.is_dir() and (path / "SKILL.md").exists():
                skill_dirs.append(path)
    return skill_dirs


def main() -> int:
    plugin_root = REPO_ROOT / "plugins" / "ispark-company"
    if not plugin_root.exists():
        raise SystemExit(f"Plugin root not found: {plugin_root}")

    if PLUGIN_SKILLS_ROOT.exists():
        shutil.rmtree(PLUGIN_SKILLS_ROOT)
    PLUGIN_SKILLS_ROOT.mkdir(parents=True, exist_ok=True)

    copied: list[str] = []
    for skill_dir in find_skill_dirs():
        target = PLUGIN_SKILLS_ROOT / skill_dir.name
        shutil.copytree(
            skill_dir,
            target,
            ignore=shutil.ignore_patterns(*sorted(IGNORE_NAMES), "*.pyc", "*.pyo"),
        )
        copied.append(skill_dir.name)

    print(f"Built plugin snapshot with {len(copied)} skills.")
    for name in copied:
        print(f"  - {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
