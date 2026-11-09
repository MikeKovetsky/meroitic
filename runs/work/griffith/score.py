import re, json, sys
# Sign-level scoring: my blind readings of Griffith's type vs FHN III no. 267 (REM transliteration).
# Tokens: se, te, to are one sign each; ñ = ne sign; ḫ and h̲ distinct; ':' and line numbers dropped.
SYL = ('se', 'te', 'to')
def toks(s, keep_paren=True):
    s = s.lower().replace('h̲', 'H').replace('ẖ', 'H').replace('ḫ', 'X')
    s = re.sub(r'\[=[^\]]*\]', ' ', s)          # FHN's normalised forms are not on the stone
    s = re.sub(r'\(\d+\)', '', s)                # line numbers
    s = re.sub(r'\(([a-z]+)\)', (r'\1' if keep_paren else ''), s)   # editor's supplements
    s = re.sub(r'[*:,.|?\[\]]', ' ', s)
    out = []
    for w in s.split():
        i = 0
        while i < len(w):
            if w[i:i+2] in SYL: out.append(w[i:i+2]); i += 2
            elif w[i] == '|': i += 1
            else: out.append(w[i]); i += 1
    return out
def align(a, b):
    n, m = len(a), len(b)
    D = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n+1): D[i][0] = i
    for j in range(m+1): D[0][j] = j
    for i in range(1, n+1):
        for j in range(1, m+1):
            D[i][j] = min(D[i-1][j]+1, D[i][j-1]+1, D[i-1][j-1] + (a[i-1] != b[j-1]))
    i, j, ops = n, m, []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and D[i][j] == D[i-1][j-1] + (a[i-1] != b[j-1]):
            if a[i-1] != b[j-1]: ops.append(('sub', a[i-1], b[j-1], j-1))
            i, j = i-1, j-1
        elif i > 0 and D[i][j] == D[i-1][j] + 1: ops.append(('ins', a[i-1], '-', j)); i -= 1
        else: ops.append(('del', '-', b[j-1], j-1)); j -= 1
    return D[n][m], ops[::-1]
