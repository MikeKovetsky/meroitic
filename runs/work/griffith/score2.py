import re, json, importlib.util
spec = importlib.util.spec_from_file_location('s', '/private/tmp/claude-501/griffith_scripts/score.py')
src = open('/private/tmp/claude-501/griffith_scripts/score.py').read().split('tot = {')[0]
ns = {}; exec(src, ns)
toks, align, mine, fhn = ns['toks'], ns['align'], ns['mine'], ns['fhn']
mine['0120'] = 'yeseboh̲e tniqo qoro mret meyte tlo wos selo'
fhn['0120'] = '(1)Yesebohemniqo,, (2)qoro,, mretmetey(3)te,,tlo,, Wosselo,,'
H_LENIENT = {('0111', 'H', 'X'), ('0120', 'H', 'h')}   # FHN diacritic not legible at scan size
def fhn_words(s, keep_paren=True):
    s = re.sub(r'\[=[^\]]*\]', ' ', s); s = re.sub(r'\(\d+\)', '', s)
    s = re.sub(r'\(([a-z]+)\)', (r'\1' if keep_paren else ''), s.lower()); s = re.sub(r'[*]', '', s); s = re.sub(r'[,.|:]', ' ', s)
    return [w for w in s.split() if toks(w)]
res = {}
for k in mine:
    for kp in (True, False):
        a = toks(mine[k]); b = toks(fhn[k], keep_paren=kp)
        if k == '0120': b = ['h' if t == 'h' else t for t in b]
        d, ops = align(a, b)
        ws = fhn_words(fhn[k], kp); spans = []; p = 0
        for w in ws:
            n = len(toks(w)); spans.append((p, p + n, w)); p += n
        bad = set()
        for op, x, y, j in ops:
            for wi, (s0, s1, w) in enumerate(spans):
                if (op != 'ins' and s0 <= j < s1) or (op == 'ins' and s0 <= j < s1): bad.add(wi)
        res[(k, kp)] = dict(n=len(b), err=d, ops=ops, words=len(ws), wbad=len(bad))
order = ['0097','0098','0102','0103','0104','0105','0106','0107','0108','0109','0111','0120']
print('text  FHN-signs right  %    FHN-words fully-right   ops (my sign, FHN sign, FHN index)')
T = [0, 0, 0, 0]
for k in order:
    r = res[(k, True)]
    right = r['n'] - r['err']; T[0] += r['n']; T[1] += right; T[2] += r['words']; T[3] += r['words'] - r['wbad']
    print(f"{k}  {r['n']:4d} {right:4d} {100*right/r['n']:5.1f}   {r['words']:3d} {r['words']-r['wbad']:3d}   {[(o[1],o[2],o[3]) for o in r['ops']]}")
print('TOTAL', T, f'{100*T[1]/T[0]:.1f}%  words {100*T[3]/T[2]:.1f}%')
print('my signs per text:', {k: len(toks(mine[k])) for k in order}, 'total', sum(len(toks(mine[k])) for k in order))
for k in order:
    print(k, 'FHN words:', fhn_words(fhn[k]))
