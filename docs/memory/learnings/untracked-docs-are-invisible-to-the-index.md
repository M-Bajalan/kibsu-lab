---
type: learning
---

# A document git does not know yet does not exist for kibsu

`python -m kibsu index .` builds the index from `git ls-files`. A Markdown file that has
been written but not yet added to git is not in that list, so it is not in the index, so
every line `report` derives from the index reads as if the file had never been written.

Found on 2026-10-12, by a check failing to fail. `tools/check_baseline.py` was written to
compare `README.md`'s Baseline block with what the tool prints, and its plan
(`docs/plans/2026-10-12-baseline-check.md`) predicted that its first real run would exit 1:
the plan file itself was an eighteenth document, and the page said seventeen. The run exited
0. The page was "right" only because the new file was untracked. After `git add`, the same
command exited 1 on exactly the line predicted.

**Check this first whenever a count from `report` looks one short, or a check passes that
you expected to fail right after adding a file:**

```
git ls-files --others --exclude-standard -- "*.md"
```

Anything it prints is invisible to the index. `git add` it, rebuild the index, and run the
check again:

```
python -m kibsu index .
python tools/check_baseline.py
```

Two consequences worth keeping:

- **A check run before `git add` passes for the wrong reason.** The commit that follows is
  then the first moment the page is wrong, and nothing ran after it. `tools/check_baseline.py`
  now names untracked Markdown files in its output and says its verdict does not cover them.
- **This is not a defect in the index.** A fresh clone holds only what git tracks, and the
  Baseline is defined as what a fresh clone prints. Reading `git ls-files` is what makes the
  two agree. The trap is in the working tree, not in the tool.
