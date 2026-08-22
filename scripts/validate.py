#!/usr/bin/env python3
"""Validate protocol structure, rule bounds, and sanitized distributable text."""

from __future__ import annotations

import os
import re
from pathlib import Path

try:
    from .install import INSTALLS, ROOT
    from .handoff import PROTOCOL_VERSION, REQUIRED_METADATA, REQUIRED_SECTIONS, parse_markdown
except ImportError:  # Direct script execution.
    from install import INSTALLS, ROOT
    from handoff import PROTOCOL_VERSION, REQUIRED_METADATA, REQUIRED_SECTIONS, parse_markdown


RULES = (
    ROOT / ".cursor/rules/model-handoff.mdc",
    ROOT / ".cursor/rules/project-execution.mdc",
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

    handoff_text = (ROOT / "templates/MODEL_HANDOFF.md").read_text(encoding="utf-8")
    handoff = parse_markdown(handoff_text)
    for heading in REQUIRED_SECTIONS:
        if heading not in handoff.sections:
            errors.append(f"handoff template missing heading: {heading}")
    for key in REQUIRED_METADATA:
        if key not in handoff.metadata:
            errors.append(f"handoff template missing metadata: {key}")
    if handoff.metadata.get("Protocol version") != PROTOCOL_VERSION:
        errors.append("handoff template protocol version is not current")

    prompt_requirements = {
        "prompts/outgoing-handoff.txt": "handoff.py check",
        "prompts/incoming-implementer.txt": "handoff.py snapshot",
        "prompts/incoming-reviewer.txt": "handoff.py snapshot",
        "prompts/switch-out.txt": "检查交接",
        "prompts/switch-in.txt": "bootstrap",
    }
    for relative, required in prompt_requirements.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        if required not in text:
            errors.append(f"prompt missing compact workflow command: {relative}")

    policy_requirements = {
        ".cursor/rules/model-handoff.mdc": (
            "root invariant",
            "non-behavioral corrections",
            "external writes without explicit authority",
            "review before `main`",
            "Obey `Review mode`",
            "Never ask the user to choose a reviewer",
        ),
        "docs/MODEL_HANDOFF_PLAYBOOK.md": (
            "Root-cause corrections and bounded autonomy", "Do not invent adversarial cases",
            "A new dependency",
            "Never push an unreviewed target-project rule change directly to upstream `main`",
            "Milestone review versus specialized review",
            "The checker rejects missing, invalid, or state-conflicting modes",
        ),
        "templates/MODEL_HANDOFF.md": (
            "Root invariant:",
            "not applicable with reason",
            "no new dependency",
            "name exactly /review-bugbot or /review-security",
        ),
        "prompts/incoming-implementer.txt": (
            "root invariants", "returned behavioral defect", "introducing dependencies",
        ),
        "prompts/incoming-reviewer.txt": (
            "Obey the checked `Review mode`",
            "Never ask the user to choose between review modes",
        ),
        "templates/HANDOFF_FEEDBACK.md": (
            "project-specific | protocol-generic | unclear",
            "Candidate branch:",
            "Resolution proof:",
        ),
        "README.md": (
            "never push an unreviewed target-project rule directly to upstream `main`",
            "never asks the user to choose Bugbot or Security Review",
        ),
        "README.zh-CN.md": (
            "通用候选不应直接推送到GitHub `main`",
            "不应再让你二选一",
        ),
    }
    for relative, required_phrases in policy_requirements.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        for phrase in required_phrases:
            if phrase not in text:
                errors.append(f"required protocol policy missing from {relative}: {phrase}")

    for example in sorted((ROOT / "examples").glob("*.md")):
        text = example.read_text(encoding="utf-8")
        if "abbreviated teaching example, not a valid live packet" not in text:
            errors.append(f"example missing non-copyable warning: {example.relative_to(ROOT)}")

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
