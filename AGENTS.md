---
type: agents
status: active
---

# AGENTS.md

You're a fresh agent in **kibsu-lab** -- a public, cloneable virtual workspace for
one fictional distribution company, **Tuppi Trading Co.** This file is thin on
purpose: it points, it doesn't restate. Read in this order.

## 1. How to think here

`skills/doctrine/SKILL.md` -- judgment, not procedure. Read it before you act on
anything ambiguous.

## 2. What is true right now

`docs/STATE.md` -- one row per track (DATA / REPORTING / RECONCILIATION / TASKS),
each with a `Next action`. This is the current state; it is not history.

## 3. What has already happened

`docs/CHANGELOG.md` -- newest entry first. `docs/memory/learnings/` -- reusable
lessons from past fixes; read before you re-derive something that's already known.

## 4. What you can be asked to do

`tasks/` -- three machine-checkable tasks (`T1_add_kpi.md`, `T2_fix_reconciliation.md`,
`T3_resume_the_work.md`). Each names its own verifier under `tools/check_task.py`.
Run the verifier before and after your change -- it will exit non-zero on a
pristine repo by design; that is the starting state, not a broken checker.

## 5. How work gets logged and gated

`skills/change-log/SKILL.md` (what to write, where, when you finish something) and
`skills/gate/SKILL.md` (what needs a green check before you commit). For anything
spanning 3+ steps, `skills/planner/SKILL.md`.

## 6. The data

`data/` does not exist until you generate it -- it is gitignored on purpose; the
shipped artifact is the generator, never its output:

```
python tools/generate_data.py
```

Every tool in this repo (`tools/reconcile.py`, `tools/sales_report.py`,
`tools/check_task.py`) generates `data/` itself with the default seed if it's
missing, so you never have to run this by hand first -- but running it explicitly
is fine too.

## 7. Tooling config

`.kibsu.json` -- docs root, skills dir, and the commit gate wired to
`tools/reconcile.py`. This repo depends on the `kibsu` package (PyPI) to read its
own governance; see `README.md` for the version pin.

## Provenance

`PROVENANCE.md` -- every name, company, and row of data here is fictional and
generated, never committed, never sourced from anything real.
