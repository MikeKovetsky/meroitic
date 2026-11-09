import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont
# b2_crop.py out.png scale strip(0/1) x0,y0,x1,y1 [x0,y0,x1,y1 ...]  -> stacked crops of n69 (or page given by P=name)
out, scale, strip = sys.argv[1], float(sys.argv[2]), sys.argv[3] == '1'
page = '/private/tmp/claude-501/griffith/mi2_n69.jpg'
parts = []
if strip:
    s = Image.open('/private/tmp/claude-501/griffith_scripts/signstrip.png').convert('L')
    parts.append(s)
for spec in sys.argv[4:]:
    if spec.startswith('P='):
        page = '/private/tmp/claude-501/griffith/' + spec[2:]; continue
    x0, y0, x1, y1 = map(int, spec.split(','))
    im = Image.open(page).convert('L').crop((x0, y0, x1, y1))
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    parts.append(ImageOps.autocontrast(im, cutoff=1))
W = max(p.width for p in parts); H = sum(p.height + 12 for p in parts)
sheet = Image.new('L', (W, H), 255); y = 0
for p in parts:
    sheet.paste(p, (W - p.width, y)); y += p.height + 12
sheet.save(out); print(out, sheet.size)
