#!/usr/bin/env python3
"""Validate ISpark Codex plugin repository structure."""

from __future__ import annotations

import json
import re
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - the fallback keeps the helper standalone
    yaml = None

try:
    from tools.build_plugin_snapshot import IGNORE_NAMES, IGNORE_SUFFIXES
except ModuleNotFoundError:
    from build_plugin_snapshot import IGNORE_NAMES, IGNORE_SUFFIXES


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
PROFILES_ROOT = REPO_ROOT / "profiles"
PLUGIN_ROOT = REPO_ROOT / "plugins" / "ispark-company"
PLUGIN_SKILLS_ROOT = PLUGIN_ROOT / "skills"
PLUGIN_MANIFEST = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"

NAME_RE = re.compile(r"(?m)^name:\s*([a-z0-9-]+)\s*$")
DESCRIPTION_RE = re.compile(r"(?m)^description:\s*.+$")
OUTPUT_LANGUAGE_RE = re.compile(r"Simplified Chinese|简体中文")
TEMP_PATH_RE = re.compile(r"working-delta/|\.tmp/|tmp/")
YAML_STRING_RE = re.compile(r'(?m)^\s*{key}:\s*"([^"]+)"\s*$')
REFERENCE_PATH_RE = re.compile(r"`(references/[^`]+)`")
IMPLICIT_INVOCATION_RE = re.compile(
    r"(?m)^[ \t]+allow_implicit_invocation:[ \t]*true[ \t]*$"
)
FRONTMATTER_RE = re.compile(
    r"\A---[ \t]*\r?\n(?P<body>.*?)(?:\r?\n)---[ \t]*(?:\r?\n|\Z)",
    re.DOTALL,
)
FRONTMATTER_KEY_RE = re.compile(r"^[A-Za-z0-9_-]+:")
UNQUOTED_MAPPING_COLON_RE = re.compile(r":(?:[ \t]|$)")
FRONTMATTER_ALLOWED_KEYS = frozenset({"name", "description", "license", "allowed-tools", "metadata"})
MAX_DISCOVERY_DESCRIPTION_CHARS = 280
EMAIL_RE = re.compile(r"(?i)\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b")
WINDOWS_USER_HOME_RE = re.compile(
    r"(?i)\b[A-Z]:[\\/]+(?:Users|Documents and Settings)[\\/]+[^\\/\s\"'<>]+"
)
POSIX_USER_HOME_RE = re.compile(r"(?i)(?<![A-Z0-9])/(?:home|Users)/([^/\s\"'<>]+)")
INTERNAL_HOST_RE = re.compile(
    r"(?i)(?<![A-Z0-9_.-])(?:[A-Z0-9<][A-Z0-9<>-]*\.)+(?:internal|local)\b"
)
PROJECT_RUNTIME_MARKER_RE = re.compile(
    r"(?i)dramawork|DRAMAWORK_|dw:v2:|X-DW-|/var/tmp/dramawork|skills-archive"
)
RESERVED_EMAIL_DOMAINS = frozenset({"example.com", "example.net", "example.org"})
PORTABLE_POSIX_HOME_USERS = frozenset({"appuser"})
PORTABLE_INTERNAL_HOSTS = frozenset({"temporal-frontend.default.svc.cluster.local"})


def yaml_string(text: str, key: str) -> str | None:
    match = re.compile(YAML_STRING_RE.pattern.format(key=re.escape(key))).search(text)
    if not match:
        return None
    return match.group(1)


