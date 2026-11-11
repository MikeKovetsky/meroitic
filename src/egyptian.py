"""Egyptian words behind Meroitic ones: a search by sound alone, tested on the known loans.

  python3 -I src/egyptian.py first            the two word lists as the search sees them, and the answer key
  python3 -I src/egyptian.py find <word>      the pool entries whose letters equal those of an Egyptian word
  python3 -I src/egyptian.py build            the test, the comparison words and the search; writes the local
                                              result files and the public list of candidates
  python3 -I src/egyptian.py check            the checkers' pack: the best matches and unmarked decoys
  python3 -I src/egyptian.py merge            the checkers' answers against the key of decoys
  python3 -I src/egyptian.py vowels           the same test and search with the vowels compared too, on the
                                              Coptic entries (Demotic writes none); its own result files and list
  python3 -I src/egyptian.py check vowels     the pack of its best matches that the first pack did not hold
  python3 -I src/egyptian.py merge vowels     the checkers' answers to that pack

The question (NEXT_STEPS.md, E 17): can a mechanical search find the Egyptian word behind a Meroitic title or
noun? Mechanical means that the scorer has read no literature: it knows the letters and nothing else, so its hits
on words whose source is known measure what its hits on unknown words are worth (data/discovery/egyptian.md).

1. The pools. Every lemma of the TLA's Demotic sentences (data/sources/egyptian/demotic/train.jsonl) with the
   kinds of word its tokens are tagged as, and every entry of the Comprehensive Coptic Lexicon
   (data/sources/egyptian/coptic/), Greek loans in Coptic included. Each form is reduced to its consonants in one
   alphabet (EGY): a Demotic lemma with and without its bracketed and dotted endings, a Coptic entry in each
   dialect form.
2. The model. One Egyptian word becomes a Meroitic one letter by letter: a letter is kept, changed or dropped,
   and a Meroitic letter may be added. The chances start from a neutral table (a consonant most often stays what
   it is, the weak ones drop easily) and are re-counted from the aligned known loans. An Egyptian word may come
   with its article (p or t) in front; how often is counted from the same loans.
3. The test. Each known loan whose source stands in the pools is searched with a model trained on the others,
   and the place of the true source among all candidates of its kind is reported.
4. The comparison. A best match counts only as far as it beats the best matches of made-up words of the same
   length, built letter by letter as letters follow one another in the lexicon's headwords. The Meroitic words
   with an accepted meaning that nobody derives from Egyptian go through the same search, to see that the
   made-up words are a fair yardstick.
5. The check. The pieces whose best match beats the bar go to two checkers, mixed with unmarked decoys.
6. With vowels. The build compares consonants only. `vowels` runs the test, the comparison and the search again
   on the Coptic entries with the written vowels in the letter strings (Meroitic e, i, o; Coptic vowels in four
   classes), and keeps the consonant figures of the same pool beside them.

Both word lists, the answer key (drawn from Rilly's lexicon) and the result files are local
(data/sources/egyptian/). The public files are the page and the list of candidates.
"""
import collections, csv, json, math, random, re, sys, unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import lexique as L    # noqa: E402
import coverage as C   # noqa: E402

HERE = ROOT / "data/sources/egyptian"                       # local only
COPTIC = HERE / "coptic/Comprehensive_Coptic_Lexicon-v1.2-2020.xml"
DEMOTIC = HERE / "demotic/train.jsonl"
KEY = HERE / "loans_both.jsonl"
SOURCES = HERE / "key_sources.json"                         # the pool entries that are each known loan's source
OUT = HERE / "out"
UNKNOWN = ROOT / "data/discovery/coverage_unknown.tsv"
PUBLIC = ROOT / "data/discovery/egyptian_candidates.tsv"

# The search's letters. Meroitic: its consonants, and 0 for a word that opens with a vowel (the signs se, ne, te
# and to are s, n and t). Egyptian: T ṯ, D ḏ (Coptic ϫ), S š, x ḫ (and Demotic h̭), X ẖ, h for h and ḥ, A for ꜣ, ꞽ,
# ꜥ and a vowel at the start of a Coptic word.
MER = "pbmnrltdkqsxXwy0"
EGY = "pbfmnrltdTDkqgsSxXhAyw"
GROUP = {"p": "P", "b": "P", "f": "P", "m": "M", "n": "N", "r": "R", "l": "R", "t": "T", "d": "T", "T": "T",
         "D": "T", "k": "K", "q": "K", "g": "K", "s": "S", "S": "S", "x": "X", "X": "X", "h": "H", "A": "A",
         "0": "A", "y": "Y", "w": "W", "a": "V", "e": "V", "i": "V", "o": "V"}
WEAK = "hAywaeio"             # letters that drop easily: laryngeals, glides and (in the vowel search) vowels
VOWELS_M = "eio"              # the Meroitic vowels written inside a word (a is written at the start only: 0)
VOWELS_E = "aeio"             # the Coptic vowels in four classes: ⲁ; ⲉ and ⲏ; ⲓ and ⲉⲓ; ⲟ, ⲱ, ⲟⲩ and ⲩ
VOWEL_OF = {"ⲁ": "a", "ⲉ": "e", "ⲏ": "e", "ⲓ": "i", "ⲟ": "o", "ⲱ": "o", "ⲩ": "o"}
SAME = {"A": "0"}             # the Meroitic letter that is "the same" as an Egyptian one, when it is not spelled alike
STRENGTH = 3.0                # how many counted cases the starting table is worth, per Egyptian letter
ARTICLES = ("", "p", "t")     # an Egyptian word alone, or with its article pꜣ or tꜣ in front
SHORTEST = 3                  # a Meroitic word with fewer letters is not searched: anything fits it
DEM = {"ꜣ": "A", "ꞽ": "A", "ꜥ": "A", "y": "y", "w": "w", "b": "b", "p": "p", "f": "f", "m": "m", "n": "n",
       "r": "r", "l": "l", "h": "h", "ḥ": "h", "ḫ": "x", "h̭": "x", "ẖ": "X", "s": "s", "z": "s", "š": "S",
       "q": "q", "k": "k", "g": "g", "t": "t", "ṱ": "t", "ṯ": "T", "d": "d", "ḏ": "D"}
COP = {"ⲡ": "p", "ⲃ": "b", "ϥ": "f", "ⲫ": "p", "ⲙ": "m", "ⲛ": "n", "ⲣ": "r", "ⲗ": "l", "ⲧ": "t", "ⲇ": "d",
       "ⲑ": "t", "ϯ": "t", "ϫ": "D", "ϭ": "g", "ⲕ": "k", "ⲅ": "g", "ⲭ": "k", "ⲝ": "ks", "ⲯ": "ps", "ⲥ": "s",
       "ⲍ": "s", "ϣ": "S", "ϩ": "h", "ϧ": "x", "ⳉ": "x"}
