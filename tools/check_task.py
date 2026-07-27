#!/usr/bin/env python3
"""check_task.py -- verifier for kibsu-lab's machine-checkable agent tasks.

Usage:
    python tools/check_task.py T1|T2|T3
    python tools/check_task.py --selftest [path/to/transactions.csv]

Every checker below is a NEGATIVE CONTROL by construction: run against a
pristine, unmodified clone (nothing solved yet) it must exit 1. A checker
that passes on an untouched repo proves nothing about the task it claims
to check -- see the design contract's L4 section. Do not "fix" a checker
by making it more lenient; if it cannot fail, the task needs redesigning,
not the checker.

Exit codes (every checker): 0 = task done and verified · 1 = not done yet
(or verification failed) · 2 = could not run (see printed reason).
"""
import csv
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
REPORTS_DIR = REPO_ROOT / "reports"
CANNOT_RUN_EXIT = 2

# T3's continuation proof: the branch task/T1-in-progress ships a real,
# partial commit. Its SHA is recorded here AND in tasks/T3_resume_the_work.md
# -- both copies must name the same commit, and check_T3() below verifies it
# is an ancestor of HEAD rather than trusting either file blindly.
T3_MARKER_FILE = REPO_ROOT / "tasks" / "T3_resume_the_work.md"


# --------------------------------------------------------------------------- shared helpers --

def ensure_data():
    required = ["transactions.csv", "monthly_summary.csv", "customers.csv"]
    if all((DATA_DIR / name).is_file() for name in required):
        return
    sys.path.insert(0, str(REPO_ROOT / "tools"))
    import generate_data
    generate_data.generate(generate_data.DEFAULT_SEED, DATA_DIR)


