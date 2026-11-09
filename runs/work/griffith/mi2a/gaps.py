import sys
from PIL import Image
# gaps.py leaf x0 y0 x1 y1 [min]: column ink profile of one type line; prints ink runs and the gaps between them (full-res px)
leaf = sys.argv[1]; x0, y0, x1, y1 = map(int, sys.argv[2:6]); mn = int(sys.argv[6]) if len(sys.argv) > 6 else 8
im = Image.open(f'/private/tmp/claude-501/griffith/mi2_n{leaf}.jpg').convert('L').crop((x0, y0, x1, y1)); w, h = im.size; px = im.load()
ink = [sum(1 for y in range(h) if px[x, y] < 120) > 0 for x in range(w)]
runs = []; x = 0
while x < w:
    if ink[x]:
        s = x
        while x < w and ink[x]: x += 1
        runs.append((s + x0, x - 1 + x0))
    else: x += 1
out = []
for i, (a, b) in enumerate(runs):
    if i: g = a - runs[i - 1][1] - 1; out.append(f'|{g}|' if g >= mn else '')
    out.append(f'[{a}-{b}]')
print(' '.join(o for o in out if o))
