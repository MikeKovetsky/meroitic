import sys
from PIL import Image, ImageDraw
# usage: signcmp.py out scale label:leaf:x0:y0:x1:y1 ... -> grid of sign crops
out, sc = sys.argv[1], float(sys.argv[2]); K='/private/tmp/claude-501/expansion/karanog/'
cache={}; cells=[]
for a in sys.argv[3:]:
    lab, leaf, x0, y0, x1, y1 = a.split(':')
    if leaf not in cache: cache[leaf]=Image.open(K+'leaf_%s.jpg'%leaf).convert('L')
    c = cache[leaf].crop((int(x0),int(y0),int(x1),int(y1))); c=c.resize((int(c.width*sc),int(c.height*sc)),Image.LANCZOS)
    cells.append((lab,c))
cw = max(c.width for _,c in cells)+10; ch = max(c.height for _,c in cells)+30
n=len(cells); cols=min(n,6); rows=(n+cols-1)//cols
o=Image.new('L',(cw*cols,ch*rows),255); d=ImageDraw.Draw(o)
for i,(lab,c) in enumerate(cells):
    x=(i%cols)*cw; y=(i//cols)*ch; o.paste(c,(x,y)); d.text((x+4,y+ch-26),lab,fill=0); d.rectangle((x,y,x+cw-1,y+ch-1),outline=180)
o.save(out); print(out,o.size)
