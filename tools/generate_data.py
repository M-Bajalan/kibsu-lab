#!/usr/bin/env python3
"""generate_data.py -- seeded, stdlib-only synthetic data generator for kibsu-lab.

Generates one fictional distribution company (Tuppi Trading Co.): its
distributor customers, product catalog, sales reps, and a year of daily
sell-through transactions with a pre-aggregated monthly summary.

The generator IS the shipped artifact. Its output (data/) is never committed.
Same --seed always produces byte-identical files; a different --seed produces
a different (but still internally consistent) dataset.

Determinism rules this file follows on purpose:
  - exactly one random.Random(seed) instance is threaded through everything;
    the module-level `random` functions are never called.
  - no set() is ever iterated to decide output order or content; every
    grouping is written out in an explicitly sorted or list-built order.
  - every float that reaches a CSV is formatted with "%.2f", never str()/repr().
  - CSV files are opened with newline="" and written with lineterminator="\n"
    so output does not depend on platform line-ending conventions.
  - no timestamps, no os.urandom, no PIDs, nothing from the clock or the
    environment ever reaches the output -- the fiscal year is a hardcoded
    constant, not datetime.now().

Usage:
    python tools/generate_data.py [--seed 20260727] [--out data/]
"""

import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

# --- fixed structural constants -------------------------------------------

DEFAULT_SEED = 20260727
START_DATE = date(2025, 1, 1)  # fictional fiscal year; hardcoded, never datetime.now()
NUM_DAYS = 365

NUM_PRODUCTS = 50
NUM_REPS = 12

CATEGORIES = ["Beverages", "Snacks", "Household", "Personal Care"]
SHELF_LIFE_CLASSES = ["short", "medium", "long"]
ZONES = ["Zone-1", "Zone-2", "Zone-3", "Zone-4"]
CHANNELS = ["Modern Trade", "Traditional Trade", "Wholesale"]

CATEGORY_BASE_PRICE = {
    "Beverages": 3.50,
    "Snacks": 2.25,
    "Household": 6.75,
    "Personal Care": 8.90,
}

CUSTOMER_NAME_STEMS = [
    "Cedar Route", "Harborlight", "Stonebridge", "Amberfield",
    "Northgate", "Rivermouth", "Silverline", "Oakwell",
]

REP_FIRST_NAMES = [
    "Alex", "Elliot", "Taylor", "Morgan", "Casey", "Reese",
    "Sam", "Drew", "Jamie", "Quinn", "Avery", "Riley",
    "Peyton", "Rowan", "Skyler", "Emerson",
]
REP_LAST_NAMES = [
    "Carter", "Bennett", "Hayes", "Foster", "Griffin", "Palmer",
    "Reyes", "Sawyer", "Mercer", "Whitfield", "Doyle", "Kessler",
    "Abernathy", "Bryant", "Coleman", "Deacon",
]

# planted-defect knobs (see PROVENANCE/design doc for the full story)
ORPHAN_PRODUCT_IDS = ["P51", "P52"]  # deliberately absent from products.csv (P2)
ORPHAN_COUNT = 10
P1_MONTH = 7          # mid-year month the double-loaded batch lands in (July)
P3_GAP_DAYS = 21       # ~3 weeks of silence for one distributor (P3)
MIN_LINES_PER_CUSTOMER_DAY = 20
MAX_LINES_PER_CUSTOMER_DAY = 32


# --- master data ------------------------------------------------------------

def build_customers(rng):
    customers = []
    for i, stem in enumerate(CUSTOMER_NAME_STEMS, start=1):
        customers.append({
            "customer_id": f"C{i:02d}",
            "customer_name": f"{stem} Distribution",
            "zone": ZONES[(i - 1) % len(ZONES)],
            "channel": rng.choice(CHANNELS),
        })
    return customers


def build_products(rng):
    products = []
    for i in range(1, NUM_PRODUCTS + 1):
        category = CATEGORIES[(i - 1) % len(CATEGORIES)]
        jitter = rng.uniform(0.7, 1.4)
        unit_price = round(CATEGORY_BASE_PRICE[category] * jitter, 2)
        products.append({
            "product_id": f"P{i:02d}",
            "product_name": f"{category} Product {i:02d}",
            "category": category,
            "shelf_life_class": rng.choice(SHELF_LIFE_CLASSES),
            "unit_price": unit_price,
        })
    return products


