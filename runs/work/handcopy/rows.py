import sys
from PIL import Image
# usage: rows.py leaf prefix xsplit scale y0:y1 y0:y1 ...  -> prefix_rNr.png (right part) and prefix_rNl.png (left part)
K='/private/tmp/claude-501/expansion/karanog/'
leaf, pre, xs, sc = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
im = Image.open(K+'leaf_%s.jpg'%leaf).convert('L')
for i, r in enumerate(sys.argv[5:]):
    p = r.split(":"); y0, y1 = int(p[0]), int(p[1]); name = p[2] if len(p) > 2 else str(i)
    for side, (a, b) in (('r', (xs-150, im.width-120)), ('l', (200, xs+150))):
        c = im.crop((a, y0, b, y1)); c = c.resize((int(c.width*sc), int(c.height*sc)), Image.LANCZOS)
        c.save('%s_r%s%s.png' % (pre, name, side))
    print(name, y0, y1)
