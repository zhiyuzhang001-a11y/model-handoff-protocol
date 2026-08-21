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
