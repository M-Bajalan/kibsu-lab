---
type: plan
---

# Plan: the gate skill names commands that run, and stops pointing at one that rewrites the baseline

**Goal:** every command `skills/gate/SKILL.md` tells an agent to run exits without an
argument error, and none of them changes what this repository has agreed to accept.
**Verifier:** `python -m kibsu gate --check` -> exit 0, `python -m kibsu gate --status` ->
exit 0, and `git status --porcelain` empty after both.

Why it is needed: `docs/STATE.md`'s SKILLS row has carried this since 2026-10-11 -- the skill
names `kibsu gate --check .`, `--status .` and `--baseline .`, and kibsu rejects all three
with exit 2, `unrecognized arguments: .`.

## Phase 1: the baseline before the edit

A skill is a measured unit, so the audit is taken before the file is touched, with the same
kibsu on both sides (`kibsu 0.10.0`, scorer 0.11.0), at commit `afa7381`.

- [x] Record `python -m kibsu audit .` per unit.

**Verify:** `python -m kibsu audit .` -> expected exit 0
**Verify:** `python tools/check_baseline.py` -> expected exit 0 (the page is right before the
change)

**Recorded:**

| unit | genre | instructions | checkable |
|---|---|---|---|
| skills/architect | procedure | 14 | 8 |
| skills/change-log | procedure | 11 | 3 |
| skills/gate | procedure | 12 | 10 |
| skills/planner | procedure | 8 | 5 |
| skills/strategist | doctrine | 9 | 0 |
| skills/thinking-partner | doctrine | 6 | 0 |

Procedure: 45 instructions, 26 checkable, 57.8%. Two of the gate unit's ten checkable
verdicts rest on a command that does not run (`gate --check .`, `gate --baseline .`): the
scorer counts a command that is named, not one that works.

## Phase 2: find out what the three commands do before reviving them

- [x] In a scratch clone, run each command with the dot (as written) and without it.
- [x] Watch `git status` after each: does it write?

**Verify:** `python -m kibsu gate --check .` -> expected exit 2 (the defect as recorded)
**Verify:** `python -m kibsu gate --check` -> expected exit 0, nothing written
**Verify:** `python -m kibsu gate --status` -> expected exit 0, nothing written
**Verify:** `python -m kibsu gate --baseline` -> expected exit 0 and nothing written, if the
skill's own words are right ("see `python -m kibsu gate --baseline .`")

**What happened:** with the dot, all three exit 2 and write nothing. Without it, `--check`
and `--status` exit 0 and write nothing. `--baseline` exits 0 and **modifies
`.kibsu/gate_baseline.json`** -- the skill's "see" was wrong. It does not show the baseline;
it rewrites it to accept whatever the gates report now. Proven further in a scratch clone:
with one accepted violation removed, `gate --check` exits 1 and names it; after
`gate --baseline`, `gate --check` exits 0 again. Dropping the dot alone would have pointed
an agent, at the moment of judging a mismatch, to the command that hides it.
(Said plainly: this exploration was first run before this plan file was written, and run
again in order afterwards. The Phase 4 prediction was made knowing it.)

## Phase 3: edit the skill

- [x] Drop the dot from `gate --check` and `gate --status`.
- [x] Whatever Phase 2 finds for `gate --baseline`, the sentence that points to it must end
      up pointing at a command that only reads. Done: it points to `gate --check`, and a
      sentence says never to run `--baseline` to settle the question.

**Verify:** every `python -m kibsu gate ...` command the skill tells an agent to RUN exits 0
on a pristine clone, and `git status --porcelain` is empty afterwards.

## Phase 4: the audit after the edit

**Predicted before measuring:** the gate unit goes from 12 instructions / 10 checkable to
13 / 11, and the headline from 57.8% (26 of 45) to 58.7% (27 of 46). If Phase 2 changes what
Phase 3 has to write, this prediction is revised there, before the audit is run.

- [x] `python -m kibsu audit .` per unit, compared with Phase 1.

**Verify:** `python -m kibsu audit .` -> expected exit 0; only `skills/gate` may differ from
Phase 1.

**What happened:** as predicted. Gate 13 instructions, 11 checkable; procedure 27 of 46,
58.7%; no other unit moved. The newly counted checkable sentence is the prohibition
("Never run `python -m kibsu gate --baseline` ..."): it names a command in order to forbid it.
So the point gained is not the improvement, and the README says so.

## Phase 5: re-capture the README block

This plan file and any learning are new documents, and the audit table moves with the skill.

- [x] `README.md` Baseline -- both blocks, from what the tool prints.

**Verify:** `python tools/check_baseline.py` -> expected exit 1 before the re-capture (once
the new files are known to git), expected exit 0 after it, with no "not tracked by git" note.

**What happened:** exit 1 on five lines (`19 docs` against `21 docs`, and four audit and
report figures), then exit 0 after the re-capture. Two new documents, not one: the lesson
became `docs/memory/learnings/find-out-what-a-dead-command-does-before-reviving-it.md`.

## Phase 6: record it

- [x] `README.md` -- say that this time the repository moved, and what the rise means.
- [x] `docs/STATE.md` SKILLS row -- the known defect is closed.
- [x] `docs/CHANGELOG.md` -- the entry.

**Verify:** `python tools/check_baseline.py` -> expected exit 0
**Verify:** `python -m kibsu check .` -> expected exit 0
**Verify:** `python -m kibsu gate --check` -> expected exit 0
