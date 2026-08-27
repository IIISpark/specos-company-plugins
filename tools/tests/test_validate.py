from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

from tools.install_or_update import update_marketplace
from tools.validate import compare_skill_snapshot


REPO_ROOT = Path(__file__).resolve().parents[2]


class CompareSkillSnapshotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        root = Path(self.temporary_directory.name)
        self.source_root = root / "source"
        self.snapshot_root = root / "snapshot"
        self.source_root.mkdir()
        self.snapshot_root.mkdir()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write_skill_file(self, root: Path, relative_path: str, content: str) -> None:
        skill_file = root / "ispark-example" / "SKILL.md"
        skill_file.parent.mkdir(parents=True, exist_ok=True)
        if not skill_file.exists():
            skill_file.write_text("---\nname: ispark-example\n---\n", encoding="utf-8")
        path = root / "ispark-example" / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_matching_snapshot_has_no_errors(self) -> None:
        self.write_skill_file(self.source_root, "references/detail.md", "same\n")
        self.write_skill_file(self.snapshot_root, "references/detail.md", "same\n")

        self.assertEqual(compare_skill_snapshot(self.source_root, self.snapshot_root), [])

    def test_stale_content_is_reported(self) -> None:
        self.write_skill_file(self.source_root, "references/detail.md", "current\n")
        self.write_skill_file(self.snapshot_root, "references/detail.md", "stale\n")

        errors = compare_skill_snapshot(self.source_root, self.snapshot_root)

        self.assertIn(
            "Plugin snapshot content differs: ispark-example/references/detail.md",
            errors,
        )

    def test_missing_and_extra_files_are_reported(self) -> None:
        self.write_skill_file(self.source_root, "references/source-only.md", "source\n")
        self.write_skill_file(self.snapshot_root, "references/snapshot-only.md", "snapshot\n")

        errors = compare_skill_snapshot(self.source_root, self.snapshot_root)

        self.assertIn(
            "Plugin snapshot missing file: ispark-example/references/source-only.md",
            errors,
        )
        self.assertIn(
            "Plugin snapshot has extra file: ispark-example/references/snapshot-only.md",
            errors,
        )

    def test_builder_ignored_files_do_not_cause_drift(self) -> None:
        self.write_skill_file(self.source_root, "references/detail.md", "same\n")
        self.write_skill_file(self.snapshot_root, "references/detail.md", "same\n")
        ignored_file = self.source_root / "ispark-example" / "__pycache__" / "helper.pyc"
        ignored_file.parent.mkdir(parents=True)
        ignored_file.write_bytes(b"ignored")

        self.assertEqual(compare_skill_snapshot(self.source_root, self.snapshot_root), [])
class UpdateMarketplaceTests(unittest.TestCase):
    @patch("tools.install_or_update.run")
    def test_local_marketplace_skips_git_upgrade_error(self, run_mock: object) -> None:
        run_mock.return_value = CompletedProcess(
            args=["codex", "plugin", "marketplace", "upgrade", "ispark-company"],
            returncode=1,
            stdout="",
            stderr="Error: marketplace `ispark-company` is not configured as a Git marketplace",
        )

        update_marketplace("codex", "ispark-company")

        run_mock.assert_called_once_with(
            ["codex", "plugin", "marketplace", "upgrade", "ispark-company"],
            check=False,
        )

    @patch("tools.install_or_update.run")
    def test_other_marketplace_upgrade_error_stops(self, run_mock: object) -> None:
        run_mock.return_value = CompletedProcess(
            args=["codex", "plugin", "marketplace", "upgrade", "ispark-company"],
            returncode=1,
            stdout="",
            stderr="Error: network unavailable",
        )

        with self.assertRaises(SystemExit) as error:
            update_marketplace("codex", "ispark-company")

        self.assertEqual(error.exception.code, 1)


