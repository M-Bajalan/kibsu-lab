---
type: task
status: active
---

# T1 -- Add a KPI: rolling 3-month distributor share

**Verifier:** `python tools/check_task.py T1` (exit 0 = done, 1 = not yet, 2 = could not run)

## The ask

Extend `tools/sales_report.py` to compute, for every `(month, customer_id)` pair, that
distributor's **rolling 3-month share of total company sell-through**: the customer's
trailing 3-month total sell-through amount (that month plus the two before it, or fewer
if less than 3 months of history exists) divided by the company-wide trailing 3-month
total, as a percentage.

## Contract the checker expects

`tools/sales_report.py`, when run, must additionally write:

```
reports/rolling_3mo_share.csv
    month,customer_id,rolling_3mo_amount,company_rolling_3mo_amount,rolling_3mo_share_pct
```

- `rolling_3mo_amount` = sum of that customer's `total_amount` over the trailing window
  (current month + up to 2 prior months, from `data/monthly_summary.csv`).
- `company_rolling_3mo_amount` = the same window, summed across every customer.
- `rolling_3mo_share_pct` = `100 * rolling_3mo_amount / company_rolling_3mo_amount`,
  rounded to 2 decimal places.
- Base the computation on `data/monthly_summary.csv` (the reconciled source of truth),
  not on raw `data/transactions.csv` -- that file still carries the P1 double-loaded
  batch until task T2's fix is applied, and T1 does not depend on T2.

## Governance is part of done

Once the numbers check out, log the change per `skills/change-log/SKILL.md`: prepend an
entry to `docs/CHANGELOG.md` whose title mentions **T1**. `check_task.py T1` checks for
this explicitly -- a correct computation with no log entry still fails the check.

## Accept

```
python tools/sales_report.py     # regenerates reports/, including the new file
python tools/check_task.py T1    # must exit 0
```

`check_task.py T1` recomputes the rolling 3-month share independently, straight from
`data/monthly_summary.csv` -- it does not trust `sales_report.py`'s own math, so a
plausible-looking but wrong formula will not pass.
