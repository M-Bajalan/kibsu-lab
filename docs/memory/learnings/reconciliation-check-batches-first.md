---
type: learning
status: active
---

# Reconciliation mismatch: check batch duplication first

A sell-through mismatch between `data/transactions.csv` and
`data/monthly_summary.csv` was once chased for hours through join logic --
re-checking the product join, the customer join, whether a rep code was being
double-counted by some downstream aggregation. None of that was the cause.

The cause was a double-loaded import batch: one day's transactions had been
re-loaded verbatim under a second batch id, one batch later than the original --
the readable shape of a scheduler that re-ran, or a stale source file that got
picked up twice. Every join was correct. The raw data itself contained the same
rows counted twice.

**Check batch duplication FIRST, before anything else, whenever a reconciliation
disagrees:**

```
python -c "
import csv, sys
from collections import defaultdict
rows_by_batch = defaultdict(list)
with open('data/transactions.csv', newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        key = (row['txn_date'], row['customer_id'], row['product_id'], row['rep_id'], row['quantity'], row['unit_price'])
        rows_by_batch[row['batch_id']].append(key)
seen = {}
for b in sorted(rows_by_batch, key=int):
    sig = tuple(sorted(rows_by_batch[b]))
    if sig in seen:
        print('duplicate batch:', seen[sig], '->', b)
    seen[sig] = b
"
```

If that probe finds a hit, the fix is to dedupe by batch id before summing --
drop the later, re-loaded batch entirely, never average the two or widen a
tolerance to make the gap disappear. This is the exact shape of the fix
`tools/reconcile.py` needs for task T2 (`tasks/T2_fix_reconciliation.md`): find
the join bug you expect, rule it out fast, then check for a duplicated batch
before spending real time anywhere else.

This file is consulted, not just filed away -- `tools/check_task.py T2` checks
that it exists and is non-empty before it will pass T2 as done.
