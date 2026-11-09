import sys
from PIL import Image, ImageOps
# cut.py out.png leaf x0 y0 x1 y1 [scale] [nostrip]: crop a leaf of MI II (full-res coords), scale, sign strip on top
out, leaf = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = map(int, sys.argv[3:7])
sc = float(sys.argv[7]) if len(sys.argv) > 7 else 1.0
im = Image.open(f'/private/tmp/claude-501/griffith/mi2_n{leaf}.jpg').convert('L').crop((x0, y0, x1, y1))
if sc != 1.0:
    im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
im = ImageOps.autocontrast(im, cutoff=1)
if len(sys.argv) > 8:
    im.save(out); print(out, im.size); sys.exit()
st = Image.open('/private/tmp/claude-501/griffith_scripts/signstrip.png').convert('L')
W = max(im.width, 1200)
st = st.resize((W, int(st.height * W / st.width)), Image.LANCZOS)
s = Image.new('L', (W, st.height + 10 + im.height), 255)
s.paste(st, (0, 0)); s.paste(im, (W - im.width, st.height + 10))
s.save(out); print(out, s.size)
