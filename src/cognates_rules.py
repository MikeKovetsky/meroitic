"""Do Meroitic words fit their Nubian-family equivalents under Rilly's sound correspondences?

src/cognates.py compared forms by raw letter similarity and found no signal (p = 0.12). Cognates
follow regular sound correspondences, not surface likeness, so this engine scores a Northern East
Sudanic (NES) word by how well it fits the reflexes that the correspondences in
data/nes/sound_correspondences.tsv ("T<n>" = its n-th data row) predict for a Meroitic word.

1. pattern(form) reads a Meroitic word, standard or corpus spelling, as consonant and vowel slots.
   The inherent /a/ of a bare consonant sign gets no slot (Rilly's table pairs it with every NES
   vowel), initial y before e/i is a dummy, e may stand for no vowel. Each consonant slot gets the
   NES reflexes the rules allow, each with a weight, its conditions and the rows behind it.
2. segments(form, dataset, lang) turns an NES form into plain segments: tone, length and stress
   marks dropped; GLD and IDS IPA, ASJPcode and Wiktionary's Old Nubian (Coptic) transliteration
   mapped onto one alphabet of 5 vowels and 21 consonants.
3. align() aligns the two by dynamic programming. A regular correspondence earns its weight (up to
   1), a near sound with no rule NEAR, an irregular consonant SUB; a Meroitic consonant with no
   counterpart costs DEL unless a rule lets it vanish, an extra NES consonant INS (nothing for a
   nasal before a consonant: Meroitic does not write it, and T59 gives prenasalised and plain
   consonants one reflex). Vowels weigh little, since the script hardly writes them. The score is
   the total over the number of Meroitic consonants.

validate() repeats the cognates.py shuffle test with this scorer and with raw similarity on the same
words, lists and variants, and adds precision at the top.

  python3 -I src/cognates_rules.py [shuffles]
"""
import csv, functools, json, random, re, sys, unicodedata
from collections import namedtuple
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import cognates  # noqa: E402  raw similarity, gloss keys, the circular list

NUBIAN = {"old_nubian", "nobiin", "kenzi", "dongolawi", "midob", "birgid", "hill_nubian"}
NAMES = {"proper noun", "letter", "symbol"}            # Wiktionary rows that are not words to compare
SKIP_CATEGORIES = {"deity", "place", "people"}         # as in cognates.py

# Egyptian, Demotic and Greek loans in the gold lexicon (from its evidence notes, or named in the brief)
LOANS = {
    "ant": "Egyptian hm-ntr 'prophet' (gold note)",
    "apote": "Egyptian wpwtj 'messenger' (gold note)",
    "pelmos": "Egyptian p3-mr-msa 'the general' (gold note)",
    "peseto": "named as a loan in the brief",
    "ssor": "Egyptian sš 'scribe' (gold note)",
    "perite": "Egyptian, Coptic prit 'agent' (gold note)",
    "nbr": "Egyptian nbw 'gold' (gold note)",
    "tewiseti": "Demotic 'adoration' (gold note); the brief's tewisti",
    "kisri": "Greek Kaisar (gold note)",
    "aroẖe-": "Lipiński compares Demotic hrh 'watch over' (gold note)",
}
# Gold words the correspondences were built from: Rilly 2003's 17 series (pp. 301-306) and the words
# cited as examples in the prose rules. Scoring them with those rules is partly circular.
RULE_WORDS = {"abr", "are-", "ato", "dime", "dm-", "ḫlbi", "ḫre", "kdi", "ked", "l-", "lẖ", "mte", "pwrite",
              "st", "tre-", "wle", "yer",                           # the 17 series
              "wide", "abore", "qore", "nob", "ms"}                 # T73, T78, T80, T82

SUB, NEAR, DEL, INS, INS_GLIDE, VSUB = -1.0, 0.3, -0.8, -0.6, -0.3, -0.1
POS_FACTOR = 0.7       # a rule seen in another position of the word still counts, at this share
NEG = float("-inf")