VOWELS = "ⲁⲉⲏⲓⲟⲩⲱ"
# the Demotic tags and the Coptic word classes -> the search's kinds of pool entry
TAG = {"TITL": "title", "DIVN": "god", "TOPN": "place", "PERSN": "person", "ROYLN": "person", "N": "noun",
       "V": "verb", "ADJ": "adjective", "Subst.": "noun", "Vb.": "verb", "Adj.": "adjective"}
NAMES = {"god", "place", "person"}
# the kind of a Meroitic word -> the pool entries of its kind, narrow and wide
SCOPE = {"title": ({"title"}, {"title", "noun"}), "epithet": ({"title"}, {"title", "noun", "adjective"}),
         "god name": ({"god"}, NAMES), "place name": ({"place"}, NAMES), "person name": ({"person"}, NAMES),
         "name": (NAMES, NAMES), "people name": (NAMES, NAMES),
         "noun": ({"noun"}, {"noun", "title"}), "kin term": ({"noun"}, {"noun", "title"}),
         "numeral or measure": ({"noun"}, {"noun", "title"}),
         "verb": ({"verb"}, {"verb"}), "benediction verb": ({"verb"}, {"verb"}),
         "adjective": ({"adjective"}, {"adjective", "noun"})}
# the vowel search: the Coptic entries a Meroitic word of each kind is searched among (names are not searched:
# the Coptic lexicon holds few)
VOWEL_SCOPE = {"title": {"noun"}, "epithet": {"noun", "adjective"}, "noun": {"noun"}, "kin term": {"noun"},
               "numeral or measure": {"noun"}, "verb": {"verb"}, "benediction verb": {"verb"},
               "adjective": {"adjective", "noun"}}
VOWEL_LONGEST = 12            # with vowels the letter strings are longer; this many letters or more go together
KEY_KIND = {"other": "noun"}  # the readers' kinds that the coverage map does not have
MADE_UP = 300                 # made-up words of each length that a best match is compared with
LONGEST = 8                   # words of this many letters or more are compared together
SEED = 17
BAR = 0.05                    # a best match beats the bar when at most this share of made-up words do as well
FDR = 0.2                     # the bar for many tries: at most this share of the pieces passing it are chance
# Rilly's Egyptian transliteration -> the TLA's, for finding a printed source word in the pools
RILLY = {"3": "ꜣ", "ʿ": "ꜥ", "ᶜ": "ꜥ", "ͨ": "ꜥ", "ʾ": "ꜣ", "ỉ": "ꞽ", "i": "ꞽ", "j": "y", "ś": "s", "ḳ": "q",
         "ṭ": "ṱ", "ı": "ꞽ"}


# ------------------------------------------------------------------------------------------------ letters

def meroitic(spelling, vowels=False):
    """The search's letters of a word in the corpus spelling: consonants, and 0 for a vowel at the start.
    With `vowels`, the written e, i and o stay where they stand (a is written at the start only)."""
    s = re.sub(r"[^a-zA-Z]", "", spelling)
    out = ["0"] if s[:1].lower() in tuple("aeio") else []
    for c in s:
        if c.lower() not in "aeio":
            out.append({"S": "s", "N": "n", "X": "X"}.get(c, c.lower()))
        elif vowels and c.lower() in VOWELS_M:
            out.append(c.lower())
    return "".join(c for c in out if c in MER + VOWELS_M)


def headword(word, vowels=False):
    """The search's letters of a word in Rilly's spelling, or "" when it has lost signs."""
    spellings = L.corpus_spellings(word)
    return meroitic(min(spellings), vowels) if spellings else ""


def consonants(word):
    """How many of a Meroitic letter string's letters are not vowels."""
    return sum(c not in VOWELS_M for c in word)


def demotic(lemma, endings=True):
    """A Demotic lemma in the search's letters, with its bracketed and dotted endings (.t, (.w)) or without."""
    s = unicodedata.normalize("NFC", lemma.lower())
    if not endings:
        s = re.sub(r"\.[^-=\s()]*", "", re.sub(r"\([^)]*\)", "", s))
    out = []
    for part in re.findall(r"h̭|.", s, re.S):
        if part in DEM:
            out.append(DEM[part])
        elif part in "aei" and not out:
            out.append("A")
    return "".join(out)


def coptic(form, vowels=False):
    """A Coptic form in the search's letters: ⲟⲩ and ⲉⲓ/ⲓ before a vowel are w and y, ⲩ after a vowel is w.
    With `vowels`, every other vowel is written as its class (VOWEL_OF; ⲟⲩ is o, ⲉⲓ is i), a doubled one once."""
    s = [c for c in unicodedata.normalize("NFD", form.lower()) if c in VOWELS or c in COP]
    out, i = [], 0
    while i < len(s):
        c, nxt, prev = s[i], "".join(s[i + 1:i + 2]), "".join(s[i - 1:i]) if i else ""
        if c in COP:
            out.append(COP[c])
            i += 1
            continue
        pair = c + nxt in ("ⲟⲩ", "ⲉⲓ")
        after = "".join(s[i + 2:i + 3]) if pair else nxt
        if c + nxt == "ⲟⲩ" and (after and after in VOWELS or prev and prev in VOWELS):
            out.append("w")
        elif (c + nxt == "ⲉⲓ" or c == "ⲓ") and after and after in VOWELS:
            out.append("y")
        elif c == "ⲩ" and prev and prev in VOWELS:
            out.append("w")
        else:
            if not out and i == 0:
                out.append("A")
            vowel = "o" if c + nxt == "ⲟⲩ" else "i" if c + nxt == "ⲉⲓ" else VOWEL_OF[c]
            if vowels and out[-1:] != [vowel]:
                out.append(vowel)
        i += 2 if pair else 1
    return "".join(out)


# -------------------------------------------------------------------------------------------------- pools

def demotic_pool(path=DEMOTIC):
    """One entry for each lemma: its kinds are the tags that a tenth or more of its tokens carry."""
    tags, forms = collections.defaultdict(collections.Counter), {}
    for line in path.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        for lemma, gloss in zip(r["lemmatization"].split(), r["glossing"].split()):
            ident, _, form = lemma.partition("|")
            tags[ident][re.split(r"[.:]", gloss)[0]] += 1
            forms[ident] = form
    out = []
    for ident, form in forms.items():
        n = sum(tags[ident].values())
        kinds = {TAG[t] for t, k in tags[ident].items() if t in TAG and k * 10 >= n}
        codes = {demotic(form, True), demotic(form, False)} - {""}
        if codes:
            out.append({"id": "tla:" + ident, "form": form, "kinds": sorted(kinds), "codes": sorted(codes),
                        "tokens": n, "meaning": ""})
    return out


