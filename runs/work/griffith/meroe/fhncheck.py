import json, re
# Edit-distance check of my readings of Griffith's type against FHN's (REM) text, signs only.
def toks(s):
    s = s.lower().replace('h̲', 'X').replace('ẖ', 'X').replace('ḫ', 'x').replace('ñ', 'N')
    s = re.sub(r'\[=[^\]]*\]', ' ', s); s = re.sub(r'\(\d+\)', '', s); s = re.sub(r'\[\.+\]|\[\.\]', ' ', s)
    s = re.sub(r'[^a-zNXx ]', ' ', s.replace('ne', 'N') if False else s)
    out = []
    for w in s.split():
        i = 0
        while i < len(w):
            if w[i:i+2] in ('se', 'te', 'to'): out.append(w[i:i+2]); i += 2
            else: out.append(w[i]); i += 1
    return out
def align(a, b):
    n, m = len(a), len(b); D = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n+1): D[i][0] = i
    for j in range(m+1): D[0][j] = j
    for i in range(1, n+1):
        for j in range(1, m+1):
            ca = a[i-1]; cb = b[j-1]
            same = ca == cb or (cb == 'h' and ca in ('x', 'X'))   # FHN OCR lost h diacritics
            D[i][j] = min(D[i-1][j]+1, D[i][j-1]+1, D[i-1][j-1] + (0 if same else 1))
    return D[n][m]
rows = {json.loads(l)['griffith_no']: json.loads(l) for l in open('/Users/mike/repos/mike/meroitic/data/expansion/griffith_meroe.jsonl')}
fhn = {
 7: "Pedemk Soborete kempl Yesebohe qore bowidlo bi kye Wos Pileqete ste Pileqe pe Yesebohetowi Ar ywidl Pileqe pe ytkidetowi Wos Atiyete Atiye pe Yesebohetowi Ar Atiyete Atiye pe ytkidetowi Wos Tebwete Tebwe pe Yesebohetowi Ar Tebwete Tebwe pe ytkidetowi Amnpte Npte k mk tNyN witw ytkidetowi s webhetel ywi yiretwi Aro hire webhlit yhi nthetwi rekl ahN witw yeritowi teris ahNwitw nthetowi ayi s ayi",
 12: "ekete Ws wide l etktetewi mseqnei d yi ekete Wos wke tk to Teriteqse qoro Amnirense kdke Akinidd ss te lo",
 5: "ato wt li etohto mk dqrite Apedemk TNyidmni pwrite elhte dqrito mewito Mno qore l w ewkenki Apedemki W l e k kte Apedemki",
}
for k, f in fhn.items():
    mine = rows[k]['text_std'].replace('ñ', 'N')
    a = toks(mine.replace('ne', 'ne')); b = toks(f.replace('nei', 'Ni'))
    d = align(a, b); print(k, 'my signs', len(a), 'FHN signs', len(b), 'edits', d, f'agreement {100*(len(b)-d)/len(b):.1f}%')
