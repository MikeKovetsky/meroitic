"""Counts for rules L4-1 to L4-5 (data/sources/grammar/rules/L4.jsonl).

Each test_L4_k(rows) returns (cases, holds, comparison_rate), counted on rows alone.
"""
import re

_PART = re.compile(r'(\S+?)=(.+?)(?= \S+?=|$)')


def _parts(row):
    return _PART.findall(row['parts'] or '')


def _has(row, entry):
    return any(e == entry for _, e in _parts(row))


def _index(rows):
    return {(r['text'], r['n']): r for r in rows}


def _rate(num, den):
    return num / den if den else 0.0


def test_L4_1(rows):
    cases = holds = cmp_cases = cmp_holds = 0
    for r in rows:
        P = _parts(r)
        for k, (_, e) in enumerate(P):
            if k + 1 >= len(P):
                continue
            nxt_l = P[k + 1][0][:1] == 'l'
            if e == '-te (2)':
                cases += 1
                holds += nxt_l
            elif e[:1].isupper() and e not in ('NAME', 'NUMBER'):
                cmp_cases += 1
                cmp_holds += nxt_l
    return cases, holds, _rate(cmp_holds, cmp_cases)


def _kete_rule(rows, test):
    idx = _index(rows)
    cases = holds = all_true = 0
    for r in rows:
        t = bool(test(r, idx))
        all_true += t
        if _has(r, '-kete'):
            cases += 1
            holds += t
    return cases, holds, _rate(all_true, len(rows))


def test_L4_2(rows):
    return _kete_rule(rows, lambda r, idx: 3 * r['n'] > 2 * r['words_in_text'])


def _l43(r, idx):
    for d in (1, 2):
        w = idx.get((r['text'], r['n'] - d))
        if w is not None:
            f = w['form']
            if 'mX' in f or 'mx' in f or 'mlo' in f or f.startswith('at'):
                return True
    return False


def test_L4_3(rows):
    return _kete_rule(rows, _l43)


def _l44(r, idx):
    w = idx.get((r['text'], r['n'] + 1))
    return w is None or w['form'][:1] in ('a', 'x', 'm')


def test_L4_4(rows):
    return _kete_rule(rows, _l44)


_END = re.compile(r'(te|ke|kes|to)$')
_PS = re.compile(r'^p(i)?S')


def test_L4_5(rows):
    idx = _index(rows)
    cases = holds = all_true = 0
    for r in rows:
        w = idx.get((r['text'], r['n'] + 1))
        t = bool(_END.search(r['form'])) or (w is not None and bool(_END.search(w['form'])))
        all_true += t
        if _PS.match(r['form']) and r['level'] != 'lost' and '.' not in r['form']:
            cases += 1
            holds += t
    return cases, holds, _rate(all_true, len(rows))
