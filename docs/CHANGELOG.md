---
type: changelog
---

# Changelog

kibsu-lab practices its own log chain from birth (`skills/change-log/SKILL.md`) --
every phase of this repository's own build is logged here, newest first, the same
way a task's fix would be.

## [2026-07-27 23:10] - L-GATE fixes: independent verifier findings (F1-F6)
### Fixed
- `tools/check_task.py` T2 (F3): the learning-file-exists check is permanently
  satisfied once the file is committed -- not a negative control, and its
  message claimed "consulted" when only existence is checked. Message softened
  to what is actually tested; added a `changelog_top_entry_mentions("T2")` gate
  mirroring T1's, proven live to be reachable-as-failure before this fix.
- `tools/check_task.py` T3 (F6): the on-`main` failure message said "this looks
  like a restart, not a continuation" -- reworded to the true state, that the
  continuation branch has not been checked out yet.
- `README.md` Quickstart (F1): the published baseline (`4 of 5 ready`) did not
  reproduce from the published Quickstart steps -- it was captured after
  `python -m kibsu index .`, which the Quickstart never told a reader to run.
  Added the index step to the Quickstart itself and relabeled the baseline
  section "after indexing"; re-captured from an actual fresh clone following
  the corrected steps, so the published block is reproducible again.
- `README.md` upstream claim (F2): "filed upstream" was asserted with no issue
  actually filed on the public kibsu repo. Replaced with a pointer to
  `docs/upstream-issue-draft.md` -- a prepared reproduction + proposed issue
  write-up, explicitly marked not-yet-filed, for a human to file and return the
  issue number.
### Changed
- Dropped constant `status: active` frontmatter (F4) from every doc except
  where a real lifecycle is demonstrated (currently none) -- it was 1 distinct
  value across all 13 docs while `type` had 8, and was propping up
  `Know your conventions` as an enforceable key it hadn't earned. `type` is
  unaffected (still 100% share, 13/13 docs).
### Confirmed no defect
- F5 (design doc's `install --apply`): already correct in this repo -- the
  real invocation used throughout (`install --install`, no `--apply`) matches
  the actual kibsu 0.1.0 CLI, which has no such flag on `install`.

## [2026-07-27 22:35] - L5: README/AGENTS/PROVENANCE made real, baseline recorded
### Changed
- `AGENTS.md`, `README.md`, `PROVENANCE.md` -- placeholders replaced with real
  content; `AGENTS.md` first (the cold-start drill runs on it alone)
- Added `type`/`status` frontmatter across all 13 tracked docs, including the 4
  skill files, so kibsu's own taxonomy promotes both keys to REQUIRED
### Added
- `README.md` baseline section: `kibsu report .` and `kibsu audit .` output,
  SHA-pinned to commit `db5a605`
### Verified (manual -- kibsu cannot automate this one)
- Cold-start drill: a zero-context agent given only `AGENTS.md` reached the
  right next task (T3) in 10 tool calls following the intended pointer chain;
  the same drill on an `AGENTS.md`/`docs/`-stripped control took 26 calls and
  landed on a different, less-grounded answer. PASS -- see README.md's
  "Cold-start drill" subsection for the full evidence.

## [2026-07-27 22:25] - L4: tasks + verifiers, T3 continuation branch
### Added
- `tools/check_task.py` T1/T2/T3 checkers -- each independently recomputes its
  answer rather than trusting the tool it's checking; all three exit 1 on this
  pristine repo (negative control)
- `tasks/T1_add_kpi.md`, `tasks/T2_fix_reconciliation.md`, `tasks/T3_resume_the_work.md`
- Branch `task/T1-in-progress` -- a real, half-done T1 commit merged with main's
  later history so `tasks/T3_resume_the_work.md`'s marker commit stays a genuine
  ancestor of the branch tip

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
