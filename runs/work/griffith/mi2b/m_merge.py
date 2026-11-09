import json, sys, glob
sys.path.insert(0, '/private/tmp/claude-501/griffith_scripts/mi2b')
from mkrows import conv
KEYS = ["source", "item", "griffith_no", "rem", "page", "object", "site", "text_std", "text_corpus", "uncertain", "signs", "notes"]
files = ['rows_106_111.jsonl', 'rows_110_118.jsonl', 'rows_119_120_126_128.jsonl', 'rows_121_122_124.jsonl',
         'rows_123_125.jsonl', 'rows_129_137.jsonl']

EXTRA = {
    110: "Cross-check: FHN III no. 267 (pp. 1026-1027) reads '(1)qo ḫb(2)ḫilẖ (3)Mst(4)rq(5)ye(6)qo': i where Griffith's type has e (zoomed at 4x, mi2b/a_110z.png: the sign is the e sign, not i); the rest agrees.",
    111: "Cross-check: FHN III no. 267 (pp. 1026-1027) starts its lines 5 and 10 at qer and pibr, as Griffith's superscripts do, and reads pḫeq*leb without the o that Griffith's type has in qoleb.",
    114: "FHN III (comments on Esmêtakhom's graffito, PDF p. 378) counts REM 0114, 0116 and 0117 among the Meroitic proskynemata of a family of Isis priests attested at Philae between AD 408/9 and 456/7.",
    116: "FHN III (comments on Esmêtakhom's graffito, PDF p. 378) counts REM 0114, 0116 and 0117 among the Meroitic proskynemata of a family of Isis priests attested at Philae between AD 408/9 and 456/7.",
    117: "FHN III (comments on Esmêtakhom's graffito, PDF p. 378) counts REM 0114, 0116 and 0117 among the Meroitic proskynemata of a family of Isis priests attested at Philae between AD 408/9 and 456/7.",
    126: "Cross-check: FHN III (PDF p. 153) lists REM 0126 (Moscow, Pushkin Museum, Griffith 1912, 53) among the documents of Natakamani, for his Son-of-Rê name in cursive, which agrees with ntkmn[i] here.",
    127: "Cross-check: FHN II (PDF p. 320) lists REM 0127 (Louvre 11157B, sandstone statuette of a lion-headed god, Griffith 1912, Pl. XLI/127) among the documents of Tañyidamani, which agrees with tñyidm[ni] here.",
    132: "Cross-check: FHN III (PDF p. 196) names the lady Aretroye, mother of a strategus (pelmos), as attested only in REM 0132, 'from Faras', which agrees with the o of aretroye here and gives the find-place Griffith does not state.",
}
SITE = {132: "Not stated by Griffith; FHN III (PDF p. 196) gives REM 0132 as from Faras"}
rows = {}
for f in files:
    for l in open(f):
        r = json.loads(l)
        assert list(r.keys()) == KEYS, (f, list(r.keys()))
        n = r['griffith_no']
        assert n not in rows, ('dup', n)
        corpus, signs, unc = conv(r['text_std'])
        assert (corpus, signs, unc) == (r['text_corpus'], r['signs'], r['uncertain']), (n, corpus, signs, unc)
        assert r['rem'] == f'{n:04d}' and r['source'] == 'Meroitic Inscriptions II (Griffith 1912)' and r['item'] == 'archaeologicals20egyp'
        if n in EXTRA: r['notes'] = r['notes'] + ' ' + EXTRA[n]
        if n in SITE: r['site'] = SITE[n]
        rows[n] = r
missing = [n for n in range(106, 138) if n not in rows]
out = '/Users/mike/repos/mike/meroitic/data/expansion/griffith_mi2b.jsonl'
with open(out, 'w') as fo:
    for n in sorted(rows):
        fo.write(json.dumps(rows[n], ensure_ascii=False) + '\n')
S = sum(r['signs'] for r in rows.values()); U = sum(r['uncertain'] for r in rows.values())
print('rows', len(rows), 'signs', S, 'uncertain', U, f'{100*U/S:.2f}%', 'missing', missing)
for n in sorted(rows):
    print(n, rows[n]['signs'], rows[n]['uncertain'])
