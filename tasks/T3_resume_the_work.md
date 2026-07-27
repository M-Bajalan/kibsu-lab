---
type: task
---

# T3 -- Resume the work

**Verifier:** `python tools/check_task.py T3` (exit 0 = done, 1 = not yet, 2 = could not run)

## The ask

This repository ships with T1 (the rolling 3-month distributor share KPI, see
`tasks/T1_add_kpi.md`) deliberately **half-done**, on a branch:

```
git checkout task/T1-in-progress
```

That branch has a real, partial commit -- a helper that computes each customer's
rolling 3-month amount but does not yet write `reports/rolling_3mo_share.csv` or
compute the company-wide denominator / percentage. `docs/STATE.md` on that branch
carries the trail: what was done, what is left, and why it stopped there.

**A fresh agent must CONTINUE this work, not restart it.** Read the existing helper
before writing a new one; finish wiring it to `sales_report.py`'s output per
`tasks/T1_add_kpi.md`'s contract; commit on top of the existing history.

## Accept

```
git checkout task/T1-in-progress
python tools/check_task.py T3    # must exit 0
```

`check_task.py T3` checks two independent things: that the original half-done commit
(below) is still an **ancestor** of `HEAD` -- proving this was a continuation, not a
fresh reset-and-redo -- and that `check_task.py T1`'s own independent recomputation
passes on the finished result.

## A note on the `task:` field

T3 has no `task:` field of its own -- `check_task.py T3` never looks for a literal
`task: T3` line, only for the marker's ancestry and for `check_T1()` passing. Finishing
this task IS finishing T1, so the entry that closes it out is the same `task: T1` entry
`tasks/T1_add_kpi.md` asks for. Do not invent a `task: T3` line: no checker reads one,
and `skills/change-log/SKILL.md` reserves the field strictly for entries an actual gate
checks against.

MARKER_COMMIT: fa64590aa7233a2bf18fb647cc68c6414f54b75e
