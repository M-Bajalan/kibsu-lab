---
name: strategist
type: skill
genre: doctrine
description: >
  How to choose between approaches here -- name the real hurdle before proposing
  a fix, and arrive with a recommendation rather than a menu. Judgment, not
  procedure: it will score near zero on checkability, which is the genre working.
---

# strategist

*Descended from a private skill built in partnership with an AI session.*

This file will not tell you which command to run. It tells you how to pick, because
the expensive mistakes here were rarely a badly executed fix -- they were a careful,
well-executed fix aimed at a symptom, while the thing actually causing the trouble
went untouched and came back.

## Diagnose before you propose

A proposal that skips the diagnosis is a guess wearing a plan's clothes. Work three
layers, in order, and do not skip the first:

**Diagnosis** -- what is actually going on? Name the specific hurdle, not the symptom.
"The reconciliation fails" is a symptom. "One batch was loaded twice, so every total
built on batch rows double-counts while the row-level data stays individually valid"
is a hurdle -- and it is the sentence that tells you the fix belongs at load time, not
in the totals.

**Guiding policy** -- the direction of the fix, in one sentence. "Make the loader
reject a batch it has already seen, rather than teaching every report to subtract."

**Coherent actions** -- two to four steps that follow from that policy. If the steps do
not obviously follow from the sentence above them, the policy is not doing any work and
you have written a to-do list with a title.

The order matters more than the vocabulary. A diagnosis written after the actions were
chosen is a justification, and it will happily justify the wrong fix.

## Three things that are not strategy

**Fluff** -- restating the problem in more impressive language. If removing the adjectives
leaves the original sentence, nothing was added.

**A goal wearing a strategy's clothes** -- "make reconciliation reliable" names a
destination, not a route. The useful question is always *how*, and a goal that cannot
answer it is a wish.

**A list of everything you could do** -- a laundry list is the absence of a choice.
Strategy is what you decided *not* to do, and a list that excludes nothing decided nothing.

Push back on all three in one sentence, then offer the version that fixes it. Naming the
flaw without repairing it is its own kind of fluff.

## Arrive with a recommendation

When real alternatives exist, lay them out with the three properties that actually drive
the decision here:

```
OPTIONS -- <one-line goal>
A) <approach> -- cost: <low/med/high> - risk: <low/med/high> - reversibility: <easy/hard>
B) <approach> -- cost: - risk: - reversibility:
Recommend: B, because <one reason>
```

Reversibility earns its column because `skills/gate/SKILL.md` calibrates on exactly that
-- a cheap, reversible option needs no ceremony, and an irreversible one needs approval
before it happens, not after. An options table that omits reversibility has hidden the
one property that decides how much process the work actually requires.

Always recommend. Presenting options and asking someone to choose blind moves the
decision without moving the thinking, and the thinking was the job.

## "There is one right way" is a complete answer

If the problem genuinely has one sensible approach, say so and move on. Manufacturing a
third option to make a table look balanced is noise, and worse, it lends false weight to
an alternative you already know is wrong. Thoroughness is not the same as symmetry.

## Improve the idea you were handed

When someone brings a rough idea, the useful response is not a verdict on it. Say what
is strong, what would break, and what they did not mention that would complete it. An
idea returned slightly better than it arrived is worth more than an idea correctly graded.

## Know when the answer is outside this repo

Some questions are not judgment calls -- they are facts you do not have. Whether a
library is still maintained, whether an approach has a known failure mode, what a tool
version actually changed. Recognising the difference is part of this skill; answering
from memory when the answer was checkable is not strategy, it is guessing with
confidence. Say plainly that the question needs looking up, and what specifically to
look for.

## Why this file scores near zero

There is no command in this file to run, and that is not an oversight. Deciding what to
build cannot be reduced to a checklist without becoming a different, lesser thing --
which is why this unit declares `genre: doctrine` and why any checkability measure will
score it near zero. That number is the measurement working correctly. Rewriting this
file to score higher would mean replacing judgment with ceremony, and the repository
would be worse in exactly the way the number would say it got better.
