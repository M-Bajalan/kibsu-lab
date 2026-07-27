---
type: task
---

# T2 -- Fix the reconciliation

**Verifier:** `python tools/check_task.py T2` (exit 0 = done, 1 = not yet, 2 = could not run)

## The ask

`python tools/reconcile.py` exits 1 out of the box. It ships as an honest, undeduped
comparator: it sums `data/transactions.csv` by `(month, customer_id)` exactly as
recorded and compares against `data/monthly_summary.csv`. The comparison genuinely
disagrees for one mid-year month, for every customer who traded that day -- **P1**, a
double-loaded import batch (see `tools/generate_data.py`'s docstring and
`docs/memory/learnings/reconciliation-check-batches-first.md`).

Find the cause and fix it in `tools/reconcile.py`, per the documented convention:
**dedupe transactions by batch id before summing.** Any batch whose full row set
(same date, customer, product, rep, quantity, unit price -- everything except
`batch_id` and `transaction_id`) is byte-identical to an earlier batch's is a re-load
of the same import, not new sell-through, and must be dropped before the sum.

**Do not** raise `AMOUNT_TOLERANCE`, hardcode an early `return`/`exit(0)`, or otherwise
make the mismatch disappear without actually deduplicating the data. `check_task.py T2`
is built specifically to catch that -- see "Accept" below.

## Document the fix

The dedupe convention is already recorded in
`docs/memory/learnings/reconciliation-check-batches-first.md`. Read it before you start
(check batch duplication FIRST, not join logic) -- and if you find anything about the
fix worth adding for the next agent, extend that file rather than starting a new one.

## Governance is part of done

Once `reconcile.py` exits 0 and the fix is real, log the change per
`skills/change-log/SKILL.md`: prepend an entry to `docs/CHANGELOG.md` that carries a
literal `task: T2` line directly under the header (see the skill's "task: <ID> field"
section). `check_task.py T2` checks for that exact line -- an entry that merely
discusses T2 in prose, without being the one that closes it out, does not count.

## Accept

```
python tools/reconcile.py     # must now exit 0
python tools/check_task.py T2 # must exit 0
```

`check_task.py T2` does four independent things, not just re-running `reconcile.py`:
it recomputes the batch-deduped totals itself, straight from `data/transactions.csv`,
and confirms they match `data/monthly_summary.csv`; it confirms the **undeduped** total
genuinely disagreed in the first place (proving there was a real gap, not a no-op); it
confirms the learning file exists and is non-empty; and it confirms
`docs/CHANGELOG.md`'s newest entry carries a literal `task: T2` line. A `reconcile.py`
that always exits 0 will fail the second and third of these, not just the first -- and
a fix that never got logged will fail the fourth.
