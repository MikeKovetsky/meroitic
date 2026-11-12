"""How much of the corpus can be translated today, word by word?

  python3 -I src/coverage.py first                       the lookup alone: its figures and the words it leaves
  python3 -I src/coverage.py packs <dir> [--per N] [--again N] [--more]
                                                         packs of the words left, for the analysts (A...), and
                                                         the N most frequent a second time (B...); with --more,
                                                         only the words no pack of <dir> holds yet
  python3 -I src/coverage.py build <dir> [--public]      merge the analysts' answers in <dir>; write the gloss
                                                         file, the ranked list and the figures
  python3 -I src/coverage.py correct <dir> [--public]    the same map with the corrections (below), written
                                                         beside the first: corrected/ and the list
                                                         coverage_unknown_corrected.tsv

Every word of data/corpus_v5.jsonl gets a gloss, a level and a confidence (data/discovery/coverage.md):

1. The lookup. A word that is a spelling of an entry of Rilly's 2003 lexicon (data/rilly2003/, local only) takes
   that entry's gloss; so does a word made of a stem of three letters or more and one of the endings of
   lexique.SUFFIXES, when Rilly gives the stem a meaning (without one the match proves nothing: pXolkete is not
   the title pẖo with an ending). A masked name is a name, digits are a number, a word with a lost sign is lost,
   and a word that Griffith's tables print as a name of its Karanog inscription is a name.
2. The analysts. A word the lookup leaves goes, with its contexts and Rilly's entries, to a reader who cuts it
   into parts, each an entry of the lexicon, a name, a number or an unknown piece ("?"), and says what kind of
   word it is. The parts must spell the word, and an entry must exist: an answer that fails either is dropped.
   The most frequent words are analysed twice, independently; where the two differ, the lower level stands.

Levels: meaning, grammar, name and number count as translated (the entry is "established" or "probable" in
Rilly); hypothesis (Rilly gives a proposal only, or the analyst is unsure of the cut); kind (no meaning, but
the kind of word is known: a title, a name, a verb of the benedictions); unknown; lost.

The gloss file leans on Rilly's lexicon and stays local (data/sources/coverage/). The public files are the
counts and the list of words without a meaning, each with its kind and the texts it blocks.

The corrections (`correct`). Later work found words that the map counts wrongly, and four rules set them right.
The map as first built stays as it was, because two searches read its list (src/egyptian.py, src/variants.py).
1. The rest of a masked name. The older corpus was padded with copies in which names were swapped; a name of
   several words left its other words behind the mask: "mokelowi" and "mete l" directly after NAME are such a
   rest and count as a name. A name leaves one rest: the mokelowi of "NAME mete l mokelowi" is the frame's own.
2. A stem of two signs. The lookup asks a stem for three letters, but the signs se and ne are two letters each
   in Rilly's spelling: smlowi is sem "wife" with -lowi. Only for an entry Rilly holds as established.
3. A word written apart. Two or three neighbours, one of them of one or two letters, that together spell a word
   the lookup translates, when that word also stands written as one in other texts: wo Si is woSi, "O Isis".
4. A spelling of a known word. The pieces that two blind checkers both took for a spelling or a form of a word
   with an accepted meaning (data/discovery/variants.md), without the two whose pack showed a hint; and three
   forms of kdise "sister" that a reader of the families of Karanog read so (SISTER).
"""
import collections, json, re, statistics, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import lexique as L   # noqa: E402

CORPUS = ROOT / "data/corpus_v5.jsonl"
KAR_REFS = ROOT / "data/expansion/karanog/refs/by_inscription"
OUT = ROOT / "data/sources/coverage"                       # local only
PUBLIC = ROOT / "data/discovery/coverage_unknown.tsv"
CORRECTED = OUT / "corrected"                               # local only: the map after the corrections
PUBLIC_CORRECTED = ROOT / "data/discovery/coverage_unknown_corrected.tsv"
VARIANTS = ROOT / "data/discovery/variants_confirmed.tsv"   # the confirmed spellings of known words (variants.py)
BRIEF = ROOT / "data/discovery/coverage_brief.md"

TRANSLATED = ("meaning", "grammar", "name", "number")
LEVELS = TRANSLATED + ("hypothesis", "kind", "unknown", "lost")
RANK = {"meaning": 0, "grammar": 0, "name": 0, "number": 0, "hypothesis": 1, "kind": 2, "unknown": 3}
CONFIDENCE = {"established": 5, "probable": 4, "hypothesis": 2}
SURE = 4                      # an analyst's cut counts from this confidence up (the scale of runs/unknown/)
# The corrections. What the padding of the older corpus left directly after a masked name: Millet marks "amxye
# mokelowi" and "yetmetN-mete-l", "Yetmetne the younger", as personal names (MilletExamples.txt, l. 1142 and 120;
# "tqo mete l" is in clean_v2.FILLERS); the first word was masked and the rest stayed, in the same frames. A name
# leaves one rest: where "NAME mete l" or "NAME mokelowi" stands before mokelowi, that mokelowi is the frame's own
# word, of the second passage of GA 19 A ("tni mEkelEwi : xteri", l. 1141; Millet does not mark it as a name).
# Where a name of one word stood in that slot (T0051), the rule cannot tell the frame's word from a rest.
NAME_TAILS = (("mokelowi",), ("mete", "l"))
MASKED = ("NAME", "RNAME")
SYLLABLE_SIGNS = "sN"         # the signs se and ne: one sign in the corpus spelling, two letters in Rilly's
FRAGMENT = 2                  # a word of this many letters or fewer can be a piece of its neighbour written apart
WRITTEN = 2                   # ... when the two together stand as one word in this many texts or more
SET_APART = ("mXeyot", "yetmetl")   # confirmed variants whose pack showed a word holding their letters (variants.md)
CHECKED = "two blind checkers (data/discovery/variants.md)"
# Rule 4 also takes the forms of kdise "sister" that the correction was asked to count (data/sources/notes/
# PROGRESS.md, entry 43, local) and the checkers did not confirm. The reader who rebuilt the families of Karanog
# read them so (data/sources/dig/kin/REPORT.md, section 6, local), and the analysts cut each into kdi or kdise and
# endings without being sure of the endings.
SISTER = {"kdito": "kdise", "kdisbetowi": "kdise", "kditebkwi": "kdise"}
FAMILIES = "the reader who rebuilt the families of Karanog (one reader, not blind)"
# Rilly's category -> the kind of word, the first that fits
CATEGORY_KIND = (("anthroponyme", "person name"), ("nom de personne", "person name"), ("toponyme", "place name"),
                 ("nom de lieu", "place name"), ("ethnonyme", "people name"), ("théonyme", "god name"),
                 ("theonyme", "god name"), ("nom divin", "god name"), ("divinit", "god name"),
                 ("nom propre", "name"), ("titre", "title"), ("épithète", "epithet"), ("epithete", "epithet"),
                 ("verbe", "verb"), ("adjectif", "adjective"), ("numéral", "numeral or measure"),
                 ("substantif", "noun"), ("nom", "noun"))
