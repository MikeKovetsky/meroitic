"""Track A of the evidence from outside the texts: two whole dictionaries of Nile Nubian, typed from the page
images, compared with the Meroitic words of known meaning by Rilly's sound correspondences
(data/discovery/outside_evidence.md, section 2; the typists' brief is runs/prompts/NUBIAN_typists.md).

Everything is read and written under data/sources/nubian/ (local only), except the list of known words
(runs/nubian/known_words.json, committed with this script) and `public`.

  python3 -I src/nubian.py words     the known words of gate A1, each kept or dropped by the page's rules
                                     (runs/nubian/known_words.json; with their meanings, known_words_local.json)
  python3 -I src/nubian.py merge     the typed pages checked and joined (dictionary.tsv, merge_report.json)
  python3 -I src/nubian.py agree     the typing's bar on the 34 pages typed twice (agree.json)
  python3 -I src/nubian.py gate      gate A1, once (gate.json)
  python3 -I src/nubian.py public    data/discovery/outside_nubian_figures.json, counts only

The rules and the bars are the page's, with the rules it added at about 22:15 (section 2). What the page leaves
open is decided here, before any typed page was seen (the typists' notes on how they filled the cells were read,
data/sources/nubian/typists_notes.json; no typed page):

1. The meaning of a known word is taken in the page's order (wording()): the short wording of the public table
   (data/discovery/lexicon_statuses.tsv, `meaning_in_our_words`) where it has one; else, for a word a layer gives
   its meaning, the wording the layers' lines state for it most often; else the lexicon's English. Track B takes
   it the same way (src/frames.py).
2. FUNCTION_WORDS are taken out of that wording and out of the typists' English meanings before the engine makes
   its keys (keys_of()). The engine is not changed.
3. The third reduction by name (BY_NAME) drops a word only where the lexicon's entry named there names the word
   it rests on, and that word is one the correspondences were built from, or a loan by both readers of the
   Egyptian key. A named word that fails the check is kept by that rule, and the list says so.
4. A file that fails a check is listed and left out of dictionary.tsv; nothing in it is repaired. The gate does
   not run while a page is missing or fails, or while the typing's bar is not counted as met.
5. A headword cell may hold two or three forms of the word ("Bīr, bírri", "Kúsu und kússu", "Hilgē (D), halgē
   (K)"): forms() splits it, and the first form is the headword. The typing's bar compares the first forms; the
   gate scores every form as a variant of the row, as the engine does with "a ~ b" in the short lists, except a
   later form that begins or ends with a hyphen ("Mūr, -kā", "jom-bay, -bai"): that is an ending or a shortened
   form, which only the print completes. A form a typist put in `see` or `note` is not scored: there it stands
   beside pointers to other entries and comparisons, and nothing in the cell tells them apart.
6. The typing's bar sets aside, in a headword: every mark on a vowel (macron, acute and any other combining
   mark) and the case of the letters. It does not set aside a mark on a consonant (š ž ñ ṅ ǵ ń ǰ: there the mark
   makes another consonant), a hyphen or a space; but a mark that the books print in one way and the typists
   render in two counts as one (letters()): a g with any mark (both books print one marked g), and an n with a
   tilde or an acute (the palatal nasal: Reinisch prints ñ, Lepsius ń). The dot of ṅ, Lepsius's velar nasal, is
   another letter: the typists name it apart from ń, and the gate reads the two as two sounds. The German
   meanings are compared as written, but for the case, the composition of the letters and the long s (ſs, ſ
   and ß are one: a typing convention, not a reading).
7. For the engine a typed headword is read as the two books define their letters (Reinisch p. 1-2, Lepsius
   p. 5-7): ṅ is the velar nasal, ñ and ń the palatal nasal, a g with any mark the palatal stop that Reinisch
   writes j, and Reinisch's q the palatal he pairs with j. The engine reads the rest itself: length and accent
   dropped, š, ž, j, ǰ, y, z.
8. A dialect cell is split at commas, spaces and stops ("K, DF, M", "KDFM", "K. D."). K is Kenzi, D Dongola, F
   and M Nobiin; an entry with several marks is a row for each of those languages. A part that is not made of
   those letters ("Derr", a place) is no dialect mark: it is listed and gives no language. An entry without a
   mark is one row, as Nobiin: the engine scores the three by the same correspondences, so the choice cannot
   change the test, and one row keeps such an entry from counting three times at the top. A sub-row has the
   dialect and the loan mark of the entry it stands in.
9. Any `loan` that is not empty ("Ar", "*", "Kopt", "Tigré", "vgl. Ar.", "Ar?") drops the entry and its sub-rows,
   and nothing else does: an entry whose note names a source word in brackets but whose `loan` is empty stays.
"""
import collections
import csv
import difflib
import json
import pathlib
import re
import subprocess
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(ROOT / "src" / "v6")]
import cognates_rules as cr                            # noqa: E402  the engine, as it stands
import recurring as W                                  # noqa: E402
import themap as T                                     # noqa: E402
import words as D                                      # noqa: E402

HOME = ROOT / "data/sources/nubian"
LIST = ROOT / "runs/nubian/known_words.json"
PUBLIC = ROOT / "data/discovery/outside_nubian_figures.json"
PAGE = "data/discovery/outside_evidence.md"
LOANS = ROOT / "data/sources/egyptian/loans_both.jsonl"
TABLE = ROOT / "data/discovery/lexicon_statuses.tsv"    # the meanings in the project's own words (public)
# The books: the PDF indexes of the Nubian-German part, what is taken off an index for the printed page, and the
# name its rows carry in the engine.
BOOKS = {"R": {"first": 333, "last": 520, "page": 332, "list": "reinisch1879"},
         "L": {"first": 410, "last": 561, "page": 147, "list": "lepsius1880"}}
# The pages typed a second time, drawn by lot before any typist started (random.Random(SEED_SECOND): 19 of
# Reinisch's indexes, then 15 of Lepsius's).
SEED_SECOND = 20261116
SECOND = {"R": (334, 336, 381, 386, 387, 395, 415, 419, 426, 436, 461, 462, 466, 477, 480, 493, 495, 498, 509),
          "L": (419, 441, 457, 462, 467, 475, 501, 513, 521, 527, 529, 543, 552, 553, 556)}
