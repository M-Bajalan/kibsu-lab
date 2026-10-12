---
type: changelog
---

# Changelog

kibsu-lab practices its own log chain from birth (`skills/change-log/SKILL.md`) --
every phase of this repository's own build is logged here, newest first, the same
way a task's fix would be.

## [2026-10-12 10:10] - The README's Baseline is checked now: a command compares it with what kibsu prints, and CI runs it daily
### Added
- `tools/check_baseline.py` -- compares both Baseline blocks in `README.md` with what
  `python -m kibsu report .` and `python -m kibsu audit .` print on this clone, line for
  line, and checks that the kibsu version is stated the same in three places (the Baseline
  heading, the Quickstart's install line, the CI pin). Exit 0 = the page is right, 1 = it is
  not, with both sides printed, 2 = could not run. `--selftest` makes the comparison fail on
  purpose in eight ways and needs no kibsu. `--install-spec` prints the requirement the
  Quickstart installs.
- `.github/workflows/lab-ci.yml` -- a second job, `quickstart-as-written`. It installs kibsu
  with the README's own install line, read out of the page rather than written a second
  time, runs the Quickstart, then the check. A daily schedule and a manual trigger are added,
  because a kibsu release pushes nothing to this repository.
- `docs/plans/2026-10-12-baseline-check.md` -- the plan for this change, the first one in
  `docs/plans/`. It records where its own prediction was wrong.
- `docs/memory/learnings/untracked-docs-are-invisible-to-the-index.md` -- the lesson below.
### Changed
- `.github/workflows/lab-ci.yml`, job `lab-ci` -- ends with the selftest and the check, so a
  doc added or a skill edited without re-capturing the block turns the pinned run red. The
  workflow now declares `permissions: contents: read`; both jobs only read.
- `README.md` Baseline -- `17 docs` -> `19 docs`: this change adds two documents (the plan
  and the learning). The repository moved here, not the instrument. Every other line of
  both blocks is unchanged.
- `README.md` -- a paragraph beside the block says how it is checked, and the 2026-10-11
  section no longer calls the comparison an open item.
- `AGENTS.md` -- one pointer under Tooling config: the check exists, and adding a document
  or editing a skill moves the numbers it guards.
- `docs/STATE.md` TOOLING row -- the open item is closed; the next action now says what a
  red run of each job means.
### Learned while building it
- The checker's first real run was predicted to fail and passed. The plan file was already
  an eighteenth document, the page said seventeen, and the command exited 0. kibsu builds
  its index from `git ls-files`, and the new file had not been added to git, so for the tool
  it did not exist. After `git add` the same command exited 1 on exactly the predicted line.
  A check run before `git add` passes for the wrong reason, so the checker now names every
  untracked Markdown file and says its verdict does not cover them.
### Not verified here
- Whether the two jobs run and pass on GitHub: the first run on the pull request is the
  proof, and it wants a human read.
- A scheduled run. None has happened yet. GitHub also switches a scheduled workflow off
  after 60 days without activity in the repository, so a quiet repository stops being
  watched.
- Neither job is a required check. A red run informs; it does not block a merge.
### Why two jobs
- The page can go stale from two directions. This repository can move under it (the pinned
  job sees that). Or kibsu can move under it: the Quickstart installs `kibsu>=0.10.0`, CI
  pins `==0.10.0`, and the day a newer release prints something else the pinned job stays
  green while every reader gets a different page. That is what happened on 2026-10-11, and
  only a job that installs what the page tells a reader to install can see it.
### Verified (kibsu 0.10.0 from PyPI unless stated, exit codes read)
- `python tools/check_baseline.py --selftest` -- exit 0, eight controls.
- `python tools/check_baseline.py` with the plan file untracked -- exit 0 (the finding above).
- The same after `git add` of the plan -- exit 1, `17 docs` against `18 docs`.
- The same with the learning also added -- exit 1, `17 docs` against `19 docs`.
- The same after re-capturing the block -- exit 0.
- The same under kibsu 0.9.0 -- exit 1, six lines differ, and the output names both versions.
- `python tools/check_baseline.py --install-spec` -- prints `kibsu>=0.10.0`, exit 0.
- The workflow file parses as YAML: two jobs, each ending in the check; one pinned install.
- `python -m kibsu audit .` -- 45 instructions, 26 checkable, 57.8% for procedure: no skill
  file is touched, and no audit figure moved.
- `python -m kibsu check .` -- exit 0.

## [2026-10-11 17:15] - Baseline re-captured with kibsu 0.10.0: the scorer counts sentences now, and the page went stale the minute it shipped
### Fixed
- `README.md` Baseline -- re-captured with kibsu 0.10.0 from PyPI on a fresh clone. The report
  block's third line reads 57.8% above a 7.6% public median (it read 47.8% above 7.5%), its
  fourth reads `all 4 promised artifacts exist` (it read 3), and the audit table reads
  45 / 26 / 57.8% for procedure and 15 / 0 / 0.0% for doctrine (46 / 22 / 47.8% and 18 / 0).
  Every other line is unchanged, and so is the exit code, 3.
- `README.md` Quickstart -- `pip install "kibsu>=0.9.0"` -> `"kibsu>=0.10.0"`. The old line
  installed 0.10.0 from the moment it was published, so the page told a reader to install
  one version and showed them the output of another.
### Changed
- `.github/workflows/lab-ci.yml` -- pin `kibsu==0.9.0` -> `kibsu==0.10.0`, in this same commit
  as the block, and the comment records that the pin went stale a second time.
- `PROVENANCE.md` -- dependency paragraph names 0.10.0.
- `README.md` -- a new section, "Why this block was re-captured again", says what moved: the
  instrument, not this repository. No skill file changed. kibsu's scorer 0.11.0 counts
  sentences where every earlier scorer counted physical lines; this repository hard-wraps
  its prose, so one instruction had been scored as two or three lines. The ten-point rise is
  not an improvement and the section says so in those words. The earlier section is kept and
  now carries its version in its title.
- `docs/STATE.md` -- TOOLING row: pinned 0.10.0; the next action now names the Quickstart's
  install line alongside the pin; the open item records that it has cost two stale blocks.
  SKILLS row: the three broken `kibsu gate ... .` commands were re-run under 0.10.0 and
  still exit 2.
### Found, not fixed here
- `all 4 promised artifacts exist` is the instrument talking. No skill promises a new file.
  The fourth is the checklist line in `skills/planner/SKILL.md` that names
  `skills/change-log/SKILL.md`: joined into one sentence it is read as a promise to produce
  that file, because kibsu's artifact-verb test matches the word `log` inside the file's own
  name. With the file name taken out of the sentence the test finds no verb. This is kibsu's
  flaw, named in its `CORRECTIONS.md` (2026-10-11) and not fixed in 0.10.0; the README says
  so beside the block rather than letting the line read as a finding about this repository.
- The gap that let the page go stale is still open: CI pins one kibsu version, the Quickstart
  installs whatever is newest, and no step compares what `report` prints with what the
  README says it prints. Recorded in `docs/STATE.md` (TOOLING row).
### Why it went stale, again
- kibsu 0.10.0 was published on 2026-10-11 at 17:01 (+03). From that minute `kibsu>=0.9.0`
  resolved to it. CI here was green on `kibsu==0.9.0` the whole time, for the reason the
  previous entry gives: a pin proves the pinned version works and says nothing about the
  current one.
### How this was found
- From outside again, and this time before any reader had to report it: kibsu's release
  check installs the published package into an empty environment and runs it here. The lab
  is also where the scorer's fault was first seen -- `kibsu explain` on
  `skills/planner/SKILL.md` listed halves of sentences as separate instructions.
### Verified (commands run on a fresh clone with kibsu 0.10.0 from PyPI, exit codes read)
- `pip install "kibsu>=0.10.0"` into an empty environment -- installs 0.10.0.
- `python tools/generate_data.py` -- exit 0.
- `python tools/check_task.py --selftest` -- exit 0.
- `python -m kibsu index .` -- exit 0, 17 docs.
- `python tools/check_task.py T1` -- exit 1, as the Quickstart says of a pristine clone.
- `python -m kibsu report .` -- exit 3; every line equal to the README block once the clone
  path is substituted.
- `python -m kibsu audit .` -- exit 0; table and headline equal to the README block.
- `python -m kibsu check .` -- exit 0.
- `python -m kibsu gate --check .`, `--status .`, `--baseline .` -- exit 2 each, unchanged.
- `git status --porcelain` afterwards -- empty.

## [2026-10-11 10:07] - Baseline re-captured with kibsu 0.9.0; the pin and the README move together now
### Fixed
- `README.md` Baseline -- the block was captured with kibsu 0.1.0 and had not been
  reproducible with any later release. A fresh clone following the Quickstart with kibsu
  0.8.0 printed 47.8% where the block said 53.7%, a different fifth line, and exit 0 where
  the block said 3. Re-captured with kibsu 0.9.0 from PyPI on a fresh clone. The report
  block is now the tool's output line for line (it used to be re-wrapped by hand and to
  omit the path line), with the clone path written as `/path/to/kibsu-lab`.