KINDS = ("person name", "place name", "god name", "people name", "name", "title", "kin term", "epithet",
         "benediction verb", "filiation word", "verb", "noun", "adjective", "numeral or measure", "function word",
         "two words written as one", "unknown")
NAME_KINDS = ("person name", "place name", "god name", "people name", "name")
SPECIAL = ("NAME", "NUMBER", "?")       # what a part can be besides an entry of the lexicon
PLAIN = re.compile(r"[a-zSNX]+")
# a meaning that only names the kind of word: "a priestly title linked with the cults of ...", "an epithet of Isis"
KIND_ONLY = re.compile(r"^(?:an?\s+|the\s+)?(?:[\w-]+\s+){0,3}(?:title|epithet)\b", re.I)


# ---------------------------------------------------------------------------------------------- the lexicon

def kind_of(category):
    cat = (category or "").lower()
    if any(g in cat for g in L.GRAMMAR):
        return "function word"
    return next((k for c, k in CATEGORY_KIND if c in cat), "")


QUOTES = re.compile(r"(?<![A-Za-z])['\"‘’“”]|['\"‘’“”](?![A-Za-z])")
CLAUSE = re.compile(r"[;(]| - |: |, (?=and perhaps|perhaps|probably|possibly|according|after |borrowed|an? |the |one of|in )")


QUOTED = re.compile(r"['\"‘“]([^'\"’”]{2,})['\"’”]")


def short(meaning, n=48):
    """The first clause of a meaning, without its quotation marks, for the gloss line; the first quoted gloss
    when the meaning opens with an analysis of the word ("ḫ(re) + lẖ + l 'a great meal'"). Cut at a word's end."""
    whole = re.sub(r"^a mis-segmentation:\s*", "", (meaning or "").strip())
    first = CLAUSE.split(whole, maxsplit=1)[0]
    m = QUOTES.sub("", first).strip(" ,.")
    quoted = QUOTED.search(whole)
    if quoted and (len(m) < 4 or "+" in first):
        m = quoted.group(1).strip(" ,.")
    m = m or QUOTES.sub("", whole)
    return m if len(m) <= n else m[:n + 1].rsplit(" ", 1)[0].rstrip(" ,")


def entry(e):
    """One entry of the lexicon as the glosser needs it. level is what a word that is this entry counts as."""
    head = e["headword"].strip()
    bare = re.sub(r"\s*\([^)]*\)", "", head).lstrip("*").strip()
    starts, ends = bare.startswith(("-", "–")), bare.endswith(("-", "–"))
    affix = "infix" if starts and ends else "suffix" if starts else "prefix" if ends else ""
    cat = (e.get("category") or "").lower()
    kind = kind_of(cat) or ("function word" if affix else "")
    name = kind in NAME_KINDS or (not affix and bare[:1].isupper())
    meaning, status = (e.get("meaning_en") or "").strip(), e.get("status") or ""
    good = status in L.GOOD and bool(meaning)
    if good:
        level = "name" if name else "grammar" if kind == "function word" else "meaning"
    elif meaning and status == "hypothesis":
        level = "hypothesis"
    else:
        level = "kind" if (kind or name) else "unknown"
    forms = set()
    for h in [head] + list(e.get("variants") or []):
        forms |= L.corpus_spellings(h)
    return {"headword": head, "forms": forms, "affix": affix, "kind": kind or ("name" if name else ""),
            "level": level, "status": status, "meaning": meaning, "page": e.get("page_printed") or e.get("page_pdf"),
            "vague": level == "meaning" and bool(KIND_ONLY.match(meaning)),
            "confidence": CONFIDENCE.get(status, 1) if (good or level == "hypothesis") else 1}


SENDS_TO = re.compile(r"^(?:(?:a|an|the|graphic|archaic|late|rare|frequent|dialectal|simple)\s+)*variants?\s+of\s+(?:the\s+)?(\S+)"
                      r"|^see\s+(\S+)", re.I)


def bare(headword):
    """A headword without its number, its star and its hyphens: 'mẖe', '-se (1)' -> 'se'."""
    return re.sub(r"\s*\([^)]*\)", "", headword).strip("*-– ").strip(" ,.;:'\"")


def lexicon(raw=None):
    """The entries of the lexicon proper (the appendix of rejected glosses left out), best level first. An entry
    whose meaning only sends to another ("variant of mẖe", "see peseto") takes that entry's level, kind and
    meaning when it is the only entry of that name and stands higher."""
    raw = L.load() if raw is None else raw
    es = [entry(e) for e in raw if (e.get("page_pdf") or 0) < L.REJECTED_FROM]
    named = collections.defaultdict(list)
    for e in es:
        named[bare(e["headword"])].append(e)
    for e in es:
        m = SENDS_TO.match(e["meaning"])
        to = named.get(bare(m.group(1) or m.group(2)), []) if m else []
        if len(to) == 1 and to[0] is not e and RANK[to[0]["level"]] <= RANK[e["level"]] and to[0]["level"] in TRANSLATED:
            e.update(level=to[0]["level"], kind=to[0]["kind"], confidence=min(c for c in (e["confidence"], to[0]["confidence"]) if c > 1) if max(e["confidence"], to[0]["confidence"]) > 1 else 1,
                     meaning=f"{short(to[0]['meaning'])} ({e['meaning']})")
    return sorted(es, key=lambda e: (RANK[e["level"]], -e["confidence"]))


