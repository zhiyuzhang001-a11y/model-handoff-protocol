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

The installed `.model-handoff/handoff.py` helper checks the live contract and
renders a bounded bootstrap snapshot. It does not decide what to do; it prevents
the incoming role from starting with stale or unnecessarily broad context.

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

## Capability-aware routing

The default distribution is asymmetric by design:

- economical models implement most bounded, reversible, test-protected units;
- capable models plan milestones, resolve material ambiguity, independently
  review results, and implement the smaller set of judgment-heavy, difficult, or
  high-risk units where local mechanics require substantial reasoning.

This is a routing preference, not an authority grant. A capable model that writes
code assumes the implementer role and obeys the same scope, gates, and stop
conditions. An economical model that encounters an architectural choice, an
unfrozen invariant, or an unsafe assumption returns to planning/review instead of
guessing. For high-risk code written by a capable model, use a separate capable
review context or model when practical; self-review alone is not the independent
gate.

## Right-sized contracts

Do not maximize planning detail. A useful contract freezes the outcome,
invariants, acceptance evidence, authority boundary, stopping conditions, and
first verifiable action. It does not prescribe every edit when those choices are
local, reversible, and protected by named tests.

Use more planning when failure is costly, requirements are ambiguous, architecture
or public behavior may change, or evidence is expensive. Use a thinner contract
for routine, reversible work in known files. The implementer may choose local
mechanics inside the boundary and must return when a frozen assumption fails.

Over-specification creates stale micro-steps, longer handoffs, duplicated
reasoning, mechanical execution of bad assumptions, and a planner/reviewer
bottleneck. Under-specification forces the implementer to invent goals or gates.
Optimize for the smallest contract that makes unsafe guessing unnecessary.
Record `Contract depth` as `thin`, `standard`, or `high-risk` so the incoming
role knows whether detail is intentionally sparse or accidentally missing.

## Staged context loading

Incoming roles load context in three stages and stop as soon as the contract is
safe to execute or review:

1. **Bootstrap:** run `python3 .model-handoff/handoff.py snapshot .`. This yields
   status, live contract, observed Git state, open risks, and evidence pointers
   within a fixed character budget.
2. **Required expansion:** open only each exact `path#heading` under `Must read
   now`. Read the smallest region that establishes the frozen requirement.
3. **Conditional expansion:** open a `Read on demand` pointer only when its named
   trigger occurs, or when observed evidence materially conflicts with bootstrap.

Do not preload the full implementation plan, completed milestone history, full
reports, logs, or chat transcript. Detailed evidence remains in artifacts; the
handoff records the result, path, and reason it matters. If required context
cannot fit in the bootstrap budget, reduce duplication and add precise pointers
instead of raising the budget by default.

The helper enforces 9,000 characters for the live handoff, 3,000 for status,
1,200 per handoff section, and 7,000 for the rendered bootstrap. These are hard
character bounds rather than model-specific token estimates. Projects may fork
the limits only after measuring a real reconstruction failure that precise
pointers cannot solve.

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

`PLAN_TO_EXECUTE` and `REVIEW_TO_EXECUTE` target `implementer`. All other states
target `planner/reviewer`. The user can therefore use one generic incoming phrase;
the checked state determines the role instead of relying on model identity.
Only the planner/reviewer may originate plan/review-to-execute, `COMPLETE`, or
`IDLE`; only the implementer may originate `EXECUTION_TO_REVIEW`.

## Required handoff packet

Use `templates/MODEL_HANDOFF.md`. Every switch records:

- protocol version, stable ID, roles, recommended capability, explicit review mode, verified time,
  milestone, Git baseline, and working-tree ownership;
- one user-visible objective and explicit non-goals;
- exact acceptance commands, thresholds, artifacts, and cleanup;
- verified completed work that must not be repeated;
- remaining ordered work and one exact next action;
- files, diffs, commits, generated assets, and pre-existing changes;
- commands with exit status, counts, duration, and artifacts;
- failed attempts and whether they changed state;
- decisions, rejected alternatives, deviations, risks, and unknowns;
- allowed autonomy, stop conditions, live resources, and requested response.
- only the delta since the previous handoff, exact required/on-demand context
  headings, evidence artifact paths, and content that is safe to skip.

Write `none` when a field is inapplicable but omission would be ambiguous. Avoid
“mostly done”, “seems fine”, “tests pass”, and “continue working”.

`STATUS.md` owns the short project dashboard. `MODEL_HANDOFF.md` owns the transfer
contract. Their active-milestone value and exact-next-action text must match;
plans own durable scope and acceptance; reports own detailed evidence. Reference
owned facts instead of copying them across files.

## Planner/reviewer to implementer

1. Run the bootstrap snapshot and expand only its required context pointers.
2. Convert the desired outcome into one milestone or bounded stage.
3. Freeze the objective, non-goals, allowed changes, acceptance evidence, and
   stop conditions. Resolve only choices whose deferral would force unsafe
   guessing; leave reversible local mechanics to the implementer.
