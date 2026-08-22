# Security policy

This repository copies local text files into a user-selected project. The
installer is dry-run-first, refuses symlinked destination paths, and does not
overwrite existing files or change global configuration.

The installed handoff helper reads the six protocol files and invokes read-only
Git inspection commands. It does not modify files, launch network requests, read
credentials, or execute commands recorded inside a handoff packet.

The separate `.model-handoff/update.py` helper accesses the fixed upstream only
when explicitly invoked. For the current private repository, it uses the
machine's existing Git credentials, disables interactive credential prompts, and
never asks for a token in project text. It validates the requested Git ref,
fetches into a temporary directory without a shell, prints the resolved commit,
and delegates to the dry-run-first installer. It never changes an existing
destination file; `differs` and `conflict` require manual review.

Please report path traversal, overwrite, symlink, credential exposure, or unsafe
default issues privately through the repository's GitHub security reporting
channel. Do not include real credentials or private project handoffs in an issue.

Only the latest commit on the default branch is supported during the initial
private development phase.
