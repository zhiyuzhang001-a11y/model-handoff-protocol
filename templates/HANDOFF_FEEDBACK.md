# Model handoff feedback

This file is local operational feedback, not bootstrap context. Add an entry only
when a switch causes measurable friction; do not log routine successful switches.
Keep at most 20 open/recent entries and archive older resolved entries in reports.

Keep project-specific fixes here. For a potentially generic defect, use this file
as private evidence, then reproduce the issue generically in a separate clone of
the protocol source. Never upload this file or a target-project rule directly to
public upstream `main` without privacy review, regression tests, and branch review.

## Entry template

### `<YYYY-MM-DD>-<short-id>` — `<OPEN | RESOLVED | REJECTED>`

- Direction: `<planner/verifier -> implementer | implementer -> planner/verifier | same-role>`
- Symptom: `<missing context, repeated work, stale pointer, wrong route, oversized packet, or other>`
- Evidence: `<handoff ID and exact observable impact; no full logs>`
- Scope: `<project-specific | protocol-generic | unclear, with reason>`
- Local workaround: `<target-project-only adjustment, or none>`
- Proposed change: `<smallest protocol, prompt, checker, or template adjustment>`
- Candidate branch: `<protocol-source branch/commit, or none>`
- Validation: `<regression test and commands/results, or pending>`
- Decision: `<owner, review condition, and OPEN/RESOLVED/REJECTED reason>`
- Resolution proof: `<later real handoff ID that proved the improvement, or pending>`
