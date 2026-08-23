from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.install import INSTALLS, install


class InstallerTests(unittest.TestCase):
    def test_dry_run_creates_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            result = install(target)
            self.assertEqual("dry-run", result["mode"])
            self.assertTrue(all(item["status"] == "would_create" for item in result["entries"]))
            for _, destination in INSTALLS:
                self.assertFalse((target / destination).exists())

    def test_apply_installs_all_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            result = install(target, apply=True)
            self.assertTrue(all(item["status"] == "created" for item in result["entries"]))
            for _, destination in INSTALLS:
                self.assertTrue((target / destination).is_file())
            self.assertTrue((target / ".model-handoff/handoff.py").is_file())
            self.assertTrue((target / ".model-handoff/update.py").is_file())

    def test_installed_project_contains_improvement_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            install(target, apply=True)
            feedback = (target / ".model-handoff/FEEDBACK.md").read_text(encoding="utf-8")
            playbook = (target / "docs/MODEL_HANDOFF_PLAYBOOK.md").read_text(
                encoding="utf-8"
            )
            rule = (target / ".cursor/rules/model-handoff.mdc").read_text(
                encoding="utf-8"
            )
            execution_rule = (
                target / ".cursor/rules/project-execution.mdc"
            ).read_text(encoding="utf-8")
            handoff = (target / "MODEL_HANDOFF.md").read_text(encoding="utf-8")
            plan = (target / "docs/IMPLEMENTATION_PLAN.md").read_text(
                encoding="utf-8"
            )
            updater = (target / ".model-handoff/update.py").read_text(
                encoding="utf-8"
            )
            recovery = (
                target / ".model-handoff/recover-review-selector.txt"
            ).read_text(encoding="utf-8")
            control = (target / ".model-handoff/CONTROL.md").read_text(
                encoding="utf-8"
            )
        self.assertIn("project-specific | protocol-generic | unclear", feedback)
        self.assertIn("Never push an unreviewed target-project rule", playbook)
        self.assertIn("Milestone verification depth versus specialized review", playbook)
        self.assertIn("independently verify before `main`", rule)
        self.assertIn("Never ask the user to choose a reviewer", rule)
        self.assertIn("return to the project handoff", rule)
        self.assertIn("never infer a specialized gate", rule)
        self.assertIn("economical implementers", rule)
        self.assertIn("second post-fix failure", rule)
        self.assertIn("Capability-aware routing", playbook)
        self.assertIn("deterministic hooks/barriers", execution_rule)
        self.assertIn("largest cohesive batch", execution_rule)
        self.assertIn("not a forced handoff boundary", execution_rule)
        self.assertIn(
            "Verification mode: `self | independent | bugbot | security | none`",
            handoff,
        )
        self.assertIn("Recommended capability: `economical | capable`", handoff)
        self.assertIn("name exactly /review-bugbot or /review-security", handoff)
        self.assertIn("High-risk coverage matrix", handoff)
        self.assertIn("Execution routing", plan)
        self.assertIn("economical-batch | capable-direct | hybrid", plan)
        self.assertIn("Batch boundary", plan)
        self.assertIn("REPOSITORY_URL", updater)
        self.assertIn("check=False", updater)
        self.assertIn("不要选择审查器", recovery)
        self.assertIn("Verification mode", recovery)
        self.assertIn("Mode: `active`", control)
        self.assertIn("退出模型交接协议，保留文件。", control)
        self.assertIn("恢复模型交接协议。", control)

    def test_apply_never_overwrites_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            existing = target / "STATUS.md"
            existing.write_text("user-owned\n", encoding="utf-8")
            result = install(target, apply=True)
            status = next(item for item in result["entries"] if item["path"] == "STATUS.md")
            self.assertEqual("differs", status["status"])
            self.assertEqual("user-owned\n", existing.read_text(encoding="utf-8"))

    def test_apply_never_overwrites_existing_update_helper(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            existing = target / ".model-handoff/update.py"
            existing.parent.mkdir()
            existing.write_text("# project-pinned updater\n", encoding="utf-8")
            result = install(target, apply=True)
            updater = next(
                item
                for item in result["entries"]
                if item["path"] == ".model-handoff/update.py"
            )
            self.assertEqual("differs", updater["status"])
            self.assertEqual(
                "# project-pinned updater\n", existing.read_text(encoding="utf-8")
            )

    def test_repeat_install_reports_identical_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            install(target, apply=True)
            result = install(target, apply=True)
            self.assertTrue(all(item["status"] == "identical" for item in result["entries"]))

    def test_existing_directory_at_destination_is_a_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "STATUS.md").mkdir()
            result = install(target)
            status = next(item for item in result["entries"] if item["path"] == "STATUS.md")
            self.assertEqual("conflict", status["status"])

    def test_rejects_missing_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing"
            with self.assertRaisesRegex(ValueError, "target does not exist"):
                install(missing)

    def test_rejects_symlinked_destination_parent(self) -> None:
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            target = Path(directory)
            cursor = target / ".cursor"
            cursor.symlink_to(Path(outside), target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "destination parent is a symlink"):
                install(target, apply=True)


if __name__ == "__main__":
    unittest.main()
