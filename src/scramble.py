"""Re-spell the corpus with a random one-to-one letter swap.

Every sign maps to a different Latin letter and never to itself, so the
scrambled corpus keeps all structure (repeats, word order, affixes, numerals,
NAME masks) and loses every surface form a reader could recall.
"""
import json, random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIGNS = list("abdeghiklmnopqrstuwxyNSX")
TARGET = list("abcdefghijklmnopqrstuvwxyz")
KEEP = {"NAME", "RNAME"}


def make_map(seed):
    rng = random.Random(seed)
    while True:
        out = rng.sample(TARGET, len(SIGNS))
        if all(s.lower() != o for s, o in zip(SIGNS, out)):
            return dict(zip(SIGNS, out))


def word(w, m):
    return w if w in KEEP else "".join(m.get(c, c) for c in w)


def text(t, m):
    return " ".join(word(w, m) for w in t.split())


if __name__ == "__main__":
    m = make_map(7)
    assert len(set(m.values())) == len(m)
    print(json.dumps(m))
    print(text("woSi Soreyi qo NAME qowi ato mXe psixrkete 32 abr", m))
