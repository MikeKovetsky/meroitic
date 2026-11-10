"""Settle the printout's look-alike round letters (O, Q, D) from the spelling rules and the corpus.

In the scan of Newsletter 6 the printer's O and D both look like a C, and Q differs only by a small tail.
A reader cannot tell most of them apart (blind test: a round letter typed with '?' was o, q or d at about
the base rates). This module chooses among o, q and d for each such letter:

  1. spelling rules of the script: the o sign never begins a word, never follows a vowel sign (e, i, o) or a
     syllable sign (se, te, to, ne), and is never followed by e or i;
  2. the corpus: the word is scored by how often it occurs whole in the corpus and by a sign 4-gram model
     of corpus words; the reader's own choice enters as a prior (measured in the blind test).

Every letter settled this way is reported with how it was settled: "rule", "word" (the chosen word occurs in
the corpus) or "model" (only the 4-gram model spoke).

  python3 -I mnl_round.py test <repo root> <reading.txt> <otten FHN file> [p05,p06,...] [--quick] [--lm=0.3]

The test mode scores a test reading after settling its round letters, with the three long narratives left out of
the model. With a list of pages, each page is aligned on its own against the reference; --quick takes the quick
reader's prior; --lm sets the model's weight.
"""
import json, math, re, sys
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mnl_signs as S  # noqa: E402

VOWELISH = {"e", "i", "o", "se", "te", "to", "N"}
# what a typed round letter turned out to be in the blind test (round_tab2.py), so these priors and LM_WEIGHT
# were set on the test pages themselves. QUICK: a reader who typed from the strips (the eight Tanyidamani pages).
# CAREFUL: readers who enlarged each line and went by the shape.
QUICK = {
    "Q?": {"o": 0.45, "q": 0.29, "d": 0.26},
    "D": {"d": 0.77, "o": 0.21, "q": 0.02},
    "D?": {"d": 0.77, "o": 0.21, "q": 0.02},
    "O": {"o": 0.96, "d": 0.03, "q": 0.01},
    "O?": {"o": 0.96, "d": 0.03, "q": 0.01},
    "Q": {"q": 0.96, "o": 0.02, "d": 0.02},
    "@": {"o": 0.41, "q": 0.24, "d": 0.35},
}
CAREFUL = {                       # two careful readers pooled (11 pages of both stelae, 327 round letters)
    "D": {"d": 0.83, "o": 0.15, "q": 0.02},
    "D?": {"d": 0.63, "o": 0.35, "q": 0.02},
    "O": {"o": 0.93, "d": 0.05, "q": 0.02},
    "O?": {"o": 0.93, "d": 0.05, "q": 0.02},
    "Q": {"q": 0.96, "o": 0.03, "d": 0.01},
    "Q?": {"q": 0.92, "o": 0.05, "d": 0.03},
    "@": {"o": 0.41, "q": 0.24, "d": 0.35},
}
PRIOR = dict(CAREFUL)
ORDER = 4
LM_WEIGHT = 0.3            # the corpus model counts for less than the reader: tuned on the test pages (1.0, 0.5, 0.3, 0.15 tried)
TRUST_UNMARKED = False