HEADER = ["book", "index", "page", "n", "headword", "dialect", "loan", "plural", "pos", "gloss_de", "gloss_en", "see",
          "parent", "note"]
COLUMNS = ["book", "page", "headword", "dialect", "loan", "pos", "gloss_de", "gloss_en", "parent"]   # dictionary.tsv
CONTINUED = "(continued)"
COUNT = re.compile(r"# entries=(\d+) subrows=(\d+)")
# The bars, as the page states them (set and committed before any typist or this script was started).
TYPING = {"found": 0.95, "same_meaning": 0.90, "likeness": 0.8}
GATE = {"p": 0.05, "words": 30, "sims": 2000, "seed": 3, "short_rows": 5442, "engine": "1b4f0ff"}
# The known words: the map of 2026-11-16, the page's counts, and the words Rilly's correspondences were built from.
MAP_LAYERS = ("recurring", "rare_sure", "rare_later", "unnamed", "rare_millet", "leftover", "leftover_stems")
COUNTS = {"with_a_meaning": 160, "loans_by_both_readers": 15, "rule_words": 18, "left": 127}
RULE_WORDS = "abr are ato dime dm ḫlbi ḫre kdi ked l lẖ mte pwrite st tre wle yer wide abore qore nob ms".split()
MIN_LETTERS = 3
# The third reduction, by name (the page, 22:15): headword -> (what it is, the word it rests on, the lexicon entry
# whose text names that word, how). A form of a word the correspondences were built from, or a word built on a
# loan by both readers of the Egyptian key. ḫ- (1) 'meal' and ḫmlol 'a good meal' rest on the entry ḫlẖl, which
# writes their element ḫ- 'meal' as ḫ(re), Rilly's *ḫre 'repas' (correspondence N° 7); their own entries do not
# name it.
BY_NAME = {
    "qor": ("form", "qore", "qor", "qore with the article"),
    "yeto": ("form", "ato", "yeto", "a rare variant"),
    "mse": ("form", "mte", "mse", "a variant (?)"),
    "ḫlẖl": ("form", "ḫre", "ḫlẖl", "ḫ(re) + lẖ + l"),
    "ḫ- (1)": ("form", "ḫre", "ḫlẖl", "the element ḫ- 'meal', written ḫ(re) in the entry ḫlẖl"),
    "ḫmlol": ("form", "ḫre", "ḫlẖl", "ḫ- 'meal' + mlo + l, its ḫ- written ḫ(re) in the entry ḫlẖl"),
    "apote-lẖ": ("loan", "apote", "apote-lẖ", "apote + lẖ"),
    "pesto": ("loan", "peseto", "pesto", "a short form"),
    "at (1)": ("loan", "ant", "at (1)", "a variant"),
}
# Words of grammar and of cross-reference, taken out of a meaning's wording and out of the typists' English
# meanings before the engine makes its keys (the page, 22:15): articles, prepositions, conjunctions, auxiliaries,
# pronouns (with the determiners that stand as pronouns) and the negation; the words of cross-reference and of
# doubt the page names, with their plurals; and the hedges of the same sort as "perhaps" and "probably". No word
# of content is on it. The engine's own STOP list and its rule of three letters take the shorter ones out anyway.
FUNCTION_WORDS = frozenset("""
    a an the
    about above across after against along amid among amongst around at before behind below beneath beside besides
    between beyond by despite down during except for from in inside into near of off on onto out outside over per
    since through throughout till to toward towards under underneath until unto up upon via with within without
    and or but nor yet so if as than that because while whilst when whenever where wherever whether although though
    unless either neither both
    am is are was were be been have has had do does did will would shall should can could may might must ought
    i me my mine myself you your yours yourself yourselves he him his himself she her hers herself it its itself
    we us our ours ourselves they them their theirs themselves thou thee thy thine ye this these those who whom whose
    which what whoever whomever whatever whichever another other others each every all any some none one ones
    someone somebody something anyone anybody anything everyone everybody everything nobody nothing such
    not no
    see also variant variants form forms cf etc perhaps probably kind kinds sort sorts type types
    likely possibly maybe rather very
""".split())
CONNECTIVES = frozenset("und auch oder neben meist seltener".split())   # how the books join two forms of a headword
# A dialect mark typed into a headword cell: "(D)", "(KD)", "(K, D)", or "M.", "MK." standing as a word.
DIALECT_MARK = re.compile(r"\((?:[KDFM]+[.,\s]*)+\)|(?:(?<=[\s,;])|^)[KDFM]+\.(?=[\s,;]|$)")
DIALECTS = {"K": "kenzi", "D": "dongolawi", "F": "nobiin", "M": "nobiin"}
UNMARKED = "nobiin"
VOWELS = "aeiou"
DOT, ACUTE, TILDE = "\u0307", "\u0301", "\u0303"     # the combining dot above, acute and tilde
ENGINE = "src/cognates_rules.py"
FRAMEWORK = ("src/nubian.py", ENGINE, "src/cognates.py", "runs/nubian/known_words.json")   # what the gate is run with


def read(name):
    return json.loads((HOME / name).read_text(encoding="utf-8"))


def write(name, data):
    HOME.mkdir(parents=True, exist_ok=True)
    (HOME / name).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def share(x, n):
    return round(x / n, 4) if n else None


# ------------------------------------------------------------------------------------------ the known words

def bare(headword):
    """The letters of a headword of the lexicon: no sense number such as " (2)", no hyphen, no space."""
    return re.sub(r"[-\s]", "", re.sub(r"\s*\(\d+\)$", "", unicodedata.normalize("NFC", headword)))


def the_map():
    """(the map of 2026-11-16, its layers' lines): the layers it had when the page was set, and no later one."""
    names = tuple(l["name"] for l in T.LAYERS)
    if names[:len(MAP_LAYERS)] != MAP_LAYERS:
        raise SystemExit(f"the layers are no longer {MAP_LAYERS}")
    return T.current(upto=len(MAP_LAYERS)), [(l["name"], T.lines_of(l)) for l in T.LAYERS[:len(MAP_LAYERS)]]


