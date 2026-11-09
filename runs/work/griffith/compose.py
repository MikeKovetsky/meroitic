import sys
from PIL import Image
# compose.py out.png strip.png crop1.png [crop2.png ...]: strip on top, crops stacked below, all at strip width
out, strip = sys.argv[1], Image.open(sys.argv[2]).convert('L')
W = 1600
s = strip.resize((W, int(strip.height * W / strip.width)))
parts = [s]
for p in sys.argv[3:]:
    c = Image.open(p).convert('L')
    if c.width > W:
        c = c.resize((W, int(c.height * W / c.width)))
    parts.append(c)
H = sum(p.height for p in parts) + 10 * len(parts)
im = Image.new('L', (W, H), 255)
y = 0
for p in parts:
    im.paste(p, (W - p.width, y)); y += p.height + 10
im.save(out); print(out, im.size)
