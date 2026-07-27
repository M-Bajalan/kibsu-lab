---
type: drill
genre: reference
---

# Cold-start drill: protocol and results

This is a manual check -- kibsu cannot automate it, because it measures how a fresh agent
session actually behaves, not a property of a file on disk. `README.md`'s "Cold-start drill"
section points here rather than publishing numbers itself, on purpose (see "Why this file, not
the README" below).

## Protocol

Two fresh agent sessions, no prior context beyond what each is handed, one arm each:

- **Arm A** -- a genuinely fresh clone of this repo: full git history, `docs/` intact,
  `AGENTS.md` intact. Told to read `AGENTS.md` first and go from there.
- **Arm B (control)** -- a copy of the same clone with `docs/` and `.git` stripped;
  `AGENTS.md` retained. Same starting instruction.

Both arms are asked the same two questions: what is the project's current state, and what is
the single most concrete next task?

## Results (2026-07-28, real run)

**Arm A -- PASSED, grounded.** Followed the pointer chain `AGENTS.md` promises into
`docs/STATE.md`, read all four state tracks (DATA / REPORTING / RECONCILIATION / TASKS),
correctly identified T3 as a continuation to resume rather than a fresh restart, and made no
changes to the repo while doing it.

**Arm B -- could not ground state, and said so.** With `docs/` absent, there is no
`docs/STATE.md` to read -- this is a structural fact of the control copy, not a reasoning
failure, and the arm reported the gap honestly instead of guessing at a coherent state it had
no way to actually know. It partially reconstructed an intended next action by reading the
`tasks/*.md` briefs directly, since that was the only task-shaped information left available to
it.

## Protocol disclosures

Named here because a drill that hides its own rough edges is exactly the failure this repo
exists to catch:

- **Self-identification contamination.** The control copy used for this run still contained
  the *old* `README.md` text -- the one this very change replaces -- which described specific
  fabricated drill results. An agent running in that control copy could, in principle, have
  read its own "expected" answer straight out of the README instead of reasoning about the
  stripped repo in front of it. This round's fix removes that risk going forward on two levels:
  the fabricated text is gone, and the real results now live in `docs/drill.md`, which controls
  strip along with the rest of `docs/` -- so a future control copy carries no version of this
  file to read at all.
- **Mount leak.** The way the control copy was mounted exposed the sibling folder's real name
  (this repo's own folder name, distinct from the control's path). It did not appear to change
  either arm's answer, but it is a context leak worth naming rather than quietly ignoring.

## Why this file, not the README

Control copies strip `docs/` **by design** -- that is the whole mechanism that makes Arm B a
fair test of what a doc-less agent can and can't ground. Publishing this drill's protocol and
results inside `docs/` means the information architecture itself is the fix: as long as future
controls keep stripping `docs/`, this file cannot leak into a future control the way the old
README text just did. Putting the results anywhere outside `docs/` -- the README included --
would have reintroduced exactly that risk.