def index(es):
    """({spelling: entries that are words}, {spelling: entries that are endings or beginnings}, {headword: entry})."""
    words, affixes = collections.defaultdict(list), collections.defaultdict(list)
    for e in es:
        for f in e["forms"]:
            (affixes if e["affix"] else words)[f].append(e)
    return words, affixes, {e["headword"]: e for e in es}


def source(e):
    return f"Rilly 2003, p. {e['page']} ({e['headword']}, {e['status'] or 'no status'})"


# ---------------------------------------------------------------------------------------------- the lookup

def gloss(form, level, confidence, text, src, parts=(), kind="", by="lookup", **more):
    return {"form": form, "level": level, "confidence": confidence, "gloss": text, "kind": kind, "source": src,
            "parts": list(parts), "by": by, **more}


def of_entries(form, cands, parts=None, ending=""):
    """The gloss a word takes from the entries that own its spelling: the best one, the others named."""
    e = cands[0]
    senses = []                                    # the meanings of every entry at the best entry's level
    for c in cands:
        m = short(c["meaning"]) or (f"[{c['kind']}]" if c["kind"] else "[no gloss]")
        if RANK[c["level"]] == RANK[e["level"]] and m not in senses:
            senses.append(m)
    text = " / ".join(senses[:3]) if e["level"] == "meaning" else senses[0]      # two words, not two notes on one ending
    if ending:
        text += f" +{ending}"
    return gloss(form, e["level"], e["confidence"], text, source(e), kind=e["kind"],
                 parts=parts or [{"form": form, "entry": e["headword"]}], senses=len(cands), vague=e["vague"],
                 # open: another entry with this spelling is of a lower level, so the level rests on a choice
                 open=any(RANK[c["level"]] > RANK[e["level"]] for c in cands))


GRIFFITH_NAME = re.compile(r"n\. ?[A-C]+\b")      # Index C: "n. A." is the name of A, the person of the epitaph


def griffith_name(tok, printed):
    """The entry of Griffith's that prints a Karanog word as a name of its inscription (his table of names, or
    an index entry marked "n. A.", "n. B.", "n. C."), or "". A name with qowi or lowi written on is one too."""
    for ws, src, gl in printed or ():
        if tok in ws and (src.startswith("names table") or GRIFFITH_NAME.match(gl)):
            return f"Griffith 1911, {src}" + (f" ({gl})" if gl else "")
    return ""


def lookup(tok, prev, words, affixes, printed=None, two_signs=False):
    """The gloss of one word by lookup alone, or None for a word left to the analysts. prev is the word before it
    in the text: wi after a word in -lo or -qo is the particle of -lowi and qowi, written apart. printed is what
    Griffith prints for the word's inscription (griffith_entries), for a Karanog row. two_signs (the corrections):
    a stem of two signs counts as three letters when one of them is the sign se or ne."""
    if tok in ("NAME", "RNAME"):
        return gloss(tok, "name", 5, "NAME", "a name, masked in the corpus", kind="person name")
    if tok.isdigit():
        return gloss(tok, "number", 5, tok, "a numeral")
    if "." in tok or "|" in tok:
        return gloss(tok, "lost", 0, f"<{tok}>", "a word with a lost sign")
    if not PLAIN.fullmatch(tok):
        return None
    if tok == "wi" and prev and PLAIN.fullmatch(prev) and prev.endswith(("lo", "qo")):
        whole = affixes.get(prev[-2:] + "wi") or words.get(prev[-2:] + "wi")
        if whole:
            return of_entries(tok, whole, parts=[{"form": tok, "entry": whole[0]["headword"]}])
    cands = words.get(tok, []) + affixes.get(tok, [])
    if tok in L.FUNCTION and any(c["kind"] == "function word" for c in cands):
        cands = [c for c in cands if c["kind"] == "function word"]
    if cands:
        return of_entries(tok, sorted(cands, key=lambda e: (RANK[e["level"]], -e["confidence"])))
    best = None
    for end in L.SUFFIXES[1:]:
        stem = tok[:-len(end)]
        # two_signs: one of them se or ne, and an entry Rilly holds as established (a short stem must be sure)
        long = len(stem) >= 3 or (two_signs and len(stem) == 2 and any(c in SYLLABLE_SIGNS for c in stem)
                                  and stem in words and words[stem][0]["confidence"] == CONFIDENCE["established"])
        if tok.endswith(end) and long and stem in words and words[stem][0]["level"] not in ("kind", "unknown"):
            e = words[stem][0]
            key = (RANK[e["level"]], -e["confidence"], -len(stem))
            if best is None or key < best[0]:
                best = (key, stem, end)
    if best:
        _, stem, end = best
        g = of_entries(tok, words[stem], ending=end,
                       parts=[{"form": stem, "entry": words[stem][0]["headword"]}, {"form": end, "entry": "ending"}])
        # as for an analyst's cut, an ending whose function is open does not lower the level; the gloss records it
        # when the lexicon has the ending and gives none of its entries an accepted function
        owners = [e for e in affixes.get(end, []) if e["affix"] == "suffix"]
        g["open_grammar"] = bool(owners) and not any(e["level"] in TRANSLATED for e in owners)
        return g
    by = griffith_name(tok, printed)
    if by:
        end = next((e for e in ("qowi", "qo") if tok.endswith(e) and len(tok) > len(e) + 2), "")
        name = tok[:len(tok) - len(end)].capitalize()
        return gloss(tok, "name", 4, f"this is {name}" if end else name, by, kind="person name",
                     parts=[{"form": tok, "entry": "NAME"}])
    return None


# ---------------------------------------------------------------------------------------------- the texts

def texts(path=CORPUS):
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def group(row):
    """Which part of the corpus a text is from."""
    if row["id"].startswith("G-karanog"):
        return "Karanog and Shablul (Griffith 1911)"
    if row["id"].startswith("G-"):
        return "Griffith's other volumes"
    return "the older corpus (names masked)"


