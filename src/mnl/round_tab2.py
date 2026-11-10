"""Per page: what the reader typed for each round letter against the reference sign.
  python3 -I round_tab2.py <reading.txt> <otten FHN file> <page,page,...>
"""
import sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mnl_signs as S
import mnl_round as R
from mnl_score import align, heyler_rows, split

if len(sys.argv) < 4:
    sys.exit(__doc__)
S.need(*sys.argv[1:3])
pages = sys.argv[3].split(",")
ref, _ = split(S.tokens(S.fhn(Path(sys.argv[2]).read_text())))
ref0 = ["0" if t in "oqd" else t for t in ref]
rows = heyler_rows(sys.argv[1])
tab = defaultdict(Counter)
tot = Counter()
for p in pages:
    toks, raw = [], []
    for text, _ in S.heyler_lines([r[3] for r in rows if r[0] == p]):
        for w in R.parse(text):
            for s, lab in w:
                toks.append(s); raw.append(lab)
    ops = align(toks, ref0, free_ref_ends=True)
    c = Counter(o for o, _, _ in ops)
    tot.update(c)
    for o, i, j in ops:
        if o in "=s" and raw[i]:
            tab[raw[i]][ref[j] if ref[j] in "oqd" else "other"] += 1
n = tot["="] + tot["s"] + tot["d"]
print(f"round letters as one: agreement {tot['='] / n:.1%} of {n} reference signs (different {tot['s']}, extra {tot['i']}, missing {tot['d']})")
for k in sorted(tab):
    m = sum(tab[k].values())
    print(f"  typed {k:3} ({m:3}): " + ", ".join(f"{r} {v} ({v / m:.0%})" for r, v in tab[k].most_common()))
