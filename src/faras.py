"""Griffith's 46 Faras funerary texts (1922): open readings typed from his hand copies.

F. Ll. Griffith, "Meroitic funerary inscriptions from Faras, Nubia", in *Recueil d'études égyptologiques dédiées à
la mémoire de Jean-François Champollion* (Paris 1922), pp. 565-600 (public domain; archive.org
bibliothquedel234ecol, PDF pages 601 to 648). He prints each text as a hand copy in Meroitic cursive, with an
English rendering that spells the names, titles and formula words in Latin letters, and notes on the formulae in his
transliteration (pp. 599-600). He prints no transliteration of whole texts and no indexes.

Readers (Claude Opus 5.5) typed all 46 texts from page images, pack by pack (data/expansion/faras/readings/<pack>/
readings.jsonl, the brief beside them): first from the copy alone (`first`), then checked against his Latin letters
(`final`). Five texts drawn by lot before typing (BAR.md)
were typed a second time by a fresh reader who saw nothing of the first typing (data/expansion/faras/second/).
Where the two differ, the place was settled against the page (settled.jsonl), and the row takes the settled
reading.

Faras n is REM 05nn (three passages of the Meroitic Newsletter agree: README.md), as Karanòg n is REM 02nn. Each row
is an open reading of its REM number in corpus_v6: src/v6/readings.py reads this folder like the folder of REM 1003
(data/expansion/jea), as texts an article prints, with no number of Griffith's and no row of corpus_v5. The row sits in
a sub-folder that src/expand.py does not read, so corpus_v3 and corpus_v5 stay as they were.

  python3 -I src/faras.py              writes data/expansion/faras/griffith_faras.jsonl and prints the counts
  python3 -I src/faras.py measure      the second typing against the first on the five drawn texts (the bar)
  python3 -I src/faras.py compare      the typed texts against the readings corpus_v6 already holds (local; the
                                       counts go to data/expansion/faras/comparison.json)
  python3 -I src/faras.py verdicts     before the rebuild: two readers' verdicts on Millet's lines 286 and 779 into
                                       the build's verdicts (local)
  python3 -I src/faras.py recur        after the rebuild: the map's open spellings that stood in one text and now
                                       stand in a new Faras text too (local; data/expansion/faras/recur.json)
"""
import collections
import difflib
import itertools
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(ROOT / "src" / "v6")]
import karanog as K     # noqa: E402  the reading's marks, signs, words and corpus spelling are the Karanòg rows'

FARAS = ROOT / "data/expansion/faras"
READINGS = FARAS / "readings"
SECOND = FARAS / "second"
SETTLED = FARAS / "settled.jsonl"
ROW = FARAS / "griffith_faras.jsonl"
MEASURE = FARAS / "measure.json"
COMPARISON = FARAS / "comparison.json"
RECUR = FARAS / "recur.json"
VERDICTS = FARAS / "verdicts.jsonl"                     # two readers on the Millet lines the Faras texts settle
V6 = ROOT / "data/sources/v6/inscriptions.jsonl"

SOURCE = 'Griffith, "Meroitic funerary inscriptions from Faras, Nubia", Recueil Champollion (1922)'
ITEM = "bibliothquedel234ecol"
TEXTS = range(1, 47)
DRAWN = (2, 10, 13, 14, 15)          # BAR.md: random.Random(20261117).sample(range(1, 47), 5), sorted
SEED = 20261117
OFFSET = 36                          # the PDF's page number less the printed one before the first plate (603 is p. 567)
# the PDF pages of Plates VIII to XIII and their blank backs, which carry no printed number: after each plate the
# printed number falls two further behind the PDF's (PDF p. 609 is p. 571, PDF p. 647 is p. 599)
PLATES = (605, 606, 615, 616, 621, 622, 629, 630, 639, 640, 643, 644)
REM_FARAS = re.compile(r"05(0[1-9]|[1-3]\d|4[0-6])")      # REM 0501 to 0546: Faras n is REM 05nn
NUMERAL = re.compile(r"(?<![\d(])(\d+)(?![\d)])")       # a numeral of the stone ("1" after each prince, Faras 44),
#                                                      not a line number "(13)"
LINES = ROOT / "data/sources/v6/lines.jsonl"


def number(text):
    """'Faras 7' -> 7; None for anything else."""
    m = re.fullmatch(r"\s*Faras\s+(\d+)\s*", text or "")
    return int(m.group(1)) if m else None


