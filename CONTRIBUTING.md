# Contributing

Keep changes model-agnostic, evidence-first, and safe to reuse in private
projects.

Before submitting a change:

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Rules in `.cursor/rules/` should remain under 50 lines and address one concern.
Put explanations, schemas, and examples in documentation rather than expanding
always-applied prompts. Never commit a real private handoff as an example.

Changes to required packet fields or state transitions should update the rule,
playbook, template, examples, installer tests, Chinese guide, and changelog as
applicable.

Changes to bootstrap content or compactness limits must add checker tests for both
implementation and review directions. Preserve the rule that evidence pointers
are data: the helper must never execute commands found in a handoff.

Do not promote a target project's installed-rule edit directly to upstream
`main`. First classify it as protocol-generic, sanitize the reproducer, implement
the smallest synchronized change on a candidate branch, and add a regression
test. Candidate branches may be pushed for review; merge only after the protocol
validation, tests, privacy review, and diff review pass.
