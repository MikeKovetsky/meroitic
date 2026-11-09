import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont
# b1_seg.py out.png page.jpg x0 y0 x1 y1 segw scale [strip]
# crops the region, cuts it into segments of segw px from the RIGHT (RTL order), stacks them top to bottom at scale
out, page = sys.argv[1], sys.argv[2]
x0, y0, x1, y1, segw = map(int, sys.argv[3:8]); scale = float(sys.argv[8])
strip = len(sys.argv) > 9 and sys.argv[9] == 'strip'
im = Image.open(page).convert('L').crop((x0, y0, x1, y1))
try: font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 22)
except Exception: font = ImageFont.load_default()
segs = []
x = im.width
while x > 0:
    a = max(0, x - segw)
    s = im.crop((a, 0, x, im.height))
    s = ImageOps.autocontrast(s.resize((int(s.width * scale), int(s.height * scale)), Image.LANCZOS), cutoff=1)
    cell = Image.new('L', (int(segw * scale), s.height + 24), 255)
    cell.paste(s, (cell.width - s.width, 24))
    ImageDraw.Draw(cell).text((5, 0), f'x {x0+a}-{x0+x}', fill=0, font=font)
    segs.append(cell); x = a + 40 if a > 0 else 0  # 40 px overlap
    if a == 0: break
parts = []
if strip:
    st = Image.open('/private/tmp/claude-501/griffith_scripts/signstrip.png').convert('L')
    W = segs[0].width
    parts.append(st.resize((W, int(st.height * W / st.width))))
parts += segs
W = max(p.width for p in parts); H = sum(p.height + 6 for p in parts)
sheet = Image.new('L', (W, H), 255); y = 0
for p in parts: sheet.paste(p, (W - p.width, y)); y += p.height + 6
sheet.save(out); print(out, sheet.size)
