import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont
# lines.py out.png leaf x0 x1 scale y0:y1 [y0:y1 ...] : stack horizontal bands, labelled
out, leaf, x0, x1, sc = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
src = Image.open(f'/private/tmp/claude-501/griffith/mi2_n{leaf}.jpg').convert('L')
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 22)
parts = []
for k, b in enumerate(sys.argv[6:]):
    y0, y1 = map(int, b.split(':'))
    im = src.crop((x0, y0, x1, y1))
    im = ImageOps.autocontrast(im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS), cutoff=1)
    parts.append(im)
W = max(p.width for p in parts); H = sum(p.height + 6 for p in parts)
s = Image.new('L', (W, H), 255); y = 0
for p in parts:
    s.paste(p, (0, y)); ImageDraw.Draw(s).line([(0, y + p.height + 2), (W, y + p.height + 2)], fill=160); y += p.height + 6
s.save(out); print(out, s.size)