# Mine: frozen 09:41:28. 'ñ' written for the ne sign; 'n e' where I read the n and e signs.
mine = {
 '0097': 'qo pelmos atolise bekemeteli sete mnitwwiqo wete siyeteli yetetke womñtm pilqetelo ant qo rito steli qo re semlo ḫbḫñ sqtelh̲lo mlostoh̲elo',
 '0098': 'qo kroro bekemete mte pelmos a tolit yerikelo mni se mtelo pesetolo pelmos adblito nobow nkelbo',
 '0102': 'ḫbḫñ wosqer qo mstrqyeqo wosi yntke pikl pḫilm pli ptroti pikn pbḫ',
 '0103': 'qo mstrq qo wosi bedewi psdk pro h̲eñ dḫe wiyleb',
 '0104': 'qo apmloqo pelmos adlito',
 '0105': 'qo pelmos atolise mnitwwiqo',
 '0106': 'qo kroro bekemetelo pesetolo',
 '0107': 'qo kroro bekemetelo pelmos adblito',
 '0108': 'snneblilo mseqeto',
 '0109': 'qo mstrqoye wosqerlo',
 '0111': 'qo qoreñ wosse perite wosse wos qer mstrq ye yewi wosi yntke lw pibr ph̲e qleb ksbñ wosse bto skel nḫeñ',
}
# FHN III pp. 1025-1027 as printed (OCR checked against the page images). '35' in 0098 is not a sign: dropped.
fhn = {
 '0097': '(1)qo pelmos (2)atolise (3)Bekemete(4)li sete (5)Mnitw(6)wiqo (7)wete *Si(8)yeteli (9)yetet(10)ke womnet(11)h̲,, [=womneselh̲] Pilqe(12)telo,, an(13)t qorito [=qoriselo] (14)steli qo(15)re,, *semlo (16)ḫbḫñ,, s(17)qotelh̲(18)lo mlo sto*se(19)lo',
 '0098': '(1)qo kroro (2)Bekeme(3)te ste pe(4)lmos a(5)tolit [=atolisel] (6)ye(7)rik(8)elo (9)*Mni(10)se m(11)telo (12)pese(13)tolo pe(14)lmos a(15)dblito [=adbliselo] (16)nobow,, (17) kelbo',
 '0102': '(1)ḫbḫñ Wos qer,, (2)qo Mstrqye qo,, (3)Wosi,, yntk*e,, pipl,, (4)pḫilh̲,, p*li,, Ptro(5)ti pipn,, p(6)bḫ,,',
 '0103': '(1)qo Mstrq,, qo,, Wo(2)si,, Bedewi *ksdk,, p(3)roḫeñ,, dḫe,, wiyleb,,',
 '0103full': '(1)qo Mstrq,, qo,, Wo(2)si,, Bedewi *ksdk,, p(3)roḫeñ,, dḫe,, wiyleb,, (4)ptteb,, [=ptseleb] Ptroti (5)ptrqo *b*o (6)*m*l*e kw,,',
 '0104': '(1)qo Apmlo qo (2)pelmos ad(b)li(3)to [=ad(b)liselo],,',
 '0105': '(1)qo pel(2)mos ato(3)lise Mnit(4)wwi(5)qo',
 '0106': '(1)qo kro(2)ro Be(3)keme(4)telo (5)pe(6)se(7)to(8)lo',
 '0107': '(1)qo kro(2)ro Be(3)keme(4)telo pe(5)lmos a(6)dbli(7)to [=adbliselo]',
 '0108': '(1)Snñ*bli(2)lo mseqe(3)to [=mseqeselo]',
 '0109': '(1)qo,, Ms(2)trqo(3)ye (4)Wos (5)qe(6)r(7)lo',
 '0111': '(1)qo qoreñ (2)Wosse pe(3)rite Wo(4)sse Wos (5)qer Mst(6)(rqo)ye (7)*qewi (8)W*osi yn(9)tkelw (10)pibr (11)pḫeq*le(12)b ksbñ Wo(13)sse bto (14)skelnḫ(15)eñ',
}
def words(s):
    s = re.sub(r'\[=[^\]]*\]', ' ', s.lower()); s = re.sub(r'\(\d+\)', '', s)
    s = re.sub(r'\(([a-z]+)\)', r'\1', s); s = re.sub(r'[*,.|]', '', s)
    return s.split()
tot = {'ref': 0, 'err': 0, 'ref_np': 0, 'err_np': 0}
rows = []
for k in mine:
    ref = 'fhn' if k != '0103' else 'fhn'
    a = toks(mine[k].replace('h̲', 'h̲'))
    b = toks(fhn[k]); bn = toks(fhn[k], keep_paren=False)
    d, ops = align(a, b); dn, opsn = align(a, bn)
    tot['ref'] += len(b); tot['err'] += d; tot['ref_np'] += len(bn); tot['err_np'] += dn
    mw = set(''.join(toks(w)) for w in mine[k].split()); fw = words(fhn[k])
    wright = sum(1 for w in fw if ''.join(toks(w)) in mw)
    rows.append((k, len(b), len(b) - d, d, len(bn), len(bn) - dn, wright, len(fw), ops))
    print(f"{k}: FHN signs {len(b)}, right {len(b)-d} ({100*(len(b)-d)/len(b):.1f}%), errors {d}; "
          f"without FHN's ( ) supplements {len(bn)-dn}/{len(bn)}; FHN words matched {wright}/{len(fw)}")
    for o in ops: print('    ', o)
print('TOTAL with ( ):', tot['ref'] - tot['err'], '/', tot['ref'], f"{100*(tot['ref']-tot['err'])/tot['ref']:.1f}%")
print('TOTAL without ( ):', tot['ref_np'] - tot['err_np'], '/', tot['ref_np'], f"{100*(tot['ref_np']-tot['err_np'])/tot['ref_np']:.1f}%")
json.dump([r[:8] for r in rows], open('/private/tmp/claude-501/griffith_scripts/score.json', 'w'))
