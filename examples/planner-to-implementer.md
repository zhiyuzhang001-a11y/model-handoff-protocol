# Example: planner to implementer

This is an abbreviated teaching example, not a valid live packet. Start from
`templates/MODEL_HANDOFF.md` and complete every required field.

- Protocol version: `0.3`
- Review mode: `none`
- Handoff ID: `2026-01-15-m4-cache-key`
- State: `PLAN_TO_EXECUTE`
- From role: `planner/reviewer`
- To role: `implementer`
- Contract depth: `standard`
- Last verified: `2026-01-15T09:30:00Z`
- Active milestone: `M4 Stage 1`
- Base branch: `main`
- Base HEAD: `<CURRENT_HEAD>`
- Working tree: clean

## Objective and user-visible outcome

Add a bounded cache for successful read-only symbol lookups so a repeated query
returns without restarting the provider.

## Frozen scope and non-goals

- Allowed: service cache module and its focused tests.
- Non-goals: persistent daemon, disk cache, write queries, eviction redesign.

## Acceptance and required evidence

- `python -m unittest tests.test_cache tests.test_service -v` passes.
- Capacity is 64; timeout/error responses are not cached; close clears the cache.
- A repeated focused test proves the provider starts once.

## Verified completed work

- Baseline tests pass: 18 tests, exit 0.
- Profile identifies provider startup as the repeated cost.

## Remaining ordered work

1. Add the in-memory cache and focused tests.
2. Run the focused suite and record counts.
3. Return for review before full regression.

## Exact next action

Inspect the service query entry point and cache lifecycle, then propose the
smallest edit region. Do not edit before confirming timeout/error behavior.

## Context delta and evidence pointers

- Changed since previous handoff: M4 Stage 1 is now approved for execution.
- Must read now: `docs/IMPLEMENTATION_PLAN.md#M4 Stage 1` for frozen cache gates.
- Read on demand: `reports/M4_PROFILE.md#Provider startup` only if the baseline
  assumption conflicts with observed code.
- Evidence artifacts: `reports/M4_BASELINE.md`.
- Safe to skip: completed M0–M3 reports and full profiling logs.

## Authority and stop conditions

- Continue automatically inside the two named modules and focused tests.
- Stop if cache identity cannot include repository, query type, and target range,
  or if provider ownership must become persistent.

## Requested response from the next role

Implement the bounded change and request `ACCEPT_STAGE_1` with exact evidence.
