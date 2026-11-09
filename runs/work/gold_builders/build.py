import json, re, sys, collections
sys.path.insert(0, sys.argv[1])
from lex_entries import L
C='/Users/mike/repos/mike/meroitic/data/otten/Data/mero-corpus.txt'
txt=open(C,encoding='utf-8',errors='replace').read()
toks=collections.Counter(t for line in txt.split('\n') for t in re.split(r'[\s.]+', line) if t)
def presence(f):
    if not f: return False
    if toks.get(f): return 'token'
    if any(f in t for t in toks): return 'substring'
    return False
out=[]
seen=set()
for e in L:
    assert e['form'] not in seen, e['form']; seen.add(e['form'])
    cf=e['corpus_form']
    e['in_corpus']=presence(cf)
    if e.get('corpus_note','').startswith('absent'): e['in_corpus']=False
    e['corpus_token_count']=toks.get(cf,0) if e['in_corpus'] else 0
    kept=[]
    for v in e['corpus_variants']:
        if v!=cf and presence(v): kept.append(v)
    e['corpus_variants']=kept
    out.append(e)
json.dump(out, open(sys.argv[2],'w',encoding='utf-8'), ensure_ascii=False, indent=2)
print(len(out),'entries ->',sys.argv[2])
c=collections.Counter((e['category'],e['confidence']) for e in out)
for k,v in sorted(c.items()): print(k,v)
print('not in corpus:',[e['form'] for e in out if not e['in_corpus']])
