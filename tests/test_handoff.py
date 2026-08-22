from __future__ import annotations

import tempfile
import unittest
import subprocess
from unittest.mock import patch
from pathlib import Path

from scripts.handoff import (
    MAX_BOOTSTRAP_CHARACTERS,
    inspect_project,
    parse_markdown,
    render_snapshot,
)
from scripts.install import install


HANDOFF = """# Current model handoff

- Protocol version: `0.2`
- Handoff ID: `2026-08-22-m1-execute`
- State: `PLAN_TO_EXECUTE`
- From role: `planner/reviewer`
- To role: `implementer`
- Contract depth: `thin`
- Last verified: `2026-08-22T10:00:00Z`
- Active milestone: `docs/IMPLEMENTATION_PLAN.md#M1`
- Base branch: `main`
- Base HEAD: `abc1234`
- Working tree: `dirty`

## Objective and user-visible outcome

Deliver the bounded feature.

## Frozen scope and non-goals

Only the named module; no public API change.

## Acceptance and required evidence

Run the focused test and store its summary.

## Verified completed work

Baseline passed; do not repeat it.

## Remaining ordered work

1. Implement the local change.

## Exact next action

Inspect `src/service.py` and identify the smallest edit region.

## Context delta and evidence pointers

- Changed since previous handoff: M1 approved.
- Must read now: `docs/IMPLEMENTATION_PLAN.md#M1` for frozen acceptance.
- Read on demand: none.
- Evidence artifacts: `reports/M1_BASELINE.md`.
- Safe to skip: completed M0 history.

## Changes and repository state

No task-owned source change yet.

## Commands and results

Focused baseline exited zero with 12 tests.

## Decisions and rationale

Keep the public API unchanged.

## Risks, deviations, and unknowns

No known deviation.

## Authority and stop conditions

Continue locally; stop for a public API change.

## Owned live resources

None.

## Requested response from the next role

Implement and request ACCEPT_STAGE_1.
"""

STATUS = """# Current status

- Date: `2026-08-22`
- State: `M1 / ACTIVE`
- Active milestone: `docs/IMPLEMENTATION_PLAN.md#M1`
- Current handoff: `MODEL_HANDOFF.md`

## Completed

Baseline passed.

## Current constraints

No public API change.

## Next action

Inspect `src/service.py` and identify the smallest edit region.
"""


