#!/usr/bin/env python3
"""check_baseline.py -- does README.md's Baseline say what kibsu prints on this clone?

Usage:
    python tools/check_baseline.py                  compare; exit 0 / 1 / 2
    python tools/check_baseline.py --selftest       prove the comparison can fail
    python tools/check_baseline.py --install-spec   print the requirement the Quickstart installs

README.md publishes two blocks of tool output -- the whole of `python -m kibsu report .`
and the table and headline of `python -m kibsu audit .` -- and says of them that a fresh
clone following the Quickstart reproduces them. That claim went stale twice while CI stayed
green, because nothing compared the page with the tool. This does.

What it checks:
  1. The report block, line for line, with the clone path written as /path/to/kibsu-lab.
  2. The audit excerpt, from the table header to the "genre declared" line.
  3. The kibsu version is stated in three places -- the Baseline heading, the Quickstart's
     install line and the pin in .github/workflows/lab-ci.yml -- and they agree.

It rebuilds the index first (`python -m kibsu index .`, a gitignored file), exactly as the
Quickstart does, so a stale local index can neither hide a difference nor invent one. It
writes nothing else.

One blind spot, stated because this checker's own first run fell into it: kibsu builds its
index from `git ls-files`, so a document git does not know yet is not counted. Run before
`git add`, the check passes on a page that a fresh clone of the commit would contradict. It
therefore names every untracked Markdown file it finds, and says the verdict does not cover
them. See docs/memory/learnings/untracked-docs-are-invisible-to-the-index.md.

A mismatch is not always this repository's doing. If the installed kibsu is not the version
the heading names, the output may differ because the instrument moved; the report says which
version it ran, so the two cases can be told apart.

Exit codes: 0 = the page says what the tool prints · 1 = it does not (both sides printed)
· 2 = could not run (see printed reason).
"""
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "lab-ci.yml"
PLACEHOLDER = "/path/to/kibsu-lab"
CANNOT_RUN_EXIT = 2

REPORT_MARK = "WHAT YOUR AGENTS CANNOT DO HERE YET"
AUDIT_FIRST = "  genre        units"
AUDIT_LAST = "  genre declared in frontmatter"

HEADING_RE = re.compile(r"^## Baseline \(.*\bkibsu (\d+(?:\.\d+)+) from PyPI\)\s*$", re.M)
INSTALL_RE = re.compile(r'^pip install "(kibsu>=(\d+(?:\.\d+)+))"', re.M)
PIN_RE = re.compile(r"^\s*run: pip install kibsu==(\d+(?:\.\d+)+)\s*$", re.M)
VERSION_RE = re.compile(r"\bkibsu (\d+(?:\.\d+)+)")


class CannotRun(Exception):
    """The check could not be made at all -- distinct from "made, and the page is wrong"."""


# --------------------------------------------------------------------------- reading the page --

def fenced_blocks(text):
    """Every ``` block in a Markdown text, as lists of right-stripped lines."""
    blocks, current, inside = [], [], False
    for line in text.replace("\r\n", "\n").split("\n"):
        if line.startswith("```"):
            if inside:
                blocks.append(current)
                current = []
            inside = not inside
        elif inside:
            current.append(line.rstrip())
    return blocks


def trim(lines):
    """Drop blank lines from both ends; the lines between are kept exactly."""
    lines = list(lines)
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def readme_blocks(text):
    """(report block, audit excerpt) as README.md publishes them."""
    report = audit = None
    for block in fenced_blocks(text):
        if report is None and any(REPORT_MARK in line for line in block):
            report = trim(block)
        if audit is None and any(line.startswith(AUDIT_FIRST) for line in block):
            audit = trim(block)
    if report is None:
        raise CannotRun("README.md has no fenced block containing %r" % REPORT_MARK)
    if audit is None:
        raise CannotRun("README.md has no fenced block starting the audit table (%r)" % AUDIT_FIRST)
    return report, audit


def stated_versions(readme_text, workflow_text):
    """The kibsu version as each of the three places states it. None = not found there."""
    heading = HEADING_RE.search(readme_text)
    install = INSTALL_RE.search(readme_text)
    pin = PIN_RE.search(workflow_text)
    return {
        "README Baseline heading": heading.group(1) if heading else None,
        "README Quickstart install line (floor)": install.group(2) if install else None,
        ".github/workflows/lab-ci.yml pin": pin.group(1) if pin else None,
    }


