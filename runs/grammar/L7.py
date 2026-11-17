"""Counts for the grammar rules L7-1 to L7-6 (data/sources/grammar/rules/L7.jsonl).

Each function takes rows (list of dicts with keys text, kind, words_in_text, n, form,
level, parts, gloss) and returns (cases, holds, comparison_rate).
"""
import itertools
import re


def _texts(rows):
    """Map text -> {n: form}."""
    out = {}
    for r in rows:
        out.setdefault(r["text"], {})[int(r["n"])] = r["form"]
    return out


def _share(rows, pred):
    forms = [r["form"] for r in rows]
    return sum(1 for f in forms if pred(f)) / len(forms) if forms else 0.0


def _is_off(t, n):
    """Row n has form 'ato' and the next row's form lowercased is 'mxe'."""
    return t.get(n) == "ato" and (t.get(n + 1) or "").lower() == "mxe"


def _is_at(t, n):
    return t.get(n) == "at" and (t.get(n + 1) or "").lower() == "mxe"


def test_L7_1(rows):
    cases = holds = 0
    for t in _texts(rows).values():
        for n, f in t.items():
            if f.lower() == "mxe":
                cases += 1
                nxt = t.get(n + 1)
                if nxt is not None and nxt[:1] in ("p", "b", "y"):
                    holds += 1
    comp = _share(rows, lambda f: f[:1] in ("p", "b", "y"))
    return cases, holds, comp


def test_L7_2(rows):
    cases = holds = 0
    for t in _texts(rows).values():
        a = [n for n in t if _is_off(t, n)]
        b = [n for n in t if _is_at(t, n)]
        if a and b:
            cases += 1
            if min(a) < min(b):
                holds += 1
    return cases, holds, 0.5


def test_L7_3(rows):
    end = re.compile(r"(wi|te|s)$")
    cases = holds = 0
    for t in _texts(rows).values():
        for n in t:
            if n > 1 and _is_off(t, n):
                cases += 1
                prev = t.get(n - 1)
                if prev is not None and end.search(prev):
                    holds += 1
    comp = _share(rows, lambda f: bool(end.search(f)))
    return cases, holds, comp


_MARKERS = [
    ("INV", lambda t, n: t[n].lower().startswith(("wos", "wis"))),
    ("SOR", lambda t, n: t[n].startswith(("Sor", "aSor"))),
    ("QOWI", lambda t, n: t[n].endswith("qowi")),
    ("REL", lambda t, n: t[n].startswith(("teri", "tedx", "tdx", "tereke"))),
    ("OFF", _is_off),
]


def test_L7_4(rows):
    cases = holds = 0
    for t in _texts(rows).values():
        first = {}
        for name, pred in _MARKERS:
            ns = [n for n in t if pred(t, n)]
            first[name] = min(ns) if ns else None
        for (a, _), (b, _) in itertools.combinations(_MARKERS, 2):
            if first[a] is not None and first[b] is not None:
                cases += 1
                if first[a] < first[b]:
                    holds += 1
    return cases, holds, 0.5


def test_L7_5(rows):
    pool = [r["form"] for r in rows if len(r["form"]) >= 4 and "." not in r["form"]]
    case_forms = [f for f in pool if f.endswith("wi")]
    cases = len(case_forms)
    holds = sum(1 for f in case_forms if f[-3] == "o")
    comp = sum(1 for f in pool if f[-3] == "o") / len(pool) if pool else 0.0
    return cases, holds, comp


def test_L7_6(rows):
    xr = re.compile(r"xr|kr")
    cases = holds = n_ato = n_at = 0
    for t in _texts(rows).values():
        for n, f in t.items():
            prev = t.get(n - 1)
            prev2 = t.get(n - 2)
            if prev is None or prev.lower() != "mxe" or prev2 not in ("ato", "at"):
                continue
            cases += 1
            if prev2 == "ato":
                n_ato += 1
                if "X" in f and not xr.search(f):
                    holds += 1
            else:
                n_at += 1
                if xr.search(f):
                    holds += 1
    p_x = _share(rows, lambda f: "X" in f and not xr.search(f))
    p_xr = _share(rows, lambda f: bool(xr.search(f)))
    comp = (n_ato * p_x + n_at * p_xr) / cases if cases else 0.0
    return cases, holds, comp
