"""Track B of the evidence from outside the texts (data/discovery/outside_evidence.md, section 3): the royal and
temple texts read against frames built from the Kushite kings' Egyptian texts, as a blind test on known words.

The texts are the inscriptions of corpus_v6 whose kind is royal or temple or oracular decree, and every text of
100 words or more. Each is shown word by word: a word is the map's reading or a code. A word without a meaning is
a code. The known dictionary words that stand in these texts are dealt by lot into two halves; in each of two
folds one half is shown as codes too, drawn from the same numbering as the codes of the open words. Two aligners a
pack read it with the frames, two without. Two judges compare each answer for a hidden word with its meaning, and
with the meaning of another hidden word (a decoy). Gate B is counted on the arm with the frames.

What a pack shows of a word (token): the map's gloss in square brackets for a word it reads; a code for each
hidden entry of such a word and for an open word (levels hypothesis, unknown, kind), with the glosses of the
endings the map names beside it; a god's name in English; a code that says person, place or name; a number;
`[lost]`. No Meroitic letters: a gloss that names a Meroitic word is replaced or has the word blanked. The key says
what each code is, and for a hidden word the meaning its answers are judged against: the project's words of the
public table of the lexicon's sure entries, else the lexicon's English, else the map's reading.

A hidden word that stands in several packs is answered in each. The count takes it as given when both aligners
of one of its packs give it a meaning, and as right only when it is right in every pack where it is given
(arm_figures); the same count by word and pack stands beside it.

Everything is read and written under data/sources/frames/ (local only: the packs show the map), except `public`.
The six files frames_*.json there are the frame builders'; this script never writes them.

  python3 -I src/frames.py texts          the texts with their words and the four counts of the page (texts.json)
  python3 -I src/frames.py folds          the known words dealt into two halves (folds.json; drawn once)
  python3 -I src/frames.py packs          the packs of each fold, the key and the aligners' briefs (packs/, briefs/)
  python3 -I src/frames.py answers-check  each aligner's file against its pack and the frames (answers/<arm>/<pack>_<a|b>.jsonl)
  python3 -I src/frames.py judge-packs    the rows for two judges: answers for hidden words, each with a decoy (judge/)
  python3 -I src/frames.py count          gate B for the arm with the frames, the same count without (result.json)
  python3 -I src/frames.py open-packs     only once the gate is met: the open words' pairs of answers, for the judges (open/)
  python3 -I src/frames.py public         data/discovery/outside_frames_figures.json (counts only)

What the aligners and the judges are given is in runs/prompts/FRAMES_aligners.md and FRAMES_judges.md.
"""
import collections
import csv
import json
import pathlib
import random
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(ROOT / "src" / "v6")]
import coverage as C                                    # noqa: E402
import recurring as W                                   # noqa: E402
import themap as M                                      # noqa: E402
import words as D                                       # noqa: E402

HOME = ROOT / "data/sources/frames"
FOLDER = "data/sources/frames"                           # as the briefs name it
REPO = "/Users/mike/repos/mike/meroitic"                 # where the agents work
PUBLIC = ROOT / "data/discovery/outside_frames_figures.json"
TABLE = ROOT / "data/discovery/lexicon_statuses.tsv"     # the meanings in the project's own words (public)
SEED = 20261116
LAYERS = ("recurring", "rare_sure", "rare_later", "unnamed", "rare_millet", "leftover", "leftover_stems")   # the map when the test was set
LONG = 100                                               # words: a long text, and a pack of its own
PACK = 300                                               # words: about the size of a pack of shorter texts
PAGE = {"texts": 99, "words": 2945, "open": 1370, "known": 102, "places": 624}   # the page's counts: `texts` stops if its own differ
FOLDS = (1, 2)
ARMS = ("frames", "plain")                               # with the frames, and the pack alone
ALIGNERS = ("a", "b")
JUDGES = (1, 2)
VERDICTS = ("same", "partly", "another")
BARS = {"given_at_least": 10, "right": 0.80, "margin": 0.30, "kappa": 0.6}       # gate B, as the page states it
FRAMES = {"K": "the king's names, titles and epithets", "G": "the gods: epithets, speeches, hymns",
          "D": "dates, enthronement and journeys", "W": "war: the report of a campaign, the lists of booty and of captives",
          "O": "gifts and buildings: donations and offerings with their numbers, dedications",
          "P": "the texts of people who are not kings: officials, graffiti, oracles and decrees"}
JUDGE_PACK = 120                                         # rows in a judges' pack
WIDTH = 110                                              # a text's tokens are wrapped at this many characters

# What a pack may hold of Meroitic: nothing. A reading that names a Meroitic word is taken from another source or
# has the word blanked (clean, blank). These English words are spelled like a Meroitic word and stay.
ENGLISH = frozenset({"a", "are", "as", "at", "be", "on", "so", "to"})
ENGLISH_AS_WRITTEN = frozenset({"I", "O"})
# Gods the map's gloss does not name in English ("name of a deity", "a name (god)", "probably a variant of ..."):
# the name the lexicon's entry gives, its cross-reference followed.
GODS = {"Amnp": "Amanap", "Amnpte": "probably Amun of Napata", "Amnb": "probably Amun of Pnoubs", "Mne": "probably Amun",
        "Aritene": "Aritene"}
# The gloss of an ending, a prefix or a particle beside a code: the project's words of the public table, else the
# lexicon's first clause. Here those that name a Meroitic ending in them are said without it.
ENDINGS = {
    "-li (1)": "postposed article", "-lo": "article and copula, 'it is the'", "-lowi": "article and copula, 'it is the'",
    "-to (2)": "genitive, article and copula, 'it is of the'", "-se (2)": "suffix deriving nouns",
    "-lḫe": "article, likely with a postposition", "-t (2)": "genitive with the singular article, 'of the'",
    "-teb": "genitive with the plural article, 'of the'", "-le": "article, a late form", "-wit(w)": "a determiner, like the article",
    "-lebkwi": "plural article and plural copula, 'they are the'", "-lw (1)": "article with a postposition, or a form of the article",
    "-r": "ending of men's names", "-ose": "suffix used in forming titles", "-wi (5)": "optional particle following the copula",
    "ye- (2)": "verbal prefix (?)", "e-": "prefix (?) of the benediction verbs", "-i (1)": "suffix on the article",
    "-k (2)": "plural (?) copula, 'are'", "-ne (4)": "rare verbal suffix", "-ne (3)": "verbal suffix",
    "-ḫe (2)": "a nominal suffix or a postposition 'towards', 'for'", "a-": "rare variant of a verbal prefix (?)",
    "p- (2)": "a prefix or lexical element in some nouns", "-bte": "marks a plural object of the verb (?)",
    "-kene": "and also (?)", "-bto": "a suffix", "-ror": "element of personal names", "-m-": "negative particle (?)",
    "-yotise-": "until, as far as (?)", "-ni (1)": "suffix or determiner often placed after numerals",
    "-i (3)": "a nominalising suffix", "deqeni-": "an obscure element of royal texts and of personal names",
    "eqe-": "a preposed pronoun of the third person (?)",
}
GENERIC = re.compile(r"(?i)^(?:an? |the )?(?:divine |place )?name\b")            # a gloss that says "a name", not which
KIND_ONLY = re.compile(r"(?i)^(?:an? )?(?:adjective|noun|verb)\b[^'\"]*$")       # a gloss that says only the kind of word
REFERS = re.compile(r"(?i)\b(?:variant|form)s? ?(?:\(\?\))? ?of\b")              # "a form of ...": what follows names a word
ONLY_REFERS = re.compile(r"(?i)^(?:(?:probably|perhaps|rather|another|an?|the)\s+)*(?:variant|form)s? ?(?:\(\?\))? ?of\b")   # and says no more
ARTICLES = frozenset({"the", "a", "an", "this", "that"})
TAIL = re.compile(r"(?:\s*\+\s*\S+)+\s*$")                                       # the lookup's mark of an ending it does not name: "+lw"
WHOLE = re.compile(r"^\(?(?:part|(?:first|second|last) (?:piece|half)) of [^:)']+(?::\s*|\)\s*|(?='))")   # "part of xlbi: bull"
QUOTED_FIRST = re.compile(r"^('[^']+')\s*:.*$")                                  # "'I took': ye- 1sg + ..."
REMARK = re.compile(r"\s*\((?!\?\))[^()]*\)")                                    # a remark in round brackets; "(?)" stays
RUN = re.compile(r"(?<![^\W_])-?[^\W\d_]+(?:['’][^\W\d_]+)*(?:-[^\W\d_]+)*-?(?![^\W_])")   # a word with its hyphens, none beside a digit
PIECE = re.compile(r"^\(?(?:part|(?:first|second|last) (?:piece|half)) of\b|\((?:first|second) half\b|\((?:start|end) of\b")
NONE = re.compile(r"(?i)^\W*(?:none|no meaning|unknown|n/a)?\W*$")               # an answer that gives no meaning

