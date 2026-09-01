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

    def test_chinese_writing_checks_high_frequency_scaffolds_with_exceptions(self) -> None:
        content = (REPO_ROOT / "skills" / "ispark-writing" / "references" / "chinese-writing.md").read_text(encoding="utf-8")
        for phrase in ("不是……而是……", "不仅……还……", "通过……从而……", "一方面……另一方面……"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)
        self.assertIn("不是禁句", content)
        self.assertIn("删除整组对照骨架", content)

    def test_chinese_ai_patterns_are_routed_on_demand_and_not_banned(self) -> None:
        skill = (REPO_ROOT / "skills" / "ispark-writing" / "SKILL.md").read_text(encoding="utf-8")
        patterns = (REPO_ROOT / "skills" / "ispark-writing" / "references" / "chinese-ai-patterns.md").read_text(encoding="utf-8")
        self.assertIn("references/chinese-ai-patterns.md", skill)
        self.assertIn("do not load its inventory for ordinary Chinese edits", skill)
        for phrase in ("局部密度", "不是违禁词表", "这次不是生产发布，而是本地试验", "不强制禁用"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, patterns)
        for cluster in ("假深刻", "三件套", "商务黑话", "伪口语", "金句收尾"):
            with self.subTest(cluster=cluster):
                self.assertIn(cluster, patterns)

    def test_skill_authoring_requires_pressure_test_loop(self) -> None:
        content = (REPO_ROOT / "skills" / "ispark-agent-tools" / "references" / "skill-authoring.md").read_text(encoding="utf-8")
        for phrase in ("RED/GREEN/REFACTOR", "pressure", "rationalization", "frontmatter or snapshot validation"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_architecture_routes_domain_model_changes_to_glossary_and_adr(self) -> None:
        content = (REPO_ROOT / "skills" / "ispark-dev-workflow" / "references" / "architecture.md").read_text(encoding="utf-8")
        for phrase in ("domain glossary", "concrete scenario", "hard to reverse", "working plan"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_review_and_react_owners_keep_expanded_source_boundaries(self) -> None:
        review = (REPO_ROOT / "skills" / "ispark-review-risk" / "references" / "code-review.md").read_text(encoding="utf-8")
        react = (REPO_ROOT / "skills" / "ispark-react-performance" / "references" / "react-performance.md").read_text(encoding="utf-8")
        agent_files = (REPO_ROOT / "skills" / "ispark-agent-tools" / "references" / "agent-instruction-files.md").read_text(encoding="utf-8")
        for phrase in ("IDOR", "race/TOCTOU", "neighboring implementations", "secret leakage"):
            with self.subTest(owner="review", phrase=phrase):
                self.assertIn(phrase, review)
        for phrase in ("barrel imports", "dynamic imports", "passive global listeners", "content-visibility"):
            with self.subTest(owner="react", phrase=phrase):
                self.assertIn(phrase, react)
        for phrase in ("one authoritative file", "repo-relative", "exact commands"):
            with self.subTest(owner="agent-files", phrase=phrase):
                self.assertIn(phrase, agent_files)

    def test_academic_owner_keeps_research_protocol_ledger(self) -> None:
        content = (REPO_ROOT / "skills" / "ispark-academic-writing" / "references" / "academic-method.md").read_text(encoding="utf-8")
        for phrase in ("source provenance", "dataset/version", "baseline", "original paper, data, code"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_skill_behavior_testing_reference_is_routable(self) -> None:
        skill = (REPO_ROOT / "skills" / "ispark-agent-tools" / "SKILL.md").read_text(encoding="utf-8")
        reference = (REPO_ROOT / "skills" / "ispark-agent-tools" / "references" / "skill-testing.md").read_text(encoding="utf-8")
        self.assertIn("references/skill-testing.md", skill)
        for phrase in ("RED", "GREEN", "REFACTOR", "three combined pressures", "Metadata, snapshots"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, reference)


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

    def test_tmeet_skill_is_short_and_routes_details_on_demand(self) -> None:
        skill_root = REPO_ROOT / "skills" / "ispark-tmeet"
        content = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        description = next(line.removeprefix("description: ") for line in content.splitlines() if line.startswith("description: "))
        self.assertLessEqual(len(description), 280)
        self.assertLessEqual(len(content.splitlines()), 70)
        for reference in ("auth", "meetings", "recordings", "reports", "contacts", "live-control", "troubleshooting"):
            with self.subTest(reference=reference):
                self.assertTrue((skill_root / "references" / f"{reference}-routing.md").is_file())
                self.assertIn(f"references/{reference}-routing.md", content)
        self.assertIn("allow_implicit_invocation: true", (skill_root / "agents" / "openai.yaml").read_text(encoding="utf-8"))

    def test_tmeet_skill_keeps_privacy_and_confirmation_boundaries(self) -> None:
        skill_root = REPO_ROOT / "skills" / "ispark-tmeet"
        content = "\n".join(path.read_text(encoding="utf-8") for path in skill_root.rglob("*.md"))
        for phrase in ("不是通用人员检索接口", "下一条明确确认", "meeting code", "next_page_token", "permission-apply-prepare"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)
        self.assertNotIn("npm install -g", content)
        self.assertNotIn("TMEET_AGENT", content)

    def test_tmeet_is_scoped_to_fallback_profiles(self) -> None:
        profiles = list((REPO_ROOT / "profiles").glob("*.yml"))
        self.assertEqual({path.stem for path in profiles if "- ispark-tmeet" in path.read_text(encoding="utf-8")}, {path.stem for path in profiles})

    def test_notion_skill_is_short_and_routes_details_on_demand(self) -> None:
        skill_root = REPO_ROOT / "skills" / "ispark-notion"
        content = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        description = next(line.removeprefix("description: ") for line in content.splitlines() if line.startswith("description: "))
        self.assertLessEqual(len(description), 280)
        self.assertLessEqual(len(content.splitlines()), 70)
        for reference in ("auth", "pages", "datasources", "files", "api", "workspace"):
            with self.subTest(reference=reference):
                self.assertTrue((skill_root / "references" / f"{reference}-routing.md").is_file())
                self.assertIn(f"references/{reference}-routing.md", content)
        self.assertIn("allow_implicit_invocation: true", (skill_root / "agents" / "openai.yaml").read_text(encoding="utf-8"))

    def test_notion_skill_keeps_authentication_and_mutation_boundaries(self) -> None:
        skill_root = REPO_ROOT / "skills" / "ispark-notion"
        content = "\n".join(path.read_text(encoding="utf-8") for path in skill_root.rglob("*.md"))
        for phrase in ("ntn auth token", "explicit confirmation", "Paginate only", "raw internal identifiers"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)
        for marker in ("NOTION_API_TOKEN", "curl -", "npm install -g"):
            with self.subTest(marker=marker):
                self.assertNotIn(marker, content)

    def test_notion_is_scoped_to_fallback_profiles(self) -> None:
        profiles = list((REPO_ROOT / "profiles").glob("*.yml"))
        self.assertEqual({path.stem for path in profiles if "- ispark-notion" in path.read_text(encoding="utf-8")}, {path.stem for path in profiles})

    def test_apifox_skill_is_short_and_routes_official_domains_on_demand(self) -> None:
        skill_root = REPO_ROOT / "skills" / "ispark-apifox"
        content = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        description = next(line.removeprefix("description: ") for line in content.splitlines() if line.startswith("description: "))
        self.assertLessEqual(len(description), 280)
        self.assertLessEqual(len(content.splitlines()), 70)
        for reference in ("cli", "contracts", "import-export", "test-case", "test-scenario", "automation", "branches", "troubleshooting", "lifecycle"):
            with self.subTest(reference=reference):
                self.assertTrue((skill_root / "references" / f"{reference}-routing.md").is_file())
                self.assertIn(f"references/{reference}-routing.md", content)
        self.assertIn("allow_implicit_invocation: true", (skill_root / "agents" / "openai.yaml").read_text(encoding="utf-8"))

    def test_apifox_skill_keeps_official_quality_and_safety_boundaries(self) -> None:
        skill_root = REPO_ROOT / "skills" / "ispark-apifox"
        content = "\n".join(path.read_text(encoding="utf-8") for path in skill_root.rglob("*.md"))
        for phrase in ("cli-schema validate", "agentHints", "empty object bodies", "ignored count", "pick-to", "Uploading a report"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)
        for marker in ("npm i -g", "npm install", "APIFOX_TOKEN", "--access-token <token>", "C:\\Users\\"):
            with self.subTest(marker=marker):
                self.assertNotIn(marker, content)

    def test_apifox_is_scoped_to_fallback_profiles(self) -> None:
        profiles = list((REPO_ROOT / "profiles").glob("*.yml"))
        self.assertEqual({path.stem for path in profiles if "- ispark-apifox" in path.read_text(encoding="utf-8")}, {path.stem for path in profiles})

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