def distinct(rows, share=0.8):
    """The texts left when near-copies are counted once: going from the longest text down, a text is a copy when
    `share` or more of its runs of three words stand in one text already kept. (The older corpus holds families
    of such copies; one of them, the 86 texts that hold "aribet yete kemxr yetmdelowi", is about a third of its
    words.)"""
    tri = lambda t: {tuple(t[i:i + 3]) for i in range(len(t) - 2)} or {tuple(t)}
    kept, index = [], collections.defaultdict(set)
    for r in sorted(rows, key=lambda r: -len(r["text"].split())):
        g = tri(r["text"].split())
        shared = collections.Counter(k for x in g for k in index[x])
        if shared and max(shared.values()) / len(g) >= share:
            continue
        for x in g:
            index[x].add(len(kept))
        kept.append(r)
    ids = {r["id"] for r in kept}
    return [r for r in rows if r["id"] in ids]


def griffith_entries(row, refs=KAR_REFS):
    """Griffith's printed entries for a Karanog row, as [(words in the corpus spelling, source, his gloss)]."""
    m = re.fullmatch(r"G-karanog-(Sh)?(\d+)", row["id"])
    if not m:
        return []
    import karanog as K
    out = []
    for e in K.entries("Sh" if m.group(1) else "Kar", int(m.group(2)), refs):
        ws = [w for w in K.to_corpus(e["reading"]).split() if PLAIN.fullmatch(w)]
        if ws:
            out.append((ws, e["source"], e.get("gloss") or ""))
    return out


def hints(tok, printed):
    """What Griffith prints about a word of a Karanog text: up to three of his entries that are the word, hold it
    or are held by it (four letters or more)."""
    out = []
    for ws, src, gl in printed:
        if tok in ws or any(len(w) >= 4 and (w in tok or tok in w) for w in ws):
            line = f"{src}: {' '.join(ws)}" + (f" [{gl}]" if gl else "")
            if line not in out:
                out.append(line)
    return sorted(out, key=lambda l: ("names table" not in l and "Index" not in l, l))[:3]


def left(rows, words, affixes, refs=KAR_REFS, contexts=4, width=6):
    """The words the lookup leaves: [{word, count, texts, contexts, griffith}], the most frequent first."""
    seen = collections.defaultdict(lambda: {"count": 0, "texts": set(), "contexts": [], "griffith": []})
    for r in rows:
        toks, printed = r["text"].split(), griffith_entries(r, refs)
        for i, tok in enumerate(toks):
            if lookup(tok, toks[i - 1] if i else "", words, affixes, printed) is not None:
                continue
            s = seen[tok]
            s["count"] += 1
            if r["id"] not in s["texts"] and len(s["contexts"]) < contexts:
                s["contexts"].append(f"{r['id']}: " + " ".join(toks[max(0, i - width):i] + [f"[{tok}]"] + toks[i + 1:i + 1 + width]))
                for h in hints(tok, printed):
                    if h not in s["griffith"] and len(s["griffith"]) < 4:
                        s["griffith"].append(h)
            s["texts"].add(r["id"])
    out = [{"word": w, "count": s["count"], "texts": len(s["texts"]), "contexts": s["contexts"], "griffith": s["griffith"]}
           for w, s in seen.items()]
    return sorted(out, key=lambda x: (-x["count"], -x["texts"], x["word"]))


# ---------------------------------------------------------------------------------------------- the analysts

def lexicon_table(es):
    """The lexicon as the analysts see it: one line an entry."""
    lines = ["headword\tspellings in the corpus's letters\tis\tkind\tstatus\tmeaning\tpage"]
    for e in sorted(es, key=lambda e: e["headword"].lstrip("-–*").lower()):
        lines.append("\t".join([e["headword"], " ".join(sorted(e["forms"])), e["affix"] or "word", e["kind"],
                                e["status"], re.sub(r"\s+", " ", e["meaning"])[:150], str(e["page"])]))
    return "\n".join(lines) + "\n"


def write_packs(out, residue, es, per=110, again=0, more=False):
    """Packs A001... hold every word left, per words each; packs B001... hold the `again` most frequent once more,
    for a second analyst who sees nothing of the first. With more, only the words that no pack of out holds yet
    are written, into the A packs after the last one."""
    table = lexicon_table(es)
    made, first = [], 0
    if more:
        old = sorted(p for p in out.iterdir() if p.is_dir() and re.fullmatch(r"A\d+", p.name))
        have = {json.loads(l)["word"] for p in old for l in (p / "words.jsonl").read_text().splitlines() if l.strip()}
        # numbered after the highest pack, not after the count: a gap must not make a new pack overwrite an old one
        residue, again, first = [w for w in residue if w["word"] not in have], 0, max((int(p.name[1:]) for p in old), default=0)
    for letter, words in (("A", residue), ("B", residue[:again])):
        for k in range(0, len(words), per):
            pack = out / f"{letter}{k // per + 1 + (first if letter == 'A' else 0):03d}"
            pack.mkdir(parents=True, exist_ok=True)
            (pack / "words.jsonl").write_text("".join(json.dumps(w, ensure_ascii=False) + "\n" for w in words[k:k + per]))
            (pack / "lexicon.tsv").write_text(table)
            (pack / "BRIEF.md").write_text(BRIEF.read_text())
            made.append(pack.name)
    return made


def check(a, word, heads):
    """Why an analyst's answer for word can't be used, or "" when it can."""
    if not isinstance(a, dict) or a.get("word") != word:
        return "not an answer for this word"
    parts = a.get("parts")
    if not isinstance(parts, list) or not parts or not all(isinstance(p, dict) and isinstance(p.get("form"), str) and p["form"] for p in parts):
        return "no parts"
    if "".join(p["form"] for p in parts) != word:
        return "the parts do not spell the word"
    if not all(isinstance(p.get("entry"), str) for p in parts):
        return "a part without an entry"
    bad = [p["entry"] for p in parts if p["entry"] not in SPECIAL and p["entry"] not in heads]
    if bad:
        return f"not an entry of the lexicon: {bad[0]!r}"
    if not isinstance(a.get("kind"), str) or a["kind"] not in KINDS:
        return f"not a kind: {a.get('kind')!r}"
    if type(a.get("confidence")) is not int or a["confidence"] not in (1, 2, 3, 4, 5):
        return "confidence is not 1 to 5"
    if not all(isinstance(a.get(k), (str, type(None))) for k in ("gloss", "evidence", "recalled")):
        return "gloss, evidence or recalled is not text"
    return ""


