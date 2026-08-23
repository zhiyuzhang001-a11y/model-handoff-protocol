# Example: capable implementer to same-context verification

This is an abbreviated teaching example, not a valid live packet. Start from
`templates/MODEL_HANDOFF.md` and complete every required field.

- Protocol version: `0.6`
- Verification mode: `self`
- Handoff ID: `2026-01-18-m2-local-refactor-self-review`
- State: `EXECUTION_TO_VERIFY`
- From role: `implementer`
- To role: `planner/verifier`
- Recommended capability: `capable`
- Contract depth: `standard`

## Verified completed work

- The capable model implemented a bounded local refactor in the named files.
- All frozen focused and regression gates passed.

## Risks, deviations, and unknowns

- No scope, dependency, public/API/schema, migration, external-write, or frozen
  assumption changed; no independent gate was required.

## Requested response from the next role

Do not switch models. In this context, change role to planner/verifier and inspect
only plan conformance, diff scope, named gates, evidence, and deviations. Return
`ACCEPT_STAGE` or stop and reroute to `independent` if an independence trigger appears.
