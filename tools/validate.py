#!/usr/bin/env python3
"""Validate ISpark Codex plugin repository structure."""

from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
PROFILES_ROOT = REPO_ROOT / "profiles"
PLUGIN_ROOT = REPO_ROOT / "plugins" / "ispark-company"
PLUGIN_SKILLS_ROOT = PLUGIN_ROOT / "skills"
PLUGIN_MANIFEST = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"

NAME_RE = re.compile(r"(?m)^name:\s*([a-z0-9-]+)\s*$")
DESCRIPTION_RE = re.compile(r"(?m)^description:\s*.+$")
PERSONAL_PATH_RE = re.compile(r"C:\\Users\\nmg_w|skills-archive")
OUTPUT_LANGUAGE_RE = re.compile(r"Simplified Chinese|简体中文")
TEMP_PATH_RE = re.compile(r"working-delta/|\.tmp/|tmp/")
YAML_STRING_RE = re.compile(r'(?m)^\s*{key}:\s*"([^"]+)"\s*$')


def yaml_string(text: str, key: str) -> str | None:
    match = re.compile(YAML_STRING_RE.pattern.format(key=re.escape(key))).search(text)
    if not match:
        return None
    return match.group(1)


def validate_relative_asset(base: Path, raw_path: str, owner: Path, errors: list[str]) -> None:
    if not raw_path.startswith("./assets/"):
        errors.append(f"Asset path must begin with ./assets/: {owner} => {raw_path}")
        return
    resolved = base / raw_path[2:]
    if not resolved.exists():
        errors.append(f"Asset path does not exist: {owner} => {raw_path}")


def find_skill_dirs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.iterdir() if path.is_dir() and (path / "SKILL.md").exists())


def profile_skill_names(path: Path) -> list[str]:
    names: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\s*-\s*([a-z0-9-]+)\s*$", line)
        if match:
            names.append(match.group(1))
    return names


def validate_skills(errors: list[str]) -> set[str]:
    skill_dirs = find_skill_dirs(SKILLS_ROOT)
    skill_names: set[str] = set()
    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        text = skill_file.read_text(encoding="utf-8")
        if not text.startswith("---"):
            errors.append(f"Missing YAML frontmatter: {skill_file}")
        name_match = NAME_RE.search(text)
        if not name_match:
            errors.append(f"Missing or invalid name: {skill_file}")
        elif name_match.group(1) != skill_dir.name:
            errors.append(f"Skill name does not match directory: {skill_file} => {name_match.group(1)}")
        else:
            skill_names.add(name_match.group(1))
        if not DESCRIPTION_RE.search(text):
            errors.append(f"Missing description: {skill_file}")
        if PERSONAL_PATH_RE.search(text):
            errors.append(f"Runtime text references personal archive path: {skill_file}")
        if not OUTPUT_LANGUAGE_RE.search(text):
            errors.append(f"Missing Simplified Chinese output rule: {skill_file}")
        if not TEMP_PATH_RE.search(text):
            errors.append(f"Missing temporary artifact path rule: {skill_file}")
        agents_file = skill_dir / "agents" / "openai.yaml"
        if agents_file.exists():
            agents_text = agents_file.read_text(encoding="utf-8")
            default_prompt = yaml_string(agents_text, "default_prompt")
            if not default_prompt:
                errors.append(f"Missing agents default_prompt: {agents_file}")
            elif f"${skill_dir.name}" not in default_prompt:
                errors.append(f"agents default_prompt must mention ${skill_dir.name}: {agents_file}")
            for key in ("icon_small", "icon_large"):
                icon_path = yaml_string(agents_text, key)
                if icon_path:
                    validate_relative_asset(skill_dir, icon_path, agents_file, errors)
    return skill_names


def validate_profiles(skill_names: set[str], errors: list[str]) -> None:
    for profile in sorted(PROFILES_ROOT.glob("*.yml")):
        for skill_name in profile_skill_names(profile):
            if skill_name not in skill_names:
                errors.append(f"Profile {profile.name} references missing skill: {skill_name}")


def validate_plugin(skill_names: set[str], errors: list[str]) -> None:
    if not PLUGIN_ROOT.exists():
        errors.append(f"Missing plugin root: {PLUGIN_ROOT}")
        return
    if not PLUGIN_MANIFEST.exists():
        errors.append(f"Missing plugin manifest: {PLUGIN_MANIFEST}")
    else:
        manifest = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))
        if manifest.get("name") != "ispark-company":
            errors.append(f"Plugin manifest name must be ispark-company: {PLUGIN_MANIFEST}")
        if manifest.get("skills") != "./skills/":
            errors.append(f"Plugin manifest skills path must be ./skills/: {PLUGIN_MANIFEST}")
        interface = manifest.get("interface", {})
        if not isinstance(interface, dict):
            errors.append(f"Plugin manifest interface must be an object: {PLUGIN_MANIFEST}")
        else:
            for key in ("composerIcon", "logo", "logoDark"):
                value = interface.get(key)
                if isinstance(value, str):
                    validate_relative_asset(PLUGIN_ROOT, value, PLUGIN_MANIFEST, errors)
            screenshots = interface.get("screenshots", [])
            if screenshots:
                if not isinstance(screenshots, list):
                    errors.append(f"Plugin screenshots must be a list: {PLUGIN_MANIFEST}")
                else:
                    for value in screenshots:
                        if isinstance(value, str):
                            validate_relative_asset(PLUGIN_ROOT, value, PLUGIN_MANIFEST, errors)
                        else:
                            errors.append(f"Plugin screenshot path must be a string: {PLUGIN_MANIFEST}")

    if not MARKETPLACE.exists():
        errors.append(f"Missing repo marketplace: {MARKETPLACE}")
    else:
        marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        entries = [entry for entry in marketplace.get("plugins", []) if entry.get("name") == "ispark-company"]
        if not entries:
            errors.append(f"Marketplace missing ispark-company entry: {MARKETPLACE}")
        elif entries[0].get("source", {}).get("path") != "./plugins/ispark-company":
            errors.append(f"Marketplace ispark-company path must be ./plugins/ispark-company: {MARKETPLACE}")

    if not PLUGIN_SKILLS_ROOT.exists():
        errors.append(f"Missing plugin skills root: {PLUGIN_SKILLS_ROOT}")
        return
    plugin_skill_names = {path.name for path in find_skill_dirs(PLUGIN_SKILLS_ROOT)}
    for name in sorted(skill_names - plugin_skill_names):
        errors.append(f"Plugin snapshot missing skill: {name}")
    for name in sorted(plugin_skill_names - skill_names):
        errors.append(f"Plugin snapshot has unknown skill: {name}")


def main() -> int:
    errors: list[str] = []
    skill_names = validate_skills(errors)
    validate_profiles(skill_names, errors)
    validate_plugin(skill_names, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {len(skill_names)} skills validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