def content(part, heads):
    """Is a part a word of its own (a stem, a name, a number, an unknown piece), not an ending or a beginning?
    ("ending" is the lookup's ending of a stem.)"""
    e = heads.get(part["entry"])
    return part["entry"] != "ending" and (e is None or e["kind"] != "function word")


def settle(a, heads):
    """The gloss of a word from one analyst's answer (already checked). The level is that of the parts that are
    words of their own; an ending or a beginning whose function is open does not lower it, and open_grammar
    records it: terikelowi is "begotten by" whatever its t- does."""
    levels, variant, shown, grammar = [], False, [], []
    for p in a["parts"]:
        e = heads.get(p["entry"])
        if e is None:
            levels.append({"NAME": "name", "NUMBER": "number", "?": "unknown"}[p["entry"]])
            shown.append({"NAME": p["form"].capitalize(), "NUMBER": p["form"], "?": f"<{p['form']}>"}[p["entry"]])
        else:
            (levels if content(p, heads) else grammar).append(e["level"])
            variant = variant or p["form"] not in e["forms"]
            shown.append(short(e["meaning"]) or f"[{e['kind'] or 'no gloss'}]")
    open_grammar = bool(levels) and any(l not in TRANSLATED for l in grammar)
    stems = [heads[p["entry"]] for p in a["parts"] if p["entry"] in heads and content(p, heads)]
    vague = bool(stems) and all(e["vague"] for e in stems if e["level"] == "meaning") and any(e["vague"] for e in stems)
    levels = levels or grammar
    worst = max(levels, key=RANK.get)
    kind = a["kind"]
    if worst in TRANSLATED:
        level = next(l for l in ("meaning", "name", "number", "grammar") if l in levels)
        if a["confidence"] < SURE:
            level = "hypothesis"                     # an unsure cut is a proposal
    elif worst == "unknown" and kind != "unknown" and a["confidence"] >= SURE:
        level = "kind"
    else:
        level = worst
    if level == "name" and kind not in NAME_KINDS:
        kind = "name"
    src = "; ".join(source(heads[p["entry"]]) for p in a["parts"] if p["entry"] in heads) or "the analyst, from the texts"
    return gloss(a["word"], level, a["confidence"], (a.get("gloss") or "").strip() or "-".join(shown), src, kind=kind,
                 parts=[{"form": p["form"], "entry": p["entry"]} for p in a["parts"]], by="analyst", variant=variant,
                 open_grammar=open_grammar, vague=vague,
                 evidence=(a.get("evidence") or "").strip(), recalled=(a.get("recalled") or "").strip())


def analyses(folder, heads):
    """({word: gloss}, report) from the analysts' answers in the packs of folder. A word analysed twice (a pack A
    and a pack B) keeps the first analyst's answer when the two give it the same level, and the answer of the
    lower level when they do not. report counts what was read, dropped and compared: how many words the two put
    at the same level, how many of those they also cut alike, and how many words each put at a translated level
    with the other."""
    answers, dropped, missing = collections.defaultdict(dict), [], []
    for pack in sorted(p for p in Path(folder).iterdir() if p.is_dir()):
        asked = [json.loads(l)["word"] for l in (pack / "words.jsonl").read_text().splitlines() if l.strip()]
        got = {}
        if (pack / "analysis.jsonl").exists():
            for n, line in enumerate((pack / "analysis.jsonl").read_text().splitlines(), 1):
                if not line.strip():
                    continue
                try:
                    a = json.loads(line)
                except ValueError:
                    dropped.append((pack.name, f"line {n}", "not JSON"))
                    continue
                w = a.get("word") if isinstance(a, dict) else None
                why = check(a, w, heads) if w in asked else "not a word of this pack"
                if why:
                    dropped.append((pack.name, str(w), why))
                elif w not in got:
                    got[w] = settle(a, heads)
        missing += [(pack.name, w) for w in asked if w not in got]
        for w, g in got.items():
            answers[w][pack.name[0]] = g
    out, twice, same_cut, same_side, differ = {}, 0, 0, 0, []
    done = collections.Counter()
    cut = lambda g: tuple(p["entry"] for p in g["parts"])
    for w, by in answers.items():
        first = by.get("A") or by["B"]
        if len(by) == 2:
            a, b = by["A"], by["B"]
            twice += 1
            same_side += (a["level"] in TRANSLATED) == (b["level"] in TRANSLATED)
            done.update(k for k, yes in (("first", a["level"] in TRANSLATED), ("second", b["level"] in TRANSLATED),
                                         ("both", a["level"] in TRANSLATED and b["level"] in TRANSLATED)) if yes)
            if RANK[a["level"]] == RANK[b["level"]]:
                same_cut += cut(a) == cut(b)
                first = dict(a, twice=True, cut_differs=cut(a) != cut(b))
            else:
                differ.append(w)
                first = dict(max((a, b), key=lambda g: RANK[g["level"]]), twice=True, differ=True)
        out[w] = first
    return out, {"analysed": len(out), "twice": twice, "same_level": twice - len(differ), "same_level_and_cut": same_cut,
                 "same_translated_or_not": same_side, "differ": differ, "translated_by": dict(done),
                 "dropped": dropped, "missing": missing}


# ---------------------------------------------------------------------------------------------- the map

def gloss_texts(rows, words, affixes, analysed=None, refs=KAR_REFS):
    """[(row, [gloss of each word])]: the lookup, then the analysts' answer, then unknown."""
    out = []
    for r in rows:
        toks, gs, printed = r["text"].split(), [], griffith_entries(r, refs)
        for i, tok in enumerate(toks):
            g = lookup(tok, toks[i - 1] if i else "", words, affixes, printed) or (analysed or {}).get(tok)
            gs.append(g or gloss(tok, "unknown", 0, f"<{tok}>", "not in the lexicon, not analysed", by="nobody"))
        out.append((r, gs))
    return out