def install_spec(readme_text):
    """The requirement the Quickstart tells a reader to install, e.g. kibsu>=0.10.0."""
    found = INSTALL_RE.search(readme_text)
    if not found:
        raise CannotRun('README.md has no line of the form: pip install "kibsu>=X.Y.Z"')
    return found.group(1)


# --------------------------------------------------------------------------- reading the tool --

def run(cmd):
    proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    return proc.returncode, proc.stdout, proc.stderr


def kibsu(*args):
    return run([sys.executable, "-m", "kibsu"] + list(args))


def installed_version():
    code, out, err = kibsu("--version")
    found = VERSION_RE.search(out)
    if code != 0 or not found:
        last = ((err or out).strip().splitlines() or [""])[-1]
        raise CannotRun("kibsu is not installed for this interpreter (%s) -- follow the "
                        "Quickstart's install line first.\n  %s" % (sys.executable, last))
    return found.group(1), out.strip()


def live_blocks():
    """(report lines, audit excerpt lines) as the tool prints them on this clone, now."""
    code, out, _ = run(["git", "rev-parse", "--is-shallow-repository"])
    if code == 0 and out.strip() == "true":
        raise CannotRun("this is a shallow clone. The Baseline is a full clone's -- on a shallow "
                        "one `report` rightly answers its fourth question differently. "
                        "Run: git fetch --unshallow")
    code, out, err = kibsu("index", ".")
    if code != 0:
        raise CannotRun("`python -m kibsu index .` exited %d:\n%s" % (code, (err or out).strip()))
    code, out, err = kibsu("report", ".")
    if code not in (0, 3):
        raise CannotRun("`python -m kibsu report .` exited %d (0 or 3 expected):\n%s"
                        % (code, (err or out).strip()))
    root = str(REPO_ROOT)
    report = []
    for line in trim(out.replace("\r\n", "\n").split("\n")):
        for spelling in (root, root.replace("\\", "/")):
            line = line.replace(spelling, PLACEHOLDER)
        report.append(line.rstrip())
    code, out, err = kibsu("audit", ".")
    if code != 0:
        raise CannotRun("`python -m kibsu audit .` exited %d:\n%s" % (code, (err or out).strip()))
    lines = [line.rstrip() for line in out.replace("\r\n", "\n").split("\n")]
    try:
        first = next(i for i, line in enumerate(lines) if line.startswith(AUDIT_FIRST))
        last = next(i for i, line in enumerate(lines) if line.startswith(AUDIT_LAST))
    except StopIteration:
        raise CannotRun("`python -m kibsu audit .` printed no table this checker recognises")
    return report, lines[first:last + 1]


def untracked_markdown():
    """Markdown files git does not know yet -- invisible to kibsu's index, so to this check."""
    code, out, _ = run(["git", "ls-files", "--others", "--exclude-standard", "--", "*.md"])
    return sorted(line.strip() for line in out.splitlines() if line.strip()) if code == 0 else []


# --------------------------------------------------------------------------- comparing --

def differences(page, tool):
    """[(line number, what the page says, what the tool prints)] -- empty when equal."""
    out = []
    for i in range(max(len(page), len(tool))):
        a = page[i] if i < len(page) else "<no such line>"
        b = tool[i] if i < len(tool) else "<no such line>"
        if a != b:
            out.append((i + 1, a, b))
    return out


def version_disagreements(versions):
    """Reasons the three statements of the version do not agree -- empty when they do."""
    problems = ["%s: no version found" % place for place, v in versions.items() if v is None]
    stated = {v for v in versions.values() if v is not None}
    if len(stated) > 1:
        problems.append("they name different versions: "
                        + "; ".join("%s = %s" % (p, v) for p, v in versions.items()))
    return problems


# --------------------------------------------------------------------------- modes --

