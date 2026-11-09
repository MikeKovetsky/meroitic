import sys, glob
from PIL import Image
# split each band crop into right and left halves (with overlap) at full resolution
for f in sorted(glob.glob(sys.argv[1]+'_[0-9][0-9].png')):
    im = Image.open(f); w = im.width; mid = int(sys.argv[2]) if len(sys.argv)>2 else w//2
    im.crop((mid-120, 0, w, im.height)).save(f.replace('.png','R.png'))
    im.crop((0, 0, mid+120, im.height)).save(f.replace('.png','L.png'))
    print(f, im.size)
