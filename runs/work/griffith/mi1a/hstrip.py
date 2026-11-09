import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
# Hieroglyphic + cursive reference strip from MI I p. 49 (leaf n60), labelled with modern values.
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('L')
ys = [1324, 1443, 1557, 1671, 1793, 1914, 2029, 2146, 2261, 2379, 2493, 2614]
left = ['a', 'e', 'o', 'i', 'y', 'w', 'b', 'p', 'm', 'n', 'ne', 'r']
right = ['l', 'ḫ', 'h̲', 'se', 's', 'k', 'q', 't', 'te', 'to', 'd', ':']
cw, ch = 330, 120
try:
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 30)
except Exception:
    font = ImageFont.load_default()
cells = []
for labs, x0 in ((left, 410), (right, 1690)):
    for lab, y in zip(labs, ys):
        c = ImageOps.autocontrast(im.crop((x0, y - 60, x0 + cw, y + 60)), cutoff=1)
        cell = Image.new('L', (cw, ch + 40), 255)
        cell.paste(c, (0, 0))
        ImageDraw.Draw(cell).text((10, ch + 3), lab, fill=0, font=font)
        cells.append(cell)
cols = 12
sheet = Image.new('L', (cols * cw, 2 * (ch + 40)), 255)
for i, c in enumerate(cells):
    sheet.paste(c, ((i % cols) * cw, (i // cols) * (ch + 40)))
d = ImageDraw.Draw(sheet)
for i in range(1, cols):
    d.line([(i * cw, 0), (i * cw, sheet.height)], fill=150)
sheet = sheet.resize((sheet.width * 2 // 3, sheet.height * 2 // 3), Image.LANCZOS)
sheet.save(out)
print(out, sheet.size)
