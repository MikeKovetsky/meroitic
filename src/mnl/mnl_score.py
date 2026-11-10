"""Score a blind reading against a reference text, sign by sign.

  python3 -I mnl_score.py heyler <reading.txt> <otten file> [--pages p05,p06] [--swap-h]
  python3 -I mnl_score.py millet <reading.txt> <otten FHN file> <otten Millet-thesis file>
  python3 -I mnl_score.py pair   <reading A> <reading B>            (two readings of the same pages)
  python3 -I mnl_score.py three  <reading A> <reading B> <otten file>

A reading line is "page | inscription | segment | text" (heyler) or "entry | text" (millet).
Word boundaries are scored apart from the signs.
"""
import re
import sys
from collections import Counter, defaultdict
from itertools import groupby
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mnl_signs as S  # noqa: E402


def align(read, ref, free_read_ends=False, free_ref_ends=False):
    """Edit-distance alignment. Returns a list of (op, read index or None, ref index or None); op is = s i d.

    free_read_ends: reading may have extra signs before and after the reference (not counted).
    free_ref_ends: the reference may run on before and after the reading (not counted).
    """
    n, m = len(read), len(ref)
    prev = [0 if free_ref_ends else j for j in range(m + 1)]
    back = [bytearray(m + 1) for _ in range(n + 1)]      # 0 diag, 1 up (reading-only sign), 2 left (ref-only sign)
    for j in range(1, m + 1):
        back[0][j] = 2
    for i in range(1, n + 1):
        cur = [0 if free_read_ends else i] + [0] * m
        back[i][0] = 1
        ri = read[i - 1]
        bi = back[i]
        for j in range(1, m + 1):
            d = prev[j - 1] + (ri != ref[j - 1])
            u = prev[j] + 1
            l = cur[j - 1] + 1
            if d <= u and d <= l:
                cur[j] = d
            elif u <= l:
                cur[j] = u
                bi[j] = 1
            else:
                cur[j] = l
                bi[j] = 2
        prev = cur
    # end point
    i, j = n, m
    if free_ref_ends:
        j = min(range(m + 1), key=lambda k: prev[k])
    ops = []
    if free_read_ends:
        # recompute the best end row for the full reference: rerun cheaply by tracking the last column
        col = _last_column(read, ref, free_ref_ends)
        i = min(range(n + 1), key=lambda k: col[k])
    while i > 0 or j > 0:
        if i == 0 and free_ref_ends:
            break
        if j == 0 and free_read_ends:
            break
        b = back[i][j]
        if i > 0 and j > 0 and b == 0:
            ops.append(("=" if read[i - 1] == ref[j - 1] else "s", i - 1, j - 1))
            i, j = i - 1, j - 1
        elif i > 0 and (b == 1 or j == 0):
            ops.append(("i", i - 1, None))
            i -= 1
        else:
            ops.append(("d", None, j - 1))
            j -= 1
    ops.reverse()
    return ops


def _last_column(read, ref, free_ref_ends):
    n, m = len(read), len(ref)
    prev = [0 if free_ref_ends else j for j in range(m + 1)]
    col = [prev[m]]
    for i in range(1, n + 1):
        cur = [0] + [0] * m
        ri = read[i - 1]
        for j in range(1, m + 1):
            d = prev[j - 1] + (ri != ref[j - 1])
            u = prev[j] + 1
            l = cur[j - 1] + 1
            cur[j] = d if d <= u and d <= l else (u if u <= l else l)
        prev = cur
        col.append(cur[m])
    return col


def split(toks):
    """Signs without the boundary marks, and the set of sign positions a word ends after."""
    signs, ends = [], set()
    for t in toks:
        if t == "|":
            if signs:
                ends.add(len(signs) - 1)
        else:
            signs.append(t)
    return signs, ends


def heyler_rows(path):
    """The reading's lines (page, inscription, segment, text), first printings only (mnl_signs.first_printing)."""
    rows = [[p.strip() for p in line.split("|", 3)] for line in Path(path).read_text().splitlines()]
    return S.first_printing([(p, i, (p, i, g), t) for p, i, g, t in (r for r in rows if len(r) == 4)])


def read_heyler(path, pages=None, g="x", x="X"):
    rows = [r for r in heyler_rows(path) if not pages or r[0] in pages]
    toks, page_of = [], []
    for page, group in groupby(rows, key=lambda r: r[0]):
        for text, _ in S.heyler_lines([r[3] for r in group]):
            for t in S.tokens(S.heyler(text, g, x)):
                toks.append(t)
                page_of.append(page)
    body = [re.sub(S.CONTINUED, "", r[3]) for r in rows]
    return toks, page_of, dict(lines=len(rows), unsure=sum(b.count("?") for b in body),
                               unread=sum(b.count("#") for b in body), cut=sum(b.count(">>") for b in body))


