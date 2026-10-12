---
type: learning
---

# Before you fix a command that never ran, find out what it does when it runs

`skills/gate/SKILL.md` named three commands with a trailing dot -- `kibsu gate --check .`,
`--status .`, `--baseline .` -- and kibsu rejected all three with exit 2, `unrecognized
arguments: .`. The recorded defect was "drop the dot". That fix was right for two of them
and would have been harmful for the third.

Without the dot, `python -m kibsu gate --baseline` does not show the accepted baseline. It
**rewrites** `.kibsu/gate_baseline.json` to accept whatever the configured gates report
right now. And the skill pointed to it at the worst possible moment: when
`tools/reconcile.py` has just exited 1 and the agent must decide whether the mismatch is
pre-existing or new ("see `python -m kibsu gate --baseline .`"). An agent following the
corrected sentence would have turned a new mismatch into an accepted one with a single
command, and `kibsu gate --check` would have passed afterwards.

The typo had been holding that door shut since the skill was written.

**Check this first, before reviving any command a document names and that has never run:**

```
git status --porcelain
<the command, in a throwaway clone>
git status --porcelain
```

If the second status differs from the first, the command writes, and the sentence around it
has to say so -- or point somewhere else. Here the read-only answer already existed:

```
python -m kibsu gate --check
```

Exit 0 = everything the gates report is already in the accepted baseline. Exit 1 = something
is new, and the output names it.

Two more things this taught:

- **A wrong command and a wrong sentence are different defects.** The dot was a typo. The
  word "see" in front of a command that writes was a misunderstanding of the tool, and it
  would have survived the typo fix.
- **The score never saw any of it.** kibsu counted both broken sentences as checkable,
  because a command was named; it counts the corrected ones the same way, and it counts
  the new warning ("never run ... to settle the question") as checkable too, because a
  prohibition also names a command. A number that cannot tell a working command from a
  dead one, or an instruction from a prohibition, is not evidence about either. Run the
  command.