def _basic_frontmatter_errors(body: str) -> list[str]:
    """Check the scalar frontmatter shape when PyYAML is unavailable."""

    errors: list[str] = []
    keys: set[str] = set()
    values: dict[str, str] = {}
    block_scalar = False
    block_mapping = False
    for line_number, line in enumerate(body.splitlines(), start=1):
        if not line.strip():
            continue
        if block_scalar or block_mapping:
            if line.startswith((" ", "\t")):
                continue
            block_scalar = False
            block_mapping = False
        if line.startswith((" ", "\t")) or not FRONTMATTER_KEY_RE.match(line):
            errors.append(f"line {line_number} is not a top-level YAML field")
            continue
        key, value = line.split(":", 1)
        if key in keys:
            errors.append(f"line {line_number} repeats YAML field {key}")
        keys.add(key)
        value = value.lstrip()
        values[key] = value
        if not value:
            if key == "metadata":
                block_mapping = True
                values[key] = "{}"
                continue
            errors.append(f"line {line_number} has no YAML value for {key}")
            continue
        if value[0] in {"'", '"'}:
            quote = value[0]
            if len(value) < 2 or value[-1] != quote:
                errors.append(f"line {line_number} has an unterminated YAML string")
        elif value[0] in {"|", ">"}:
            block_scalar = True
        elif UNQUOTED_MAPPING_COLON_RE.search(value):
            errors.append(f"line {line_number} contains an unquoted mapping colon")
    for key in sorted(keys - FRONTMATTER_ALLOWED_KEYS):
        errors.append(f"unexpected field {key}")
    for required_key in ("name", "description"):
        if required_key not in keys:
            errors.append(f"missing field {required_key}")
        elif values[required_key].lower() in {"null", "~", "true", "false"} or values[required_key].startswith(("[", "{")):
            errors.append(f"field {required_key} must be a string")
    description = values.get("description", "").strip("\"'")
    if description:
        if len(description) > MAX_DISCOVERY_DESCRIPTION_CHARS:
            errors.append(
                f"description exceeds {MAX_DISCOVERY_DESCRIPTION_CHARS} characters"
            )
        if "<" in description or ">" in description:
            errors.append("description contains angle brackets")
    return errors


def validate_frontmatter(skill_file: Path, text: str, errors: list[str]) -> None:
    """Validate a skill's YAML frontmatter with a parser or a conservative fallback."""

    match = FRONTMATTER_RE.match(text)
    if not match:
        errors.append(f"Invalid YAML frontmatter: {skill_file}")
        return
    body = match.group("body")
    if yaml is None:
        for detail in _basic_frontmatter_errors(body):
            errors.append(f"Invalid YAML frontmatter: {skill_file}: {detail}")
        return
    try:
        parsed = yaml.safe_load(body)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        line = f" line {mark.line + 1}" if mark is not None else ""
        problem = getattr(exc, "problem", str(exc))
        errors.append(f"Invalid YAML frontmatter: {skill_file}:{line} {problem}")
    else:
        if not isinstance(parsed, dict):
            errors.append(f"Invalid YAML frontmatter: {skill_file}: expected a mapping")
            return
        unknown_keys = sorted(set(parsed) - FRONTMATTER_ALLOWED_KEYS)
        if unknown_keys:
            errors.append(
                f"Invalid YAML frontmatter: {skill_file}: unexpected field(s) {', '.join(unknown_keys)}"
            )
        for required_key in ("name", "description"):
            if required_key not in parsed:
                errors.append(f"Invalid YAML frontmatter: {skill_file}: missing {required_key}")
            elif not isinstance(parsed[required_key], str):
                errors.append(
                    f"Invalid YAML frontmatter: {skill_file}: {required_key} must be a string"
                )
        description = parsed.get("description")
        if isinstance(description, str):
            if len(description) > MAX_DISCOVERY_DESCRIPTION_CHARS:
                errors.append(
                    f"Invalid YAML frontmatter: {skill_file}: description exceeds "
                    f"{MAX_DISCOVERY_DESCRIPTION_CHARS} characters"
                )
            if "<" in description or ">" in description:
                errors.append(
                    f"Invalid YAML frontmatter: {skill_file}: description contains angle brackets"
                )


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