def coptic_pool(path=COPTIC):
    t = "{http://www.tei-c.org/ns/1.0}"
    lang = "{http://www.w3.org/XML/1998/namespace}"
    out = []
    for e in ET.parse(path).getroot().iter(t + "entry"):
        orths = [o.text.strip() for o in e.iter(t + "orth") if o.text and o.text.strip()]
        codes = {coptic(o) for o in orths} - {""}
        if not codes:
            continue
        pos = next(e.iter(t + "pos"), None)            # on the entry, or on each of its forms
        kind = TAG.get((pos.text or "").strip().rstrip("?")) if pos is not None else None
        en = [q.text.strip() for q in e.iter(t + "quote") if q.get(lang + "lang") == "en" and q.text]
        greek = [r.text for r in e.iter(t + "ref") if r.get("type") == "greek_lemma::grl_lemma" and r.text]
        out.append({"id": "ccl:" + e.get(lang + "id"), "form": orths[0], "kinds": [kind] if kind else [],
                    "codes": sorted(codes), "voiced": sorted({coptic(o, True) for o in orths} - {""}),
                    "tokens": 0, "meaning": en[0] if en else "", "greek": greek[0] if greek else ""})
    return out


def pools():
    for p in (DEMOTIC, COPTIC):
        if not p.exists():
            sys.exit(f"no {p.relative_to(ROOT)}: the two word lists are kept locally (data/discovery/egyptian.md)")
    return demotic_pool() + coptic_pool()


class Trie:
    """The letter strings of some pool entries, sharing their beginnings."""

    def __init__(self, entries, codes="codes"):
        self.root = {}
        self.size = len(entries)
        for k, e in entries:
            for code in e[codes]:
                node = self.root
                for c in code:
                    node = node.setdefault(c, {})
                node.setdefault("", []).append(k)


def tries(pool):
    """A trie for each set of kinds that SCOPE names, and one for everything ("all")."""
    wanted = {frozenset(s) for pair in SCOPE.values() for s in pair}
    out = {s: Trie([(k, e) for k, e in enumerate(pool) if s & set(e["kinds"])]) for s in wanted}
    out["all"] = Trie(list(enumerate(pool)))
    return out


# -------------------------------------------------------------------------------------------------- model

def neutral(e, mer=MER):
    """The starting chances for one Egyptian letter: {Meroitic letter or "" (dropped): chance}. `mer` is the
    Meroitic alphabet: the consonants, or (in the vowel search) the consonants and the vowels."""
    same = SAME.get(e, e if e in mer else "")
    group = [m for m in mer if GROUP[m] == GROUP[e] and m != same]
    drop, own, rest = (0.45, 0.35, 0.20) if e in WEAK else (0.10, 0.80, 0.10)
    p = {m: rest / len(mer) for m in mer}
    p[""] = drop
    if e == "h":                             # no h in Meroitic: a vowel at the start, or one of its two ḫ signs
        for m, share in (("0", 0.5), ("x", 0.25), ("X", 0.25)):
            p[m] += own * share
    elif same and group:
        p[same] += own * 0.75
        for m in group:
            p[m] += own * 0.25 / len(group)
    elif same:
        p[same] += own
    else:
        for m in group:
            p[m] += own / len(group)
    return p


def model(counts=None, mer=MER, egy=EGY):
    """Log chances from the counts of aligned loans, on top of the neutral table, for the two alphabets."""
    c = counts or {"out": collections.Counter(), "add": collections.Counter(), "article": collections.Counter()}
    out = {}
    for e in egy:
        n = sum(k for (x, _), k in c["out"].items() if x == e)
        out[e] = {m: math.log((c["out"][(e, m)] + STRENGTH * p) / (n + STRENGTH)) for m, p in neutral(e, mer).items()}
    added, kept = sum(c["add"].values()), sum(c["out"].values())
    p_add = (added + 1.0) / (added + kept + 10.0)
    add = {m: math.log(p_add * (c["add"][m] + 2.0 / len(mer)) / (added + 2.0)) for m in mer}
    stay = math.log(1 - p_add)
    n = sum(c["article"].values())
    article = {a: math.log((c["article"][a] + 1.0) / (n + len(ARTICLES))) for a in ARTICLES}
    return {"out": {e: {m: v + stay for m, v in row.items()} for e, row in out.items()}, "add": add,
            "article": article}


def step(row, e, word, md):
    """The row after one more Egyptian letter: row[j] is the best log chance of the word's first j letters."""
    out_e, add = md["out"][e], md["add"]
    new = [row[0] + out_e[""]]
    for j in range(1, len(row)):
        m = word[j - 1]
        new.append(max(row[j] + out_e[""], row[j - 1] + out_e[m], new[j - 1] + add[m]))
    return new


def first_row(word, md):
    row = [0.0]
    for m in word:
        row.append(row[-1] + md["add"][m])
    return row


def score(word, code, md):
    """The best log chance that the Egyptian letters `code`, alone or with an article, give the Meroitic word."""
    best = -math.inf
    for a in ARTICLES:
        row = first_row(word, md)
        for e in a + code:
            row = step(row, e, word, md)
        best = max(best, row[-1] + md["article"][a])
    return best


def align(word, code, md):
    """The best alignment: (article, [(Egyptian letter or "", Meroitic letter or "")])."""
    best = None
    for a in ARTICLES:
        full = a + code
        rows = [first_row(word, md)]
        for e in full:
            rows.append(step(rows[-1], e, word, md))
        total = rows[-1][-1] + md["article"][a]
        if best is None or total > best[0]:
            i, j, ops = len(full), len(word), []
            while i or j:
                here = rows[i][j]
                if i and j and math.isclose(here, rows[i - 1][j - 1] + md["out"][full[i - 1]][word[j - 1]]):
                    ops.append((full[i - 1], word[j - 1]))
                    i, j = i - 1, j - 1
                elif i and math.isclose(here, rows[i - 1][j] + md["out"][full[i - 1]][""]):
                    ops.append((full[i - 1], ""))
                    i -= 1
                else:
                    ops.append(("", word[j - 1]))
                    j -= 1
            best = (total, a, ops[::-1])
    return best[1], best[2]


def train(pairs, rounds=3, mer=MER, egy=EGY):
    """The model counted from known loans: pairs of (Meroitic letters, the letter strings of the true source)."""
    md = model(None, mer, egy)
    for _ in range(rounds):
        counts = {"out": collections.Counter(), "add": collections.Counter(), "article": collections.Counter()}
        for word, codes in pairs:
            code = max(codes, key=lambda c: (score(word, c, md), c))
            a, ops = align(word, code, md)
            counts["article"][a] += 1
            used = 0                         # Egyptian letters aligned so far; the first len(a) are the article
            for e, m in ops:
                if not e:
                    counts["add"][m] += 1    # a Meroitic letter added, also when it comes before the article
                    continue
                used += 1
                if used > len(a):            # the article's own letter is the article, not a sound match
                    counts["out"][(e, m)] += 1
        md = model(counts, mer, egy)
    return md


