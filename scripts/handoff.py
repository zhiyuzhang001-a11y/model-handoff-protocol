#!/usr/bin/env python3
"""Check a live model handoff and render a bounded bootstrap snapshot."""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


PROTOCOL_VERSION = "0.4"
VALID_STATES = {
    "PLAN_TO_EXECUTE",
    "EXECUTION_TO_REVIEW",
    "REVIEW_TO_EXECUTE",
    "BLOCKED_TO_DECIDE",
    "COMPLETE",
    "IDLE",
}
VALID_ROLES = {"planner/reviewer", "implementer"}
VALID_CAPABILITIES = {"economical", "capable"}
VALID_CONTRACT_DEPTHS = {"thin", "standard", "high-risk"}
VALID_REVIEW_MODES = {"inline", "bugbot", "security", "none"}
EXPECTED_TARGET_ROLE = {
    "PLAN_TO_EXECUTE": "implementer",
    "REVIEW_TO_EXECUTE": "implementer",
    "EXECUTION_TO_REVIEW": "planner/reviewer",
    "BLOCKED_TO_DECIDE": "planner/reviewer",
    "COMPLETE": "planner/reviewer",
    "IDLE": "planner/reviewer",
}
EXPECTED_SOURCE_ROLE = {
    "PLAN_TO_EXECUTE": "planner/reviewer",
    "REVIEW_TO_EXECUTE": "planner/reviewer",
    "EXECUTION_TO_REVIEW": "implementer",
    "COMPLETE": "planner/reviewer",
    "IDLE": "planner/reviewer",
}
REQUIRED_FILES = (
    Path(".cursor/rules/model-handoff.mdc"),
    Path(".cursor/rules/project-execution.mdc"),
    Path("MODEL_HANDOFF.md"),
    Path("STATUS.md"),
    Path("docs/IMPLEMENTATION_PLAN.md"),
    Path("docs/MODEL_HANDOFF_PLAYBOOK.md"),
)
REQUIRED_METADATA = (
    "Protocol version",
    "Handoff ID",
    "State",
    "From role",
    "To role",
    "Recommended capability",
    "Review mode",
    "Contract depth",
    "Last verified",
    "Active milestone",
    "Base branch",
    "Base HEAD",
    "Working tree",
)
REQUIRED_SECTIONS = (
    "Objective and user-visible outcome",
    "Frozen scope and non-goals",
    "Acceptance and required evidence",
    "Verified completed work",
    "Remaining ordered work",
    "Exact next action",
    "Context delta and evidence pointers",
    "Changes and repository state",
    "Commands and results",
    "Decisions and rationale",
    "Risks, deviations, and unknowns",
    "Authority and stop conditions",
    "Owned live resources",
    "Requested response from the next role",
)
BOOTSTRAP_SECTIONS = (
    "Objective and user-visible outcome",
    "Frozen scope and non-goals",
    "Acceptance and required evidence",
    "Verified completed work",
    "Remaining ordered work",
    "Exact next action",
    "Context delta and evidence pointers",
    "Risks, deviations, and unknowns",
    "Authority and stop conditions",
    "Owned live resources",
    "Requested response from the next role",
)
REVIEW_BOOTSTRAP_SECTIONS = (
    "Changes and repository state",
    "Commands and results",
    "Decisions and rationale",
)
MAX_HANDOFF_CHARACTERS = 9_000
MAX_STATUS_CHARACTERS = 3_000
MAX_BOOTSTRAP_CHARACTERS = 7_000
MAX_BOOTSTRAP_SECTION_CHARACTERS = 1_200
PLACEHOLDER_PATTERN = re.compile(r"<[A-Za-z][^>\n]*>")
CONTEXT_FIELDS = (
    "Changed since previous handoff",
    "Must read now",
    "Read on demand",
    "Evidence artifacts",
    "Safe to skip",
)


@dataclass(frozen=True)
class MarkdownRecord:
    metadata: dict[str, str]
    sections: dict[str, str]


def _clean(value: str) -> str:
    return " ".join(value.replace("`", "").split()).strip()


def _is_placeholder(value: str) -> bool:
    cleaned = _clean(value)
    return not cleaned or PLACEHOLDER_PATTERN.search(cleaned) is not None


