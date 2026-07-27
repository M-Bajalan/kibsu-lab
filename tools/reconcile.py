#!/usr/bin/env python3
"""reconcile.py -- verifies data/monthly_summary.csv against data/transactions.csv.

Ships as an HONEST, undeduped comparator: it groups transactions.csv by
(month, customer_id) exactly as recorded and compares the sums against
monthly_summary.csv. Out of the box this MUST fail (exit 1) -- P1, the
double-loaded July import batch (see tools/generate_data.py), means the
raw transactions for one day get counted twice for every customer that
traded that day, so the raw sum is higher than the reconciled summary for
that month. monthly_summary.csv was computed BEFORE the duplicate batch
was injected, so it is the correct answer.

THE FIX (documented, not hidden -- see
docs/memory/learnings/reconciliation-check-batches-first.md):
dedupe transactions by BATCH ID before summing. Any batch whose full row
set is byte-identical to an earlier batch's is a re-load of the same
import, not new sell-through, and must be dropped before the sum -- never
averaged away, never tolerance-widened. That dedupe step is NOT in this
file yet -- it is what task T2 (tasks/T2_fix_reconciliation.md) asks an
agent to add.

This tool is self-sufficient: data/ is gitignored and never committed, so
if it is missing this script generates it itself with the DEFAULT seed
before reconciling. No separate "generate" step is required to run it.

Usage:
    python tools/reconcile.py [--data data/]

Exit codes:
    0  reconciled clean -- raw total matches monthly_summary.csv
    1  MISMATCH -- a real reconciliation failure was found
    2  CANNOT RUN -- data files missing/unreadable and could not be generated
       (this is reconcile.py's documented cannot_run_exit for .kibsu.json's
       "gates" wiring -- see .kibsu.json and skills/gate/SKILL.md)
"""
import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

CANNOT_RUN_EXIT = 2

# Do not widen this to make a real gap disappear -- that is the exact fudge
# task T2's checker (tools/check_task.py T2) is built to catch. 1 cent of
# rounding drift across a year of daily "%.2f" amounts is expected; a real
# double-loaded batch is orders of magnitude larger than this tolerance.
AMOUNT_TOLERANCE = 0.01

DEFAULT_DATA_DIR = Path("data")


def ensure_data(data_dir):
    """Generate data/ with the default seed if it does not exist yet."""
    required = ["transactions.csv", "monthly_summary.csv"]
    if all((data_dir / name).is_file() for name in required):
        return True
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        import generate_data
    except Exception as exc:
        print("reconcile: CANNOT RUN -- data/ is missing and tools/generate_data.py "
              "could not be imported (%s)" % exc, file=sys.stderr)
        return False
    try:
        generate_data.generate(generate_data.DEFAULT_SEED, data_dir)
    except Exception as exc:
        print("reconcile: CANNOT RUN -- data/ is missing and generation failed (%s)"
              % exc, file=sys.stderr)
        return False
    return True


def load_transactions(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_summary(path):
    summary = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row["month"], row["customer_id"])
            summary[key] = {
                "transaction_count": int(row["transaction_count"]),
                "total_quantity": int(row["total_quantity"]),
                "total_amount": float(row["total_amount"]),
            }
    return summary


def group_by_month_customer(transactions):
    """Sum every row of transactions.csv exactly as recorded -- no dedupe.
    See the module docstring: this is intentional. Adding a dedupe-by-batch
    step here, before this groupby, is task T2."""
    grouped = defaultdict(lambda: {"transaction_count": 0, "total_quantity": 0,
                                    "total_amount": 0.0})
    for row in transactions:
        month = row["txn_date"][:7]  # "YYYY-MM-DD" -> "YYYY-MM"
        key = (month, row["customer_id"])
        bucket = grouped[key]
        bucket["transaction_count"] += 1
        bucket["total_quantity"] += int(row["quantity"])
        bucket["total_amount"] += float(row["amount"])
    return grouped


def reconcile(data_dir):
    transactions = load_transactions(data_dir / "transactions.csv")
    summary = load_summary(data_dir / "monthly_summary.csv")

    computed = group_by_month_customer(transactions)

    violations = []
    for key in sorted(set(summary) | set(computed)):
        month, customer_id = key
        expected = summary.get(key, {"transaction_count": 0, "total_quantity": 0,
                                      "total_amount": 0.0})
        actual = computed.get(key, {"transaction_count": 0, "total_quantity": 0,
                                     "total_amount": 0.0})
        diff = round(actual["total_amount"] - expected["total_amount"], 2)
        if (actual["transaction_count"] != expected["transaction_count"]
                or actual["total_quantity"] != expected["total_quantity"]
                or abs(diff) > AMOUNT_TOLERANCE):
            violations.append(
                "%s %s: raw=%.2f summary=%.2f diff=%.2f  (txn_count %d vs %d, qty %d vs %d)"
                % (month, customer_id, actual["total_amount"], expected["total_amount"], diff,
                   actual["transaction_count"], expected["transaction_count"],
                   actual["total_quantity"], expected["total_quantity"]))
    return violations


def main():
    parser = argparse.ArgumentParser(
        description="Reconcile data/transactions.csv against data/monthly_summary.csv.")
    parser.add_argument("--data", type=str, default=str(DEFAULT_DATA_DIR))
    args = parser.parse_args()
    data_dir = Path(args.data)

    if not ensure_data(data_dir):
        sys.exit(CANNOT_RUN_EXIT)

    try:
        violations = reconcile(data_dir)
    except Exception as exc:
        print("reconcile: CANNOT RUN -- %s" % exc, file=sys.stderr)
        sys.exit(CANNOT_RUN_EXIT)

    if not violations:
        print("reconcile: PASS -- monthly_summary.csv matches transactions.csv, "
              "0 violations")
        sys.exit(0)

    # [RULE] header shape kibsu's gate command parses (see skills/gate/SKILL.md and
    # .kibsu.json's "gates" entry) -- a plain PASS/FAIL print would be invisible to it.
    print("[RECONCILE] Sell-through mismatch between transactions.csv and "
          "monthly_summary.csv (%d):" % len(violations))
    for v in violations:
        print("    - %s" % v)
    sys.exit(1)


if __name__ == "__main__":
    main()
