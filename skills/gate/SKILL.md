---
name: gate
type: skill
genre: procedure
description: >
  What may not happen without a green gate in this repository. Names the
  reversibility rule, the commands that check it, and the exact exit codes
  that mean pass/fail/could-not-run.
---

# gate

## The rule

Make a change reversible if you can. Gate it only if you can't. Before any change,
ask: can this be cheaply taken back? If yes, act and report -- no ceremony. If no,
name what you'll verify afterward, in one line, before you touch anything.

## What this repo already gates, mechanically

`python -m kibsu gate --check .` runs every command configured under `.kibsu.json`'s
`"gates"` key and blocks a commit only on a **NEW** violation -- never on the
pre-existing baseline. Check what's wired and whether it's live:

```
python -m kibsu gate --status .
```

Read `.kibsu.json` directly to see which commands are configured before assuming
none are. A repo with `"gates": []` has zero enforcement and `kibsu gate --check`
says so plainly -- that is an abstention, not a pass.

## Before any commit

```
python tools/reconcile.py
```

Exit 0 = clean. Exit 1 = a real reconciliation mismatch -- do not commit past it
silently; either it's a pre-existing accepted baseline violation (see
`python -m kibsu gate --baseline .`) or it's new and must be fixed first. Exit 2 =
could not run (data missing and could not be generated) -- this is
`tools/reconcile.py`'s documented `cannot_run_exit`; a gate wired with that value
skips the check rather than blocking, and says so on stderr.

## Task checkers are gates too

Before reporting any of T1/T2/T3 as done:

```
python tools/check_task.py T1
python tools/check_task.py T2
python tools/check_task.py T3
```

Exit 0 = verified done. Exit 1 = not done, or a claim of "done" that the checker
could not confirm from the repo -- treat exit 1 the same as a failing test, never as
a formality to route around. Exit 2 = the checker itself could not run.

## The one hard rule

No irreversible action -- an overwrite with no snapshot, a force-push, a delete with
no undo path -- without it being explicitly, just-in-time approved for exactly that
action. A plan is not approval. Presenting options is not approval.

## Verify from the source, not from your own report

After any change, re-run the check that names the invariant -- never just re-read the
diff you produced and conclude it worked. `git status` and `git diff` show what
changed; they do not prove the change is correct. The commands above do.

## Checklist before you say "done"

- [ ] Is the change reversible? If yes, did you act and report rather than seeking
      permission you didn't need?
- [ ] If irreversible, did you name the undo path (or state plainly "no undo exists")
      before acting?
- [ ] Did you run the relevant checker (`tools/reconcile.py`, `tools/check_task.py`)
      and read its **exit code**, not just its printed text?
- [ ] Did you log the change per `skills/change-log/SKILL.md`?