def blockers(g, heads):
    """The pieces of a word that keep it from being translated, as [(piece, entry)]: an entry without an accepted
    meaning under its headword, an unknown piece under its letters (entry None). An ending or a beginning blocks
    only a word that has nothing else, since it does not lower the level of a word with a stem (settle); a word
    whose stems are all known stands untranslated because its cut is unsure, and blocks under its own letters.
    [] for a translated or a lost word."""
    if g["level"] in TRANSLATED or g["level"] == "lost":
        return []
    stems, ends = [], []
    for p in g["parts"]:
        e = heads.get(p["entry"])
        if e is not None and e["level"] not in TRANSLATED:
            (stems if content(p, heads) else ends).append((e["headword"], e))
        elif p["entry"] == "?":
            stems.append((p["form"], None))
    if any(content(p, heads) for p in g["parts"]):
        ends = []
    return stems or ends or [(g["form"], None)]


def figures(glossed):
    """Counts of words by level: for each part of the corpus, for all of it, for the texts left when near-copies
    are counted once, and for the different words (each spelling once, at the level it has most often)."""
    out = {}
    once = {r["id"] for r in distinct([r for r, _ in glossed])}
    spellings = collections.defaultdict(collections.Counter)
    for _, gs in glossed:
        for g in gs:
            spellings[g["form"]][g["level"]] += 1
    types = collections.Counter(c.most_common(1)[0][0] for c in spellings.values())
    n = sum(types.values())
    out["different words"] = {"texts": len(glossed), "words": n, "levels": {l: types[l] for l in LEVELS},
                              "translated": sum(types[l] for l in TRANSLATED), "translated_on_a_choice": 0,
                              "title_or_epithet_only": 0, "by": {}}
    for name in sorted({group(r) for r, _ in glossed}) + ["all", "near-copies counted once"]:
        part = [(r, gs) for r, gs in glossed
                if name == "all" or group(r) == name or (name == "near-copies counted once" and r["id"] in once)]
        levels = collections.Counter(g["level"] for _, gs in part for g in gs)
        done = [g for _, gs in part for g in gs if g["level"] in TRANSLATED]
        mine = [g for g in done if g["by"] == "analyst"]
        out[name] = {"texts": len(part), "words": sum(levels.values()), "levels": {l: levels[l] for l in LEVELS},
                     "translated": len(done), "translated_on_a_choice": sum(bool(g.get("open")) for g in done),
                     "title_or_epithet_only": sum(g["level"] == "meaning" and bool(g.get("vague")) for g in done),
                     "by_one_analyst": sum(not g.get("twice") for g in mine),
                     "by_a_spelling_variant": sum(bool(g.get("variant")) for g in mine),
                     "with_open_grammar": dict(collections.Counter(g["by"] for g in done if g.get("open_grammar"))),
                     "by": dict(collections.Counter(g["by"] for g in done))}
    return out


def ranking(glossed, heads):
    """The pieces without an accepted meaning, the one that blocks most texts first:
    [{piece, is, kind, level, words, texts, alone, all_texts, forms}]. A piece is a headword of the lexicon or
    letters that no entry explains (is), and the two stay apart when they are spelled alike. Its kind is the
    lexicon's for a headword that has one, otherwise what the analysts named for the words it stands in; its level
    is that of those words (most often), and for a headword the lexicon's own when that is higher. texts counts
    near-copies once (distinct()); alone counts those texts in which it is the only piece still untranslated (lost
    words apart), so that its meaning would complete them; words and all_texts count every text. The second value
    counts the texts themselves, near-copies once: how many have a word that is not lost (legible), how many of
    those have no such piece and how many have one, and the median share of their legible words translated."""
    seen = collections.defaultdict(lambda: {"words": 0, "texts": set(), "all": set(), "alone": 0, "entry": None,
                                            "forms": collections.Counter(), "kinds": collections.Counter(),
                                            "levels": collections.Counter()})
    once = {r["id"] for r in distinct([r for r, _ in glossed])}
    whole = one = 0
    shares = []
    for r, gs in glossed:
        here = collections.Counter()
        for g in gs:
            for b, e in blockers(g, heads):
                s = seen[b, e is not None]
                s["entry"] = e
                s["words"] += 1
                s["all"].add(r["id"])
                if r["id"] in once:
                    s["texts"].add(r["id"])
                s["forms"][g["form"]] += 1
                s["levels"][g["level"]] += 1
                own = e["kind"] if e is not None else ""
                kind = (own or g["kind"]) if len(g["parts"]) > 1 else (g["kind"] or own)
                if kind == "two words written as one":      # the kind of the whole, not of this piece
                    kind = own
                s["kinds"][kind or "unknown"] += 1
                here[b, e is not None] += 1
        read = [g for g in gs if g["level"] != "lost"]
        if r["id"] in once and read:
            whole += not here
            shares.append(sum(g["level"] in TRANSLATED for g in read) / len(read))
            if len(here) == 1:
                one += 1
                seen[next(iter(here))]["alone"] += 1
    rows = []
    for (b, is_entry), s in seen.items():
        level = s["levels"].most_common(1)[0][0]
        if is_entry:
            level = min(level, s["entry"]["level"], key=RANK.get)
        rows.append({"piece": b, "is": "headword" if is_entry else "letters", "kind": s["kinds"].most_common(1)[0][0],
                     "level": level, "words": s["words"], "texts": len(s["texts"]), "alone": s["alone"],
                     "all_texts": len(s["all"]), "forms": [f for f, _ in s["forms"].most_common(4)]})
    rows.sort(key=lambda x: (-x["texts"], -x["words"], x["piece"], x["is"]))
    return rows, {"texts": len(once), "legible": len(shares), "no_blocker": whole, "one_blocker": one,
                  "median": statistics.median(shares) if shares else 0.0}