# meroitic, nes, weight, position (I/M/F, "" any), language groups ("" any), TSV rows, condition
RULES = [
    ("b", "b", 1.0, "", "", (18, 19), None),
    ("b", "f", 0.8, "", "nyima", (19,), None),
    ("b", "g", 0.9, "", "", (64, 71, 73, 79), "rounded"),        # *g next to o/u > b
    ("p", "b", 1.0, "", "", (58,), None),                         # p is a spelling of /b/
    ("p", "f", 0.8, "", "nyima", (19, 58), None),
    ("p", "g", 0.9, "", "", (58, 64, 73), "rounded"),
    ("m", "m", 1.0, "", "", (38, 39), None),
    ("n", "n", 1.0, "", "", (73,), None),                         # nob ~ *nogu
    ("t", "t", 1.0, "", "", (47, 49, 50, 60, 66), None),
    ("t", "d", 1.0, "M", "", (49,), None),
    ("t", "s", 0.8, "MF", "", (48, 51), None),
    ("d", "t", 1.0, "I", "", (20,), None),
    ("d", "d", 1.0, "", "", (21, 22, 57), None),
    ("d", "n", 0.8, "I", "nara", (21,), None),
    ("d", "r", 1.0, "", "", (23, 78, 81), None),                  # wide ~ wer-i; *r > d initially
    ("l", "d", 1.0, "I", "", (34, 35, 55, 61, 65), None),         # lambdacism
    ("l", "n", 0.8, "I", "nara", (34,), None),
    ("l", "r", 0.9, "F", "", (36,), None),
    ("l", "l", 1.0, "", "", (37, 69), None),
    ("r", "r", 1.0, "", "", (41, 42, 43, 44, 45), None),
    ("r", "l", 0.9, "", "nyima", (42,), None),
    ("s", "s", 1.0, "", "", (46, 67), None),
    ("s", "ʃ", 1.0, "", "", (82,), None),                          # ms ~ mašal
    ("s", "t", 0.7, "F", "taman", (51,), None),
    ("k", "k", 1.0, "", "", (32, 33, 63), None),
    ("k", "ŋ", 0.9, "I", "nubian", (33,), None),                   # *ᵑk > Proto-Nubian *ŋ
    ("k", "t", 0.8, "I", "nyima", (33, 63, 75), None),             # Nyima dental t
    ("k", "d", 0.6, "", "nyima", (75,), None),
    ("ḫ", "g", 1.0, "", "", (26, 27, 28, 54, 56, 62), None),       # *g > ḫ, ẖ
    ("ḫ", "k", 0.7, "I", "nyima", (26,), None),
    ("ḫ", "t", 0.7, "", "nyima", (26, 75), None),
    ("ḫ", "d", 0.6, "", "nyima", (75,), None),
    ("ḫ", "h", 0.9, "", "nara", (28,), None),
    ("ḫ", "ŋ", 0.9, "M", "nyima", (28,), None),
    ("ḫ", "ŋ", 0.8, "F", "taman nyima", (76,), None),             # objective -xe = /ŋ/
    ("ḫ", "j", 0.8, "", "nubian", (74,), "front"),                # *g next to i/e > Proto-Nubian *ɟ
    ("w", "w", 1.0, "", "", (53, 69), None),
    ("w", "g", 0.8, "I", "nyima", (53,), None),
    ("w", "g", 0.7, "F", "", (72,), None),                        # accusative -w < *g + vowel
]
RULES += [("ẖ",) + r[1:] for r in RULES if r[0] == "ḫ"]          # ẖ (xʷ) shares ḫ's reflexes (T28, T54)
# one Meroitic consonant for two NES segments
TWO = {("t", "st"): (1.0, (48,)), ("ḫ", "gw"): (0.9, (28,)), ("ẖ", "gw"): (1.0, (28,)),
       ("ḫ", "kw"): (0.6, ()), ("ẖ", "kw"): (0.7, ()), ("q", "kw"): (0.6, ()), ("q", "gw"): (0.6, ())}
# a Meroitic consonant that a rule lets vanish: weight, position, groups, rows, condition
DROPS = {"m": (0.5, "F", "", (40,), None), "d": (0.4, "F", "nyima", (22,), None),
         "r": (0.4, "F", "taman", (45,), None), "q": (0.9, "I", "", (80,), "before_u")}
GLIDE_DROP = {"w": -0.3, "y": -0.2}
# near sounds: same class, no rule (worth NEAR, not SUB)
NEAR_SET = {"b": "pbfwm", "p": "pbfwm", "m": "mbn", "n": "nmŋɲ", "t": "tdsʃc", "d": "dtrln", "l": "lrdn",
            "r": "rld", "s": "sʃzcjt", "k": "kgŋhc", "ḫ": "hgkŋ", "ẖ": "hgkŋw", "q": "kgwŋ", "w": "wbfpg",
            "y": "yjɲ"}
