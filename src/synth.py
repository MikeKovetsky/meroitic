"""A synthetic inscription language for a leak-free control.

Same scale and texture as the real corpus (about 1,000 short, formulaic texts,
about 20k words, masked names, numerals, a few long narratives, fused and split
endings, lost signs), but every word and ending is invented, so a model can't
know any meaning in advance. The matching test is then built exactly like the
real one: half the meanings given, the other half to match.
"""
import json, random, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLIND = Path("/private/tmp/claude-501/blind")
rng = random.Random(2026)
C, V = list("ptkbdgmnlrszhwyf"), list("aeiou")


def syl():
    return rng.choice(C) + rng.choice(V) + (rng.choice("nlrsk") if rng.random() < 0.25 else "")


def stem(n=None):
    return "".join(syl() for _ in range(n or rng.choice([1, 2, 2, 2, 3])))


MEANINGS = {
    "deity": ["GOD_A", "GOD_B", "GOD_C", "GOD_D"],
    "noun": ["water", "bread", "beer", "milk", "ox", "cow", "sheep", "gold", "silver", "field", "house",
             "temple", "offering", "life", "city", "land", "boat"],
    "person": ["king", "queen", "prince", "priest", "scribe", "general", "envoy", "man", "woman", "child",
               "son", "daughter", "brother", "sister", "mother", "father", "wife", "relative", "captive"],
    "adj": ["great", "good", "abundant", "pure", "small"],
    "verb": ["give", "pour", "offer", "take", "love", "go", "seize", "kill", "build", "protect"],
    "filiation": ["born of (mother)", "begotten by (father)"],
    "other": ["and", "two", "adoration"],
}
LEX, used = {}, set()
for cat, ms in MEANINGS.items():
    for m in ms:
        while True:
            s = stem(1 if m in ("and", "two") else None)
            if s not in used:
                used.add(s)
                LEX[m] = s
                break
AFF = {}
for name in ["DET", "PL", "GEN", "LOC", "COP", "VOC", "IMP", "PAST"]:
    while True:
        a = rng.choice(C) + rng.choice(V) if name not in ("VOC",) else rng.choice(V)
        if name in ("COP",):
            a += rng.choice(C) + rng.choice(V)
        if a not in AFF.values():
            AFF[name] = a
            break
PLACES = [stem(2) for _ in range(12)]


def w(m, *affs):
    """A word with endings; endings are written fused or split, as scribes did."""
    out = LEX.get(m, m)
    parts = [out] + [AFF[a] for a in affs]
    s, cur = [], parts[0]
    for p in parts[1:]:
        if rng.random() < 0.25:
            s.append(cur)
            cur = p
        else:
            cur += p
    s.append(cur)
    return " ".join(s)


def noisy(tok):
    if tok.isupper() or tok.isdigit() or rng.random() > 0.03:
        return tok
    i = rng.randrange(len(tok))
    return tok[:i] + "." + tok[i + 1:]


def epitaph():
    t = []
    for g in rng.sample(["GOD_A", "GOD_B"], rng.choice([1, 2])):
        t.append(w(g, "VOC"))
    t += ["NAME", AFF["COP"]] if rng.random() < 0.3 else ["NAME" + AFF["COP"]]
    if rng.random() < 0.85:
        t += ["NAME", w("born of (mother)", "COP")]
    if rng.random() < 0.85:
        t += ["NAME", w("begotten by (father)", "COP")]
    for _ in range(rng.choice([0, 0, 1, 1, 2, 3, 4, 6])):
        rel = rng.choice(["relative", "relative", "brother", "sister", "son", "daughter", "wife", "mother"])
        if rng.random() < 0.6:
            title = rng.choice(["priest", "scribe", "general", "envoy", "prince", "priest"])
            t.append(w(title))
            if rng.random() < 0.4:
                t.append(w(rng.choice(PLACES + [LEX["temple"], LEX["city"]]), "GEN"))
            if title == "priest" and rng.random() < 0.5:
                t.append(w(rng.choice(["GOD_A", "GOD_C", "GOD_D"]), "GEN"))
        t += ["NAME", w(rel, "COP")]
    if rng.random() < 0.3:
        t.append(w(rng.choice(["good", "great"]), "COP"))
    for obj in rng.sample(["water", "bread", "milk", "beer"], rng.choice([1, 2, 2, 3])):
        verb = "pour" if obj in ("water", "milk") else "give"
        adj = rng.choice(["abundant", "abundant", "good", "pure"])
        t += [w(obj), w(adj), w(verb, "IMP")]
    return t


def votive():
    t = [w("adoration"), w(rng.choice(["GOD_A", "GOD_B", "GOD_C"]), "GEN"), "NAME",
         w(rng.choice(["priest", "scribe", "general", "envoy", "king", "queen"]))]
    for _ in range(rng.choice([1, 1, 2])):
        o = rng.choice(["gold", "silver", "ox", "cow", "sheep", "bread", "beer"])
        t += [w(o, "PL") if rng.random() < 0.5 else w(o), str(rng.choice([1, 2, 3, 5, 10, 20]))]
    t += [w(rng.choice(["temple", "house"]), "LOC"), w("offer", "PAST")]
    if rng.random() < 0.4:
        t += [w("life", "GEN"), w("protect", "IMP")]
    return t


