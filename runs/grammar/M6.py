"""Rule tests for brief M6 (frames that repeat). Each test returns (cases, holds, comparison_rate)."""
import random
import re

_LETTERS = re.compile(r'[A-Za-z]+')


def _word(form):
    """True when the form is a whole written word: letters only (no lost sign '.', no digit)."""
    return _LETTERS.fullmatch(form) is not None


def _texts(rows):
    """The rows grouped by text, each text's words in table order."""
    order, groups = [], {}
    for r in rows:
        t = r['text']
        if t not in groups:
            groups[t] = []
            order.append(t)
        groups[t].append(r['form'])
    return [groups[t] for t in order]


def test_M6_1(rows):
    """-owi stands after l or t (-lowi, -towi)."""
    cases = holds = 0
    for r in rows:
        f = r['form']
        if _word(f) and len(f) >= 4 and f.endswith('owi'):
            cases += 1
            holds += f[-4] in 'lt'
    n = hit = 0
    for r in rows:
        f = r['form']
        if _word(f) and len(f) >= 4:
            n += 1
            hit += f[-4] in 'lt'
    return cases, holds, (hit / n if n else 0.0)


def test_M6_2(rows):
    """A word-final -wi stands after the vowel o or e."""
    cases = holds = 0
    for r in rows:
        f = r['form']
        if _word(f) and len(f) >= 3 and f.endswith('wi'):
            cases += 1
            holds += f[-3] in 'oe'
    n = hit = 0
    for r in rows:
        f = r['form']
        if _word(f) and len(f) >= 3:
            n += 1
            hit += f[-3] in 'oe'
    return cases, holds, (hit / n if n else 0.0)


def _frame_count(texts):
    cases = holds = 0
    for f in texts:
        occ = {}
        for i, x in enumerate(f):
            if _word(x):
                occ.setdefault(x, []).append(i)
        for ii in occ.values():
            if len(ii) < 2:
                continue
            for i in ii:
                cases += 1
                ok = False
                for j in ii:
                    if j == i:
                        continue
                    for d in (-1, 1):
                        a, b = i + d, j + d
                        if 0 <= a < len(f) and 0 <= b < len(f) and f[a] == f[b]:
                            ok = True
                if ok:
                    holds += 1
    return cases, holds


def test_M6_3(rows):
    """A word that recurs in a text comes back inside the same frame: same neighbour on one side."""
    texts = _texts(rows)
    cases, holds = _frame_count(texts)
    rng = random.Random(20261128)
    shuffled = []
    for f in texts:
        g = list(f)
        rng.shuffle(g)
        shuffled.append(g)
    c2, h2 = _frame_count(shuffled)
    return cases, holds, (h2 / c2 if c2 else 0.0)