def run(cmd, cwd=None):
    proc = subprocess.run(cmd, cwd=cwd or REPO_ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    return proc.returncode, proc.stdout, proc.stderr


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def changelog_top_entry_mentions(token):
    changelog = REPO_ROOT / "docs" / "CHANGELOG.md"
    if not changelog.is_file():
        return False
    text = changelog.read_text(encoding="utf-8")
    # top entry = from the first "## [" header to the second (or EOF) -- CHANGELOG.md is
    # prepend-style (newest first), see skills/change-log/SKILL.md.
    lines = text.split("\n")
    starts = [i for i, ln in enumerate(lines) if ln.startswith("## [")]
    if not starts:
        return False
    top = lines[starts[0]:(starts[1] if len(starts) > 1 else len(lines))]
    return token.lower() in "\n".join(top).lower()


# --------------------------------------------------------------------------- P1 selftest -----

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


def run_selftest(argv):
    extra_args = [a for a in argv if a != "--selftest"]
    txn_path = extra_args[0] if extra_args else str(DATA_DIR / "transactions.csv")
    hit = find_duplicate_batch(txn_path)
    if hit:
        print("P1 selftest PASS: batch %s was re-loaded verbatim as batch %s" % hit)
        return 0
    print("P1 selftest FAIL: no duplicated batch found in", txn_path)
    return 1


# --------------------------------------------------------------------------- T1 --------------

def independent_rolling_3mo_share(data_dir):
    """Recompute rolling 3-month distributor share directly from
    monthly_summary.csv -- independent of sales_report.py's own code, so this
    is a real check, not a re-read of the thing being verified."""
    summary = load_csv(data_dir / "monthly_summary.csv")
    by_customer_month = defaultdict(dict)  # customer_id -> {month: total_amount}
    months = sorted({r["month"] for r in summary})
    for r in summary:
        by_customer_month[r["customer_id"]][r["month"]] = float(r["total_amount"])

    company_by_month = defaultdict(float)
    for r in summary:
        company_by_month[r["month"]] += float(r["total_amount"])

    result = {}
    for customer_id, month_totals in by_customer_month.items():
        for i, month in enumerate(months):
            if month not in month_totals:
                continue
            window = months[max(0, i - 2):i + 1]
            cust_rolling = sum(month_totals.get(m, 0.0) for m in window)
            company_rolling = sum(company_by_month.get(m, 0.0) for m in window)
            pct = (100.0 * cust_rolling / company_rolling) if company_rolling else 0.0
            result[(month, customer_id)] = round(pct, 2)
    return result


def check_T1():
    ensure_data()
    code, out, err = run([sys.executable, str(REPO_ROOT / "tools" / "sales_report.py")])
    if code != 0:
        print("T1 FAIL: tools/sales_report.py exited %d\n%s%s" % (code, out, err))
        return 1

    output_path = REPORTS_DIR / "rolling_3mo_share.csv"
    if not output_path.is_file():
        print("T1 FAIL: %s was not produced -- the rolling 3-month distributor share "
              "KPI has not been added to tools/sales_report.py yet. See tasks/T1_add_kpi.md."
              % output_path)
        return 1

    produced = {}
    for row in load_csv(output_path):
        try:
            produced[(row["month"], row["customer_id"])] = round(
                float(row["rolling_3mo_share_pct"]), 2)
        except (KeyError, ValueError) as exc:
            print("T1 FAIL: %s has an unexpected shape (%s)" % (output_path, exc))
            return 1

    expected = independent_rolling_3mo_share(DATA_DIR)
    mismatches = []
    for key, exp_val in expected.items():
        got = produced.get(key)
        if got is None:
            mismatches.append("%s missing from output" % (key,))
        elif abs(got - exp_val) > 0.01:
            mismatches.append("%s: expected %.2f got %.2f" % (key, exp_val, got))
    if mismatches:
        print("T1 FAIL: %d mismatch(es) against an independent recomputation:" % len(mismatches))
        for m in mismatches[:10]:
            print("  -", m)
        return 1

    if not changelog_top_entry_mentions("T1"):
        print("T1 FAIL: computation is correct, but docs/CHANGELOG.md's newest entry does not "
              "mention T1 -- governance is part of done. Log the change (skills/change-log/SKILL.md) "
              "before calling this task finished.")
        return 1

    print("T1 PASS: rolling 3-month distributor share matches an independent recomputation "
          "(%d rows) and the change was logged." % len(expected))
    return 0


# --------------------------------------------------------------------------- T2 --------------

def independent_reconciled_summary(data_dir):
    """Independent, from-scratch dedupe-by-batch-id + sum -- does NOT call
    tools/reconcile.py. This is what makes T2's check resistant to a fudge in
    reconcile.py itself (e.g. an unconditional exit 0)."""
    transactions = load_csv(data_dir / "transactions.csv")
    rows_by_batch = defaultdict(list)
    for row in transactions:
        rows_by_batch[row["batch_id"]].append(row)

    def sig(row):
        return (row["txn_date"], row["customer_id"], row["product_id"], row["rep_id"],
                row["quantity"], row["unit_price"])

    seen, kept = {}, []
    for batch_id in sorted(rows_by_batch, key=int):
        rows = rows_by_batch[batch_id]
        signature = tuple(sorted(sig(r) for r in rows))
        if signature in seen:
            continue
        seen[signature] = batch_id
        kept.extend(rows)

    deduped_totals = defaultdict(float)
    naive_totals = defaultdict(float)
    for row in transactions:
        naive_totals[(row["txn_date"][:7], row["customer_id"])] += float(row["amount"])
    for row in kept:
        deduped_totals[(row["txn_date"][:7], row["customer_id"])] += float(row["amount"])
    return deduped_totals, naive_totals


def check_T2():
    ensure_data()
    code, out, err = run([sys.executable, str(REPO_ROOT / "tools" / "reconcile.py")])
    if code != 0:
        print("T2 FAIL: tools/reconcile.py exited %d (expected 0)\n%s%s" % (code, out, err))
        return 1

    summary = {(r["month"], r["customer_id"]): round(float(r["total_amount"]), 2)
               for r in load_csv(DATA_DIR / "monthly_summary.csv")}
    deduped_totals, naive_totals = independent_reconciled_summary(DATA_DIR)

    # anti-fudge #1: the independently-deduped total must genuinely match the source of truth.
    bad = [k for k in summary if abs(round(deduped_totals.get(k, 0.0), 2) - summary[k]) > 0.01]
    if bad:
        print("T2 FAIL: reconcile.py exits 0, but an independent batch-dedupe recomputation "
              "does NOT match monthly_summary.csv for %d bucket(s) -- exit 0 does not mean "
              "correct." % len(bad))
        return 1

    # anti-fudge #2: prove there WAS a real gap to fix -- the naive (undeduped) sum must have
    # genuinely disagreed with the summary. If it didn't, P1 never reached this data and the
    # "fix" fixed nothing.
    naive_gap = any(abs(round(naive_totals.get(k, 0.0), 2) - summary[k]) > 0.01 for k in summary)
    if not naive_gap:
        print("T2 FAIL: the undeduped (naive) total already matches monthly_summary.csv -- "
              "P1 (the double-loaded batch) never reached this data, so there was nothing for "
              "the fix to prove. This points at a data generation problem, not a real pass.")
        return 1

    learning = REPO_ROOT / "docs" / "memory" / "learnings" / "reconciliation-check-batches-first.md"
    if not learning.is_file() or not learning.read_text(encoding="utf-8").strip():
        print("T2 FAIL: %s is missing or empty -- the learning must exist and be consulted "
              "per skills/change-log/SKILL.md." % learning)
        return 1

    print("T2 PASS: reconcile.py exits 0, an independent batch-dedupe recomputation matches "
          "monthly_summary.csv, and the naive total genuinely disagreed (real fix, not a fudge).")
    return 0


# --------------------------------------------------------------------------- T3 --------------

def read_t3_marker():
    if not T3_MARKER_FILE.is_file():
        return None
    text = T3_MARKER_FILE.read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        if line.upper().startswith("MARKER_COMMIT:"):
            return line.split(":", 1)[1].strip()
    return None


def check_T3():
    marker = read_t3_marker()
    if not marker:
        print("T3 FAIL: no MARKER_COMMIT recorded in tasks/T3_resume_the_work.md.")
        return 1

    code, _, _ = run(["git", "merge-base", "--is-ancestor", marker, "HEAD"])
    if code != 0:
        print("T3 FAIL: commit %s (the half-done T1 work on task/T1-in-progress) is NOT an "
              "ancestor of HEAD -- this looks like a restart, not a continuation." % marker)
        return 1

    t1_result = check_T1()
    if t1_result != 0:
        print("T3 FAIL: the marker commit is a real ancestor (continuation proven), but T1 is "
              "not finished yet on this branch.")
        return 1

    print("T3 PASS: %s is an ancestor of HEAD (genuine continuation) and T1 is complete." % marker)
    return 0


# --------------------------------------------------------------------------- entry point -----

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: check_task.py T1|T2|T3 | check_task.py --selftest [path]")

    if "--selftest" in sys.argv:
        sys.exit(run_selftest(sys.argv[1:]))

    task = sys.argv[1]
    dispatch = {"T1": check_T1, "T2": check_T2, "T3": check_T3}
    if task not in dispatch:
        sys.exit("usage: check_task.py T1|T2|T3 | check_task.py --selftest [path]")
    sys.exit(dispatch[task]())


if __name__ == "__main__":
    main()
