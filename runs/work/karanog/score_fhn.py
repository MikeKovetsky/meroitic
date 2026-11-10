"""Score readings of Kar. 47, 77, 78 and 121 against FHN III, the way the first test scored its readings.

  python3 -I runs/work/karanog/score_fhn.py <repo root> <name> <file.jsonl> [<file.jsonl> ...]

Each file holds objects with "text" ("Kar. 47"), "part" and "reading"; parts of one text are joined in file order.
The tokenizer, the alignment and the FHN texts are the first test's (runs/work/griffith/score.py and
runs/work/handcopy/score_hc.py), and so is the measure: the signs right are the edition's signs less the edit
distance, so a sign the reading has and the edition has not counts against it too. Kar. 47, 77 and 78 are also
scored against Carrier's edition (Meroitic Newsletter 28, in copyright) when the local copy of the Newsletter texts
is there (data/sources/mnl/mnl_texts.jsonl, not in the repo); only counts are printed.
"""
import json, re, sys, unicodedata
from pathlib import Path

KAR = {"47": "0247", "77": "0277", "78": "0278", "121": "0321"}
CARRIER = "data/sources/mnl/mnl_texts.jsonl"


def first_test(root):
    """The first test's tokenizer and alignment, and its FHN texts."""
    ns, env = {}, {}
    exec((root / "runs/work/griffith/score.py").read_text().split("# Mine:")[0], ns)
    src = (root / "runs/work/handcopy/score_hc.py").read_text()
    exec(src[src.index("FHN = {"):src.index("MINE = ")], env)
    return (lambda s: ns["toks"](re.sub(r"\(([^\d)]+)\)", r"\1", s))), ns["align"], env["FHN"]


def clean(reading):
    """A reading without line numbers, lost signs and query marks, each of which parts two signs: "arwt(14)e" is
    t and e, and "s?e" is s and e, not the te and se signs."""
    return re.sub(r"\(\d+\)|\[\.\]|\?", " ", reading)


def readings(files):
    """{REM number: the reading} for the four texts, the parts of a text joined in file order."""
    rd = {}
    for p in files:
        for line in Path(p).read_text().splitlines():
            if line.strip():
                o = json.loads(line)
                m = re.match(r"Kar\.\s*(\d+)$", o["text"].strip())
                if m and m.group(1) in KAR:
                    rem = KAR[m.group(1)]
                    rd[rem] = rd.get(rem, "") + " " + o["reading"]
    return rd


def carrier(root):
    """Carrier's REM 0247, 0277 and 0278 in the readings' spelling (ne is ñ; his circled line numbers and the
    stray "(" printed before 0247 are not signs; his bracketed signs count, as FHN's do), or {} without the file."""
    p = root / CARRIER
    if not p.exists():
        return {}
    out = {}
    for line in p.read_text().splitlines():
        r = json.loads(line)
        if r.get("rem") in ("0247", "0277", "0278") and "Newsletter 28" in r.get("source", ""):
            t = "".join(" " if unicodedata.name(c, "").startswith("CIRCLED") else c for c in " ".join(r["lines"]))
            out[r["rem"]] = t.replace("(", " ").replace("ne", "ñ")
    return out


def score(toks, align, edition, rd):
    """{REM number: (the edition's signs, right, different, missing, extra, [(reading, edition)])}."""
    out = {}
    for rem, text in edition.items():
        if rem in rd:
            b = toks(text)
            d, ops = align(toks(clean(rd[rem])), b)
            count = lambda kind: sum(op[0] == kind for op in ops)
            out[rem] = (len(b), len(b) - d, count("sub"), count("del"), count("ins"),
                        [(op[1], op[2]) for op in ops if op[0] == "sub"])
    return out


def main():
    root, name, files = Path(sys.argv[1]), sys.argv[2], sys.argv[3:]
    toks, align, fhn = first_test(root)
    rd = readings(files)
    print(name)
    for label, edition in (("FHN III", fhn), ("Carrier, Meroitic Newsletter 28", carrier(root))):
        if not edition:
            print(f"  {label}: not scored ({CARRIER} is kept locally and is not here)")
            continue
        res = score(toks, align, edition, rd)
        print(f"  {label}")
        for kar, rem in KAR.items():
            if rem not in edition:
                continue
            if rem not in res:
                print(f"    Kar. {kar}: no reading")
                continue
            n, right, subs, dels, ins, wrong = res[rem]
            print(f"    Kar. {kar}: {right} of {n} signs right ({right / n:.1%}); different {subs}, missing {dels}, "
                  f"extra {ins}; (reading, edition): {wrong[:16]}")
        n, right = sum(r[0] for r in res.values()), sum(r[1] for r in res.values())
        if n:
            print(f"    ALL: {right} of {n} ({right / n:.1%})")


if __name__ == "__main__":
    main()
