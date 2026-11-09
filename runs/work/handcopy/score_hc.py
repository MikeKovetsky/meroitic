import re, json, sys
# Sign-level scoring of the blind hand-copy readings (readings_frozen_*.md) against FHN III (REM text).
src = open('/private/tmp/claude-501/griffith_scripts/score.py').read().split('# Mine:')[0]
ns = {}; exec(src, ns); _toks, align = ns['toks'], ns['align']
def toks(s):
    return _toks(re.sub(r'\(([^\d)]+)\)', r'\1', s))

def frozen(rem):
    t = open('readings.md', encoding='utf-8').read()
    blk = t.split('## Kar. ')
    for b in blk:
        if '(REM %s)' % rem in b: return b.split('\n')[1].strip()
    raise KeyError(rem)

FHN = {
 '0247': 'qo Ḫwitrorqo peseto Akiñtelo nk Akiñtelo ḫrpḫñ Ph̲rsetelo lh̲ smlo Woto tbqo Tmñtelo qore deklo amoke Nlotilo mlomrse Akiñtelo womnith̲ Akiñtelo ant boqḫw dik Pedemeyotito pqr qorise Atmetñ tbo yetmdelo Sotnkel yetmdelo Tbḫemḫr yetmdelo Litḫror yetmdelo kdi akw knw ḫte kke s destel mteto qorese mle Dewekdil mteto arwtl mteto mlolo Tebwe wwikelo',
 '0277': 'Wosi Asoreyi Mlotonqowi ḫdḫiye tedḫelowi dk*retr*i Smedtli terikelowi peseto Akiñtelowi bel*i*l*oke Nptetelowi womnise krorolowi ato mh̲e ph̲te at mh̲e ps(i) ḫr kete ḫ *mlol p h̲ol kete',
 '0278': 'Wosi Asoreyi Ñtewitrqowi dkretri Msidt terikelowi Mlitrqide ted(ḫ)elowi pesto Akiñtelowi wleke krorolowi sekesekiñ ssimetelowi smrso krorolo absolowi qorbtowi nbr wñli ipḫetelo wi pqrl yetmdelowi atomh̲e psih̲ete atmh̲e psḫrkte ḫmlol yidetedikte ḫh̲ll psiplte',
 # REM 0321: only the parts the spout copy covers (lines 1, 7-8, 14-15, 21-22), in order
 '0321': '(W)osi Sore ant Boq(ḫ)w dik Pe roh̲eleb btesw kete ḫ mlol h̲ol kete',
}
MINE = {k: frozen(k) for k in FHN}
# Tokenizer fixes only (the reading is unchanged): where I wrote t+e or s(sh)+e as two signs, the tokenizer would
# merge them into the te / se sign. 0247 'arwte' = a r w t e (signs ·ϟ S); 0321 'ḫseo' = ḫ s e o (signs 3 S).
MINE['0247'] = MINE['0247'].replace('arwte', 'arwt e'); MINE['0321'] = MINE['0321'].replace('ḫseo', 'ḫs eo')
# 0321: drop break marks only; the spout pieces are compared in order
# 0277 with the two last words in the order the copy runs (my write-up swapped them): reported separately
MINE['0277_order'] = MINE['0277'].replace('pq?lkete : ḫblol? :', 'ḫblol? : pq?lkete :')
FHN['0277_order'] = FHN['0277']

def words(s):
    s = re.sub(r'\[=[^\]]*\]', ' ', s); s = re.sub(r'\(\d+\)', '', s)
    s = re.sub(r'\(([^)]*)\)', r'\1', s); s = s.replace('*', '')
    return [w for w in re.split(r'[\s,:|]+', s) if toks(w)]

res = {}
for k in ['0247', '0277', '0278', '0321', '0277_order']:
    a, b = toks(MINE[k]), toks(FHN[k])
    d, ops = align(a, b)
    ws = words(FHN[k]); spans = []; p = 0
    for w in ws:
        n = len(toks(w)); spans.append((p, p + n, w)); p += n
    assert p == len(b), (k, p, len(b))
    bad = set()
    for op, x, y, j in ops:
        for wi, (s0, s1, w) in enumerate(spans):
            if s0 <= j < s1 or (op == 'ins' and j == s1 and False): bad.add(wi)
    # an insertion before FHN index j is charged to the word holding j (or the previous word at a word end)
    for op, x, y, j in ops:
        if op == 'ins':
            for wi, (s0, s1, w) in enumerate(spans):
                if s0 < j <= s1: bad.add(wi); break
    unc = sum(1 for t in re.findall(r'[^\s:|]\?', MINE[k]))
    res[k] = dict(mine_signs=len(a), fhn_signs=len(b), err=d, right=len(b) - d, pct=round(100 * (len(b) - d) / len(b), 1),
                  words=len(ws), words_ok=len(ws) - len(bad), unc_marks=unc,
                  ops=[(o, x, y, spans[[i for i, s in enumerate(spans) if s[0] <= min(j, len(b) - 1) < s[1]][0]][2]) for o, x, y, j in ops])
for k, r in res.items():
    print(k, {x: r[x] for x in r if x != 'ops'})
    for o in r['ops']: print('    ', o)
T = [sum(res[k][x] for k in ['0247', '0277', '0278', '0321']) for x in ('fhn_signs', 'right', 'words', 'words_ok', 'mine_signs', 'unc_marks')]
print('TOTAL fhn_signs %d right %d (%.1f%%) words %d ok %d (%.1f%%) mine_signs %d unc %d' % (T[0], T[1], 100*T[1]/T[0], T[2], T[3], 100*T[3]/T[2], T[4], T[5]))
json.dump(res, open('score_hc.json', 'w'), ensure_ascii=False, indent=1)
