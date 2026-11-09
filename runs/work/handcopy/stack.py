import sys
from PIL import Image, ImageDraw
# usage: stack.py leaf out scale label:x0:y0:x1:y1 ...
K='/private/tmp/claude-501/expansion/karanog/'
leaf, out, sc = sys.argv[1], sys.argv[2], float(sys.argv[3])
im = Image.open(K+'leaf_%s.jpg'%leaf).convert('L')
crops=[]
for a in sys.argv[4:]:
    lab, x0, y0, x1, y1 = a.split(':'); c = im.crop((int(x0), int(y0), int(x1), int(y1)))
    c = c.resize((int(c.width*sc), int(c.height*sc)), Image.LANCZOS); crops.append((lab, c))
W = max(c.width for _, c in crops) + 60; H = sum(c.height + 8 for _, c in crops)
o = Image.new('L', (W, H), 255); d = ImageDraw.Draw(o); y = 0
for lab, c in crops:
    o.paste(c, (60, y)); d.text((5, y + 10), lab, fill=0); y += c.height + 8
    d.line((0, y - 4, W, y - 4), fill=160)
o.save(out); print(out, o.size)
