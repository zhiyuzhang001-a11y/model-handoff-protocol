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
EXAMPLE_REQUIREMENTS = {
    "examples/planner-to-implementer.md": (
        "full regression passes before any",
        "Only after every batch gate passes, return once for verification",
        "complete both focused and full regression gates",
    ),
    "examples/implementer-to-verifier.md": (
        "before this `EXECUTION_TO_VERIFY` packet",
        "Every focused and full-regression gate in the batch completed before handoff",
        "completed focused/full-regression evidence",
    ),
    "examples/capable-self-verification.md": (
        "one boundary record, one self closeout, zero additional snapshots",
        "Do not switch models or run snapshot",
        "proves only contract",
    ),
}
EXAMPLE_FORBIDDEN = {
    "examples/planner-to-implementer.md": (
        "Return for review before full regression",
    ),
    "examples/implementer-to-verifier.md": (
        "Full regression has not run",
        "authorize the full regression",
    ),
    "examples/capable-self-verification.md": (
        "Run snapshot and create a second handoff",
    ),
}


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


def _example_policy_errors(relative: str, text: str) -> list[str]:
    errors: list[str] = []
    for phrase in EXAMPLE_REQUIREMENTS.get(relative, ()):
        if phrase not in text:
            errors.append(f"example missing batch-boundary evidence in {relative}: {phrase}")
    for phrase in EXAMPLE_FORBIDDEN.get(relative, ()):
        if phrase in text:
            errors.append(f"example violates the verification boundary in {relative}: {phrase}")
    return errors


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

    control = parse_markdown(
        (ROOT / "templates/PROTOCOL_CONTROL.md").read_text(encoding="utf-8")
    )
    if control.metadata.get("Mode") != "active":
        errors.append("protocol control template must default to active")

    prompt_requirements = {
        "prompts/outgoing-handoff.txt": "handoff.py check",
        "prompts/incoming-implementer.txt": "handoff.py snapshot",
        "prompts/incoming-verifier.txt": "handoff.py snapshot",
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
            "economical implementers",
            "judgment-heavy or high-risk implementation",
            "observation/publication",
            "second post-fix failure",
            "Recommended capability: economical | capable",
            "not every check needs a model switch",
            "separate capable context",
            "independently verify before `main`",
            "Obey `Verification mode`",
            "Never ask the user to choose a reviewer",
            "return to the project handoff",
            ".model-handoff/CONTROL.md",
            "Mode: paused",
            "Only explicit user resume",
            "acceptance boundaries, not model switches or micro-steps",
            "integrated closeout, not a handoff",
            "contract/status/Git/routing consistency only",
        ),
        ".cursor/rules/project-execution.mdc": (
            "deterministic hooks/barriers",
            "second post-fix failure",
            "largest cohesive batch",
            "not a forced handoff boundary",
            "correction loops would cost as much",
            "batch acceptance boundary—not a model change",
        ),
        "docs/MODEL_HANDOFF_PLAYBOOK.md": (
            "Root-cause corrections and bounded autonomy", "Do not invent adversarial cases",
            "Capability-aware routing",
            "economical models implement most",
            "observation and publication",
            "If the same invariant fails a second time",
            "A new dependency",
            "Never push an unreviewed target-project rule change directly to upstream `main`",
            "Milestone verification depth versus specialized review",
            "Stage verification is mandatory; a model switch is not",
            "self-verification into a substitute for an independent gate",
            "The checker rejects missing, invalid, or state-conflicting modes",
            "Recover from an accidental specialized-review selector",
            "Pause or resume the protocol",
            "Updating, pausing, or resuming never deletes protocol files",
            "Execution-batch economics",
            "largest cohesive execution batch",
            "one consolidated",
            "Passing it proves only contract consistency",
            "integrated execution closeout, not a handoff",
            "same uncompacted context",
            "creates no second handoff",
        ),
        "templates/MODEL_HANDOFF.md": (
            "Root invariant:",
            "not applicable with reason",
            "High-risk coverage matrix:",
            "Recommended capability:",
            "Verification mode: `self | independent | bugbot | security | none`",
            "no new dependency",
            "name exactly /review-bugbot or /review-security",
            "without a model handoff or full snapshot reload",
        ),
        "templates/IMPLEMENTATION_PLAN.md": (
            "Execution routing:",
            "economical-batch | capable-direct | hybrid",
            "Batch boundary:",
            "Verification routing:",
            "one self closeout at the batch acceptance boundary",
            "High-risk coverage matrix:",
        ),
        "prompts/incoming-implementer.txt": (
            "root invariants", "returned behavioral defect", "introducing dependencies",
            "deterministic hooks or barriers", "second post-fix failure",
            "execute the entire", "approved batch",
        ),
        "prompts/incoming-verifier.txt": (
            "Obey the checked `Verification mode`",
            "never ask the user to choose between specialized reviewers",
            "For `self`, remain in the current capable context",
            "For `independent`, use a separate capable context",
            "most bounded, reversible, test-protected implementation",
            "preserve a separate verification gate whenever risk",
            "do not reload the snapshot",
            "one integrated",
        ),
        "templates/HANDOFF_FEEDBACK.md": (
            "project-specific | protocol-generic | unclear",
            "Candidate branch:",
            "Resolution proof:",
        ),
        "README.md": (
            "never push an unreviewed target-project rule directly to upstream `main`",
            "never asks the user to choose Bugbot or Security Review",
            "Recommended capability: economical | capable",
            "Verification mode: self | independent | bugbot | security | none",
            "Every stage is verified, but a model switch is not always required",
            "Do not select a reviewer",
            "Exit the model-handoff protocol and retain its files",
            "Resume the model-handoff protocol",
            "economical models most simple",
            "A second post-fix failure",
            "execution batch rather than many tiny handoffs",
            "capable-direct",
            "python3 .model-handoff/update.py .",
            "Preview first; never overwrite differs/conflict",
            "Verification is triggered by",
            "only a contract-consistency check",
        ),
        "README.zh-CN.md": (
            "通用候选不应直接推送到GitHub `main`",
            "不要选择审查器",
            "退出模型交接协议，保留文件",
            "恢复模型交接协议",
            "Recommended capability: economical | capable",
            "Verification mode: self | independent | bugbot | security | none",
            "不要选择审查器",
            "每个阶段都要",
            "不一定切换模型",
            "默认由经济模型执行大多数简单",
            "修复后第二次失败",
            "最大安全执行批次",
            "capable-direct",
            "python3 .model-handoff/update.py .",
            "绝不覆盖 differs 或 conflict",
            "复核由批次验收边界触发",
            "只是交接合同检查",
        ),
        "docs/REMOTE_INSTALL.md": (
            "One-sentence request for a project model",
            "only protocol-generic changes",
            "`differs` remain untouched",
            "migrating all protocol-owned schema and routing names together",
            "repository is public",
            "raw.githubusercontent.com",
            "without credentials",
        ),
        "scripts/bootstrap.py": (
            "REPOSITORY_URL",
            "validate_ref",
            "check=False",
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
        errors.extend(_example_policy_errors(example.relative_to(ROOT).as_posix(), text))

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