MARKS = """Marks:

- `[ruler]`: a word the map of the corpus reads, by its reading in English; `(?)` in a reading: the map is unsure.
- `{code}`: a word whose reading is not shown, behind a code. The same code is the same word wherever it stands, in
  this pack and in the others. A code may be any kind of word.
- `+` joins what is written as one word: `{code}+[plural article]` is the word {code} with an ending the map names,
  `[verbal prefix (?)]+{code}` the same with a prefix. A code may be joined to a reading or to another code as well:
  one written word built of two.
- `PERSON-07`, `PLACE-03`: the name of a person, of a place; `NAME-02`: a name, the map does not say of what;
  `GOD-01`: a god the map does not name in English. The same name has the same code. A god the map names is a
  reading: `[Amun]`.
- `25`: a number. `[lost]`: a word with a lost sign. `[part of a word]`, `[part of a name]`: a piece written apart.
- A text is headed by a label and its kind. The lines are a wrap only: the lines of the stone are not kept.
"""

ALIGNER_BRIEF = """# Give each code of a pack of Meroitic texts a meaning, or "none"

Meroitic is written in a script that can be read aloud, but most of its words are not understood. The pack

    {repo}/{folder}/packs/{pack}.md

holds royal and temple texts, oracular decrees and long texts of the Meroitic corpus, word by word. Every word
stands in its place, one word a token. A word is shown either by its reading in English, as a word-by-word map of
the corpus has it, or by a code (`{code}`). You never see how a word is written. The head of the pack explains
the marks.

A code stands for one word: the same code is the same word wherever it stands, in this pack and in the others. A
code may be any kind of word: a noun, a verb, a title, an epithet, an adjective, a particle. For some of the codes
a meaning is known and is held back here, as a check; nothing in a code tells which.

{given}

**Your task.** Give every code of the pack a meaning in a few English words, or "none".

- "none" is a full answer. Never guess for the sake of an answer: give a meaning only where the places of the code
  give a reason for it{reason}.
- A code that stands in several places has one meaning: weigh all its places.
- The pack lists its codes at its end and states their number: {n}. Give one line for each of them, none left out
  and none twice: your file must have exactly {n} lines.

Write the lines to the file

    {answers}

(the path is relative to {repo}/), nothing else in it, one JSON line a code:

    {line}

- "meaning": a few English words, or "none".
{fields}- "why": one short sentence: what in the text decides it; for "none" it may be empty.

Work alone and use only {only}. Do not open any other file of the repository, do not search the web,
do not spawn agents, and write no file but your answers file. You may not look up the inscription: do not try to
work out which inscription a text is, and do not use what you may know of published translations of Meroitic
texts.

When the file is written, count its lines against {n}, then reply in one line: how many codes, and how many of
them you gave a meaning.
"""
# The two variants of the brief: what the aligner is given, what a reason is, the line and the fields of an answer.
GIVEN = {
    "frames": """You are also given six files of frames:

{files}

They were built from the Egyptian texts of the kings of Kush (8th to 1st century BC) in their editors' English,
by readers who saw no Meroitic text. A frame is a run of slots in a fixed order that stands in at least three of
those texts. Each file lists its frames under `frames`: a frame has an id (`K3`) and its slots in order, each with
its number (`n`), its meaning and the wording of the translation. Read the six files first. Then read each text
of the pack against them: where the readings, the names and the numbers of a Meroitic text follow a frame, a code
that stands in one of the frame's slots may have that slot's meaning.""",
    "plain": """You are given the pack alone. Read each text for what the readings, the names, the numbers and the order of
the words say about the codes among them.""",
}
REASON = {"frames": ": a frame that the words around it follow, with the code in one of its slots", "plain": ""}
LINE = {"frames": '{{"code": "{code}", "meaning": "a few English words, or none", "frame": "K3", "slot": 2, "why": "one short sentence"}}',
        "plain": '{{"code": "{code}", "meaning": "a few English words, or none", "why": "one short sentence"}}'}
FIELDS = {"frames": '- "frame" and "slot": the frame the meaning rests on, by its id in the six files, and the number of its slot.\n'
                    '  Every meaning you give rests on one; null for both where you give "none".\n', "plain": ""}
ONLY = {"frames": "the pack and the six files of frames", "plain": "the pack"}

JUDGE_BRIEF = """# Does an answer give the meaning of a word? {n} rows

Each row below pairs two short texts. The answer is what a reader took a word of a text to mean, from the text
around it; the reader did not see the word. The meaning is what is known of a word. For each row say whether the
answer gives that meaning.

- "same": the answer names what the meaning names: the same thing, person, deed or quality, in the same or in
  other words ("sovereign" for "king, ruler"; "to slay" for "to kill, slaughter"). Where the meaning lists several
  senses, one of them is enough. Words of doubt in either text ("probably", "(?)") do not count.
- "partly": the answer is wider or narrower than the meaning, or names something close to it of the same field
  ("an official" for "viceroy"; "a relative" for "nephew or niece"; "an offering" for "bread").
- "another": anything else: another meaning, or a meaning that does not say what the word means.

Many rows pair an answer with a meaning that is not its word's: you are not told which rows, and you are not told
who gave an answer or what the reader was given. Judge each row on its own, by the two texts alone.

For each row give one JSON line, in the order of this file, in the file `{answers}` (the path is relative to
{repo}/), nothing else in it:

    {{"row": "R0001", "verdict": "same"}}

Work alone: open no other file, do not search the web, do not spawn agents, and write no file but your answers
file. This file lists {n} rows: your file must have {n} lines. When it is written, count its lines against that
number, then reply in one line: how many rows, and how many of each verdict.
"""

