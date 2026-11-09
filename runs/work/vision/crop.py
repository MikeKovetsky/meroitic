"""crop.py <src> <dst> <x0> <y0> <x1> <y1> [scale] [enhance]  (fractions 0-1 or pixels)"""
import sys
from PIL import Image, ImageOps, ImageEnhance
src, dst = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = map(float, sys.argv[3:7])
scale = float(sys.argv[7]) if len(sys.argv) > 7 else 1.0
enh = sys.argv[8] if len(sys.argv) > 8 else ""
im = Image.open(src).convert("RGB")
W, H = im.size
f = lambda v, n: int(v * n) if v <= 1.0 else int(v)
box = (f(x0, W), f(y0, H), f(x1, W), f(y1, H))
c = im.crop(box)
if scale != 1.0:
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
if "gray" in enh:
    c = ImageOps.grayscale(c)
if "auto" in enh:
    c = ImageOps.autocontrast(c, cutoff=1)
if "eq" in enh:
    c = ImageOps.equalize(c)
if "sharp" in enh:
    c = ImageEnhance.Sharpness(c).enhance(2.0)
c.save(dst)
print(dst, box, c.size)