def rem(n):
    return f"{500 + n:04d}"


def load(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()] if path.exists() else []


def stray(final):
    """What a final reading holds besides signs, marks and numerals (karanog.stray, with the stone's numerals let be)."""
    return K.stray(NUMERAL.sub(" ", final or ""))


def readings(folder=READINGS):
    """{n: the reader's object for Faras n} from every pack under folder; a text read twice in one folder, a text
    that is not 'Faras N', or a final reading that holds something neither sign nor mark stops the run. The first
    reading (before the check) is only compared with the final one: a letter in it that is no sign (a reader's
    "v?" for a shape it could not name, Faras 7) drops out of that count."""
    out = {}
    for pack in sorted(p for p in folder.iterdir() if p.is_dir()) if folder.exists() else []:
        for o in load(pack / "readings.jsonl"):
            n = number(o.get("text"))
            if n is None or n not in TEXTS:
                raise ValueError(f"{pack.name}: text {o.get('text')!r} is not 'Faras N' (1 to 46)")
            if n in out:
                raise ValueError(f"{pack.name}: Faras {n} is read twice (also in pack {out[n]['pack']})")
            if stray(o.get("final")):                      # the row's reading: signs, marks and numerals
                raise ValueError(f"{pack.name}: the final reading of Faras {n} holds "
                                 f"{stray(o['final'])!r}, neither signs nor marks: {o['final']!r}")
            out[n] = dict(o, pack=pack.name)
    return out


def bare(reading):
    """The signs of a reading with lost and restored signs left out (the measure's unit)."""
    return [s for s in K.signs(reading) if s != "."]


def distance(a, b):
    """Edit distance between two lists of signs (insert, delete, change: one each)."""
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def agreement(pairs):
    """(signs that agree, signs) over [(first, second)] readings: the first's signs less the edit distance."""
    agree = total = 0
    for a, b in pairs:
        sa, sb = bare(a), bare(b)
        total += len(sa)
        agree += max(len(sa) - distance(sa, sb), 0)
    return agree, total


def formula_pairs(refs=K.KAR / "refs/by_inscription"):
    """The 17 pairs of formula words that Griffith's Karanòg formula tables print apart for 5 inscriptions or more
    ("ato mẖe", "at mẖe", "mẖe psḫrkete"), which the Karanòg rows part in every row (karanog.py, README section 5).
    The Faras rows are parted the same way, so that a formula is spelled and divided alike in both."""
    held = collections.Counter()
    for p in sorted(refs.glob("*.jsonl")):
        held.update(K.phrases(load(p)))
    return [p for p, k in held.items() if k >= K.EVERYWHERE]


def settled(path=SETTLED):
    """{n: the settled object of Faras n}: the reading the row takes where the two typings differed."""
    out = {}
    for o in load(path):
        n = number(o.get("text"))
        if n is None or stray(o.get("final")):
            raise ValueError(f"{path.name}: {o.get('text')!r} or its reading is not well formed")
        out[n] = o
    return out


def printed(pdf):
    """The printed page number of a page of the PDF; a plate has none."""
    if pdf in PLATES:
        raise ValueError(f"PDF p. {pdf} is a plate (or its back), with no printed page number")
    return pdf - OFFSET - sum(p < pdf for p in PLATES)


def page(o):
    """'p. 567 (PDF p. 603)', or 'pp. 568-569 (PDF pp. 604-607)' across a plate."""
    pdf = sorted(int(re.sub(r"\D", "", p)) for p in o.get("pages", []) if re.search(r"\d", p))
    if not pdf:
        return ""
    if len(pdf) == 1:
        return f"p. {printed(pdf[0])} (PDF p. {pdf[0]})"
    return f"pp. {printed(pdf[0])}-{printed(pdf[-1])} (PDF pp. {pdf[0]}-{pdf[-1]})"


def restored(reading):
    """The reading with a restoration that runs over a word end written as one bracket a word: "terike[li teri]kelowi"
    (Faras 5) is "terike[li] [teri]kelowi". karanog.marked() makes a whole bracket one stretch of lost signs, which
    would join the two words; the signs are the same either way."""
    return re.sub(r"\[([^\]]*\s[^\]]*)\]", lambda m: " ".join(f"[{w}]" for w in m.group(1).split()), reading)


GRIFFITH_ROWS = (ROOT / "data/expansion", K.KAR)       # the other public Griffith rows: his volumes and Karanòg
KNOWN = 3              # a spelling that stands in this many of those rows is a word a gap of the copy does not part