OPEN_BRIEF = """# Do two answers give the same meaning? {n} rows

Each row below pairs two short answers. Two readers, each alone, said what a word of a text means, from the text
around it; they did not see the word. For each row say whether the two answers give the same meaning.

- "same": both name the same thing, person, deed or quality, in the same or in other words ("sovereign" and
  "king, ruler"; "to slay" and "to kill"). Words of doubt in either ("probably", "(?)") do not count.
- "partly": one is wider or narrower than the other, or they name close things of the same field ("an official"
  and "viceroy"; "an offering" and "bread").
- "another": anything else.

For each row give one JSON line, in the order of this file, in the file `{answers}` (the path is relative to
{repo}/), nothing else in it:

    {{"row": "P0001", "verdict": "same"}}

Work alone: open no other file, do not search the web, do not spawn agents, and write no file but your answers
file. This file lists {n} rows: your file must have {n} lines. When it is written, count its lines against that
number, then reply in one line: how many rows, and how many of each verdict.
"""


def read(path):
    return json.loads((HOME / path).read_text(encoding="utf-8"))


def write(path, data):
    (HOME / path).parent.mkdir(parents=True, exist_ok=True)
    (HOME / path).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def write_text(path, text):
    (HOME / path).parent.mkdir(parents=True, exist_ok=True)
    (HOME / path).write_text(text, encoding="utf-8")


# ------------------------------------------------------------------------------- readings without Meroitic letters

def meroitic(gl, lex):
    """Every spelling a pack must not show, lowercased: the words and the cut pieces of the whole map, and the
    lexicon's headwords, in its letters and in the corpus's."""
    out = set()
    for gs in gl.values():
        for g in gs:
            out.update([g["form"]] + [p["form"] for p in g.get("parts") or []])
    for h in lex:
        bare = re.sub(r"[-()]", "", re.sub(r"\s*\(\d+\)$", "", h))
        out.update([bare, bare.replace("ẖ", "X").replace("ḫ", "x")] + bare.split())
    return {f.lower() for f in out if f and not re.search(r"[\d.|]", f)}


def is_meroitic(word, mero):
    """Whether a run of letters is a Meroitic spelling. A capital standing alone is a label ("formula A", "whom X
    begot") unless it is one of the corpus's own capitals."""
    if word in ENGLISH_AS_WRITTEN or word.lower() in ENGLISH or (len(word) == 1 and word.isupper() and word not in "SNX"):
        return False
    return word.lower() in mero


def suspects(text, mero):
    """The runs of letters of a text that are Meroitic: a spelling of the map or a headword (ENGLISH aside), the
    notation of an ending or a prefix (`-lw`, `ye-`), or the word named after "a form of", "a variant of" (the
    lexicon in hand does not hold every word it refers to)."""
    out, named = [], {m.end() for m in REFERS.finditer(text or "")}
    for m in RUN.finditer(text or ""):
        run = m.group()
        after = any(m.start() - 1 <= at <= m.start() for at in named) and run.lower() not in ARTICLES
        if after or run.startswith("-") or run.endswith("-") or all(is_meroitic(p, mero) for p in run.split("-")):
            out.append(m)
    return out


def blank(text, mero):
    """A text with each Meroitic run replaced by a mark."""
    for m in reversed(suspects(text, mero)):
        text = text[:m.start()] + "…" + text[m.end():]
    return text


def clean(text, cut=True):
    """A gloss as a pack may show it: without the lookup's mark of an unnamed ending ("+lw"), without the spelling
    of the whole word a piece belongs to ("part of xlbi: bull"), its first clause only (`cut`: what follows a
    semicolon in the lexicon is comment), and without remarks in round brackets, which name spellings, guesses
    and the words beside it. "(?)" stays."""
    t = " ".join((text or "").split())
    if cut:
        t = t.split(";")[0]
    t = WHOLE.sub("", t)
    while REMARK.search(t):
        t = REMARK.sub("", t)
    t = TAIL.sub("", t)
    if cut:
        t = QUOTED_FIRST.sub(r"\1", t)
    return " ".join(t.replace("[", "").replace("]", "").split()).strip(" ,:/")


def shown(text, mero, cut=True):
    """clean(), and "" when what is left names a Meroitic word or nothing."""
    t = clean(text, cut)
    return "" if t in ("", "?", "(?)") or suspects(t, mero) else t


# ------------------------------------------------------------------------------------------------------ the texts

def the_map():
    """The map with the layers it had when the test was set."""
    names = tuple(l["name"] for l in M.LAYERS)
    if names[:len(LAYERS)] != LAYERS:
        raise SystemExit(f"the layers of the test are no longer {LAYERS}")
    return M.current(upto=len(LAYERS))


def with_a_meaning(gl, lex):
    """The dictionary words in use that have a meaning on the map: those the lexicon calls established or probable
    and those a layer gives one from a later source (the north star's count, src/themap.py)."""
    layers = [(l["name"], M.lines_of(l)) for l in M.LAYERS[:len(LAYERS)]]
    known, _, _ = D.population_of(gl, lex, fix=True)
    return set(D.translated(known, lex)) | {w for v in M.given_by_layers(layers, known, lex).values() for w in v}


def chosen(gl, rows):
    """The texts of the test, in the corpus's order: royal or temple, oracular decree, or 100 words or more."""
    return [t for t in rows if t in gl and (rows[t]["kind"].startswith("royal") or rows[t]["kind"] == "oracular decree" or len(gl[t]) >= LONG)]


def kind_shown(kind):
    return "royal or temple" if kind.startswith("royal") else "oracular decree" if kind == "oracular decree" else "long text"


def places_of(texts, done):
    """entry -> the [text, index] where a known word stands: the word's level is `meaning` and one of its parts has
    that entry."""
    out = collections.defaultdict(list)
    for t, gs in texts:
        for i, g in enumerate(gs):
            if g["level"] == "meaning":
                for e in sorted({p.get("entry") for p in g.get("parts") or []} & done):
                    out[e].append([t, i])
    return dict(sorted(out.items()))


def counts_of(texts, places):
    return {"texts": len(texts), "words": sum(len(gs) for _, gs in texts),
            "open": sum(g["level"] in W.OPEN for _, gs in texts for g in gs),
            "known": len(places), "places": sum(map(len, places.values()))}


def is_piece(g):
    return g.get("why") == "piece" or bool(PIECE.search(g.get("gloss") or "")) or (not g.get("parts") and g["level"] in W.READ + ("name",))


def meaning_to_judge(e, lex, table, glosses):
    """(the meaning a hidden word's answers are judged against, where it is from): the project's own words of the
    public table; else the lexicon's English; else, where the lexicon gives none (a word a layer gave its meaning
    from a later source), the map's reading at its places."""
    if (table.get(e) or "").strip():
        return table[e].strip(), "the project's words (lexicon_statuses.tsv)"
    if (lex[e].get("meaning") or "").strip():
        return lex[e]["meaning"].strip(), "the lexicon's English"
    return collections.Counter(TAIL.sub("", g) for g in glosses).most_common(1)[0][0], "the map's reading (a later source, laid by a layer)"


def ending_gloss(e, lex, table, mero):
    """What a pack shows of an ending, a prefix or a particle beside a code: ENDINGS, else the public table's
    words, else the lexicon's first clause; "" when none is left without a Meroitic word. An entry the lexicon does
    not call established or probable is marked unsure."""
    text = ENDINGS.get(e) or shown(table.get(e), mero, cut=False) or shown(lex[e].get("meaning"), mero)
    unsure = (lex[e].get("status") or "") not in W.SURE and text and "?" not in text
    return f"{text} (?)" if unsure else text


