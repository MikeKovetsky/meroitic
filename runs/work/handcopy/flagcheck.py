import re
exec(open('score_hc.py').read().split('res = {}')[0])
def ftoks(s):
    t = toks(s.replace('?', '§')); out = []
    for x in t:
        if x == '§':
            if out: out[-1] = (out[-1][0], True)
        else: out.append((x, False))
    return out
tot = dict(err_sub_ins=0, flagged=0, dels=0, my_flags=0, my_signs=0, right_flagged=0)
for k in ['0247', '0277_order', '0278', '0321']:
    a = ftoks(MINE[k]); b = toks(FHN[k]); A = [x for x, f in a]
    assert A == toks(MINE[k]), k
    n, m = len(A), len(b)
    D = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n+1): D[i][0] = i
    for j in range(m+1): D[0][j] = j
    for i in range(1, n+1):
        for j in range(1, m+1):
            D[i][j] = min(D[i-1][j]+1, D[i][j-1]+1, D[i-1][j-1] + (A[i-1] != b[j-1]))
    i, j = n, m; e = fl = de = 0; wrong = set()
    while i > 0 or j > 0:
        if i > 0 and j > 0 and D[i][j] == D[i-1][j-1] + (A[i-1] != b[j-1]):
            if A[i-1] != b[j-1]: e += 1; fl += a[i-1][1]; wrong.add(i-1)
            i, j = i-1, j-1
        elif i > 0 and D[i][j] == D[i-1][j] + 1: e += 1; fl += a[i-1][1]; wrong.add(i-1); i -= 1
        else: de += 1; j -= 1
    mf = sum(f for x, f in a); rf = sum(1 for idx, (x, f) in enumerate(a) if f and idx not in wrong)
    print(k, 'wrong my-signs', e, 'of them flagged', fl, '| FHN signs I omitted', de, '| my flags', mf, 'flags on right signs', rf)
    tot['err_sub_ins'] += e; tot['flagged'] += fl; tot['dels'] += de; tot['my_flags'] += mf; tot['my_signs'] += n; tot['right_flagged'] += rf
print(tot)
