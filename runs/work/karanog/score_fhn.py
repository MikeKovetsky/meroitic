"""Score fresh readings of Kar. 47, 77, 78 and 121 against FHN III, with the first test's tokenizer and alignment.

  python3 -I score_kar2.py <repo root> <name> <file.jsonl> [<file.jsonl> ...]

Each file holds objects with "text" ("Kar. 47"), "part" and "reading"; parts of one text are joined in file order.
"""
import json, re, sys
from pathlib import Path
ROOT = Path(sys.argv[1])
ns = {}
exec((ROOT / "runs/work/griffith/score.py").read_text().split("# Mine:")[0], ns)
_toks, align = ns["toks"], ns["align"]
toks = lambda s: _toks(re.sub(r"\(([^\d)]+)\)", r"\1", s))
src = (ROOT / "runs/work/handcopy/score_hc.py").read_text()
env = {}
exec(src[src.index("FHN = {"):src.index("MINE = ")], env)
FHN = env["FHN"]
KAR = {"47": "0247", "77": "0277", "78": "0278", "121": "0321"}

def clean(s):
    s = re.sub(r"\(\d+\)", " ", s)
    return s.replace("[.]", " ").replace("?", "")

rd = {}
for p in sys.argv[3:]:
    for line in Path(p).read_text().splitlines():
        if line.strip():
            o = json.loads(line)
            m = re.match(r"Kar\.\s*(\d+)$", o["text"].strip())
            if m and m.group(1) in KAR:
                rd[m.group(1)] = rd.get(m.group(1), "") + " " + o["reading"]
tot_ok = tot_n = 0
print(sys.argv[2])
for kar, rem in KAR.items():
    if kar not in rd:
        print(f"  Kar. {kar}: no reading"); continue
    a, b = toks(clean(rd[kar])), toks(FHN[rem])
    d, ops = align(a, b)
    subs = sum(op[0] == "sub" for op in ops); dels = sum(op[0] == "del" for op in ops); ins = sum(op[0] == "ins" for op in ops)
    match = len(b) - subs - dels
    wrong = [(op[1], op[2]) for op in ops if op[0] == "sub"]
    tot_ok += match; tot_n += len(b)
    print(f"  Kar. {kar}: {match} of {len(b)} FHN signs ({match / len(b):.1%}); different {subs}, missing {dels}, extra {ins}; (mine, FHN): {wrong[:16]}")
if tot_n:
    print(f"  ALL: {tot_ok} of {tot_n} ({tot_ok / tot_n:.1%})")
