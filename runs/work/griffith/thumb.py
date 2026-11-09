import sys
from PIL import Image
# usage: thumb.py out.jpg width in1.jpg in2.jpg ... -> side-by-side contact sheet
out, w = sys.argv[1], int(sys.argv[2])
ims = []
for p in sys.argv[3:]:
    im = Image.open(p).convert('L')
    h = int(im.height * w / im.width)
    ims.append(im.resize((w, h)))
H = max(i.height for i in ims)
sheet = Image.new('L', (w * len(ims) + 10 * (len(ims) - 1), H), 255)
x = 0
for i in ims:
    sheet.paste(i, (x, 0)); x += w + 10
sheet.save(out, quality=85)
print(out, sheet.size)