def given_by(gl, lex, layers):
    """headword -> what gives it its meaning, for the dictionary words in use that have one on the map: "the
    lexicon" for a word the lexicon calls established or probable, "layer <name>" for a word a layer gives a
    meaning from a later source (the north star's count, src/themap.py). Track B counts the same words."""
    known, _, _ = D.population_of(gl, lex, fix=True)
    by = {h: "the lexicon" for h in D.translated(known, lex)}
    for name, hs in T.given_by_layers(layers, known, lex).items():
        by.update({h: f"layer {name}" for h in hs})
    return by


def the_table(path=TABLE):
    """headword -> the short wording of the public table (`meaning_in_our_words`), where it has one."""
    with open(path, encoding="utf-8", newline="") as f:
        rows = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
        return {r["headword"]: r["meaning_in_our_words"].strip() for r in rows if r["meaning_in_our_words"].strip()}


def stated_most(layers, headword):
    """The wording the layers' lines state most often for a word (at a tie the one that comes first)."""
    seen = collections.Counter(o["gloss"] for _, lines in layers for o in lines
                               if o.get("item") == headword and o["why"] == "stated" and o.get("level") in W.READ)
    return seen.most_common(1)[0][0] if seen else ""


def wording(h, lex, table, layers, by):
    """(the meaning of a word that has one on the map, where it is from), in the page's order (22:15): the public
    table's short wording where it has one; else, for a word a layer gives its meaning (`by`, given_by()), the
    wording the layers' lines state for it most often; else the lexicon's English."""
    if table.get(h):
        return table[h], "the public table"
    if by.get(h, "the lexicon") != "the lexicon":
        return stated_most(layers, h), "the layers' lines"
    return (lex[h].get("meaning") or "").strip(), "the lexicon"


def keys_of(text):
    """The engine's keys of a wording (cognates.keys, by its own rule) once FUNCTION_WORDS are taken out of it."""
    left = [w for w in re.split(r"[^a-z]+", (text or "").lower()) if w and w not in FUNCTION_WORDS]
    return frozenset(cr.cognates.keys(" ".join(left)))


def named_in(word, entry):
    """Whether a lexicon entry (its headword, English meaning and proposals) names a word: its letters as a word
    of their own, read through the lexicon's brackets and stars ("ḫ(re)" and "*ḫre" name ḫre)."""
    text = " ".join([entry.get("headword") or "", entry.get("meaning") or ""] + [p.get("proposal") or "" for p in entry.get("proposals") or []])
    text = re.sub(r"[()*]", "", unicodedata.normalize("NFC", text))
    return re.search(rf"(?<![^\W\d_]){re.escape(word)}(?![^\W\d_])", text) is not None


def by_name(h, lex, loans):
    """(whether the third reduction drops a word it names, the rule): only where the word it rests on is one the
    correspondences were built from (a form) or a loan by both readers of the Egyptian key (`loans`), and the
    lexicon's entry named in BY_NAME names it."""
    what, base, entry, how = BY_NAME[h]
    if (base in RULE_WORDS if what == "form" else base in loans) and entry in lex and named_in(base, lex[entry]):
        if what == "form":
            return True, f"by name, a form of {base}, a word the correspondences were built from: {how} (the lexicon's entry {entry})"
        return True, f"by name, built on {base}, a loan by both readers of the Egyptian key: {how} (the lexicon's entry {entry})"
    return False, f"named by the third reduction, but the lexicon's entry {entry} does not name {base} as a {'word the correspondences were built from' if what == 'form' else 'loan'}"


def reductions(left, rule, lex=None, loans=frozenset()):
    """The page's reductions of the words left, in their order: {headword: (kept, the rule)}.

    1. A word built on a word the correspondences were built from is left out: its letters begin or end with
       the letters of one of `rule` that has MIN_LETTERS letters or more.
    2. By name (the third reduction, BY_NAME, by_name()): a form of a word the correspondences were built from,
       and a word built on a loan, each only where the lexicon's entry names the word it rests on.
    3. Words built on one stem count once: the shortest headword stands for those whose letters begin with its
       letters (of two with the same letters, the first by its headword). A stem of MIN_LETTERS letters or more
       does so by the second reduction; a stem under that by the third, as the shortest headword of its family,
       which then stands more than once."""
    lex = lex or {}
    stems = sorted({bare(r) for r in rule if len(bare(r)) >= MIN_LETTERS})
    out, rest = {}, []
    for h in left:
        on = [s for s in stems if bare(h).startswith(s) or bare(h).endswith(s)]
        if on:
            out[h] = (False, "built on the rule word " + " and ".join(on))
        elif h in BY_NAME and (named := by_name(h, lex, loans))[0]:
            out[h] = (False, named[1])
        else:
            rest.append(h)
    kept = []
    for h in sorted(rest, key=lambda h: (len(bare(h)), bare(h), h)):
        stem = next((k for k in kept if bare(h).startswith(bare(k))), None)
        if stem is None:
            kept.append(h)
            out[h] = (True, "kept" if h not in BY_NAME else "kept; " + by_name(h, lex, loans)[1])
        elif len(bare(stem)) >= MIN_LETTERS:
            out[h] = (False, f"counted once, under {stem}")
        else:
            out[h] = (False, f"counted once, in the family of {stem}, a stem under three letters")
    return out


def engine_differences(done, loans):
    """Where the engine's own lists differ from the page's on the words with a meaning: the page's lists decide."""
    mine, theirs = set(RULE_WORDS), {bare(w) for w in cr.RULE_WORDS}
    engine_loans = {h for h in done if bare(h) in {bare(w) for w in cr.LOANS}}
    return {"rule_words_only_in_the_engine": sorted(theirs - mine), "rule_words_only_on_the_page": sorted(mine - theirs),
            "loans_only_in_the_engine": sorted(engine_loans - loans), "loans_only_on_the_page": sorted(loans - engine_loans)}


def words_of(pairs):
    """(headword, meaning) pairs as the engine's words (form, the meaning's keys, meaning), and those without a
    key, which the engine cannot compare (as its own gold_words leaves them out). The keys are keys_of()'s."""
    words, left = [], []
    for h, meaning in pairs:
        keys = keys_of(meaning)
        if keys:
            words.append((h, keys, meaning))
        else:
            left.append(h)
    return words, left


def loans_both():
    """The headwords both readers of the Egyptian key take for loans into Meroitic."""
    return {e["headword"] for e in map(json.loads, LOANS.read_text(encoding="utf-8").splitlines()) if e.get("both_into_meroitic")}