def known_words(folders=GRIFFITH_ROWS, least=KNOWN):
    """The spellings (corpus spelling, letters only) that stand in `least` texts or more of the other public Griffith
    rows (Meroitic Inscriptions, Meroë, Karanòg): wosi, soreyi, tedxelowi, pSoXte and the like."""
    texts = collections.Counter()
    for folder in folders:
        for path in sorted(folder.glob("griffith_*.jsonl")):
            for r in load(path):
                texts.update({w for w in r.get("text_corpus", "").split() if re.fullmatch(r"[A-Za-z]+", w)})
    return {w for w, n in texts.items() if n >= least}


def holds(words, pairs):
    """Whether words, joined into one, stay joined: karanog.divided() parts the joined word at none of their gaps.
    "ato" and "mẖe" spell atomẖe, which three of the other rows write, but the pair (ato, mẖe) parts it again: two
    words that the reader set apart, not a gap of the copy."""
    gaps = set(itertools.accumulate(len(w) for w in words[:-1]))
    parts, _ = K.divided([[s for w in words for s in w]], pairs)
    return not gaps & set(itertools.accumulate(len(p) for p in parts[:-1]))


def joined(runs, known, pairs=(), most=K.JOIN):
    """The words of runs (karanog.runs: the words between two dividers, each a list of signs) as one list, with
    neighbours of one run joined where together they spell a known word: the copies leave gaps inside words (the
    altars' borders, a raised number of Griffith's), and the readers wrote a space at each gap ("so (2) reyi",
    "a(6)t", "pSi Xte"). Two to `most` words, the longest join first; a divider is the stone's and is never crossed,
    and nor is a word end that the formula pairs would part again (holds()). Returns (words, gaps closed)."""
    out, closed = [], 0
    for run in runs:
        i = 0
        while i < len(run):
            j = next((j for j in range(min(len(run), i + most), i + 1, -1)
                      if K.spell([[s for w in run[i:j] for s in w]]) in known and holds(run[i:j], pairs)), i + 1)
            out.append([s for w in run[i:j] for s in w])
            closed += j - i - 1
            i = j
    return out, closed


def words_of(reading, known, pairs):
    """(the words of a reading, each a list of signs or [numeral], gaps closed, formula words parted). A numeral is a
    word of its own and parts the text around it; the rest goes through joined() and karanog.divided()."""
    words, closed = [], 0
    for k, part in enumerate(NUMERAL.split(restored(reading))):
        if k % 2:
            words.append([part])
            continue
        ws, c = joined(K.runs(part), known, pairs)
        words += ws
        closed += c
    words, parted = K.divided(words, pairs)
    return words, closed, parted


def counted(word):
    """A word that counts: it has a letter or is a numeral (a stretch of lost signs does not)."""
    return bool(re.search(r"[A-Za-z0-9]", word))


def count(n, noun):
    return K.count(n, noun)


def rows(first=None, second=None, decided=None, pairs=None, known=None):
    """One row per text, in Griffith's order."""
    first = readings() if first is None else first
    second = readings(SECOND) if second is None else second
    decided = settled() if decided is None else decided
    pairs = formula_pairs() if pairs is None else pairs
    known = known_words() if known is None else known
    out = []
    for n in sorted(first):
        o = first[n]
        final = decided[n]["final"] if n in decided else o["final"]
        words, closed, parted = words_of(final, known, pairs)
        corpus = K.spell(words)
        notes = [f"Typed from Griffith's hand copy by Claude Opus 5.5 (pack {o['pack']}), then checked against his "
                 f"Latin letters (the names, titles and formula words of his English rendering, and his notes on the "
                 f"formulae): {count(K.changed(o['first'], o['final']), 'sign')} changed by the check."]
        if n in second:
            agree, total = agreement([(o["final"], second[n]["final"])])
            settled_places = len(decided.get(n, {}).get("places", []))
            notes.append(f"Typed a second time, blind, by another reader (pack {second[n]['pack']}): the two agree on "
                         f"{agree} of {total} signs" + (f". The row takes the reading settled against the page and "
                         f"Griffith's notes where they differ ({count(settled_places, 'place')}; settled.jsonl)."
                         if settled_places else "."))
        if o.get("kept"):
            notes.append("Copy kept against his Latin letters: " + "; ".join(
                f"{k.get('copy', '')} (his Latin: {k.get('latin', '')})" for k in o["kept"]) + ".")
        if closed:
            notes.append(f"text_corpus closes {count(closed, 'gap')} of the copy inside a word that the other Griffith "
                         f"rows spell whole (so reyi is soreyi).")
        if parted:
            notes.append(f"text_corpus parts {count(parted, 'formula word')} as Griffith's Karanòg formula tables do "
                         f"(ato mẖe, at mẖe, mẖe psḫrkete and the like).")
        if (o.get("notes") or "").strip():
            notes.append(o["notes"].strip())
        out.append({"source": SOURCE, "item": ITEM, "griffith_no": None, "rem": rem(n), "label": f"Faras {n}",
                    "page": page(o), "object": o.get("object", ""), "site": "Faras",
                    "text_std": final, "text_corpus": corpus,
                    "uncertain": final.count("?"), "signs": len(bare(final)),
                    "words": sum(counted(w) for w in corpus.split()),
                    "rendering": o.get("rendering", ""),
                    "doubts": o.get("unsure", []), "notes": " ".join(notes)})
    return out


