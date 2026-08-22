#!/usr/bin/env python3
"""Dry-run-first installer for the model handoff protocol."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INSTALLS = (
    (Path(".cursor/rules/model-handoff.mdc"), Path(".cursor/rules/model-handoff.mdc")),
    (Path(".cursor/rules/project-execution.mdc"), Path(".cursor/rules/project-execution.mdc")),
    (Path("templates/MODEL_HANDOFF.md"), Path("MODEL_HANDOFF.md")),
    (Path("templates/STATUS.md"), Path("STATUS.md")),
    (Path("templates/IMPLEMENTATION_PLAN.md"), Path("docs/IMPLEMENTATION_PLAN.md")),
    (Path("docs/MODEL_HANDOFF_PLAYBOOK.md"), Path("docs/MODEL_HANDOFF_PLAYBOOK.md")),
    (Path("scripts/handoff.py"), Path(".model-handoff/handoff.py")),
    (Path("templates/HANDOFF_FEEDBACK.md"), Path(".model-handoff/FEEDBACK.md")),
)


def _validate_target(target: Path) -> Path:
    if not target.exists():
        raise ValueError(f"target does not exist: {target}")
    if not target.is_dir():
        raise ValueError(f"target is not a directory: {target}")
    return target.resolve(strict=True)


def _validate_destination(base: Path, relative: Path) -> None:
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"unsafe destination: {relative}")
    current = base
    for part in relative.parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"destination parent is a symlink: {current}")
        if current.exists() and not current.is_dir():
            raise ValueError(f"destination parent is not a directory: {current}")
    destination = base / relative
    if destination.is_symlink():
        raise ValueError(f"destination is a symlink: {destination}")


def _ensure_parent(base: Path, relative: Path) -> None:
    current = base
    for part in relative.parts[:-1]:
        current = current / part
        if not current.exists():
            current.mkdir(mode=0o755)


def install(target: Path, *, apply: bool = False) -> dict[str, Any]:
    base = _validate_target(target)
    for source_relative, destination_relative in INSTALLS:
        source = ROOT / source_relative
        if not source.is_file():
            raise ValueError(f"installer source is missing: {source_relative}")
        _validate_destination(base, destination_relative)

    entries: list[dict[str, str]] = []
    for source_relative, destination_relative in INSTALLS:
        source = ROOT / source_relative
        destination = base / destination_relative
        if destination.exists():
            if not destination.is_file():
                status = "conflict"
            elif destination.read_bytes() == source.read_bytes():
                status = "identical"
            else:
                status = "differs"
            entries.append({"path": destination_relative.as_posix(), "status": status})
            continue
        if not apply:
            entries.append({"path": destination_relative.as_posix(), "status": "would_create"})
            continue

        _ensure_parent(base, destination_relative)
        data = source.read_bytes()
        descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
        entries.append({"path": destination_relative.as_posix(), "status": "created"})

    return {
        "mode": "apply" if apply else "dry-run",
        "target": str(base),
        "entries": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="existing project directory")
    parser.add_argument("--apply", action="store_true", help="create missing files")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()

    try:
        result = install(args.target, apply=args.apply)
    except ValueError as error:
        parser.error(str(error))

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"model handoff install: {result['mode']} ({result['target']})")
        for entry in result["entries"]:
            print(f"{entry['status']:>12}  {entry['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
