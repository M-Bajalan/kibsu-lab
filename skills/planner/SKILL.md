---
name: planner
type: skill
genre: procedure
description: >
  How multi-step work gets planned and recorded in this repository before
  execution starts. Produces a phased plan file that the gate skill can
  check off, phase by phase.
---

# planner

## When to use this

Any task with 3 or more distinct steps, or any task that touches more than one file
under `tools/`, `skills/`, or `docs/`. A one-line fix does not need a plan file --
just make the change, verify it, log it (`skills/change-log/SKILL.md`).

## Step 1 -- write the plan file

Create `docs/plans/<YYYY-MM-DD>-<slug>.md` with this shape:

```md
# Plan: <name>

**Goal:** <one line -- what "done" looks like>
**Verifier:** <exact command that proves it, e.g. `python tools/check_task.py T1`>

## Phase 1: <name>
- [ ] Task
- [ ] Task
**Verify:** <command> -> expected exit <N>

## Phase 2: <name>
- [ ] Task
**Verify:** <command> -> expected exit <N>
```

Every phase names its own verify command and expected exit code **before** the phase
starts -- naming the proof after the change is how a wrong fix gets reported as a
right one.

## Step 2 -- work one phase at a time

Do not start Phase 2 until Phase 1's verify command has actually been run and its
exit code checked. Check off each task box (`- [ ]` -> `- [x]`) only after its own
verify step passed, not when you believe it should pass.

## Step 3 -- STOP on ambiguity

If a phase's done-state cannot be checked by a command (an exit code, a diff, a file
that must exist), that is a planning defect: redesign the phase into something
checkable, or say plainly that this step is not machine-checkable and needs a human
read before the plan continues. Never soften a checker to make an unclear phase pass.

## Step 4 -- close the plan

When every phase's box is checked and every verify command has actually been run
(not assumed), log the change per `skills/change-log/SKILL.md` and update
`docs/STATE.md`'s row for the track this plan touched.

## Checklist before you say "planned"

- [ ] Does every phase name an exact verify command and expected exit code?
- [ ] Is there at least one phase, or was a single-file change correctly routed to
      `skills/change-log/SKILL.md` instead of a plan file?
- [ ] Is the plan file saved at `docs/plans/<date>-<slug>.md`?