# What each reduction writes as its rule, at its start: the counts of the public list.
REDUCED = {"built_on_a_rule_word": "built on the rule word", "a_form_of_a_rule_word_by_name": "by name, a form of",
           "built_on_a_loan_by_name": "by name, built on", "counted_under_a_shorter_stem": "counted once, under",
           "counted_once_in_a_family_under_three_letters": "counted once, in the family of"}


def word_list():
    """(the public list, the local list): the dictionary words in use that have a meaning on the map, each kept
    or dropped by the page's rules, and the kept ones with their meaning. Stops if the page's counts are not met."""
    lex = W.lexicon()
    gl, layers = the_map()
    by = given_by(gl, lex, layers)
    both = loans_both()
    loans = set(by) & both
    rule = {h for h in set(by) - loans if bare(h) in RULE_WORDS}
    left = sorted(set(by) - loans - rule)
    counts = {"with_a_meaning": len(by), "loans_by_both_readers": len(loans), "rule_words": len(rule), "left": len(left)}
    if counts != COUNTS:
        raise SystemExit(f"the page counts {COUNTS}, the map gives {counts}: nothing is written")
    verdict = {h: (False, "a loan into Meroitic by both readers of the Egyptian key") for h in loans}
    verdict |= {h: (False, "a word the correspondences were built from") for h in rule}
    verdict |= reductions(left, rule, lex, both)
    kept = sorted(h for h, (k, _) in verdict.items() if k)
    table = the_table()
    said = {h: wording(h, lex, table, layers, by) for h in by}
    words, no_key = words_of([(h, said[h][0]) for h in kept])
    rows = cr.load_nes()
    if len(rows) != GATE["short_rows"]:
        raise SystemExit(f"the short lists have {len(rows)} rows, the page counts {GATE['short_rows']}")
    with_a_row = sum(1 for _, n, _ in cr.comparanda(words, rows) if n)
    counts |= {k: sum(r.startswith(start) for _, r in verdict.values()) for k, start in REDUCED.items()}
    counts |= {"kept": len(kept), "kept_by_the_lexicon": sum(by[h] == "the lexicon" for h in kept),
               "kept_by_a_layer": sum(by[h] != "the lexicon" for h in kept),
               "kept_wording_from": dict(collections.Counter(said[h][1] for h in kept).most_common()),
               "kept_without_a_key": len(no_key), "kept_with_a_same_meaning_row_in_the_short_lists": with_a_row}
    public = {"page": f"{PAGE}, section 2, gate A1", "map_layers": list(MAP_LAYERS), "counts": counts,
              "engine": engine_differences(set(by), loans), "function_words": sorted(FUNCTION_WORDS),
              "words": [{"headword": h, "kind": lex[h].get("kind") or "", "meaning_from": by[h], "wording_from": said[h][1],
                         "kept": verdict[h][0], "rule": verdict[h][1]} for h in sorted(by)]}
    local = {"words": [{"headword": h, "kind": lex[h].get("kind") or "", "meaning": said[h][0], "wording_from": said[h][1],
                        "keys": sorted(keys_of(said[h][0])), "meaning_from": by[h], "lexicon_status": lex[h].get("status") or "",
                        "lexicon_meaning": lex[h].get("meaning") or ""} for h in kept]}
    return public, local