class HandoffTests(unittest.TestCase):
    def _project(self, directory: str) -> Path:
        target = Path(directory)
        install(target, apply=True)
        (target / "MODEL_HANDOFF.md").write_text(HANDOFF, encoding="utf-8")
        (target / "STATUS.md").write_text(STATUS, encoding="utf-8")
        (target / "docs/IMPLEMENTATION_PLAN.md").write_text(
            "# Implementation plan\n\n## M1\n\nFrozen acceptance.\n", encoding="utf-8"
        )
        return target

    def test_parser_separates_metadata_and_sections(self) -> None:
        record = parse_markdown(HANDOFF)
        self.assertEqual("0.2", record.metadata["Protocol version"])
        self.assertIn("Exact next action", record.sections)

    def test_parser_ignores_headings_inside_fenced_evidence(self) -> None:
        text = HANDOFF.replace(
            "Focused baseline exited zero with 12 tests.",
            "```text\n## not a real section\ncommand > result.log\n```",
        )
        record = parse_markdown(text)
        self.assertIn("## not a real section", record.sections["Commands and results"])
        self.assertNotIn("not a real section", record.sections)

    def test_valid_non_git_project_has_only_git_warning(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = inspect_project(self._project(directory))
        self.assertEqual([], result["errors"])
        self.assertTrue(any("Git state unavailable" in item for item in result["warnings"]))

    def test_detects_status_handoff_next_action_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._project(directory)
            (target / "STATUS.md").write_text(
                STATUS.replace("Inspect `src/service.py`", "Edit `src/service.py`"),
                encoding="utf-8",
            )
            result = inspect_project(target)
        self.assertTrue(any("Next action" in item for item in result["errors"]))

    def test_snapshot_is_bounded_and_contains_context_pointers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = inspect_project(self._project(directory))
            snapshot = render_snapshot(result)
        self.assertLessEqual(len(snapshot), MAX_BOOTSTRAP_CHARACTERS)
        self.assertIn("Context delta and evidence pointers", snapshot)
        self.assertIn("Observed", snapshot)

    def test_review_snapshot_adds_diff_commands_and_decisions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._project(directory)
            review = (
                HANDOFF.replace("PLAN_TO_EXECUTE", "EXECUTION_TO_REVIEW")
                .replace("- From role: `planner/reviewer`", "- From role: `implementer`")
                .replace("- To role: `implementer`", "- To role: `planner/reviewer`")
            )
            (target / "MODEL_HANDOFF.md").write_text(review, encoding="utf-8")
            snapshot = render_snapshot(inspect_project(target))
        self.assertIn("## Changes and repository state", snapshot)
        self.assertIn("## Commands and results", snapshot)
        self.assertIn("## Decisions and rationale", snapshot)

    def test_rejects_oversized_bootstrap_section(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._project(directory)
            oversized = HANDOFF.replace("No known deviation.", "x" * 1_201)
            (target / "MODEL_HANDOFF.md").write_text(oversized, encoding="utf-8")
            result = inspect_project(target)
        self.assertTrue(any("section exceeds" in item for item in result["errors"]))

    def test_detects_duplicate_section_and_invalid_verified_time(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._project(directory)
            invalid = HANDOFF.replace(
                "2026-08-22T10:00:00Z", "2026-08-22 10:00"
            ) + "\n## Exact next action\n\nDuplicate.\n"
            (target / "MODEL_HANDOFF.md").write_text(invalid, encoding="utf-8")
            errors = inspect_project(target)["errors"]
        self.assertTrue(any("Last verified" in item for item in errors))
        self.assertTrue(any("duplicate handoff section" in item for item in errors))

    def test_state_must_target_the_correct_role(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._project(directory)
            invalid = HANDOFF.replace(
                "- To role: `implementer`", "- To role: `planner/reviewer`"
            )
            (target / "MODEL_HANDOFF.md").write_text(invalid, encoding="utf-8")
            errors = inspect_project(target)["errors"]
        self.assertTrue(any("must target role implementer" in item for item in errors))

    def test_review_to_execute_requires_actionable_correction_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._project(directory)
            review = HANDOFF.replace("PLAN_TO_EXECUTE", "REVIEW_TO_EXECUTE")
            (target / "MODEL_HANDOFF.md").write_text(review, encoding="utf-8")
            errors = inspect_project(target)["errors"]
        self.assertTrue(any("Root invariant" in item for item in errors))
        self.assertTrue(any("Correction variants" in item for item in errors))
        self.assertTrue(any("Local implementation discretion" in item for item in errors))
        self.assertTrue(any("Rejected shallow fix" in item for item in errors))

    def test_nonbehavioral_review_correction_may_explain_no_variants(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._project(directory)
            review = HANDOFF.replace("PLAN_TO_EXECUTE", "REVIEW_TO_EXECUTE")
            review = review.replace(
                "Run the focused test and store its summary.",
                "Run the focused test and store its summary.\n\n"
                "- Root invariant: Published evidence must name the exact command.\n"
                "- Correction variants: not applicable — documentation-only correction.",
            ).replace(
                "Keep the public API unchanged.",
                "Keep the public API unchanged.\n\n"
                "- Local implementation discretion: Edit the named report only.\n"
                "- Rejected shallow fix: none.",
            )
            (target / "MODEL_HANDOFF.md").write_text(review, encoding="utf-8")
            result = inspect_project(target)
        self.assertEqual([], result["errors"])

    def test_missing_context_pointer_heading_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._project(directory)
            invalid = HANDOFF.replace("#M1`", "#Missing heading`")
            (target / "MODEL_HANDOFF.md").write_text(invalid, encoding="utf-8")
            errors = inspect_project(target)["errors"]
        self.assertTrue(any("pointer heading missing" in item for item in errors))

    def test_missing_git_executable_becomes_warning(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._project(directory)
            with patch("scripts.handoff.subprocess.run", side_effect=OSError):
                result = inspect_project(target)
        self.assertEqual([], result["errors"])
        self.assertTrue(any("Git state unavailable" in item for item in result["warnings"]))

    def test_detects_code_commit_after_recorded_git_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._project(directory)
            commands = (
                ("git", "init", "-b", "main"),
                ("git", "config", "user.name", "Test User"),
                ("git", "config", "user.email", "test@example.invalid"),
                ("git", "add", "."),
                ("git", "commit", "-m", "baseline"),
            )
            for command in commands:
                subprocess.run(command, cwd=target, check=True, stdout=subprocess.DEVNULL)
            head = subprocess.run(
                ("git", "rev-parse", "HEAD"),
                cwd=target,
                check=True,
                stdout=subprocess.PIPE,
                text=True,
            ).stdout.strip()
            (target / "MODEL_HANDOFF.md").write_text(
                HANDOFF.replace("abc1234", head), encoding="utf-8"
            )
            self.assertEqual([], inspect_project(target)["errors"])

            (target / "src.py").write_text("value = 1\n", encoding="utf-8")
            subprocess.run(("git", "add", "src.py"), cwd=target, check=True)
            subprocess.run(
                ("git", "commit", "-m", "unexpected code change"),
                cwd=target,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            errors = inspect_project(target)["errors"]
        self.assertTrue(any("stale base HEAD" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
