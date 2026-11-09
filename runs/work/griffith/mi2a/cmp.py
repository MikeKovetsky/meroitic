import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
# cmp.py out.png scale label|leaf|x0|y0|x1|y1 ... : cells side by side at one scale (leaf 18 = the sign table)
out, sc = sys.argv[1], float(sys.argv[2])
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 24)
cells = []
for spec in sys.argv[3:]:
    lab, leaf, x0, y0, x1, y1 = spec.split('|'); x0, y0, x1, y1 = map(int, (x0, y0, x1, y1))
    im = Image.open(f'/private/tmp/claude-501/griffith/mi2_n{leaf}.jpg').convert('L').crop((x0, y0, x1, y1))
    im = ImageOps.autocontrast(im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS), cutoff=1)
    c = Image.new('L', (max(im.width, 120), im.height + 34), 255); c.paste(im, (0, 34))
    ImageDraw.Draw(c).text((4, 2), lab, fill=0, font=font); cells.append(c)
W = sum(c.width + 10 for c in cells); H = max(c.height for c in cells)
s = Image.new('L', (W, H), 255); x = 0
for c in cells: s.paste(c, (x, 0)); x += c.width + 10
s.save(out); print(out, s.size)