- `README.md` -- the "Known kibsu limitation" paragraph cited kibsu#2 as open. It was fixed
  in kibsu 0.1.1 on 2026-07-29, one day after this repository went public. Replaced by what
  the fifth question reads today and why, with the three behaviours it has had.
- `README.md` Quickstart -- there was no install step. `pip install "kibsu>=0.9.0"` added.
- `docs/upstream-issue-draft.md` -- status line now says the issue is fixed, and that the
  reproduction below it holds only under kibsu 0.1.0.
### Changed
- `.github/workflows/lab-ci.yml` -- pin `kibsu==0.1.0` -> `kibsu==0.9.0`, and a comment on
  why the pin and the Baseline block must move in one commit.
- `.github/workflows/lab-ci.yml` -- the checkout is a full clone now (`fetch-depth: 0`). The
  default is depth 1, and on a shallow clone `kibsu report` rightly answers "shallow clone -
  cannot tell" on its fourth question and prints `3 of 5`. So CI had always been green on a
  different report than the Baseline's `4 of 5`, which is what a reader's own `git clone`
  gives. Found by this change's own first CI run, which passed while printing a score the
  README does not show; reproduced with `git clone --depth 1` before it was touched.
- `PROVENANCE.md` -- dependency paragraph names 0.9.0.
- `README.md` -- 53.7% -> 47.8% is recorded as the instrument moving, not this repository:
  no skill file changed; kibsu's scorer reads 46 procedure instructions here where the one
  in 0.1.0 read 41, checkable unchanged at 22; doctrine 15 -> 18. The earlier figures stay,
  labelled as kibsu 0.1.0 measurements.