SAME = {"p": "p", "y": "y"}      # same sound with no row behind it
# vowel slots: A initial a, Y initial e/i (ye-, yi-), e / i / o the vowel signs
VOWELS = {"A": {"a": (0.25, (1,)), "e": (0.25, (2, 17)), "u": (0.2, (1,)), "o": (0.1, ())},
          "Y": {"e": (0.25, (24,)), "i": (0.2, (24,))},
          "e": {"e": (0.2, ()), "o": (0.2, (25,)), "a": (0.1, (25,)), "i": (0.1, ())},
          "i": {"i": (0.25, (29, 30, 31)), "e": (0.2, (29, 31))},
          "o": {"u": (0.25, ()), "o": (0.25, ()), "i": (0.15, (52,)), "a": (0.1, (52,))}}
VDROP = {"A": -0.1, "Y": -0.1, "e": 0.0, "i": -0.05, "o": -0.1}

NES_V = "aeiou"
NES_C = "pbfmwtdnszʃcjrlykgŋɲh"
NASALS = "mnŋɲ"
SEG = {**{c: c for c in NES_V + NES_C},
       "ɛ": "e", "ə": "e", "ǝ": "e", "ɪ": "i", "ı": "i", "ɨ": "i", "ɔ": "o", "ɒ": "o", "ω": "o", "ʊ": "u", "ʉ": "u",
       "ʌ": "a", "ɑ": "a", "æ": "a",
       "ɓ": "b", "β": "b", "v": "b", "ф": "f", "ʋ": "w", "ʷ": "w", "ʈ": "t", "θ": "t", "ɖ": "d", "ɗ": "d", "ð": "d",
       "ɕ": "ʃ", "ʒ": "j", "ʓ": "j", "ɟ": "j", "ȷ": "j", "ɽ": "r", "ɾ": "r", "ɼ": "r", "ʸ": "y", "q": "k", "ɡ": "g",
       "x": "h", "ɣ": "h", "χ": "h", "ħ": "h", "ʕ": "h"}
# ASJPcode capitals and digits (E open e, 3 high central vowel, N ŋ, 5 ɲ, S ʃ, Z ʒ, C tʃ, T palatal stop,
# L other lateral, X uvular fricative, G uvular voiced stop, 7 glottal stop, 8 dental fricative, 4 dental nasal)
ASJP = str.maketrans({"E": "e", "3": "ə", "N": "ŋ", "5": "ɲ", "S": "ʃ", "Z": "ʒ", "C": "c", "T": "c", "L": "l",
                      "X": "x", "G": "g", "7": "", "8": "θ", "4": "n", "~": "", "*": "", '"': "", "$": ""})
CARON = {"c": "c", "s": "ʃ", "z": "j", "j": "j"}                # č š ž ǰ ǯ

Row = namedtuple("Row", "lang form gloss keys dataset variety variants")   # variants: ((raw, segs), ...)
Slot = namedtuple("Slot", "kind sym pos")


def group(lang):
    return "nubian" if lang in NUBIAN else lang


# ---------- the NES side ----------

def variants(form, dataset=""):
    """The spellings to try for one NES cell: each ~ / , alternative, brace spelling and bracket reading,
    whole and, for a form with morpheme breaks (- = space), its first and its longest piece."""
    s = unicodedata.normalize("NFC", form)
    if dataset == "asjp":
        s = re.sub(r'[~*"$]', "", s)                 # ASJPcode modifiers, not variant breaks
    s = re.sub(r"\[[^\]]*\]", " ", s)               # GLD source tags such as [Wb.]
    alts = re.findall(r"\{([^}]*)\}", s)
    s = re.sub(r"\{[^}]*\}", " ", s)
    pieces = []
    for chunk in [s] + alts:
        for t in (re.sub(r"\([^)]*\)", " ", chunk), re.sub(r"[()]", "", chunk)):
            pieces += re.split(r"\s*[~/,;]\s*", t)
    out = []
    for p in pieces:
        parts = [x for x in re.split(r"[-=\s.#?{}]+", p) if x]
        if not parts:
            continue
        for c in ["".join(parts)] + ([parts[0], max(parts, key=len)] if len(parts) > 1 else []):
            if c not in out:
                out.append(c)
    return out


