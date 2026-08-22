#!/usr/bin/env python3
"""Fetch a pinned protocol revision and run its dry-run-first installer."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


REPOSITORY_URL = "https://github.com/zhiyuzhang001-a11y/model-handoff-protocol.git"
DEFAULT_REF = "main"
REF_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]{0,127}")


def validate_ref(ref: str) -> str:
    if (
        not REF_PATTERN.fullmatch(ref)
        or ".." in ref
        or "//" in ref
        or ref.endswith(("/", "."))
    ):
        raise ValueError(f"unsafe Git ref: {ref}")
    return ref


def _run_git(*args: str, cwd: Path | None = None) -> str:
    environment = os.environ.copy()
    environment["GIT_TERMINAL_PROMPT"] = "0"
    process = subprocess.run(
        ("git", *args),
        cwd=cwd,
        check=True,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=60,
    )
    return process.stdout.strip()


def _fetch_source(destination: Path, ref: str) -> str:
    _run_git("init", "--quiet", str(destination))
    _run_git("remote", "add", "origin", REPOSITORY_URL, cwd=destination)
    _run_git("fetch", "--quiet", "--depth=1", "--no-tags", "origin", ref, cwd=destination)
    _run_git("checkout", "--quiet", "--detach", "FETCH_HEAD", cwd=destination)
    return _run_git("rev-parse", "HEAD", cwd=destination)


def bootstrap(
    target: Path,
    *,
    ref: str = DEFAULT_REF,
    apply: bool = False,
    json_output: bool = False,
) -> tuple[int, str]:
    target = target.resolve(strict=True)
    if not target.is_dir():
        raise ValueError(f"target is not a directory: {target}")
    ref = validate_ref(ref)

    with tempfile.TemporaryDirectory(prefix="model-handoff-bootstrap-") as directory:
        source = Path(directory) / "source"
        revision = _fetch_source(source, ref)
        installer = source / "scripts/install.py"
        if not installer.is_file():
            raise ValueError("fetched revision does not contain scripts/install.py")
        command = [sys.executable, str(installer), str(target)]
        if apply:
            command.append("--apply")
        if json_output:
            command.append("--json")
        print(
            f"model handoff source: {REPOSITORY_URL}@{revision}",
            file=sys.stderr,
        )
        result = subprocess.run(command, check=False)
    return result.returncode, revision


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default=".", type=Path)
    parser.add_argument("--ref", default=DEFAULT_REF, help="branch, tag, or commit")
    parser.add_argument("--apply", action="store_true", help="create missing files")
    parser.add_argument("--json", action="store_true", help="pass JSON output through")
    args = parser.parse_args()
    try:
        return bootstrap(
            args.target,
            ref=args.ref,
            apply=args.apply,
            json_output=args.json,
        )[0]
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