def is_ignored_file(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return any(part in IGNORE_NAMES for part in relative.parts) or path.suffix in IGNORE_SUFFIXES


def source_skill_files(root: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    for skill_dir in find_skill_dirs(root):
        for path in skill_dir.rglob("*"):
            if path.is_file() and not is_ignored_file(path, root):
                files[path.relative_to(root).as_posix()] = path
    return files


def find_skill_privacy_violations(root: Path) -> list[str]:
    """Find personal or downstream-specific identifiers in skill payload text.

    Parameters
    ----------
    root : Path
        Source skill root to scan.

    Returns
    -------
    list[str]
        Deterministic validation errors without echoing the matched value.

    Notes
    -----
    This scope is every UTF-8 text file in the distributable skill payload, regardless
    of extension. Binary assets are skipped. Plugin manifest author fields are
    intentional public package metadata and are validated separately.
    """

    errors: list[str] = []
    for relative_path, path in sorted(source_skill_files(root).items()):
        try:
            payload = path.read_bytes()
        except OSError:
            errors.append(f"Skill payload could not be read: {relative_path}")
            continue
        if b"\x00" in payload:
            # Binary assets are not text-bearing instructions or metadata.
            continue
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError:
            # Unknown binary files may be shipped as assets. Text files should
            # remain UTF-8, but rejecting an opaque binary here would be noisy.
            continue

        findings: list[tuple[str, re.Match[str]]] = []
        for match in EMAIL_RE.finditer(text):
            if match.group(1).lower() not in RESERVED_EMAIL_DOMAINS:
                findings.append(("personal email", match))
        findings.extend(("Windows user home", match) for match in WINDOWS_USER_HOME_RE.finditer(text))
        for match in POSIX_USER_HOME_RE.finditer(text):
            if match.group(1).lower() not in PORTABLE_POSIX_HOME_USERS:
                findings.append(("POSIX user home", match))
        for match in INTERNAL_HOST_RE.finditer(text):
            hostname = match.group(0).lower()
            if "<" not in hostname and hostname not in PORTABLE_INTERNAL_HOSTS:
                findings.append(("internal hostname", match))
        findings.extend(
            ("project/runtime marker", match)
            for match in PROJECT_RUNTIME_MARKER_RE.finditer(text)
        )

        for kind, match in sorted(findings, key=lambda item: (item[1].start(), item[0])):
            line_number = text.count("\n", 0, match.start()) + 1
            errors.append(f"Skill payload contains {kind}: {relative_path}:{line_number}")
    return errors


def snapshot_skill_files(root: Path) -> dict[str, Path]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file() and not is_ignored_file(path, root)
    }


def compare_skill_snapshot(source_root: Path, snapshot_root: Path) -> list[str]:
    source_files = source_skill_files(source_root)
    snapshot_files = snapshot_skill_files(snapshot_root)
    errors: list[str] = []

    for relative_path in sorted(source_files.keys() - snapshot_files.keys()):
        errors.append(f"Plugin snapshot missing file: {relative_path}")
    for relative_path in sorted(snapshot_files.keys() - source_files.keys()):
        errors.append(f"Plugin snapshot has extra file: {relative_path}")
    for relative_path in sorted(source_files.keys() & snapshot_files.keys()):
        if source_files[relative_path].read_bytes() != snapshot_files[relative_path].read_bytes():
            errors.append(f"Plugin snapshot content differs: {relative_path}")
    return errors


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
        validate_frontmatter(skill_file, text, errors)
        name_match = NAME_RE.search(text)
        if not name_match:
            errors.append(f"Missing or invalid name: {skill_file}")
        elif name_match.group(1) != skill_dir.name:
            errors.append(f"Skill name does not match directory: {skill_file} => {name_match.group(1)}")
        else:
            skill_names.add(name_match.group(1))
        if not DESCRIPTION_RE.search(text):
            errors.append(f"Missing description: {skill_file}")
        if not OUTPUT_LANGUAGE_RE.search(text):
            errors.append(f"Missing Simplified Chinese output rule: {skill_file}")
        if not TEMP_PATH_RE.search(text):
            errors.append(f"Missing temporary artifact path rule: {skill_file}")
        for reference_path in sorted(set(REFERENCE_PATH_RE.findall(text))):
            if not (skill_dir / reference_path).is_file():
                errors.append(f"Skill reference does not exist: {skill_file} => {reference_path}")
        agents_file = skill_dir / "agents" / "openai.yaml"
        if not agents_file.exists():
            errors.append(f"Missing agents metadata: {agents_file}")
        else:
            agents_text = agents_file.read_text(encoding="utf-8")
            default_prompt = yaml_string(agents_text, "default_prompt")
            if not default_prompt:
                errors.append(f"Missing agents default_prompt: {agents_file}")
            elif f"${skill_dir.name}" not in default_prompt:
                errors.append(f"agents default_prompt must mention ${skill_dir.name}: {agents_file}")
            if not IMPLICIT_INVOCATION_RE.search(agents_text):
                errors.append(f"agents metadata must explicitly allow implicit invocation: {agents_file}")
            for key in ("icon_small", "icon_large"):
                icon_path = yaml_string(agents_text, key)
                if not icon_path:
                    errors.append(f"Missing agents {key}: {agents_file}")
                else:
                    validate_relative_asset(skill_dir, icon_path, agents_file, errors)
    errors.extend(find_skill_privacy_violations(SKILLS_ROOT))
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
    errors.extend(compare_skill_snapshot(SKILLS_ROOT, PLUGIN_SKILLS_ROOT))


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