# ------------------------------------------------------------------------------------------ the bar

def measure(first=None, second=None):
    """The second typing against the first on the drawn texts: after the check (the bar, 95%) and before it."""
    first = readings() if first is None else first
    second = readings(SECOND) if second is None else second
    missing = [n for n in DRAWN if n not in first or n not in second]
    if missing:
        raise SystemExit(f"not typed twice yet: Faras {missing}")
    out = {"texts": [f"Faras {n}" for n in DRAWN], "seed": SEED, "bar": 0.95,
           "how": "the signs of the first typing less the edit distance between the two typings, over the signs of "
                  "the first typing; lost and restored signs and line numbers left out (BAR.md)"}
    for key in ("final", "first"):
        agree, total = agreement([(first[n][key], second[n][key]) for n in DRAWN])
        out[key] = {"agree": agree, "signs": total, "share": round(agree / total, 4) if total else None,
                    "by_text": {f"Faras {n}": dict(zip(("agree", "signs"), agreement([(first[n][key], second[n][key])])))
                                for n in DRAWN}}
    # on the counts, not on the rounded share: 37,999 of 40,000 rounds to 0.95 and misses the bar
    out["met"] = out["final"]["signs"] > 0 and out["final"]["agree"] * 100 >= out["final"]["signs"] * 95
    return out


def places(a, b):
    """[(first's signs, second's signs, signs before, signs after)] where two readings differ: the list the
    settling of the drawn texts started from (settled.jsonl)."""
    sa, sb = K.signs(a), K.signs(b)
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, sa, sb, autojunk=False).get_opcodes():
        if tag != "equal":
            out.append(("".join(sa[i1:i2]), "".join(sb[j1:j2]), "".join(sa[max(0, i1 - 4):i1]), "".join(sa[i2:i2 + 4])))
    return out


# ------------------------------------------------------------------------------------------ the comparison

def fold(text):
    """A text as one string of letters, spelled alike whatever convention wrote it (as src/akinidad.py: o and e,
    se and s, ne and n, capitals and small letters folded; dots and masked names out)."""
    t = re.sub(r"\bR?NAME\b|[.…]+", "", text).lower()
    t = t.replace("o", "e").replace("se", "s").replace("ne", "n")
    return re.sub(r"[^a-z]", "", t)


def held_by_letters():
    """{Faras n: [(verdict, share of the Faras text, share of the other, own runs shared, key)]}: the readings that
    corpus_v6 already holds (every edition, narrative and source line but the Faras rows) that each typed text
    matches by the rule of src/v6/readings.py (local: it reads Otten's files and the editions' text layers)."""
    import readings as R
    editions, narratives, lines = R.load()
    ours = {r["key"] for r in editions if r["key"].startswith("griffith:G-faras-")}
    pool = [r for r in editions + narratives + lines if r["key"] not in ours]
    skip = R.formulae(editions)
    out = {}
    for r in editions:
        if r["key"] in ours:
            n = int(r["key"].rsplit("-", 1)[1]) - 500
            out[n] = R.matches(r, pool, skip, top=5)
    return out


def against(text, other):
    """(letters of the other text that agree, its letters): the other's folded letters less the edit distance."""
    a, b = list(fold(other)), list(fold(text))
    return max(len(a) - distance(a, b), 0), len(a)


