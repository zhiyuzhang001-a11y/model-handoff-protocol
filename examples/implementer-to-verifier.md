# Example: implementer to verifier

This is an abbreviated teaching example, not a valid live packet. Start from
`templates/MODEL_HANDOFF.md` and complete every required field.

- Protocol version: `0.6`
- Verification mode: `independent`
- Handoff ID: `2026-01-15-m4-cache-key-review`
- State: `EXECUTION_TO_VERIFY`
- From role: `implementer`
- To role: `planner/verifier`
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
- `python -m unittest discover -s tests -v`
- Exit 0; 96 tests passed in 4.8 seconds before this `EXECUTION_TO_VERIFY` packet.
- One initial assertion expected two provider starts and failed before the test
was corrected to the frozen requirement of one; no source state changed.

## Context delta and evidence pointers

- Changed since previous handoff: cache implementation and focused tests added.
- Must read now: diff for `src/service.py` and `tests/test_service.py`.
- Read on demand: `reports/M4_BASELINE.md` only if test-count attribution differs.
- Evidence artifacts: focused/full-regression commands and Git diff named above.
- Safe to skip: M0–M3 reports and unchanged design alternatives.

## Risks, deviations, and unknowns

- No deviation from scope.
- Every focused and full-regression gate in the batch completed before handoff.

## Owned live resources

None.

## Requested response from the next role

Inspect the two-file diff and completed focused/full-regression evidence, then
choose `ACCEPT_STAGE_1` or return one consolidated defect batch and acceptance delta.
