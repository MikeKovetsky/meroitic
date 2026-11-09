"""Do Meroitic words look like their Nubian-family equivalents more than chance?

For every Meroitic word with an accepted meaning, find the words with the same
meaning in each Northern East Sudanic list (data/nes/*.tsv) and take the best
form similarity. Then shuffle the Meroitic meanings 2,000 times and recompute:
if the real pairing beats most shuffles, the lists carry a family signal.
Also prints the closest pairs, as candidate cognates.

proto_nes.tsv is left out: Rilly reconstructed and chose those forms while
comparing them with Meroitic (many rows cite the Meroitic form), so they would
make the test circular. Forms are compared as plain letters: accents and tone
marks dropped, IPA letters turned into their nearest Latin letter, and each
variant of a "kello ~ kellω" form tried on its own.
"""
import csv, functools, json, random, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STOP = {"a", "an", "the", "to", "of", "be", "one", "s", "sg", "pl", "n", "v", "adj"}
CIRCULAR = {"proto_nes"}
# IPA letters, then ASJP's digits (3 = high central vowel, 5 = palatal nasal, 7 = glottal stop, 8 = dental fricative)
PLAIN = str.maketrans({"ɛ": "e", "ə": "e", "ɪ": "i", "ı": "i", "ɨ": "i", "ɔ": "o", "ω": "o", "ʊ": "u", "ʉ": "u",
                       "ʌ": "a", "ɑ": "a", "æ": "a", "ɲ": "n", "ŋ": "n", "ʃ": "s", "ɕ": "s", "ʒ": "z", "ʓ": "z",
                       "ɽ": "r", "ɾ": "r", "ɖ": "d", "ɗ": "d", "ð": "d", "ɓ": "b", "β": "b", "ʈ": "t", "θ": "t",
                       "ɡ": "g", "ɣ": "g", "ʋ": "v", "ɟ": "j", "ʄ": "j", "χ": "h", "ħ": "h", "x": "h", "q": "k",
                       "3": "e", "5": "n", "7": "", "8": "t"})


def skeleton(form):
    f = unicodedata.normalize("NFD", form.lower())
    f = "".join(c for c in f if not unicodedata.combining(c)).translate(PLAIN)
    f = re.sub(r"[^a-z]", "", f)
    return re.sub(r"(.)\1+", r"\1", f)


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


@functools.lru_cache(maxsize=None)
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
        if "meroitic" in p.stem or p.stem.startswith("sound_") or p.stem in CIRCULAR:
            continue
        with open(p) as f:
            for r in csv.DictReader(f, delimiter="\t"):
                if r.get("form") and r.get("gloss"):
                    rows += [(p.stem, v, keys(r["gloss"])) for v in re.split(r"\s*[~/,]\s*", r["form"]) if v.strip()]
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
    # the real pairing counts as one of the arrangements, so p is never 0
    print(f"mean best similarity {stat:.3f}; shuffled >= real in {ge}/{sims} (p={(ge + 1) / (sims + 1):.4f})")
    for form, (s, lang, f) in sorted(real, key=lambda x: -x[1][0])[:25]:
        print(f"  {s:.2f} {form:12} ~ {lang}:{f}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2000)
