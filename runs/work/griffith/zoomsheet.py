import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
# zoomsheet.py out.png  label|page|x0|y0|x1|y1 ...  (scale 2.5, stacked with labels)
out = sys.argv[1]
try: font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 30)
except Exception: font = ImageFont.load_default()
parts = []
for spec in sys.argv[2:]:
    lab, page, x0, y0, x1, y1 = spec.split('|'); x0, y0, x1, y1 = map(int, (x0, y0, x1, y1))
    im = Image.open(f'/private/tmp/claude-501/griffith/{page}').convert('L').crop((x0, y0, x1, y1))
    im = ImageOps.autocontrast(im.resize((int(im.width * 2.5), int(im.height * 2.5)), Image.LANCZOS), cutoff=1)
    cell = Image.new('L', (max(im.width, 400), im.height + 40), 255); cell.paste(im, (0, 40))
    ImageDraw.Draw(cell).text((5, 2), lab, fill=0, font=font); parts.append(cell)
W = max(p.width for p in parts); H = sum(p.height + 8 for p in parts)
sheet = Image.new('L', (W, H), 255); y = 0
for p in parts: sheet.paste(p, (0, y)); y += p.height + 8
sheet.save(out); print(out, sheet.size)
