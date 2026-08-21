# Current model handoff

- Handoff ID: `<date-or-sequence>-<short-purpose>`
- State: `PLAN_TO_EXECUTE | EXECUTION_TO_REVIEW | REVIEW_TO_EXECUTE | BLOCKED_TO_DECIDE | COMPLETE | IDLE`
- From role: `planner/reviewer | implementer`
- To role: `planner/reviewer | implementer`
- Active milestone: `<ID and stage, or none>`
- Branch/commit: `<branch and HEAD>`
- Working tree: `<clean, or separate task-owned and pre-existing paths>`

## Objective and user-visible outcome

`<One concrete outcome, not an activity such as “continue working”.>`

## Frozen scope and non-goals

- Allowed: `<repositories, files, actions, and decisions>`
- Deferred or forbidden: `<explicit non-goals>`

## Acceptance and required evidence

- `<Exact test, dataset, threshold, artifact, cleanup, or documentation gate>`

## Verified completed work

- `<Completed change and its evidence; the next role must not repeat it>`

## Remaining ordered work

1. `<bounded step>`
2. `<bounded step>`

## Exact next action

`<One command, inspection, edit, or decision with target and expected result.>`

## Changes and repository state

- `<Files, commits, diffs, generated assets, and pre-existing changes>`

## Commands and results

- Command: `<exact command>`
- Result: `<exit status, counts, duration, and artifact path>`

## Decisions and rationale

- `<Chosen and rejected alternatives; mark frozen decisions>`

## Risks, deviations, and unknowns

- `<Observation, impact, and whether it changes later work>`

## Authority and stop conditions

- Continue automatically: `<in-scope actions>`
- Stop and escalate: `<specific conditions>`

## Owned live resources

- `<Terminal/session IDs, processes, CI URLs, temporary directories, or none>`

## Requested response from the next role

`<Implement, review, choose, diagnose, approve, or close—with one precise result.>`
