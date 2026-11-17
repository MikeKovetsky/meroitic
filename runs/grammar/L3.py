"""Counts for the clause rules L3-1 to L3-8 (data/sources/grammar/rules/L3.jsonl)."""
import random
import re
from collections import OrderedDict

SEED = 20261128
SHUFFLES = 2000

INVOC = re.compile(r'(wo|wi)Si?')
FILIATION = re.compile(r'te?dxe?l|terike?l')


def _texts(rows):
    t = OrderedDict()
    for r in rows:
        t.setdefault(r['text'], []).append(r)
    for k in t:
        t[k].sort(key=lambda r: r['n'])
    return t


def _by_n(text_rows):
    return {r['n']: r for r in text_rows}


def _is_mx(form):
    return form.lower() in ('mxe', 'mx')


def _ben_starts(t, which=('ato', 'at')):
    d = _by_n(t)
    return [r['n'] for r in t
            if r['form'] in which and (r['n'] + 1) in d and _is_mx(d[r['n'] + 1]['form'])]


def _order_rule(rows, get_a, get_b, holds_fn):
    rng = random.Random(SEED)
    cases = holds = 0
    comp = 0.0
    for t in _texts(rows).values():
        a, b = get_a(t), get_b(t)
        if not a or not b:
            continue
        cases += 1
        holds += holds_fn(a, b)
        pos = list(a) + list(b)
        k = 0
        for _ in range(SHUFFLES):
            p = pos[:]
            rng.shuffle(p)
            k += holds_fn(p[:len(a)], p[len(a):])
        comp += k / SHUFFLES
    return cases, holds, (comp / cases if cases else 0.0)


def _first_before(a, b):
    return min(a) < min(b)


def _all_before(a, b):
    return max(a) < min(b)


def test_L3_1(rows):
    cs = [r for r in rows if r['form'] in ('woSi', 'wiSi')]
    h = sum(r['n'] == 1 for r in cs)
    comp = sum(r['n'] == 1 for r in rows) / len(rows) if rows else 0.0
    return len(cs), h, comp


def test_L3_2(rows):
    cases = holds = base = 0
    for t in _texts(rows).values():
        d = _by_n(t)
        for r in t:
            near = any(m in d and INVOC.fullmatch(d[m]['form'])
                       for m in range(r['n'] - 3, r['n']))
            base += near
            if re.fullmatch(r'a?Sor(eyi|iyi|ei|i|e)', r['form']):
                cases += 1
                holds += near
    return cases, holds, (base / len(rows) if rows else 0.0)


def _filiation(t):
    return [r['n'] for r in t if FILIATION.search(r['form'])]


def test_L3_3(rows):
    return _order_rule(rows,
                       lambda t: [r['n'] for r in t if r['form'].endswith('qowi')],
                       _filiation, _first_before)


def test_L3_4(rows):
    return _order_rule(rows, _filiation, _ben_starts, _all_before)


def test_L3_5(rows):
    return _order_rule(rows,
                       lambda t: _ben_starts(t, ('ato',)),
                       lambda t: _ben_starts(t, ('at',)), _first_before)


def _stem_case(v):
    return re.search(r'X|xr|kr', v) is not None


def _agrees(first, v):
    if first == 'ato':
        return 'X' in v and re.search(r'xr|kr', v) is None
    return re.search(r'xr|kr', v) is not None


def test_L3_6(rows):
    cs = []
    pool = []
    for t in _texts(rows).values():
        d = _by_n(t)
        for r in t:
            nx = d.get(r['n'] + 1)
            if _is_mx(r['form']) and nx and _stem_case(nx['form']):
                pool.append(nx['form'])
            if r['form'] in ('ato', 'at') and nx and _is_mx(nx['form']):
                v = d.get(r['n'] + 2)
                if v and _stem_case(v['form']):
                    cs.append((r['form'], v['form']))
    if not cs:
        return 0, 0, 0.0
    h = sum(_agrees(a, v) for a, v in cs)
    pa = sum(_agrees('ato', v) for v in pool) / len(pool) if pool else 0.0
    pb = sum(_agrees('at', v) for v in pool) / len(pool) if pool else 0.0
    na = sum(a == 'ato' for a, _ in cs)
    nb = len(cs) - na
    return len(cs), h, (na * pa + nb * pb) / len(cs)


def test_L3_7(rows):
    cases = holds = 0
    for t in _texts(rows).values():
        d = _by_n(t)
        for r in t:
            if _is_mx(r['form']):
                cases += 1
                nx = d.get(r['n'] + 1)
                holds += bool(nx and nx['form'][:1] in ('p', 'y', 'b'))
    comp = sum(r['form'][:1] in ('p', 'y', 'b') for r in rows) / len(rows) if rows else 0.0
    return cases, holds, comp


def test_L3_8(rows):
    end = re.compile(r'(kete|kte|kes|ketes)$')
    cs = [r for r in rows if end.search(r['form'])]
    h = sum(2 * r['n'] > r['words_in_text'] for r in cs)
    comp = sum(2 * r['n'] > r['words_in_text'] for r in rows) / len(rows) if rows else 0.0
    return len(cs), h, comp
