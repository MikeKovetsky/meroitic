import sys
from PIL import Image
K='/private/tmp/claude-501/expansion/karanog/'
leaf, pre, sc = sys.argv[1], sys.argv[2], float(sys.argv[3])
im = Image.open(K+'leaf_%s.jpg'%leaf).convert('L')
crops=[]
for r in sys.argv[4:]:
    y0, y1 = map(int, r.split(':')); c = im.crop((300, y0, im.width-120, y1)); crops.append(c.resize((int(c.width*sc), int(c.height*sc)), Image.LANCZOS))
# stack rows two per image
for i in range(0, len(crops), 2):
    pair = crops[i:i+2]; W = max(c.width for c in pair); H = sum(c.height for c in pair) + 6
    o = Image.new('L', (W, H), 255); y = 0
    for c in pair: o.paste(c, (0, y)); y += c.height + 6
    o.save('%s_%d.png' % (pre, i//2 + 1)); print('%s_%d.png' % (pre, i//2 + 1), o.size)