def build_reps(rng):
    first_names = list(REP_FIRST_NAMES)
    last_names = list(REP_LAST_NAMES)
    rng.shuffle(first_names)
    rng.shuffle(last_names)
    reps = []
    for i in range(1, NUM_REPS + 1):
        reps.append({
            "rep_id": f"R{i:02d}",
            "rep_name": f"{first_names[i - 1]} {last_names[i - 1]}",
            "zone": ZONES[(i - 1) % len(ZONES)],
        })
    return reps


def choose_gap_window(rng, customers):
    """P3: one distributor goes silent for ~3 weeks (a reporting gap)."""
    gap_customer_id = rng.choice(customers)["customer_id"]
    earliest_offset = 30
    latest_offset = NUM_DAYS - P3_GAP_DAYS - 30
    start_offset = rng.randint(earliest_offset, latest_offset)
    gap_start = START_DATE + timedelta(days=start_offset)
    gap_end = gap_start + timedelta(days=P3_GAP_DAYS)  # exclusive
    return gap_customer_id, gap_start, gap_end


# --- transactions ------------------------------------------------------------

def generate_clean_transactions(rng, customers, products, reps, gap_customer_id, gap_start, gap_end):
    """One row per line item, one batch per calendar day, no defects yet."""
    transactions = []
    for day_index in range(NUM_DAYS):
        current_date = START_DATE + timedelta(days=day_index)
        batch_id = day_index + 1
        for customer in customers:
            if customer["customer_id"] == gap_customer_id and gap_start <= current_date < gap_end:
                continue  # this distributor filed nothing during its gap window
            line_count = rng.randint(MIN_LINES_PER_CUSTOMER_DAY, MAX_LINES_PER_CUSTOMER_DAY)
            for _ in range(line_count):
                product = rng.choice(products)
                rep = rng.choice(reps)
                quantity = rng.randint(1, 40)
                price_jitter = rng.uniform(0.9, 1.05)
                unit_price = round(product["unit_price"] * price_jitter, 2)
                amount = round(quantity * unit_price, 2)
                transactions.append({
                    "batch_id": batch_id,
                    "txn_date": current_date,
                    "customer_id": customer["customer_id"],
                    "product_id": product["product_id"],
                    "rep_id": rep["rep_id"],
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "amount": amount,
                })
    return transactions


def compute_monthly_summary(transactions):
    """The correct, reconciled picture -- computed from the CLEAN transactions,
    before the double-loaded batch (P1) is injected into the raw export. This
    is what makes monthly_summary.csv disagree with transactions.csv."""
    totals = {}
    for txn in transactions:
        key = (txn["txn_date"].strftime("%Y-%m"), txn["customer_id"])
        bucket = totals.setdefault(key, {"transaction_count": 0, "total_quantity": 0, "total_amount": 0.0})
        bucket["transaction_count"] += 1
        bucket["total_quantity"] += txn["quantity"]
        bucket["total_amount"] += txn["amount"]

    rows = []
    for key in sorted(totals.keys()):  # explicit sort -- never rely on dict/set iteration order
        month, customer_id = key
        bucket = totals[key]
        rows.append({
            "month": month,
            "customer_id": customer_id,
            "transaction_count": bucket["transaction_count"],
            "total_quantity": bucket["total_quantity"],
            "total_amount": round(bucket["total_amount"], 2),
        })
    return rows


def inject_double_loaded_batch(rng, transactions):
    """P1: a mid-year day's import batch gets re-loaded verbatim, one batch id
    later -- the readable shape of a real ETL bug (a scheduler re-ran, or a
    stale source file got picked up twice), not a labeled defect."""
    july_day_indices = [
        d for d in range(NUM_DAYS)
        if (START_DATE + timedelta(days=d)).month == P1_MONTH
    ]
    dup_day_index = rng.choice(july_day_indices)
    dup_date = START_DATE + timedelta(days=dup_day_index)
    original_batch_id = dup_day_index + 1

    slice_start = next(i for i, t in enumerate(transactions) if t["txn_date"] == dup_date)
    slice_end = slice_start
    while slice_end < len(transactions) and transactions[slice_end]["txn_date"] == dup_date:
        slice_end += 1

    duplicate_rows = []
    for txn in transactions[slice_start:slice_end]:
        dup = dict(txn)
        dup["batch_id"] = original_batch_id + 1
        duplicate_rows.append(dup)

    # every batch loaded after the duplicated day shifts up by one to make room
    for txn in transactions[slice_end:]:
        txn["batch_id"] += 1

    merged = transactions[:slice_end] + duplicate_rows + transactions[slice_end:]
    protected_start, protected_end = slice_start, slice_end + len(duplicate_rows)
    return merged, protected_start, protected_end


