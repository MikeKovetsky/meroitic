import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont
# rl.py out.png page.jpg scale nseg x0 x1 y0:y1 [y0:y1 ...]
# each line cut into nseg segments, RIGHTMOST first (top), overlapping 40px; lines stacked in order given
out, page, scale, nseg = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
x0, x1 = int(sys.argv[5]), int(sys.argv[6])
im = Image.open(page).convert('L')
try: font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 24)
except Exception: font = ImageFont.load_default()
parts = []
w = (x1 - x0) / nseg
for li, spec in enumerate(sys.argv[7:]):
    y0, y1 = map(int, spec.split(':'))
    for s in range(nseg):
        b = x1 - s * w; a = b - w
        c = im.crop((int(max(x0, a - 40)), y0, int(min(x1, b + 40)), y1))
        c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
        c = ImageOps.autocontrast(c, cutoff=1)
        cell = Image.new('L', (c.width, c.height + 26), 255); cell.paste(c, (0, 26))
        ImageDraw.Draw(cell).text((5, 0), f'L{li+1} seg{s+1} (R->L)', fill=0, font=font); parts.append(cell)
W = max(p.width for p in parts); H = sum(p.height + 6 for p in parts)
sheet = Image.new('L', (W, H), 255); y = 0
for p in parts: sheet.paste(p, (W - p.width, y)); y += p.height + 6
sheet.save(out); print(out, sheet.size)