# ---------------------------------------------------------------------------------------- the corrections

def fixed(g, rule, **change):
    """A gloss set right by one of the corrections: what it was stays in `was`."""
    return dict(g, by="correction", corrected=rule, was={"level": g["level"], "gloss": g["gloss"], "by": g["by"]},
                **change)


def name_tails(r, gs):
    """Rule 1: in the older corpus, the rest of a masked name of several words, directly after the mask, is part
    of the name. A name leaves one rest, so a word after a rest is not one (NAME_TAILS). Returns the number of
    words set right."""
    if group(r) != "the older corpus (names masked)":
        return 0
    forms, n = [g["form"] for g in gs], 0
    for i in range(1, len(gs)):
        t = next((t for t in NAME_TAILS if forms[i - 1] in MASKED and tuple(forms[i:i + len(t)]) == t), ())
        for k in range(i, i + len(t)):
            gs[k] = fixed(gs[k], "the rest of a masked name", level="name", confidence=4, gloss="NAME",
                          kind="person name", parts=[{"form": forms[k], "entry": "NAME"}],
                          source="the rest of a name of several words, left behind its mask by the padding of the "
                                 "older corpus")
        n += len(t)
    return n


def short_stems(gs, words, affixes):
    """Rule 2: a word the map leaves untranslated, which the lookup translates once a stem of two signs with se
    or ne counts as three letters."""
    n = 0
    for i, g in enumerate(gs):
        if g["level"] in TRANSLATED or g["level"] == "lost" or g.get("corrected"):
            continue
        new = lookup(g["form"], gs[i - 1]["form"] if i else "", words, affixes, two_signs=True)
        if new and new["level"] in TRANSLATED:
            gs[i] = fixed(g, "a stem of two signs", **{k: new[k] for k in ("level", "confidence", "gloss", "kind",
                                                                          "source", "parts")})
            n += 1
    return n


def written_whole(glossed):
    """In how many texts each plain word stands, written as one word."""
    out = collections.Counter()
    for _, gs in glossed:
        out.update({g["form"] for g in gs if PLAIN.fullmatch(g["form"])})
    return out


def joins(gs, words, affixes, whole):
    """Rule 3: two or three neighbouring words that are one word written apart. At least one of them is not
    translated, at least one has FRAGMENT letters or fewer, together they spell a word the lookup translates, and
    that word stands written as one in WRITTEN texts or more. The longer join is tried first; the words of a join
    are corrected, so no later join takes them. Returns the joins made as [(the words, the joined word)]."""
    made = []
    for i in range(len(gs)):
        for n in (3, 2):
            part = gs[i:i + n]
            forms = [g["form"] for g in part]
            if (len(part) < n or not all(PLAIN.fullmatch(f) for f in forms) or any(g.get("corrected") for g in part)
                    or all(g["level"] in TRANSLATED for g in part) or min(map(len, forms)) > FRAGMENT):
                continue
            word = "".join(forms)
            new = lookup(word, gs[i - 1]["form"] if i else "", words, affixes) if whole[word] >= WRITTEN else None
            if new and new["level"] in TRANSLATED:
                for k, g in enumerate(part):
                    gs[i + k] = fixed(g, "a word written apart", level=new["level"], confidence=new["confidence"],
                                      gloss=new["gloss"] if k == 0 else f"(part of {word})", kind=new["kind"],
                                      source=new["source"], parts=new["parts"] if k == 0 else [], joined=word)
                made.append((" ".join(forms), word))
                break
    return made


def confirmed_variants(path=VARIANTS):
    """The pieces that two blind checkers took for a spelling or a form of a word with an accepted meaning:
    {(piece, it is a headword): the word}, without the two set apart."""
    out = {}
    if not path.exists():
        return out
    lines = [l.split("\t") for l in path.read_text(encoding="utf-8").splitlines()[1:] if l.strip()]
    for piece, is_, word, accepted, *_ in lines:
        if accepted == "yes" and piece not in SET_APART:
            out[piece, is_ == "headword"] = word.split(" / ")[0]
    return out


def known_spellings(path=VARIANTS):
    """What rule 4 takes: {(piece, it is a headword): (the word, who read it so)}, the confirmed variants and the
    forms of "sister" (SISTER)."""
    out = {k: (w, CHECKED) for k, w in confirmed_variants(path).items()}
    out.update({(p, False): (w, FAMILIES) for p, w in SISTER.items()})
    return out


def spellings(gs, known, heads):
    """Rule 4: a word whose every blocking piece is a known spelling of a word with an accepted meaning takes
    that word's meaning. known is known_spellings()."""
    n = 0
    for i, g in enumerate(gs):
        blocks = {(b, e is not None) for b, e in blockers(g, heads)}
        if not blocks or g.get("corrected") or not blocks <= set(known):
            continue
        es = [(heads[known[b][0]], known[b][1]) for b in sorted(blocks) if known[b][0] in heads]
        if not es or any(e["level"] not in TRANSLATED for e, _ in es):
            continue
        e, by = es[0]
        gs[i] = fixed(g, "a spelling of a known word", level=e["level"], confidence=4, kind=e["kind"] or g["kind"],
                      gloss=(short(e["meaning"]) or f"[{e['kind'] or 'no gloss'}]") + f" (a form of {e['headword']})",
                      source=source(e) + f"; the spelling by {by}", parts=[{"form": g["form"], "entry": e["headword"]}])
        n += 1
    return n


