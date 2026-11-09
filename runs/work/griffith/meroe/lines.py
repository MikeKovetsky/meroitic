import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont
# lines.py out.png page.jpg scale y0:y1[:x0:x1] ... -> stacked crops (orig px coords), each scaled, with labels
out, page, scale = sys.argv[1], sys.argv[2], float(sys.argv[3])
im = Image.open(page).convert('L')
try: font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 26)
except Exception: font = ImageFont.load_default()
parts = []
for spec in sys.argv[4:]:
    v = list(map(int, spec.split(':')))
    y0, y1 = v[0], v[1]; x0, x1 = (v[2], v[3]) if len(v) > 2 else (0, im.width)
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c = ImageOps.autocontrast(c, cutoff=1)
    cell = Image.new('L', (c.width, c.height + 30), 255); cell.paste(c, (0, 30))
    ImageDraw.Draw(cell).text((5, 0), spec, fill=0, font=font); parts.append(cell)
W = max(p.width for p in parts); H = sum(p.height + 6 for p in parts)
sheet = Image.new('L', (W, H), 255); y = 0
for p in parts: sheet.paste(p, (W - p.width, y)); y += p.height + 6
sheet.save(out); print(out, sheet.size)
