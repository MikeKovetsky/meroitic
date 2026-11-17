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

The rules and the bars are the page's. What the page leaves open is decided here, before any typed page was seen:

1. The meaning of a known word is the one the map has: the lexicon's for a word the lexicon calls established
   or probable, and for a word a layer gives a meaning the wording the layers' lines state for it most often.
2. A file that fails a check is listed and left out of dictionary.tsv; nothing in it is repaired. The gate does
   not run while a page is missing or fails, or while the typing's bar is not counted as met.
3. The typing's bar sets aside, in a headword: every mark on a vowel (macron, acute and any other combining
   mark) and the case of the letters. It does not set aside a mark on a consonant (š ž ñ ṅ ǵ ń ǧ: there the mark
   makes another consonant), a hyphen or a space.
4. For the engine a typed headword is read as the two books define their letters (Reinisch p. 1-2, Lepsius
   p. 5-7): ṅ is the velar nasal, ñ and ń the palatal nasal, a g with any mark the palatal stop that Reinisch
   writes j, and Reinisch's q the palatal he pairs with j. The engine reads the rest itself: length and accent
   dropped, š, ž, j, y, z.
5. K is Kenzi, D Dongola, F and M Nobiin; an entry with several marks is a row for each of those languages. An
   entry without a mark is one row, as Nobiin: the engine scores the three by the same correspondences, so the
   choice cannot change the test, and one row keeps such an entry from counting three times at the top. A
   sub-row has the dialect and the loan mark of the entry it stands in.
"""
import collections
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
DIALECTS = {"K": "kenzi", "D": "dongolawi", "F": "nobiin", "M": "nobiin"}
UNMARKED = "nobiin"
VOWELS = "aeiou"
DOT, ACUTE = "\u0307", "\u0301"                      # the combining dot above and acute
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


def reductions(left, rule):
    """The page's two reductions on the words left, in their order: {headword: (kept, the rule)}.

    1. A word built on a word the correspondences were built from is left out: its letters begin or end with
       the letters of one of `rule` that has MIN_LETTERS letters or more.
    2. Words built on one stem count once: the shortest headword of MIN_LETTERS letters or more stands for those
       whose letters begin with its letters (of two with the same letters, the first by its headword)."""
    stems = sorted({bare(r) for r in rule if len(bare(r)) >= MIN_LETTERS})
    out, rest = {}, []
    for h in left:
        on = [s for s in stems if bare(h).startswith(s) or bare(h).endswith(s)]
        if on:
            out[h] = (False, "built on the rule word " + " and ".join(on))
        else:
            rest.append(h)
    kept = []
    for h in sorted(rest, key=lambda h: (len(bare(h)), bare(h), h)):
        stem = next((k for k in kept if len(bare(k)) >= MIN_LETTERS and bare(h).startswith(bare(k))), None)
        if stem is None:
            kept.append(h)
        out[h] = (True, "kept") if stem is None else (False, f"counted once, under {stem}")
    return out


def stated_most(layers, headword):
    """The wording the layers' lines state most often for a word (at a tie the one that comes first)."""
    seen = collections.Counter(o["gloss"] for _, lines in layers for o in lines
                               if o.get("item") == headword and o["why"] == "stated" and o.get("level") in W.READ)
    return seen.most_common(1)[0][0] if seen else ""


def engine_differences(done, loans):
    """Where the engine's own lists differ from the page's on the words with a meaning: the page's lists decide."""
    mine, theirs = set(RULE_WORDS), {bare(w) for w in cr.RULE_WORDS}
    engine_loans = {h for h in done if bare(h) in {bare(w) for w in cr.LOANS}}
    return {"rule_words_only_in_the_engine": sorted(theirs - mine), "rule_words_only_on_the_page": sorted(mine - theirs),
            "loans_only_in_the_engine": sorted(engine_loans - loans), "loans_only_on_the_page": sorted(loans - engine_loans)}


def words_of(pairs):
    """(headword, meaning) pairs as the engine's words (form, the meaning's keys, meaning), and those without a
    key, which the engine cannot compare (as its own gold_words leaves them out)."""
    words, left = [], []
    for h, meaning in pairs:
        keys = frozenset(cr.cognates.keys(meaning or ""))
        if keys:
            words.append((h, keys, meaning))
        else:
            left.append(h)
    return words, left