class QualityRoutingTests(unittest.TestCase):
    def test_anti_slop_entry_routes_to_domain_owners(self) -> None:
        content = (REPO_ROOT / "skills" / "ispark-anti-slop" / "SKILL.md").read_text(encoding="utf-8")

        for skill_name in (
            "$ispark-writing",
            "$ispark-academic-writing",
            "$ispark-product-design",
            "$ispark-dev-workflow",
        ):
            with self.subTest(skill_name=skill_name):
                self.assertIn(skill_name, content)

    def test_academic_skill_is_scoped_to_research_profile(self) -> None:
        research = (REPO_ROOT / "profiles" / "research.yml").read_text(encoding="utf-8")
        self.assertIn("- ispark-academic-writing", research)

        for profile_name in ("backend", "frontend", "ops", "product"):
            content = (REPO_ROOT / "profiles" / f"{profile_name}.yml").read_text(encoding="utf-8")
            with self.subTest(profile_name=profile_name):
                self.assertNotIn("ispark-academic-writing", content)

    def test_routes_define_short_circuit_and_negative_boundaries(self) -> None:
        anti_slop = (REPO_ROOT / "skills" / "ispark-anti-slop" / "SKILL.md").read_text(encoding="utf-8")
        routing = (REPO_ROOT / "skills" / "ispark-anti-slop" / "references" / "routing.md").read_text(encoding="utf-8")
        normalized_anti_slop = " ".join(anti_slop.split())

        self.assertIn("Do not load this skill's routing reference", normalized_anti_slop)
        self.assertIn("no more than the two owner skills", normalized_anti_slop)
        self.assertIn("Do not load `ispark-anti-slop` again after handoff", routing)

        boundaries = {
            "ispark-writing": "visual or interaction changes use ispark-product-design",
            "ispark-product-design": "wording-only edits use ispark-writing",
            "ispark-dev-workflow": "review-only use ispark-review-risk",
            "ispark-review-risk": "For implementation use ispark-dev-workflow",
        }
        for skill_name, boundary in boundaries.items():
            with self.subTest(skill_name=skill_name):
                content = (REPO_ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(boundary, content)


class CandidateSkillIntegrationTests(unittest.TestCase):
    def test_specialized_skills_are_implicitly_discoverable_and_runtime_free(self) -> None:
        for skill_name in ("ispark-codebase-understanding", "ispark-react-performance"):
            with self.subTest(skill_name=skill_name):
                skill_root = REPO_ROOT / "skills" / skill_name
                agents = (skill_root / "agents" / "openai.yaml").read_text(encoding="utf-8")
                self.assertIn("allow_implicit_invocation: true", agents)
                self.assertFalse((skill_root / "scripts").exists())

    def test_specialized_skills_keep_nearby_negative_boundaries(self) -> None:
        boundaries = {
            "ispark-codebase-understanding": (
                "large unfamiliar codebase",
                "Do not use for routine edits",
            ),
            "ispark-react-performance": (
                "React or Next.js",
                "Do not use for visual design",
            ),
        }
        for skill_name, phrases in boundaries.items():
            with self.subTest(skill_name=skill_name):
                content = (REPO_ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
                for phrase in phrases:
                    self.assertIn(phrase, content)

    def test_specialized_discovery_entries_stay_within_context_budget(self) -> None:
        for skill_name in ("ispark-codebase-understanding", "ispark-react-performance"):
            with self.subTest(skill_name=skill_name):
                content = (REPO_ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
                description = next(
                    line.removeprefix("description: ")
                    for line in content.splitlines()
                    if line.startswith("description: ")
                )
                self.assertLessEqual(len(description), 280)
                self.assertLessEqual(len(content.splitlines()), 35)

    def test_fallback_profiles_scope_specialized_skills(self) -> None:
        expected_profiles = {
            "ispark-codebase-understanding": {
                "agent-maintainer",
                "backend",
                "dramawork",
                "engineer",
                "frontend",
            },
            "ispark-react-performance": {"dramawork", "engineer", "frontend"},
        }
        profile_paths = sorted((REPO_ROOT / "profiles").glob("*.yml"))

        for skill_name, expected in expected_profiles.items():
            actual = {
                path.stem
                for path in profile_paths
                if f"- {skill_name}" in path.read_text(encoding="utf-8")
            }
            with self.subTest(skill_name=skill_name):
                self.assertEqual(actual, expected)

    def test_candidate_methods_live_under_existing_owners(self) -> None:
        owner_references = {
            "ispark-dev-workflow": (
                "references/planning.md",
                "references/testing.md",
                "references/architecture.md",
                "references/verification.md",
            ),
            "ispark-review-risk": ("references/audit-context.md",),
            "ispark-agent-tools": ("references/subagents.md",),
        }
        for skill_name, references in owner_references.items():
            skill_root = REPO_ROOT / "skills" / skill_name
            entrypoint = (skill_root / "SKILL.md").read_text(encoding="utf-8")
            for reference in references:
                with self.subTest(skill_name=skill_name, reference=reference):
                    self.assertTrue((skill_root / reference).is_file())
                    self.assertIn(f"`{reference}`", entrypoint)


class SkillPrivacyBoundaryTests(unittest.TestCase):
    def test_source_skills_exclude_project_specific_temporal_identifiers(self) -> None:
        forbidden_markers = (
            "dramawork",
            "DramaWork",
            "DRAMAWORK_",
            "dw:v2:",
            "X-DW-",
            "/var/tmp/dramawork",
            "prometheus-operated.monitoring.svc.cluster.local",
            "pypi.company.internal",
        )
        text_files = [
            path
            for path in (REPO_ROOT / "skills").rglob("*")
            if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".toml", ".py"}
        ]

        for path in text_files:
            content = path.read_text(encoding="utf-8")
            for marker in forbidden_markers:
                with self.subTest(path=path.relative_to(REPO_ROOT), marker=marker):
                    self.assertNotIn(marker, content)


class SkillIconMetadataTests(unittest.TestCase):
    def test_all_source_skills_have_resolved_icon_assets(self) -> None:
        for skill_root in sorted((REPO_ROOT / "skills").iterdir()):
            if not skill_root.is_dir() or not (skill_root / "SKILL.md").is_file():
                continue
            agents = (skill_root / "agents" / "openai.yaml").read_text(encoding="utf-8")
            for key in ("icon_small", "icon_large"):
                with self.subTest(skill=skill_root.name, key=key):
                    match = re.search(
                        rf'^\s*{key}:\s*"(\./assets/[^"\n]+)"\s*$',
                        agents,
                        flags=re.MULTILINE,
                    )
                    self.assertIsNotNone(match)
                    self.assertTrue((skill_root / match.group(1)[2:]).is_file())


if __name__ == "__main__":
    unittest.main()