def inject_orphan_products(rng, transactions, protected_range):
    """P2: a handful of transactions reference a product id that was never in
    products.csv -- common master-data drift. Kept out of the P1 slice so the
    double-loaded batch stays an exact, clean duplicate."""
    protected_start, protected_end = protected_range
    eligible = [i for i in range(len(transactions)) if not (protected_start <= i < protected_end)]
    victims = sorted(rng.sample(eligible, k=min(ORPHAN_COUNT, len(eligible))))
    for position, idx in enumerate(victims):
        transactions[idx]["product_id"] = ORPHAN_PRODUCT_IDS[position % len(ORPHAN_PRODUCT_IDS)]
    return transactions


def finalize_transaction_ids(transactions):
    for i, txn in enumerate(transactions, start=1):
        txn["transaction_id"] = f"T{i:06d}"
    return transactions


# --- output formatting -------------------------------------------------------

def format_customers(customers):
    return [
        {
            "customer_id": c["customer_id"],
            "customer_name": c["customer_name"],
            "zone": c["zone"],
            "channel": c["channel"],
        }
        for c in customers
    ]


def format_products(products):
    return [
        {
            "product_id": p["product_id"],
            "product_name": p["product_name"],
            "category": p["category"],
            "shelf_life_class": p["shelf_life_class"],
            "unit_price": "%.2f" % p["unit_price"],
        }
        for p in products
    ]


def format_reps(reps):
    return [
        {"rep_id": r["rep_id"], "rep_name": r["rep_name"], "zone": r["zone"]}
        for r in reps
    ]


def format_transactions(transactions):
    return [
        {
            "transaction_id": t["transaction_id"],
            "batch_id": t["batch_id"],
            "txn_date": t["txn_date"].isoformat(),
            "customer_id": t["customer_id"],
            "product_id": t["product_id"],
            "rep_id": t["rep_id"],
            "quantity": t["quantity"],
            "unit_price": "%.2f" % t["unit_price"],
            "amount": "%.2f" % t["amount"],
        }
        for t in transactions
    ]


def format_summary(rows):
    return [
        {
            "month": r["month"],
            "customer_id": r["customer_id"],
            "transaction_count": r["transaction_count"],
            "total_quantity": r["total_quantity"],
            "total_amount": "%.2f" % r["total_amount"],
        }
        for r in rows
    ]


def write_csv(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


# --- entry point --------------------------------------------------------------

def generate(seed, out_dir):
    rng = random.Random(seed)  # the ONLY random source used anywhere in this module

    customers = build_customers(rng)
    products = build_products(rng)
    reps = build_reps(rng)

    gap_customer_id, gap_start, gap_end = choose_gap_window(rng, customers)
    clean_transactions = generate_clean_transactions(
        rng, customers, products, reps, gap_customer_id, gap_start, gap_end
    )

    summary_rows = compute_monthly_summary(clean_transactions)

    raw_transactions, protected_start, protected_end = inject_double_loaded_batch(rng, clean_transactions)
    raw_transactions = inject_orphan_products(rng, raw_transactions, (protected_start, protected_end))
    raw_transactions = finalize_transaction_ids(raw_transactions)

    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "customers.csv",
              ["customer_id", "customer_name", "zone", "channel"],
              format_customers(customers))
    write_csv(out_dir / "products.csv",
              ["product_id", "product_name", "category", "shelf_life_class", "unit_price"],
              format_products(products))
    write_csv(out_dir / "reps.csv",
              ["rep_id", "rep_name", "zone"],
              format_reps(reps))
    write_csv(out_dir / "transactions.csv",
              ["transaction_id", "batch_id", "txn_date", "customer_id", "product_id", "rep_id",
               "quantity", "unit_price", "amount"],
              format_transactions(raw_transactions))
    write_csv(out_dir / "monthly_summary.csv",
              ["month", "customer_id", "transaction_count", "total_quantity", "total_amount"],
              format_summary(summary_rows))

    return len(raw_transactions)


def main():
    parser = argparse.ArgumentParser(description="Generate kibsu-lab's seeded synthetic dataset.")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out", type=str, default="data/")
    args = parser.parse_args()

    row_count = generate(args.seed, Path(args.out))
    print(f"generated {row_count} transactions in {args.out} (seed={args.seed})")


if __name__ == "__main__":
    main()
