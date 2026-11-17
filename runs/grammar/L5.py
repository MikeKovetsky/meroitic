"""Counts for the rules L5-1 to L5-6 (data/sources/grammar/rules/L5.jsonl)."""
import re
from collections import defaultdict


def _index(rows):
    t = defaultdict(dict)
    for r in rows:
        t[r['text']][int(r['n'])] = r
    return t


def _ok(r):
    return r is not None and r['level'] != 'lost'


def _entries(r):
    return [p.split('=', 1)[1] for p in r['parts'].split() if '=' in p]


def _bare(r):
    return not any(e.startswith('-') or e == 'ending' for e in _entries(r)[1:])


def _share(rows, pred):
    fs = [r['form'] for r in rows if r['level'] != 'lost']
    return sum(1 for f in fs if pred(f)) / len(fs) if fs else 0.0


def test_L5_1(rows):
    t = _index(rows)
    cases = holds = b = bn = 0
    for d in t.values():
        for n, w in d.items():
            if w['level'] in ('lost', 'number'):
                continue
            bn += 1
            b += _bare(w)
            nb = (d.get(n - 1), d.get(n + 1))
            if any(x is not None and x['level'] == 'number' for x in nb):
                cases += 1
                holds += _bare(w)
    return cases, holds, (b / bn if bn else 0.0)


def test_L5_2(rows):
    t = _index(rows)
    cases = holds = 0
    for d in t.values():
        a = [n for n, w in d.items() if w['form'] == 'ato']
        b = [n for n, w in d.items() if w['form'] == 'at']
        if a and b:
            cases += 1
            holds += min(a) < min(b)
    return cases, holds, 0.5


def _next_rule(rows, forms, pat, step):
    t = _index(rows)
    cases = holds = 0
    for d in t.values():
        for n, w in d.items():
            nb = d.get(n + step)
            if w['form'] in forms and _ok(nb):
                cases += 1
                holds += bool(re.search(pat, nb['form']))
    return cases, holds, _share(rows, lambda f: bool(re.search(pat, f)))


def test_L5_3(rows):
    return _next_rule(rows, ('ato', 'at'), r'^m', 1)


def test_L5_4(rows):
    return _next_rule(rows, ('mXe', 'mxe'), r'^p', 1)


def test_L5_5(rows):
    t = _index(rows)
    cases = holds = n_ato = n_at = n_x = n_xr = 0
    for d in t.values():
        for n, w in d.items():
            m, v = d.get(n + 1), d.get(n + 2)
            if w['form'] in ('ato', 'at') and m is not None and m['form'] in ('mXe', 'mxe') and _ok(v):
                f = v['form']
                is_xr = 'xr' in f
                is_x = (not is_xr) and bool(re.search('[Xx]', f))
                cases += 1
                n_ato += w['form'] == 'ato'
                n_at += w['form'] == 'at'
                n_x += is_x
                n_xr += is_xr
                holds += (w['form'] == 'ato' and is_x) or (w['form'] == 'at' and is_xr)
    if not cases:
        return 0, 0, 0.0
    comp = (n_ato / cases) * (n_x / cases) + (n_at / cases) * (n_xr / cases)
    return cases, holds, comp


def test_L5_6(rows):
    return _next_rule(rows, ('at',), r'(^p|te$|s$)', -1)
