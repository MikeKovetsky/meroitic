"""Tests of the rules in data/sources/grammar/rules2/M2.jsonl.

Each function takes rows (list of dicts with the table's columns) and returns
(cases, holds, comparison_rate), counted on rows alone.
"""

VOWELS = set("aeio")
CONSONANTS = set("bdhklmnNpqrsStwxXy")
LETTERS = VOWELS | CONSONANTS


def _words(rows):
    """Forms usable as whole words: level is not 'lost' and every character is a letter sign."""
    out = []
    for r in rows:
        f = r["form"]
        if r["level"] != "lost" and f and all(ch in LETTERS for ch in f):
            out.append(f)
    return out


def test_M2_1(rows):
    """The sign a stands only at the start of a word."""
    words = _words(rows)
    cases = holds = 0
    for f in words:
        for i, ch in enumerate(f):
            if ch == "a":
                cases += 1
                if i == 0:
                    holds += 1
    letters = sum(len(f) for f in words)
    comparison = len(words) / letters if letters else 0.0
    return cases, holds, comparison


def test_M2_2(rows):
    """After e, i or o inside a word comes a consonant sign, never another vowel sign."""
    words = _words(rows)
    cases = holds = 0
    later = cons_later = 0
    for f in words:
        for i in range(len(f) - 1):
            if f[i] in "eio":
                cases += 1
                if f[i + 1] in CONSONANTS:
                    holds += 1
        for ch in f[1:]:
            later += 1
            if ch in CONSONANTS:
                cons_later += 1
    comparison = cons_later / later if later else 0.0
    return cases, holds, comparison


def test_M2_3(rows):
    """Inside a word the sign q is followed by o or e."""
    words = _words(rows)
    cases = holds = 0
    other = other_oe = 0
    for f in words:
        for i in range(len(f) - 1):
            if f[i] == "q":
                cases += 1
                if f[i + 1] in "oe":
                    holds += 1
            elif f[i] in CONSONANTS:
                other += 1
                if f[i + 1] in "oe":
                    other_oe += 1
    comparison = other_oe / other if other else 0.0
    return cases, holds, comparison


def test_M2_4(rows):
    """A word ending in -wi has a vowel sign (o, e or i) just before the w."""
    words = _words(rows)
    cases = holds = 0
    other = other_v = 0
    for f in words:
        if len(f) < 3 or not f.endswith("i"):
            continue
        if f.endswith("wi"):
            cases += 1
            if f[-3] in "oei":
                holds += 1
        else:
            other += 1
            if f[-3] in "oei":
                other_v += 1
    comparison = other_v / other if other else 0.0
    return cases, holds, comparison


def test_M2_5(rows):
    """Inside a word the sign N (ne) is followed by a consonant sign, never by a vowel sign."""
    words = _words(rows)
    cases = holds = 0
    other = other_c = 0
    for f in words:
        for i in range(len(f) - 1):
            if f[i] == "N":
                cases += 1
                if f[i + 1] in CONSONANTS:
                    holds += 1
            elif f[i] in CONSONANTS:
                other += 1
                if f[i + 1] in CONSONANTS:
                    other_c += 1
    comparison = other_c / other if other else 0.0
    return cases, holds, comparison