def parse_markdown(text: str) -> MarkdownRecord:
    metadata: dict[str, str] = {}
    sections: dict[str, list[str]] = {}
    current: str | None = None
    fence: str | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        marker = stripped[:3]
        if marker in {"```", "~~~"}:
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            if current is not None:
                sections[current].append(line)
            continue
        if fence is not None:
            if current is not None:
                sections[current].append(line)
            continue
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            current = heading.group(1)
            sections.setdefault(current, [])
            continue
        if current is None:
            item = re.match(r"^-\s+([^:]+):\s*(.*)$", line)
            if item:
                metadata[item.group(1).strip()] = _clean(item.group(2))
            continue
        sections[current].append(line)
    return MarkdownRecord(
        metadata=metadata,
        sections={name: "\n".join(lines).strip() for name, lines in sections.items()},
    )


def _bullet_fields(text: str) -> dict[str, str]:
    fields: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        item = re.match(r"^-\s+([^:]+):\s*(.*)$", line)
        if item:
            current = item.group(1).strip()
            fields.setdefault(current, []).append(item.group(2).strip())
        elif current and line.strip():
            fields[current].append(line.strip())
    return {key: " ".join(parts).strip() for key, parts in fields.items()}


def _validate_path_pointer(root: Path, pointer: str, key: str, errors: list[str]) -> None:
    path_text, separator, heading = pointer.partition("#")
    relative = Path(path_text)
    if relative.is_absolute() or ".." in relative.parts:
        errors.append(f"unsafe context pointer in {key}: {pointer}")
        return
    target = root / relative
    if not target.is_file():
        errors.append(f"context pointer target missing in {key}: {path_text}")
        return
    if separator:
        try:
            target_text = target.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(f"context pointer is not readable text in {key}: {pointer}")
            return
        pattern = rf"^#{{1,6}}\s+{re.escape(heading)}\s*$"
        if not re.search(pattern, target_text, re.MULTILINE):
            errors.append(f"context pointer heading missing in {key}: {pointer}")


def _validate_context_pointers(root: Path, content: str, errors: list[str]) -> None:
    fields = _bullet_fields(content)
    for key in CONTEXT_FIELDS:
        if key not in fields or _is_placeholder(fields[key]):
            errors.append(f"context field missing or placeholder: {key}")
    for key in ("Must read now", "Read on demand"):
        value = fields.get(key, "")
        if re.fullmatch(r"none[.!]?", _clean(value).lower()):
            continue
        pointers = re.findall(r"`([^`]+)`", value)
        if not pointers:
            errors.append(f"{key} must use backticked relative path pointers or none")
            continue
        for pointer in pointers:
            _validate_path_pointer(root, pointer, key, errors)


def _is_bare_inapplicable(value: str) -> bool:
    return _clean(value).lower().rstrip(".") in {"none", "n/a", "not applicable"}


def _validate_review_correction(handoff: MarkdownRecord, errors: list[str]) -> None:
    """Require actionable correction data only when review returns work."""
    if handoff.metadata.get("State") != "REVIEW_TO_EXECUTE":
        return

    acceptance = _bullet_fields(
        handoff.sections.get("Acceptance and required evidence", "")
    )
    decisions = _bullet_fields(handoff.sections.get("Decisions and rationale", ""))
    required = (
        (acceptance, "Root invariant"),
        (acceptance, "Correction variants"),
        (decisions, "Local implementation discretion"),
        (decisions, "Rejected shallow fix"),
    )
    for fields, key in required:
        value = fields.get(key, "")
        if _is_placeholder(value):
            errors.append(f"REVIEW_TO_EXECUTE requires correction field: {key}")
        elif key in {
            "Root invariant",
            "Correction variants",
        } and _is_bare_inapplicable(value):
            errors.append(
                f"REVIEW_TO_EXECUTE {key} cannot be bare none/not applicable; "
                "state the invariant or give a non-behavioral reason"
            )


def _validate_high_risk_contract(handoff: MarkdownRecord, errors: list[str]) -> None:
    """Require an explicit coverage matrix or a reasoned inapplicability record."""
    if handoff.metadata.get("Contract depth") != "high-risk":
        return
    acceptance = _bullet_fields(
        handoff.sections.get("Acceptance and required evidence", "")
    )
    value = acceptance.get("High-risk coverage matrix", "")
    if _is_placeholder(value):
        errors.append("high-risk contract requires High-risk coverage matrix")
    elif _is_bare_inapplicable(value):
        errors.append(
            "high-risk coverage matrix cannot be bare none/not applicable; "
            "list applicable dimensions or give a reason"
        )


