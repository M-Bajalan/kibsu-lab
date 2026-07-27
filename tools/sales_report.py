#!/usr/bin/env python3
"""sales_report.py -- monthly sell-through report for Tuppi Trading Co.

Reads the RECONCILED source of truth, data/monthly_summary.csv (never the
raw data/transactions.csv -- that file still carries the P1 double-loaded
batch until tools/reconcile.py's dedupe fix is applied; this report must
not inherit that bug just to print a table), joined against
data/customers.csv for names/zone/channel.

Ships in this BASELINE form producing only the monthly sell-through table.
Task T1 (tasks/T1_add_kpi.md) asks an agent to extend it with a second
output: each distributor's rolling 3-month share of total company
sell-through. Until that KPI is added, reports/rolling_3mo_share.csv does
not exist -- tools/check_task.py T1 checks for exactly that file.

Self-sufficient: generates data/ with the DEFAULT seed if missing, same as
every other tool in this repo -- no separate "generate" step required.

Usage:
    python tools/sales_report.py [--data data/] [--out reports/]

Output:
    reports/monthly_sell_through.csv
        month,customer_id,customer_name,zone,channel,total_quantity,total_amount
"""
import argparse
import csv
import sys
from pathlib import Path

DEFAULT_DATA_DIR = Path("data")
DEFAULT_OUT_DIR = Path("reports")


def ensure_data(data_dir):
    required = ["monthly_summary.csv", "customers.csv"]
    if all((data_dir / name).is_file() for name in required):
        return True
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import generate_data
    generate_data.generate(generate_data.DEFAULT_SEED, data_dir)
    return True


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_monthly_sell_through(data_dir):
    summary_rows = load_csv(data_dir / "monthly_summary.csv")
    customers = {c["customer_id"]: c for c in load_csv(data_dir / "customers.csv")}

    rows = []
    for row in summary_rows:
        customer = customers.get(row["customer_id"], {})
        rows.append({
            "month": row["month"],
            "customer_id": row["customer_id"],
            "customer_name": customer.get("customer_name", "UNKNOWN"),
            "zone": customer.get("zone", "UNKNOWN"),
            "channel": customer.get("channel", "UNKNOWN"),
            "total_quantity": row["total_quantity"],
            "total_amount": row["total_amount"],
        })
    rows.sort(key=lambda r: (r["month"], r["customer_id"]))
    return rows


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description="Monthly sell-through report.")
    parser.add_argument("--data", type=str, default=str(DEFAULT_DATA_DIR))
    parser.add_argument("--out", type=str, default=str(DEFAULT_OUT_DIR))
    args = parser.parse_args()
    data_dir = Path(args.data)
    out_dir = Path(args.out)

    ensure_data(data_dir)
    rows = build_monthly_sell_through(data_dir)
    out_path = out_dir / "monthly_sell_through.csv"
    write_csv(out_path,
              ["month", "customer_id", "customer_name", "zone", "channel",
               "total_quantity", "total_amount"],
              rows)
    print("wrote %d rows to %s" % (len(rows), out_path))
    print("note: rolling 3-month distributor share is not in this report yet -- "
          "see tasks/T1_add_kpi.md")


if __name__ == "__main__":
    main()