def correct(glossed, words, affixes, heads, known=None):
    """The map with the four corrections, each word set right once and by the first rule that fits. Changes the
    glosses in place and returns what each rule did: the words it set right in every text, how many of those were
    not translated before, and the same with near-copies counted once. known: what rule 4 takes, by default
    known_spellings()."""
    known = known_spellings() if known is None else known
    whole = written_whole(glossed)
    once = {r["id"] for r in distinct([r for r, _ in glossed])}
    rules = ("the rest of a masked name", "a stem of two signs", "a word written apart", "a spelling of a known word")
    report = {rule: {"words": 0, "newly_translated": 0, "words_once": 0, "newly_translated_once": 0} for rule in rules}
    made = collections.Counter()
    for r, gs in glossed:
        name_tails(r, gs)
        short_stems(gs, words, affixes)
        made.update(joins(gs, words, affixes, whole))
        spellings(gs, known, heads)
        for g in gs:
            if g.get("corrected"):
                new = g["was"]["level"] not in TRANSLATED and g["level"] in TRANSLATED
                c = report[g["corrected"]]
                c["words"] += 1
                c["newly_translated"] += new
                c["words_once"] += r["id"] in once
                c["newly_translated_once"] += new and r["id"] in once
    report["joins"] = [[a, b, n] for (a, b), n in sorted(made.items(), key=lambda x: (-x[1], x[0]))]
    return report


def draft(gs):
    """The word-by-word line of a text."""
    return " ".join(g["gloss"] if g["level"] != "unknown" else f"<{g['form']}>" for g in gs)


COLUMNS = ("piece", "headword or letters", "kind", "level", "texts (near-copies once)", "texts it alone blocks",
           "words", "all texts", "spellings")


def public_list(ranked):
    """The public list of the pieces without an accepted meaning: counts and corpus spellings, no gloss."""
    rows = [[r["piece"], r["is"], r["kind"], r["level"], str(r["texts"]), str(r["alone"]), str(r["words"]),
             str(r["all_texts"]), " ".join(r["forms"])] for r in ranked]
    return "".join("\t".join(cells) + "\n" for cells in [list(COLUMNS)] + rows)


def write(glossed, ranked, figs, texts_by, report, out=OUT, public=None):
    out.mkdir(parents=True, exist_ok=True)
    with (out / "glosses.jsonl").open("w") as f:
        for r, gs in glossed:
            n = sum(g["level"] != "lost" for g in gs)
            f.write(json.dumps({"id": r["id"], "group": group(r), "text": r["text"], "draft": draft(gs),
                                "translated": sum(g["level"] in TRANSLATED for g in gs), "words": n, "glosses": gs},
                               ensure_ascii=False) + "\n")
    (out / "unknown_ranked.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in ranked))
    (out / "figures.json").write_text(json.dumps({"figures": figs, "texts": texts_by, "analysts": report},
                                                 ensure_ascii=False, indent=1) + "\n")
    if public:
        public.write_text(public_list(ranked))


def show(figs, texts_by=None):
    for name, f in figs.items():
        n = f["words"]
        print(f"{name}: {f['texts']} texts, {n} words; translated {f['translated']} ({f['translated'] / n:.1%}), "
              f"of them on a choice between entries {f['translated_on_a_choice']}, "
              f"known only as a title or an epithet {f['title_or_epithet_only']}")
        print("   " + ", ".join(f"{l} {f['levels'][l]} ({f['levels'][l] / n:.1%})" for l in LEVELS))
    if texts_by:
        t = texts_by
        print(f"texts, near-copies counted once: {t['texts']}, {t['legible']} with a word that is not lost; of those, "
              f"every such word translated in {t['no_blocker']}, one piece missing in {t['one_blocker']}; "
              f"the median text {t['median']:.1%} translated")


def main(argv):
    if len(argv) < 2 or argv[1] not in ("first", "packs", "build", "correct") or (argv[1] != "first" and len(argv) < 3):
        sys.exit(__doc__)
    es = lexicon()
    words, affixes, heads = index(es)
    rows = texts()
    if argv[1] == "first":
        glossed = gloss_texts(rows, words, affixes)
        show(figures(glossed))
        residue = left(rows, words, affixes)
        print(f"left to the analysts: {len(residue)} different words, {sum(w['count'] for w in residue)} in all; "
              f"seen once: {sum(w['count'] == 1 for w in residue)}")
        return
    folder = Path(argv[2])
    opt = lambda flag, default: int(argv[argv.index(flag) + 1]) if flag in argv else default
    if argv[1] == "packs":
        made = write_packs(folder, left(rows, words, affixes), es, per=opt("--per", 110), again=opt("--again", 0),
                           more="--more" in argv)
        print(f"{len(made)} packs written in {folder}" + (f": {made[0]} to {made[-1]}" if made else ""))
        return
    analysed, report = analyses(folder, heads)
    glossed = gloss_texts(rows, words, affixes, analysed)
    if argv[1] == "correct":
        report["corrections"] = correct(glossed, words, affixes, heads)
    figs = figures(glossed)
    ranked, texts_by = ranking(glossed, heads)
    if argv[1] == "correct":
        write(glossed, ranked, figs, texts_by, report, out=CORRECTED,
              public=PUBLIC_CORRECTED if "--public" in argv else None)
        for rule, c in report["corrections"].items():
            if rule != "joins":
                print(f"corrected, {rule}: {c['words']} words, {c['newly_translated']} of them not translated "
                      f"before (near-copies once: {c['words_once']}, {c['newly_translated_once']})")
    else:
        write(glossed, ranked, figs, texts_by, report, public=PUBLIC if "--public" in argv else None)
    show(figs, texts_by)
    by = report["translated_by"]
    print(f"analysts: {report['analysed']} words analysed; twice {report['twice']}, at the same level "
          f"{report['same_level']}, of them cut alike {report['same_level_and_cut']}, the same on translated or "
          f"not {report['same_translated_or_not']}; translated by the first "
          f"{by.get('first', 0)}, by the second {by.get('second', 0)}, by both {by.get('both', 0)}; "
          f"answers dropped {len(report['dropped'])}; words without an answer {len(report['missing'])}")
    a = figs["all"]
    print(f"of the {a['translated']} translated words: by an analyst {a['by'].get('analyst', 0)} (by one analyst alone "
          f"{a['by_one_analyst']}; through a spelling variant {a['by_a_spelling_variant']}); with an ending or "
          f"beginning of open function {sum(a['with_open_grammar'].values())} ({a['with_open_grammar']})")
    print(f"pieces without an accepted meaning: {len(ranked)}; the first: "
          + ", ".join(f"{r['piece']} ({r['kind']}, {r['texts']} texts)" for r in ranked[:12]))


if __name__ == "__main__":
    main(sys.argv)
