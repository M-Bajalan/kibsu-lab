# Changelog

kibsu-lab practices its own log chain from birth (`skills/change-log/SKILL.md`) --
every phase of this repository's own build is logged here, newest first, the same
way a task's fix would be.

## [2026-07-27 22:15] - L3: state registry, changelog, and the planted learning
### Added
- `docs/STATE.md` -- the project-state registry (DATA / REPORTING / RECONCILIATION / TASKS)
- `docs/CHANGELOG.md` -- this file, seeded with the build's own history
- `docs/memory/learnings/reconciliation-check-batches-first.md` -- the planted
  learning: check batch duplication first, before chasing join logic

## [2026-07-27 22:00] - L2: skill team ported (change-log, gate, planner, doctrine)
### Added
- `skills/change-log/SKILL.md` -- the log chain, generalized from the origin
  workspace's post-change discipline
- `skills/gate/SKILL.md` -- the reversibility rule and this repo's concrete
  checkers (`tools/reconcile.py`, `tools/check_task.py`)
- `skills/planner/SKILL.md` -- phased plans with a named verify command per phase
- `skills/doctrine/SKILL.md` -- how to think here; declared `genre: doctrine`,
  intentionally near-zero checkable

## [2026-07-27 21:45] - L1: kibsu wired in from PyPI
### Added
- `.kibsu.json` gates entry: `tools/reconcile.py` as a commit gate, with its
  documented `cannot_run_exit`
- `.github/workflows/lab-ci.yml` -- generates data, runs the P1 selftest, then
  `python -m kibsu index .` / `report .` / `check .` against the released package
### Why
- The lab is kibsu's first real deployment -- its CI dogfoods the PyPI package,
  not the origin source tree.

## [2026-07-27 16:04] - L0: scaffold and seeded data generator
### Added
- Repository skeleton per the design contract (`README.md`, `AGENTS.md`,
  `PROVENANCE.md`, `LICENSE`, `.kibsu.json`, `.gitignore`)
- `tools/generate_data.py` -- seeded, stdlib-only, byte-deterministic generator
  for Tuppi Trading Co.'s fictional distribution data, with three planted
  defects (P1 double-loaded batch, P2 orphan products, P3 reporting gap)
- `tools/check_task.py --selftest` -- proves P1 is present in generated data
