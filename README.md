# Model Handoff Protocol

An evidence-first, bidirectional handoff protocol for switching between planning,
implementation, and review models without treating chat history as durable
project state.

The protocol is model-agnostic. A frontier model may plan and review while a
cost-efficient model implements bounded work, but roles—not model names—define
authority.

## Why this exists

Model switches, new conversations, and context compaction can lose unstated
rationale. This protocol makes the repository the operational memory:

- permanent rules define stable behavior;
- a live handoff packet records the exact current state;
- status and milestone plans define project truth;
- Git state and reproducible commands verify claims;
- every handoff names one exact next action and one requested response.
- incoming models start from a checked, bounded bootstrap and expand only exact
  context pointers, so project history does not grow every model switch.

## Workflow

```text
planner/reviewer defines a bounded contract
                  ↓
implementer verifies context and executes
                  ↓
implementer returns diff, evidence, and a precise question
                  ↓
planner/reviewer independently reviews
                  ↓
ACCEPT_STAGE | REFINE | BLOCKED_DECISION | COMPLETE
                  ↓
repeat when needed
```

The return direction is equally strict: after bounded execution, the implementer
records the diff base, owned versus pre-existing changes, command/exit/count
evidence, failures, deviations, risks, cleanup, and one named review decision.
The planner/reviewer independently inspects the referenced diff and evidence.

## Quick start

Preview installation into an existing project:

```bash
python3 scripts/install.py /path/to/project
```

Apply only missing files:

```bash
python3 scripts/install.py /path/to/project --apply
```

The installer never overwrites an existing file. It installs:

```text
.cursor/rules/model-handoff.mdc
.cursor/rules/project-execution.mdc
MODEL_HANDOFF.md
STATUS.md
docs/IMPLEMENTATION_PLAN.md
docs/MODEL_HANDOFF_PLAYBOOK.md
.model-handoff/handoff.py
.model-handoff/FEEDBACK.md
```

For existing destinations, preview reports `identical`, `differs`, or `conflict`
without changing them. Merge `differs` manually so project-specific rules and
live state are preserved during protocol upgrades.

You can also copy these files manually. Customize only project-specific paths,
approval boundaries, and the live handoff content; keep the bidirectional schema
stable.

## What the user says when switching

The shortest safe interaction is:

```text
Before: I am switching models. Complete and check the project handoff, then stop.
After: Continue from the project handoff.
```

The incoming model reads `To role` from the bootstrap. Role-specific prompts are
only needed when the user intentionally overrides the recorded route.

Before changing models:

```text
Prepare a compact, delta-first handoff using the project model-handoff rule.
Update owned records, point to exact evidence, run the handoff check, leave a
recoverable Git state, then stop.
```

The outgoing role finishes by checking the live packet:

```bash
python3 .model-handoff/handoff.py check .
```

The incoming role starts with a compact snapshot instead of preloading every
plan and report:

```bash
python3 .model-handoff/handoff.py snapshot .
```

After switching to an implementer:

```text
Act as implementer. Run the handoff snapshot, read only its exact required
context headings, verify the contract, then execute the exact next action.
```

After switching to a planner/reviewer:

```text
Act as planner/reviewer. Run the handoff snapshot, then inspect the named Git diff
and evidence independently. Return ACCEPT_STAGE, REFINE, BLOCKED_DECISION, or
COMPLETE, and write a bounded return handoff if work remains.
```

Copy-ready versions live in [`prompts/`](prompts/).

## Planning depth

The protocol does not require a powerful model to prescribe every code edit. It
should freeze outcomes, invariants, acceptance, authority, stop conditions, and
the first verifiable action. A bounded implementer may choose reversible local
mechanics protected by named tests. Add planning detail only as ambiguity, risk,
irreversibility, or evidence cost increases.

## Local improvement loop

The installed protocol is fully local and needs no recurring download. Log only
measurable switch friction in `.model-handoff/FEEDBACK.md`, outside bootstrap
context. After three completed switches or one severe failure, review open items,
change this local source repository with a regression test, and use installer
preview to merge `differs` safely into the working project.

## Core files

- [Model handoff rule](.cursor/rules/model-handoff.mdc)
- [Generic project execution rule](.cursor/rules/project-execution.mdc)
- [Detailed playbook](docs/MODEL_HANDOFF_PLAYBOOK.md)
- [Live handoff template](templates/MODEL_HANDOFF.md)
- [Live handoff checker and compact snapshot](scripts/handoff.py)
- [Examples](examples/)

Examples are intentionally abbreviated to teach decision shapes. Start a real
handoff from the complete template, not from an example.

## Safety and privacy

This repository contains templates only. Do not publish a real project's live
handoff without reviewing it for local paths, repository names, commit hashes,
internal decisions, credentials, issue links, logs, customer data, or other
private context.

The installer is local, dependency-free, dry-run-first, and does not modify
global model, editor, or agent settings.

## Validate

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Before publishing, add project-specific terms without storing them in this
repository:

```bash
MHP_FORBIDDEN_TERMS='private-project,account-name' python3 scripts/validate.py
```

## License

Apache License 2.0. See [LICENSE](LICENSE).