def segments(v, dataset="", lang=""):
    """One spelling as a tuple of plain segments, geminates and long vowels collapsed."""
    if dataset == "asjp":
        v = v.translate(ASJP)
    v = v.lower()
    if dataset == "wiktionary":
        if lang == "old_nubian":                     # Coptic ⲟⲩ, ⲉⲓ
            v = re.sub(r"ou(?=[aeiouēō])", "w", v).replace("ou", "u").replace("ei", "i")
        v = v.replace("sh", "ʃ")
    out = []
    for ch in unicodedata.normalize("NFD", v):
        if unicodedata.combining(ch):
            if out and ch == "̌":
                out[-1] = CARON.get(out[-1], out[-1])
            elif out and ch == "̧" and out[-1] == "c":     # Old Nubian ⳝ, Nobiin dç
                out[-1] = "j"
            elif out and ch == "̃" and out[-1] == "n":
                out[-1] = "ɲ"
            continue
        seg = SEG.get(ch)
        if seg:
            out.append(seg)
    return tuple(s for i, s in enumerate(out) if i == 0 or s != out[i - 1])


def load_nes(proto=False):
    """Rows of the independent lists (proto_nes.tsv only when proto=True, and then alone)."""
    rows = []
    for p in sorted((ROOT / "data/nes").glob("*.tsv")):
        if "meroitic" in p.stem or p.stem.startswith("sound_") or (p.stem in cognates.CIRCULAR) != proto:
            continue
        with open(p) as f:
            for r in csv.DictReader(f, delimiter="\t"):
                if not (r.get("form") and r.get("gloss")) or (r.get("dataset") == "wiktionary" and r.get("pos") in NAMES):
                    continue
                vs = tuple((v, segments(v, r.get("dataset", ""), p.stem)) for v in variants(r["form"], r.get("dataset", "")))
                vs = tuple((v, s) for v, s in vs if s)
                if vs:
                    rows.append(Row(p.stem, r["form"], r["gloss"], frozenset(cognates.keys(r["gloss"])),
                                    r.get("dataset", ""), r.get("variety") or r.get("proto_language", ""), vs))
    return rows


# ---------- the Meroitic side ----------

def mer_letters(form):
    """Corpus spelling (x X S N E h) and standard transliteration onto one letter string."""
    f = unicodedata.normalize("NFC", form)
    for a, b in (("X", "ẖ"), ("x", "ḫ"), ("H", "ḫ"), ("h", "ḫ"), ("N", "ne"), ("E", "o"), ("S", "s")):
        f = f.replace(a, b)
    return re.sub(r"[^abdeiklmnopqrstwyḫẖ]", "", f.lower())


@functools.lru_cache(maxsize=None)
def pattern(form):
    """Meroitic form -> slots. C slots carry the consonant and its position (I, M, F; IF for a lone
    initial one); V slots: A initial a, Y initial e/i, e i o the vowel signs."""
    f, slots, i = mer_letters(form), [], 0
    if f[:2] in ("ye", "yi"):
        slots, i = [Slot("V", "Y", "")], 2
    elif f[:1] in ("e", "i"):
        slots, i = [Slot("V", "Y", "")], 1
    elif f[:1] in ("a", "o"):
        slots, i = [Slot("V", "A" if f[0] == "a" else "o", "")], 1
    for ch in f[i:]:
        if ch in "eio":
            slots.append(Slot("V", ch, ""))
        elif ch != "a":                              # a after a consonant: the inherent vowel, no slot
            slots.append(Slot("C", ch, ""))
    cons = [k for k, s in enumerate(slots) if s.kind == "C"]
    for n, k in enumerate(cons):
        pos = ("I" if n == 0 and k == 0 else "") + ("F" if n == len(cons) - 1 else "")
        slots[k] = slots[k]._replace(pos=pos or "M")
    return tuple(slots)


def label(mer, nes, rows):
    return f"{mer}~{nes or 'Ø'} ({','.join('T%d' % r for r in rows)})" if rows else f"{mer}~{nes} (same sound)"


@functools.lru_cache(maxsize=None)
def reflexes(mer, pos, grp):
    """{nes segment: (weight, label, condition)} for one Meroitic consonant in one position and group."""
    out = {}
    for m, n, w, p, groups, rows, cond in RULES:
        if m != mer or (groups and grp not in groups.split()):
            continue
        w = w if not p or any(c in p for c in pos) else w * POS_FACTOR
        if n not in out or w > out[n][0]:
            out[n] = (w, label(m, n, rows), cond)
    if mer in SAME and mer not in out:
        out[mer] = (0.8, label(mer, mer, ()), None)
    return out


