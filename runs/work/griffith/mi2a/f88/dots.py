import sys
from PIL import Image
# dots.py leaf x0 y0 x1 y1: list small compact blobs (dots) left to right with sizes
leaf = sys.argv[1]; x0, y0, x1, y1 = map(int, sys.argv[2:6])
im = Image.open(f'/private/tmp/claude-501/griffith/mi2_n{leaf}.jpg').convert('L').crop((x0, y0, x1, y1))
w, h = im.size; px = im.load(); thr = 110
seen = [[False]*w for _ in range(h)]; blobs = []
for y in range(h):
    for x in range(w):
        if px[x, y] < thr and not seen[y][x]:
            st = [(x, y)]; seen[y][x] = True; pts = []
            while st:
                a, b = st.pop(); pts.append((a, b))
                for da in (-1, 0, 1):
                    for db in (-1, 0, 1):
                        c, d = a + da, b + db
                        if 0 <= c < w and 0 <= d < h and not seen[d][c] and px[c, d] < thr:
                            seen[d][c] = True; st.append((c, d))
            xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
            bw, bh = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
            if len(pts) > 15: blobs.append((min(xs) + x0, min(ys) + y0, bw, bh, len(pts)))
blobs.sort()
for b in blobs: print(b)
