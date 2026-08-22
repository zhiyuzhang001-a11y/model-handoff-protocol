from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.bootstrap import REPOSITORY_URL, _run_git, bootstrap, validate_ref


class BootstrapTests(unittest.TestCase):
    def test_ref_validation_accepts_branch_tag_and_commit_shapes(self) -> None:
        for ref in ("main", "v0.4.0", "release/0.4", "4f8a2b3"):
            self.assertEqual(ref, validate_ref(ref))

    def test_ref_validation_rejects_option_and_traversal_shapes(self) -> None:
        for ref in ("--upload-pack=bad", "../main", "feature//x", "main."):
            with self.subTest(ref=ref):
                with self.assertRaisesRegex(ValueError, "unsafe Git ref"):
                    validate_ref(ref)

    def test_bootstrap_fetches_then_delegates_without_shell(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)

            def fake_fetch(source: Path, ref: str) -> str:
                self.assertEqual("main", ref)
                installer = source / "scripts/install.py"
                installer.parent.mkdir(parents=True)
                installer.write_text("raise SystemExit(0)\n", encoding="utf-8")
                return "a" * 40

            completed = subprocess.CompletedProcess(args=[], returncode=0)
            with patch("scripts.bootstrap._fetch_source", side_effect=fake_fetch), patch(
                "scripts.bootstrap.subprocess.run", return_value=completed
            ) as run:
                code, revision = bootstrap(target, apply=True, json_output=True)

        self.assertEqual(0, code)
        self.assertEqual("a" * 40, revision)
        command = run.call_args.args[0]
        self.assertIn(str(target.resolve()), command)
        self.assertIn("--apply", command)
        self.assertIn("--json", command)
        self.assertFalse(run.call_args.kwargs["check"])
        self.assertNotIn("shell", run.call_args.kwargs)

    def test_bootstrap_rejects_missing_target_before_fetch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing"
            with patch("scripts.bootstrap._fetch_source") as fetch:
                with self.assertRaises(FileNotFoundError):
                    bootstrap(missing)
            fetch.assert_not_called()

    def test_repository_source_is_fixed_to_upstream(self) -> None:
        self.assertEqual(
            "https://github.com/zhiyuzhang001-a11y/model-handoff-protocol.git",
            REPOSITORY_URL,
        )

    def test_git_fetch_path_disables_prompts_and_has_a_timeout(self) -> None:
        completed = subprocess.CompletedProcess(args=[], returncode=0, stdout="ok\n")
        with patch("scripts.bootstrap.subprocess.run", return_value=completed) as run:
            self.assertEqual("ok", _run_git("rev-parse", "HEAD"))
        self.assertEqual("0", run.call_args.kwargs["env"]["GIT_TERMINAL_PROMPT"])
        self.assertEqual(60, run.call_args.kwargs["timeout"])
        self.assertTrue(run.call_args.kwargs["check"])
        self.assertNotIn("shell", run.call_args.kwargs)


if __name__ == "__main__":
    unittest.main()
