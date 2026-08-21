from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from scripts.validate import validate


class ValidationTests(unittest.TestCase):
    def test_repository_protocol_is_valid(self) -> None:
        self.assertEqual([], validate())

    def test_custom_forbidden_term_is_detected(self) -> None:
        with patch.dict(os.environ, {"MHP_FORBIDDEN_TERMS": "Model Handoff Protocol"}):
            errors = validate()
        self.assertTrue(any("Model Handoff Protocol" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
