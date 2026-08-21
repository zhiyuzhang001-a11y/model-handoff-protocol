# Example: completed milestone

- Handoff ID: `2026-01-20-m4-complete`
- State: `COMPLETE`
- From role: `planner/reviewer`
- To role: `planner/reviewer`
- Active milestone: `M4 complete`

## Acceptance and required evidence

- Focused tests: 23/23.
- Full tests: 146/146.
- Packaging verification: pass.
- Clean installation smoke: pass.
- Working tree: clean; no owned process remains.

## Decisions and rationale

The bounded in-session cache met the frozen performance target without a daemon,
disk state, or incomplete-response caching. `ACCEPT_STAGE` and final gates pass.

## Exact next action

None. Set project status to `IDLE`. Future work requires a new milestone contract.

## Requested response from the next role

No action until a user selects or approves the next milestone.