def _git(root: Path, *args: str) -> tuple[int, str]:
    try:
        process = subprocess.run(
            ("git", "-C", str(root), *args),
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except OSError:
        return 127, ""
    return process.returncode, process.stdout.strip()


def observed_git(root: Path) -> dict[str, Any]:
    branch_code, branch = _git(root, "branch", "--show-current")
    head_code, head = _git(root, "rev-parse", "HEAD")
    status_code, status = _git(root, "status", "--porcelain=v1")
    if branch_code or head_code or status_code:
        return {"available": False}
    changed = [line for line in status.splitlines() if line]
    return {
        "available": True,
        "branch": branch or "detached",
        "head": head,
        "working_tree": "dirty" if changed else "clean",
        "changed_count": len(changed),
        "changed_paths": changed[:30],
    }


def inspect_project(root: Path) -> dict[str, Any]:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    handoff_path = root / "MODEL_HANDOFF.md"
    status_path = root / "STATUS.md"
    if not handoff_path.is_file() or not status_path.is_file():
        return {"root": root, "errors": errors, "warnings": warnings}

    handoff_text = handoff_path.read_text(encoding="utf-8")
    status_text = status_path.read_text(encoding="utf-8")
    handoff = parse_markdown(handoff_text)
    status = parse_markdown(status_text)

    handoff_preamble = handoff_text.split("\n## ", 1)[0]
    for key in REQUIRED_METADATA:
        occurrences = len(
            re.findall(rf"^-\s+{re.escape(key)}:\s*", handoff_preamble, re.MULTILINE)
        )
        if occurrences > 1:
            errors.append(f"duplicate handoff metadata: {key}")

    if len(handoff_text) > MAX_HANDOFF_CHARACTERS:
        errors.append(
            f"MODEL_HANDOFF.md exceeds {MAX_HANDOFF_CHARACTERS} characters; "
            "move detail to evidence artifacts"
        )
    if len(status_text) > MAX_STATUS_CHARACTERS:
        errors.append(
            f"STATUS.md exceeds {MAX_STATUS_CHARACTERS} characters; keep it as a dashboard"
        )

    for key in REQUIRED_METADATA:
        value = handoff.metadata.get(key, "")
        if _is_placeholder(value):
            errors.append(f"handoff metadata missing or placeholder: {key}")
    if handoff.metadata.get("Protocol version") != PROTOCOL_VERSION:
        errors.append(
            f"protocol version must be {PROTOCOL_VERSION}: "
            f"{handoff.metadata.get('Protocol version', 'missing')}"
        )
    if handoff.metadata.get("State") not in VALID_STATES:
        errors.append(f"invalid handoff state: {handoff.metadata.get('State', 'missing')}")
    for key in ("From role", "To role"):
        if handoff.metadata.get(key) not in VALID_ROLES:
            errors.append(f"invalid {key.lower()}: {handoff.metadata.get(key, 'missing')}")
    capability = handoff.metadata.get("Recommended capability", "")
    if capability not in VALID_CAPABILITIES:
        errors.append(f"invalid recommended capability: {capability or 'missing'}")
    if handoff.metadata.get("Contract depth") not in VALID_CONTRACT_DEPTHS:
        errors.append(
            f"invalid contract depth: {handoff.metadata.get('Contract depth', 'missing')}"
        )
    state = handoff.metadata.get("State", "")
    expected_role = EXPECTED_TARGET_ROLE.get(state)
    if expected_role and handoff.metadata.get("To role") != expected_role:
        errors.append(f"state {state} must target role {expected_role}")
    expected_source = EXPECTED_SOURCE_ROLE.get(state)
    if expected_source and handoff.metadata.get("From role") != expected_source:
        errors.append(f"state {state} must originate from role {expected_source}")
    if handoff.metadata.get("To role") == "planner/reviewer" and capability != "capable":
        errors.append("planner/reviewer handoff requires Recommended capability capable")
    if handoff.metadata.get("Contract depth") == "high-risk" and capability != "capable":
        errors.append("high-risk handoff requires Recommended capability capable")
    review_mode = handoff.metadata.get("Review mode", "")
    if review_mode not in VALID_REVIEW_MODES:
        errors.append(f"invalid review mode: {review_mode or 'missing'}")
    elif state == "EXECUTION_TO_REVIEW":
        if review_mode == "none":
            errors.append("EXECUTION_TO_REVIEW requires Review mode inline, bugbot, or security")
    elif review_mode != "none":
        errors.append(f"state {state or 'missing'} requires Review mode none")

    requested_response = handoff.sections.get("Requested response from the next role", "")
    specialized_command = {
        "bugbot": "/review-bugbot",
        "security": "/review-security",
    }.get(review_mode)
    if re.search(r"/review(?![-\w])", requested_response):
        errors.append(
            "generic /review is ambiguous; use Review mode inline or an exact "
            "/review-bugbot or /review-security command"
        )
    if specialized_command and specialized_command not in requested_response:
        errors.append(
            f"Review mode {review_mode} requires {specialized_command} in requested response"
        )
    if review_mode == "inline" and re.search(
        r"/review-(?:bugbot|security)", requested_response
    ):
        errors.append("Review mode inline conflicts with a specialized review request")
    working_tree = handoff.metadata.get("Working tree", "").lower()
    if working_tree not in {"clean", "dirty"}:
        errors.append("Working tree must be clean or dirty")
    base_head = handoff.metadata.get("Base HEAD", "")
    if base_head.lower() != "none" and not re.fullmatch(r"[0-9a-fA-F]{7,40}", base_head):
        errors.append("Base HEAD must be a 7–40 character hexadecimal commit hash")
    verified = handoff.metadata.get("Last verified", "")
    try:
        datetime.strptime(verified, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        errors.append("Last verified must use UTC format YYYY-MM-DDTHH:MM:SSZ")
    active_milestone = handoff.metadata.get("Active milestone", "")
    if active_milestone.lower() != "none":
        if "#" not in active_milestone:
            errors.append("Active milestone must be none or a relative path#exact heading")
        else:
            _validate_path_pointer(root, active_milestone, "Active milestone", errors)

    for heading in REQUIRED_SECTIONS:
        occurrences = len(
            re.findall(rf"^##\s+{re.escape(heading)}\s*$", handoff_text, re.MULTILINE)
        )
        if occurrences > 1:
            errors.append(f"duplicate handoff section: {heading}")
        content = handoff.sections.get(heading)
        if content is None:
            errors.append(f"handoff section missing: {heading}")
        elif _is_placeholder(content):
            errors.append(f"handoff section is empty or placeholder: {heading}")
        elif len(content) > MAX_BOOTSTRAP_SECTION_CHARACTERS:
            errors.append(
                f"handoff section exceeds {MAX_BOOTSTRAP_SECTION_CHARACTERS} "
                f"characters: {heading}; move detail to a referenced artifact"
            )

    context = handoff.sections.get("Context delta and evidence pointers", "")
    if context:
        _validate_context_pointers(root, context, errors)
    _validate_review_correction(handoff, errors)
    _validate_high_risk_contract(handoff, errors)

    for key in ("Date", "State", "Active milestone", "Current handoff"):
        if _is_placeholder(status.metadata.get(key, "")):
            errors.append(f"status metadata missing or placeholder: {key}")
    try:
        datetime.strptime(status.metadata.get("Date", ""), "%Y-%m-%d")
    except ValueError:
        errors.append("STATUS.md Date must use YYYY-MM-DD")
    if status.metadata.get("Current handoff") != "MODEL_HANDOFF.md":
        errors.append("STATUS.md Current handoff must be MODEL_HANDOFF.md")
    for heading in ("Completed", "Current constraints", "Next action"):
        occurrences = len(
            re.findall(rf"^##\s+{re.escape(heading)}\s*$", status_text, re.MULTILINE)
        )
        if occurrences != 1:
            errors.append(f"STATUS.md must contain exactly one section: {heading}")
        elif _is_placeholder(status.sections.get(heading, "")):
            errors.append(f"status section is empty or placeholder: {heading}")

    status_milestone = status.metadata.get("Active milestone", "")
    handoff_milestone = handoff.metadata.get("Active milestone", "")
    if status_milestone and _clean(status_milestone) != _clean(handoff_milestone):
        errors.append("STATUS.md and MODEL_HANDOFF.md disagree on Active milestone")

    status_next = _clean(status.sections.get("Next action", ""))
    handoff_next = _clean(handoff.sections.get("Exact next action", ""))
    if status_next and handoff_next and status_next != handoff_next:
        errors.append("STATUS.md Next action must exactly match handoff Exact next action")

    git = observed_git(root)
    if not git.get("available"):
        warnings.append("Git state unavailable; verify repository state manually")
    else:
        declared_branch = handoff.metadata.get("Base branch", "")
        declared_head = handoff.metadata.get("Base HEAD", "")
        declared_tree = handoff.metadata.get("Working tree", "").lower()
        if not _is_placeholder(declared_branch) and declared_branch != git["branch"]:
            errors.append(
                f"stale base branch: handoff={declared_branch}, observed={git['branch']}"
            )
        if not _is_placeholder(declared_head) and not git["head"].startswith(declared_head):
            errors.append(
                f"stale base HEAD: handoff={declared_head}, observed={git['head'][:12]}"
            )
        if declared_tree in {"clean", "dirty"} and declared_tree != git["working_tree"]:
            errors.append(
                f"working-tree mismatch: handoff={declared_tree}, "
                f"observed={git['working_tree']}"
            )

    return {
        "root": root,
        "errors": errors,
        "warnings": warnings,
        "handoff": handoff,
        "status": status,
        "git": git,
    }


def render_snapshot(result: dict[str, Any]) -> str:
    handoff: MarkdownRecord | None = result.get("handoff")
    status: MarkdownRecord | None = result.get("status")
    git = result.get("git", {"available": False})
    lines = [f"# Model handoff bootstrap · protocol {PROTOCOL_VERSION}"]
    if handoff:
        for key in REQUIRED_METADATA:
            lines.append(f"- {key}: {handoff.metadata.get(key, 'missing')}")
    if git.get("available"):
        lines.extend(
            (
                f"- Observed Git: {git['branch']} at {git['head'][:12]}",
                f"- Observed working tree: {git['working_tree']} "
                f"({git['changed_count']} changed paths)",
            )
        )
        lines.extend(f"  {item}" for item in git["changed_paths"])
    else:
        lines.append("- Observed Git: unavailable")
    lines.append("")
    if status:
        lines.append("## Status dashboard")
        for key, value in status.metadata.items():
            lines.append(f"- {key}: {value}")
        for heading in ("Completed", "Current constraints", "Next action"):
            content = status.sections.get(heading)
            if content:
                lines.extend((f"### {heading}", content))
    if handoff:
        headings = list(BOOTSTRAP_SECTIONS)
        if (
            handoff.metadata.get("To role") == "planner/reviewer"
            or handoff.metadata.get("State")
            in {"EXECUTION_TO_REVIEW", "BLOCKED_TO_DECIDE", "COMPLETE"}
        ):
            insertion = headings.index("Risks, deviations, and unknowns")
            headings[insertion:insertion] = REVIEW_BOOTSTRAP_SECTIONS
        for heading in headings:
            content = handoff.sections.get(heading, "")
            lines.append(f"## {heading}")
            if len(content) > MAX_BOOTSTRAP_SECTION_CHARACTERS:
                lines.append(
                    f"[omitted: {len(content)} characters exceeds the "
                    f"{MAX_BOOTSTRAP_SECTION_CHARACTERS}-character bootstrap limit]"
                )
            else:
                lines.append(content or "[missing]")
    if result["errors"] or result["warnings"]:
        lines.append("## Check result")
        lines.extend(f"- ERROR: {error}" for error in result["errors"])
        lines.extend(f"- WARNING: {warning}" for warning in result["warnings"])
    snapshot = "\n".join(lines).rstrip() + "\n"
    if len(snapshot) > MAX_BOOTSTRAP_CHARACTERS:
        snapshot = (
            f"# Model handoff bootstrap · protocol {PROTOCOL_VERSION}\n\n"
            f"ERROR: bootstrap would be {len(snapshot)} characters, above the "
            f"{MAX_BOOTSTRAP_CHARACTERS}-character limit. Compact MODEL_HANDOFF.md "
            "and STATUS.md; preserve detail in referenced artifacts.\n"
        )
    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "snapshot"))
    parser.add_argument("target", nargs="?", default=".", type=Path)
    args = parser.parse_args()
    result = inspect_project(args.target)
    if args.command == "snapshot":
        snapshot = render_snapshot(result)
        print(snapshot, end="")
    else:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")
        if not result["errors"]:
            print("model handoff check: PASS")
    oversized_snapshot = args.command == "snapshot" and "ERROR: bootstrap would be" in snapshot
    return 1 if result["errors"] or oversized_snapshot else 0


if __name__ == "__main__":
    raise SystemExit(main())
