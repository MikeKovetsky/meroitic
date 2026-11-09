import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont
# sheet.py out.png scale page.jpg label:y0:y1:x0:x1 ...
out, scale, page = sys.argv[1], float(sys.argv[2]), sys.argv[3]
im = Image.open(page).convert('L'); font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 24)
cells = []
for spec in sys.argv[4:]:
    lab, y0, y1, x0, x1 = spec.split(':'); y0, y1, x0, x1 = map(int, (y0, y1, x0, x1))
    c = im.crop((x0, y0, x1, y1)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c = ImageOps.autocontrast(c, cutoff=1)
    cell = Image.new('L', (c.width + 90, c.height), 255); cell.paste(c, (90, 0)); ImageDraw.Draw(cell).text((2, c.height // 2 - 12), lab, fill=0, font=font); cells.append(cell)
W = max(c.width for c in cells); H = sum(c.height + 4 for c in cells); s = Image.new('L', (W, H), 255); y = 0
for c in cells: s.paste(c, (0, y)); y += c.height + 4
s.save(out); print(out, s.size)
