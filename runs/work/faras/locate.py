"""locate.py: find each Faras copy on its page from the ink lines: (page, y0, y1, x0, x1) in pixels."""
import collections, json, subprocess, sys
S = "/private/tmp/claude-501/-Users-mike-repos-mike-meroitic--claude-worktrees-f2-finish-23c420/590bbaca-8cd8-4d82-898d-49b4ecf39ba1/scratchpad"
PAGES = {603: [1], 604: [2], 607: [3], 608: [4], 609: [5, 6], 610: [7, 8], 611: [9, 10], 612: [11], 613: [12, 13],
         614: [14, 15], 617: [16, 17], 618: [18], 619: [19, 20], 623: [21], 624: [22], 625: [23, 24], 626: [25],
         627: [26, 27], 628: [28], 631: [29, 30], 632: [31, 32], 633: [33], 634: [34], 635: [35, 36], 636: [37],
         637: [38, 39], 638: [40, 41], 641: [42, 43], 642: [44], 646: [45], 647: [46]}
def lines(p):
    out = subprocess.run([f"{S}/tools/pdfpng", "lines", f"{S}/allpages/p{p}.png"], capture_output=True, text=True).stdout
    return [tuple(map(int, l.split())) for l in out.splitlines()]
res = {}
for p, texts in PAGES.items():
    ls = lines(p)
    big = [l for l in ls if l[1] - l[0] > 150]
    L = collections.Counter(round(l[2] / 10) for l in big).most_common(1)[0][0] * 10
    R = collections.Counter(round(l[3] / 10) for l in big).most_common(1)[0][0] * 10
    heads = [i for i, l in enumerate(ls) if l[2] > 1000 and l[3] < 1750 and 35 < l[1] - l[0] < 110]
    print(f"p{p} L={L} R={R} heads={len(heads)} texts={texts}")
    for k, n in enumerate(texts):
        if k >= len(heads):
            print("  no heading for", n); continue
        i = heads[k] + 1
        copy = []
        while i < len(ls) and i not in heads:
            y0, y1, x0, x1, ink = ls[i]
            printed = (abs(x0 - L) <= 35 or abs(x0 - L - 95) <= 35) and abs(x1 - R) <= 40
            if printed and copy:
                break
            copy.append(ls[i]); i += 1
        nxt = ls[i] if i < len(ls) else None
        res[n] = (p, copy[0][0], copy[-1][1], min(c[2] for c in copy), max(c[3] for c in copy))
        print(f"  {n}: copy {res[n][1]}-{res[n][2]} x{res[n][3]}-{res[n][4]} ({len(copy)} blocks); next {nxt}")
json.dump(res, open(f"{S}/tools/located.json", "w"))