def search(word, trie, md, top=1, floor=None):
    """The best pool entries for a word: [(score, entry number)], best first and ties by entry number, one row an
    entry: what scoring every entry would give.

    With `floor`, every entry that scores `floor` or better instead. A branch is left as soon as no word below
    it can reach the bar: a row's best cell bounds every score under it.
    """
    found = {}
    bar = [floor if floor is not None else -math.inf]

    def walk(node, row, bonus):
        for e, child in node.items():
            if e == "":
                s = row[-1] + bonus
                if s >= bar[0]:
                    for k in child:
                        if s > found.get(k, -math.inf):
                            found[k] = s
                    if floor is None and top == 1:
                        bar[0] = s               # only an equal or better score can still be the best match
                    if floor is None and len(found) > 4 * top:
                        # ties by entry number, as in the final ranking: an entry left out here has `top` entries
                        # ranked above it, so it could not be among the best
                        keep = sorted(found.items(), key=lambda kv: (-kv[1], kv[0]))[:top]
                        bar[0] = keep[-1][1]
                        found.clear()
                        found.update(keep)
                continue
            new = step(row, e, word, md)
            if max(new) + bonus >= bar[0]:
                walk(child, new, bonus)

    for a in ARTICLES:
        row = first_row(word, md)
        for e in a:
            row = step(row, e, word, md)
        walk(trie.root, row, md["article"][a])
    ranked = sorted(((s, k) for k, s in found.items()), key=lambda x: (-x[0], x[1]))
    return ranked if floor is not None else ranked[:top]


# ------------------------------------------------------------------------------------------ the answer key

def key():
    if not KEY.exists():
        sys.exit(f"no {KEY.relative_to(ROOT)}: the answer key is drawn from Rilly's lexicon and kept locally")
    return [json.loads(l) for l in KEY.read_text(encoding="utf-8").splitlines() if l.strip()]


def known(pool):
    """The known loans the test can use: accepted by Rilly, a borrowing for both readers, and with a source
    that stands in the pools (key_sources.json names it): [{"headword", "kind", "word", "sources"}]."""
    by_id = {e["id"]: k for k, e in enumerate(pool)}
    named = json.loads(SOURCES.read_text(encoding="utf-8")) if SOURCES.exists() else {}
    out = []
    for r in key():
        if not (r["both_into_meroitic"] and r["status"] in L.GOOD):
            continue
        ids = [i for i in named.get(r["headword"], []) if i in by_id]
        out.append({"headword": r["headword"], "kind": KEY_KIND.get(r["kind"], r["kind"]),
                    "word": headword(r["headword"]), "voiced": headword(r["headword"], True),
                    "sources": [by_id[i] for i in ids], "etymon": r["etymon"], "also": r["also"]})
    return out


def pairs(items, pool, without=(), word="word", codes="codes"):
    """The training pairs of the known loans, leaving out every loan that shares a source with `without`.
    `word` and `codes` name the letter strings to pair: with vowels, "voiced" for both."""
    return [(it[word], sorted({c for k in it["sources"] for c in pool[k][codes]}))
            for it in items if it["sources"] and it[word] and not set(it["sources"]) & set(without)]


def place(word, sources, trie, md, pool, codes="codes"):
    """How many entries of the trie score as well as the best of the true sources, or None when none is in it."""
    inside = [k for k in sources if any(k in ks for ks in leaves(trie, pool[k][codes]))]
    if not inside:
        return None, None
    best = max(score(word, c, md) for k in inside for c in pool[k][codes])
    return len(search(word, trie, md, floor=best - 1e-9)), best


def leaves(trie, codes):
    for code in codes:
        node = trie.root
        for c in code:
            node = node.get(c)
            if node is None:
                break
        else:
            yield node.get("", [])


def printed(r):
    """The letter strings of the Egyptian and Demotic words that a key row prints as the source."""
    out = set()
    for lang, _, form in [(r["language"], "", r["etymon"])] + [a.partition(" ") for a in r["also"]]:
        if lang in ("Egyptian", "Demotic") and form:
            form = "".join(RILLY.get(c, c) for c in unicodedata.normalize("NFC", form.lower()))
            out |= {demotic(form, True), demotic(form, False)}
        elif lang == "Coptic" and form:
            out.add(coptic(form))
    return {c for c in out if len(c) >= 2}


def place_of_letters(word, codes, trie, md):
    """How many entries score as well as the best entry that has one of these letter strings, or None."""
    inside = [c for c in codes if any(ks for ks in leaves(trie, [c]))]
    if not inside:
        return None
    return len(search(word, trie, md, floor=max(score(word, c, md) for c in inside) - 1e-9))


def made_up(words, n=MADE_UP, seed=SEED, longest=LONGEST, least=0):
    """n made-up words of each length from SHORTEST to `longest` (and longer): each letter is drawn as letters
    follow one another in `words`, so the made-up words sound like Meroitic ones. {length: [letters]}
    With `least`, only words of that many consonants or more are kept (the vowel search's words)."""
    rnd = random.Random(seed)
    follows = collections.defaultdict(list)
    for w in sorted(words):
        for a, b in zip("^" + w, w + "$"):
            follows[a].append(b)
    out = {k: [] for k in range(SHORTEST, longest + 1)}
    while any(len(v) < n for v in out.values()):
        w, c = "", rnd.choice(follows["^"])
        while c != "$" and len(w) < longest + 2:
            w, c = w + c, rnd.choice(follows[c])
        k = min(len(w), longest)
        if k in out and len(out[k]) < n and consonants(w) >= least:
            out[k].append(w)
    return out


def headwords(vowels=False):
    """The letters of every entry of the lexicon proper that is not a name or a grammatical word."""
    out = []
    for e in L.load():
        kind = C.kind_of(e.get("category"))
        if e.get("page_pdf", 0) < L.REJECTED_FROM and kind not in C.NAME_KINDS and kind != "function word":
            word = headword(e["headword"], vowels)
            if consonants(word) >= 2:
                out.append(word)
    return out


def passing(chances, q=FDR):
    """How many of the chances pass Benjamini and Hochberg's bar: at most a share q of those passing are
    expected to be chance."""
    ranked = sorted(chances)
    return max([k + 1 for k, p in enumerate(ranked) if p <= q * (k + 1) / len(ranked)], default=0)


def as_many(k, n, p=BAR):
    """The chance that k or more of n words beat a bar that each beats with chance p."""
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def fewest_to_pass(n, q=FDR, made=MADE_UP):
    """How many of n pieces must sit at the smallest chance there is, 1 / (made + 1), before Benjamini and
    Hochberg's bar lets any of them pass: a single piece never can when q / n is smaller than that."""
    return math.ceil(n / (q * (made + 1)) - 1e-12)


# ----------------------------------------------------------------------------------------------- commands