def report(name, ops, read, ref, read_ends, ref_ends, page_of=None):
    c = Counter(o for o, _, _ in ops)
    ref_len = c["="] + c["s"] + c["d"]
    print(f"{name}: reference signs covered {ref_len}, reading signs {c['='] + c['s'] + c['i']}")
    print(f"  same {c['=']}  different {c['s']}  only in reading {c['i']}  only in reference {c['d']}")
    print(f"  agreement {c['='] / max(1, ref_len):.1%} of reference signs "
          f"(errors per 100 reference signs {100 * (c['s'] + c['i'] + c['d']) / max(1, ref_len):.1f})")
    conf = Counter()
    for o, i, j in ops:
        if o == "s":
            conf[(read[i], ref[j])] += 1
        elif o == "i":
            conf[(read[i], "-")] += 1
        elif o == "d":
            conf[("-", ref[j])] += 1
    print("  most frequent differences (reading, reference):", conf.most_common(14))
    both = [(i, j) for o, i, j in ops if o in "=s"]
    r_end = sum(1 for i, j in both if i in read_ends)
    f_end = sum(1 for i, j in both if j in ref_ends)
    same_end = sum(1 for i, j in both if i in read_ends and j in ref_ends)
    print(f"  word ends: reading {r_end}, reference {f_end}, at the same sign {same_end} "
          f"({same_end / max(1, f_end):.0%} of the reference's, {same_end / max(1, r_end):.0%} of the reading's)")
    if page_of:
        per = defaultdict(Counter)
        last = None
        for o, i, j in ops:
            if i is not None:
                last = page_of[i]
            if last is not None:
                per[last][o] += 1
        for p in sorted(per):
            k = per[p]
            n = k["="] + k["s"] + k["d"]
            print(f"    {p}: {k['='] / max(1, n):.1%} of {n} reference signs (different {k['s']}, extra {k['i']}, missing {k['d']})")
    return c


def main():
    mode = sys.argv[1]
    if mode == "heyler":
        pages = None
        if "--pages" in sys.argv:
            pages = set(sys.argv[sys.argv.index("--pages") + 1].split(","))
        g, x = ("X", "x") if "--swap-h" in sys.argv else ("x", "X")
        toks, page_of, info = read_heyler(sys.argv[2], pages, g, x)
        print("reading:", info)
        page_signs = [p for t, p in zip(toks, page_of) if t != "|"]
        read, read_ends = split(toks)
        ref, ref_ends = split(S.tokens(S.fhn(Path(sys.argv[3]).read_text())))
        if "--fold-round" in sys.argv:                    # the printer's look-alike round letters count as one
            read = ["0" if t in "oqd" else t for t in read]
            ref = ["0" if t in "oqd" else t for t in ref]
        if pages:
            for p in sorted(pages):
                idx = [k for k, q in enumerate(page_signs) if q == p]
                if not idx:
                    continue
                sub = read[idx[0]:idx[-1] + 1]
                ends = {e - idx[0] for e in read_ends if idx[0] <= e <= idx[-1]}
                ops = align(sub, ref, free_ref_ends=True)
                report(p, ops, sub, ref, ends, ref_ends)
        else:
            ops = align(read, ref, free_read_ends=True)
            report("whole text", ops, read, ref, read_ends, ref_ends, page_signs)
    elif mode == "millet":
        text = "\n".join(l.split("|", 1)[1] for l in Path(sys.argv[2]).read_text().splitlines() if "|" in l and not l.startswith("-"))
        read, read_ends = split(S.tokens(S.millet_2003(text)))
        for label, path, conv in (("against Otten's FHN file", sys.argv[3], S.fhn), ("against Otten's file of Millet's thesis", sys.argv[4], S.millet_thesis)):
            ref, ref_ends = split(S.tokens(conv(Path(path).read_text())))
            ops = align(read, ref)
            report(label, ops, read, ref, read_ends, ref_ends)
            diffs = [(o, read[i] if i is not None else "-", ref[j] if j is not None else "-", i, j) for o, i, j in ops if o != "="]
            print("   every difference (kind, reading, reference, reading pos, reference pos):", diffs[:60])
    elif mode == "pair":
        a, pa, ia = read_heyler(sys.argv[2])
        b, pb, ib = read_heyler(sys.argv[3])
        pages = sorted(set(pa) & set(pb))
        print("pages in both:", pages)
        tot = Counter()
        for p in pages:
            ra, ea = split([t for t, q in zip(a, pa) if q == p])
            rb, eb = split([t for t, q in zip(b, pb) if q == p])
            ops = align(ra, rb)
            tot.update(report(f"{p} (A as reading, B as reference)", ops, ra, rb, ea, eb))
        n = tot["="] + tot["s"] + tot["d"]
        print(f"ALL PAGES: the two readings agree on {tot['='] / max(1, n):.1%} of {n} signs")
    elif mode == "three":
        a, pa, _ = read_heyler(sys.argv[2])
        b, pb, _ = read_heyler(sys.argv[3])
        ref, _ = split(S.tokens(S.fhn(Path(sys.argv[4]).read_text())))
        k = Counter()
        for p in sorted(set(pa) & set(pb)):
            ra, _ = split([t for t, q in zip(a, pa) if q == p])
            rb, _ = split([t for t, q in zip(b, pb) if q == p])
            oa = {j: ra[i] for o, i, j in align(ra, ref, free_ref_ends=True) if o in "=s"}
            ob = {j: rb[i] for o, i, j in align(rb, ref, free_ref_ends=True) if o in "=s"}
            lo = min(list(oa) + list(ob)); hi = max(list(oa) + list(ob))
            for j in range(lo, hi + 1):
                x, y = oa.get(j), ob.get(j)
                if x == y:
                    k["both agree, and with the reference" if x == ref[j] else ("both miss the sign" if x is None else "both agree, against the reference")] += 1
                else:
                    k["readers differ, one has the reference's sign" if ref[j] in (x, y) else "readers differ, neither has the reference's sign"] += 1
        n = sum(k.values())
        for key, v in k.most_common():
            print(f"  {key}: {v} ({v / n:.1%})")
        agree = k["both agree, and with the reference"] + k["both agree, against the reference"]
        print(f"  where the two readers agree on a sign, it is the reference's sign in {k['both agree, and with the reference'] / max(1, agree):.1%} of {agree} cases")


if __name__ == "__main__":
    main()