def within(text, other, folded=True):
    """(letters of the other text that agree, its letters) for a passage quoted from a text: the other's letters less
    the fewest edits that make them one stretch of the text, wherever it starts and ends. folded: letters spelled
    alike (fold()); otherwise only word division and lost signs are left out (x and X, s and S stay apart)."""
    letters = fold if folded else (lambda t: re.sub(r"[^A-Za-z]", "", t))
    a, b = letters(other), letters(text)
    prev = [0] * (len(b) + 1)                      # the passage may start anywhere in the text ...
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return max(len(a) - min(prev), 0), len(a)      # ... and end anywhere


def quoted(path=LINES):
    """{REM number: [the source line]} of the source lines of Otten's files that the build of corpus_v6 gives to a
    Faras text, as a reading or as a phrase (local), or None."""
    if not path.exists():
        return None
    out = collections.defaultdict(list)
    for o in load(path):
        rem_ = (o.get("inscription") or "").removeprefix("REM ")
        if REM_FARAS.fullmatch(rem_) and o.get("text"):
            out[rem_].append(o)
    return dict(out)


def closed_readings(path=V6):
    """{REM number: {key: text}} of the readings corpus_v6 holds for REM 0501 to 0546 (local), or None."""
    if not path.exists():
        return None
    out = collections.defaultdict(dict)
    for line in path.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        for x in r["readings"]:
            if x.get("text") and not x["key"].startswith("griffith:G-faras-"):
                for value in r.get("rem") or []:
                    if REM_FARAS.fullmatch(value):
                        out[value][x["key"]] = x["text"]
    return dict(out)


def comparison(rows):
    """The counts of the comparison (public; no closed text): which held readings each typed text matches by the
    rule, how far each typed text agrees with the readings of its REM number that corpus_v6 already holds, and how
    far it agrees with the source lines (Millet's quotations) that the build gives to it."""
    by_letters = held_by_letters()
    closed = closed_readings() or {}
    lines = quoted() or {}
    out = {"how": {"by_letters": "the rule of src/v6/readings.py (runs of five letters, formula runs left out) from "
                                 "each typed text to every reading corpus_v6 holds but the Faras rows",
                   "by_number": "the readings corpus_v6 holds under the text's REM number; letters spelled alike "
                                "(fold()); the other's letters less the edit distance, over the other's letters",
                   "lines": "the source lines of Otten's files that the build gives to the text (a quotation of a "
                            "part of it, as a phrase or a reading): the line's letters less the fewest edits that "
                            "make them a stretch of the typed text, over the line's letters; folded with letters "
                            "spelled alike (fold()), strict with nothing folded but word division and lost signs"},
           "texts": {}}
    for r in rows:
        n = int(r["label"].split()[1])
        entry = {"rem": r["rem"], "matches": [{"verdict": v, "share_faras": a, "share_other": b, "shared": s, "key": k}
                                               for v, a, b, s, k in by_letters.get(n, [])]}
        if r["rem"] in closed:
            entry["against"] = {k: dict(zip(("agree", "letters"), against(r["text_corpus"], t)))
                                for k, t in sorted(closed[r["rem"]].items())}
        if r["rem"] in lines:
            entry["lines"] = [{"key": o["key"], "class": o["class"], "by": o["by"],
                               **{how: dict(zip(("agree", "letters"), within(r["text_corpus"], o["text"], folded)))
                                  for how, folded in (("folded", True), ("strict", False))}}
                              for o in sorted(lines[r["rem"]], key=lambda o: (o["file"], o["line"]))]
        if entry["matches"] or entry.get("against") or entry.get("lines"):
            out["texts"][r["label"]] = entry
    return out


# ------------------------------------------------------------------------------------------ what recurs now