def word_list():
    """(the public list, the local list): the dictionary words in use that have a meaning on the map, each kept
    or dropped by the page's rules, and the kept ones with their meaning. Stops if the page's counts are not met."""
    lex = W.lexicon()
    gl, layers = the_map()
    known, _, _ = D.population_of(gl, lex, fix=True)
    by = {h: "the lexicon" for h in D.translated(known, lex)}
    for name, hs in T.given_by_layers(layers, known, lex).items():
        by.update({h: f"layer {name}" for h in hs})
    both = {e["headword"] for e in map(json.loads, LOANS.read_text(encoding="utf-8").splitlines()) if e.get("both_into_meroitic")}
    loans = set(by) & both
    rule = {h for h in set(by) - loans if bare(h) in RULE_WORDS}
    left = sorted(set(by) - loans - rule)
    counts = {"with_a_meaning": len(by), "loans_by_both_readers": len(loans), "rule_words": len(rule), "left": len(left)}
    if counts != COUNTS:
        raise SystemExit(f"the page counts {COUNTS}, the map gives {counts}: nothing is written")
    verdict = {h: (False, "a loan into Meroitic by both readers of the Egyptian key") for h in loans}
    verdict |= {h: (False, "a word the correspondences were built from") for h in rule}
    verdict |= reductions(left, rule)
    kept = sorted(h for h, (k, _) in verdict.items() if k)
    meaning = {h: lex[h].get("meaning") or "" if by[h] == "the lexicon" else stated_most(layers, h) for h in kept}
    words, no_key = words_of([(h, meaning[h]) for h in kept])
    rows = cr.load_nes()
    if len(rows) != GATE["short_rows"]:
        raise SystemExit(f"the short lists have {len(rows)} rows, the page counts {GATE['short_rows']}")
    with_a_row = sum(1 for _, n, _ in cr.comparanda(words, rows) if n)
    counts |= {"built_on_a_rule_word": sum(r.startswith("built on") for _, r in verdict.values()),
               "counted_under_a_shorter_stem": sum(r.startswith("counted once") for _, r in verdict.values()),
               "kept": len(kept), "kept_by_the_lexicon": sum(by[h] == "the lexicon" for h in kept),
               "kept_by_a_layer": sum(by[h] != "the lexicon" for h in kept), "kept_without_a_key": len(no_key),
               "kept_with_a_same_meaning_row_in_the_short_lists": with_a_row}
    public = {"page": f"{PAGE}, section 2, gate A1", "map_layers": list(MAP_LAYERS), "counts": counts,
              "engine": engine_differences(set(by), loans),
              "words": [{"headword": h, "kind": lex[h].get("kind") or "", "meaning_from": by[h], "kept": verdict[h][0], "rule": verdict[h][1]}
                        for h in sorted(by)]}
    local = {"words": [{"headword": h, "kind": lex[h].get("kind") or "", "meaning": meaning[h], "meaning_from": by[h],
                        "lexicon_status": lex[h].get("status") or "", "lexicon_meaning": lex[h].get("meaning") or ""} for h in kept]}
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
    or fails a check it is not attached. The printed page is counted from the file's index."""
    books = books or BOOKS
    out, fails, missing, loose = [], {}, [], []
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
                c["unsure"] += "unsure" in r["note"]
                out.append({**{k: r[k] for k in COLUMNS if k in r}, "page": str(index - books[book]["page"]), "parent": parent})
        by_book[book] = {k: c[k] for k in ("pages", "pages_without_a_row", "entries", "subrows", "marked_as_loans", "continued", "unsure")}
    report = {"pages": {"expected": len(wanted), "merged": sum(b["pages"] for b in by_book.values()), "failed": len(fails), "missing": len(missing)},
              "entries": sum(b["entries"] for b in by_book.values()), "subrows": sum(b["subrows"] for b in by_book.values()),
              "by_book": by_book, "continued_not_attached": loose, "failed": fails, "missing": missing, "other_files": extra}
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
    for name, why in report["failed"].items():
        print("  failed", name, "-", "; ".join(why))
    if report["missing"]:
        print("  missing:", ", ".join(report["missing"]))
    if report["other_files"]:
        print("  not a page's file:", ", ".join(report["other_files"]))


# ------------------------------------------------------------------------------------------ the typing's bar

def letters(headword):
    """A headword as the typing's bar compares it: lower case, every combining mark on a vowel set aside (the
    macron of length, the acute of the accent, any other). A mark on a consonant stays (it makes another
    consonant), and so do hyphens and spaces."""
    out = []
    for ch in unicodedata.normalize("NFD", headword.strip().lower()):
        if unicodedata.combining(ch) and out and out[-1] in VOWELS:
            continue
        out.append(ch if not unicodedata.combining(ch) or not out else out.pop() + ch)
    return unicodedata.normalize("NFC", "".join(out))


