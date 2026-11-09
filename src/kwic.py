"""Concordance: every occurrence of a word (or regex over words) with context.

  python3 src/kwic.py WORD [--re] [--width 5] [--src narrative|funerary]
"""
import argparse, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("word")
    ap.add_argument("--re", action="store_true")
    ap.add_argument("--width", type=int, default=5)
    ap.add_argument("--src")
    ap.add_argument("--max", type=int, default=60)
    a = ap.parse_args()
    pat = re.compile(a.word if a.re else re.escape(a.word) + "$")
    n = 0
    for r in map(json.loads, open(ROOT / "data/corpus.jsonl")):
        if a.src and r["src"] != a.src:
            continue
        t = r["text"].split()
        for i, w in enumerate(t):
            if pat.match(w):
                n += 1
                if n <= a.max:
                    left = " ".join(t[max(0, i - a.width):i])
                    right = " ".join(t[i + 1:i + 1 + a.width])
                    print(f"{r['id']:>12} | {left:>45} [{w}] {right}")
    print(f"{n} hits")


if __name__ == "__main__":
    main()