def god_names(texts, lex, mero):
    """entry -> the god's name in English: the map's commonest gloss where the name stands alone and the gloss
    names it; else the lexicon's; else GODS."""
    seen = collections.defaultdict(collections.Counter)
    for _, gs in texts:
        for g in gs:
            es = [p.get("entry") for p in g.get("parts") or [] if p.get("entry") != "ending"]
            if g["level"] == "name" and len(es) == 1 and es[0] in lex and lex[es[0]].get("kind") == "god name":
                text = shown(g.get("gloss"), mero)
                if text and not GENERIC.search(text):
                    seen[es[0]][text] += 1
    out = {}
    for e in sorted(h for h in lex if lex[h].get("kind") == "god name"):
        text = shown(lex[e].get("meaning"), mero)
        out[e] = seen[e].most_common(1)[0][0] if seen[e] else text if text and not GENERIC.search(text) else GODS.get(e, "")
    return out


def reading_of(g, known, entries, mero):
    """What a pack shows of a word the map reads when none of its entries is hidden: the map's gloss, cleaned. Where
    that names a Meroitic word, is empty, or says only the kind of word, the meanings of the word's known entries
    stand for it; a piece of a word that names no known entry is shown as a piece, without the whole word's
    meaning. Failing those: the glosses of its endings where the word is made of them (not where a layer laid
    the reading: the parts are the base's), else the gloss with its Meroitic words blanked."""
    mine = [e for e in (p.get("entry") for p in g.get("parts") or []) if e in known]
    if is_piece(g) and not mine:
        return "part of a word"
    text = shown(g.get("gloss"), mero)
    own = " + ".join(dict.fromkeys(known[e]["reading"] for e in mine if known[e]["reading"]))
    if text and not (own and KIND_ONLY.search(text)):
        return text
    if own:
        return own
    parts = [entries.get(p.get("entry"), {}) for p in g.get("parts") or []]
    if parts and not g.get("layer") and all(p.get("class") == "affix" and p.get("gloss") for p in parts):
        return " + ".join(p["gloss"] for p in parts)
    return blank(clean(g.get("gloss")), mero).strip(" ,:/…") or "?"


def texts_of(gl, rows, lex, table):
    """What `texts` writes: the texts with their words as the packs need them, the known words with the meaning to
    judge against, what is known of each entry that is a part of a word, and the four counts."""
    ids = chosen(gl, rows)
    texts = [(t, gl[t]) for t in ids]
    places = places_of(texts, with_a_meaning(gl, lex))
    mero = meroitic(gl, lex)
    known = {}
    for e, ps in places.items():
        meaning, source = meaning_to_judge(e, lex, table, [gl[t][i].get("gloss") or "" for t, i in ps])
        reading = shown(meaning, mero, cut=source != "the project's words (lexicon_statuses.tsv)") or blank(clean(meaning), mero)
        known[e] = {"kind": lex[e].get("kind") or "", "places": len(ps), "texts": len({t for t, _ in ps}), "meaning": meaning, "from": source,
                    "names_another_word": bool(ONLY_REFERS.search(meaning)), "reading": reading}
    gods = god_names(texts, lex, mero)
    entries = {}
    for e in sorted({p.get("entry") for _, gs in texts for g in gs for p in g.get("parts") or []} & set(lex)):
        kind = lex[e].get("kind") or ""
        if e in known:
            entries[e] = {"class": "known", "kind": kind}
        elif kind in C.NAME_KINDS:
            entries[e] = {"class": "name", "kind": kind} | ({"god": gods[e]} if kind == "god name" and gods.get(e) else {})
        elif D.ending(e, lex):
            entries[e] = {"class": "affix", "kind": kind, "gloss": ending_gloss(e, lex, table, mero)}
        else:
            entries[e] = {"class": "stem", "kind": kind} | ({"bound": True} if W.affix(e) else {})
    out = []
    for t, gs in texts:
        ws = []
        for g in gs:
            w = {"form": g["form"], "level": g["level"], "kind": g.get("kind") or "", "gloss": g.get("gloss") or "",
                 "parts": [[p.get("form") or "", p.get("entry") or ""] for p in g.get("parts") or []], "piece": is_piece(g)}
            if g["level"] in W.READ:
                w["reading"] = reading_of(g, known, entries, mero)
            ws.append(w)
        out.append({"id": t, "kind": kind_shown(rows[t]["kind"]), "words": ws})
    return {"counts": counts_of(texts, places), "seed": SEED, "layers": list(LAYERS), "texts": out, "known": known, "entries": entries}


def the_table():
    with open(TABLE, encoding="utf-8", newline="") as f:
        return {r["headword"]: r["meaning_in_our_words"] for r in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)}


def texts():
    data = texts_of(the_map(), W.corpus_rows(), W.lexicon(), the_table())
    print(data["counts"])
    if data["counts"] != PAGE:
        raise SystemExit(f"the counts are not the page's {PAGE}: nothing is written")
    if (HOME / "folds.json").exists() and (HOME / "texts.json").exists() and read("texts.json") != data:
        raise SystemExit("the folds are drawn and the texts would differ from texts.json: nothing is written")
    write("texts.json", data)


# ------------------------------------------------------------------------------------------------------ the folds

def folds_of(known, seed=SEED):
    """The known words dealt by lot into two halves: the sorted list shuffled, the first half and the rest. Fold n
    hides half n."""
    order = sorted(known)
    random.Random(seed).shuffle(order)
    half = (len(order) + 1) // 2
    return {"seed": seed, "halves": {"1": sorted(order[:half]), "2": sorted(order[half:])}}


def folds():
    if (HOME / "folds.json").exists():
        raise SystemExit("the folds are drawn: not drawn again")
    out = folds_of(read("texts.json")["known"])
    write("folds.json", out)
    print({k: len(v) for k, v in out["halves"].items()})


# ------------------------------------------------------------------------------------------------------ the packs

def packs_of(texts):
    """The texts in packs, as lists of their indexes: the texts under 100 words in the corpus's order, in packs of
    about PACK words (as many packs as their words make, each text where its middle falls), then each text of 100
    words or more as a pack of its own. A text is never split."""
    short = [i for i, t in enumerate(texts) if len(t["words"]) < LONG]
    total = sum(len(texts[i]["words"]) for i in short)
    n = max(1, round(total / PACK))
    out, before = [[] for _ in range(n)], 0
    for i in short:
        size = len(texts[i]["words"])
        out[min(n - 1, int((before + size / 2) * n / total))].append(i)
        before += size
    return [p for p in out if p] + [[i] for i, t in enumerate(texts) if len(t["words"]) >= LONG]


def open_units(w, entries):
    """What the codes of an open word stand for, as [(the part's number, the unit)]; (None, ...) where one code
    stands for the whole word. A unit is ("entry", a headword) or ("spelling", letters).

    Where the map names every part: each stem that is an entry without a meaning has its own code. Without one,
    the code stands for the word's first known entry (a known word at a place where the map is unsure), else for
    its first stem written with a hyphen, else for a name in it; an ending or a particle standing alone is its
    own stem. Where the map leaves one piece unnamed and names the rest as endings, the code stands for that
    piece (the stem of src/words.py). Any other word is coded by its whole spelling."""
    parts = w["parts"]
    kinds = [entries[e]["class"] if e in entries else e for _, e in parts]
    if "?" not in kinds:
        free = [i for i, k in enumerate(kinds) if k == "stem" and not entries[parts[i][1]].get("bound")]
        if free:
            return [(i, ("entry", parts[i][1])) for i in free]
        for wanted in (("known",), ("stem",), ("name", "NAME")):
            at = [i for i, k in enumerate(kinds) if k in wanted]
            if at:
                return [(at[0], ("spelling", parts[at[0]][0]) if kinds[at[0]] == "NAME" else ("entry", parts[at[0]][1]))]
        if kinds == ["affix"]:
            return [(0, ("entry", parts[0][1]))]
    elif kinds.count("?") == 1 and all(k in ("?", "affix", "ending") for k in kinds):
        return [(kinds.index("?"), ("spelling", parts[kinds.index("?")][0]))]
    return [(None, ("spelling", w["form"]))]