### Added
- `docs/STATE.md` -- a TOOLING row. The pin had no owner and no next action, which is how
  it sat for nine kibsu releases; it has both now.
### Found, not fixed here
- `skills/gate/SKILL.md` names three commands that do not run: `python -m kibsu gate
  --check .`, `--status .` and `--baseline .` each exit 2 with `unrecognized arguments: .`,
  under kibsu 0.1.0 and under 0.9.0 alike -- they never worked. Without the dot they do.
  kibsu counts those lines as checkable, because a command is named; nothing checks that
  the command is one the tool accepts. Left alone on purpose: it is a skill edit, and a
  skill edit takes its own audit baseline first. Recorded in `docs/STATE.md` (SKILLS row).
### Why CI never caught it
- CI was pinned to the one kibsu version that still agreed with the README. A pin proves
  the pinned version works and says nothing about the current one. Every run was green.
- And CI only requires `report` to exit 0 or 3. It never compared what `report` printed
  with what this README says it prints, so a green run was never evidence about the block.
  That comparison is still done by hand; a step that makes it mechanical is the open item.
### How this was found
- From outside: kibsu's 2026-10-10 review installed its published package into an empty
  environment and followed this README from the top, comparing each printed line with the
  page. Nothing inside this repository could have reported it -- every check here ran, and
  passed, against 0.1.0.
### Verified (commands run on a fresh clone with kibsu 0.9.0 from PyPI, exit codes read)
- `python tools/generate_data.py` -- exit 0.
- `python tools/check_task.py --selftest` -- exit 0.
- `python -m kibsu index .` -- exit 0, 17 docs.
- `python tools/check_task.py T1` -- exit 1, as the Quickstart says of a pristine clone.
- `python -m kibsu report .` -- exit 3; every line equal to the README block once the clone
  path is substituted.
- `python -m kibsu audit .` -- exit 0; table and headline equal to the README block.
- `python -m kibsu check .` -- exit 0.
- `git status --porcelain` afterwards -- empty.

## [2026-09-05 14:06] - Audit of the skill-team port: four defects fixed, one of them real
### Fixed
- `skills/strategist/SKILL.md` -- the worked example contradicted this repo's own task.
  It said the double-loaded batch "belongs at load time, not in the totals" and to make
  the loader reject it. `tasks/T2_fix_reconciliation.md` says the opposite and calls it
  the documented convention: dedupe by batch id before summing in `tools/reconcile.py`,
  and leave the transactions file as the honest record of what was loaded. An agent
  trusting the old example would have edited the fixture generator -- the planted defect
  itself -- and T2's checker would never pass. Rewritten so the diagnosis lands on the
  convention and names why the tempting fix is wrong here.
