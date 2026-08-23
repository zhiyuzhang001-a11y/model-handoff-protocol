# Current model handoff

- Protocol version: `0.6`
- Handoff ID: `<date-or-sequence>-<short-purpose>`
- State: `PLAN_TO_EXECUTE | EXECUTION_TO_VERIFY | VERIFY_TO_EXECUTE | BLOCKED_TO_DECIDE | COMPLETE | IDLE`
- From role: `planner/verifier | implementer`
- To role: `planner/verifier | implementer`
- Recommended capability: `economical | capable`
- Verification mode: `self | independent | bugbot | security | none`
- Contract depth: `thin | standard | high-risk`
- Last verified: `<YYYY-MM-DDTHH:MM:SSZ>`
- Active milestone: `<relative path#exact heading, or none>`
- Base branch: `<branch name or detached>`
- Base HEAD: `<full or unambiguous short commit hash>`
- Working tree: `<clean | dirty>`

## Objective and user-visible outcome

`<One concrete outcome, not an activity such as “continue working”.>`

## Frozen scope and non-goals

- Allowed: `<repositories, files, actions, and decisions>`
- Deferred or forbidden: `<explicit non-goals>`

## Acceptance and required evidence

- `<Exact test, dataset, threshold, artifact, cleanup, or documentation gate>`
- Root invariant: `<required for VERIFY_TO_EXECUTE; otherwise invariant or none>`
- Correction variants: `<behavioral reproducer plus adjacent case; for a non-behavioral correction, not applicable with reason; otherwise none>`
- High-risk coverage matrix: `<all applicable dimensions, omitted reasons, and deterministic hook/barrier; or not applicable>`

## Verified completed work

- `<Completed change and its evidence; the next role must not repeat it>`

## Remaining ordered work

1. `<bounded step>`
2. `<bounded step>`

## Exact next action

`<Exact text copied to STATUS.md Next action. One command, inspection, edit, or decision.>`

## Context delta and evidence pointers

- Changed since previous handoff: `<only new facts and decisions>`
- Must read now: `<relative path#exact heading and why, or none>`
- Read on demand: `<path#heading and triggering condition, or none>`
- Evidence artifacts: `<paths, test reports, or commits; do not paste full output>`
- Safe to skip: `<completed history or unrelated areas>`

## Changes and repository state

- Diff base: `<commit or comparison point>`
- Task-owned changes: `<files, commits, diffs, and generated assets>`
- Pre-existing changes: `<paths not owned by this task, or none>`

## Commands and results

- Command: `<exact command>`
- Result: `<exit status, counts, duration, and artifact path>`
- Not run: `<required or useful gate not run, with reason, or none>`

## Decisions and rationale

- `<Chosen and rejected alternatives; mark frozen decisions>`
- Local implementation discretion: `<mechanics/refactors/tests allowed within named paths; no new dependency, public/API/schema change, migration, or external write unless authorized>`
- Rejected shallow fix: `<known case-specific approach not to repeat, or none>`

## Risks, deviations, and unknowns

- `<Observation, impact, and whether it changes later work>`

## Authority and stop conditions

- Continue automatically: `<in-scope actions, including bounded refactors and adjacent tests>`
- Stop and escalate: `<specific conditions>`

## Owned live resources

- `<Terminal/session IDs, processes, CI URLs, temporary directories, or none>`

## Requested response from the next role

`<Implement, verify, choose, diagnose, approve, or close—with one precise result
such as ACCEPT_STAGE_1 or a named defect plus acceptance delta. When Verification
mode is self, keep the capable model in this context for a lightweight conformance
check; independent requires a separate capable context. Only a preselected bugbot
or security mode may name exactly /review-bugbot or /review-security. Never use
generic /review or ask the user to select a reviewer.>`
