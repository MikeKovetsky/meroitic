import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont
# grid.py out.png leaf scale cols label|x|y ... : cells of 130x120 (full-res) centred at x,y
out, leaf, sc, cols = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
src = Image.open(f'/private/tmp/claude-501/griffith/mi2_n{leaf}.jpg').convert('L')
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 20)
cells = []
for spec in sys.argv[5:]:
    lab, x, y = spec.split('|'); x, y = int(x), int(y)
    c = src.crop((x - 75, y - 70, x + 75, y + 60))
    c = ImageOps.autocontrast(c.resize((int(c.width * sc), int(c.height * sc)), Image.LANCZOS), cutoff=1)
    cell = Image.new('L', (c.width, c.height + 26), 255); cell.paste(c, (0, 26))
    ImageDraw.Draw(cell).text((4, 2), lab, fill=0, font=font); cells.append(cell)
w, h = cells[0].size
rows = (len(cells) + cols - 1) // cols
s = Image.new('L', (cols * (w + 6), rows * (h + 6)), 200)
for i, c in enumerate(cells):
    s.paste(c, ((i % cols) * (w + 6), (i // cols) * (h + 6)))
s.save(out); print(out, s.size)
