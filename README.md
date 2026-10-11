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
pip install "kibsu>=0.9.0"             # the only dependency -- everything else here is stdlib
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

## Baseline (after indexing; measured at this commit, kibsu 0.9.0 from PyPI)

Captured by literally running the Quickstart above, verbatim, against a fresh clone --
`git clone`, `pip install`, `generate_data.py`, `kibsu index .`, then the two commands below.
If your own run doesn't match this block, the difference is real and worth reporting -- this
block is not allowed to say anything a fresh clone can't reproduce by following this README's
own steps. (No commit hash is pinned here on purpose: a commit that changes the numbers below
cannot cite its own hash in advance. Run `git log -1 --oneline` on your clone to see which
commit you're reading this block from.)

The version in the heading is part of the claim. `.github/workflows/lab-ci.yml` pins the same
one, and the two move together -- see "Why this block was re-captured" below for what happened
when they did not.

```
python -m kibsu report .
```

```
  WHAT YOUR AGENTS CANNOT DO HERE YET
  /path/to/kibsu-lab
  --------------------------------------------------------------------------
  +  Find your docs             17 docs, index present.
  +  Know your conventions      consistent frontmatter (type) - enforceable.
  +  Prove they followed        47.8% of your procedural instructions are verifiable (above the 7.5% public median).
  +  Resume after a break       all 3 promised artifacts exist.
  ?  Follow your own rules      COULD NOT CHECK - .kibsu/index.json has never been committed (built locally, or gitignored), so there is no index history to replay.
                                reads only, writes nothing:  git -C /path/to/kibsu-lab log --oneline -- .kibsu/index.json
  --------------------------------------------------------------------------
  4 of 5 ready.  1 could NOT be checked - that is not a pass.
  Nothing was written to this repo - run `git status` to confirm.
```

That is the tool's own output, line for line, with one substitution: your clone's path
appears where `/path/to/kibsu-lab` is written (twice).

`exit 3` -- honest, by contract: one check genuinely could not run, so the report
says so instead of rounding up to "5 of 5."

The fifth question cannot be checked here because of a layout choice, not a defect: this
repository builds its index locally and gitignores it (the Quickstart's `kibsu index .`
step), so the index has no commit history for kibsu to replay.

```
python -m kibsu audit .
```

```
  genre        units    instr    check   CHECK%   0-check
  procedure        4       46       22    47.8%      0/4  
  doctrine         2       18        0     0.0%      2/2  
  --------------------------------------------------------
  ALL              6       64       22    34.4%      2/6  

  >> HEADLINE (procedure units only - the fair comparison): 47.8% checkable

  genre declared in frontmatter: 6 unit(s), 0 disagreeing with detection
```

(An excerpt: the table and the headline. The command prints a version banner above them and
the most claimable units below.)

### Why this block was re-captured (2026-10-11)

**53.7% became 47.8%, and that is the instrument moving, not this repository.** Not one skill
file changed between the two measurements. kibsu's scorer did: the one shipped in 0.1.0 read
41 procedure instructions here and the one in 0.9.0 (scorer 0.10.0) reads 46, with the
checkable count unchanged at 22; doctrine went from 15 instructions to 18. The ruler got
better at seeing instructions, and what it newly sees is mostly unverifiable -- the same
re-measurement lowered every public collection kibsu surveys, and the median this report
compares against came down with them, 11.1% to 7.5%. kibsu's own `CORRECTIONS.md` indexes
each round.

This block showed the 0.1.0 figures for ten weeks after they had stopped being reproducible,
and the reason is worth keeping. CI here pinned `kibsu==0.1.0`. A pin proves the pinned
version works and says nothing about the current one, so the workflow stayed green through
nine kibsu releases while a fresh clone with any of them printed something else. The fifth
line is the clearest case:

- **kibsu 0.1.0** printed `COULD NOT CHECK` for the wrong reason -- a scoping bug this lab
  found and filed as [kibsu#2](https://github.com/M-Bajalan/kibsu/issues/2), fixed in 0.1.1.
  The reproduction record is `docs/upstream-issue-draft.md`.
- **kibsu 0.1.1 through 0.8.0** printed an accusation instead: `x ... 6 of your last 200
  commits changed a doc without updating the index they claim to keep` -- every commit that
  ever added a doc, convicted against a file that was never committed, on a repository with
  twenty commits. That was kibsu's defect, not this repository's.
- **kibsu 0.9.0** abstains, and says why (kibsu `CORRECTIONS.md`, 2026-10-10 -- the round
  that found all of this by following this README as a stranger would).

The pin and this block now move together in one commit; `docs/STATE.md`'s TOOLING row carries
the next action.

### The earlier history, measured with kibsu 0.1.0

It stands and is not overwritten. **The rise from 46.7% to 53.7% was composition, not
improvement, and must not be read as one.** Two units were *added* (`skills/architect`,
`skills/strategist`); not one line of an existing skill was edited. `architect` happens to be
an unusually checkable unit, so the average moved -- which is the average doing arithmetic,
not this repository getting better at anything. Before that: 51.9%, then 46.7% once
`skills/change-log/SKILL.md` picked up 3 more instructions than it had matching checks for
(its `task: <ID>` example is a fenced block labeled `md`, an unsupported language for kibsu's
runnable-fence detection, so it reads as instruction text with nothing to check against it).
Each published number was true of the corpus it was measured on, under the instrument that
measured it.

Any future before/after that claims an *improvement* measures against a fresh baseline taken
at that moment, with the same kibsu version on both sides -- never against a number that a
corpus change or an instrument change moved.

`skills/thinking-partner` and `skills/strategist` scoring 0% is correct, not a defect -- both
declare `genre: doctrine`, and judgment guidance has nothing for a checker to check. Raising
either number would mean replacing judgment with ceremony. See each file's own closing note.
(Its `genre: doctrine` frontmatter value is the taxonomy word, unchanged by this rename -- see
the table above.)

### Cold-start drill (manual check, not automatable by kibsu itself)

The lab's acceptance includes a manual cold-start drill, run by fresh external agents.

Protocol and results: `docs/drill.md`.

## Design

Full build contract (locked decisions, phase-by-phase accept criteria):
`Kibsu_Lab_v1_Design_2026-07-27.md` (in the design's own workspace, not this repo --
this repo is the built artifact, not the design doc).

## License

MIT. See `LICENSE`. Every name and every row of data here is fictional -- see
`PROVENANCE.md`.
