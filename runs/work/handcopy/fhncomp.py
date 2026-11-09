import sys
from PIL import Image, ImageChops
import numpy as np
for p in sys.argv[1:]:
    layers = []
    for k in range(5):
        try: I = Image.open('fhn/p%s_%d.png' % (p, k)).convert('L')
        except FileNotFoundError: break
        a = np.array(I.resize((1926, 2834)))
        print(p, k, I.size, round(a.mean(), 1))
        layers.append(a)
    # text layers: those mostly white with dark text; combine by min over layers whose mean > 200
    txt = [a for a in layers[1:] if a.mean() > 200] or layers
    comp = np.minimum.reduce(txt)
    Image.fromarray(comp).save('fhn/comp_%s.png' % p)
