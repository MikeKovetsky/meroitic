import sys, io
from pypdf import PdfReader
from PIL import Image
r = PdfReader('/private/tmp/claude-501/expansion/survey/fhn/fhn03.pdf')
for p in map(int, sys.argv[1:]):
    pg = r.pages[p-1]
    imgs = list(pg.images)
    for k, im in enumerate(imgs):
        I = Image.open(io.BytesIO(im.data)); out = 'fhn/p%d_%d.png' % (p, k)
        I.convert('L').save(out); print(out, I.size)
