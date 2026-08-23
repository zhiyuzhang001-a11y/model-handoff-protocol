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
- `EXECUTION_TO_VERIFY` was recorded once, only after the whole batch passed:
  one boundary record, one self closeout, zero additional snapshots.

## Commands and results

- Focused and full-regression commands both exited 0; exact counts are recorded
  in the named evidence artifact.
- `python3 .model-handoff/handoff.py check .` passed and proves only contract,
  status, Git, and routing consistency—not code correctness or test evidence.

## Risks, deviations, and unknowns

- No scope, dependency, public/API/schema, migration, external-write, or frozen
  assumption changed; no independent gate was required.

## Requested response from the next role

Do not switch models or run snapshot. Reuse the already loaded checked contract,
change role to planner/verifier, and perform one integrated closeout over plan
conformance, final diff scope, named gates, evidence, and deviations. Return
`ACCEPT_STAGE` or stop and reroute to `independent` if an independence trigger appears.
