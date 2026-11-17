"""Counts for the rules in data/sources/grammar/rules2/M1.jsonl.

Each function takes the table as a list of dicts (keys text, kind, words_in_text,
n, form, level, parts, gloss) in table order and returns
(cases, holds, comparison_rate).
"""

VOWELS = set("aeio")


def _whole(form):
    """A form with no lost signs that is not a numeral."""
    return bool(form) and "." not in form and not form.isdigit()


def _next_in_text(rows, i):
    if i + 1 < len(rows) and rows[i + 1]["text"] == rows[i]["text"]:
        return rows[i + 1]
    return None


def test_M1_1(rows):
    """A word ending in -se is followed by a short word (at most 3 letters)."""
    cases = holds = 0
    base_n = base_h = 0
    for i, r in enumerate(rows):
        f = r["form"]
        nxt = _next_in_text(rows, i)
        if not _whole(f) or nxt is None or not _whole(nxt["form"]):
            continue
        short = len(nxt["form"]) <= 3
        base_n += 1
        base_h += short
        if len(f) >= 3 and f.endswith("se"):
            cases += 1
            holds += short
    rate = base_h / base_n if base_n else 0.0
    return cases, holds, rate


def test_M1_2(rows):
    """A word ending in the letter b has e just before it (-eb)."""
    cases = holds = 0
    base_n = base_h = 0
    for r in rows:
        f = r["form"]
        if not _whole(f) or len(f) < 3:
            continue
        if f[-1] == "b":
            cases += 1
            holds += f[-2] == "e"
        elif f[-1] not in VOWELS:
            base_n += 1
            base_h += f[-2] == "e"
    rate = base_h / base_n if base_n else 0.0
    return cases, holds, rate
