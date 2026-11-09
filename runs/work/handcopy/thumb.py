import sys
from PIL import Image
# usage: thumb.py src dst maxw [x0 y0 x1 y1]
src, dst, maxw = sys.argv[1], sys.argv[2], int(sys.argv[3])
im = Image.open(src).convert('L')
if len(sys.argv) > 4:
    x0, y0, x1, y1 = map(int, sys.argv[4:8]); im = im.crop((x0, y0, x1, y1))
if im.width > maxw:
    im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
im.save(dst); print(dst, im.size)
