"""Counts for rules L2-1 to L2-8 (data/sources/grammar/rules/L2.jsonl).

Each test_L2_k(rows) returns (cases, holds, comparison_rate), counted on rows alone.
rows: list of dicts in table order with keys text, kind, words_in_text, n, form, level, parts, gloss.
"""
import re

PS = re.compile(r'^(piS|peS|pS|bS|ps)')
END = re.compile(r'(kete|kte|te|to|kes|kese|ketes|ks|ktes)$')
MXE = re.compile(r'm[Xx][eo]?')          # used with fullmatch
MXE_END = re.compile(r'm[Xx][eo]?$')
XOL = re.compile(r'(Xol|Xl|Xool|ql)')


def _texts(rows):
    """Rows grouped by text, in order of first appearance, row order kept."""
    groups = {}
    for r in rows:
        groups.setdefault(r['text'], []).append(r)
    return list(groups.values())


def _clean(w):
    return '.' not in w['form'] and w['level'] != 'lost'


def _rate(h, c):
    return h / c if c else 0.0


def _rest(form):
    """Letters after the ps- prefix, one leading i or o skipped; also returns that vowel."""
    s = form[PS.match(form).end():]
    v = s[0] if s[:1] in ('i', 'o') else ''
    return v, s[len(v):]


def _is_x(s):
    return bool(re.match(r'[Xx]', s)) and not s.startswith('xr')


def _is_r(s):
    return s.startswith('xr') or s.startswith('kr')


def _ps_word(w):
    f = w['form']
    return _clean(w) and len(f) >= 4 and bool(PS.match(f)) and w['level'] != 'name'


def _verb(w):
    f = w['form']
    return (_clean(w) and len(f) >= 4 and bool(END.search(f))
            and (bool(PS.match(f)) or bool(XOL.search(f))))


def test_L2_1(rows):
    def holds(noun, f):
        if noun == 'ato':
            return bool(re.search('[Xx]', f)) and 'xr' not in f and 'kr' not in f
        return 'xr' in f or 'kr' in f
    cases = []
    for ws in _texts(rows):
        for i, w in enumerate(ws):
            if (i >= 2 and _clean(w) and len(w['form']) >= 4
                    and MXE.fullmatch(ws[i - 1]['form'])
                    and ws[i - 2]['form'] in ('ato', 'at')):
                cases.append((ws[i - 2]['form'], w['form']))
    h = sum(holds(a, b) for a, b in cases)
    nouns = [a for a, _ in cases]
    forms = [b for _, b in cases]
    pairs = len(nouns) * len(forms)
    comp = _rate(sum(holds(a, b) for a in nouns for b in forms), pairs)
    return len(cases), h, comp


def test_L2_2(rows):
    c = h = 0
    for ws in _texts(rows):
        for i, w in enumerate(ws):
            if i > 0 and _ps_word(w):
                c += 1
                h += bool(MXE_END.search(ws[i - 1]['form']))
    comp = _rate(sum(bool(MXE_END.search(r['form'])) for r in rows), len(rows))
    return c, h, comp


def test_L2_3(rows):
    words = [w['form'] for w in rows if _ps_word(w)]
    c = h = 0
    allx = 0
    for f in words:
        v, s = _rest(f)
        allx += _is_x(s)
        if v == 'o':
            c += 1
            h += _is_x(s)
    return c, h, _rate(allx, len(words))


def test_L2_4(rows):
    c = h = 0
    for w in rows:
        f = w['form']
        if _clean(w) and XOL.search(f) and END.search(f):
            c += 1
            h += not PS.match(f)
    bc = bh = 0
    for ws in _texts(rows):
        for i, w in enumerate(ws):
            f = w['form']
            if (i > 0 and MXE.fullmatch(ws[i - 1]['form']) and _clean(w)
                    and len(f) >= 4 and END.search(f)):
                bc += 1
                bh += not PS.match(f)
    return c, h, _rate(bh, bc)


def test_L2_5(rows):
    kk = lambda f: bool(re.search(r'k(e)?te$', f))
    c = h = xc = xh = 0
    for w in rows:
        f = w['form']
        if _ps_word(w) and f.endswith('te'):
            _, s = _rest(f)
            if _is_r(s):
                c += 1
                h += kk(f)
            elif _is_x(s):
                xc += 1
                xh += kk(f)
    return c, h, _rate(xh, xc)


def test_L2_6(rows):
    c = h = 0
    for ws in _texts(rows):
        for i, w in enumerate(ws):
            if (w['form'] == 'ato' and i > 0 and i + 1 < len(ws)
                    and MXE.fullmatch(ws[i + 1]['form'])
                    and '.' not in ws[i - 1]['form']):
                c += 1
                h += ws[i - 1]['form'].endswith('i')
    fun = [r['form'] for r in rows if r['kind'] == 'funerary' and '.' not in r['form']]
    return c, h, _rate(sum(f.endswith('i') for f in fun), len(fun))


def test_L2_7(rows):
    hb = lambda f: bool(re.search(r'bx|b(kes|kete|te)$', f))
    c = h = oc = oh = 0
    for ws in _texts(rows):
        for i, w in enumerate(ws):
            if not _verb(w):
                continue
            j = i - 1
            while j >= 0 and not ws[j]['form'].endswith('wi'):
                j -= 1
            if j < 0:
                continue
            if ws[j]['form'].endswith('bkwi'):
                c += 1
                h += hb(w['form'])
            else:
                oc += 1
                oh += hb(w['form'])
    return c, h, _rate(oh, oc)


def test_L2_8(rows):
    c = h = n = s = 0
    for ws in _texts(rows):
        prev = None
        for w in ws:
            if not _verb(w):
                continue
            f = w['form']
            n += 1
            s += f.endswith('s')
            if prev is not None and prev.endswith('s'):
                c += 1
                h += f.endswith('s')
            prev = f
    return c, h, _rate(s, n)