def units_of(w, entries, hidden):
    """The coded units of a word in a fold: each hidden entry of a word the map reads, or the units of an open word."""
    if w["level"] in W.READ:
        return [("hidden", e) for e in dict.fromkeys(e for _, e in w["parts"] if e in hidden)]
    return list(dict.fromkeys(u for _, u in open_units(w, entries))) if w["level"] in W.OPEN else []


def codes_of(texts, entries, hidden, fold, seed=SEED):
    """unit -> its code. The hidden entries and the open words' units are numbered together after one shuffle, so
    nothing in a code tells which of the two it is."""
    units = sorted({u for t in texts for w in t["words"] for u in units_of(w, entries, hidden)})
    random.Random(seed + fold).shuffle(units)
    width = max(3, len(str(len(units))))
    return {u: f"W{n:0{width}d}" for n, u in enumerate(units, 1)}


def name_of(w, entries):
    """(what a name's code stands for, its kind), or None for a piece of a name written apart."""
    named = [(f, e) for f, e in w["parts"] if e == "NAME" or entries.get(e, {}).get("class") == "name"]
    if not named and (w["piece"] or not w["parts"]):
        return None
    f, e = named[0] if named else (w["form"], "")
    kind = w["kind"] if w["kind"] in C.NAME_KINDS[:3] else entries.get(e, {}).get("kind") or ""
    if kind not in C.NAME_KINDS[:3]:
        kind = next((k for k in C.NAME_KINDS[:3] if f"({k.split()[0]})" in w["gloss"]), "name")
    return (e if e in entries else f"spelled {f}"), kind


def names_of(texts, entries):
    """name -> its code, numbered by kind in the order the names first stand: PERSON-01, PLACE-01, NAME-01, and
    GOD-01 for a god the map does not name in English."""
    out, n = {}, collections.Counter()
    for t in texts:
        for w in t["words"]:
            got = name_of(w, entries) if w["level"] == "name" else None
            if got and got[0] not in out and not (got[1] == "god name" and entries.get(got[0], {}).get("god")):
                label = {"person name": "PERSON", "place name": "PLACE", "god name": "GOD"}.get(got[1], "NAME")
                n[label] += 1
                out[got[0]] = f"{label}-{n[label]:02d}"
    return out


def beside(w, entries, at):
    """A coded word as its parts, joined by "+": `at` gives the token of a part (a code, a name, the reading of a
    known entry that is not hidden) or None; an ending, a prefix or a particle the map names is shown by its
    gloss; what else the word holds is not shown."""
    out = []
    for i, (_, e) in enumerate(w["parts"]):
        tok = at(i, e)
        if tok is None and entries.get(e, {}).get("class") == "affix" and entries[e].get("gloss"):
            tok = f"[{entries[e]['gloss']}]"
        if tok:
            out.append(tok)
    return "+".join(out)


def token(w, entries, known, hidden, code, names):
    """One word as a pack shows it: a reading or a code, never a spelling."""
    level = w["level"]
    if level == "lost":
        return "[lost]"
    if level == "number":
        return w["form"]
    if level == "name":
        got = name_of(w, entries)
        if got is None:
            return "[part of a name]"
        head = names.get(got[0]) or f"[{entries[got[0]]['god']}]"
        first = next((i for i, (f, e) in enumerate(w["parts"]) if e == "NAME" or entries.get(e, {}).get("class") == "name"), None)
        return beside(w, entries, lambda i, e: head if i == first else None) if first is not None else head
    other = lambda e: f"[{known[e]['reading']}]" if e in known and e not in hidden else None       # noqa: E731
    if level in W.OPEN:
        plan = open_units(w, entries)
        if plan[0][0] is None:
            return code[plan[0][1]]
        return beside(w, entries, lambda i, e: code[dict(plan)[i]] if i in dict(plan) else other(e))
    if not any(e in hidden for _, e in w["parts"]):
        return f"[{w['reading']}]"
    return beside(w, entries, lambda i, e: code["hidden", e] if e in hidden else other(e))


def wrap(tokens, width=WIDTH):
    lines, line = [], ""
    for tok in tokens:
        if line and len(line) + 1 + len(tok) > width:
            lines.append(line)
            line = tok
        else:
            line = f"{line} {tok}" if line else tok
    return lines + ([line] if line else [])


def example(codes):
    """A code of the shape of a pack's codes, for the marks and the brief."""
    return "W" + "0123456789"[:len(codes[0]) - 1 if codes else 3]


def pack_text(name, toks, codes):
    """A pack: its head with the marks, each text under a neutral label and its kind, and the codes to answer."""
    words = sum(len(ts) for _, _, ts in toks)
    out = [f"# Pack {name}: {len(toks)} Meroitic text{'s' if len(toks) != 1 else ''}, {words} words, {len(codes)} codes", "",
           MARKS.format(code=example(codes))]
    for label, kind, ts in toks:
        out += [f"## {label} ({kind}, {len(ts)} word{'s' if len(ts) != 1 else ''})", ""] + wrap(ts) + [""]
    out += [f"## The codes of this pack: {len(codes)}", "", f"Give each of these {len(codes)} codes one line in your answers file.", ""]
    return "\n".join(out + wrap(codes, 80)) + "\n"


def decoys_of(hidden, known, rng):
    """entry -> the hidden word whose meaning is its decoy: another hidden word of the fold and of its kind, drawn
    by lot among those whose meaning shares no content word with its own (two words for "to give" are no decoys
    of each other) and says what its word means (not "another form of ..."); of another kind where the kind has
    none. One decoy a hidden word: every answer for the word is paired with the same meaning, so that the decoys
    are counted as the words are."""
    out = {}
    for e in sorted(hidden):
        far = [o for o in sorted(hidden) if o != e and not known[o]["names_another_word"]
               and not W.content(known[o]["meaning"]) & W.content(known[e]["meaning"])]
        same = [o for o in far if known[o]["kind"] == known[e]["kind"]]
        if not far:
            raise SystemExit(f"no hidden word of the fold has a meaning apart from that of {e}: it has no decoy")
        out[e] = rng.choice(same or far)
    return out


def labels_of(texts, groups):
    """text index -> its neutral label, numbered in the order of the packs."""
    order = [i for g in groups for i in g]
    return {i: f"Text {n:0{max(2, len(str(len(order))))}d}" for n, i in enumerate(order, 1)}