def expected(form, lang="dongolawi"):
    """The reflex pattern of a Meroitic form for one NES language, readable: one group per slot."""
    grp, out = group(lang), []
    for s in pattern(form):
        if s.kind == "V":
            out.append("(" + "|".join(VOWELS[s.sym]) + ")")
            continue
        refl = sorted(reflexes(s.sym, s.pos, grp).items(), key=lambda x: -x[1][0])
        alts = [n + ("°" if c else "") for n, (w, _, c) in refl]
        alts += [m[1] for m in TWO if m[0] == s.sym]
        d = DROPS.get(s.sym)
        if d and any(c in d[1] for c in s.pos) and (not d[2] or grp in d[2].split()):
            alts.append("Ø°" if d[4] else "Ø")
        out.append("|".join(alts) or "?")
    return " ".join(out)


# ---------- the alignment ----------

def _match(slot, segs, j, grp):
    """Weight and label for slot against NES segment j, or None when they cannot pair."""
    seg = segs[j]
    if slot.kind == "V":
        if seg not in NES_V:
            return None
        w, rows = VOWELS[slot.sym].get(seg, (VSUB, ()))
        return w, (f"{slot.sym}~{seg}" if w > 0 else "")
    if seg in NES_V:                                 # a glide may answer a vowel
        if (slot.sym, seg) in (("w", "u"), ("w", "o"), ("y", "i"), ("y", "e")):
            return 0.5, f"{slot.sym}~{seg} (glide)"
        return None
    hit = reflexes(slot.sym, slot.pos, grp).get(seg)
    if hit:
        w, lab, cond = hit
        near = {segs[k] for k in (j - 1, j + 1) if 0 <= k < len(segs)}
        if cond is None or (cond == "rounded" and near & {"o", "u"}) or (cond == "front" and near & {"i", "e"}):
            return w, lab
    if seg in NEAR_SET.get(slot.sym, ""):
        return NEAR, f"{slot.sym}~{seg} (near, no rule)"
    return SUB, f"{slot.sym}~{seg} (irregular)"


def _drop(slot, segs, j, grp):
    """Weight and label for slot left without an NES counterpart; j is the next NES segment."""
    if slot.kind == "V":
        return VDROP[slot.sym], ""
    d = DROPS.get(slot.sym)
    if d:
        w, p, groups, rows, cond = d
        if any(c in p for c in slot.pos) and (not groups or grp in groups.split()) and \
                (cond != "before_u" or (j < len(segs) and segs[j] in "uo")):
            return w, label(slot.sym, "", rows)
    if slot.sym in GLIDE_DROP and "I" not in slot.pos:
        return GLIDE_DROP[slot.sym], f"{slot.sym}~Ø (glide)"
    return DEL, f"{slot.sym}~Ø (missing)"


def _insert(segs, j):
    seg = segs[j]
    if seg in NES_V:
        return 0.0, ""
    if seg in NASALS and j + 1 < len(segs) and segs[j + 1] in NES_C and segs[j + 1] not in NASALS:
        return 0.0, f"+{seg} unwritten nasal (T59)"
    return (INS_GLIDE if seg in "ywh" else INS), f"+{seg} extra"


def align(form, segs, lang, trace=False):
    """Best alignment of a Meroitic form with one NES segment tuple: score per Meroitic consonant,
    and with trace=True the list of correspondences used."""
    slots, grp, m = pattern(form), group(lang), len(segs)
    n = len(slots)
    ins = [_insert(segs, j) for j in range(m)]
    D = [[NEG] * (m + 1) for _ in range(n + 1)]
    B = [[None] * (m + 1) for _ in range(n + 1)]
    D[0][0] = 0.0
    for j in range(1, m + 1):
        D[0][j], B[0][j] = D[0][j - 1] + ins[j - 1][0], ("ins", ins[j - 1][1])
    for i in range(1, n + 1):
        sl = slots[i - 1]
        for j in range(m + 1):
            w, lab = _drop(sl, segs, j, grp)
            best, bp = D[i - 1][j] + w, ("del", lab)
            if j:
                hit = _match(sl, segs, j - 1, grp)
                if hit and D[i - 1][j - 1] + hit[0] > best:
                    best, bp = D[i - 1][j - 1] + hit[0], ("sub", hit[1])
                if D[i][j - 1] + ins[j - 1][0] > best:
                    best, bp = D[i][j - 1] + ins[j - 1][0], ("ins", ins[j - 1][1])
            if j >= 2 and sl.kind == "C" and (sl.sym, segs[j - 2] + segs[j - 1]) in TWO:
                w2, rows = TWO[(sl.sym, segs[j - 2] + segs[j - 1])]
                if D[i - 1][j - 2] + w2 > best:
                    best, bp = D[i - 1][j - 2] + w2, ("two", label(sl.sym, segs[j - 2] + segs[j - 1], rows))
            D[i][j], B[i][j] = best, bp
    score = D[n][m] / max(1, sum(s.kind == "C" for s in slots))
    if not trace:
        return score
    used, i, j = [], n, m
    while i or j:
        kind, lab = B[i][j]
        if lab:
            used.append(lab)
        i, j = {"ins": (i, j - 1), "del": (i - 1, j), "sub": (i - 1, j - 1), "two": (i - 1, j - 2)}[kind]
    return score, used[::-1]


