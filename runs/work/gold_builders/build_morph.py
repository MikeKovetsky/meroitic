import json, re, sys, collections
sys.path.insert(0, sys.argv[1])
from morph_entries import M
C='/Users/mike/repos/mike/meroitic/data/otten/Data/mero-corpus.txt'
txt=open(C,encoding='utf-8',errors='replace').read()
toks=collections.Counter(t for line in txt.split('\n') for t in re.split(r'[\s.]+', line) if t)
for e in M:
    cf=e.get('corpus_form')
    if cf:
        e['corpus_variants']=[v for v in e['corpus_variants'] if v!=cf and any(v in t for t in toks)]
json.dump(M, open(sys.argv[2],'w',encoding='utf-8'), ensure_ascii=False, indent=2)
print(len(M),'morphemes ->',sys.argv[2])
print(collections.Counter(e['confidence'] for e in M))
