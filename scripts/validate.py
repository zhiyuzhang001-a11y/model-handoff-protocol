#!/usr/bin/env python3
"""Validate protocol structure, rule bounds, and sanitized distributable text."""

from __future__ import annotations

import os
import re
from pathlib import Path

try:
    from .install import INSTALLS, ROOT
except ImportError:  # Direct script execution.
    from install import INSTALLS, ROOT


RULES = (
    ROOT / ".cursor/rules/model-handoff.mdc",
    ROOT / ".cursor/rules/project-execution.mdc",
)
REQUIRED_HANDOFF_HEADINGS = (
    "Objective and user-visible outcome",
    "Frozen scope and non-goals",
    "Acceptance and required evidence",
    "Verified completed work",
    "Remaining ordered work",
    "Exact next action",
    "Changes and repository state",
    "Commands and results",
    "Decisions and rationale",
    "Risks, deviations, and unknowns",
    "Authority and stop conditions",
    "Owned live resources",
    "Requested response from the next role",
)
PRIVATE_PATH_PATTERNS = (
    re.compile(r"/Users/[A-Za-z0-9._-]+/"),
    re.compile(r"/home/[A-Za-z0-9._-]+/"),
    re.compile(r"[A-Za-z]:\\Users\\[A-Za-z0-9._-]+\\"),
)


def _forbidden_terms() -> tuple[str, ...]:
    raw = os.environ.get("MHP_FORBIDDEN_TERMS", "")
    return tuple(term.strip() for term in raw.split(",") if term.strip())


def _text_files() -> list[Path]:
    paths: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.name == "LICENSE":
            continue
        if path.suffix.lower() in {".md", ".mdc", ".txt", ".py", ".yml", ".yaml"}:
            paths.append(path)
    return sorted(paths)


def validate() -> list[str]:
    errors: list[str] = []
    for rule in RULES:
        lines = rule.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0] != "---" or "---" not in lines[1:]:
            errors.append(f"invalid frontmatter: {rule.relative_to(ROOT)}")
        if "alwaysApply: true" not in lines:
            errors.append(f"rule must always apply: {rule.relative_to(ROOT)}")
        if len(lines) > 50:
            errors.append(f"rule exceeds 50 lines: {rule.relative_to(ROOT)} ({len(lines)})")

    handoff = (ROOT / "templates/MODEL_HANDOFF.md").read_text(encoding="utf-8")
    for heading in REQUIRED_HANDOFF_HEADINGS:
        if f"## {heading}" not in handoff:
            errors.append(f"handoff template missing heading: {heading}")

    for source, _ in INSTALLS:
        if not (ROOT / source).is_file():
            errors.append(f"installer source missing: {source}")

    for path in _text_files():
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        for forbidden in _forbidden_terms():
            if forbidden in text:
                errors.append(f"private/project-specific text in {relative}: {forbidden}")
        for pattern in PRIVATE_PATH_PATTERNS:
            if pattern.search(text):
                errors.append(f"absolute user path in {relative}: {pattern.pattern}")
        for line_number, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                errors.append(f"trailing whitespace: {relative}:{line_number}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"protocol validation: PASS ({len(_text_files())} text files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
