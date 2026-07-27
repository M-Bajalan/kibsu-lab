---
type: upstream-issue-draft
---

# Draft: kibsu issue -- existence-mode history backtest returns no verdict when `index_path` lives outside `docs_root`

**Status: NOT YET FILED.** This is a reproduction and a proposed issue write-up, prepared so a
human can review it and file it on the real, public `kibsu` repository. Until it is actually
filed there and has an issue number, nothing in this repo should claim it "was filed upstream" --
see `README.md`'s baseline section, which now links here instead of making that claim.

## Reproduction

```
git clone <kibsu-lab> c && cd c
python tools/generate_data.py
python -m kibsu index .
python -m kibsu report .
```

The fifth check ("Follow your own rules") prints:

```
?  Follow your own rules      COULD NOT CHECK - the history replay returned no
                               verdict (no git history here, or a shallow clone).
```

Reproducing the exact underlying command by hand:

```
python -m kibsu check . --all --index .kibsu/index.json \
  --backtest 200 --backtest-index .kibsu/index.json --backtest-mode existence
```

prints:

```
0 of 7 commits touched a .md under .kibsu/ -- nothing to test.
```

That is the literal cause: existence-mode backtest is scoping "touched" files to the **directory
the index file itself lives in** (here, `.kibsu/`) rather than to the repo's configured
`docs_root` (`docs`) / `skills_dir` (`skills`) / `instruction_files`. No commit in this repo's
history touches a `.md` file under `.kibsu/` -- of course not, that directory holds the
*generated* index, not the *tracked* docs the backtest is supposed to be replaying history
against. So the check has nothing to test and reports COULD NOT CHECK, correctly by its own
logic, against the wrong file set.

**This is not specific to this repo's config shape.** kibsu's own `config.py` DEFAULTS ship
`docs_root="docs"` and `index_path=".kibsu/index.json"` -- the default index path already lives
outside the default docs root. Any repo that accepts kibsu's own defaults and has real git
history should reproduce the same COULD NOT CHECK, for the same reason.

(Before indexing, the same slot in the report prints a different message --
`COULD NOT CHECK - no index file to check history against` -- which is expected and not part of
this finding; it just means no index exists yet.)

## Proposed issue

**Title:** `check --backtest-mode existence` scopes "touched" files to `dirname(--backtest-index)` instead of `docs_root`/`skills_dir` -- backtest reports nothing to test on kibsu's own default config shape

**Body:**

> `kibsu report` calls `check --all --backtest N --backtest-index <path> --backtest-mode existence`
> internally to answer "does history replay agree with the current index." In existence mode,
> the backtest appears to only consider commits that touched a `.md` file under the *directory
> containing the index file* (`dirname(index_path)`), rather than the repo's configured
> `docs_root` / `skills_dir` / `instruction_files`.
>
> Because kibsu's own `DEFAULTS` set `index_path=".kibsu/index.json"` while `docs_root="docs"`,
> this means the backtest scopes to `.kibsu/` -- a directory that, by design, holds the
> *generated* index, not tracked documentation -- so on a repo using kibsu's own defaults, the
> backtest finds 0 relevant commits and `report` always reports the fifth check as
> COULD NOT CHECK, regardless of how well-governed the repo actually is.
>
> **Repro:** clone any repo using kibsu's default `.kibsu.json` shape, run
> `python -m kibsu index .`, then `python -m kibsu check . --all --index .kibsu/index.json
> --backtest 200 --backtest-index .kibsu/index.json --backtest-mode existence`. Expect it to
> replay history against `docs_root`; observe it print "0 of N commits touched a .md under
> `.kibsu/` -- nothing to test" instead.
>
> **Suggested fix direction:** scope the existence-mode backtest's "touched" filter to
> `docs_root` + `skills_dir` + `instruction_files` (the same file set `index` itself walks),
> not to the directory the index artifact happens to be written into.
>
> Environment: kibsu 0.1.0 from PyPI, reproduced against a `kibsu-lab` clone (a public test
> fixture repo) with 8+ real commits and no shallow clone involved.

## Who files it

Fable/the verifier owns the actual filing on the public kibsu repository and will record the
resulting issue number back to this repo once filed -- see `_relay_opus-to-fable.md` in the
governing workspace.
