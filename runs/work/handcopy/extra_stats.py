import re
src = open('/private/tmp/claude-501/griffith_scripts/score.py').read().split('# Mine:')[0]
ns = {}; exec(src, ns); toks = ns['toks']
t = open('readings.md', encoding='utf-8').read()
tot = [0, 0, 0]
for b in t.split('## Kar. ')[1:]:
    head, body = b.split('\n')[0], b.split('\n')[1]
    n = len(toks(body)); q = len(re.findall(r'\?', body)); brk = len(re.findall(r'\[\.+\]', body))
    print('%-10s signs %3d  uncertain %3d (%4.1f%%)  breaks %d' % (head.split(' (')[0], n, q, 100*q/n, brk))
    if head.split(' (')[0] in ('48', '76', '79', '122'): tot[0] += n; tot[1] += q
print('extra total signs %d uncertain %d (%.1f%%)' % (tot[0], tot[1], 100*tot[1]/tot[0]))
