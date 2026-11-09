"""What the test files share: how a check asks for a local-only file, and the runner.

Data without an open licence is not in the public repo: it is listed in .gitignore and kept on the author's
machine (README, Data). A check that reads such a file calls needs() first, so a clone without the file reports
the check as skipped instead of failed. needs() takes only paths that .gitignore lists: a missing file that the
repo should hold is still a failure.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Skip(Exception):
    """A check that can't run here: a local-only file it reads is absent."""


def ignored():
    """The paths .gitignore lists (its folder and file entries, not the bare name patterns)."""
    lines = [l.strip() for l in (ROOT / ".gitignore").read_text().splitlines()]
    return [l.rstrip("/") for l in lines if l and not l.startswith("#") and "/" in l.rstrip("/")]


def needs(*paths):
    """Skip the calling check unless every path, given from the repo's root, exists."""
    listed = ignored()
    tracked = [p for p in paths if not any(p == g or p.startswith(g + "/") for g in listed)]
    if tracked:
        raise ValueError(f"needs() is for local-only files; .gitignore does not list {', '.join(tracked)}")
    missing = [p for p in paths if not (ROOT / p).exists()]
    if missing:
        raise Skip("needs " + ", ".join(missing))


def run(checks):
    """Run each (name, function), print ok, skip or FAIL for it, and exit 1 if any failed."""
    failed = skipped = 0
    for name, fn in checks:
        try:
            fn()
            print("ok  ", name)
        except Skip as e:
            skipped += 1
            print("skip", name, "-", e)
        except Exception as e:      # noqa: BLE001 - report every failing check, then exit non-zero
            failed += 1
            print("FAIL", name, type(e).__name__, e)
    note = f", {skipped} skipped (local-only data absent: README, Data)" if skipped else ""
    print(f"{len(checks) - failed - skipped}/{len(checks)} passed{note}")
    sys.exit(1 if failed else 0)
