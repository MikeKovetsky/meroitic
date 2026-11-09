import sys
from PIL import Image, ImageDraw, ImageFont
# sheet2.py out.jpg width n1 n2 ... : leaves side by side, labelled
out, w = sys.argv[1], int(sys.argv[2])
ns = sys.argv[3:]
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 28)
ims = []
for n in ns:
    im = Image.open(f'/private/tmp/claude-501/griffith/mi2_n{n}.jpg').convert('L')
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    ImageDraw.Draw(im).text((10, 10), f'n{n}', fill=0, font=font)
    ims.append(im)
H = max(i.height for i in ims)
s = Image.new('L', (sum(i.width for i in ims) + 12 * (len(ims) - 1), H), 255)
x = 0
for i in ims:
    s.paste(i, (x, 0)); x += i.width + 12
s.save(out, quality=88); print(out, s.size)