def build(data, halves, seed=SEED):
    """Every pack of both folds as text, and the key. `halves` is folds.json's."""
    texts, entries, known = data["texts"], data["entries"], data["known"]
    groups = packs_of(texts)
    labels, names = labels_of(texts, groups), names_of(texts, entries)
    key = {"seed": seed, "packs": {f"p{n:02d}": {"texts": {labels[i]: texts[i]["id"] for i in g}, "words": sum(len(texts[i]["words"]) for i in g)}
                                   for n, g in enumerate(groups, 1)},
           "names": {c: n for n, c in names.items()}, "folds": {}}
    files, rng = {}, random.Random(seed)
    for fold in FOLDS:
        hidden = set(halves[str(fold)])
        code, decoy = codes_of(texts, entries, hidden, fold, seed), decoys_of(hidden, known, rng)
        of = {c: {"fold": fold, "sort": "hidden" if s == "hidden" else "open", "entry" if s != "spelling" else "spelling": u,
                  "kind": (known[u]["kind"] if s == "hidden" else entries[u]["kind"] if s == "entry" else ""), "packs": [], "places": 0}
              for (s, u), c in code.items()}
        for c, k in of.items():
            if k["sort"] == "hidden":
                e = k["entry"]
                k |= {"meaning": known[e]["meaning"], "from": known[e]["from"], "names_another_word": known[e]["names_another_word"],
                      "decoy": decoy[e], "decoy_meaning": known[decoy[e]]["meaning"]}
            elif k.get("entry") in known:
                k["known_where_the_map_is_sure"] = True
        in_pack = {}
        for n, g in enumerate(groups, 1):
            name, toks, mine = f"f{fold}_p{n:02d}", [], set()
            for i in g:
                toks.append((labels[i], texts[i]["kind"], [token(w, entries, known, hidden, code, names) for w in texts[i]["words"]]))
                for w in texts[i]["words"]:
                    for u in units_of(w, entries, hidden):
                        of[code[u]]["places"] += 1
                        mine.add(code[u])
                        if of[code[u]]["sort"] == "open" and not of[code[u]]["kind"]:
                            of[code[u]]["kind"] = w["kind"]
            for c in sorted(mine):
                of[c]["packs"].append(name)
            in_pack[name] = sorted(mine)
            files[name] = pack_text(name, toks, in_pack[name])
        key["folds"][str(fold)] = {"hidden": sorted(hidden), "codes": dict(sorted(of.items())), "packs": in_pack}
    return files, key


def brief_of(arm, pack, aligner, n, code="W012"):
    """The brief of one aligner: the arm's variant, with its pack, its answers file and the number of codes."""
    files = "\n".join(f"    {REPO}/{FOLDER}/frames_{k}.json   ({what})" for k, what in FRAMES.items())
    return ALIGNER_BRIEF.format(repo=REPO, folder=FOLDER, pack=pack, code=code, n=n, given=GIVEN[arm].format(files=files),
                                reason=REASON[arm], line=LINE[arm].format(code=code), fields=FIELDS[arm], only=ONLY[arm],
                                answers=f"{FOLDER}/answers/{arm}/{pack}_{aligner}.jsonl")


def answer_files():
    return sorted((HOME / "answers").glob("*/*.jsonl")) if (HOME / "answers").exists() else []


def packs():
    if answer_files():
        raise SystemExit("aligners have answered: the packs are not written again")
    files, key = build(read("texts.json"), read("folds.json")["halves"])
    for name, text in files.items():
        write_text(f"packs/{name}.md", text)
    write("packs/key.json", key)
    for fold in FOLDS:
        f = key["folds"][str(fold)]
        for pack, codes in f["packs"].items():
            for arm in ARMS:
                for a in ALIGNERS:
                    write_text(f"briefs/{arm}/{pack}_{a}.md", brief_of(arm, pack, a, len(codes), example(codes)))
        sorts = collections.Counter(k["sort"] for k in f["codes"].values())
        print(f"fold {fold}: {len(f['packs'])} packs; codes: {sorts['hidden']} hidden, {sorts['open']} open")
        for pack, codes in f["packs"].items():
            c = collections.Counter(f["codes"][x]["sort"] for x in codes)
            print(f"  {pack}: {len(key['packs'][pack[3:]]['texts'])} texts, {key['packs'][pack[3:]]['words']} words, {len(codes)} codes ({c['hidden']} hidden, {c['open']} open)")


# ---------------------------------------------------------------------------------------------------- the answers

def meaning_given(answer):
    """The meaning an answer gives, its spaces squeezed; None for "none", an empty answer or no answer."""
    m = answer.get("meaning") if isinstance(answer, dict) else None
    m = " ".join(m.split()) if isinstance(m, str) else ""
    return None if NONE.match(m) else m


def frame_slots():
    """frame id -> the numbers of its slots, from the six files of the frame builders; {} while one is missing."""
    out = {}
    for k in FRAMES:
        f = HOME / f"frames_{k}.json"
        if not f.exists():
            return {}
        for frame in json.loads(f.read_text(encoding="utf-8")).get("frames") or []:
            out[frame["id"]] = {slot.get("n") for slot in frame.get("slots") or []}
    return out


def slot_of(answer):
    """The slot an answer names, as a number where it is written as one ("2")."""
    slot = answer.get("slot")
    return int(slot) if isinstance(slot, str) and slot.strip().isdigit() else slot


def check_answers(text, codes, arm="plain", frames=None):
    """(code -> its line, what is wrong with an aligner's file): every line a JSON object, every code of the pack
    answered once and no other, a meaning in each (a text, "none" included), and with the frames a frame and a
    slot for every meaning that is not "none": one of the frames of the six files (`frames`: frame_slots()),
    and one of its slots."""
    got, wrong = {}, []
    for n, line in enumerate((l for l in text.splitlines() if l.strip()), 1):
        try:
            a = json.loads(line)
        except json.JSONDecodeError:
            wrong.append(f"line {n} is no JSON")
            continue
        c = a.get("code") if isinstance(a, dict) else None
        if c not in codes:
            wrong.append(f"line {n}: {c!r} is no code of the pack")
        elif c in got:
            wrong.append(f"{c} is answered twice")
        elif not isinstance(a.get("meaning"), str) or not a["meaning"].strip():
            wrong.append(f"{c} has no meaning (\"none\" is one)")
        elif arm == "frames" and meaning_given(a) is not None and (not a.get("frame") or a.get("slot") is None):
            wrong.append(f"{c} has a meaning that names no frame and slot")
        elif arm == "frames" and meaning_given(a) is not None and frames and slot_of(a) not in frames.get(a["frame"], ()):
            wrong.append(f"{c} names a frame or a slot that the six files do not have")
        else:
            got[c] = a
    missing = [c for c in codes if c not in got]
    if missing:
        wrong.append(f"{len(missing)} codes without a valid line: {', '.join(missing[:5])}{' ...' if len(missing) > 5 else ''}")
    return got, wrong


def the_answers(key, folder=None):
    """(arm, pack, aligner) -> (code -> line) for every aligner's file, and what is wrong or missing, by file."""
    folder, got, wrong, frames = folder or HOME / "answers", {}, {}, frame_slots()
    for arm in ARMS:
        for fold in FOLDS:
            for pack, codes in key["folds"][str(fold)]["packs"].items():
                for a in ALIGNERS:
                    f = folder / arm / f"{pack}_{a}.jsonl"
                    if not f.exists():
                        wrong[f"{arm}/{f.name}"] = ["no file"]
                        continue
                    got[arm, pack, a], bad = check_answers(f.read_text(encoding="utf-8"), codes, arm, frames)
                    if bad:
                        wrong[f"{arm}/{f.name}"] = bad
    return got, wrong


def answers_check():
    key = read("packs/key.json")
    got, wrong = the_answers(key)
    for (arm, pack, a), lines in sorted(got.items()):
        given = sum(meaning_given(x) is not None for x in lines.values())
        print(f"{arm}/{pack}_{a}: {len(lines)} of {len(key['folds'][pack[1]]['packs'][pack])} codes, {given} with a meaning"
              + ("" if f"{arm}/{pack}_{a}.jsonl" not in wrong else "  NOT VALID"))
    for f, bad in sorted(wrong.items()):
        print(f"{f}: " + "; ".join(bad))
    if wrong:
        raise SystemExit(f"{len(wrong)} of {len(FOLDS) * len(ARMS) * len(ALIGNERS) * len(key['packs'])} files are missing or not valid")
    print("every file is valid")