def ration():
    t = []
    items = rng.sample(["bread", "beer", "ox", "cow", "sheep", "milk", "field"], rng.choice([2, 3, 4]))
    for i, o in enumerate(items):
        if i == len(items) - 1 and rng.random() < 0.6:
            t.append(LEX["and"])
        t += [w(o), str(rng.choice([1, 2, 3, 4, 6, 8, 12, 20, 40, 100]))]
    if rng.random() < 0.5:
        t += [w("temple", "GEN"), w("offering", "DET")]
    return t


def label():
    k = rng.random()
    if k < 0.4:
        return ["NAME", w(rng.choice(["priest", "scribe", "general", "envoy", "prince", "queen"]))]
    if k < 0.7:
        return ["NAME", w(rng.choice(["son", "daughter", "wife", "brother", "sister"]), "COP"), "NAME"]
    return [w(rng.choice(["general", "envoy", "scribe"])), w(rng.choice(PLACES), "GEN"), "NAME"]


def narrative():
    t = [w("king"), "RNAME", w("queen"), "RNAME", w("prince"), "RNAME"]
    for _ in range(14):
        p = rng.choice(PLACES)
        t += [w(p, "LOC"), w("go", "PAST")]
        t += [w(rng.choice(["city", "land", "boat"]), "PL"), w("seize", "PAST")]
        if rng.random() < 0.7:
            t += [w("man", "PL"), str(rng.randint(10, 400)), w("woman", "PL"), str(rng.randint(10, 400))]
            if rng.random() < 0.5:
                t += [w("child", "PL"), str(rng.randint(5, 90))]
            t += [w("captive", "PL"), w("take", "PAST")]
        if rng.random() < 0.5:
            t += [w("ox", "PL"), str(rng.randint(20, 900)), LEX["and"], w("cow", "PL"), str(rng.randint(20, 900)),
                  w("take", "PAST")]
        if rng.random() < 0.4:
            t += [w("man", "PL"), w("kill", "PAST")]
        if rng.random() < 0.4:
            t += [w(rng.choice(["GOD_A", "GOD_C"]), "GEN"), w("temple", "DET"), w("build", "PAST"),
                  w("gold"), str(rng.randint(2, 50)), w("give", "PAST")]
        if rng.random() < 0.3:
            t += [w("king"), "RNAME", w(rng.choice(["GOD_A", "GOD_C"]), "GEN"), w("love", "PAST")]
        if rng.random() < 0.2:
            t += [w("prince", "PL"), LEX["two"], w("go", "PAST")]
    return t


def corpus():
    texts = []
    for i in range(1000):
        k = rng.random()
        f = epitaph if k < 0.6 else votive if k < 0.72 else ration if k < 0.82 else label
        texts.append(" ".join(noisy(x) for x in " ".join(f()).split()))
    for _ in range(3):
        texts.append(" ".join(noisy(x) for x in " ".join(narrative()).split()))
    return texts


def build(folds=2, seed=7):
    texts = corpus()
    toks = [x for t in texts for x in t.split()]
    test_pool = [m for m in LEX if not m.startswith("GOD")]
    r = random.Random(seed)
    r.shuffle(test_pool)
    gloss = {m: m for m in test_pool}
    keys = {}
    body_corpus = "\n".join(f"S{i:04d}: {t}" for i, t in enumerate(texts))
    head = open(ROOT / "src/build_tasks.py").read()
    from build_tasks import HEAD   # same instructions as the real test
    for f in range(folds):
        test = [m for i, m in enumerate(test_pool) if i % folds == f]
        given = [m for i, m in enumerate(test_pool) if i % folds != f]
        meanings = test[:]
        random.Random(seed + f).shuffle(meanings)
        run = f"Y_f{f}"
        d = BLIND / run
        d.mkdir(parents=True, exist_ok=True)
        body = HEAD.format(
            what="a corpus of ancient inscriptions in one language, one text per line",
            spelling=("The script has been transliterated letter by letter into a Latin alphabet. Spaces mark word boundaries, "
                      "but scribes sometimes wrote endings apart from their word. NAME stands for a personal name and RNAME for "
                      "a royal name (the names were masked). Digits are numerals. A dot marks a lost sign."),
            glossary="\n".join(f"- {LEX[m]}: {gloss[m]}" for m in given),
            k=len(test), fromcorpus=" from the corpus",
            evidence=" in the corpus: where each word occurs, what it occurs with, its affixes, the glossary words around it",
            words="\n".join(f"- {LEX[m]}" for m in test),
            meanings="\n".join(f"- {x}" for x in meanings), out=d / "answer.json")
        (d / "task.md").write_text(body + "\n## Corpus\n\n" + body_corpus + "\n")
        keys[run] = {LEX[m]: m for m in test}
    old = json.load(open(ROOT / "runs/keys/step0.json"))
    old.update(keys)
    json.dump(old, open(ROOT / "runs/keys/step0.json", "w"), indent=1)
    json.dump({"lexicon": LEX, "affixes": AFF, "places": PLACES}, open(ROOT / "runs/keys/synth_language.json", "w"), indent=1)
    (ROOT / "data/synth_corpus.txt").write_text("\n".join(texts) + "\n")
    print(f"texts {len(texts)} tokens {len(toks)} types {len(set(toks))}; test items {len(test_pool)}")
    print(texts[0][:200]); print(texts[700][:200]); print(texts[-1][:300])


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    build()
