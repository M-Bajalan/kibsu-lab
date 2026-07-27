#!/usr/bin/env python3
"""check_task.py -- verifier for kibsu-lab's machine-checkable tasks.

L0 ships only the --selftest probe: it proves P1 (the double-loaded batch)
is actually present in generated data, by finding two distinct batch ids
whose row content is byte-for-byte identical. A probe that can never fail
proves nothing, so this one does: run it against deduped data and it exits 1.

T1/T2/T3 checkers are added in L4; this file is not their home yet.

Usage:
    python tools/check_task.py --selftest [path/to/transactions.csv]
"""
import csv
import sys
from collections import defaultdict

DEFAULT_TRANSACTIONS_PATH = "data/transactions.csv"


def find_duplicate_batch(path):
    rows_by_batch = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row["txn_date"], row["customer_id"], row["product_id"],
                   row["rep_id"], row["quantity"], row["unit_price"])
            rows_by_batch[row["batch_id"]].append(key)

    seen_signatures = {}
    for batch_id in sorted(rows_by_batch, key=int):
        signature = tuple(sorted(rows_by_batch[batch_id]))
        if signature in seen_signatures:
            return seen_signatures[signature], batch_id
        seen_signatures[signature] = batch_id
    return None


if __name__ == "__main__":
    if "--selftest" not in sys.argv:
        sys.exit("usage: check_task.py --selftest [path/to/transactions.csv]")
    extra_args = [a for a in sys.argv[1:] if a != "--selftest"]
    txn_path = extra_args[0] if extra_args else DEFAULT_TRANSACTIONS_PATH

    hit = find_duplicate_batch(txn_path)
    if hit:
        print(f"P1 selftest PASS: batch {hit[0]} was re-loaded verbatim as batch {hit[1]}")
        sys.exit(0)
    print("P1 selftest FAIL: no duplicated batch found in", txn_path)
    sys.exit(1)
