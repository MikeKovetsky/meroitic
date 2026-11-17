"""Counts for the rules L6-1 to L6-8 (data/sources/grammar/rules/L6.jsonl).

Each function takes the table as a list of dicts (one word each, keys text, kind,
words_in_text, n, form, level, parts, gloss) and returns (cases, holds, comparison_rate).
"""
import re
from collections import OrderedDict
from math import comb


def _texts(rows):
    texts = OrderedDict()
    for r in rows:
        texts.setdefault(r["text"], []).append(r)
    return [sorted(ws, key=lambda w: int(w["n"])) for ws in texts.values()]


def _cls(form):
    if re.search(r"tedx|tdx|edxl|dhel", form):
        return "M"
    if re.search(r"erike|yerik|teorik", form):
        return "P"
    if re.search(r"tmde|tmdl", form):
        return "R"
    return None


def _rate(num, den):
    return num / den if den else 0.0


def test_L6_1(rows):
    cases = holds = 0
    chance = 0.0
    for ws in _texts(rows):
        fs = [w["form"] for w in ws]
        iq = [i for i, f in enumerate(fs) if re.search(r"qo(wi)?$", f) and not _cls(f)]
        ip = [i for i, f in enumerate(fs) if _cls(f)]
        if iq and ip:
            cases += 1
            holds += iq[0] < ip[0]
            chance += len(iq) / (len(iq) + len(ip))
    return cases, holds, _rate(chance, cases)


def test_L6_2(rows):
    cases = holds = 0
    for ws in _texts(rows):
        for i in range(1, len(ws)):
            prev = ws[i - 1]
            if _cls(ws[i]["form"]) in ("M", "P") and not _cls(prev["form"]) and prev["level"] != "lost":
                cases += 1
                holds += prev["level"] == "name"
    pool = [r for r in rows if not _cls(r["form"]) and r["level"] != "lost"]
    return cases, holds, _rate(sum(r["level"] == "name" for r in pool), len(pool))


def test_L6_3(rows):
    cases = holds = tot = tot_r = 0
    for ws in _texts(rows):
        for i in range(1, len(ws)):
            k = _cls(ws[i]["form"])
            if k and not _cls(ws[i - 1]["form"]):
                tot += 1
                tot_r += k == "R"
                if ws[i - 1]["form"].endswith("leb"):
                    cases += 1
                    holds += k == "R"
    return cases, holds, _rate(tot_r, tot)


def test_L6_4(rows):
    cases = holds = 0
    chance = 0.0
    for ws in _texts(rows):
        fs = [w["form"] for w in ws]
        a = [i for i, f in enumerate(fs) if _cls(f) in ("M", "P")]
        b = [i for i, f in enumerate(fs) if _cls(f) == "R"]
        if a and b:
            cases += 1
            holds += min(b) > max(a)
            chance += 1 / comb(len(a) + len(b), len(b))
    return cases, holds, _rate(chance, cases)


def test_L6_5(rows):
    cases = holds = 0
    chance = 0.0
    for ws in _texts(rows):
        fs = [w["form"] for w in ws]
        b = [i for i in range(len(fs) - 1) if fs[i] in ("ato", "at") and fs[i + 1] in ("mXe", "mxe", "mlo")]
        a = [i for i, f in enumerate(fs) if _cls(f)]
        if a and b:
            cases += 1
            holds += min(b) > max(a)
            chance += 1 / comb(len(a) + len(b), len(b))
    return cases, holds, _rate(chance, cases)


def test_L6_6(rows):
    found = []
    for ws in _texts(rows):
        fs = [w["form"] for w in ws]
        for i in range(2, len(fs)):
            if fs[i - 2] in ("ato", "at") and fs[i - 1] in ("mXe", "mxe"):
                xr = bool(re.search(r"xr|kr", fs[i]))
                if xr or "X" in fs[i]:
                    found.append((fs[i - 2] == "at", xr))
    cases = len(found)
    holds = sum(a == x for a, x in found)
    if not cases:
        return 0, 0, 0.0
    pa = sum(a for a, _ in found) / cases
    px = sum(x for _, x in found) / cases
    return cases, holds, pa * px + (1 - pa) * (1 - px)


def _same(a, b):
    return (_cls(b) is not None and _cls(b) == _cls(a)) or a[:3] == b[:3]


def test_L6_7(rows):
    cases = holds = pairs = pairs_same = 0
    for ws in _texts(rows):
        fs = [w["form"] for w in ws]
        for i in range(len(fs) - 1):
            a, b = fs[i], fs[i + 1]
            if "." in a or "." in b:
                continue
            pairs += 1
            pairs_same += _same(a, b)
            if _cls(a) in ("M", "P") and a.endswith("li"):
                cases += 1
                holds += _same(a, b)
    return cases, holds, _rate(pairs_same, pairs)


def test_L6_8(rows):
    cases = holds = 0
    chance = 0.0
    for ws in _texts(rows):
        fs = [w["form"] for w in ws]
        m = [i for i, f in enumerate(fs) if _cls(f) == "M"]
        p = [i for i, f in enumerate(fs) if _cls(f) == "P"]
        if m and p:
            cases += 1
            holds += m[0] < p[0]
            chance += len(m) / (len(m) + len(p))
    return cases, holds, _rate(chance, cases)