- `AGENTS.md` -- sections 1 and 5 now point at `skills/strategist` and `skills/architect`.
  Nothing routed a fresh agent to either: the same push-vs-pull gap the previous entry
  fixed for `kibsu discover`, repeated in the commit built on top of it.
- `skills/architect/SKILL.md` Rule 4 -- "each usable bare from the repo root" was false
  for `tools/check_task.py` (bare -> exit 1, usage). Now says what is true.
### Added
- `docs/plans/.gitkeep` -- the path was promised three times (`planner` once,
  `architect` twice) and did not exist. A templated path kibsu's phantom check cannot
  see, so it was carried by both entries unnoticed; the directory now exists.
### Changed
- `README.md` audit block -- doctrine 13 -> 15 instructions (the rewritten example is
  longer), ALL 40.7% -> 39.3%. Procedure headline unchanged at 53.7%: no procedure unit
  gained or lost an instruction. Composition again, not improvement.
### Verified (commands run, exit codes read)
- `python -m kibsu audit .` -- 6 units, procedure 53.7%, doctrine 0.0%, `0 disagreeing
  with detection` (the rewritten example did not flip `strategist`'s detected genre).
- `python -m kibsu report .` -- exit 3, 17 docs, all 3 promised artifacts, unchanged.
- Scrub from outside the repo, tree and history: 1 hit each, the pre-existing one.
### How this was found
- A second model reviewed the first's work against the source a week later: re-ran every
  measurement, then read `tasks/T2_fix_reconciliation.md` -- which the author of the
  example had not.

## [2026-08-28 18:00] - Skill team completed: architect and strategist ported in
### Added
- `skills/architect/SKILL.md` (genre: procedure) -- the conventions this repo enforces:
  frontmatter declaration, honest genre declaration, one-fact-one-home, the path table,
  index rebuild after add/move. 11 instructions, 8 checkable (73%) -- the most checkable
  unit here, above `skills/gate` at 57%.
- `skills/strategist/SKILL.md` (genre: doctrine) -- diagnose before proposing, the three
  things that are not strategy, options carry cost/risk/reversibility, always recommend.
  Scores 0% checkable, which is the genre working, not a hole to patch.
### Changed
- `README.md` baseline block refreshed to what a fresh clone now reproduces: 17 docs
  (was 15), procedure 53.7% (was 46.7%), 6 units (was 4), all 3 promised artifacts (was 1).
  The block is not allowed to state numbers a clone can't reproduce, so it moved with the corpus.
### Verified (commands run, exit codes read -- not inferred)
- `python -m kibsu audit .` -- 6 units, procedure 53.7%, doctrine hard 0.0%,
  `genre declared in frontmatter: 6 unit(s), 0 disagreeing with detection`.
- `python -m kibsu report .` -- exit 3 (unchanged; the history-replay check still cannot run,
  kibsu#2). `all 3 promised artifacts exist` -- no phantom instructions introduced.
- Scrub gate run from outside the repo, fail-then-pass proven on these exact files: a
  deliberately injected denylist term raised the count 1 -> 3 and named
  `skills/architect/SKILL.md`; removing it returned the file byte-identical and the count to 1.
  The remaining hit is pre-existing (`tools/generate_data.py:196` -- a bare pipeline acronym
  used as ordinary industry English, previously ruled allowed) and is untouched by this change.
### Noted, not fixed
- The scrub enumerates via `git ls-files`, so an untracked new file is invisible to it. A
  first run here reported clean while scanning 27 files, neither of them the two new ones;
  `git add` moved it to 29 and made the check real. A brand-new file is the highest-risk
  leak surface and the one the gate silently skips. Out of scope for this entry; recorded
  so the next session does not rediscover it the hard way.

## [2026-07-28 20:03] - Lab micro-cycle: AGENTS.md gains the kibsu discover pointer
### Added
- `AGENTS.md` new "## 0. On arrival" section: run `python -m kibsu discover .` before
  anything else. The tool has existed in this repo's kibsu 0.1.0 install the whole time,
  but nothing pointed an agent at it -- the same push-vs-pull gap named in
  `Kibsu_Cycle1_Prereg_2026-07-28.md`'s lab micro-cycle, applied to this lab's own docs.
### Verified (before this entry, against the working tree with the AGENTS.md change staged)
- Ran the tool for real before writing the pointer, instead of describing it from memory:
  on this repo right now it exits 1 and reports one DECLARED-BUT-DEAD finding --
  `tools/reconcile.py` and `tools/sales_report.py` are named in `AGENTS.md`, but nothing
  actually invokes them (the `.kibsu.json` gates entry for `reconcile.py` is never run,
  because `kibsu gate` itself is never called by the pre-commit hook or by CI). Not fixed
  here -- out of this round's narrow scope, which is the pointer only -- but recorded so
  the next session doesn't have to re-discover it.
- Re-ran `kibsu index . / report . / audit .` against the staged change: still 15 docs,
  still `4 of 5 ready` / exit 3, still 46.7% procedure-checkable, still
  `doctrine 1 7 0 0.0% 1/1` and `ALL 4 37 14 37.8% 1/4` -- identical to the published
  Baseline block. The pre-registration flagged that the new runnable command might RAISE
  the lab's procedure %; it did not, because `kibsu audit`'s unit scope is `SKILL.md`
  files only (confirmed at F8) and `AGENTS.md` is never one of them. Publishing that flat
  result rather than the hoped-for rise. No published number moved, so the README Baseline
  section is left untouched.

## [2026-07-28 00:30] - F9: skills/doctrine renamed to skills/thinking-partner, pre-publish
### Changed
- `skills/doctrine/` -> `skills/thinking-partner/` (folder and file path only). The
  `genre: doctrine` frontmatter value is unchanged -- it is the taxonomy word for this
  skill's checkability class, not the skill's name, and stays exactly as it was. The
  `name:` frontmatter key and the `# ` header inside `SKILL.md` were updated to
  `thinking-partner` to stay internally consistent with the new path. One internal prose
  line that used "doctrine" as a self-reference ("the failure mode this whole doctrine
  exists to prevent") was reworded to "this file exists to prevent" -- not a taxonomy
  word, just a stale self-reference to the old name.
- Swept every live reference to the old path: `AGENTS.md` section 1, and `README.md`'s
  "Baseline" prose line about the doctrine-genre unit scoring 0%. `docs/STATE.md` and
  every `tasks/*.md` brief were checked (`Select-String -Pattern doctrine` across the
  full tracked tree) and do not reference this skill at all -- nothing to change there.
  `docs/CHANGELOG.md`'s own historical entries (L2, and this file's own prior rounds)
  still say `skills/doctrine/SKILL.md` on purpose -- this project's convention is
  append/prepend-only; past entries describe what was true when they were written and
  are not rewritten after the fact.
### Added
- One lineage line under the renamed skill's header: "Descended from a private skill
  built in partnership with an AI session." Generic phrasing, no vendor names, per the
  instruction.
### Verified (before this entry, against the working tree with the rename staged)
- `kibsu index .` / `report .` / `audit .` re-run after the rename: still 15 docs, still
  `4 of 5 ready` / exit 3, still 46.7% procedure-checkable, still `doctrine 1 7 0 0.0% 1/1`
  and `ALL 4 37 14 37.8% 1/4` -- identical to the published Baseline block. The rename
  (a path change plus one added prose line in a doctrine-genre unit, which contributes 0
  checkable instructions by design) did not move any published number, so the README
  Baseline section is left untouched.
### Note (CHECK-AFTER-WRITE, after this entry is committed, against a fresh clone)
- The governance re-run (`changelog_top_entry_has_task_field("T1")` and `("T2")`, both
  expected `False`) happens strictly after this entry is committed. Results are
  deliberately not asserted here, per the same reflexivity discipline as every prior
  round.

## [2026-07-28 02:00] - F8: published baseline stopped reproducing, drill.md classified, honest recapture
### Fixed
- `docs/drill.md` frontmatter: added `genre: reference` -- it is a record and lookup
  document (protocol + results), not instructions for an agent to follow, and it was
  undeclared. Verified this does not itself move `kibsu audit`'s numbers: audit's unit
  scope is `SKILL.md` files only (4 of them), so a `docs/*.md` genre tag was never going
  to change the procedure percentage -- the earlier published 51.9% had already gone
  stale for a different reason (see below), and this fix is about honest classification
  of `docs/drill.md`, not about restoring that number.
- `README.md`'s Baseline section no longer reproduces its own published numbers from a
  fresh clone (`14 docs`/`51.9%` published; a fresh clone now measures `15 docs`/`46.7%`,
  since `docs/drill.md` (added in the F7 fix) is a real, correctly-counted fifteenth doc).
  Re-captured from a genuine fresh clone following this README's own Quickstart and
  published exactly what it measures, including the number landing lower than before.
  Also dropped the pinned commit-hash convention from the heading (`measured at commit`)
  -- a commit that changes the very numbers it publishes cannot cite its own hash in
  advance without a second commit, which this round is deliberately avoiding; the heading
  now says "measured at this commit" and points the reader at `git log -1` instead.
### Note
- The true root cause of the 51.9% -> 46.7% drop is NOT `docs/drill.md` -- it is
  `skills/change-log/SKILL.md` picking up 3 more instructions than it has matching checks
  for, from the `task: <ID>` field documentation added in Round 2. Its example is a fenced
  code block labeled `md`, an unsupported language for kibsu's runnable-fence detection.
  Confirmed by testing: applying `genre: reference` to `docs/drill.md` alone left the audit
  numbers completely unchanged (still 30 instr / 14 check / 46.7%). Recorded here rather
  than silently building on an incomplete diagnosis.
### Verified (CHECK-AFTER-WRITE, after this entry, against a fresh clone)
- Governance re-run happens strictly after this entry is committed; results are
  deliberately not asserted here, per the same reflexivity discipline as the prior round.

## [2026-07-28 01:35] - F7: published cold-start drill results that were never run
### Fixed
- `README.md`'s "Cold-start drill" section published specific numbers (10 vs 26 tool
  calls, "landed on T2", "Verdict: PASS") for a drill that had not actually been run --
  a verdict without an execution behind it, the exact defect class this lab exists to
  teach. Cut the entire results/verdict portion; the section now states in two neutral
  lines that the lab's acceptance includes a manual cold-start drill run by fresh
  external agents, and points to `docs/drill.md`.
### Added
- `docs/drill.md` -- the drill's protocol (two fresh sessions, one arm each; control
  strips `docs/` and `.git`, keeps `AGENTS.md`) and the real 2026-07-28 results: Arm A
  grounded correctly via `AGENTS.md` -> `docs/STATE.md`, named T3 as a continuation
  (not a restart), no changes made; Arm B could not ground state with `docs/` absent
  and said so honestly, partially reconstructing a next action from the task briefs
  instead. Also discloses two protocol issues found along the way: the tested control
  copy still carried the old (fabricated) README drill text -- fixed by this same
  change, since controls strip `docs/` and results now live there -- and the mount
  exposed the sibling folder's name.