# ----------------------------------------------------------------------------------------------------- the judges

def hidden_answers(key, got):
    """Every answer that gives a hidden word a meaning: (arm, fold, pack, aligner, code) -> the meaning given."""
    out = {}
    for (arm, pack, a), lines in got.items():
        codes = key["folds"][pack[1]]["codes"]
        for c, x in lines.items():
            m = meaning_given(x)
            if m is not None and codes[c]["sort"] == "hidden":
                out[arm, int(pack[1]), pack, a, c] = m
    return out


def pair(answer, meaning):
    """What a judges' row is told by: the answer without its case, and the meaning. An answer given twice for one
    meaning is judged once."""
    return answer.lower(), meaning


def judge_rows(key, given, seed=SEED):
    """The judges' rows: each answer for a hidden word beside its word's meaning, and beside its decoy, in one
    shuffled list; a pair of texts stands once. Returns {row id: [answer, meaning]}."""
    pairs = {}
    for (arm, fold, pack, a, c), m in sorted(given.items()):
        k = key["folds"][str(fold)]["codes"][c]
        for meaning in (k["meaning"], k["decoy_meaning"]):
            pairs.setdefault(pair(m, meaning), [m, meaning])
    order = sorted(pairs)
    random.Random(seed).shuffle(order)
    return {f"R{n:04d}": pairs[p] for n, p in enumerate(order, 1)}


def rows_text(brief, rows, answers, labels=("answer", "meaning")):
    body = "\n".join(f"- `{r}`\n  - {labels[0]}: {a}\n  - {labels[1]}: {b}" for r, (a, b) in rows)
    return brief.format(n=len(rows), answers=answers, repo=REPO) + "\n---\n\n" + body + "\n"


def write_rows(folder, brief, rows, letter, labels=("answer", "meaning")):
    """A list of rows as packs of JUDGE_PACK for each of the two judges, and which rows each pack holds."""
    ids, in_pack = list(rows), {}
    for n in range(0, len(ids), JUDGE_PACK):
        name = f"{letter}{n // JUDGE_PACK + 1:02d}"
        in_pack[name] = ids[n:n + JUDGE_PACK]
        for j in JUDGES:
            write_text(f"{folder}/packs/{name}_j{j}.md", rows_text(brief, [(r, rows[r]) for r in in_pack[name]],
                                                                    f"{FOLDER}/{folder}/answers{j}/{name}.jsonl", labels))
    return in_pack


def judged(folder):
    return any(True for j in JUDGES for _ in (HOME / folder / f"answers{j}").glob("*.jsonl"))


