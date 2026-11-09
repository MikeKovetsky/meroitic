import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
# cells.py out.png scale label|page|cx|cy|w|h ... -> row(s) of cells centred on (cx,cy)
out, sc = sys.argv[1], float(sys.argv[2])
try: font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 26)
except Exception: font = ImageFont.load_default()
cells = []
for spec in sys.argv[3:]:
    lab, page, cx, cy, w, h = spec.split('|'); cx, cy, w, h = map(int, (cx, cy, w, h))
    im = Image.open(f'/private/tmp/claude-501/griffith/{page}').convert('L').crop((cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2))
    im = ImageOps.autocontrast(im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS), cutoff=1)
    c = Image.new('L', (im.width + 10, im.height + 36), 255); c.paste(im, (5, 36))
    ImageDraw.Draw(c).text((5, 2), lab, fill=0, font=font); cells.append(c)
per = max(1, 1600 // (cells[0].width))
rows = [cells[i:i + per] for i in range(0, len(cells), per)]
W = max(sum(c.width for c in r) for r in rows); H = sum(max(c.height for c in r) for r in rows)
sheet = Image.new('L', (W, H), 255); y = 0
for r in rows:
    x = 0
    for c in r: sheet.paste(c, (x, y)); x += c.width
    y += max(c.height for c in r)
d = ImageDraw.Draw(sheet)
sheet.save(out); print(out, sheet.size)
