---
type: state
---

# STATE

Project-state registry for kibsu-lab -- one row per track. This is the file a fresh
agent reads (via `AGENTS.md`) to find out what is true right now and what to do
next, without re-deriving it from the whole repository.

| Track | Status | Next action | Last touched |
|---|---|---|---|
| DATA | STABLE | `tools/generate_data.py` ships with 3 planted defects (P1 double-loaded batch, P2 orphan products, P3 reporting gap). No change needed unless a task calls for a new defect. | 2026-07-27 |
| REPORTING | BASELINE | `tools/sales_report.py` produces `reports/monthly_sell_through.csv`. Rolling 3-month distributor share is NOT yet added on `main` -- that is task T1 (`tasks/T1_add_kpi.md`). A partial start exists on branch `task/T1-in-progress` -- see task T3 (`tasks/T3_resume_the_work.md`). | 2026-07-27 |
| RECONCILIATION | BROKEN (by design) | `tools/reconcile.py` exits 1 out of the box (P1). Fixing it -- batch-id dedupe -- is task T2 (`tasks/T2_fix_reconciliation.md`). | 2026-07-27 |
| TASKS | 3 SHIPPED | T1 (add KPI), T2 (fix reconciliation), T3 (resume half-done T1 work on `task/T1-in-progress`) all have machine checkers under `tools/check_task.py`. All three currently FAIL on this pristine repo -- that is correct; see `tasks/*.md`. | 2026-07-27 |
| TOOLING | PINNED kibsu 0.9.0 | `.github/workflows/lab-ci.yml` pins `kibsu==0.9.0` and `README.md`'s Baseline block was captured with that version from a fresh clone. When kibsu publishes a newer release, re-run the README Quickstart on a fresh clone with it; if any printed line differs from the Baseline block, re-capture the block and move the pin in the SAME commit, and say in `docs/CHANGELOG.md` whether the instrument moved or this repository did. OPEN: CI checks out a full clone so its report is the Baseline's, but nothing yet COMPARES the two -- a green run is not evidence about the block until a step does. | 2026-10-11 |
| SKILLS | 6 UNITS | Skill team complete at 6 units -- `gate`, `planner`, `change-log`, `architect` (procedure); `thinking-partner`, `strategist` (doctrine). ONE KNOWN DEFECT, not yet fixed: `skills/gate/SKILL.md` names three commands with a trailing `.` (`kibsu gate --check .`, `--status .`, `--baseline .`) and kibsu rejects all three with exit 2, `unrecognized arguments: .` -- on every version from 0.1.0 to 0.9.0. The working forms drop the dot (or pass `--repo .`). Fixing it is a skill edit: take a fresh `python -m kibsu audit .` baseline and record it BEFORE the edit -- see the baseline note in `README.md`. | 2026-10-11 |

## How to read this file

Each row's `Next action` is what an agent should do if they pick up that track --
not a history of what happened (that's `docs/CHANGELOG.md`) and not a lesson
learned (that's `docs/memory/learnings/`). When you finish a next action, update
this row before you report the task done -- see `skills/change-log/SKILL.md`.
