# kibsu-lab

Clone this, point any coding agent at `AGENTS.md`, give it a task from `tasks/` --
then check its work with one command.

kibsu-lab is a public, cloneable virtual workspace for one fictional distribution
company, **Tuppi Trading Co.** It exists to demonstrate and test the
[`kibsu`](https://pypi.org/project/kibsu/) package against a realistic,
machine-checkable, multi-agent workflow -- and to be a fair, disposable place to
run kibsu's own governance tooling against a repo nobody has to protect.

The clay tablet was the ancient world's hard drive -- the first structured
database. This lab teaches with tablets of its own.

## Quickstart

```
git clone <this-repo>
cd kibsu-lab
python tools/generate_data.py          # data/ is gitignored -- generate it yourself
```

Give a coding agent `AGENTS.md` and one of the three tasks in `tasks/`:

```
python tools/check_task.py T1          # exit 1 -- not done yet, on a pristine clone
# ... hand the agent tasks/T1_add_kpi.md, let it work ...
python tools/check_task.py T1          # exit 0 once it's actually done
```

Then see what the repo's own governance says about itself:

```
python -m kibsu report .
```

## What's here

| Task | File | Checker |
|---|---|---|
| Add a KPI (rolling 3-month distributor share) | `tasks/T1_add_kpi.md` | `python tools/check_task.py T1` |
| Fix the reconciliation (a planted double-loaded batch) | `tasks/T2_fix_reconciliation.md` | `python tools/check_task.py T2` |
| Resume a half-done task from another agent's session | `tasks/T3_resume_the_work.md` | `python tools/check_task.py T3` |

Every checker exits 1 on this pristine repo -- see `docs/STATE.md`. A checker that
passes before the task is done proves nothing; that was verified, not assumed --
see `docs/memory/learnings/`.

## Baseline (recorded at commit `PENDING-FILL-AT-SHIP`)

```
python -m kibsu report .
```

```
PENDING-FILL-IN-AT-SHIP -- see README.md history for the exact recorded run
```

```
python -m kibsu audit . --definitions
```

```
PENDING-FILL-IN-AT-SHIP
```

## Design

Full build contract (locked decisions, phase-by-phase accept criteria):
`Kibsu_Lab_v1_Design_2026-07-27.md` (in the design's own workspace, not this repo --
this repo is the built artifact, not the design doc).

## License

MIT. See `LICENSE`. Every name and every row of data here is fictional -- see
`PROVENANCE.md`.
