# Example: implementer to reviewer

This is an abbreviated teaching example, not a valid live packet. Start from
`templates/MODEL_HANDOFF.md` and complete every required field.

- Protocol version: `0.4`
- Review mode: `inline`
- Handoff ID: `2026-01-15-m4-cache-key-review`
- State: `EXECUTION_TO_REVIEW`
- From role: `implementer`
- To role: `planner/reviewer`
- Recommended capability: `capable`
- Contract depth: `standard`
- Last verified: `2026-01-15T11:10:00Z`
- Active milestone: `M4 Stage 1`
- Base branch: `feature/cache`
- Base HEAD: `<CURRENT_HEAD>`
- Working tree: dirty

## Verified completed work

- Added a 64-entry in-session cache keyed by repository, query type, symbol, and
  target range.
- Timeout and error responses bypass insertion; close clears all entries.
- No persistent process or disk state was introduced.

## Commands and results

- `python -m unittest tests.test_cache tests.test_service -v`
- Exit 0; 23 tests passed in 1.4 seconds.
- One initial assertion expected two provider starts and failed before the test
was corrected to the frozen requirement of one; no source state changed.

## Context delta and evidence pointers

- Changed since previous handoff: cache implementation and focused tests added.
- Must read now: diff for `src/service.py` and `tests/test_service.py`.
- Read on demand: `reports/M4_BASELINE.md` only if test-count attribution differs.
- Evidence artifacts: focused test command and Git diff named above.
- Safe to skip: M0–M3 reports and unchanged design alternatives.

## Risks, deviations, and unknowns

- No deviation from scope.
- Full regression has not run because the plan requires review first.

## Owned live resources

None.

## Requested response from the next role

Inspect the two-file diff and choose `ACCEPT_STAGE_1` or return a named defect and
acceptance delta. If accepted, authorize the full regression as the next action.