def recur(corpus_path=ROOT / "data/corpus_v6.jsonl"):
    """How the new Faras texts meet the map (src/themap.py, the map as it stands): the open spellings of the map
    that stood in one of its texts and now stand in a new Faras text too, and those that reach three texts (the
    line of the recurring study, src/recurring.py); and how many distinct spellings of the new texts the map holds
    already, open or not (a word with a lost sign left out). The map itself holds only the texts the analysts
    glossed, so a new text is counted here from corpus_v6 (local), word by word as the build gives it; a word at a
    place the build marks as a name is counted apart. Faras 44 is REM 0544, already on the map: only the new texts
    count."""
    import themap as M
    import recurring as W
    gl = M.current()
    level, on_the_map, _ = W.spellings_of(gl)
    opened = {f for f, c in level.items() if c.most_common(1)[0][0] in W.OPEN}
    corpus = load(corpus_path)
    new = [c for c in corpus if c["reading"].startswith("griffith:G-faras-") and c["id"] not in gl]
    # a text of the map that the rebuild no longer holds has been found to be a part of another inscription (Millet's
    # example line 414 is ll. 26-28 of Faras 21): its spellings are not a second text beside the Faras one
    gone = set(gl) - {c["id"] for c in corpus}
    texts = {f: ts - gone for f, ts in on_the_map.items()}
    faras, as_name = collections.defaultdict(set), collections.defaultdict(set)
    for c in new:
        named = set(c.get("names") or ())
        for i, tok in enumerate(c["text"].split()):
            (as_name if i in named else faras)[tok].add(c["id"])
    faras, as_name = dict(faras), dict(as_name)       # looked up below: no empty entry may be made by a lookup
    spelt = [f for f in faras if "." not in f]         # the new texts' spellings, a word with a lost sign left out
    on_map = [f for f in spelt if f in level]
    off_map = [f for f in spelt if f not in level]
    single = sorted(f for f in opened if len(texts[f]) == 1)
    again = [f for f in single if f in faras]
    reach = [f for f in opened if len(texts[f]) < W.MIN_TEXTS <= len(texts[f]) + len(faras.get(f, ()))]
    return {"map": {"inscriptions": len(gl), "open_spellings": len(opened),
                    "in_one_text_on_the_map": sum(len(on_the_map[f]) == 1 for f in opened),
                    "in_one_text": len(single), "texts_now_part_of_another_inscription": sorted(gone)},
            "new_texts": len(new),
            "in_one_text_now_in_a_faras_text": len(again),
            "in_one_text_now_in_a_faras_text_as_a_name_only": sum(1 for f in single if f in as_name and f not in faras),
            "reach_three_texts": len(reach),
            "new_words": sum(len(c["text"].split()) for c in new),
            "new_spellings": {"distinct": len(spelt), "on_the_map": len(on_map),
                              "open_on_the_map": sum(f in opened for f in on_map), "new_to_the_map": len(off_map),
                              "new_to_the_map_in_two_faras_texts": sum(len(faras[f]) > 1 for f in off_map)},
            "spellings": {f: {"map_texts": len(texts[f]), "faras_texts": len(faras.get(f, ()))}
                          for f in sorted(set(again) | set(reach))}}


# ------------------------------------------------------------------------------------------ the readers' verdicts

def merge_verdicts(ours=VERDICTS, path=None):
    """Write the verdicts of VERDICTS into the corpus build's verdicts (data/sources/v6/readers/verdicts.jsonl,
    local), in place of the earlier verdict on the same line, so that src/v6/build.py takes them: Millet's line 286,
    a text not identified before, is Faras 43, and his line 779 quotes Faras 38. Returns the lines replaced and added."""
    import build as B
    path = B.VERDICTS if path is None else path
    new = {o["line"]: {k: o[k] for k in ("line", "same_as", "part")} for o in load(ours)}
    old = load(path)
    out = [new.get(o["line"], o) for o in old]
    out += [v for k, v in new.items() if k not in {o["line"] for o in old}]
    path.write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in out), encoding="utf-8")
    return sum(o["line"] in new for o in old), len(out) - len(old)

def main(argv):
    if argv[:1] == ["measure"]:
        m = measure()
        MEASURE.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        for key in ("final", "first"):
            v = m[key]
            print(f"{key}: {v['agree']} of {v['signs']} signs agree ({v['share']:.1%})")
        print("bar (95%) met" if m["met"] else "bar (95%) NOT met")
        return
    if argv[:1] == ["verdicts"]:
        replaced, added = merge_verdicts()
        print(f"data/sources/v6/readers/verdicts.jsonl: {count(replaced, 'verdict')} replaced, {added} added")
        return
    if argv[:1] == ["recur"]:
        r = recur()
        RECUR.write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print({k: v for k, v in r.items() if k != "spellings"})
        return
    out = rows()
    if argv[:1] == ["compare"]:
        c = comparison(out)
        COMPARISON.write_text(json.dumps(c, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        for label, e in c["texts"].items():
            print(label, e)
        return
    ROW.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out), encoding="utf-8")
    print(f"{ROW.relative_to(ROOT)}: {len(out)} texts, {sum(r['signs'] for r in out)} signs, "
          f"{sum(r['words'] for r in out)} words, {sum(r['uncertain'] for r in out)} query marks")


if __name__ == "__main__":
    main(sys.argv[1:])