4. Split risky or independently verifiable units and identify the first action.
5. Record pre-existing changes and owned commands/processes.
6. Set state to `PLAN_TO_EXECUTE` or `REVIEW_TO_EXECUTE` and request a precise
   implementation result.

The contract is incomplete if the implementer must choose the architecture,
define success, infer whether external writes are allowed, or discover which
test suite is authoritative.

The contract is too detailed if it duplicates source code, full reports, or
step-by-step edits whose correctness can be decided locally and verified by the
named gates.

## Implementer acceptance

Before editing, the implementer verifies:

- objective and user-visible outcome;
- active milestone, exact next action, and ordered remaining work;
- allowed scope and non-goals;
- acceptance evidence and stop conditions;
- pre-existing versus task-owned changes;
- absence of material conflicts among plan, handoff, Git, and observed state.

Start from the bootstrap. Do not expand optional context merely to become
familiar with the whole project.

If a material conflict exists, record it and switch to `BLOCKED_TO_DECIDE`.

## Implementer execution

- Execute one verified unit at a time.
- Update plan, status, report, and handoff when a verified result changes the next
  action or later feasibility.
- Make reversible local implementation choices without requesting a new plan;
  record only decisions that affect later work or review.
- Do not rerun expensive completed evidence unless inputs changed or independent
  reproduction is required.
- Preserve unknown dirty-worktree changes; never manufacture a clean state with a
  broad reset.
- Keep one writer for overlapping files. Parallel work requires explicit,
  non-overlapping ownership.

## Root-cause corrections and bounded autonomy

Goals, public behavior, scope, acceptance gates, safety invariants, and stop
conditions remain planner/user authority. The implementer has local discretion
over reversible mechanics: it may refactor bounded code, replace a suggested
implementation technique, and add adjacent negative tests without asking again.
It may not weaken a gate, redefine success, or broaden the milestone.

When review returns a behavioral defect, the handoff must include four things:

1. the root invariant that the product must preserve;
2. a minimal reproducible counterexample and exact expected result;
3. at least one adjacent adversarial variant likely to defeat a case-specific fix;
4. a known shallow or rejected approach when one has already failed.

For a non-behavioral correction such as wording, formatting, or missing evidence,
the handoff still names the violated requirement but may record correction
variants as `not applicable` with a short reason. Do not invent adversarial cases
that add no verification value.

The implementer first converts the behavioral reproducer and adjacent variant
into failing tests, then chooses the smallest mechanism that satisfies the
invariant. For an ordinary correction, one meaningful adjacent variant is the
minimum. For path, identity, concurrency, snapshot/cache, state-publication,
recovery, security, or similarly high-risk work, the contract and tests cover
every applicable dimension in this matrix:

- input value and object/file identity;
- path, ancestry, alias, and replacement identity;
- ordering and the boundary between observation and publication;
- before, during, and after replacement or invalidation;
- failure and interruption points.

Record why a dimension is inapplicable rather than silently omitting it. Exercise
timing with deterministic hooks or barriers, not sleeps, timestamp luck, or one
observed interleaving. For state publication, only inputs actually observed and
included by the same successful generation may be marked fresh; a modification
after observation remains dirty.

If the same invariant fails a second time after a correction, stop serial
case-specific patching. Set `Contract depth` to `high-risk` and return to the
planner/reviewer to rebuild the coverage matrix before more edits. The code change
may still be small, but acceptance must prove the class-wide invariant.

If the suggested mechanism cannot satisfy the invariant, choose a safer in-scope
method; escalate only when that requires a public, architectural, or scope
decision. Local discretion remains inside the handoff's allowed paths and
actions. A new dependency, public interface or schema change, migration, external
write, or edit outside that boundary requires explicit authority even when it
appears to be the cleanest implementation.

A correction is not reviewable merely because the named reproducer passes. It
must pass the adjacent variants, prior regression suite, required real workflow,
and evidence/cleanup gates. Record which root invariant was proven and which
variant dimensions were exercised.

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

For `EXECUTION_TO_REVIEW`, the bootstrap automatically adds changes/repository
state, commands/results, and decisions/rationale. The reviewer receives the
review index and measured results, not full logs; it then opens the named diff and
evidence artifacts independently.

### Milestone review versus specialized review

Every packet carries `Review mode: inline | bugbot | security | none`. For
`EXECUTION_TO_REVIEW`, `inline` means the current planner/reviewer performs the
milestone review directly from the checked packet, diff, gates, and evidence,
then returns `ACCEPT_STAGE`, `REFINE`, `BLOCKED_DECISION`, or `COMPLETE`. Other
states require `none`.

`bugbot` and `security` are optional specialized modes. They require the matching
`/review-bugbot` or `/review-security` command in `Requested response from the
next role`. The checker rejects missing, invalid, or state-conflicting modes and
rejects an `inline` packet that also requests a specialized command. The incoming
role therefore follows a single checked route and never asks the user to choose.
After a specialized result returns, the planner/reviewer still makes the protocol
decision unless the frozen contract explicitly says otherwise.

Never put generic `/review` in a handoff packet: that command intentionally opens
a specialized-review selector. The checker rejects it in every mode.

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