def check():
    readme_text = README.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.is_file() else ""
    page_report, page_audit = readme_blocks(readme_text)
    versions = stated_versions(readme_text, workflow_text)
    version, banner = installed_version()
    tool_report, tool_audit = live_blocks()

    failed = False
    print("check_baseline: README.md's Baseline against %s" % banner)
    for name, page, tool in (("report block", page_report, tool_report),
                             ("audit excerpt", page_audit, tool_audit)):
        diff = differences(page, tool)
        print("  %-14s README %2d lines, tool %2d lines: %s"
              % (name, len(page), len(tool), "equal" if not diff else "%d line(s) differ" % len(diff)))
        for number, a, b in diff:
            print("    line %d\n      README: %s\n      tool  : %s" % (number, a, b))
        failed = failed or bool(diff)

    problems = version_disagreements(versions)
    print("  %-14s %s" % ("version", "stated the same in all three places (%s)"
                          % next(iter(versions.values())) if not problems else "DISAGREE"))
    for problem in problems:
        print("    " + problem)
    failed = failed or bool(problems)

    heading = versions["README Baseline heading"]
    if heading and heading != version:
        print("  note: the heading says this block was captured with kibsu %s; this run used "
              "kibsu %s." % (heading, version))
        if failed:
            print("        So the instrument may have moved, not this repository. If the "
                  "Quickstart installs %s today, the page is stale for it." % version)
    unseen = untracked_markdown()
    if unseen:
        print("  note: %d Markdown file(s) are not tracked by git, so kibsu's index does not "
              "count them and this verdict does not cover them:" % len(unseen))
        for path in unseen:
            print("        %s" % path)
        print("        `git add` them and run this again before trusting a PASS.")
    if failed:
        print("\nFAIL. To re-capture: follow the Quickstart on a fresh clone, replace each block "
              "with what the tool prints (the clone path written as %s), move the heading, the "
              "install line and the CI pin together, and say in docs/CHANGELOG.md whether the "
              "instrument moved or this repository did." % PLACEHOLDER)
        return 1
    print("\nPASS. The page says what the tool prints.")
    return 0


def selftest():
    """The comparison and the version rule, each made to fail on purpose. Needs no kibsu."""
    page_report, page_audit = readme_blocks(README.read_text(encoding="utf-8"))
    results = []

    results.append(("identical blocks compare equal",
                    differences(page_report, list(page_report)) == []))
    # One digit, on one line: the smallest way the page can be wrong.
    target = next((i for i, line in enumerate(page_report) if re.search(r"\d", line)), None)
    altered = list(page_report)
    if target is not None:
        altered[target] = re.sub(r"\d", lambda m: str((int(m.group(0)) + 1) % 10),
                                 altered[target], count=1)
    results.append(("one changed digit is reported",
                    target is not None and len(differences(page_report, altered)) == 1))
    results.append(("a missing last line is reported",
                    len(differences(page_audit, page_audit[:-1])) == 1))
    results.append(("an extra line is reported",
                    len(differences(page_audit, page_audit + ["  extra"])) == 1))
    agree = {"a": "1.2.0", "b": "1.2.0", "c": "1.2.0"}
    results.append(("three equal versions agree", version_disagreements(agree) == []))
    results.append(("a different pin is reported",
                    len(version_disagreements(dict(agree, c="1.1.0"))) == 1))
    results.append(("a version that cannot be found is reported",
                    len(version_disagreements(dict(agree, b=None))) == 1))
    fake = '## Quickstart\n\n```\npip install "kibsu>=9.9.9"   # comment\n```\n'
    results.append(("the install line is read as written", install_spec(fake) == "kibsu>=9.9.9"))

    for name, passed in results:
        print("  %s  %s" % ("ok  " if passed else "FAIL", name))
    if all(passed for _, passed in results):
        print("check_baseline selftest PASS: the comparison fails when it should")
        return 0
    print("check_baseline selftest FAIL: a check that cannot fail proves nothing")
    return 1


def main(argv):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):      # the tool's own lines can carry non-ASCII
            stream.reconfigure(encoding="utf-8", errors="replace")
    try:
        if argv[1:] == ["--selftest"]:
            return selftest()
        if argv[1:] == ["--install-spec"]:
            print(install_spec(README.read_text(encoding="utf-8")))
            return 0
        if argv[1:]:
            print(__doc__)
            return CANNOT_RUN_EXIT
        return check()
    except CannotRun as reason:
        print("check_baseline: COULD NOT RUN -- %s" % reason, file=sys.stderr)
        return CANNOT_RUN_EXIT
    except OSError as reason:
        print("check_baseline: COULD NOT RUN -- %s" % reason, file=sys.stderr)
        return CANNOT_RUN_EXIT


if __name__ == "__main__":
    sys.exit(main(sys.argv))
