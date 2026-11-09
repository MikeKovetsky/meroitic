"""Kober-style affix table: endings and beginnings shared by many stems.

For every word type and every split stem+ending (ending 1-5 letters), count
how many distinct stems take that ending where the stem also occurs on its own
or with another ending. The top endings, with example stems, are what a
grammar has to explain.
"""
import collections, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def table(words, side="suffix", top=40, maxlen=5):
    types = collections.Counter(words)
    vocab = set(types)
    pieces = collections.defaultdict(set)
    for w in vocab:
        for n in range(1, min(maxlen, len(w) - 1) + 1):
            stem, aff = (w[:-n], w[-n:]) if side == "suffix" else (w[n:], w[:n])
            pieces[stem].add(aff)
    support = collections.defaultdict(set)
    for stem, affs in pieces.items():
        if len(stem) < 2:
            continue
        if stem in vocab or len(affs) >= 2:
            for a in affs:
                support[a].add(stem)
    rows = sorted(support.items(), key=lambda kv: -len(kv[1]))[:top]
    return [{"affix": a, "stems": len(s), "examples": sorted(s, key=lambda x: -types[x])[:8]} for a, s in rows]


if __name__ == "__main__":
    corpus = [json.loads(l) for l in open(ROOT / "data/corpus.jsonl")]
    words = [w for r in corpus for w in r["text"].split() if "NAME" not in w and not w.isdigit()]
    for side in ("suffix", "prefix"):
        for r in table(words, side, top=12):
            print(side, r["affix"], r["stems"], r["examples"][:6])
