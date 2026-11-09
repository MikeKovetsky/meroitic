import json, glob, re, sys
# build.py: read/*.json (internal codes) -> griffith_mi2a.jsonl
# Internal codes, left to right after reading right to left:
#   a e i o y w b p m n r l k q t d as is; N = ñ (ne); x = ḫ; X = ẖ; S = s-sign (Griffith š); s = se-sign (Griffith s);
#   T = te; O = to (Griffith tê); ':' divider; '?' after a sign = my doubt; '^' after a sign = Griffith's printed '?';
#   '[.]' = lost sign; '[abc]' = signs Griffith restores in brackets (counted as lost, kept in text_std in brackets);
#   '{3}' = a numeral of value 3 (kept as digits in both texts), '{x}' = another non-letter sign (std only);
#   '(5)' = Griffith's superscript stone-line number; '/' = end of a type line (ignored); spaces = Griffith's word spaces.
STD = {'N': 'ñ', 'x': 'ḫ', 'X': 'ẖ', 'S': 's', 's': 'se', 'T': 'te', 'O': 'to'}
COR = {'N': 'N', 'x': 'x', 'X': 'X', 'S': 'S', 's': 's', 'T': 'te', 'O': 'to'}
SIGNS = set('aeioywbpmnrlkqtdNxXSsTO')
def conv(t):
    std, cor, n, unc, gq, mine, rest = [], [], 0, 0, 0, 0, 0
    i = 0
    t = t.replace('/', ' ')
    while i < len(t):
        c = t[i]
        if c in SIGNS:
            std.append(STD.get(c, c)); cor.append(COR.get(c, c)); n += 1
            if i + 1 < len(t) and t[i + 1] in '?^':
                std.append('?'); unc += 1
                if t[i + 1] == '^': gq += 1
                else: mine += 1
                i += 1
        elif c == '[':
            j = t.index(']', i)
            inner = t[i + 1:j]
            if inner == '.':
                std.append('[.]'); cor.append('.')
            else:
                std.append('[' + ''.join(STD.get(k, k) for k in inner) + ']')
                cor.append('.' * sum(1 for k in inner if k in SIGNS)); rest += sum(1 for k in inner if k in SIGNS)
            i = j
        elif c == '{':
            j = t.index('}', i)
            inner = t[i + 1:j]
            std.append(inner if inner.isdigit() else '{' + inner + '}')
            if inner.isdigit(): cor.append(inner)
            i = j
        elif c == '(':
            j = t.index(')', i)
            std.append(t[i:j + 1]); i = j
        elif c == ':':
            std.append(' : '); cor.append(' ')
        elif c == ' ':
            std.append(' '); cor.append(' ')
        else:
            raise ValueError(f'bad char {c!r} in {t!r}')
        i += 1
    s = re.sub(r'\s+', ' ', ''.join(std)).strip()
    s = re.sub(r'\s+:', ' :', s)
    c = re.sub(r'\s+', ' ', ''.join(cor)).strip()
    return s, c, n, unc, gq, mine, rest
rows = []
for f in sorted(glob.glob('/private/tmp/claude-501/griffith_scripts/mi2a/read/*.json')):
    r = json.load(open(f))
    text = ' / '.join(r['lines'])
    s, c, n, unc, gq, mine, rest = conv(text)
    note = r.get('notes', '')
    note += f" [Signs read: {n}; marked '?': {unc} ({gq} carry Griffith's printed '?', {mine} are my doubts)"
    note += f"; {rest} signs restored by Griffith in brackets, not counted]." if rest else "]."
    note += " '(n)' in text_std is Griffith's superscript stone-line number."
    rows.append(dict(source='Meroitic Inscriptions II (Griffith 1912)', item='archaeologicals20egyp',
                     griffith_no=r['griffith_no'], rem=r['rem'], page=r['page'], object=r['object'], site=r['site'],
                     text_std=s, text_corpus=c, uncertain=unc, signs=n, notes=note.strip(), _k=(r['griffith_no'], r['rem'])))
rows.sort(key=lambda r: r['_k'])
out = sys.argv[1] if len(sys.argv) > 1 else '/Users/mike/repos/mike/meroitic/data/expansion/griffith_mi2a.jsonl'
with open(out, 'w') as fh:
    for r in rows:
        r.pop('_k'); fh.write(json.dumps(r, ensure_ascii=False) + '\n')
tn = sum(r['signs'] for r in rows); tu = sum(r['uncertain'] for r in rows)
print(out, len(rows), 'rows', tn, 'signs', tu, 'uncertain', f'{100*tu/max(tn,1):.1f}%')
for r in rows: print(r['rem'], r['signs'], r['uncertain'], r['text_corpus'][:90])