def judge_packs():
    if judged("judge"):
        raise SystemExit("the judges have answered: their packs are not written again")
    key = read("packs/key.json")
    got, wrong = the_answers(key)
    if wrong:
        raise SystemExit(f"{len(wrong)} answer files are missing or not valid (answers-check): the judges get every answer at once")
    rows = judge_rows(key, hidden_answers(key, got))
    write("judge/key.json", {"rows": rows, "packs": write_rows("judge", JUDGE_BRIEF, rows, "J")})
    print(len(rows), "rows in", -(-len(rows) // JUDGE_PACK), "packs for each of the two judges")


def verdicts_of(folder, in_pack):
    """row -> [the first judge's verdict, the second's]; None where a judge gave none of VERDICTS."""
    out = {r: [None, None] for rs in in_pack.values() for r in rs}
    for j in JUDGES:
        for name, rs in in_pack.items():
            f = HOME / folder / f"answers{j}" / f"{name}.jsonl"
            for line in f.read_text(encoding="utf-8").splitlines() if f.exists() else []:
                try:
                    a = json.loads(line)
                except json.JSONDecodeError:
                    continue
                r, v = (a.get("row"), str(a.get("verdict") or "").strip().lower()) if isinstance(a, dict) else (None, "")
                if r in rs and v in VERDICTS and out[r][j - 1] is None:
                    out[r][j - 1] = v
    return out


# ------------------------------------------------------------------------------------------------------ the count

def arm_figures(hidden, given, verdict):
    """One arm's count. `hidden`: the hidden words, each with its fold, code, packs, meaning and decoy_meaning;
    `given`: (fold, pack, aligner, code) -> the meaning an aligner gave; `verdict(answer, meaning)`: the two
    judges' verdicts on that pair.

    A hidden word is given in a pack when both aligners of the pack give it a meaning, and right there when both
    judges call both answers the same as its meaning. A word that stands in several packs is given when it is
    given in one of them, and right only when it is right in every pack where it is given. The decoys are counted
    the same way, against the decoy's meaning."""
    words, units = [], collections.Counter()
    for h in hidden:
        both = [p for p in h["packs"] if all((h["fold"], p, a, h["code"]) in given for a in ALIGNERS)]
        if not both:
            continue

        def same(meaning, packs):
            return all(tuple(verdict(given[h["fold"], p, a, h["code"]], meaning)) == ("same", "same") for p in packs for a in ALIGNERS)
        words.append({"fold": h["fold"], "entry": h["entry"], "packs": len(h["packs"]), "given_in": len(both),
                      "right": same(h["meaning"], both), "decoy_same": same(h["decoy_meaning"], both)})
        units.update(given=len(both), right=sum(same(h["meaning"], [p]) for p in both), decoy_same=sum(same(h["decoy_meaning"], [p]) for p in both))
    n, right, decoy = len(words), sum(w["right"] for w in words), sum(w["decoy_same"] for w in words)
    return {"hidden": len(hidden), "given": n, "right": right, "decoys_same": decoy,
            "share_right": round(right / n, 4) if n else None, "share_decoys": round(decoy / n, 4) if n else None,
            "margin": round((right - decoy) / n, 4) if n else None,
            "by_word_and_pack": {k: units[k] for k in ("given", "right", "decoy_same")}, "words": words}


def gate(f, kappa, complete=True):
    """Gate B on one arm's count: at least 80% of the given words right, on at least 10 given words; that share at
    least 30 points above the share of decoys both judges call the same; the judges' kappa at least 0.6. It is met
    only when every answer and every verdict is in."""
    n, right, decoy = f["given"], f["right"], f["decoys_same"]
    bars = {"given_at_least_10": n >= BARS["given_at_least"],
            "right_80": n > 0 and right * 100 >= round(BARS["right"] * 100) * n,
            "above_decoys_30": n > 0 and (right - decoy) * 100 >= round(BARS["margin"] * 100) * n,
            "kappa_0.6": kappa is not None and kappa >= BARS["kappa"]}
    return {"bars": bars, "complete": bool(complete), "met": bool(complete and all(bars.values()))}


def hidden_words(key):
    return [{"fold": int(f), "code": c} | {x: k[x] for x in ("entry", "packs", "meaning", "decoy_meaning")}
            for f, fold in key["folds"].items() for c, k in fold["codes"].items() if k["sort"] == "hidden"]


def open_pairs(key, got):
    """(fold, pack, code) -> the two answers of the aligners with the frames, for every open word that both give a meaning."""
    out = {}
    for fold in FOLDS:
        for pack, codes in key["folds"][str(fold)]["packs"].items():
            mine = [got.get(("frames", pack, a), {}) for a in ALIGNERS]
            for c in codes:
                ms = [meaning_given(x.get(c)) for x in mine]
                if key["folds"][str(fold)]["codes"][c]["sort"] == "open" and None not in ms:
                    out[fold, pack, c] = [x[c] for x in mine]
    return out


def open_figures(key, pairs, verdict):
    """The open words to which both aligners with the frames give the same meaning: both judges call the pair
    the same. An open word stands in both folds and may stand in several packs: it is listed with every pack
    where its pair is the same, and with the number of packs where it stands."""
    stands, agreed = collections.Counter(), collections.defaultdict(list)
    for fold in FOLDS:
        for c, k in key["folds"][str(fold)]["codes"].items():
            if k["sort"] == "open":
                stands[k.get("entry") or k["spelling"], "entry" in k] += len(k["packs"])
    for (fold, pack, c), (a, b) in sorted(pairs.items()):
        k = key["folds"][str(fold)]["codes"][c]
        if tuple(verdict(meaning_given(a), meaning_given(b)) or ()) == ("same", "same"):
            agreed[k.get("entry") or k["spelling"], "entry" in k].append(
                {"pack": pack, "code": c, "meanings": [meaning_given(a), meaning_given(b)], "frames": [[x.get("frame"), x.get("slot")] for x in (a, b)]})
    return {"open_words": len(stands), "pairs_with_two_meanings": len(pairs), "words_agreed": len(agreed),
            "agreed": [{"entry" if named else "spelling": u, "stands_in_packs": stands[u, named], "agreed_in": v} for (u, named), v in sorted(agreed.items())]}


def unordered(a, b):
    return tuple(sorted((a.lower(), b.lower())))


def count():
    key = read("packs/key.json")
    got, wrong = the_answers(key)
    judge = read("judge/key.json") if (HOME / "judge/key.json").exists() else {"rows": {}, "packs": {}}
    seen = verdicts_of("judge", judge["packs"])
    by_pair = {pair(a, m): seen[r] for r, (a, m) in judge["rows"].items()}
    given = hidden_answers(key, got)
    unjudged = sorted({pair(m, x) for (arm, fold, pack, a, c), m in given.items() for k in [key["folds"][str(fold)]["codes"][c]]
                       for x in (k["meaning"], k["decoy_meaning"]) if None in by_pair.get(pair(m, x), [None])})
    complete = not wrong and not unjudged
    both = [tuple(v) for v in seen.values() if None not in v]
    kappa, two = W.kappa(both), W.kappa([(a == "same", b == "same") for a, b in both])     # the bar is on the three verdicts
    res = {"complete": complete, "files_missing_or_not_valid": len(wrong), "pairs_without_two_verdicts": len(unjudged),
           "judges": {"rows": len(judge["rows"]), "judged_by_both": len(both), "kappa": None if kappa is None else round(kappa, 4),
                      "kappa_same_or_not": None if two is None else round(two, 4),
                      "verdicts": [dict(collections.Counter(v[j] for v in both).most_common()) for j in (0, 1)]}}
    for arm in ARMS:
        mine = {(fold, pack, a, c): m for (x, fold, pack, a, c), m in given.items() if x == arm}
        f = arm_figures(hidden_words(key), mine, lambda ans, meaning: by_pair.get(pair(ans, meaning), [None, None]))
        res[arm] = f | {"answers_with_a_meaning": len(mine), "gate": gate(f, kappa, complete)}
    res["gate_met"] = res["frames"]["gate"]["met"]
    if (HOME / "open/key.json").exists():
        o = read("open/key.json")
        ov = verdicts_of("open", o["packs"])
        said = {unordered(*o["rows"][r]): ov[r] for r in o["rows"]}
        res["open"] = open_figures(key, open_pairs(key, got), lambda a, b: said.get(unordered(a, b)))
    write("result.json", res)
    print(json.dumps({k: (v if k not in ARMS else {x: y for x, y in v.items() if x != "words"}) for k, v in res.items() if k != "open"},
                     ensure_ascii=False, indent=1))
    if "open" in res:
        print({k: v for k, v in res["open"].items() if k != "agreed"})


def open_packs():
    if not (HOME / "result.json").exists() or not read("result.json").get("gate_met"):
        raise SystemExit("`count` does not say that gate B is met: no open word is laid before the judges")
    if judged("open"):
        raise SystemExit("the judges have answered: the open words' packs are not written again")
    key = read("packs/key.json")
    got, _ = the_answers(key)
    pairs = {}
    for (fold, pack, c), (a, b) in sorted(open_pairs(key, got).items()):
        pairs.setdefault(unordered(meaning_given(a), meaning_given(b)), [meaning_given(a), meaning_given(b)])
    order = sorted(pairs)
    random.Random(SEED).shuffle(order)
    rows = {f"P{n:04d}": pairs[p] for n, p in enumerate(order, 1)}
    write("open/key.json", {"rows": rows, "packs": write_rows("open", OPEN_BRIEF, rows, "O", ("one reader", "the other"))})
    print(len(rows), "pairs in", -(-len(rows) // JUDGE_PACK), "packs for each of the two judges")


# ---------------------------------------------------------------------------------------------------- the figures

def figures():
    """What the page reports, from the local files: counts only. No word, no meaning, no reading."""
    data, key = read("texts.json"), read("packs/key.json")
    stands = collections.Counter()
    for fold in FOLDS:
        for k in key["folds"][str(fold)]["codes"].values():
            if k["sort"] == "hidden":
                stands[len(k["packs"])] += 1
    out = {"counts": data["counts"], "seed": SEED, "layers": list(LAYERS), "bars": BARS,
           "known_words": {"meaning_from": dict(collections.Counter(k["from"] for k in data["known"].values()).most_common()),
                           "meaning_names_another_word": sum(k["names_another_word"] for k in data["known"].values()),
                           "by_kind": dict(collections.Counter(k["kind"] or "no kind" for k in data["known"].values()).most_common()),
                           "by_packs_they_stand_in": {str(n): c for n, c in sorted(stands.items())},
                           "in_more_than_one_pack": sum(c for n, c in stands.items() if n > 1)},
           "packs": [{"pack": p, "texts": len(v["texts"]), "words": v["words"]}
                     | {f"fold_{f}": dict(collections.Counter(key["folds"][str(f)]["codes"][c]["sort"] for c in key["folds"][str(f)]["packs"][f"f{f}_{p}"]))
                        for f in FOLDS} for p, v in key["packs"].items()],
           "folds": {str(f): {"hidden_words": len(key["folds"][str(f)]["hidden"])}
                     | dict(collections.Counter(f"{k['sort']}_codes" for k in key["folds"][str(f)]["codes"].values())) for f in FOLDS},
           "names": dict(collections.Counter(c.split("-")[0] for c in key["names"]).most_common()),
           "aligners": len(FOLDS) * len(ARMS) * len(ALIGNERS) * len(key["packs"])}
    if (HOME / "result.json").exists():
        res = read("result.json")
        out["result"] = {k: v for k, v in res.items() if k not in ARMS + ("open",)} \
            | {arm: {k: v for k, v in res[arm].items() if k != "words"} for arm in ARMS}
        if "open" in res:
            out["result"]["open"] = {k: v for k, v in res["open"].items() if k != "agreed"}
    return out


def public():
    PUBLIC.write_text(json.dumps(figures(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", PUBLIC.relative_to(ROOT))


COMMANDS = {"texts": texts, "folds": folds, "packs": packs, "answers-check": answers_check, "judge-packs": judge_packs,
            "count": count, "open-packs": open_packs, "public": public}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        raise SystemExit(__doc__)
    COMMANDS[sys.argv[1]]()
