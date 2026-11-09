import sys
from PIL import Image
import numpy as np
# usage: bands.py leaf y0 y1 prefix [x0 x1]  -> crops each text line (ink band) at full resolution
K='/private/tmp/claude-501/expansion/karanog/'
leaf, y0, y1, pre = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
im = Image.open(K+'leaf_%s.jpg'%leaf).convert('L')
x0, x1 = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (150, im.width-100)
a = np.array(im.crop((x0, y0, x1, y1))) < 140
prof = a.sum(1)
on = prof > 6
bands=[]; s=None
for i,v in enumerate(on):
    if v and s is None: s=i
    if not v and s is not None:
        if i-s>8: bands.append([s,i])
        s=None
if s is not None: bands.append([s,len(on)])
# merge bands closer than 28 px (superscripts, dots)
m=[]
for b in bands:
    if m and b[0]-m[-1][1] < 28: m[-1][1]=b[1]
    else: m.append(b)
m=[b for b in m if b[1]-b[0] > 40]
for k,(s,e) in enumerate(m):
    c = im.crop((x0, y0+s-25, x1, y0+e+25))
    c.save('%s_%02d.png'%(pre,k+1))
    print(k+1, y0+s, y0+e, c.size)
