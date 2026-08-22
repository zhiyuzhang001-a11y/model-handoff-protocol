# Example: completed milestone

This is an abbreviated teaching example, not a valid live packet. Start from
`templates/MODEL_HANDOFF.md` and complete every required field.

- Protocol version: `0.4`
- Review mode: `none`
- Handoff ID: `2026-01-20-m4-complete`
- State: `COMPLETE`
- From role: `planner/reviewer`
- To role: `planner/reviewer`
- Recommended capability: `capable`
- Contract depth: `thin`
- Last verified: `2026-01-20T12:00:00Z`
- Active milestone: `M4 complete`

## Context delta and evidence pointers

- Changed since previous handoff: final gates accepted and M4 closed.
- Must read now: none.
- Read on demand: `reports/M4_COMPLETION.md` if independent audit is requested.
- Evidence artifacts: `reports/M4_COMPLETION.md`.
- Safe to skip: implementation handoffs and raw successful test logs.

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
