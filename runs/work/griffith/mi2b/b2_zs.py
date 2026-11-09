import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
# b2_zs.py out.png scale label|page|x0|y0|x1|y1 ...
out, sc = sys.argv[1], float(sys.argv[2])
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 28)
parts = []
for spec in sys.argv[3:]:
    lab, page, x0, y0, x1, y1 = spec.split('|'); x0, y0, x1, y1 = map(int, (x0, y0, x1, y1))
    im = Image.open(f'/private/tmp/claude-501/griffith/{page}').convert('L').crop((x0, y0, x1, y1))
    im = ImageOps.autocontrast(im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS), cutoff=1)
    cell = Image.new('L', (im.width + 220, im.height), 255); cell.paste(im, (220, 0))
    ImageDraw.Draw(cell).text((5, 5), lab, fill=0, font=font); parts.append(cell)
W = max(p.width for p in parts); H = sum(p.height + 8 for p in parts)
sheet = Image.new('L', (W, H), 255); y = 0
for p in parts: sheet.paste(p, (0, y)); y += p.height + 8
sheet.save(out); print(out, sheet.size)
