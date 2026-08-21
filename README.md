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
```

You can also copy these files manually. Customize only project-specific paths,
approval boundaries, and the live handoff content; keep the bidirectional schema
stable.

## What the user says when switching

Before changing models:

```text
Prepare a complete handoff using the project model-handoff rule. Update the live
handoff, status, active plan, and report as needed. Finish or record owned commands
and processes, leave a recoverable Git state, then stop.
```

After switching to an implementer:

```text
Act as implementer. Read the project rules, MODEL_HANDOFF.md, STATUS.md,
IMPLEMENTATION_PLAN.md, the active milestone, latest report, and Git state.
Verify the contract before editing, then execute only the exact next action.
```

After switching to a planner/reviewer:

```text
Act as planner/reviewer. Read the project rules and handoff, inspect Git, diff,
and evidence independently, then return ACCEPT_STAGE, REFINE,
BLOCKED_DECISION, or COMPLETE. Write a bounded return handoff if work remains.
```

Copy-ready versions live in [`prompts/`](prompts/).

## Core files

- [Model handoff rule](.cursor/rules/model-handoff.mdc)
- [Generic project execution rule](.cursor/rules/project-execution.mdc)
- [Detailed playbook](docs/MODEL_HANDOFF_PLAYBOOK.md)
- [Live handoff template](templates/MODEL_HANDOFF.md)
- [Examples](examples/)

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