@functools.lru_cache(maxsize=None)
def _score(form, segs, lang):
    return align(form, segs, lang)


def rule_score(form, row):
    return max(_score(form, s, row.lang) for _, s in row.variants)


def raw_score(form, row):
    return max(cognates.sim(form, v) for v, _ in row.variants)


def explain(form, row):
    """Best variant of a row for a form: (score, variant, segments, correspondences used)."""
    best = max(row.variants, key=lambda vs: _score(form, vs[1], row.lang))
    score, used = align(form, best[1], row.lang, trace=True)
    return score, best[0], best[1], used


# ---------- the validation ----------

def gold_words():
    """(form, gloss keys, gloss) for the gold words compared, and the words left out with the reason."""
    words, left = [], []
    for g in json.load(open(ROOT / "data/gold_lexicon.json")):
        if g.get("category") in SKIP_CATEGORIES:
            continue
        if g["form"] in LOANS:
            left.append((g["form"], LOANS[g["form"]]))
        elif g.get("confidence") == "debated":
            left.append((g["form"], "meaning debated in the gold lexicon"))
        elif cognates.keys(g["gloss"]):
            words.append((g["form"], frozenset(cognates.keys(g["gloss"])), g["gloss"]))
    return words, left


def matrix(words, rows, scorer):
    return {f: [scorer(f, r) for r in rows] for f, _, _ in words}


def shuffle_test(words, rows, S, sims=2000, seed=3):
    """cognates.py's design: mean over words of the best score among same-meaning NES rows, against
    `sims` shuffles of the Meroitic meanings (p counts the real pairing as one arrangement)."""
    match = [[i for i, r in enumerate(rows) if r.keys & k] for _, k, _ in words]
    best = [[max(S[f][i] for i in mt) if mt else None for mt in match] for f, _, _ in words]

    def stat(perm):
        vals = [best[a][b] for a, b in enumerate(perm) if match[b]]
        return sum(vals) / max(1, len(vals))
    real = stat(range(len(words)))
    rng, perm, ge = random.Random(seed), list(range(len(words))), 0
    for _ in range(sims):
        rng.shuffle(perm)
        ge += stat(perm) >= real - 1e-9
    return {"n": sum(1 for m in match if m), "of": len(words), "stat": real, "ge": ge, "sims": sims,
            "p": (ge + 1) / (sims + 1), "best": best, "match": match}


def top_test(words, rows, S, sims=2000, seed=3, k=1):
    """Precision at the top: for each word with a same-meaning row, the share of its top-k rows (over
    every row and meaning; ties at the cut-off shared out) that carry its meaning; chance level and a
    shuffle p as above."""
    match = [{i for i, r in enumerate(rows) if r.keys & kk} for _, kk, _ in words]
    prec = []
    for f, _, _ in words:
        order = sorted(range(len(rows)), key=lambda i: -S[f][i])
        cut = S[f][order[k - 1]]
        sure = [i for i in order if S[f][i] > cut + 1e-9]
        tied = [i for i in order if abs(S[f][i] - cut) <= 1e-9]
        slots = k - len(sure)
        prec.append([(sum(i in mt for i in sure) + slots * sum(i in mt for i in tied) / len(tied)) / k
                     for mt in match])

    def stat(perm):
        vals = [prec[a][b] for a, b in enumerate(perm) if match[b]]
        return sum(vals) / max(1, len(vals))
    real = stat(range(len(words)))
    chance = [len(match[b]) / len(rows) for b in range(len(words)) if match[b]]
    rng, perm, ge = random.Random(seed), list(range(len(words))), 0
    for _ in range(sims):
        rng.shuffle(perm)
        ge += stat(perm) >= real - 1e-9
    return {"k": k, "prec": real, "chance": sum(chance) / len(chance), "ge": ge, "p": (ge + 1) / (sims + 1),
            "hits": [words[a][0] for a in range(len(words)) if match[a] and prec[a][a] > 0]}


