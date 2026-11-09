import sys
from PIL import Image
# bands.py page.jpg x0 x1 y0 y1: print ink bands; type lines are >= 46 px tall, English lines <= 42 px
src = sys.argv[1]; x0, x1, y0, y1 = map(int, sys.argv[2:6])
c = Image.open(src).convert('L').crop((x0, y0, x1, y1)); w, h = c.size; px = c.load()
band = None; out = []
for y in range(0, h, 4):
    d = sum(1 for x in range(0, w, 3) if px[x, y] < 110)
    if d > 3 and band is None: band = [y + y0, y + y0, d]
    elif d > 3: band[1] = y + y0; band[2] = max(band[2], d)
    elif band is not None:
        if band[1] - band[0] > 12: out.append(band)
        band = None
print(' '.join(f"{a}-{b}{'*' if b - a >= 46 else ''}" for a, b, d in out))