def words():
    public, local = word_list()
    LIST.parent.mkdir(parents=True, exist_ok=True)
    LIST.write_text(json.dumps(public, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    write("known_words_local.json", local)
    print("wrote", LIST.name, public["counts"])
    print("the engine's lists against the page's:", public["engine"])


def known_words():
    """The kept words of the committed list with the meanings of the local one, as the engine's words."""
    kept = [w["headword"] for w in json.loads(LIST.read_text(encoding="utf-8"))["words"] if w["kept"]]
    meaning = {w["headword"]: w["meaning"] for w in read("known_words_local.json")["words"]}
    if set(kept) != set(meaning):
        raise SystemExit("known_words_local.json is not the list of runs/nubian/known_words.json: run `words` and compare")
    return words_of([(h, meaning[h]) for h in kept])


# ------------------------------------------------------------------------------------------- the typed pages

def name_of(book, index):
    return f"{book}{index:04d}"


def read_page(path, book, index):
    """(the rows of one typed file, what fails): the header, one row a line with every cell, the book and the
    index of the file in each row, `n` running from 1, a headword in each row, and the count line agreeing with
    the rows. A file that fails has no rows here: it is not repaired."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None, ["the file is not UTF-8"]
    lines = [l[:-1] if l.endswith("\r") else l for l in text.lstrip("\ufeff").split("\n")]
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines or lines[0].split("\t") != HEADER:
        return None, ["the first line is not the header"]
    fails, rows, blank = [], [], False
    last = lines[-1].rstrip() if len(lines) > 1 else ""
    count = COUNT.fullmatch(last)
    if not count:
        fails.append("the last line is not the count line")
    for k, line in enumerate(lines[1:-1] if count or last.startswith("#") else lines[1:], 2):
        if line == "# blank":
            blank = True
        elif line.startswith("#"):
            fails.append(f"line {k} is a comment the brief does not have")
        elif len(line.split("\t")) != len(HEADER):
            fails.append(f"line {k} has {len(line.split(chr(9)))} cells, not {len(HEADER)}")
        else:
            rows.append(dict(zip(HEADER, (c.strip() for c in line.split("\t")))))
    for k, r in enumerate(rows, 1):
        if r["n"] != str(k):
            fails.append(f"n does not run from 1: row {k} has n={r['n']}")
            break
    other = [k for k, r in enumerate(rows, 1) if r["book"] != book or r["index"].lstrip("0") != str(index)]
    if other:
        fails.append(f"row {other[0]} names another book or index")
    empty = [k for k, r in enumerate(rows, 1) if not r["headword"]]
    if empty:
        fails.append(f"row {empty[0]} has no headword")
    if blank and rows:
        fails.append("`# blank` in a page with rows")
    if count:
        typed = (sum(not r["parent"] for r in rows), sum(bool(r["parent"]) for r in rows))
        if typed != (int(count[1]), int(count[2])):
            fails.append(f"the count line says entries={count[1]} subrows={count[2]}, the rows are entries={typed[0]} subrows={typed[1]}")
    return (None, fails) if fails else (rows, [])


def indexes(book, books=None):
    b = (books or BOOKS)[book]
    return range(b["first"], b["last"] + 1)


def merge_of(folder, books=None):
    """(the rows of dictionary.tsv, the report) from the files of the first typing. A sub-row of a page that
    begins inside an entry (`parent` = "(continued)") gets the headword of the last entry before that page: of
    the page before, or of an earlier one when the pages between hold no entry. Across a page that is missing
    or fails a check it is not attached. The printed page is counted from the file's index. The report lists every
    loan mark the entries carry and every part of a dialect cell that is no dialect mark of the books, with their
    numbers: any loan mark drops an entry from the gate, so a mark that means none ("-", "none") shows here first."""
    books = books or BOOKS
    out, fails, missing, loose = [], {}, [], []
    marks, odd = collections.Counter(), collections.Counter()
    by_book = {}
    wanted = {name_of(b, i) + ".tsv" for b in books for i in indexes(b, books)}
    extra = sorted(p.name for p in folder.iterdir() if p.name not in wanted) if folder.is_dir() else []
    for book in books:
        c = collections.Counter()
        last = None                                   # the last entry so far, None once the run of pages is broken
        for index in indexes(book, books):
            name, path = name_of(book, index), folder / (name_of(book, index) + ".tsv")
            if not path.exists():
                missing.append(name)
                last = None
                continue
            rows, why = read_page(path, book, index)
            if rows is None:
                fails[name] = why
                last = None
                continue
            c["pages"] += 1
            c["pages_without_a_row"] += not rows
            before = last
            for r in rows:
                parent = r["parent"]
                if parent == CONTINUED:
                    if before is None:
                        loose.append(f"{name} row {r['n']}")
                    else:
                        parent = before
                    c["continued"] += 1
                elif not parent:
                    last = r["headword"]
                c["subrows" if r["parent"] else "entries"] += 1
                c["marked_as_loans"] += bool(r["loan"]) and not r["parent"]
                marks.update([r["loan"]] if r["loan"] else [])
                odd.update(languages(r["dialect"])[1].split())
                c["unsure"] += "unsure" in r["note"]
                out.append({**{k: r[k] for k in COLUMNS if k in r}, "page": str(index - books[book]["page"]), "parent": parent})
        by_book[book] = {k: c[k] for k in ("pages", "pages_without_a_row", "entries", "subrows", "marked_as_loans", "continued", "unsure")}
    report = {"pages": {"expected": len(wanted), "merged": sum(b["pages"] for b in by_book.values()), "failed": len(fails), "missing": len(missing)},
              "entries": sum(b["entries"] for b in by_book.values()), "subrows": sum(b["subrows"] for b in by_book.values()),
              "by_book": by_book, "continued_not_attached": loose, "failed": fails, "missing": missing, "other_files": extra,
              "loan_marks": dict(marks.most_common()), "dialect_parts_not_of_the_books": dict(odd.most_common())}
    return out, report


def write_dictionary(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join("\t".join(r) + "\n" for r in [COLUMNS] + [[row[k] for k in COLUMNS] for row in rows]), encoding="utf-8")


def read_dictionary(path):
    lines = path.read_text(encoding="utf-8").split("\n")
    if lines[0].split("\t") != COLUMNS:
        raise SystemExit(f"{path.name} does not begin with the header of `merge`")
    return [dict(zip(COLUMNS, l.split("\t"))) for l in lines[1:] if l]


def merge():
    rows, report = merge_of(HOME / "typed")
    write_dictionary(rows, HOME / "dictionary.tsv")
    write("merge_report.json", report)
    print({k: report[k] for k in ("pages", "entries", "subrows")}, "continued, not attached:", len(report["continued_not_attached"]))
    print("  loan marks (each drops its entry from the gate):", report["loan_marks"])
    print("  parts of a dialect cell that are no dialect mark:", report["dialect_parts_not_of_the_books"])
    for name, why in report["failed"].items():
        print("  failed", name, "-", "; ".join(why))
    if report["missing"]:
        print("  missing:", ", ".join(report["missing"]))
    if report["other_files"]:
        print("  not a page's file:", ", ".join(report["other_files"]))


# ------------------------------------------------------------------------------------------ the typing's bar

def letters(headword):
    """Letters as the typing's bar compares them: lower case, every combining mark on a vowel set aside (the
    macron of length, the acute of the accent, any other). A mark on a consonant stays (it makes another
    consonant), and so do hyphens and spaces; but a mark the books print in one way and the typists render in
    two is one mark: a g with any mark is ǵ (the one marked g of either book), an n with a tilde or an acute is ń
    (the palatal nasal, Reinisch's ñ and Lepsius's ń). Lepsius's ṅ, the velar nasal, stays apart."""
    signs = []                                        # [a letter, its marks]
    for ch in unicodedata.normalize("NFD", headword.strip().lower()):
        if unicodedata.combining(ch) and signs:
            signs[-1][1].append(ch)
        else:
            signs.append([ch, []])
    out = []
    for base, marks in signs:
        if base in VOWELS:
            marks = []
        elif base == "g" and marks:
            marks = [ACUTE]
        elif base == "n" and marks and set(marks) <= {TILDE, ACUTE}:
            marks = [ACUTE]
        out.append(base + "".join(marks))
    return unicodedata.normalize("NFC", "".join(out))


def german(text):
    """A German meaning as the bar compares it: composed letters, lower case, one space between words, and the
    long s as s and ß as ss (ſs, ſ and ß are a typing convention, not a reading)."""
    return " ".join(unicodedata.normalize("NFC", text).lower().replace("ſ", "s").replace("ß", "ss").split())


def likeness(a, b):
    """The likeness of two German meanings: difflib's ratio on german() of each (without its shortcut for long
    texts, which leaves common letters out of the comparison)."""
    return difflib.SequenceMatcher(None, german(a), german(b), autojunk=False).ratio()


def sounds(headword, book):
    return cr.segments(spelling(headword, book))


def in_both(first, second, key):
    """How many of the first reading's rows stand in the second by `key`, each row of the second used once."""
    a, b = collections.Counter(map(key, first)), collections.Counter(map(key, second))
    return sum((a & b).values())


def compare(first, second, book):
    """One page's rows of one sort (entries, or sub-rows) in the two readings. A row of the first reading is
    found when a row of the second has the same letters() in its headword, the first form of its cell
    (headword_of()); where several share them, the pairs are made by the likeness of their German meanings, the
    likest first. Found rows carry the same meaning at TYPING's likeness or more."""
    theirs = collections.defaultdict(list)
    for r in second:
        theirs[letters(headword_of(r["headword"]))].append(r)
    mine = collections.defaultdict(list)
    for r in first:
        mine[letters(headword_of(r["headword"]))].append(r)
    found = same = 0
    not_found, only_second, other_meaning = [], [], []
    for key in list(mine) + [k for k in theirs if k not in mine]:
        rows, others = mine.get(key, []), theirs.get(key, [])
        cands = sorted(((-likeness(a["gloss_de"], b["gloss_de"]), i, j) for i, a in enumerate(rows) for j, b in enumerate(others)))
        used_a, used_b = set(), set()
        for neg, i, j in cands:
            if i in used_a or j in used_b:
                continue
            used_a.add(i)
            used_b.add(j)
            found += 1
            if -neg >= TYPING["likeness"]:
                same += 1
            else:
                other_meaning.append({"headword": rows[i]["headword"], "first": rows[i]["gloss_de"], "second": others[j]["gloss_de"], "likeness": round(-neg, 3)})
        not_found += [r["headword"] for i, r in enumerate(rows) if i not in used_a]
        only_second += [r["headword"] for j, r in enumerate(others) if j not in used_b]
    nfc = lambda r: unicodedata.normalize("NFC", headword_of(r["headword"]))     # noqa: E731
    return {"first": len(first), "second": len(second), "found": found, "same_meaning": same, "mark_for_mark": in_both(first, second, nfc),
            "same_sounds": in_both(first, second, lambda r: sounds(headword_of(r["headword"]), book)),
            "not_found": not_found, "only_in_the_second": only_second, "other_meaning": other_meaning}


NUMBERS = ("first", "second", "found", "same_meaning", "mark_for_mark", "same_sounds")


def total(parts):
    """Counts added over pages, with the shares: found and mark for mark and same sounds of the first reading's
    rows, the same meaning of the found ones."""
    t = {k: sum(p[k] for p in parts) for k in NUMBERS}
    return t | {"found_share": share(t["found"], t["first"]), "same_meaning_share": share(t["same_meaning"], t["found"]),
                "mark_for_mark_share": share(t["mark_for_mark"], t["first"]), "same_sounds_share": share(t["same_sounds"], t["first"])}


def typing_verdict(entries, not_compared):
    """The bar is on the entries' headwords of every page typed twice: met, missed, or not decided while a
    page of either reading is missing or fails a check."""
    if not_compared or not entries["first"]:
        return "not decided"
    found = entries["found"] >= TYPING["found"] * entries["first"] - 1e-9
    same = entries["same_meaning"] >= TYPING["same_meaning"] * entries["found"] - 1e-9
    return "met" if found and same else "missed"


def agree_of(typed, typed2, second=None):
    second = second or SECOND
    pages, out = {}, {}
    for book, idx in second.items():
        for index in idx:
            name = name_of(book, index)
            both = []
            for folder in (typed, typed2):
                path = folder / (name + ".tsv")
                both.append(read_page(path, book, index) if path.exists() else (None, ["the file is missing"]))
            if both[0][0] is None or both[1][0] is None:
                out[name] = {"first": both[0][1], "second": both[1][1]}
                continue
            split = [([r for r in rows if not r["parent"]], [r for r in rows if r["parent"]]) for rows, _ in both]
            pages[name] = {"entries": compare(split[0][0], split[1][0], book), "subrows": compare(split[0][1], split[1][1], book)}
    entries = total([p["entries"] for p in pages.values()])
    return {"bars": TYPING, "pages": {"drawn": sum(map(len, second.values())), "compared": len(pages), "not_compared": len(out)},
            "entries": entries, "subrows": total([p["subrows"] for p in pages.values()]),
            "by_book": {b: {"entries": total([p["entries"] for n, p in pages.items() if n[0] == b]),
                            "subrows": total([p["subrows"] for n, p in pages.items() if n[0] == b])} for b in second},
            "verdict": typing_verdict(entries, out), "not_compared": out, "by_page": pages}


def agree():
    res = agree_of(HOME / "typed", HOME / "typed2")
    write("agree.json", res)
    print("the typing's bar:", res["verdict"], res["pages"])
    for sort in ("entries", "subrows"):
        print(f"  {sort}:", res[sort])
    for name, why in res["not_compared"].items():
        print("  not compared", name, why)


# ---------------------------------------------------------------------------------------------- the gate

def spelling(headword, book=""):
    """A typed headword in letters the engine reads as the book means them: ṅ as ŋ, ń as ɲ (the engine reads ñ
    itself), a g with any mark as ɟ, and Reinisch's q as c. Everything else is left to the engine."""
    out = []
    for ch in unicodedata.normalize("NFD", headword.lower()):
        if unicodedata.combining(ch) and out and out[-1] == "g":
            out[-1] = "ɟ"
        elif unicodedata.combining(ch) and out and out[-1] == "n" and ch in (DOT, ACUTE):
            out[-1] = "ŋ" if ch == DOT else "ɲ"
        else:
            out.append("c" if ch == "q" and book == "R" else ch)
    return unicodedata.normalize("NFC", "".join(out))


def forms(headword):
    """The forms of a headword cell, the headword first ("Bīr, bírri" -> Bīr, bírri). The cell is split at
    commas, semicolons and slashes, at the words the books join two forms with (CONNECTIVES: "Kúsu und kússu",
    "Dalū, auch dallū"), at a dialect mark typed into it ("Hilgē (D), halgē (K)", "Kāše M. kašere D."), and
    before a form in round brackets after a space ("Doin (doṅ?)"). Brackets inside a word stay: the engine reads
    them as letters that may stand or not. A part without a letter is no form."""
    text = DIALECT_MARK.sub(",", unicodedata.normalize("NFC", headword))
    text = re.sub(r"\s\(([^()]*)\)", r", \1", text)
    out = []
    for chunk in re.split(r"[,;/]", text):
        run = []
        for tok in chunk.split() + [""]:
            if tok and tok.lower() not in CONNECTIVES:
                run.append(tok)
            elif run:
                out.append(" ".join(run))
                run = []
    return [f for f in out if any(ch.isalpha() for ch in f)] or [headword.strip()]


def headword_of(cell):
    """The headword of a headword cell: its first form."""
    return forms(cell)[0]


def variants_of(headword, book):
    """What the engine scores of a headword cell: the engine's own variants (cognates_rules.variants) of each of
    its forms, read as the book means its letters (spelling()). A later form that begins or ends with a hyphen
    where the first does not ("Mūr, -kā", "jom-bay, -bai") is an ending or a shortened form that only the print
    completes: it is not scored."""
    fs = forms(headword)
    affix = lambda f: f.startswith("-") or f.endswith("-")         # noqa: E731
    out = []
    for n, f in enumerate(fs):
        if n and affix(f) and not affix(fs[0]):
            continue
        for v in cr.variants(spelling(f, book)):
            s = cr.segments(v)
            if s and (v, s) not in out:
                out.append((v, s))
    return tuple(out)


def languages(dialect):
    """(the engine's languages of a dialect cell, what in it is no dialect mark of the books). The cell is split
    at commas, semicolons, spaces, stops and brackets ("K, DF, M", "KDFM", "K. D."); a part made only of K, D, F
    and M gives a language for each letter, any other part ("Derr", a place) none. No language: the row has no
    dialect mark of the books."""
    langs, other = [], []
    for part in re.split(r"[\s,;.()]+", dialect.upper()):
        if part and set(part) <= set(DIALECTS):
            langs += [DIALECTS[ch] for ch in part]
        elif part:
            other.append(part)
    return tuple(dict.fromkeys(langs)), " ".join(other)


def engine_rows(rows):
    """(the rows of dictionary.tsv as rows the engine scores, the counts). A sub-row stands in the entry its
    `parent` names (the whole cell, or its first form), the nearest one before it on its page; where the page
    has none of that headword before it (a page that begins inside an entry, a parent typed otherwise), in the
    entry right before it. It takes that entry's loan mark, and its dialect where it has none of its own. Left
    out: an entry with any loan mark, with its sub-rows; a row without an English meaning; a row whose headword
    has no letter the engine reads. A row's keys are keys_of() its English meaning; a row without a dialect mark
    of the books is UNMARKED's."""
    out, c = [], collections.Counter()
    named, before = {}, {}
    odd, unread = collections.Counter(), collections.Counter()
    for r in rows:
        book = r["book"]
        if r["parent"]:
            own = named.get((book, r["page"], r["parent"])) or named.get((book, r["page"], headword_of(r["parent"])))
            if own is None:
                own = before.get(book)
                c["subrows_under_the_entry_before"] += 1
        else:
            own = named[(book, r["page"], r["headword"])] = named[(book, r["page"], headword_of(r["headword"]))] = before[book] = r
        c["subrows_read" if r["parent"] else "entries_read"] += 1
        if r["loan"] or (own is not None and own["loan"]):
            c["subrows_of_loans_left_out" if r["parent"] else "loans_left_out"] += 1
            continue
        if not r["gloss_en"]:
            c["without_an_english_meaning"] += 1
            continue
        vs = variants_of(r["headword"], book)
        if not vs:
            c["without_a_letter_the_engine_reads"] += 1
            continue
        unread.update(ch for ch in unicodedata.normalize("NFD", spelling(r["headword"], book)) if ch.isalpha() and ch not in cr.SEG)
        dialect = r["dialect"] or (own["dialect"] if own is not None else "")
        langs, other = languages(dialect)
        if other:
            odd[dialect] += 1
        keys = keys_of(r["gloss_en"])
        c["without_a_dialect"] += not langs
        c["without_a_key"] += not keys
        c["compared"] += 1
        for lang in langs or (UNMARKED,):
            out.append(cr.Row(lang, r["headword"], r["gloss_en"], keys, BOOKS[book]["list"], dialect, vs))
    counts = {k: c[k] for k in ("entries_read", "subrows_read", "loans_left_out", "subrows_of_loans_left_out", "without_an_english_meaning",
                                "without_a_letter_the_engine_reads", "compared", "without_a_dialect", "without_a_key",
                                "subrows_under_the_entry_before")}
    counts |= {"rows": len(out), "rows_by_list": dict(collections.Counter(r.dataset for r in out)),
               "rows_by_language": dict(collections.Counter(r.lang for r in out)),
               "dialect_marks_not_of_the_books": dict(odd), "letters_the_engine_does_not_read": dict(unread)}
    return out, counts


def verdict(n, p):
    """The bar of gate A1: p under GATE's on at least GATE's number of words that have a row of the same
    meaning; with fewer words the test is too small to decide."""
    if n < GATE["words"]:
        return "too small to decide"
    return "met" if p < GATE["p"] else "missed"


def measures(words, rows, S, sims, seed):
    """The engine's measures of one scorer on one set of rows: its shuffle test, its precision at the top (one
    row, ten rows) and the ranks of the best same-meaning row. (the numbers, the shuffle test as the engine
    gives it)"""
    t = cr.shuffle_test(words, rows, S, sims, seed)
    out = {"shuffle": {k: t[k] for k in ("n", "of", "stat", "ge", "sims", "p")} | {"seed": seed}}
    if t["n"]:
        for k in (1, 10):
            if len(rows) >= k:
                top = cr.top_test(words, rows, S, sims, seed, k)
                out[f"top{k}"] = {"precision": top["prec"], "chance": top["chance"], "ge": top["ge"], "p": top["p"], "words_with_a_hit": len(top["hits"])}
        median, best, top10 = cr.rank_stats(cr.ranks(words, rows, S))
        out["ranks"] = {"median": median, "best": best, "in_the_top_10": top10, "of_rows": len(rows)}
    return out, t


def gate_of(words, short, dictionary, sims=None, seed=None):
    """Gate A1 on the engine's words, the rows of the short lists and the rows of the two dictionaries: the
    engine's shuffle test with its score by the correspondences, on all rows; the verdict; and beside it, not
    part of the bar, the same on the dictionaries alone, the precision at the top, the ranks, and all of it with
    raw similarity. Every word is shuffled, as in the engine's own run; `n` counts those that have a row of the
    same meaning. `pairs` lists, for each word that has one, its best row of the same meaning."""
    sims, seed = sims or GATE["sims"], GATE["seed"] if seed is None else seed
    rows = short + dictionary
    scores = {"rule": cr.matrix(words, rows, cr.rule_score), "raw": cr.matrix(words, rows, cr.raw_score)}
    out = {"words": len(words), "rows": {"short_lists": len(short), "dictionaries": len(dictionary)}, "all": {}, "dictionaries": {}}
    for name, S in scores.items():
        out["all"][name], t = measures(words, rows, S, sims, seed)
        alone = {f: v[len(short):] for f, v in S.items()}
        out["dictionaries"][name], _ = measures(words, dictionary, alone, sims, seed)
        if name == "rule":
            match = t["match"]
    bar = out["all"]["rule"]["shuffle"]
    out["verdict"] = verdict(bar["n"], bar["p"])
    out["pairs"] = []
    for (f, _, meaning), mt in zip(words, match):
        if mt:
            i = max(mt, key=lambda i: scores["rule"][f][i])
            score, variant, _, used = cr.explain(f, rows[i])
            out["pairs"].append({"headword": f, "meaning": meaning, "rows_of_the_same_meaning": len(mt), "of_them_in_the_dictionaries": sum(i >= len(short) for i in mt),
                                 "best": {"language": rows[i].lang, "list": rows[i].dataset, "form": rows[i].form, "read_as": variant, "gloss": rows[i].gloss,
                                          "score": round(score, 4), "raw": round(scores["raw"][f][i], 4), "correspondences": used}})
    out["pairs"].sort(key=lambda x: -x["best"]["score"])
    return out


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True).stdout.strip()