def ranks(words, rows, S):
    """For each word with a same-meaning row: the rank of its best same-meaning row among all rows
    (ties counted in its favour)."""
    out = []
    for f, k, _ in words:
        mt = [i for i, r in enumerate(rows) if r.keys & k]
        if mt:
            b = max(S[f][i] for i in mt)
            out.append(1 + sum(s > b + 1e-9 for s in S[f]))
    return sorted(out)


def grid(sims=2000):
    """Robustness, not tuning (the decision is taken with the defaults): p on all and on held-out words
    under other cost settings, every setting reported."""
    rows, (words, _) = load_nes(), gold_words()
    held = [w for w in words if w[0] not in RULE_WORDS]
    g, base = globals(), {k: globals()[k] for k in ("NEAR", "INS", "DEL", "SUB", "POS_FACTOR")}
    out = []
    for s in ({}, {"NEAR": 0.0}, {"SUB": -0.5}, {"INS": -0.3}, {"DEL": -0.4, "INS": -0.3}, {"POS_FACTOR": 1.0}):
        g.update(base)
        g.update(s)
        _score.cache_clear()
        reflexes.cache_clear()
        S = matrix(words, rows, rule_score)
        out.append((s or "defaults", shuffle_test(words, rows, S, sims)["p"], shuffle_test(held, rows, S, sims)["p"]))
    g.update(base)
    _score.cache_clear()
    reflexes.cache_clear()
    return out


def proto_control(rows_proto, scorer):
    """Labelled circular check: Rilly's own Meroitic ~ proto-NES pairs (proto_nes.tsv's comparandum
    column), the rank of his proto form among all 330 proto rows for that Meroitic word."""
    gold = {g["form"].strip("-"): g["form"] for g in json.load(open(ROOT / "data/gold_lexicon.json"))}
    out = []
    with open(ROOT / "data/nes/proto_nes.tsv") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            c = re.sub(r"^(cf\.\s*)?(Mer\.\s*)?\*?", "", r.get("meroitic_comparandum", ""))
            head = re.split(r"[\s\[(/]", c, maxsplit=1)[0].strip("-")
            if head not in gold:
                continue
            mer = gold[head]
            target = [i for i, x in enumerate(rows_proto) if x.form == r["form"] and x.gloss == r["gloss"]]
            if not target:
                continue
            scores = [scorer(mer, x) for x in rows_proto]
            t = scores[target[0]]
            out.append((mer, r["form"], 1 + sum(s > t + 1e-9 for s in scores)))
    return out


# ---------- the report ----------

def earned(res, alpha=0.05):
    """Set before any run: lists only when the rule scorer beats the shuffles on all gold words AND on
    the held-out words that the correspondences were not built from."""
    return res["rule"]["all"]["p"] < alpha and res["rule"]["held"]["p"] < alpha


def run(sims=2000, top=5, unknown=None):
    rows = load_nes()
    words, left = gold_words()
    held = [w for w in words if w[0] not in RULE_WORDS]
    built = [w for w in words if w[0] in RULE_WORDS]
    R, W = matrix(words, rows, rule_score), matrix(words, rows, raw_score)
    res = {"rows": rows, "words": words, "held": held, "left": left, "R": R, "W": W}
    for name, S in (("rule", R), ("raw", W)):
        res[name] = {"all": shuffle_test(words, rows, S, sims), "held": shuffle_test(held, rows, S, sims),
                     "built": shuffle_test(built, rows, S, sims),
                     "top1": top_test(words, rows, S, sims), "top10": top_test(words, rows, S, sims, k=10),
                     "top1_held": top_test(held, rows, S, sims)}
    res["earned"], res["lists"] = earned(res), {}
    for u in (unknown or []) if res["earned"] else []:
        R[u] = [rule_score(u, r) for r in rows]
        order = sorted(range(len(rows)), key=lambda i: -R[u][i])
        seen, out = set(), []
        for i in order:
            sc, v, segs, used = explain(u, rows[i])
            key = (rows[i].lang, segs, rows[i].gloss)
            if key in seen:
                continue
            seen.add(key)
            out.append((sc, rows[i], v, used))
            if len(out) == top:
                break
        res["lists"][u] = out
    return res


