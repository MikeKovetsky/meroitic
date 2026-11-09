"""Undo Otten's name-swap augmentation.

src/pool.py shows two swap pools: about 179 private names that every one of
them was swapped with (a clique), and about 11 royal names. Every pool word is
replaced by NAME or RNAME, and identical skeletons collapse to one text.
Texts that differed only in names become one; that is the price of not knowing
which copy was the original.
"""
import collections, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def norm(line):
    return re.sub(r"\s+", " ", line.replace(".", " ")).strip()


def pools():
    partners = json.load(open(ROOT / "data/swap_partners.json"))
    private = {w for w, p in partners.items() if len(p) >= 150}
    royal_seed = "amaniyesbEXe"
    royal = {royal_seed} | {w for w in partners[royal_seed] if w not in private}
    royal = {w for w in royal if len(set(partners[w]) & royal) >= len(royal) - 2}
    return private, royal


def main():
    private, royal = pools()
    lines = [norm(l) for l in (ROOT / "data/otten/Data/mero-corpus.txt").read_text().split("\n")]
    lines = [l for l in lines if l]
    seen, out = {}, []
    for l in lines:
        sk = " ".join("NAME" if w in private else "RNAME" if w in royal else w for w in l.split())
        if sk in seen:
            out[seen[sk]]["copies"] += 1
            continue
        seen[sk] = len(out)
        out.append({"id": f"T{len(out):04d}", "text": sk, "copies": 1})
    with (ROOT / "data/texts.jsonl").open("w") as f:
        for r in out:
            f.write(json.dumps(r) + "\n")
    json.dump({"private": sorted(private), "royal": sorted(royal)},
              open(ROOT / "data/name_pools.json", "w"), indent=1)
    words = [w for r in out for w in r["text"].split()]
    c = collections.Counter(words)
    print(f"private pool {len(private)}, royal pool {len(royal)}: {sorted(royal)}")
    print(f"lines {len(lines)} -> texts {len(out)}; tokens {len(words)}; types {len(c)}")
    print("NAME", c["NAME"], "RNAME", c["RNAME"])
    print(c.most_common(40))


main()
