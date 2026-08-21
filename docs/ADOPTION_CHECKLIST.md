# Adoption checklist

## Before installation

- [ ] Choose canonical status, implementation-plan, milestone-plan, and report paths.
- [ ] Decide which actions may run automatically and which require confirmation.
- [ ] Decide whether external writes, releases, deployments, and destructive actions
      are ever in scope.
- [ ] Identify authoritative test suites, datasets, and performance/security gates.
- [ ] Preserve or commit current work so installer output is easy to review.

## Installation

- [ ] Run `python3 scripts/install.py <project>` without `--apply`.
- [ ] Review every `would_create` and `exists` entry.
- [ ] Run with `--apply` only after the target and paths are correct.
- [ ] Merge template content manually when a destination already exists.
- [ ] Customize project paths and approval boundaries without duplicating rules.

## First live handoff

- [ ] Give the packet a unique ID and valid state.
- [ ] Separate task-owned changes from pre-existing working-tree changes.
- [ ] Name one user-visible objective and explicit non-goals.
- [ ] Record exact gates, commands, counts, artifacts, and stop conditions.
- [ ] Record one exact next action and one requested response.
- [ ] Confirm no unrecorded process, terminal, approval prompt, or CI run remains.

## Review after two switches

- [ ] Did the incoming role reconstruct the objective without chat history?
- [ ] Was any completed work repeated?
- [ ] Did either role silently choose architecture or weaken acceptance?
- [ ] Were commands and results precise enough to reproduce?
- [ ] Were the permanent rules concise and the dynamic packet current?
- [ ] Remove instructions that are duplicated without changing a measured need.
