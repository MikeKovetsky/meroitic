"""cut2.py <outdir> <n> ...: cut each Faras copy (placed by its ink lines) into an overview, enlarged pieces and a
context crop for the check."""
import json, subprocess, sys
S = "/private/tmp/claude-501/-Users-mike-repos-mike-meroitic--claude-worktrees-f2-finish-23c420/590bbaca-8cd8-4d82-898d-49b4ecf39ba1/scratchpad"
C = {1: (603, 924, 1361), 2: (604, 655, 1105), 3: (607, 1546, 2323), 4: (608, 954, 1816), 5: (609, 599, 1111),
     6: (609, 2616, 2962), 7: (610, 701, 1147), 8: (610, 2733, 3191), 9: (611, 948, 1452), 10: (611, 3088, 3853),
     11: (612, 2152, 2616), 12: (613, 1015, 1368), 13: (613, 2917, 3285), 14: (614, 853, 1283), 15: (614, 2163, 2614),
     16: (617, 1234, 1558), 17: (617, 2792, 3522), 18: (618, 1170, 1380), 19: (619, 568, 1127), 20: (619, 2689, 3143),
     21: (623, 539, 2356), 22: (624, 2321, 2803), 23: (625, 501, 1229), 24: (625, 3018, 3799), 25: (626, 1621, 2217),
     26: (627, 373, 1005), 27: (627, 2826, 3264), 28: (628, 1401, 2012), 29: (631, 501, 844), 30: (631, 2500, 3056),
     31: (632, 1301, 1766), 32: (632, 3420, 3744), 33: (633, 1875, 2218), 34: (634, 436, 1746), 35: (635, 783, 1419),
     36: (635, 3299, 3766), 37: (636, 1815, 2527), 38: (637, 606, 1135), 39: (637, 2579, 2831), 40: (638, 362, 815),
     41: (638, 1877, 2776), 42: (641, 775, 995), 43: (641, 2533, 3237), 44: (642, 1575, 3889), 45: (646, 2240, 2639),
     46: (647, 663, 826)}
W, H, PAD, BAND, PIECE, SCALE = 2756, 4515, 25, 330, 950, 1.5
def run(*a):
    return subprocess.run([f"{S}/tools/pdfpng", *map(str, a)], check=True, capture_output=True, text=True).stdout
if __name__ == "__main__":
    out = sys.argv[1]
    for n in map(int, sys.argv[2:]):
        p, y0, y1 = C[n]
        src = f"{S}/allpages/p{p}.png"
        Y0, Y1 = max(0, y0 - PAD), min(H, y1 + PAD)
        b = run("bounds", src, ".05", Y0, ".985", Y1).split()
        X0, X1 = max(0, int(b[0]) - 40), min(W, int(b[2]) + 40)
        run("crop", src, f"{out}/f{n:02d}_0_overview.png", X0, Y0, X1, Y1, .65)
        nx, ny = max(1, -(-(X1 - X0) // PIECE)), max(1, -(-(Y1 - Y0) // BAND))
        pw, ph = (X1 - X0) / nx, (Y1 - Y0) / ny
        names = {1: ["whole"], 2: ["left", "right"], 3: ["left", "middle", "right"]}.get(nx) or [f"part{i + 1}" for i in range(nx)]
        k = 0
        for r in range(ny):
            for c in range(nx):
                k += 1
                run("crop", src, f"{out}/f{n:02d}_{k:02d}_band{r + 1}_{names[c]}.png", int(max(X0, X0 + c * pw - 50)),
                    int(max(Y0, Y0 + r * ph - 30)), int(min(X1, X0 + (c + 1) * pw + 50)), int(min(Y1, Y0 + (r + 1) * ph + 30)), SCALE)
        run("crop", src, f"{out}/context_f{n:02d}.png", int(.04 * W), max(0, y0 - 750), int(.99 * W), min(H, y1 + 750), .5)
        print(f"{n}:{nx}x{ny}", end=" ")
    print()
