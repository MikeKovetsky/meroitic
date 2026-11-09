"""Do Meroitic words look like their Nubian-family equivalents more than chance?

For every Meroitic word with an accepted meaning, find the words with the same
meaning in each Northern East Sudanic list (data/nes/*.tsv) and take the best
form similarity. Then shuffle the Meroitic meanings 2,000 times and recompute:
if the real pairing beats most shuffles, the lists carry a family signal.
Also prints the closest pairs, as candidate cognates.
"""
import csv, json, random, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STOP = {"a", "an", "the", "to", "of", "be", "one", "s", "sg", "pl", "n", "v", "adj"}


def skeleton(form):
    f = form.lower()
    f = (f.replace("x", "h").replace("š", "s").replace("ñ", "n").replace("ŋ", "n")
         .replace("q", "k").replace("ḫ", "h").replace("ẖ", "h").replace("ç", "c"))
    f = re.sub(r"[^a-z]", "", f)
    f = re.sub(r"(.)\1+", r"\1", f)
    return f


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def sim(a, b):
    a, b = skeleton(a), skeleton(b)
    if not a or not b:
        return 0.0
    return 1 - lev(a, b) / max(len(a), len(b))


def keys(gloss):
    words = re.split(r"[^a-z]+", gloss.lower())
    return {w for w in words if w and w not in STOP and len(w) > 2}


def load_nes():
    rows = []
    for p in sorted((ROOT / "data/nes").glob("*.tsv")):
        with open(p) as f:
            for r in csv.DictReader(f, delimiter="\t"):
                if r.get("form") and r.get("gloss"):
                    rows.append((p.stem, r["form"], keys(r["gloss"])))
    return rows


def best_matches(mero, nes):
    out = []
    for form, k in mero:
        cands = [(sim(form, f), lang, f) for lang, f, g in nes if k & g]
        if cands:
            out.append((form, max(cands)))
    return out


def main(sims=2000):
    gold = json.load(open(ROOT / "data/gold_lexicon.json"))
    mero = [(g["form"], keys(g["gloss"])) for g in gold
            if g.get("category") not in ("deity", "place", "people") and keys(g["gloss"])]
    nes = load_nes()
    real = best_matches(mero, nes)
    stat = sum(s for _, (s, _, _) in real) / max(1, len(real))
    rng, ge = random.Random(3), 0
    glosses = [k for _, k in mero]
    for _ in range(sims):
        rng.shuffle(glosses)
        sh = best_matches([(f, k) for (f, _), k in zip(mero, glosses)], nes)
        s = sum(x for _, (x, _, _) in sh) / max(1, len(sh))
        ge += s >= stat
    print(f"meroitic words with a same-meaning NES word: {len(real)} of {len(mero)}")
    print(f"mean best similarity {stat:.3f}; shuffled >= real in {ge}/{sims} (p={ge / sims:.4f})")
    for form, (s, lang, f) in sorted(real, key=lambda x: -x[1][0])[:25]:
        print(f"  {s:.2f} {form:12} ~ {lang}:{f}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2000)
