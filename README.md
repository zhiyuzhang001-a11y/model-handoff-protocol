# Model Handoff Protocol

An evidence-first, bidirectional handoff protocol for switching between planning,
implementation, and verification models without treating chat history as durable
project state.

The protocol is model-agnostic. By default, a cost-efficient model performs most
bounded implementation, while a capable model plans, reviews at the required
independence level, and also implements the smaller set of difficult or high-risk
units. Roles—not model names—still define authority.

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
planner/verifier defines a bounded contract
                  ↓
implementer verifies context and executes
                  ↓
implementer returns diff, evidence, and a precise question
                  ↓
planner/verifier verifies at the required independence level
                  ↓
ACCEPT_STAGE | REFINE | BLOCKED_DECISION | COMPLETE
                  ↓
repeat when needed
```

The return direction is equally strict: after bounded execution, the implementer
records the diff base, owned versus pre-existing changes, command/exit/count
evidence, failures, deviations, risks, cleanup, and one named verification decision.
The planner/verifier inspects the referenced diff and evidence; independence is
risk-based rather than automatic.

## Quick start

In a new project, the simplest request is:

```text
Install or update model-handoff-protocol from
https://github.com/zhiyuzhang001-a11y/model-handoff-protocol as this project's
rules, following the repository's safe installation and upgrade procedure.
```

A capable project model can perform the safe preview, installation, and any
manual merge from that instruction when it has repository access. See the
copy-ready Chinese version and public bootstrap procedure in
[Remote installation and updates](docs/REMOTE_INSTALL.md).
The longer safety-explicit prompt there says: `Preview first; never overwrite differs/conflict`
or project live state.

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
.model-handoff/update.py
.model-handoff/FEEDBACK.md
.model-handoff/recover-review-selector.txt
.model-handoff/CONTROL.md
```

For existing destinations, preview reports `identical`, `differs`, or `conflict`
without changing them. Merge `differs` manually so project-specific rules and
live state are preserved during protocol upgrades.

After the first installation, preview the current GitHub `main`
without another manual clone:

```bash
python3 .model-handoff/update.py .
```

The updater runs only when explicitly invoked, prints the fetched commit, and
uses the same no-overwrite installer. Pin a release or commit with `--ref` when
reproducibility matters.

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

The contract is optional at runtime and does not need to be uninstalled. To
pause it while keeping every file, say:

```text
Exit the model-handoff protocol and retain its files.
```

To resume later, say:

```text
Resume the model-handoff protocol.
```

These commands change `.model-handoff/CONTROL.md` between `active` and `paused`.
While paused, ordinary work ignores the handoff contract and snapshot stays
minimal. Resume revalidates live state before continuing.

If an unexpected Bugbot/Security selector still appears, do not choose either
option. Send one routing-correction sentence:

```text
Do not select a reviewer. Exit generic /review, read the project handoff snapshot,
and continue according to Verification mode.
```

The model must preserve the contract and resume the recorded route. If an
`EXECUTION_TO_VERIFY` packet has a missing or invalid mode, the deterministic safe
fallback is `independent`; a specialized gate is never inferred.

Each packet declares `Verification mode: self | independent | bugbot | security | none`.
Every stage is verified, but a model switch is not always required. Eligible
capable-model thin/standard work uses `self` in the same context; economical
output, high-risk work, material deviations, and explicit independent gates use
`independent` in a separate capable context. Specialized gates use their exact
mode and command. The checker rejects missing or conflicting routes, so the
incoming model never asks the user to choose Bugbot or Security Review. Protocol
verification is deliberately named differently from the optional generic
`/review` skill, which opens that selector.

Each packet also declares `Recommended capability: economical | capable`, so the
outgoing model tells the user which tier to select. A planner/verifier handoff
must recommend `capable`; an implementer handoff selects `economical` for most
bounded work and `capable` for judgment-heavy work. The checker requires
`capable` plus an explicit coverage matrix for every `high-risk` contract.

When upgrading from protocol 0.5 or earlier, merge the installed rule, playbook,
template, and checker together. Then set the live packet to protocol 0.6. Rename
`planner/reviewer` to `planner/verifier`, `Review mode` to `Verification mode`,
`inline` to `independent`, and the execution/rework states to
`EXECUTION_TO_VERIFY`/`VERIFY_TO_EXECUTE`. The checker rejects partial upgrades
instead of guessing a route.

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

For a same-context capable verification when the checked mode is `self`:

```text
Do not switch models. Change role to planner/verifier and perform the recorded
lightweight conformance check. Return one protocol decision.
```

After switching to a separate planner/verifier for `independent`:

```text
Act as planner/verifier. Run the handoff snapshot, then inspect the named Git diff
and evidence independently. Return ACCEPT_STAGE, REFINE, BLOCKED_DECISION, or
COMPLETE, and write a bounded return handoff if work remains.
```

Copy-ready versions live in [`prompts/`](prompts/).

## Planning depth

The default is to give economical models most simple, bounded, reversible, and
test-protected work. Capable models freeze outcomes, invariants, acceptance,
authority, stop conditions, and the first verifiable action; verify the result at
the required independence level; and implement judgment-heavy or high-risk code
when that is the safer allocation. Any model writing code assumes the implementer
role. Capable-model thin/standard work may receive same-context `self` verification
when all gates pass and no boundary changed. High-risk work always receives a
separate capable verification.

For high-risk behavioral corrections, cover every applicable value, identity,
path, ordering, observation/publication, replacement, failure, and interruption
dimension with deterministic tests. A second post-fix failure of the same
invariant returns to high-risk planning instead of triggering another narrow
patch.

## Local improvement loop

The installed protocol is fully local and needs no recurring download. Log only
measurable switch friction in `.model-handoff/FEEDBACK.md`, outside bootstrap
context. Keep repository-specific workarounds in their project. Promote only a
failure that can affect unrelated projects: reproduce it generically on a protocol
source branch, sanitize evidence, add a regression test, validate, and review the
candidate before merging `main`. A candidate branch may be pushed for backup or
review; never push an unreviewed target-project rule directly to upstream `main`.
After acceptance, preview the installer against the originating project and merge
only relevant `differs`. Resolve feedback only after a later live switch proves it.

## Core files

- [Model handoff rule](.cursor/rules/model-handoff.mdc)
- [Generic project execution rule](.cursor/rules/project-execution.mdc)
- [Detailed playbook](docs/MODEL_HANDOFF_PLAYBOOK.md)
- [Live handoff template](templates/MODEL_HANDOFF.md)
- [Live handoff checker and compact snapshot](scripts/handoff.py)
- [Remote bootstrap and installed update helper](scripts/bootstrap.py)
- [Remote installation and update procedure](docs/REMOTE_INSTALL.md)
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