def likeness(a, b):
    """The likeness of two German meanings: difflib's ratio on the lower-cased texts (without its shortcut for
    long texts, which leaves common letters out of the comparison)."""
    return difflib.SequenceMatcher(None, a.strip().lower(), b.strip().lower(), autojunk=False).ratio()


def sounds(headword, book):
    return cr.segments(spelling(headword, book))


def in_both(first, second, key):
    """How many of the first reading's rows stand in the second by `key`, each row of the second used once."""
    a, b = collections.Counter(map(key, first)), collections.Counter(map(key, second))
    return sum((a & b).values())


def compare(first, second, book):
    """One page's rows of one sort (entries, or sub-rows) in the two readings. A row of the first reading is
    found when a row of the second has the same letters(); where several share them, the pairs are made by
    the likeness of their German meanings, the likest first. Found rows carry the same meaning at TYPING's
    likeness or more."""
    theirs = collections.defaultdict(list)
    for r in second:
        theirs[letters(r["headword"])].append(r)
    mine = collections.defaultdict(list)
    for r in first:
        mine[letters(r["headword"])].append(r)
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
    nfc = lambda r: unicodedata.normalize("NFC", r["headword"].strip())          # noqa: E731
    return {"first": len(first), "second": len(second), "found": found, "same_meaning": same,
            "mark_for_mark": in_both(first, second, nfc), "same_sounds": in_both(first, second, lambda r: sounds(r["headword"], book)),
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


def languages(dialect):
    """(the engine's languages of a dialect cell, the letters in it that are no dialect of the books). Without a
    dialect of the books the row is UNMARKED's."""
    marks = [c for c in dialect.upper() if c.isalpha()]
    langs = list(dict.fromkeys(DIALECTS[c] for c in marks if c in DIALECTS))
    return tuple(langs) or (UNMARKED,), "".join(c for c in marks if c not in DIALECTS)


def engine_rows(rows):
    """(the rows of dictionary.tsv as rows the engine scores, the counts). A sub-row stands in the entry its
    `parent` names, the nearest one before it on its page; where the page has none of that headword before it
    (a page that begins inside an entry, a parent typed otherwise), in the entry right before it. It takes that
    entry's loan mark, and its dialect where it has none of its own. Left out: an entry marked as a loan with its
    sub-rows, a row without an English meaning, a row whose headword has no letter the engine reads."""
    out, c = [], collections.Counter()
    named, before = {}, {}
    odd, unread = collections.Counter(), collections.Counter()
    for r in rows:
        book = r["book"]
        if r["parent"]:
            own = named.get((book, r["page"], r["parent"]))
            if own is None:
                own = before.get(book)
                c["subrows_under_the_entry_before"] += 1
        else:
            own = named[(book, r["page"], r["headword"])] = before[book] = r
        c["subrows_read" if r["parent"] else "entries_read"] += 1
        if r["loan"] or (own is not None and own["loan"]):
            c["subrows_of_loans_left_out" if r["parent"] else "loans_left_out"] += 1
            continue
        if not r["gloss_en"]:
            c["without_an_english_meaning"] += 1
            continue
        spelt = spelling(r["headword"], book)
        vs = tuple((v, s) for v, s in ((v, cr.segments(v)) for v in cr.variants(spelt)) if s)
        if not vs:
            c["without_a_letter_the_engine_reads"] += 1
            continue
        unread.update(ch for ch in unicodedata.normalize("NFD", spelt) if ch.isalpha() and ch not in cr.SEG)
        dialect = r["dialect"] or (own["dialect"] if own is not None else "")
        langs, other = languages(dialect)
        if other:
            odd[dialect] += 1
        c["without_a_dialect"] += not any(ch in DIALECTS for ch in dialect.upper())
        c["compared"] += 1
        for lang in langs:
            out.append(cr.Row(lang, r["headword"], r["gloss_en"], frozenset(cr.cognates.keys(r["gloss_en"])), BOOKS[book]["list"], dialect, vs))
    counts = {k: c[k] for k in ("entries_read", "subrows_read", "loans_left_out", "subrows_of_loans_left_out", "without_an_english_meaning",
                                "without_a_letter_the_engine_reads", "compared", "without_a_dialect", "subrows_under_the_entry_before")}
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
