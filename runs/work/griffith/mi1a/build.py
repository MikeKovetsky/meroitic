import json, re, sys
# build.py draft.jsonl out.jsonl: derive text_corpus, uncertain, signs from text_std.
# Square brackets = Griffith's restorations: kept in text_std, written as one '.' per sign in text_corpus,
# and not counted as signs read (same convention as griffith_mi1b.jsonl).
SIGN = re.compile(r'se|te|to|[aeiouywbpmnñrlḫẖsktqd]')
MAP = {'se': 's', 's': 'S', 'ñ': 'N', 'ḫ': 'x', 'ẖ': 'X'}
def strip_marks(t):
    t = re.sub(r'\(\d+\)', '', t)                 # Griffith's stone column numbers
    return t.replace('(', '').replace(')', '')    # round brackets: word found only in some copies
def blank(m):                                     # restored signs -> one '.' each, dividers kept
    return SIGN.sub('.', m.group(1).replace('?', ''))
def corpus(t):
    t = strip_marks(t).replace('[.]', '.')
    t = re.sub(r'\[([^\]]*)\]', blank, t)
    t = t.replace('?', '')
    t = t.replace(' | ', ' ').replace('|', '')     # ' | ' ends a word, a bare '|' joins it
    t = t.replace(':', ' ')
    return ' '.join(SIGN.sub(lambda m: MAP.get(m.group(0), m.group(0)), w) for w in t.split())
def count(t):
    t = strip_marks(t).replace('[.]', ' ')
    t = re.sub(r'\[[^\]]*\]', ' ', t)             # restorations are not read signs
    toks = list(SIGN.finditer(t))
    return len(toks), sum(1 for m in toks if t[m.end():m.end() + 1] == '?')
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
with open(sys.argv[2], 'w') as f:
    for r in rows:
        n, u = count(r['text_std'])
        o = {"source": "Meroitic Inscriptions I (Griffith 1911)", "item": "archaeologicals19egyp",
             "griffith_no": r['no'], "rem": f"{r['no']:04d}", "page": r['page'], "object": r['object'],
             "site": r['site'], "text_std": r['text_std'], "text_corpus": corpus(r['text_std']),
             "uncertain": u, "signs": n, "notes": r['notes']}
        f.write(json.dumps(o, ensure_ascii=False) + '\n')
        print(o['griffith_no'], n, u, '|', o['text_std'], '=>', o['text_corpus'])