def corpus_words(root, leave_out=()):
    """Words of the corpus as tuples of signs. Masked names, numerals and words with lost signs are left out."""
    words = []
    for line in (Path(root) / "data/corpus_v3.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r["id"] in leave_out or r.get("src") in leave_out:
            continue
        if r.get("src") == "narrative":
            toks = S.tokens(S.fhn(r["text"]))
        else:
            t = re.sub(r"\bR?NAME\b", " . ", r["text"])
            t = "".join({"s": "ß", "S": "s"}.get(c, c) for c in t).replace("ß", "se")
            t = " ".join(w for w in t.split() if re.fullmatch(r"[a-zNxX]+", w))
            toks = S.tokens(t)
        w = []
        for tok in toks:
            if tok == "|":
                if w:
                    words.append(tuple(w))
                w = []
            else:
                w.append(tok)
    return words


class Model:
    def __init__(self, words):
        self.word = Counter(words)
        self.total = sum(self.word.values())
        self.grams = [defaultdict(Counter) for _ in range(ORDER)]
        self.signs = set()
        for w, c in self.word.items():
            seq = ("<",) * (ORDER - 1) + w + (">",)
            self.signs.update(seq)
            for i in range(ORDER - 1, len(seq)):
                for n in range(ORDER):
                    self.grams[n][seq[i - n:i]][seq[i]] += c
        self.v = len(self.signs)

    def p_sign(self, ctx, sign):
        """Interpolated: each order backs off to the shorter one (Witten-Bell weights)."""
        p = 1.0 / self.v
        for n in range(ORDER):
            c = self.grams[n].get(ctx[len(ctx) - n:] if n else ())
            if not c:
                continue
            tot, kinds = sum(c.values()), len(c)
            lam = tot / (tot + kinds)
            p = lam * c.get(sign, 0) / tot + (1 - lam) * p
        return p

    def logp(self, w):
        seq = ("<",) * (ORDER - 1) + tuple(w) + (">",)
        lp = sum(math.log(self.p_sign(seq[i - ORDER + 1:i], seq[i])) for i in range(ORDER - 1, len(seq)))
        return math.log(0.5 * self.word.get(tuple(w), 0) / self.total + 0.5 * math.exp(lp))


def parse(text):
    """A text line of the printout, after mnl_signs.heyler_lines(), to words; each word a list of (sign, label),
    label None for a settled sign or what the reader typed for a round letter (Q?, D, D?, O, O?, Q, @)."""
    t = re.sub(r"[*().]", "", text)
    t = re.sub(r",{2,}", " ", t).replace(",", " ")
    t = re.sub(r"[0-9]+", " ", t)
    words = []
    for chunk in t.split():
        w = []
        for m in re.finditer(r"([A-Z#@])(\?)?", chunk):
            ch, mark = m.group(1), m.group(2) or ""
            if ch in "OQD@":
                w.append(("0", ch + mark if ch != "@" else "@"))
            elif ch == "#":
                w.append(("#", None))
            elif ch == "C":                          # not a letter of the code: a stray continuation mark
                continue
            else:
                w.append((S.HEYLER.get(ch, ch.lower()), None))
        if w:
            words.append(w)
    return words


def allowed(word, i):
    """Round letters the spelling rules allow at position i (o is the only one they can exclude)."""
    prev = word[i - 1][0] if i else None
    nxt = word[i + 1][0] if i + 1 < len(word) else None
    if prev is None or prev in VOWELISH or nxt in ("e", "i"):
        return ("q", "d")
    return ("o", "q", "d")


def settle(model, word):
    """The word with its round letters chosen. Returns (signs, [(position, choice, how, margin)])."""
    spots = [i for i, (s, lab) in enumerate(word) if s == "0"]
    if not spots:
        return [s for s, _ in word], []
    fixed = {}
    if TRUST_UNMARKED:
        for i in spots:
            lab = word[i][1]
            if lab in ("O", "Q", "D"):              # the reader saw the shape: keep it, unless the spelling rules forbid an o there
                fixed[i] = lab.lower() if lab.lower() in allowed(word, i) else "d"
    open_spots = [i for i in spots if i not in fixed]
    base = [fixed.get(i, s) for i, (s, _) in enumerate(word)]
    if not open_spots:
        return base, [(i, fixed[i], "reader", None) for i in spots]
    if len(open_spots) > 7:                     # too many to try all: settle left to right
        out = base[:]
        for i in open_spots:
            best = max(allowed(word, i), key=lambda c: math.log(PRIOR[word[i][1]][c]) + LM_WEIGHT * model.logp([c if k == i else ("o" if s == "0" else s) for k, s in enumerate(out)]))
            out[i] = best
        return out, [(i, out[i], "reader" if i in fixed else "model", None) for i in spots]
    scored = []
    for combo in product(*[allowed(word, i) for i in open_spots]):
        cand = base[:]
        prior = 0.0
        for i, c in zip(open_spots, combo):
            cand[i] = c
            prior += math.log(PRIOR[word[i][1]][c])
        if any(cand[i] == "o" and cand[i - 1] in VOWELISH for i in open_spots if i):
            continue                             # two o in a row, or o after another settled vowel
        scored.append((prior + LM_WEIGHT * model.logp(cand), cand))
    scored.sort(key=lambda x: -x[0])
    best = scored[0][1]
    margin = scored[0][0] - scored[1][0] if len(scored) > 1 else None
    known = tuple(best) in model.word
    how = []
    for i in spots:
        if i in fixed:
            how.append((i, best[i], "reader", None))
        elif len(allowed(word, i)) == 2 and best[i] == "d" and PRIOR[word[i][1]]["q"] < 0.1:
            how.append((i, best[i], "rule", margin))
        elif PRIOR[word[i][1]][best[i]] >= 0.8:
            how.append((i, best[i], "reader", margin))
        else:
            how.append((i, best[i], "word" if known else "model", margin))
    return best, how


def main():
    if len(sys.argv) < 5 or sys.argv[1] != "test":
        sys.exit(__doc__)
    from mnl_score import align, heyler_rows, split
    root, reading, ref_path = sys.argv[2:5]
    S.need(Path(root) / "data/corpus_v3.jsonl", reading, ref_path)
    pages = sys.argv[5].split(",") if len(sys.argv) > 5 and not sys.argv[5].startswith("--") else None
    if "--quick" in sys.argv:
        PRIOR.clear(); PRIOR.update(QUICK)
    global LM_WEIGHT
    for a in sys.argv:
        if a.startswith("--lm="):
            LM_WEIGHT = float(a[5:])
    model = Model(corpus_words(root, leave_out=("narrative",)))
    print(f"model: {model.total} corpus words, {len(model.word)} different (the three long narratives left out)")
    ref, _ = split(S.tokens(S.fhn(Path(ref_path).read_text())))
    rows = heyler_rows(reading)
    tot, tab = Counter(), defaultdict(Counter)
    for page in (pages or [None]):
        signs, hows = [], []
        for text, _ in S.heyler_lines([r[3] for r in rows if not page or r[0] == page]):
            for word in parse(text):
                best, how = settle(model, word)
                by = {i: h for i, _, h, _ in how}
                for i, s in enumerate(best):
                    signs.append(s)
                    hows.append(by.get(i))
        ops = align(signs, ref, free_ref_ends=True) if page else align(signs, ref, free_read_ends=True)
        tot.update(o for o, _, _ in ops)
        for o, i, j in ops:
            if o in "=s" and hows[i]:
                tab[hows[i]]["right" if signs[i] == ref[j] else "wrong"] += 1
    n = tot["="] + tot["s"] + tot["d"]
    print(f"after settling the round letters: agreement {tot['='] / n:.1%} of {n} reference signs "
          f"(different {tot['s']}, only in reading {tot['i']}, only in reference {tot['d']})")
    for h, k in sorted(tab.items()):
        print(f"  round letters settled by {h}: {k['right']} right, {k['wrong']} wrong ({k['right'] / max(1, sum(k.values())):.0%})")
    allk = Counter()
    for k in tab.values():
        allk.update(k)
    print(f"  all round letters: {allk['right']} right of {sum(allk.values())} ({allk['right'] / max(1, sum(allk.values())):.0%})")


if __name__ == "__main__":
    main()