def not_as_committed(paths=FRAMEWORK):
    """The files whose text is not the one of the commit the checkout stands on (git is only read)."""
    return [p for p in paths if not git("rev-parse", f"HEAD:{p}") or git("rev-parse", f"HEAD:{p}") != git("hash-object", p)]


def ready():
    """What must hold before the gate runs, each as the page sets it; the first that does not hold stops it."""
    if (HOME / "gate.json").exists():
        raise SystemExit("gate.json is written: the gate is run once, and its result stands")
    changed = not_as_committed()
    if changed:
        raise SystemExit(f"not as committed: {', '.join(changed)}. The script is committed before it is run on the typed pages")
    if not git("hash-object", ENGINE) or git("hash-object", ENGINE) != git("rev-parse", f"{GATE['engine']}:{ENGINE}"):
        raise SystemExit(f"{ENGINE} is not the file of {GATE['engine']}, the engine the page names")
    for name in ("merge_report.json", "dictionary.tsv", "agree.json", "known_words_local.json"):
        if not (HOME / name).exists():
            raise SystemExit(f"data/sources/nubian/{name} is missing: run `words`, `merge` and `agree` first")
    pages = read("merge_report.json")["pages"]
    if pages["failed"] or pages["missing"]:
        raise SystemExit(f"{pages['failed']} pages fail a check and {pages['missing']} are missing (merge_report.json): the gate is for the two whole dictionaries")
    if read("agree.json")["verdict"] != "met":
        raise SystemExit(f"the typing's bar is {read('agree.json')['verdict']} (agree.json): by the page the differences are settled before this test")


