# Read an incoming handoff

This offline walkthrough stages the
[existing synthetic handoff fixture](../../tests/test_handoff.py) in a temporary
directory. It prints the receiving role, exact next action, evidence pointers
and check result. The fixture refers to a fictional module and milestone.

```mermaid
flowchart LR
  P[Planner or verifier] --> H[Handoff packet and project status]
  H --> S[Check and render snapshot]
  S --> I[Incoming implementer]
  I --> E[Diff and test evidence]
  E --> P
```

Run from the repository root with Python 3.11 or later:

```sh
python3 - <<'PY'
import runpy
import subprocess
import sys
import tempfile
from pathlib import Path

fixture = runpy.run_path("tests/test_handoff.py")
with tempfile.TemporaryDirectory() as directory:
    project = Path(directory)
    fixture["install"](project, apply=True)
    (project / "MODEL_HANDOFF.md").write_text(fixture["HANDOFF"], encoding="utf-8")
    (project / "STATUS.md").write_text(fixture["STATUS"], encoding="utf-8")
    (project / "docs/IMPLEMENTATION_PLAN.md").write_text(
        "# Implementation plan\n\n## M1\nFrozen acceptance.\n", encoding="utf-8"
    )
    subprocess.run([sys.executable, "scripts/handoff.py", "snapshot", directory], check=True)
PY
```

Selected lines from the observed output:

```text
- State: PLAN_TO_EXECUTE
- To role: implementer
...
## Exact next action
Inspect `src/service.py` and identify the smallest edit region.
...
## Check result
- WARNING: Git state unavailable; verify repository state manually
```

The warning is expected because the temporary fixture is not a Git checkout.
On a real project, verify the observed Git state and cited test evidence before
acting. The snapshot checks the packet's consistency. Its sample test results
describe the fictional project and do not execute that project's tests.

The walkthrough was run against source revision `10d1b13`. For an actual
project, start with the [dry-run installation procedure](../REMOTE_INSTALL.md).
