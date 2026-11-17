"""Tests of the M3 rules: which letter stands before a word-final ending.

Each function takes rows (list of dicts with the table's columns) and returns
(cases, holds, comparison_rate).
"""


def _pool(rows):
    """Fully read words: level not 'lost' or 'number', no '.' in the form, form not all digits."""
    out = []
    for r in rows:
        f = r["form"]
        if r["level"] in ("lost", "number") or not f or "." in f or f.isdigit():
            continue
        out.append(f)
    return out


def _before_ending(rows, ending, allowed):
    forms = _pool(rows)
    L = len(ending)
    longer = [f for f in forms if len(f) > L]
    cases = [f for f in longer if f.endswith(ending)]
    holds = sum(1 for f in cases if f[-L - 1] in allowed)
    comp = (sum(1 for f in longer if f[-L - 1] in allowed) / len(longer)) if longer else 0.0
    return len(cases), holds, comp


def test_M3_1(rows):
    # -owi stands after l, t or q
    return _before_ending(rows, "owi", set("ltq"))


def test_M3_2(rows):
    # -wi (not the whole word) stands after o or e
    return _before_ending(rows, "wi", set("oe"))


def test_M3_3(rows):
    # final b stands after e
    return _before_ending(rows, "b", set("e"))