def gate():
    ready()
    words, no_key = known_words()
    short = cr.load_nes()
    if len(short) != GATE["short_rows"]:
        raise SystemExit(f"the short lists have {len(short)} rows, the page counts {GATE['short_rows']}")
    dictionary, counts = engine_rows(read_dictionary(HOME / "dictionary.tsv"))
    res = gate_of(words, short, dictionary)
    res = {"commit": git("rev-parse", "HEAD"), "bar": GATE, "typing": read("agree.json")["verdict"],
           "known_words": {"kept": len(words) + len(no_key), "compared": len(words), "without_a_key": no_key},
           "dictionary": counts} | res
    write("gate.json", res)
    bar = res["all"]["rule"]["shuffle"]
    print(f"gate A1: {res['verdict']}. {bar['n']} of {bar['of']} words have a row of the same meaning; mean best score {bar['stat']:.3f}; "
          f"shuffled >= real in {bar['ge']} of {bar['sims']} (p = {bar['p']:.4f}); commit {res['commit'][:7]}")
    alone = res["dictionaries"]["rule"]["shuffle"]
    print(f"  the two dictionaries alone ({res['rows']['dictionaries']} rows): {alone['n']} words, p = {alone['p']:.4f}")
    print(f"  raw similarity, all rows: p = {res['all']['raw']['shuffle']['p']:.4f}")


