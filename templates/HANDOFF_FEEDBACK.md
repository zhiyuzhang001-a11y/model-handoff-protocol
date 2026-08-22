# Model handoff feedback

This file is local operational feedback, not bootstrap context. Add an entry only
when a switch causes measurable friction; do not log routine successful switches.
Keep at most 20 open/recent entries and archive older resolved entries in reports.

## Entry template

### `<YYYY-MM-DD>-<short-id>` — `<OPEN | RESOLVED | REJECTED>`

- Direction: `<planner/reviewer -> implementer | implementer -> planner/reviewer | same-role>`
- Symptom: `<missing context, repeated work, stale pointer, wrong route, oversized packet, or other>`
- Evidence: `<handoff ID and exact observable impact; no full logs>`
- Proposed change: `<smallest protocol, prompt, checker, or template adjustment>`
- Decision: `<owner and review condition>`
