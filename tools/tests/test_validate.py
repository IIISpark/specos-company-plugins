from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.validate import compare_skill_snapshot


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


if __name__ == "__main__":
    unittest.main()