# ------------------------------------------------------------------------------------------ the public figures

def figures():
    """What the page reports of track A, from the list and the local results: counts only, no headword and no
    meaning. A part that is not run yet is null."""
    def part(name, keep):
        return keep(read(name)) if (HOME / name).exists() else None

    def typing(a):
        return {k: a[k] for k in ("bars", "pages", "entries", "subrows", "by_book", "verdict")}

    def a1(g):
        return {k: g[k] for k in ("commit", "bar", "typing", "words", "rows", "all", "dictionaries", "verdict")} \
            | {"known_words": {k: (len(v) if isinstance(v, list) else v) for k, v in g["known_words"].items()},
               "dictionary": {k: v for k, v in g["dictionary"].items() if not isinstance(v, dict)}
               | {k: v for k, v in g["dictionary"].items() if k in ("rows_by_list", "rows_by_language")}}

    return {"page": f"{PAGE}, section 2", "known_words": json.loads(LIST.read_text(encoding="utf-8"))["counts"],
            "typed": part("merge_report.json", lambda m: {k: m[k] for k in ("pages", "entries", "subrows", "by_book")}
                          | {"continued_not_attached": len(m["continued_not_attached"]), "other_files": len(m["other_files"])}),
            "typed_twice": part("agree.json", typing), "gate_a1": part("gate.json", a1)}


def public():
    figs = figures()
    PUBLIC.write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", PUBLIC.name, {k: (v is not None) for k, v in figs.items() if k != "page"})


COMMANDS = {"words": words, "merge": merge, "agree": agree, "gate": gate, "public": public}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        raise SystemExit(__doc__)
    COMMANDS[sys.argv[1]]()
