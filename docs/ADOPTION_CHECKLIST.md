# Adoption checklist

## Before installation

- [ ] Choose canonical status, implementation-plan, milestone-plan, and report paths.
- [ ] Decide which actions may run automatically and which require confirmation.
- [ ] Decide whether external writes, releases, deployments, and destructive actions
      are ever in scope.
- [ ] Identify authoritative test suites, datasets, and performance/security gates.
- [ ] Preserve or commit current work so installer output is easy to review.

## Installation

- [ ] For remote installation, use the fixed upstream URL and preview the exact
      fetched revision before applying.
- [ ] Run `python3 scripts/install.py <project>` without `--apply`.
- [ ] Review every `would_create`, `identical`, `differs`, and `conflict` entry.
- [ ] Run with `--apply` only after the target and paths are correct.
- [ ] Manually merge protocol changes for `differs`; resolve `conflict` paths.
- [ ] Customize project paths and approval boundaries without duplicating rules.
- [ ] Confirm `python3 .model-handoff/handoff.py snapshot .` runs locally.
- [ ] Confirm `python3 .model-handoff/update.py .` can preview later upstream
      changes without overwriting `differs`.

## First live handoff

- [ ] Give the packet a unique ID and valid state.
- [ ] Separate task-owned changes from pre-existing working-tree changes.
- [ ] Name one user-visible objective and explicit non-goals.
- [ ] Record exact gates, commands, counts, artifacts, and stop conditions.
- [ ] Route most bounded, reversible, test-protected units to an economical model;
      reserve planning, independent review, and judgment-heavy/high-risk units for
      a capable model.
- [ ] For high-risk corrections, record all applicable invariant dimensions and
      deterministic timing controls; explain omissions.
- [ ] Record one exact next action and one requested response.
- [ ] Set `Review mode` to `self`, `inline`, `bugbot`, or `security` only for
      `EXECUTION_TO_REVIEW`; use `none` for every other state.
- [ ] Use `self` only for capable thin/standard execution with passing gates, no
      material deviation or boundary change, and no independent-review requirement;
      use `inline` in a separate capable context otherwise.
- [ ] Set `Recommended capability` to `capable` for planner/reviewer; choose
      `economical` for most bounded implementation and `capable` for difficult or
      high-risk implementation.
- [ ] Copy the active milestone and exact next action verbatim between status and
      handoff; point to exact required/on-demand headings instead of whole files.
- [ ] Keep detailed logs and history in referenced artifacts, not the bootstrap.
- [ ] Confirm no handoff section exceeds the helper's compactness limits.
- [ ] Confirm no unrecorded process, terminal, approval prompt, or CI run remains.
- [ ] Run `python3 .model-handoff/handoff.py check .` as the final switch step.

## Review after two switches

- [ ] Did the incoming role reconstruct the objective without chat history?
- [ ] Was any completed work repeated?
- [ ] Did either role silently choose architecture or weaken acceptance?
- [ ] Did a second failure of the same invariant trigger high-risk replanning
      instead of another narrow patch?
- [ ] Were commands and results precise enough to reproduce?
- [ ] Were the permanent rules concise and the dynamic packet current?
- [ ] Did the incoming role stop loading context once the contract was safe?
- [ ] Was the contract thin enough to leave reversible local choices to the
      implementer, but detailed enough to prevent unsafe guessing?
- [ ] Remove instructions that are duplicated without changing a measured need.

## Promote a protocol improvement

- [ ] Record measurable evidence privately in `.model-handoff/FEEDBACK.md`.
- [ ] Classify the issue as project-specific, protocol-generic, or unclear.
- [ ] Keep project-specific workarounds in the target project.
- [ ] Sanitize a generic reproducer before it enters the protocol source.
- [ ] Use a candidate branch; do not push an unreviewed target rule to `main`.
- [ ] Add a regression test and run full validation before review and merge.
- [ ] Preview installation and manually merge only relevant `differs`.
- [ ] Mark feedback resolved only after a later live switch proves the change.