UNKNOWN = ["temey", "tros", "tlt", "teketi", "kroro", "aribet", "ateqi", "Sklte", "mlekeyos", "tmNteleb", "Smlo",
           "brtoye", "kemxr", "kiN", "mlolo", "yiroXe", "womnitX", "SSimete"]


def main(sims=2000):
    res = run(sims, unknown=UNKNOWN)
    rows, words = res["rows"], res["words"]
    print(f"NES rows compared: {len(rows)} (independent lists; Wiktionary names and letters left out)")
    print(f"gold words left out: {', '.join(f'{f} ({why})' for f, why in res['left'])}")
    print(f"held-out words (not in Rilly's series or rule examples): {len(res['held'])} of {len(words)}")
    for name in ("rule", "raw"):
        for lab, x in (("all words", "all"), ("held-out", "held"), ("rule words only", "built")):
            a = res[name][x]
            print(f"[{name}] {lab}: {a['n']} of {a['of']} with a same-meaning NES word; mean best {a['stat']:.3f}; "
                  f"shuffled >= real in {a['ge']}/{a['sims']} (p={a['p']:.4f})")
        for lab, x in (("top-1", "top1"), ("top-10", "top10"), ("top-1 held-out", "top1_held")):
            t = res[name][x]
            print(f"[{name}] precision at {lab}: {t['prec']:.4f} (chance {t['chance']:.4f}); shuffle p={t['p']:.4f}; "
                  f"words with any same-meaning row there: {', '.join(t['hits']) or 'none'}")
        for lab, ws in (("all", words), ("held-out", res["held"])):
            rk = ranks(ws, rows, res["R" if name == "rule" else "W"])
            print(f"[{name}] rank of the best same-meaning row, {lab}: median {rk[len(rk) // 2]}, "
                  f"best {rk[0]}, in top 10 for {sum(r <= 10 for r in rk)} of {len(rk)} (of {len(rows)} rows)")
        print()
    for f, _, g in words:
        i = max(range(len(rows)), key=lambda i: res["R"][f][i])
        ties = sum(abs(s - res["R"][f][i]) <= 1e-9 for s in res["R"][f])
        print(f"  top-1 {f:9} '{g[:22]}' -> {rows[i].lang}:{rows[i].form} '{rows[i].gloss[:30]}' "
              f"{res['R'][f][i]:.2f} ({ties} tied)")
    a = res["rule"]["all"]
    print("\nbest same-meaning NES word per gold word (rule score):")
    for wi, (f, k, g) in sorted(enumerate(words), key=lambda x: -(a["best"][x[0]][x[0]] or -9)):
        if a["best"][wi][wi] is None:
            continue
        i = max(a["match"][wi], key=lambda i: res["R"][f][i])
        sc, v, segs, used = explain(f, rows[i])
        raw = max(res["W"][f][i] for i in a["match"][wi])
        print(f"  {sc:6.2f} raw {raw:.2f} {f:10} '{g}' ~ {rows[i].lang}:{v} '{rows[i].gloss[:40]}' | {'; '.join(used)}")
    proto = load_nes(proto=True)
    ctl = proto_control(proto, rule_score)
    ctl_raw = proto_control(proto, raw_score)
    print(f"\nproto control (circular, labelled): {len(ctl)} of Rilly's pairs; rank 1 for "
          f"{sum(r == 1 for *_, r in ctl)} (rule) vs {sum(r == 1 for *_, r in ctl_raw)} (raw); top 5 for "
          f"{sum(r <= 5 for *_, r in ctl)} vs {sum(r <= 5 for *_, r in ctl_raw)}, of {len(proto)} proto rows")
    for (m, p, r), (_, _, r2) in zip(ctl, ctl_raw):
        print(f"  {m:8} ~ {p:24} rank {r} (raw {r2})")
    print("\nrobustness (other cost settings; p all words / p held-out):")
    for s, pa, ph in grid(sims):
        print(f"  {s}: {pa:.4f} / {ph:.4f}")
    if not res["earned"]:
        print("\nno signal by the preset test (p < 0.05 on all gold words and on the held-out words): "
              "candidate lists not produced")
        return
    print("\ncandidate lists (hypotheses):")
    for u, out in res["lists"].items():
        print(f"  {u}: {expected(u)}")
        for sc, r, v, used in out:
            print(f"    {sc:5.2f} {r.lang}:{v} '{r.gloss[:50]}' | {'; '.join(used)}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2000)