def native(loans):
    """Meroitic words with an accepted meaning that nobody derives from Egyptian: entries of the lexicon proper
    that are established or probable, are not names or grammar, and are not among the entries that mention
    Egyptian, Demotic, Coptic, Greek or Latin. [(headword, kind, letters)]"""
    mentioned = {r["headword"] for r in loans}
    out = []
    for e in L.load():
        kind = C.kind_of(e.get("category"))
        if (e.get("page_pdf", 0) >= L.REJECTED_FROM or e.get("status") not in L.GOOD or e["headword"] in mentioned
                or kind in C.NAME_KINDS or kind == "function word"):
            continue
        word = headword(e["headword"])
        if len(word) >= SHORTEST:
            out.append((e["headword"], kind or "unknown", word))
    return out


def chance(score_, scores):
    """The share of comparison words that reach `score_` or better, counting the word itself: (k + 1) / (n + 1)."""
    return (sum(1 for s in scores if s >= score_ - 1e-9) + 1) / (len(scores) + 1)


def unknown():
    """The pieces of the coverage map's list that have a kind the pools know: [(piece, kind, letters, row)].
    A piece that is letters (not a headword) and holds a digit or a lost sign is not a word: no letters."""
    out = []
    for r in csv.DictReader(UNKNOWN.open(encoding="utf-8"), delimiter="\t"):
        if r["kind"] not in SCOPE:
            continue
        if r["headword or letters"] == "headword":
            word = headword(r["piece"])
        else:
            word = meroitic(r["piece"]) if re.fullmatch(r"[a-zA-Z]+", r["piece"]) else ""
        out.append((r["piece"], r["kind"], word, r))
    return out


def linked(rows):
    """The letters of the entries that the lexicon already links to an Egyptian word, as a loan or a proposal:
    {letters: headword}."""
    out = {}
    for r in rows:
        if r["both_into_meroitic"] or r["reader1"] == r["reader2"] == "proposed":
            word = headword(r["headword"])
            if word:
                out.setdefault(word, r["headword"])
    return out


def show(e):
    return f'{e["id"]} {e["form"]}' + (f' "{e["meaning"]}"' if e["meaning"] else "")


def first():
    pool = pools()
    kinds = collections.Counter(k for e in pool for k in e["kinds"])
    print(f"pool: {len(pool)} entries ({sum(e['id'].startswith('tla:') for e in pool)} Demotic lemmata, "
          f"{sum(e['id'].startswith('ccl:') for e in pool)} Coptic entries), "
          f"{len({c for e in pool for c in e['codes']})} different letter strings")
    print("kinds:", dict(kinds.most_common()), "| no kind:", sum(not e["kinds"] for e in pool))
    items = known(pool)
    print(f"known loans: {len(items)}; with a source in the pools: {sum(bool(i['sources']) for i in items)}")
    for it in items:
        print(f'  {it["headword"]:12} {it["kind"]:12} {it["word"]:8} <- {it["etymon"]:24} '
              + ("; ".join(show(pool[k]) for k in it["sources"]) or "NOT IN THE POOLS"))


def find(word):
    """Pool entries whose letters equal the letters of an Egyptian word in TLA or Coptic spelling."""
    pool = pools()
    codes = {demotic(word, True), demotic(word, False), coptic(word)} - {""}
    print("letters:", sorted(codes))
    for e in pool:
        if codes & set(e["codes"]):
            print(" ", show(e), e["kinds"], e["codes"], e["tokens"])


def scopes(kind):
    narrow, wide = (frozenset(x) for x in SCOPE[kind])
    return (("narrow", narrow), ("wide", wide))


