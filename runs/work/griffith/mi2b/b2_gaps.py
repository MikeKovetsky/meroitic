import sys
from PIL import Image
# b2_gaps.py x0 y0 x1 y1: ink runs (x ranges, orig px) and their vertical extent, page n69
x0, y0, x1, y1 = map(int, sys.argv[1:5])
im = Image.open('/private/tmp/claude-501/griffith/mi2_n69.jpg').convert('L').crop((x0, y0, x1, y1))
w, h = im.size; px = im.load()
cols = []
for x in range(w):
    ys = [y for y in range(h) if px[x, y] < 120]
    cols.append((min(ys), max(ys)) if ys else None)
runs, cur = [], None
for x, c in enumerate(cols):
    if c and cur is None: cur = [x, x, c[0], c[1]]
    elif c: cur[1] = x; cur[2] = min(cur[2], c[0]); cur[3] = max(cur[3], c[1])
    elif cur is not None: runs.append(cur); cur = None
if cur: runs.append(cur)
prev = None
for r in runs:
    gap = r[0] - prev if prev is not None else 0
    print(f"x {r[0]+x0}-{r[1]+x0} y {r[2]+y0}-{r[3]+y0} gap_before {gap}")
    prev = r[1]
