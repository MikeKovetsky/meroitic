"""M4: regularities of word endings in Meroitic texts that are not epitaphs.

Each test takes the table's rows (dicts with text, kind, words_in_text, n, form,
level, parts, gloss) and returns (cases, holds, comparison_rate).
"""

VOWELS = "aeio"


def _usable(r):
    """A word whose signs are all read and which is not a number."""
    return "." not in r["form"] and r["level"] != "number"


def _rate(hits, total):
    return hits / total if total else 0.0


def test_M4_1(rows):
    """The copula -wi at the end of a word follows a vowel o or e (-owi, -ewi)."""
    words = [r["form"] for r in rows if _usable(r) and len(r["form"]) >= 3]
    cases = [f for f in words if f.endswith("wi")]
    holds = sum(1 for f in cases if f[-3] in "oe")
    comp = [f for f in words
            if f[-1] == "i" and f[-2].isalpha() and f[-2] not in VOWELS + "w"]
    comp_hits = sum(1 for f in comp if f[-3] in "oe")
    return len(cases), holds, _rate(comp_hits, len(comp))


def test_M4_2(rows):
    """A word ending in the plural -b has e just before it (-eb: -leb, -seb, -teb)."""
    words = [r["form"] for r in rows if _usable(r) and len(r["form"]) >= 2]
    cases = [f for f in words if f[-1] == "b"]
    holds = sum(1 for f in cases if f[-2] == "e")
    comp = [f for f in words
            if f[-1].isalpha() and f[-1] not in VOWELS + "b"]
    comp_hits = sum(1 for f in comp if f[-2] == "e")
    return len(cases), holds, _rate(comp_hits, len(comp))


def test_M4_3(rows):
    """A word ending in -se is followed by a short word (at most 3 signs)."""
    pairs = []
    for a, b in zip(rows, rows[1:]):
        if (a["text"] == b["text"] and int(b["n"]) == int(a["n"]) + 1
                and _usable(a) and _usable(b)):
            pairs.append((a["form"], b["form"]))
    cases = [(a, b) for a, b in pairs if len(a) >= 3 and a.endswith("se")]
    holds = sum(1 for a, b in cases if len(b) <= 3)
    comp_hits = sum(1 for a, b in pairs if len(b) <= 3)
    return len(cases), holds, _rate(comp_hits, len(pairs))