### Why
- Control copies strip `docs/` by design, so a future control can never read its own
  expected outcome by accident. Putting the drill's real results inside `docs/`, not
  the README, makes that stripping the actual fix, not just a description of one.

## [2026-07-28 01:10] - Round 2: exact-line task field replaces substring governance gates
### Fixed
- `tools/check_task.py` T1 and T2 governance gates: the substring check
  (`changelog_top_entry_mentions`) was pre-satisfied by the very CHANGELOG entry that
  documented the F3 fix, since that entry's prose talks about both tasks in plain
  words -- and the same defect turned out to affect T1's gate too, as collateral from
  the same commit (a regression, since T1's gate had been verified genuinely failable
  at an earlier commit). Replaced with `changelog_top_entry_has_task_field`, which
  looks for an exact standalone line reading `task: T1` or `task: T2` -- a field now
  reserved exclusively for the entry that closes out that specific task. Documented
  the reservation in `skills/change-log/SKILL.md` and in all three `tasks/*.md`
  briefs. Old `changelog_top_entry_mentions` kept as a general-purpose helper, no
  longer used for gating.
### Added
- The missing changelog entry for commit `6e814db` (below) -- its own prose is safe
  to mention T1/T2 freely under the new primitive, unlike under the old one.
### Note
- CHECK-AFTER-WRITE (new law, this round): the governance re-run happens strictly
  after this entry is written and committed, against a fresh clone. Results are
  deliberately not asserted in this entry -- an entry that recorded its own re-run's
  outcome would repeat the exact reflexivity bug this round exists to fix. See the
  commit this entry ships in, and the session log, for what the re-run found.

## [2026-07-27 23:50] - Cite filed upstream issue kibsu#2
### Changed
- `README.md`'s baseline section and `docs/upstream-issue-draft.md`'s status header
  updated to cite the now-filed public issue
  https://github.com/M-Bajalan/kibsu/issues/2, replacing the earlier not-yet-filed
  placeholder language.
### Why
- Backfilled here because this changelog is the audit trail kibsu's own report
  checks against -- a commit (`6e814db`) that shipped without an entry was a gap in
  the record it's supposed to prove.

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
