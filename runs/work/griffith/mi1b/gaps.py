import sys
from PIL import Image
# gaps.py page.jpg x0 y0 x1 y1 [thr]: print ink runs (x ranges) and the gaps between them, at full resolution
src = sys.argv[1]; x0, y0, x1, y1 = map(int, sys.argv[2:6]); thr = int(sys.argv[6]) if len(sys.argv) > 6 else 120
im = Image.open(src).convert('L').crop((x0, y0, x1, y1)); w, h = im.size; px = im.load()
ink = [any(px[x, y] < thr for y in range(h)) for x in range(w)]
runs = []; s = None
for x, v in enumerate(ink + [False]):
    if v and s is None: s = x
    elif not v and s is not None: runs.append((s + x0, x - 1 + x0)); s = None
out = []
for i, (a, b) in enumerate(runs):
    g = a - runs[i - 1][1] - 1 if i else 0
    out.append(f"[{a}-{b}]" + (f" gap{g}" if i else ""))
print(' '.join(out))
