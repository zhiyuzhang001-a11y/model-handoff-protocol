# Model handoff playbook

## Purpose

This protocol preserves project intent and evidence when responsibility moves in
either direction between a planning/review role and an implementation role,
across context compaction, or into a new conversation. Chat history is useful,
but repository records, Git state, and reproducible evidence are the operational
source of truth.

The permanent rules are:

- `.cursor/rules/project-execution.mdc`
- `.cursor/rules/model-handoff.mdc`

`MODEL_HANDOFF.md` is the live, replaceable packet. `STATUS.md` records current
project state. `docs/IMPLEMENTATION_PLAN.md` records durable objectives and
milestones. Keep changing task state out of permanent rules.

## Roles

### Planner/reviewer

Use this role for unclear goals, milestone contracts, architecture, tradeoffs,
frozen acceptance criteria, major deviations, release decisions, and independent
review. Its job is to reduce ambiguity into a bounded execution contract.

### Implementer

Use this role when files or discovery limits, ordered work, acceptance evidence,
and stopping conditions are known. It can make normal in-scope local changes and
run non-destructive validation. It cannot redefine the objective, weaken a gate,
or silently select a materially different architecture.

Model names are routing hints, not authority. Any model can discover an issue
outside its current role and hand it back instead of guessing.

## Source-of-truth order

When records disagree, use this order and stop on a material unresolved conflict:

1. platform safety/permission boundaries and the latest explicit user instruction;
2. the active milestone's scope, acceptance, and stop conditions;
3. observed Git/filesystem state and reproducible command evidence;
4. `STATUS.md` and the latest verified report;
5. `MODEL_HANDOFF.md`;
6. conversation summaries or remembered rationale.

The handoff packet cannot override a milestone. It must surface discrepancies.

## Handoff states

- `PLAN_TO_EXECUTE`: a new bounded contract is ready for implementation.
- `EXECUTION_TO_REVIEW`: implementation evidence is ready for review.
- `REVIEW_TO_EXECUTE`: review found bounded follow-up work.
- `BLOCKED_TO_DECIDE`: continuing requires architecture, scope, approval, or user
  judgment.
- `COMPLETE`: all milestone code, evidence, records, cleanup, and release work are
  complete.
- `IDLE`: no milestone is authorized; the packet states how work may resume.

## Required handoff packet

Use `templates/MODEL_HANDOFF.md`. Every switch records:

- stable ID, state, roles, milestone, branch/commit, and working-tree ownership;
- one user-visible objective and explicit non-goals;
- exact acceptance commands, thresholds, artifacts, and cleanup;
- verified completed work that must not be repeated;
- remaining ordered work and one exact next action;
- files, diffs, commits, generated assets, and pre-existing changes;
- commands with exit status, counts, duration, and artifacts;
- failed attempts and whether they changed state;
- decisions, rejected alternatives, deviations, risks, and unknowns;
- allowed autonomy, stop conditions, live resources, and requested response.

Write `none` when a field is inapplicable but omission would be ambiguous. Avoid
“mostly done”, “seems fine”, “tests pass”, and “continue working”.

## Planner/reviewer to implementer

1. Read rules, status, plan, current handoff, latest report, and Git state.
2. Convert the desired outcome into one milestone or bounded stage.
3. Freeze the objective, non-goals, allowed changes, acceptance evidence, and
   stop conditions. Resolve choices that would otherwise force guessing.
4. Split work into independently verifiable units and identify the first action.
5. Record pre-existing changes and owned commands/processes.
6. Set state to `PLAN_TO_EXECUTE` or `REVIEW_TO_EXECUTE` and request a precise
   implementation result.

The contract is incomplete if the implementer must choose the architecture,
define success, infer whether external writes are allowed, or discover which
test suite is authoritative.

## Implementer acceptance

Before editing, the implementer verifies:

- objective and user-visible outcome;
- active milestone, exact next action, and ordered remaining work;
- allowed scope and non-goals;
- acceptance evidence and stop conditions;
- pre-existing versus task-owned changes;
- absence of material conflicts among plan, handoff, Git, and observed state.

If a material conflict exists, record it and switch to `BLOCKED_TO_DECIDE`.

## Implementer execution

- Execute one verified unit at a time.
- Update plan, status, report, and handoff when a verified result changes the next
  action or later feasibility.
- Do not rerun expensive completed evidence unless inputs changed or independent
  reproduction is required.
- Preserve unknown dirty-worktree changes; never manufacture a clean state with a
  broad reset.
- Keep one writer for overlapping files. Parallel work requires explicit,
  non-overlapping ownership.

## Implementer to planner/reviewer

Use `EXECUTION_TO_REVIEW` when evidence is reviewable, or `BLOCKED_TO_DECIDE` when
continuing requires judgment outside the contract. Include:

- exact diff/commit and separation of task-owned and pre-existing changes;
- every gate with command, exit status, count, duration, and artifact;
- failures and whether they altered state;
- deviations and downstream effects;
- cleanup, process, repository, external-run, and temporary-state status;
- one requested decision: for example `ACCEPT_STAGE`, `REFINE_X`,
  `CHOOSE_A_OR_B`, or `APPROVE_RELEASE`.

Do not ask another model to “take a look” without naming the decision.

## Planner/reviewer decision

The reviewer inspects the relevant diff and material evidence rather than
trusting the packet. It chooses one outcome:

- `ACCEPT_STAGE`: gates pass; record acceptance and define the next bounded stage;
- `REFINE`: return a concrete defect list, acceptance delta, and first action;
- `BLOCKED_DECISION`: present the material choice with evidence;
- `COMPLETE`: all implementation, evidence, records, cleanup, and release gates
  pass.

If work returns to implementation, use `REVIEW_TO_EXECUTE`. For completion, leave
the packet `COMPLETE` or `IDLE` and name the exact resumption condition.

## Switching discipline

- Switch at a verified boundary, not halfway through an edit or destructive step.
- Before switching, wait for or terminate owned commands, record terminal/session
  IDs and external run URLs, and list processes the next role must monitor.
- Never leave an unrecorded approval prompt or interactive command waiting.
- If context is compacted, repeat the incoming acceptance procedure.
- If a new conversation starts, use the full incoming prompt from `prompts/`.
- If the same conversation changes model, the short prompt is sufficient only
  when the outgoing packet was validated.

## User procedure

1. Tell the outgoing model to prepare the packet with
   `prompts/outgoing-handoff.txt`.
2. Wait until it reports a recoverable state and stops.
3. Change the model.
4. Paste `prompts/incoming-implementer.txt` or
   `prompts/incoming-reviewer.txt`.
5. Require the incoming role to report a conflict before editing if records do
   not agree.

## Privacy before publishing a real packet

Review live handoffs for:

- absolute home/workspace paths and usernames;
- private repository, branch, issue, customer, or service names;
- commit hashes and unreleased architecture decisions;
- command output, logs, URLs, tokens, credentials, and environment variables;
- temporary directories, hostnames, process IDs, and account identifiers.

Publish templates and invented examples, not an unreviewed live handoff.

## Reuse in another project

Run the installer or copy the two rules, playbook, and blank templates. Customize
only canonical plan/status/report paths and the project's approval boundaries.
Keep the handoff state machine, required fields, source-of-truth order, and
bidirectional review loop stable.
