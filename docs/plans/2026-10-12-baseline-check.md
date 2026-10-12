---
type: plan
---

# Plan: a check that README's Baseline equals what kibsu prints

**Goal:** `README.md`'s Baseline block cannot go stale silently any more -- one command
compares it with the tool's output, CI runs that command with the pinned kibsu and with
whatever the Quickstart installs today, and a daily run catches a new kibsu release.
**Verifier:** `python tools/check_baseline.py` -> exit 0 on the finished change, and exit 1
whenever the block and the tool disagree.

Why it is needed: the block went stale twice (kibsu 0.1.0 -> 0.9.0 over ten weeks, then
0.9.0 -> 0.10.0 within minutes of a release) while CI stayed green on its pin both times.
`docs/STATE.md`'s TOOLING row has carried this as its open item since 2026-10-11.

## Phase 1: the checker, and its first real run must FAIL

- [x] `tools/check_baseline.py` -- rebuild the index, run `kibsu report .` and
      `kibsu audit .`, compare with both README blocks; exit 0 / 1 / 2.
- [x] `--selftest` -- prove the comparison can fail without needing kibsu at all.
- [x] The version is stated in three places (README heading, Quickstart install line, CI
      pin); the checker fails when they disagree.

**Verify:** `python tools/check_baseline.py --selftest` -> expected exit 0
**Verify:** `python tools/check_baseline.py` -> expected exit **1**, naming `17 docs` against
`18 docs`. This plan file is the eighteenth document under `docs/`, so the README is already
wrong by the time the checker exists. A first run that passes here would mean the checker
cannot see the one defect known to be present.

**What happened (recorded, not tidied):** the selftest exited 0. The first real run exited
**0, not 1** -- the prediction above was wrong. Cause: kibsu's index reads `git ls-files`, and
this plan file was not yet added to git, so the tool still counted seventeen. After
`git add docs/plans/2026-10-12-baseline-check.md` the same command exited 1 on line 4,
`17 docs` against `18 docs`, as predicted. The checker was not softened; it gained a note
that names untracked Markdown files, and the lesson went to
`docs/memory/learnings/untracked-docs-are-invisible-to-the-index.md` -- which is a
nineteenth document, so the block to re-capture in Phase 2 reads `19 docs`, not 18.

## Phase 2: re-capture the block

- [x] `README.md` Baseline -- the report block's first line: `17 docs` -> the count the tool
      prints once every new file is known to git (19, per the note above).

**Verify:** `python tools/check_baseline.py` -> expected exit 1 before the edit (17 against
19), expected exit 0 after it, with no "not tracked by git" note in the output.

## Phase 3: wire it into CI

- [x] `.github/workflows/lab-ci.yml`, job `lab-ci` (pinned kibsu) -- run the selftest, then
      the check.
- [x] New job `quickstart-as-written` -- install kibsu with the README's own install line
      (`python tools/check_baseline.py --install-spec`), then the Quickstart, then the check.
- [x] Triggers: a daily schedule and a manual run, besides push and pull request.

**Verify:** `python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/lab-ci.yml', encoding='utf-8'))"` -> expected exit 0
**Not machine-checkable from a clone:** whether the two jobs really run and pass on GitHub.
The proof is the workflow's first run on the pull request, and it needs a human read.

## Phase 4: the checker catches what it was built for

- [x] Run it under kibsu 0.9.0, the version the page was stale against one day ago.

**Verify:** `python tools/check_baseline.py` with kibsu 0.9.0 installed -> expected exit 1,
and the output names both versions.

## Phase 5: record it

- [x] `README.md` -- say next to the block how it is kept honest.
- [x] `AGENTS.md` -- one pointer, so an agent who adds a doc knows the block moves.
- [x] `docs/STATE.md` TOOLING row -- the open item is closed; the next action changes.
- [x] `docs/CHANGELOG.md` -- the entry.

**Verify:** `python tools/check_baseline.py` -> expected exit 0
**Verify:** `python -m kibsu check .` -> expected exit 0
**Verify:** `python -m kibsu audit .` still prints `45` instructions and `57.8%` for procedure
-- no skill file is touched by this plan, so no audit figure may move.
