from __future__ import annotations

import os
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.validate import ROOT, _example_policy_errors, validate


class ValidationTests(unittest.TestCase):
    def test_repository_protocol_is_valid(self) -> None:
        self.assertEqual([], validate())

    def test_custom_forbidden_term_is_detected(self) -> None:
        with patch.dict(os.environ, {"MHP_FORBIDDEN_TERMS": "Model Handoff Protocol"}):
            errors = validate()
        self.assertTrue(any("Model Handoff Protocol" in error for error in errors))

    def test_examples_cannot_defer_batch_gates_until_after_verification(self) -> None:
        cases = (
            (
                "examples/planner-to-implementer.md",
                "Only after every batch gate passes, return once for verification.",
                "Return for review before full regression.",
                "violates the verification boundary",
            ),
            (
                "examples/implementer-to-verifier.md",
                "Every focused and full-regression gate in the batch completed before handoff.",
                "Full regression has not run because the plan requires review first.",
                "violates the verification boundary",
            ),
            (
                "examples/capable-self-verification.md",
                "one boundary record, one self closeout, zero additional snapshots.",
                "Run snapshot and create a second handoff before self review.",
                "violates the verification boundary",
            ),
        )
        for relative, valid, invalid, expected in cases:
            with self.subTest(relative=relative):
                text = (ROOT / Path(relative)).read_text(encoding="utf-8")
                errors = _example_policy_errors(relative, text.replace(valid, invalid))
                self.assertTrue(any(expected in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
