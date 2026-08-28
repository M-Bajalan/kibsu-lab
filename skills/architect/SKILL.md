---
name: architect
type: skill
genre: procedure
description: >
  The conventions this repository enforces: what every file must declare, where
  it belongs, and the commands that prove a new or moved file follows the rules
  before it lands. Run it whenever you add, move, or rename anything.
---

# architect

Conventions only survive if a command can check them. Everything below names the
command that proves it, because a rule nobody can verify is a preference, and a
preference decays into an argument the next time two agents disagree.

## Rule 1 -- every file declares what it is

Every document under `docs/` carries frontmatter with a `type:` field. Every skill
carries `name`, `type: skill`, and `genre:`. Nothing lands without its declaration.

```
python -m kibsu report .
```

The `Know your conventions` line reads `consistent frontmatter (type) - enforceable`
while this holds. If it says anything else, a file you added is missing its `type:`
-- find it before you commit, not after.

## Rule 2 -- declare the genre honestly

```
python -m kibsu audit .
```

Read the line `genre declared in frontmatter: N unit(s), 0 disagreeing with detection`.
**The `0` is the number that matters.** A non-zero count means a skill claims one genre
while its text reads as another.

A `doctrine` unit scoring near 0% checkable is correct and expected -- judgment guidance
has nothing to check. Relabelling a doctrine unit as `procedure` would raise the headline
number without changing a single instruction, which is the exact deception this repo's
tooling exists to catch. Declare what the file is; let the number land where it lands.

## Rule 3 -- one fact, one home

| The fact | Its only home |
|---|---|
| What is true right now | `docs/STATE.md` |
| What already happened | `docs/CHANGELOG.md` |
| A reusable lesson | `docs/memory/learnings/<slug>.md` |
| What a multi-step job will do | `docs/plans/<date>-<slug>.md` |
| Where roots and gates are wired | `.kibsu.json` |

Never open a second home for a fact that already has one. A duplicated fact does not
stay duplicated -- one copy gets updated, the other rots, and the next agent cannot tell
which one is lying. When you are tempted to restate something, link to it instead.

## Rule 4 -- where things belong

| Path | Holds |
|---|---|
| `docs/` | documents, each with `type:` frontmatter |
| `docs/plans/` | plan files (`skills/planner/SKILL.md`) |
| `docs/memory/learnings/` | one lesson per file |
| `skills/<name>/SKILL.md` | one skill per directory |
| `tools/` | runnable Python, each usable bare from the repo root |
| `tasks/` | task briefs graded by `tools/check_task.py` |
| `data/` | generated, never committed -- see `PROVENANCE.md` |

A file placed outside this table needs the table updated in the same commit, or it
needs to move. Do not leave the exception undocumented.

## Rule 5 -- rebuild the index after you add or move a file

The index is what lets an agent find your docs at all. It is gitignored, so it is
never carried in by a clone and never updated by anyone else's commit.

```
python -m kibsu index .
python -m kibsu report .
```

`report` reads `Find your docs` from that index. A file that exists but is not indexed
is invisible to every check that follows, so an index rebuild you skipped reads exactly
like a file you never wrote.

## Rule 6 -- when unsure, record more, not less

If you cannot decide whether a change is worth a CHANGELOG entry, write the entry. A
too-small entry is edited in seconds; a missing one is history nobody can reconstruct.
The same holds for a learning you are unsure is reusable -- the cost of writing it is a
minute, and the cost of re-deriving it is however long it took the first time.

## What counts as a change worth recording

A change is worth recording if it would confuse the next agent had it gone unrecorded.
Editing a tool, a skill, a task, or a config qualifies. Reading, auditing, or answering
a question does not -- but if the answer took real work to find, that answer is a
learning under Rule 3, not nothing.

## Checklist before you say "it follows the conventions"

- [ ] Does every file you added or edited carry its `type:` frontmatter (and `name` +
      `genre:` if it is a skill)?
- [ ] Did `python -m kibsu report .` still print `consistent frontmatter (type) - enforceable`?
- [ ] Did `python -m kibsu audit .` print `0 disagreeing with detection`?
- [ ] Is every fact you wrote in exactly one home, with links rather than copies?
- [ ] Is every file you added covered by the path table in Rule 4, or was the table updated?
- [ ] Did you re-run `python -m kibsu index .` after adding or moving a file?
- [ ] Did you log the change per `skills/change-log/SKILL.md`?
