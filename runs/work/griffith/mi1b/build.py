import json, re, sys
# Build griffith_mi1b.jsonl from std readings. Std tokens: se te to are single signs; s = Griffith's š.
TOK = re.compile(r'\[[^\]]*\]|se|te|to|[aeiouywbpmnñrlḫẖsktqd]|\?|:|#|[0-9]+|\s+')
CORP = {'s': 'S', 'se': 's', 'ñ': 'N', 'ḫ': 'x', 'ẖ': 'X'}
SIGN = re.compile(r'se|te|to|[aeiouywbpmnñrlḫẖsktqd]')

def conv(std):
    words, cur, signs, unc, lost, rest = [], '', 0, 0, 0, 0
    pos = 0
    for m in TOK.finditer(std):
        assert m.start() == pos, (std, pos, std[pos:pos + 10]); pos = m.end()
        t = m.group(0)
        if t.isspace() or t == ':':
            if cur: words.append(cur); cur = ''
        elif t == '?':
            unc += 1
        elif t == '#' or t.isdigit():
            if t.isdigit() and cur: words.append(cur); cur = ''
            words.append(t) if t.isdigit() else None
            cur += '#' if t == '#' else ''
        elif t.startswith('['):
            inner = t[1:-1]
            if inner == '.':
                cur += '.'; lost += 1
            else:
                for s in SIGN.findall(inner):
                    cur += '.'; rest += 1
        else:
            cur += CORP.get(t, t); signs += 1
    assert pos == len(std), (std, pos)
    if cur: words.append(cur)
    return ' '.join(words), signs, unc, lost, rest

rows = json.load(open(sys.argv[1]))
out = []
for r in rows:
    corp, n, u, lost, rest = conv(r['text_std'])
    # '?' after a divider is not a sign; caller writes such cases without '?'
    out.append({"source": "Meroitic Inscriptions I (Griffith 1911)", "item": "archaeologicals19egyp",
                "griffith_no": r['no'], "rem": f"{r['no']:04d}", "page": r['page'], "object": r['object'],
                "site": r['site'], "text_std": r['text_std'], "text_corpus": corp, "uncertain": u, "signs": n,
                "notes": r['notes'] + (f" Lost signs written [.]: {lost}." if lost else '') +
                         (f" Signs restored by Griffith in brackets (not counted, '.' in text_corpus): {rest}." if rest else '')})
with open(sys.argv[2], 'w') as f:
    for o in out: f.write(json.dumps(o, ensure_ascii=False) + '\n')
for o in out: print(o['griffith_no'], o['signs'], o['uncertain'], '|', o['text_corpus'])
print('total signs', sum(o['signs'] for o in out), 'uncertain', sum(o['uncertain'] for o in out))
