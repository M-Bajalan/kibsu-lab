---
name: change-log
genre: procedure
description: >
  The log chain for this repository: what to write, where, and when, after any
  meaningful change. Run it before you say a task is done. Self-contained --
  no other skill needed to execute it.
---

# change-log

You changed something in this repository. Before you report the task finished, walk
this checklist top to bottom. Every step names the exact file to touch.

## The chain

### 1. `docs/STATE.md` -- always, if a track's status changed

Open `docs/STATE.md`. Find the row for the track you touched (`DATA`, `REPORTING`,
`RECONCILIATION`, `TASKS`, or a new one you're adding). Update its `Next action`
cell and its `Last touched` date. Do not leave a stale next action after finishing it.

### 2. `docs/CHANGELOG.md` -- always, when something shipped

Prepend a new entry at the **top** of `docs/CHANGELOG.md`, directly under the file's
header, above every existing entry (newest-first):

```md
## [YYYY-MM-DD HH:MM] - <one-line title>
### Changed
- <item -- with a path>
### Fixed
- <item -- with a path>
### Added
- <item -- with a path>
```

Use only the subsections you need. The title must say what changed in plain words --
`check_task.py T1` reads this file's newest entry as evidence a task actually
finished, so a vague title ("misc updates") fails that check even when the code is
correct.

### 3. Learnings -- whenever you learn something reusable

If the change taught a durable lesson -- a gotcha, a root cause, a "check this first
next time" -- write it to `docs/memory/learnings/<slug>.md` as its own file. Do not
bury a reusable lesson inside a CHANGELOG entry where the next agent will never find
it by searching a topic.

A learning that turns out to be **consulted by a later task's checker** (see
`tools/check_task.py T2`, which requires `docs/memory/learnings/reconciliation-check-batches-first.md`
to exist and be non-empty) is not decorative -- it is load-bearing. Extend an existing
learning file rather than duplicating it when the lesson is the same one, restated.

### 4. Verify before you claim done

Run the repo's own checkers, bare, never through a pipe (a pipe swaps the exit code
you're checking for the exit code of whatever it was piped into):

```
python tools/check_task.py <TASK>
```

`echo $?` (or `echo %ERRORLEVEL%` on Windows) immediately after, to confirm the exit
code you're about to report is the one that actually happened -- not the one you
expect.

### 5. Report format

End your message with the same shape every time, so the state of the chain is
visible at a glance:

```
LOG chain: 1(STATE.md)✓ 2(CHANGELOG.md)✓ 3(learnings)— 4(verified: exit 0)✓
```

`✓` = done. `—` = not applicable, with the reason stated inline. If a step is
neither `✓` nor a stated `—`, the task is **not done** -- say what's missing instead
of reporting completion.

## Decision table

| You did... | Steps |
|---|---|
| Fixed a bug / added a feature | 1, 2, 4, 5, (3 if you learned something reusable) |
| Doc-only edit | 1, 5 |
| Learned a reusable lesson with no code change | 3, 5 |
| Anything a task's checker (`tools/check_task.py`) will grade | 1, 2, 4, 5 |
