import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
# Reference strip: Griffith's cursive type forms from MI II p. xv (leaf n18), labelled with modern values.
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('L')
left = [('a', 1221), ('e', 1341), ('o (ê)', 1454), ('i', 1572), ('y', 1687), ('w', 1806),
        ('b', 1921), ('p', 2040), ('m', 2156), ('n', 2275), ('ne (ñ)', 2391), ('r', 2510)]
right = [('l', 1221), ('ḫ', 1341), ('h̲ (ẖ)', 1462), ('se (s)', 1575), ('s (š)', 1694), ('k', 1806),
         ('q', 1927), ('t', 2040), ('te', 2160), ('to (tê)', 2275), ('d (z)', 2391), (':', 2510)]
cw, ch = 200, 130
try:
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 34)
except Exception:
    font = ImageFont.load_default()
cells = []
for (lab, y), x0 in [(c, 690) for c in left] + [(c, 1900) for c in right]:
    c = ImageOps.autocontrast(im.crop((x0, y - 65, x0 + cw, y + 65)), cutoff=1)
    cell = Image.new('L', (cw, ch + 50), 255)
    cell.paste(c, (0, 0))
    ImageDraw.Draw(cell).text((10, ch + 5), lab, fill=0, font=font)
    cells.append(cell)
cols = 12
sheet = Image.new('L', (cols * cw, 2 * (ch + 50)), 255)
for i, c in enumerate(cells):
    sheet.paste(c, ((i % cols) * cw, (i // cols) * (ch + 50)))
d = ImageDraw.Draw(sheet)
for i in range(1, cols):
    d.line([(i * cw, 0), (i * cw, sheet.height)], fill=180)
sheet.save(out)
print(out, sheet.size)