For behavioral `REFINE`, avoid prescribing only a line edit. State the violated
invariant, reproducer, adjacent variant, rejected shallow fix, and the freedom the
implementer retains to select a stronger bounded mechanism. For non-behavioral
`REFINE`, name the exact unmet requirement and evidence needed without forcing
irrelevant adversarial variants.

## Switching discipline

- Switch at a verified boundary, not halfway through an edit or destructive step.
- Before switching, wait for or terminate owned commands, record terminal/session
  IDs and external run URLs, and list processes the next role must monitor.
- Run `python3 .model-handoff/handoff.py check .`; do not switch with a stale Git
  baseline, mismatched next action, missing section, or oversized packet.
- Never leave an unrecorded approval prompt or interactive command waiting.
- If context is compacted, repeat the incoming acceptance procedure.
- If a new conversation starts, use the full incoming prompt from `prompts/`.
- If the same conversation changes model, the short prompt is sufficient only
  when the outgoing packet was validated.

## User procedure

1. Tell the outgoing model: `我要切换模型。请按项目规则完成并检查交接，然后停止。`
2. Wait until the helper check passes and it reports a recoverable state.
3. Change to the reported `Recommended capability`: normally `economical` for
   bounded implementation and `capable` for planning/review or difficult work.
4. Tell the incoming model: `请按项目交接继续。` It reads `To role` from the
   bootstrap. Use a role-specific prompt only to override the recorded route.
5. Require the incoming role to begin from the bounded snapshot and report a
   conflict before editing if records do not agree.

Avoid replacing the incoming phrase with a bare `review` or `审核`. Those words can
route to an optional review skill instead of the protocol milestone decision.

## Privacy before publishing a real packet

Review live handoffs for:

- absolute home/workspace paths and usernames;
- private repository, branch, issue, customer, or service names;
- commit hashes and unreleased architecture decisions;
- command output, logs, URLs, tokens, credentials, and environment variables;
- temporary directories, hostnames, process IDs, and account identifiers.

Publish templates and invented examples, not an unreviewed live handoff.

## Local continuous improvement

No download, background updater, or network service is required after
installation. The installed rules, templates, helper, and feedback log are local.

Do not record every successful switch. When a switch produces measurable
friction—missing required context, repeated work, a stale or broken pointer, wrong
role routing, an oversized packet, or an unverifiable claim—append one compact
entry to `.model-handoff/FEEDBACK.md`. That file is never bootstrap context.

Do not silently generalize a target-project workaround. Classify it first:

- **Project-specific:** it depends on that repository's paths, tooling, risk
  boundary, product behavior, or approval policy. Keep it in that project.
- **Protocol-generic:** the same failure could affect unrelated installed
  projects. Treat it as a candidate change to the reusable protocol source.
- **Unclear:** keep recording evidence; do not change the shared protocol yet.

After three completed switches, or immediately after one severe failure, use this
promotion workflow for a protocol-generic candidate:

1. Finish or safely stop the active project task; do not mutate stable shared
   rules halfway through execution.
2. Preserve the reproducer and observed impact in the target project's private
   `.model-handoff/FEEDBACK.md`. Do not copy private paths, commits, logs, URLs,
   customer data, or unreleased design details into the public protocol source.
3. Never push an unreviewed target-project rule change directly to upstream `main`.
   In an up-to-date clone of the protocol source, create a candidate branch.
4. Re-express the problem generically, make the smallest synchronized change to
   rules, templates, checker, prompts, and documentation that actually need it,
   and add a regression test that fails without the correction.
5. Run protocol validation and all tests. Push the candidate branch if remote
   backup or review is useful; review the diff and evidence before merging `main`.
6. Pull the accepted source revision locally, run the installer in dry-run mode
   against the originating project, and manually merge only relevant `differs`.
   Never auto-overwrite project-specific rules or live state.
7. Mark feedback `RESOLVED` only after a later real switch proves the correction;
   otherwise keep it `OPEN` or mark the proposal `REJECTED` with the reason.

GitHub is the shared source and review history, not a runtime dependency. Installed
projects continue locally. A maintained local clone normally updates with
`git pull`; downloading a new archive for every task is unnecessary.

### Upgrade from protocol 0.3 or earlier

Update the installed rule, playbook, template, and `.model-handoff/handoff.py`
together. Then update the live `MODEL_HANDOFF.md` to protocol `0.4` and add
`Recommended capability`: use `capable` whenever `To role` is
`planner/reviewer`; for `implementer`, choose `economical` for most bounded work
or `capable` for judgment-heavy work. Every `high-risk` contract requires
`capable` and an explicit coverage matrix or reasoned inapplicability record.
Protocol 0.2 packets must also add
`Review mode`: use `inline` for ordinary `EXECUTION_TO_REVIEW` and `none` for
non-review states. Run the new checker before the next switch. A partial upgrade
intentionally fails rather than guessing a route.

## Reuse in another project

Run the installer or copy the two rules, helper, playbook, and blank templates. Customize
only canonical plan/status/report paths and the project's approval boundaries.
Keep the handoff state machine, required fields, source-of-truth order, and
bidirectional review loop stable.
