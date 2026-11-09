"""Turn a blind answer's scrambled forms back into real spelling, so a judge
can compare them with the published grammar. Usage: unscramble.py IN OUT"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def inverse():
    m = json.load(open(ROOT / "runs/keys/scramble_map.json"))
    return {v: k for k, v in m.items()}


def real(s, inv):
    # only rewrite lowercase letter runs; keep NAME/RNAME, digits, punctuation
    return re.sub(r"[a-z]+", lambda mo: "".join(inv.get(c, c) for c in mo.group()), s)


def walk(x, inv, key=None):
    if isinstance(x, dict):
        return {k: walk(v, inv, k) for k, v in x.items()}
    if isinstance(x, list):
        return [walk(v, inv, key) for v in x]
    if isinstance(x, str) and key in ("form", "word", "stems", "examples", "segments_text"):
        return real(x, inv)
    return x


if __name__ == "__main__":
    inv = inverse()
    data = json.load(open(sys.argv[1]))
    json.dump(walk(data, inv), open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
    print("wrote", sys.argv[2])
