import sys
from PIL import Image
# usage: zoom.py leaf x0 y0 x1 y1 out [scale]
K='/private/tmp/claude-501/expansion/karanog/'
leaf=sys.argv[1]; x0,y0,x1,y1=map(int,sys.argv[2:6]); out=sys.argv[6]; sc=float(sys.argv[7]) if len(sys.argv)>7 else 1.0
im=Image.open(K+'leaf_%s.jpg'%leaf).convert('L').crop((x0,y0,x1,y1))
if sc!=1.0: im=im.resize((int(im.width*sc),int(im.height*sc)),Image.LANCZOS)
im.save(out); print(out, im.size)
