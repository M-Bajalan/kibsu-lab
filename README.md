---
type: readme
---

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
python -m kibsu index .                # builds .kibsu/index.json -- also gitignored, build it yourself
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

(The `index` step above is not optional set-up trivia -- the "Baseline" section below is the
literal output of running these commands in this exact order against a fresh clone. If you skip
it, `report` truthfully scores lower, because there is nothing yet to know your conventions from.)

## What's here

| Task | File | Checker |
|---|---|---|
| Add a KPI (rolling 3-month distributor share) | `tasks/T1_add_kpi.md` | `python tools/check_task.py T1` |
| Fix the reconciliation (a planted double-loaded batch) | `tasks/T2_fix_reconciliation.md` | `python tools/check_task.py T2` |
| Resume a half-done task from another agent's session | `tasks/T3_resume_the_work.md` | `python tools/check_task.py T3` |

Every checker exits 1 on this pristine repo -- see `docs/STATE.md`. A checker that
passes before the task is done proves nothing; that was verified, not assumed --
see `docs/memory/learnings/`.

## Baseline (after indexing; measured at commit `4940183`, kibsu 0.1.0 from PyPI)

Captured by literally running the Quickstart above, verbatim, against a fresh clone --
`git clone`, `generate_data.py`, `kibsu index .`, then the two commands below. If your own run
doesn't match this block, the difference is real and worth reporting -- this block is not
allowed to say anything a fresh clone can't reproduce by following this README's own steps.

```
python -m kibsu report .
```

```
  WHAT YOUR AGENTS CANNOT DO HERE YET
  --------------------------------------------------------------------------
  +  Find your docs             14 docs, index present.
  +  Know your conventions      consistent frontmatter (type) - enforceable.
  +  Prove they followed        51.9% of your procedural instructions are verifiable
                                 (above the 11.1% public median).
  +  Resume after a break       all 1 promised artifacts exist.
  ?  Follow your own rules      COULD NOT CHECK - the history replay returned no
                                 verdict (no git history here, or a shallow clone).
  --------------------------------------------------------------------------
  4 of 5 ready.  1 could NOT be checked - that is not a pass.
```

`exit 3` -- honest, by contract: one check genuinely could not run, so the report
says so instead of rounding up to "5 of 5."

Known kibsu limitation, filed as [kibsu#2](https://github.com/M-Bajalan/kibsu/issues/2) --
existence-mode history backtesting scopes "touched" files to the index file's own directory
rather than `docs_root`/`skills_dir`, which breaks even on kibsu's own default config shape
(this repo's `.kibsu.json` hits it too). Full reproduction and the issue write-up are at
`docs/upstream-issue-draft.md`.

```
python -m kibsu audit .
```

```
  genre        units    instr    check   CHECK%   0-check
  procedure        3       27       14    51.9%      0/3
  doctrine         1        7        0     0.0%      1/1
  --------------------------------------------------------
  ALL              4       34       14    41.2%      1/4

  >> HEADLINE (procedure units only - the fair comparison): 51.9% checkable
  genre declared in frontmatter: 4 unit(s), 0 disagreeing with detection
```

`skills/doctrine` scoring 0% is correct, not a defect -- see `skills/doctrine/SKILL.md`.

### Cold-start drill (manual check, not automatable by kibsu itself)

A fresh agent with zero prior context, given only this repo and told to read `AGENTS.md`
first, should be able to state the project's current state and name the single most
concrete next task -- without exploring blind. Run against a genuinely fresh clone:

- **10 tool calls.** Read `AGENTS.md` -> `docs/STATE.md` -> `tasks/T3_resume_the_work.md`,
  in that order -- the exact pointer chain `AGENTS.md` promises. Correctly named **T3** as
  the most concrete next task, with the right verify command
  (`python tools/check_task.py T3`) and the right marker commit.
- **Control:** the same drill against a copy with `AGENTS.md` and `docs/` removed took
  **26 tool calls** (2.6x) and landed on a *different*, less-grounded answer (T2, since T3
  needs git history that copy doesn't have) -- it had to fall back to running the checkers
  directly to reconstruct ground truth, and flagged the mismatch itself. That contrast --
  cheap and correct with the bootstrap doc, expensive and degraded without it -- is what
  this drill is actually testing, and it held.

**Verdict: PASS.**

## Design

Full build contract (locked decisions, phase-by-phase accept criteria):
`Kibsu_Lab_v1_Design_2026-07-27.md` (in the design's own workspace, not this repo --
this repo is the built artifact, not the design doc).

## License

MIT. See `LICENSE`. Every name and every row of data here is fictional -- see
`PROVENANCE.md`.