def build():
    pool = pools()
    tr = tries(pool)
    items = known(pool)
    usable = [it for it in items if it["sources"] and it["word"]]
    fake = made_up(headwords())
    OUT.mkdir(parents=True, exist_ok=True)

    def chance_of(word, s, md, cache):
        """The share of made-up words of the word's length whose best match in a scope is as good as its own."""
        k = (s, min(len(word), LONGEST))
        if k not in cache:
            cache[k] = [search(w, tr[s], md)[0][0] for w in fake[k[1]]]
        return chance(search(word, tr[s], md)[0][0], cache[k])

    # 3. the test: each known loan with a model trained on the others
    test = []
    for it in items:
        row = {"headword": it["headword"], "kind": it["kind"], "letters": it["word"],
               "source": [pool[k]["id"] for k in it["sources"]]}
        if it in usable:
            md, cache = train(pairs(usable, pool, without=it["sources"])), {}
            for name, s in scopes(it["kind"]) + (("all", "all"),):
                n, sc = place(it["word"], it["sources"], tr[s], md, pool)
                best = search(it["word"], tr[s], md)[0]
                row[name] = {"place": n, "of": tr[s].size, "score": sc, "best": best[0], "best_id": pool[best[1]]["id"]}
                if len(it["word"]) >= SHORTEST and name != "all":
                    row[name]["chance"] = chance_of(it["word"], s, md, cache)
        test.append(row)
    (OUT / "test.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in test))

    # 4. everything else with the model trained on every known loan
    md, cache = train(pairs(usable, pool)), {}
    (OUT / "model.json").write_text(json.dumps(
        {"out": {e: {m or "-": round(math.exp(v), 4) for m, v in row.items()} for e, row in md["out"].items()},
         "add": {m: round(math.exp(v), 4) for m, v in md["add"].items()},
         "article": {a or "-": round(math.exp(v), 4) for a, v in md["article"].items()}}, indent=1))

    # words with an accepted meaning that nobody derives from Egyptian: do they look like the made-up words?
    plain = native(key())
    all_scopes = sorted({s for kind in SCOPE for _, s in scopes(kind)}, key=sorted)
    calm = {"+".join(sorted(s)): sorted(chance_of(w, s, md, cache) for _, _, w in plain) for s in all_scopes}

    # the proposals of the literature and the Meroitic words written in Egyptian letters
    others = []
    for r in key():
        label = ("proposal" if r["both_into_meroitic"] and r["status"] not in L.GOOD else
                 "in Egyptian letters" if r["reader1"] == r["reader2"] == "reverse" else "")
        kind, word = KEY_KIND.get(r["kind"], r["kind"]), headword(r["headword"])
        if label and kind in SCOPE and len(word) >= SHORTEST and printed(r):
            row = {"headword": r["headword"], "label": label, "kind": kind, "letters": word}
            for name, s in scopes(kind):
                row[name] = place_of_letters(word, printed(r), tr[s], md)
            others.append(row)
    (OUT / "others.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in others))

    # the pieces without a meaning
    in_key, same = {r["headword"] for r in key()}, linked(key())
    rows = []
    for piece, kind, word, r in unknown():
        row = {"piece": piece, "kind": kind, "letters": word, "level": r["level"],
               "texts": int(r["texts (near-copies once)"]), "headword": r["headword or letters"] == "headword",
               "mentions_egyptian": piece in in_key, "spelled_like": same.get(word, "")}
        if len(word) >= SHORTEST:
            for name, s in scopes(kind):
                hits = search(word, tr[s], md, top=5)
                row[name] = {"chance": chance_of(word, s, md, cache),
                             "hits": [{"id": pool[k]["id"], "form": pool[k]["form"], "meaning": pool[k]["meaning"],
                                       "score": round(sc, 3)} for sc, k in hits]}
        rows.append(row)
    (OUT / "candidates.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))

    fig = figures(pool, test, calm, others, rows, len(plain))
    (OUT / "figures.json").write_text(json.dumps(fig, ensure_ascii=False, indent=1) + "\n")
    PUBLIC.write_text(public_list(rows), encoding="utf-8")
    print(json.dumps(fig, ensure_ascii=False, indent=1))


def figures(pool, test, calm, others, rows, plain):
    def tops(rs, name):
        got = [r[name]["place"] for r in rs if name in r and r[name]["place"]]
        return {"in_scope": len(got), **{f"top{k}": sum(p <= k for p in got) for k in (1, 3, 5, 10)}}

    def beats(rs, name, bar=BAR):
        got = [r[name]["chance"] for r in rs if name in r and "chance" in r[name]]
        return {"compared": len(got), "at_most_0.05": sum(c <= bar for c in got)}

    with_source = [r for r in test if "all" in r]
    names = [r for r in test if r["kind"] in C.NAME_KINDS]
    words = [r for r in test if r["kind"] not in C.NAME_KINDS]
    searched = [r for r in rows if "narrow" in r]
    fresh = [r for r in searched if not (r["mentions_egyptian"] or r["spelled_like"])]
    below = {name: sum(r[name]["chance"] <= BAR for r in fresh) for name in ("narrow", "wide")}
    out = {
        "pool": {"entries": len(pool), "demotic": sum(e["id"].startswith("tla:") for e in pool),
                 "coptic": sum(e["id"].startswith("ccl:") for e in pool),
                 "kinds": dict(collections.Counter(k for e in pool for k in e["kinds"]).most_common())},
        "test": {"loans": len(test), "with_source": len(with_source),
                 "names": {"loans": len(names), "with_source": sum("all" in r for r in names),
                           "narrow": tops(names, "narrow"), "wide": tops(names, "wide"), "all": tops(names, "all"),
                           "chance_narrow": beats(names, "narrow"), "chance_wide": beats(names, "wide")},
                 "words": {"loans": len(words), "with_source": sum("all" in r for r in words),
                           "narrow": tops(words, "narrow"), "wide": tops(words, "wide"), "all": tops(words, "all"),
                           "chance_narrow": beats(words, "narrow"), "chance_wide": beats(words, "wide")}},
        "native": {"words": plain, "at_most_0.05": {s: sum(c <= BAR for c in v) for s, v in calm.items()},
                   "at_most_0.2": {s: sum(c <= 0.2 for c in v) for s, v in calm.items()}},
        "others": {label: {"words": len(rs),
                           **{name: {"in_scope": sum(r[name] is not None for r in rs),
                                     "top5": sum(r[name] is not None and r[name] <= 5 for r in rs)}
                              for name in ("narrow", "wide")}}
                   for label in ("proposal", "in Egyptian letters")
                   for rs in [[r for r in others if r["label"] == label]]},
        "unknown": {"pieces": len(rows), "searched": len(searched), "too_short": len(rows) - len(searched),
                    "new": len(fresh),
                    **{name: {"at_most_0.05": below[name], "expected_by_chance": round(BAR * len(fresh), 1),
                              "as_many_by_chance": round(as_many(below[name], len(fresh)), 3),
                              "passing_q_0.2": passing([r[name]["chance"] for r in fresh])}
                       for name in ("narrow", "wide")},
                    "smallest_chance": round(1 / (MADE_UP + 1), 5), "first_step_q_0.2": round(FDR / len(fresh), 6),
                    "fewest_at_the_smallest_chance_to_pass": fewest_to_pass(len(fresh)),
                    "by_kind": dict(collections.Counter(r["kind"] for r in searched).most_common())},
    }
    return out


def public_list(rows):
    """The public list: each searched piece with its best match among the words of its kind, narrow and wide.
    It holds lemma numbers and forms of the two word lists and no meaning of either, nor any gloss of the lexicon."""
    head = ["piece", "kind", "texts (near-copies once)",
            "set aside: its entry in the lexicon mentions Egyptian, Demotic, Coptic, Greek or Latin, or it is "
            "spelled like an entry linked to Egyptian",
            "narrow: chance", "narrow: best match", "narrow: its form", "wide: chance", "wide: best match",
            "wide: its form"]
    lines = ["\t".join(head)]
    searched = [r for r in rows if "narrow" in r]
    for r in sorted(searched, key=lambda r: (min(r["narrow"]["chance"], r["wide"]["chance"]), -r["texts"], r["piece"])):
        cells = [r["piece"], r["kind"], str(r["texts"]),
                 "yes" if r["mentions_egyptian"] else f'spelled like {r["spelled_like"]}' if r["spelled_like"] else "no"]
        for name in ("narrow", "wide"):
            hit = r[name]["hits"][0]
            cells += [f'{r[name]["chance"]:.3f}', hit["id"], hit["form"]]
        lines.append("\t".join(cells))
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------------------------------- with vowels

PUBLIC_VOWELS = ROOT / "data/discovery/egyptian_candidates_vowels.tsv"


def vowels():
    """The test, the comparison and the search once more with the vowels compared, on the Coptic entries.

    Everything is as in build(), but for the letter strings ("voiced": the consonants and the written vowels), the
    two alphabets, and the pools: a word is searched among the Coptic entries of VOWEL_SCOPE. Beside each place
    of the test stands the place that the consonants alone give in the same pool, with a model trained on the same
    loans, so that the two differ in the vowels only."""
    for p in (COPTIC,):
        if not p.exists():
            sys.exit(f"no {p.relative_to(ROOT)}: the two word lists are kept locally (data/discovery/egyptian.md)")
    pool = coptic_pool()
    mer, egy = MER + VOWELS_M, EGY + VOWELS_E
    sets = sorted({frozenset(v) for v in VOWEL_SCOPE.values()}, key=sorted)
    tr = {s: Trie([(k, e) for k, e in enumerate(pool) if s & set(e["kinds"])], "voiced") for s in sets}
    bare = {s: Trie([(k, e) for k, e in enumerate(pool) if s & set(e["kinds"])]) for s in sets}
    items = [it for it in known(pool) if it["sources"] and it["voiced"]]
    fake = made_up(headwords(True), longest=VOWEL_LONGEST, least=SHORTEST)
    OUT.mkdir(parents=True, exist_ok=True)

    def chance_of(word, s, md, cache):
        k = (s, min(len(word), VOWEL_LONGEST))
        if k not in cache:
            cache[k] = [search(w, tr[s], md)[0][0] for w in fake[k[1]]]
        return chance(search(word, tr[s], md)[0][0], cache[k])

    # the test: each known loan that has a Coptic source, among the Coptic entries of its kind (a name among nouns)
    test = []
    for it in items:
        s = frozenset(VOWEL_SCOPE.get(it["kind"], {"noun"}))
        md = train(pairs(items, pool, it["sources"], "voiced", "voiced"), mer=mer, egy=egy)
        plain = train(pairs(items, pool, it["sources"]))
        n, _ = place(it["voiced"], it["sources"], tr[s], md, pool, "voiced")
        best = search(it["voiced"], tr[s], md)[0]
        row = {"headword": it["headword"], "kind": it["kind"], "letters": it["voiced"],
               "source": [pool[k]["id"] for k in it["sources"]], "of": tr[s].size,
               "consonants": place(it["word"], it["sources"], bare[s], plain, pool)[0],
               "vowels": n, "best_id": pool[best[1]]["id"]}
        if consonants(it["voiced"]) >= SHORTEST:
            row["chance"] = chance_of(it["voiced"], s, md, {})
        test.append(row)
    (OUT / "vowel_test.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in test))

    # everything else with the model trained on every such loan
    md, cache = train(pairs(items, pool, (), "voiced", "voiced"), mer=mer, egy=egy), {}
    plain = [headword(h, True) for h, _, _ in native(key())]
    calm = {"+".join(sorted(s)): sorted(chance_of(w, s, md, cache) for w in plain) for s in sets}
    in_key, same = {r["headword"] for r in key()}, linked(key())
    rows = []
    for piece, kind, word, r in unknown():
        if kind not in VOWEL_SCOPE or len(word) < SHORTEST:
            continue
        head = r["headword or letters"] == "headword"
        voiced = headword(piece, True) if head else meroitic(piece, True)
        s = frozenset(VOWEL_SCOPE[kind])
        rows.append({"piece": piece, "kind": kind, "letters": voiced, "level": r["level"],
                     "texts": int(r["texts (near-copies once)"]), "headword": head,
                     "mentions_egyptian": piece in in_key, "spelled_like": same.get(word, ""),
                     "vowels": {"chance": chance_of(voiced, s, md, cache),
                                "hits": [{"id": pool[k]["id"], "form": pool[k]["form"], "meaning": pool[k]["meaning"],
                                          "score": round(sc, 3)} for sc, k in search(voiced, tr[s], md, top=5)]}})
    (OUT / "vowel_candidates.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    fig = vowel_figures(pool, test, calm, rows, len(plain))
    (OUT / "vowel_figures.json").write_text(json.dumps(fig, ensure_ascii=False, indent=1) + "\n")
    PUBLIC_VOWELS.write_text(public_vowel_list(rows), encoding="utf-8")
    print(json.dumps(fig, ensure_ascii=False, indent=1))


def vowel_figures(pool, test, calm, rows, plain):
    def tops(rs, name):
        got = [r[name] for r in rs if r[name]]
        return {"in_scope": len(got), **{f"top{k}": sum(p <= k for p in got) for k in (1, 3, 5, 10)}}

    words = [r for r in test if r["kind"] not in C.NAME_KINDS]
    names = [r for r in test if r["kind"] in C.NAME_KINDS]
    compared = [r["chance"] for r in test if "chance" in r]
    fresh = [r for r in rows if not (r["mentions_egyptian"] or r["spelled_like"])]
    below = sum(r["vowels"]["chance"] <= BAR for r in fresh)
    return {
        "pool": {"coptic": len(pool), "kinds": dict(collections.Counter(k for e in pool for k in e["kinds"]).most_common())},
        "test": {"loans": len(test), "moved_up": sum(r["vowels"] < r["consonants"] for r in test),
                 "moved_down": sum(r["vowels"] > r["consonants"] for r in test),
                 "all": {"consonants": tops(test, "consonants"), "vowels": tops(test, "vowels")},
                 "words": {"loans": len(words), "consonants": tops(words, "consonants"), "vowels": tops(words, "vowels")},
                 "names": {"loans": len(names), "consonants": tops(names, "consonants"), "vowels": tops(names, "vowels")},
                 "chance": {"compared": len(compared), "at_most_0.05": sum(c <= BAR for c in compared)}},
        "native": {"words": plain, "at_most_0.05": {s: sum(c <= BAR for c in v) for s, v in calm.items()},
                   "at_most_0.2": {s: sum(c <= 0.2 for c in v) for s, v in calm.items()}},
        "unknown": {"searched": len(rows), "new": len(fresh), "at_most_0.05": below,
                    "expected_by_chance": round(BAR * len(fresh), 1),
                    "as_many_by_chance": round(as_many(below, len(fresh)), 3),
                    "passing_q_0.2": passing([r["vowels"]["chance"] for r in fresh]),
                    "fewest_at_the_smallest_chance_to_pass": fewest_to_pass(len(fresh)),
                    "by_kind": dict(collections.Counter(r["kind"] for r in rows).most_common())},
    }


def public_vowel_list(rows):
    """The public list of the vowel search: each searched piece with its best match among the Coptic entries of
    its kind. Like the first list it holds lemma numbers and forms, no meaning and no gloss."""
    head = ["piece", "kind", "texts (near-copies once)",
            "set aside: its entry in the lexicon mentions Egyptian, Demotic, Coptic, Greek or Latin, or it is "
            "spelled like an entry linked to Egyptian",
            "letters compared", "chance", "best match", "its form"]
    lines = ["\t".join(head)]
    for r in sorted(rows, key=lambda r: (r["vowels"]["chance"], -r["texts"], r["piece"])):
        hit = r["vowels"]["hits"][0]
        lines.append("\t".join([
            r["piece"], r["kind"], str(r["texts"]),
            "yes" if r["mentions_egyptian"] else f'spelled like {r["spelled_like"]}' if r["spelled_like"] else "no",
            r["letters"], f'{r["vowels"]["chance"]:.3f}', hit["id"], hit["form"]]))
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------------------------------------ the check

GLOSSES = ROOT / "data/sources/coverage/glosses.jsonl"      # the coverage map's gloss file, local only
CHECK = HERE / "check"
CHECK_VOWELS = HERE / "check_vowels"                        # the second pack: the vowel search's best matches
DECOYS_VOWELS = 6
BRIEF = ROOT / "data/discovery/egyptian_brief.md"
DECOYS = 12                   # pieces whose best match is poor, mixed into the pack unmarked; a piece goes to
                              # the checkers when its best match beats the bar (BAR)


def contexts(spellings, texts, n=3, side=5):
    """Up to n places where one of the spellings stands, each from another text, with the map's glosses."""
    out = []
    for t in texts:
        forms = [g["form"] for g in t["glosses"]]
        k = next((k for k, f in enumerate(forms) if f in spellings), None)
        if k is not None:
            near = t["glosses"][max(0, k - side):k + side + 1]
            out.append({"text": t["id"], "words": " ".join(g["form"] for g in near),
                        "glosses": " / ".join(str(g.get("gloss") or "?")[:28] for g in near)})
        if len(out) == n:
            break
    return out


def samples(ids, n=2):
    """Up to n sentences of the Demotic file for each lemma: {id: [{"words", "german"}]}."""
    out = collections.defaultdict(list)
    for line in DEMOTIC.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        for lemma in r["lemmatization"].split():
            ident = "tla:" + lemma.partition("|")[0]
            if ident in ids and len(out[ident]) < n and r["translation"] not in [x["german"] for x in out[ident]]:
                out[ident].append({"words": r["transliteration"][:90], "german": r["translation"][:160]})
    return out


def check_pack(with_vowels=False):
    """Write the checkers' pack: the pieces whose best match beats the bar, and decoys, in one shuffled list.
    `with_vowels`: the second pack, of the vowel search's best matches that the first pack did not hold."""
    if with_vowels:
        rows = [json.loads(l) for l in (OUT / "vowel_candidates.jsonl").read_text(encoding="utf-8").splitlines()]
        seen = {a["piece"] for a in json.loads((HERE / "check_key.json").read_text(encoding="utf-8")).values()}
        fresh = [r for r in rows if not (r["mentions_egyptian"] or r["spelled_like"]) and r["piece"] not in seen]
        low = lambda r: r["vowels"]["chance"]   # noqa: E731
        names, folder, keyfile, n_decoys = ("vowels",), CHECK_VOWELS, HERE / "check_vowels_key.json", DECOYS_VOWELS
    else:
        rows = [json.loads(l) for l in (OUT / "candidates.jsonl").read_text(encoding="utf-8").splitlines()]
        fresh = [r for r in rows if "narrow" in r and not (r["mentions_egyptian"] or r["spelled_like"])]
        low = lambda r: min(r["narrow"]["chance"], r["wide"]["chance"])   # noqa: E731
        names, folder, keyfile, n_decoys = ("narrow", "wide"), CHECK, HERE / "check_key.json", DECOYS
    best = [r for r in fresh if low(r) <= BAR]
    rnd = random.Random(SEED)
    decoys = rnd.sample(sorted((r for r in fresh if low(r) >= 0.5), key=lambda r: r["piece"]), n_decoys)
    items = best + decoys
    rnd.shuffle(items)
    pool = {e["id"]: e for e in pools()}
    texts = [json.loads(l) for l in GLOSSES.read_text(encoding="utf-8").splitlines()]
    spelled = {r["piece"]: set(r["spellings"].split()) | {r["piece"]}
               for r in csv.DictReader(UNKNOWN.open(encoding="utf-8"), delimiter="\t")}
    entries = {e["headword"]: e for e in L.load() if e.get("page_pdf", 0) < L.REJECTED_FROM}
    hits = {r["piece"]: list({h["id"]: h for name in names for h in r[name]["hits"][:3]}.values())
            for r in items}
    said = samples({h["id"] for hs in hits.values() for h in hs})
    folder.mkdir(parents=True, exist_ok=True)
    pack, answer = [], {}
    for k, r in enumerate(items, 1):
        ident = f"P{k:02d}"
        answer[ident] = {"piece": r["piece"], "decoy": r in decoys, "chance": low(r)}
        e = entries.get(r["piece"]) if r["headword"] else None
        pack.append({
            "id": ident, "piece": r["piece"], "kind": r["kind"], "texts": r["texts"],
            "contexts": contexts(spelled.get(r["piece"], {r["piece"]}), texts),
            "lexicon": {k2: (e.get(k2) or "")[:500] for k2 in ("meaning_en", "rilly_view", "proposals")} if e else None,
            "candidates": [{"id": h["id"], "form": h["form"], "kinds": pool[h["id"]]["kinds"],
                            "meaning": h["meaning"], "greek": pool[h["id"]].get("greek", ""),
                            "sentences": said.get(h["id"], [])} for h in hits[r["piece"]]]})
    (folder / "pack.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in pack))
    keyfile.write_text(json.dumps(answer, ensure_ascii=False, indent=1))
    (folder / "BRIEF.md").write_text(BRIEF.read_text(encoding="utf-8"))
    print(f"{len(pack)} items ({len(best)} best matches, {len(decoys)} decoys) in {folder.relative_to(ROOT)}")


VERDICTS = ("known", "fits", "no")


def check_merge(with_vowels=False):
    """Read the checkers' answers (check/reader*.jsonl) against the key of decoys; write check.json.
    `with_vowels`: the second pack's (check_vowels/, check_vowels.json)."""
    folder, stem = (CHECK_VOWELS, "check_vowels") if with_vowels else (CHECK, "check")
    answer = json.loads((HERE / f"{stem}_key.json").read_text(encoding="utf-8"))
    readers = {}
    for path in sorted(folder.glob("reader*.jsonl")):
        got = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                a = json.loads(line)
            except ValueError:
                continue
            if isinstance(a, dict) and isinstance(a.get("id"), str) and a["id"] in answer and a.get("verdict") in VERDICTS:
                got.setdefault(a["id"], a)
        readers[path.stem] = got
    real = [i for i, a in answer.items() if not a["decoy"]]
    decoy = [i for i, a in answer.items() if a["decoy"]]
    out = {"items": len(answer), "best": len(real), "decoys": len(decoy), "readers": {}}
    for name, got in readers.items():
        out["readers"][name] = {
            "answered": len(got),
            "best": dict(collections.Counter(got[i]["verdict"] for i in real if i in got)),
            "decoys": dict(collections.Counter(got[i]["verdict"] for i in decoy if i in got))}
    names = sorted(readers)
    if len(names) >= 2:
        a, b = readers[names[0]], readers[names[1]]
        both = [i for i in answer if i in a and i in b]
        out["same_verdict"] = sum(a[i]["verdict"] == b[i]["verdict"] for i in both)
        out["answered_by_both"] = len(both)
        for v in ("fits", "known"):
            out[f"{v}_for_both"] = [{"id": i, "piece": answer[i]["piece"], "decoy": answer[i]["decoy"],
                                     "candidates": [a[i].get("candidate", ""), b[i].get("candidate", "")],
                                     "reasons": [a[i].get("reason", ""), b[i].get("reason", "")]}
                                    for i in both if a[i]["verdict"] == b[i]["verdict"] == v]
    (OUT / f"{stem}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps(out, ensure_ascii=False, indent=1))


def main(argv):
    if argv[:1] == ["first"]:
        first()
    elif argv[:1] == ["find"] and len(argv) == 2:
        find(argv[1])
    elif argv[:1] == ["build"]:
        build()
    elif argv == ["vowels"]:
        vowels()
    elif argv in (["check"], ["check", "vowels"]):
        check_pack(with_vowels=argv[1:] == ["vowels"])
    elif argv in (["merge"], ["merge", "vowels"]):
        check_merge(with_vowels=argv[1:] == ["vowels"])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
