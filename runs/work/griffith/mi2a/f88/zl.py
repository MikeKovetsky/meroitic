import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont
# zl.py out leaf x0 x1 scale up down label:yc label:yc ... -> stacked line strips, labelled
out, leaf = sys.argv[1], sys.argv[2]
x0, x1 = int(sys.argv[3]), int(sys.argv[4]); sc = float(sys.argv[5]); up, dn = int(sys.argv[6]), int(sys.argv[7])
src = Image.open(f'/private/tmp/claude-501/griffith/mi2_n{leaf}.jpg').convert('L')
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 26)
parts = []
for spec in sys.argv[8:]:
    lab, yc = spec.split(':'); yc = int(yc)
    c = src.crop((x0, yc - up, x1, yc + dn))
    c = ImageOps.autocontrast(c.resize((int(c.width * sc), int(c.height * sc)), Image.LANCZOS), cutoff=1)
    cell = Image.new('L', (c.width + 60, c.height), 255); cell.paste(c, (60, 0))
    ImageDraw.Draw(cell).text((2, 2), lab, fill=0, font=font); parts.append(cell)
W = max(p.width for p in parts); H = sum(p.height + 6 for p in parts)
s = Image.new('L', (W, H), 200); y = 0
for p in parts: s.paste(p, (0, y)); y += p.height + 6
s.save(out); print(out, s.size)
