# Example: blocked decision

- Handoff ID: `2026-01-16-m5-runtime-choice`
- State: `BLOCKED_TO_DECIDE`
- From role: `implementer`
- To role: `planner/reviewer`
- Active milestone: `M5 Stage 0`

## Objective and user-visible outcome

Reduce first-query startup without changing default privacy or lifecycle behavior.

## Verified completed work

- Profiling shows 78% of latency is provider process startup.
- In-process parsing cannot reproduce the required semantic result.

## Risks, deviations, and unknowns

- Option A keeps on-demand startup and can likely improve only 10–15%.
- Option B adds an optional resident local process and could improve 60–70%, but
  expands lifecycle, privacy, crash-recovery, and shutdown scope.

## Authority and stop conditions

The active contract forbids persistent background state. Implementing option B
would materially expand architecture and requires a new decision.

## Requested response from the next role

Choose `KEEP_ON_DEMAND` and revise the performance target, or prepare a user
decision for `OPTIONAL_RESIDENT_SERVICE`. Do not implement either before choice.
