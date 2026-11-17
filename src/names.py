"""Track C of the evidence from outside the texts (data/discovery/outside_evidence.md, section 4): personal names
cut into the parts that come back, and two gates on those parts.

The names are the places the map with its layers marks as a person's name. The texts are those of the grammar
pilot's split (data/sources/grammar/split.json): the cutter is built and tuned on the names of the 329 tuning
texts. `names` writes a row for every place, but nothing is learned, counted or printed from a name of the 219
held-back texts before `held`, which runs only once this script is in git as it stands, and once.

A name is the spelling without what the map names as an ending or a word joined to it: what the map's parts take
off its ends (a part it marks `ending`, or builds on an ending or a function word of the lexicon), and, where the
map gives the word in one piece but reads it "this is ...", the end that it takes off other names it reads so
(learned from the tuning texts: an end it takes off three names there, and that the lexicon lists as an ending or
a function word). Nothing else is taken off: an ending the map leaves in a name stays in it, for the cutter to
find. The cutter learns from the different names, endings off, so that two spellings of one name count once.

The cutter. A part is a string of at least two letters that stands in at least three different names of those it
learns from and that no longer string carries with it: a string is dropped when it stands in exactly as many names
with one more letter before it or after it (it is then a piece of that longer string). This is the plainest form
of cutting by how freely a string's neighbours vary (Harris's successor counts, branching entropy), with the
threshold on how often a string comes back that the page sets (three names) and the lowest threshold on how its
neighbours vary (they vary at all). A name is cut into such parts so that as few letters as possible are left
over, then into as few pieces as possible, then into the parts that stand in the most names; it is wholly split
when no letter is left over. Nothing but the names it is given goes into the cutter: no list of parts, no
dictionary, nothing about the script.

Why this one. Minimum description length (a Morfessor-style lexicon) was tried first on the tuning names and cut
them down to single letters or left them whole: 342 names do not pay for a lexicon of parts. Among the
recurrence cutters tried, each choice was compared on tuning names the cutter had not learned from (learn on a
random half, cut the other half, against the same names with their letters shuffled), and every stricter one made
the difference smaller: asking that a string one letter longer stand in no more than two thirds or four fifths of
a string's names, taking only strings that begin or end a name, binding a part to the place (first, middle, last)
it was seen in, cutting only between syllables, and a floor of three letters, which leaves almost no name wholly
split. The floor of two letters is the lowest that says anything (with single letters every name is wholly split,
real or made up). Keeping the carried strings as parts too made the difference 0.7 points larger on the unseen half
(1.2 on the unseen fifth); they are dropped all the same, because a carried string stands in exactly the names of
the longer string and would only be that part a second time. The thresholds are MIN_LETTERS, MIN_NAMES and CARRIED
below and are not changed after `held`.

What the comparison with shuffled letters can and cannot show: shuffling the letters also breaks the syllables
of the script (a vowel sign follows a consonant sign), so part of the difference is the sound shape of a name and
not its parts. `learn` and `held` therefore print a second comparison beside the gate's, in which the made-up
names keep their syllables and only the order of the syllables is shuffled. It is not the gate and has no bar.

Everything is read and written under data/sources/names/ (local only: the rows hold the names), except `public`.

  python3 -I src/names.py names    every place of a name with its role, site and kind of text (names.json)
  python3 -I src/names.py learn    the parts, from the tuning names alone, and how they do on unseen tuning names (parts.json)
  python3 -I src/names.py held     gate C1 on the held-back names: once, and only with this script in git (held.json)
  python3 -I src/names.py packs    gate C2: the parts as codes with their statistics, for two readers (packs/, key.json)
  python3 -I src/names.py count    gate C2: the two readers compared with the key (count-pairs.json, count.json)
  python3 -I src/names.py public   data/discovery/outside_names_figures.json: counts only

Gate C2 counts a part as standing in a name wherever its letters stand in it, as the cutter and the page count it
(not only where the one best cut of the name uses it), and it counts different names, endings off: two spellings
of one name count once. What the readers are given is BRIEF below and runs/prompts/NAMES_readers.md. Whether two
meanings are the same is not decided here: `count` writes the pairs (count-pairs.json) and reads the judge's
verdicts from count-verdicts.json, {"P017": {"same": true, "right": false}, ...}: "same" says whether the two
readers' meanings are one meaning, "right" (for a known part) whether that meaning is the key's.
"""
import collections
import json
import math
import pathlib
import random
import re
import subprocess
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(ROOT / "src" / "v6")]
import coverage as C                                    # noqa: E402
import recurring as W                                   # noqa: E402
import themap as M                                      # noqa: E402
import words as D                                       # noqa: E402

HOME = ROOT / "data/sources/names"
ANSWERS = "data/sources/names/answers"                  # the folder the packs name for the readers' answers
PUBLIC = ROOT / "data/discovery/outside_names_figures.json"
SPLIT = ROOT / "data/sources/grammar/split.json"         # the grammar pilot's split: {"tuning": [...], "held": [...]}
FROZEN = ("src/names.py", "tests/test_names.py")        # what must be in git, as it stands, before the held-back names are read
LAYERS = ("recurring", "rare_sure", "rare_later", "unnamed", "rare_millet", "leftover", "leftover_stems")   # the map when the page was set
# The page's counts (section 4), from the map with those layers: the script stops if the map no longer gives them.
TOTALS = {"places": 705, "without_a_lost_sign": 701, "spellings": 624, "tuning": 350, "held": 305, "both": 31}
NAME_KINDS = ("person name", "name", "")                 # the map's kinds of a word of the level `name` that is a person's
SEED = 20261116                                          # the page's seed: the made-up names of gate C1
SEED_LEARN = SEED + 21                                   # the halves and fifths of the tuning names, and their made-up names
SEED_SYLLABLES = SEED + 22                               # the made-up names that keep their syllables (beside the gate)
SEED_PACKS = SEED + 23                                   # the numbering of the codes
# The cutter's thresholds, fixed on the tuning names.
MIN_LETTERS = 2                                          # a part has at least two letters
MIN_NAMES = 3                                            # ... and stands in at least three of the names learned from (the page's three)
CARRIED = 1.0                                            # ... and is dropped when a string one letter longer stands in this share of its names
# The gates.
DRAWS = 200                                              # made-up names for each name
BAR_C1 = 0.30                                            # the real share at least this far above the made-up share
MIN_CODED = 5                                            # gate C2: a part with a code stands in at least five names
PACK = 40                                                # codes in a pack, about
BARS_C2 = {"rate": 0.80, "least": 8}                    # of the known parts both readers agree on, at least 8, 80% right
KINDS = ("god", "quality", "thing or person", "deed", "kin word", "title", "ending", "unclear")
NO_MEANING = ("", "none")
# The comparison on tuning names the cutter has not learned from.
RUNS, DRAWS_LEARN = 50, 50                              # the tuning names dealt this often, with this many made-up names each
# The map's wording, in English, that the names' rows are read from. None of it is Meroitic.
THIS_IS = "this is "                                     # how the map reads a name with the predicate "this one is" on it
THIS_ONE = "this one"                                    # ... and a word of its own that says the same of the name before it
BORN = re.compile(r"\b(bore|born of|borne by|maternal filiation|of a mother|of such a mother)\b")
BEGOTTEN = re.compile(r"\b(begot|begotten|paternal filiation|of such a father)\b")
RELATED = re.compile(r"\b(nephew|niece|wife|husband|sister|brother|uncle|the mother of|the father of)\b")
KIN = re.compile(r"\b(mother|father|child|son|daughter|brother|sister|wife|husband|nephew|niece|uncle|aunt)\b")
EPITAPH = ("funerary", "not known", "")                 # the kinds of text in which "this is X" names the dead
NO_SITE = "site not known"
NO_PLACE = re.compile(r"\b(provenance|unknown|not stated|not known)\b", re.I)
PIECE = re.compile(r"\b(part|half|end|tail|piece|beginning) of\b")    # how the map reads a piece of a word written apart
ROLES = ("dead", "mother", "father", "other")
ENGLISH_NAME = re.compile(r"[A-Z][a-z]+(?: of [A-Z][a-z]+)?")
NOT_NAMED = "a god the lexicon gives no English name"
# The lexicon's kind of a word -> the kind of part the readers choose from. A noun (or a word without a kind) whose
# meaning is a kin term is a kin word.
KIND_OF = {"god name": "god", "adjective": "quality", "epithet": "quality", "verb": "deed", "title": "title",
           "noun": "thing or person", "function word": "ending"}
LABEL = re.compile(r"\b(noun|title|adjective|verb)\s*:")   # a kind the lexicon's meaning names as a label
PLACES = ("first", "middle", "last", "whole name")     # where a part stands in a name
VOWELS = "eio"                                           # the script's vowel signs: only for the made-up names that keep their syllables

BRIEF = """# What kind of part is it? <<N>> parts of Meroitic personal names, shown by numbers only

Meroitic is written in a script that can be read aloud, but most of its words are not understood. A script has cut
the personal names of the Meroitic texts (about 600 names, most of them from epitaphs) into the strings of letters
that come back from name to name. Each such part stands here under a code. You are not shown its letters, and you
are not shown any name: only where the part stands and with what. Some of the parts are words or gods' names whose
meaning is known, and your answers for those will be checked; you are not told which they are.

The parts were found by a count, not by a grammar: a part is any string of two letters or more that comes back in
several names. So one part can be a piece of another, and some are only letters that happen to stand together.

For each code the pack gives, always as a number of different names:

- **names**: in how many names the part stands;
- **place**: how many names it begins (first), how many it stands inside (middle), how many it ends (last), and
  how many it is the whole of (a name in which it stands twice can count twice);
- **with gods**: the gods whose names stand in the same names, apart from it, by the god's English name;
- **whose names**: in how many names of mothers, of fathers and of the dead (the person an epitaph is for) the
  part stands, as far as the text shows whose name it is; the other names are other people's, or the text does
  not show it;
- **sites**: where the texts with these names were found;
- **beside**: the other codes that most often stand right before it or right after it in a name.

**How names are built in the two naming traditions nearest to these people.** You may lean on this, and on nothing
else you know or believe about Meroitic.

- Egyptian names of these centuries are very often a god's name with a short statement about the god or about the
  bearer: that the god gave the child, that the god is content, strong or alive, that the bearer belongs to the
  god or is the god's son, daughter or servant. The god's name can stand first or last; what goes with it is a
  deed, a quality, a kin word or a word for a person. Other Egyptian names are a quality of the bearer alone, a
  kin word, a title, or a thing or an animal.
- Nubian names, as far as the later Nubian languages show them, are more often a word for a person, a kin word or
  a quality, alone or with a second word after it that says what the bearer is like, and names that call the
  bearer the servant of a god or a saint.
- In both traditions short endings that only mark a word as a name, or as a man's or a woman's name, are common.

For each code give one JSON line, in the order of this file, in the file `<<ANSWERS>>`, nothing else in it:

    {"code": "P017", "kind": "<one of the kinds below>", "meaning": "<a few English words, or none>", "why": "<one short sentence>"}

- "kind" is one of: "god" (a god's name), "quality" (what the bearer or the god is like), "thing or person" (a
  noun that is none of the other kinds), "deed" (a verb: something done), "kin word" (a word for a relative),
  "title" (an office or a rank), "ending" (no meaning of its own: it marks a name, or a man's or a woman's name),
  "unclear".
- "meaning" is what you think the part means, in a few English words, only if the numbers give you a reason to say
  it; otherwise "none". A kind without a meaning is a full answer.
- **"unclear" and "none" are full answers,** and for most parts they are the right ones. A guess that the numbers
  do not carry counts against you.
- Use only this file. Do not open any other file of the repository, do not search the web, do not spawn agents,
  and write no file but your answers file.

This pack lists <<N>> codes: your file must have <<N>> lines, one for each code. When it is written, count its lines
against that number, then reply in one line: how many codes, and how many of each kind.
"""


def read(path):
    return json.loads((HOME / path).read_text(encoding="utf-8"))


def write(path, data):
    (HOME / path).parent.mkdir(parents=True, exist_ok=True)
    (HOME / path).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def pct(x):
    return f"{100 * x:.1f}%"


# ------------------------------------------------------------------------------------------------------ the names

def the_map():
    """The map with the layers it had when the page was set."""
    names = tuple(l["name"] for l in M.LAYERS)
    if names[:len(LAYERS)] != LAYERS:
        raise SystemExit(f"the layers are no longer {LAYERS}")
    return M.current(upto=len(LAYERS))


def the_split():
    return json.loads(SPLIT.read_text(encoding="utf-8"))


def letters(headword):
    """A headword of the lexicon in the corpus's letters: without its number, its hyphens and its capitals, `S` for
    the sign s, `s` for se, `N` for ne, `X` for ẖ, `x` for ḫ."""
    core = unicodedata.normalize("NFC", C.bare(headword).lower())
    core = core.replace("se", "\0").replace("s", "S").replace("\0", "s").replace("ne", "N").replace("ẖ", "X").replace("ḫ", "x")
    return re.sub(r"[^A-Za-z]", "", core)


def joined_entries(lex):
    """The lexicon's entries that are no part of a name where they stand on one: its endings (a hyphenated function
    word or entry without a kind) and its function words ("this one", "this one is")."""
    return {h for h, e in lex.items() if (e.get("kind") or "") == "function word" or D.ending(h, lex)}


def is_name(g):
    return g["level"] == "name" and (g.get("kind") or "") in NAME_KINDS


def by_parts(g, joined):
    """(what the map takes off before the name, the name, what it takes off after it), where the map cuts the word:
    the parts it marks as an ending or builds on an entry of `joined` are taken off both ends, one part at least
    is left. None where the map gives the word in one piece or its parts do not spell it."""
    ps = [p for p in g.get("parts") or [] if p.get("form")]
    if len(ps) < 2 or "".join(p["form"] for p in ps) != g["form"]:
        return None
    off = [p.get("entry") == "ending" or p.get("entry") in joined for p in ps]
    a, b = 0, len(ps)
    while b - a > 1 and off[b - 1]:
        b -= 1
    while b - a > 1 and off[a]:
        a += 1
    return "".join(p["form"] for p in ps[:a]), "".join(p["form"] for p in ps[a:b]), "".join(p["form"] for p in ps[b:])


def ends_read(gl, texts, lex, joined):
    """The ends the map takes off a name it reads "this is ...", in the texts given (the tuning texts): those it
    takes off at least MIN_NAMES different names and that the lexicon lists, letter for letter, as an ending or a
    function word. The longest first."""
    listed = {letters(h) for h in joined}
    seen = collections.defaultdict(set)
    for t in texts:
        for g in gl[t]:
            if is_name(g) and "." not in g["form"] and (g.get("gloss") or "").startswith(THIS_IS):
                cut = by_parts(g, joined)
                if cut and cut[2]:
                    seen[cut[2]].add(cut[1])
    return sorted((e for e, ns in seen.items() if len(ns) >= MIN_NAMES and e in listed), key=lambda e: (-len(e), e))


def name_of(g, joined, ends):
    """(the name without what the map names as an ending or a word joined to it, how it was cut, what was taken off).
    "parts": the map's parts take something off. "reading": the map's parts take nothing off but the map reads the
    word "this is ..."; the script takes off the longest of `ends` it ends in (and the row says so). "whole":
    nothing is taken off."""
    cut = by_parts(g, joined)
    if cut and (cut[0] or cut[2]):
        return cut[1], "parts", " + ".join(x for x in (cut[0], cut[2]) if x)
    if (g.get("gloss") or "").startswith(THIS_IS):
        for e in ends:
            if g["form"].endswith(e) and len(g["form"]) > len(e):
                return g["form"][:-len(e)], "reading", e
    return g["form"], "whole", ""


def reading_of(g, lex):
    """What the map says of a word, for the roles: its gloss and the lexicon's meanings of the entries it is built on."""
    return " ".join([g.get("gloss") or ""] + [lex[p["entry"]].get("meaning") or "" for p in g.get("parts") or [] if p.get("entry") in lex])


def role_of(gs, i, lex, kind):
    """Whose name the word i of a text is, where the map shows it: the dead person's (the map reads it "this is
    ...", or the next word is the map's "this one (is)"; in a text that is no epitaph such a name is another
    person's), a mother's or a father's (the next word is the map's "born of" or "begotten of"), another person's
    (the next word is another word of kinship), or what the map's own reading of the name says; else None."""
    g, nxt = gs[i], gs[i + 1] if i + 1 < len(gs) else None
    own = g.get("gloss") or ""
    if own.startswith(THIS_IS) or (nxt is not None and (nxt.get("gloss") or "").startswith(THIS_ONE)):
        return "dead" if kind in EPITAPH else "other"
    after = reading_of(nxt, lex) if nxt is not None and not is_name(nxt) else ""
    for role, rule in (("mother", BORN), ("father", BEGOTTEN), ("other", RELATED)):
        if rule.search(after):
            return role
    for role, word in (("dead", "deceased"), ("mother", "mother"), ("father", "father")):
        if word in own:
            return role
    return None


def site_of(row):
    """The place a text was found, as a short name without accents: the corpus's site up to its first colon, comma
    or bracket. A site that is a sentence (more than three words: "purchased by ... at ...") or that says the
    provenance is not known is no place."""
    site = re.split(r"[:,(]", row.get("site") or "")[0].strip()
    site = "".join(ch for ch in unicodedata.normalize("NFKD", site) if not unicodedata.combining(ch))
    return NO_SITE if not site or len(site.split()) > 3 or NO_PLACE.search(site) else site


def rows_of(gl, corpus, lex, split):
    """One row a place of a person's name, in the texts' order: the text, the word's number, the set, the spelling,
    whether a sign is lost, the name, how it was cut and what was taken off, the role, the site and the kind of
    text. The ends taken off a name the map does not cut are learned from the tuning texts alone."""
    joined = joined_entries(lex)
    ends = ends_read(gl, sorted(split["tuning"]), lex, joined)
    sets = {t: "tuning" for t in split["tuning"]} | {t: "held" for t in split["held"]}
    out = []
    for t in sorted(gl):
        kind = corpus[t].get("kind") or "not known"
        for i, g in enumerate(gl[t]):
            if is_name(g):
                name, how, off = name_of(g, joined, ends)
                out.append({"text": t, "n": i + 1, "set": sets[t], "form": g["form"], "lost": "." in g["form"], "name": name, "cut": how,
                            "off": off, "role": role_of(gl[t], i, lex, kind), "site": site_of(corpus[t]), "kind": kind})
    return out


def totals_of(rows):
    """The page's counts, from the rows: places, those without a lost sign, their spellings, by set and in both."""
    ok = [r for r in rows if not r["lost"]]
    tuning, held = ({r["form"] for r in ok if r["set"] == s} for s in ("tuning", "held"))
    return {"places": len(rows), "without_a_lost_sign": len(ok), "spellings": len(tuning | held), "tuning": len(tuning),
            "held": len(held), "both": len(tuning & held)}


def the_rows():
    """The rows from the map as it stands. The map must still give the page's counts."""
    rows = rows_of(the_map(), W.corpus_rows(), W.lexicon(), the_split())
    if totals_of(rows) != TOTALS:
        raise SystemExit(f"the names are no longer those of the page: {totals_of(rows)}")
    return rows


def spellings_of(rows, which):
    """{spelling: its name} for the readable places of a set: the name it has most often there (at a tie, first)."""
    by = collections.defaultdict(collections.Counter)
    for r in rows:
        if r["set"] == which and not r["lost"]:
            by[r["form"]][r["name"]] += 1
    return {f: c.most_common(1)[0][0] for f, c in sorted(by.items())}


def names_of(rows, which):
    """The different names of a set's readable places, endings off, sorted."""
    return sorted({r["name"] for r in rows if r["set"] == which and not r["lost"]})


def tuning_figures(rows):
    """What may be said of the tuning names: counts by how the name was cut, by role, by kind of text and by site."""
    mine = [r for r in rows if r["set"] == "tuning" and not r["lost"]]
    return {"places": len(mine), "spellings": len({r["form"] for r in mine}), "names": len(names_of(rows, "tuning")),
            "cut": dict(collections.Counter(r["cut"] for r in mine).most_common()),
            "taken_off": dict(collections.Counter(r["off"] for r in mine if r["off"]).most_common()),
            "roles": dict(collections.Counter(r["role"] or "not shown" for r in mine).most_common()),
            "kinds_of_text": dict(collections.Counter(r["kind"] for r in mine).most_common()),
            "sites": dict(collections.Counter(r["site"] for r in mine).most_common())}


def names():
    rows = the_rows()
    write("names.json", rows)
    print("all texts:", totals_of(rows))
    print("tuning texts:", json.dumps(tuning_figures(rows), ensure_ascii=False, indent=1))


# ------------------------------------------------------------------------------------------------------ the cutter

def learn_parts(names, least=MIN_NAMES, floor=MIN_LETTERS, carried=CARRIED):
    """{part: the number of names it stands in}, from the names given and nothing else: every string of `floor`
    letters or more that stands in `least` different names, unless a string one letter longer (before it or after
    it) stands in at least `carried` of those names."""
    stands = collections.Counter()
    for n in set(names):
        stands.update({n[i:j] for i in range(len(n)) for j in range(i + floor, len(n) + 1)})
    longer = collections.Counter()                       # string -> the most names a string one letter longer stands in
    for s, c in stands.items():
        if len(s) > floor:
            for inner in (s[1:], s[:-1]):
                longer[inner] = max(longer[inner], c)
    return {s: c for s, c in sorted(stands.items()) if c >= least and longer[s] < carried * c}


def cut(name, parts):
    """A name as a list of (letters, whether they are a part), in order: the cut that leaves the fewest letters
    over, then has the fewest pieces (a run of left-over letters is one piece), then whose parts stand in the most
    names (the largest sum of the logarithms of their counts); at a tie still, the cut whose pieces are the
    shortest from the left."""
    def rank(o):
        return o[0], o[1], round(o[2], 9), [len(p) for p, _ in o[3]]

    # for each prefix, the best cut that ends in a part (or is empty) and the best that ends in left-over letters:
    # (letters left over, pieces, minus the weight, the pieces)
    clean, run = [(0, 0, 0.0, [])], [None]
    for j in range(1, len(name) + 1):
        options = []
        if run[j - 1]:
            over, pieces, weight, cuts = run[j - 1]
            options.append((over + 1, pieces, weight, cuts[:-1] + [(cuts[-1][0] + name[j - 1], False)]))
        if clean[j - 1]:
            over, pieces, weight, cuts = clean[j - 1]
            options.append((over + 1, pieces + 1, weight, cuts + [(name[j - 1], False)]))
        run.append(min(options, key=rank))
        options = [(o[0], o[1] + 1, o[2] - math.log(parts[name[i:j]]), o[3] + [(name[i:j], True)])
                   for i in range(j) if name[i:j] in parts for o in (clean[i], run[i]) if o]
        clean.append(min(options, key=rank) if options else None)
    return min((o for o in (clean[-1], run[-1]) if o), key=rank)[3]


def whole(name, parts):
    """Whether a name is wholly split: it can be cut into parts with no letter left over."""
    ok = [True] + [False] * len(name)
    for j in range(1, len(name) + 1):
        ok[j] = any(ok[i] and name[i:j] in parts for i in range(j))
    return bool(name) and ok[-1]


def shuffled(name, rng):
    """A made-up name: the letters of a name in an order drawn by lot."""
    ls = list(name)
    rng.shuffle(ls)
    return "".join(ls)


def syllables(name):
    """A name in the script's syllables: a vowel sign goes with the consonant sign before it."""
    out = []
    for ch in name:
        if ch in VOWELS and out and out[-1][-1] not in VOWELS:
            out[-1] += ch
        else:
            out.append(ch)
    return out


def reordered(name, rng):
    """A made-up name that keeps its syllables: only their order is drawn by lot."""
    ss = syllables(name)
    rng.shuffle(ss)
    return "".join(ss)


def tally(names, parts, rng, rng_syllables, draws=DRAWS):
    """(how many of the names given are wholly split, how many made-up names are, how many made-up names that keep
    their syllables are), the last two as a sum over the names of the share of a name's draws: for each name in
    the order given, `draws` shuffles of its letters by `rng`; then `draws` shuffles of its syllables by
    `rng_syllables`."""
    real = sum(whole(n, parts) for n in names)
    made = sum(sum(whole(shuffled(n, rng), parts) for _ in range(draws)) / draws for n in names)
    kept = sum(sum(whole(reordered(n, rng_syllables), parts) for _ in range(draws)) / draws for n in names)
    return real, made, kept


def shares(k, real, made, kept):
    """A tally of k names as shares: the share wholly split, the same for the made-up names, and how far the first
    stands above the second; beside it the same for the made-up names that keep their syllables."""
    r = lambda x: round(x / k, 4) if k else None                                                                        # noqa: E731
    return {"names": k, "wholly_split": real, "share": r(real), "made_up": r(made), "margin": r(real - made),
            "syllables_kept": r(kept), "margin_syllables_kept": r(real - kept)}


def compare(names, parts, rng, rng_syllables, draws=DRAWS):
    """The share of the names given that are wholly split, against made-up names (tally(), as shares)."""
    return shares(len(names), *tally(names, parts, rng, rng_syllables, draws))


def unseen(names, share, runs, seed, draws):
    """How the cutter does on names it has not learned from: `runs` times, the names are dealt by lot, the cutter
    learns from `share` of them and cuts the rest, against made-up names. The counts of all runs are added up."""
    deal, rng, rng_syllables = random.Random(seed), random.Random(seed + 1), random.Random(seed + 2)
    k, total, parts_found = 0, [0, 0.0, 0.0], []
    for _ in range(runs):
        ns = sorted(set(names))
        deal.shuffle(ns)
        at = round(len(ns) * share)
        parts = learn_parts(ns[:at])
        parts_found.append(len(parts))
        k += len(ns) - at
        total = [a + b for a, b in zip(total, tally(ns[at:], parts, rng, rng_syllables, draws))]
    out = shares(k, *total)
    return {"learned_from": share, "runs": runs, "draws": draws, "names_cut": k, "parts": round(sum(parts_found) / runs, 1)} \
        | {x: out[x] for x in ("share", "made_up", "margin", "syllables_kept", "margin_syllables_kept")}


def learned_thresholds():
    return {"MIN_LETTERS": MIN_LETTERS, "MIN_NAMES": MIN_NAMES, "CARRIED": CARRIED}


def learned(rows):
    """What `learn` writes, from the rows of the tuning texts alone: the parts of all tuning names, how many of
    those names they wholly split (the names they were learned from: no test), and the comparison on tuning names
    the cutter has not learned from: learning from a half of them and cutting the other half, and (nearer to what
    `held` does, which learns from all of them) learning from four fifths and cutting the last fifth."""
    mine = names_of([r for r in rows if r["set"] == "tuning"], "tuning")
    parts = learn_parts(mine)
    return {"method": "strings of MIN_LETTERS letters or more that stand in MIN_NAMES names and that no string one letter longer carries",
            "thresholds": learned_thresholds(),
            "names": len(mine), "parts_in_three_names": len(parts),
            "strings_in_three_names_carried_ones_too": len(learn_parts(mine, carried=math.inf)),
            "by_length": dict(sorted(collections.Counter(len(p) for p in parts).items())),
            "names_wholly_split_in_sample": sum(whole(n, parts) for n in mine),
            "unseen_half": unseen(mine, 0.5, RUNS, SEED_LEARN, DRAWS_LEARN),
            "unseen_fifth": unseen(mine, 0.8, RUNS, SEED_LEARN + 3, DRAWS_LEARN),
            "parts": parts}


def learn():
    out = learned(the_rows())
    write("parts.json", out)
    print(json.dumps({k: v for k, v in out.items() if k != "parts"}, ensure_ascii=False, indent=1))
    print("the parts that stand in the most tuning names:", " ".join(f"{p} {c}" for p, c in sorted(out["parts"].items(), key=lambda kv: (-kv[1], kv[0]))[:60]))


# ---------------------------------------------------------------------------------------------------- gate C1

def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def frozen():
    """This script and its checks must be in git exactly as they stand before a held-back name is read. Gives the
    commit that last changed the script, with its time."""
    for rel in FROZEN:
        there = git("rev-parse", "-q", "--verify", f"HEAD:{rel}")
        if not there or git("hash-object", rel) != there:
            raise SystemExit(f"{rel} is not in git as it stands: commit it before the held-back names are read")
    return git("log", "-1", "--format=%h %cI", "--", FROZEN[0])


def verdict_c1(names, real, made):
    """The bar of gate C1 on a tally: the share of the names wholly split stands at least BAR_C1 above the share of
    the made-up names (as counted, before any rounding)."""
    return "met" if names and (real - made) / names >= BAR_C1 else "missed"


def gate_c1(rows, commit):
    """Gate C1 from the rows: the cutter learns from all tuning names; the share of held-back names (spellings, as
    the page counts them) it wholly splits, against made-up names (DRAWS shuffles of each name's letters, by
    random.Random(SEED), the names in the order of their spellings). Beside the gate: the same without the
    held-back spellings that also stand in a tuning text, without those whose name (endings off) does, and counted
    on the different names instead of the spellings."""
    known = set(names_of(rows, "tuning"))
    parts = learn_parts(known)
    held, tuning = spellings_of(rows, "held"), spellings_of(rows, "tuning")

    def run(names):
        return compare(names, parts, random.Random(SEED), random.Random(SEED_SYLLABLES))

    real, made, kept = tally(list(held.values()), parts, random.Random(SEED), random.Random(SEED_SYLLABLES))
    gate = shares(len(held), real, made, kept)
    return {"frozen_in": commit, "bar": BAR_C1, "draws": DRAWS, "seed": SEED,
            "thresholds": learned_thresholds(),
            "tuning_names": len(known), "parts_in_three_tuning_names": len(parts),
            "gate": gate | {"verdict": verdict_c1(len(held), real, made)},
            "without_the_spellings_also_in_tuning": run([n for f, n in held.items() if f not in tuning]),
            "without_the_names_also_in_tuning": run([n for n in held.values() if n not in known]),
            "by_different_names": run(sorted(set(held.values()))),
            "rows": [{"form": f, "name": n, "in_tuning": f in tuning, "cut": [[p, ok] for p, ok in cut(n, parts)], "wholly_split": whole(n, parts)}
                     for f, n in held.items()]}


def held():
    """Gate C1, once: only with the script in git as it stands, and not a second time."""
    commit = frozen()
    if (HOME / "held.json").exists():
        raise SystemExit("the gate has been run: it is not run again")
    out = gate_c1(the_rows(), commit)
    write("held.json", out)
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}, ensure_ascii=False, indent=1))
    g = out["gate"]
    print(f"gate C1: {g['wholly_split']} of {g['names']} held-back names wholly split = {pct(g['share'])}; made-up names {pct(g['made_up'])}; "
          f"{100 * g['margin']:.1f} points; the bar is {100 * BAR_C1:.0f} points: {g['verdict']}")


# ---------------------------------------------------------------------------------------------------- gate C2

def english_name(h, lex, seen=()):
    """A god's English name from the lexicon: the first name the entry's meaning gives in English; where that is
    another headword of the lexicon ("see X", "a variant of X"), that entry's."""
    for m in ENGLISH_NAME.findall((lex.get(h) or {}).get("meaning") or ""):
        if m in lex and m != h:
            return english_name(m, lex, seen + (h,)) if m not in seen else NOT_NAMED
        return m
    return NOT_NAMED


def gods_of(gl, lex):
    """{letters: the god's English name}: the letters of a piece of a word the map marks as a god's name (level
    `name`, kind `god name`) that the map builds on an entry of the lexicon that is a god's name. A half of a
    god's name that the edition wrote apart is no god's name: the word's pieces must spell it, the map must not
    read it as a piece of a word, and the letters must be that entry's own in the lexicon, or be three letters or
    more and stand for a god in at least MIN_NAMES places of the map. Letters the map gives to two gods go to the
    one it gives them to most often."""
    by, own = collections.defaultdict(collections.Counter), set()
    for t in sorted(gl):
        for g in gl[t]:
            ps = g.get("parts") or []
            if g["level"] == "name" and (g.get("kind") or "") == "god name" and "".join(p.get("form") or "" for p in ps) == g["form"] \
                    and not PIECE.search(g.get("gloss") or ""):
                for p in ps:
                    if p.get("form") and p.get("entry") in lex and (lex[p["entry"]].get("kind") or "") == "god name":
                        by[p["form"]][english_name(p["entry"], lex)] += 1
                        own.add(letters(p["entry"]))
    return {f: c.most_common(1)[0][0] for f, c in sorted(by.items()) if f in own or (len(f) >= 3 and sum(c.values()) >= MIN_NAMES)}


def kinds_of(entry):
    """The readers' kinds of a word of the lexicon: its kind there by the table KIND_OF, and the kinds its meaning
    names there as a label ("adjective: ...; noun: ..."). A noun, or a word without a kind, whose meaning is a kin
    term is a kin word. Empty where the table has none."""
    meaning = entry.get("meaning") or ""
    out = set()
    for kind in [entry.get("kind") or ""] + LABEL.findall(meaning):
        out.add("kin word" if kind in ("noun", "") and KIN.search(meaning) else KIND_OF.get(kind))
    return sorted(out - {None})


def words_of(gl, lex, layers_lines):
    """{letters: [what the word is]}: the dictionary words with a meaning on the map with its layers (the north
    star's: in use, no name and no ending, established or probable in the lexicon or given a meaning by a layer),
    each under its headword's letters, with the readers' kinds and the meaning (the lexicon's, or the layer's)."""
    known, _, _ = D.population_of(gl, lex, fix=True)
    meaning = {h: lex[h].get("meaning") or "" for h in D.translated(known, lex)}
    given = {h for hs in M.given_by_layers(layers_lines, known, lex).values() for h in hs}
    for _, lines in layers_lines:
        for o in lines:
            if o.get("item") in given and o["why"] == "stated" and o.get("level") in W.READ:
                meaning.setdefault(o["item"], o.get("gloss") or "")
    out = collections.defaultdict(list)
    for h in sorted(meaning):
        if letters(h):
            out[letters(h)].append({"entry": h, "kinds": kinds_of(lex[h]), "meaning": meaning[h]})
    return dict(out)


def known_of(part, gods, words):
    """What a part is, if its letters are a god's name of the map or a dictionary word with a meaning; else None."""
    what = ([{"entry": None, "kinds": ["god"], "meaning": f"the god {gods[part]}"}] if part in gods else []) + words.get(part, [])
    return what or None


def people_of(rows):
    """{name: its sites and its roles} over the readable places of all texts: a name counts once, whatever its
    spellings and however often it stands."""
    out = {}
    for r in rows:
        if not r["lost"]:
            p = out.setdefault(r["name"], {"sites": set(), "roles": set()})
            p["sites"].add(r["site"])
            if r["role"]:
                p["roles"].add(r["role"])
    return out


def stands_at(name, part):
    """Every place a part stands in a name: where it begins."""
    return [i for i in range(len(name) - len(part) + 1) if name.startswith(part, i)]


def statistics(people, parts, gods):
    """{part: its statistics} for every part that stands in MIN_CODED names or more. A part stands in a name where
    its letters do, as the cutter and the page count it. For each part: the names it stands in; those it begins,
    those it ends, those it stands inside and those it is the whole of; the gods whose names stand in the same
    name clear of it (a god's name is a part whose letters are a god's name); the names of mothers, of fathers and
    of the dead; the sites; and the other parts with a code that touch it (they end where it begins, or begin
    where it ends). Every number is a number of names."""
    stands = {p: [n for n in sorted(people) if p in n] for p in sorted(parts)}
    coded = [p for p in sorted(parts) if len(stands[p]) >= MIN_CODED]
    divine = {q: god for q, god in gods.items() if q in parts}
    out = {}
    for p in coded:
        s = out[p] = {"names": len(stands[p]), "place": collections.Counter(), "gods": collections.Counter(), "roles": collections.Counter(),
                      "sites": collections.Counter(), "beside": collections.Counter()}
        for n in stands[p]:
            at = stands_at(n, p)
            s["place"].update({"whole name" if len(p) == len(n) else "first" if i == 0 else "last" if i + len(p) == len(n) else "middle" for i in at})
            s["gods"].update({god for q, god in divine.items() if q != p
                              and any(j + len(q) <= i or j >= i + len(p) for i in at for j in stands_at(n, q))})
            s["roles"].update(people[n]["roles"])
            s["sites"].update(people[n]["sites"])
            s["beside"].update({q for q in coded if q != p and any(n.startswith(q, i + len(p)) or (i >= len(q) and n.startswith(q, i - len(q))) for i in at)})
    return out


def block(code, s, codes):
    """A code's statistics as the pack shows them: numbers, English names of gods, sites and other codes. No letters."""
    def listed(counter, most=None):
        return ", ".join(f"{k} {v}" for k, v in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[:most]) or "none"

    return "\n".join([
        f"## {code}", "",
        f"- names: {s['names']}",
        "- place: " + ", ".join(f"{k} {s['place'].get(k, 0)}" for k in PLACES),
        f"- with gods: {listed(s['gods'])}",
        f"- whose names: mothers {s['roles'].get('mother', 0)}, fathers {s['roles'].get('father', 0)}, the dead {s['roles'].get('dead', 0)}",
        f"- sites: {listed(s['sites'], 8)}",
        f"- beside: {listed({codes[p]: v for p, v in s['beside'].items()}, 5)}", ""])


def packs_of(rows, gods, words, seed=SEED_PACKS):
    """(the key, {pack: its text for one reader, with the place of the answers file left open}): the cutter learns
    its parts from the tuning names, and each part that stands in MIN_CODED of all the names gets a code from a
    numbering drawn by lot. The codes are dealt into packs of about PACK, the known ones first and then the others,
    each in the order of their codes, so that every pack holds as many known parts as another, give or take one;
    within a pack the codes stand in their order, so that nothing in a pack says which are known. The key says of
    each code what part it is and, if its letters are a god's name of the map or a dictionary word with a meaning,
    what that is."""
    parts = learn_parts(names_of(rows, "tuning"))
    stats = statistics(people_of(rows), parts, gods)
    order = sorted(stats)
    random.Random(seed).shuffle(order)
    codes = {p: f"P{n:03d}" for n, p in enumerate(order, 1)}
    known = {p: known_of(p, gods, words) for p in order}
    deal = [p for p in order if known[p]] + [p for p in order if not known[p]]
    k = max(1, round(len(order) / PACK))
    groups = {f"N{i + 1}": sorted(deal[i::k], key=codes.get) for i in range(k)}
    key = {"codes": {}, "packs": {name: [codes[p] for p in ps] for name, ps in groups.items()}}
    for name, ps in groups.items():
        for p in ps:
            what = known[p]
            key["codes"][codes[p]] = {"part": p, "pack": name, "names": stats[p]["names"], "known": bool(what),
                                      "kinds": sorted({k for w in what or [] for k in w["kinds"]}), "is": what or []}
    texts = {name: BRIEF.replace("<<N>>", str(len(ps))) + "\n---\n\n" + "\n".join(block(codes[p], stats[p], codes) for p in ps)
             for name, ps in groups.items()}
    return key, texts


def packs():
    """The packs of gate C2, with the script in git as it stands (they are counted on the held-back names too),
    and not again once a reader has answered."""
    frozen()
    if any((HOME / "answers").glob("*.jsonl")):
        raise SystemExit("answers exist: the packs are not written again")
    gl, lex = the_map(), W.lexicon()
    key, texts = packs_of(the_rows(), gods_of(gl, lex), words_of(gl, lex, [(l["name"], M.lines_of(l)) for l in M.LAYERS[:len(LAYERS)]]))
    (HOME / "packs").mkdir(parents=True, exist_ok=True)
    (HOME / "answers").mkdir(exist_ok=True)
    for name, text in texts.items():
        for reader in "ab":
            (HOME / "packs" / f"{name}_{reader}.md").write_text(text.replace("<<ANSWERS>>", f"{ANSWERS}/{name}_{reader}.jsonl"),
                                                                encoding="utf-8")
    write("key.json", key)
    known = [c for c in key["codes"].values() if c["known"]]
    print(len(key["codes"]), "codes in", len(texts), "packs:", [len(v) for v in key["packs"].values()], "| known:", len(known),
          "of them with a kind:", sum(bool(c["kinds"]) for c in known))


def answers_of(key, folder):
    """{(reader, code): the reader's line}: a reader's file counts only for the codes of its own pack, the first
    line a code, and only with one of the kinds (capitals and spaces set aside)."""
    out = {}
    for name, codes in key["packs"].items():
        for reader in "ab":
            f = folder / f"{name}_{reader}.jsonl"
            for line in f.read_text(encoding="utf-8").splitlines() if f.exists() else []:
                try:
                    a = json.loads(line)
                except json.JSONDecodeError:
                    continue
                kind = " ".join(str(a.get("kind") or "").lower().split()) if isinstance(a, dict) else None
                if kind in KINDS and a.get("code") in codes:
                    out.setdefault((reader, a["code"]), a | {"kind": kind})
    return out


def meant(a):
    """A reader's meaning, or None where it gives none."""
    m = " ".join(str(a.get("meaning") or "").split())
    return None if m.lower() in NO_MEANING else m


def pairs_of(key, ans):
    """The pairs of meanings a judge has to compare: every code for which both readers give a meaning, with the
    key's meanings where the part is known."""
    out = []
    for code, c in key["codes"].items():
        a, b = ans.get(("a", code)), ans.get(("b", code))
        if a and b and meant(a) and meant(b):
            out.append({"code": code, "a": meant(a), "b": meant(b), "key": [w["meaning"] for w in c["is"]] if c["known"] else None})
    return out


def bar_c2(right, agreed):
    """A bar of gate C2: of the known parts both readers agree on, at least 8, and 80% of them right. With fewer
    than 8 it is neither met nor missed."""
    if agreed < BARS_C2["least"]:
        return "too small to decide"
    return "met" if right / agreed >= BARS_C2["rate"] else "missed"


def counted(key, ans, verdicts):
    """Gate C2 from the key, the readers' lines and the judge's verdicts (None: not judged yet).

    Kinds: the known parts whose key has a kind, to which both readers give one and the same kind (not "unclear");
    right where that kind is one of the key's. Meanings: the known parts to which both give a meaning that the
    judge calls the same; right where the judge calls it the key's. Kappa: the two readers' kinds over every code
    both answered. Listed: if the kinds' bar is met, the parts without a known meaning that both give the same
    kind; with the meaning both give (the first reader's wording) only if the meanings' bar is met too."""
    rows, pairs = [], []
    for code, c in key["codes"].items():
        a, b = ans.get(("a", code)), ans.get(("b", code))
        if a and b:
            pairs.append((a["kind"], b["kind"]))
        same_kind = a["kind"] if a and b and a["kind"] == b["kind"] != "unclear" else None
        v = (verdicts or {}).get(code) or {}
        both_mean = bool(a and b and meant(a) and meant(b))
        rows.append({"code": code, "part": c["part"], "known": c["known"], "kinds": c["kinds"], "a": a and a["kind"], "b": b and b["kind"],
                     "same_kind": same_kind, "kind_right": None if not (c["kinds"] and same_kind) else same_kind in c["kinds"],
                     "meanings": [meant(a), meant(b)] if both_mean else None,
                     "same_meaning": bool(v.get("same")) if both_mean and verdicts is not None else None,
                     "meaning_right": bool(v.get("same") and v.get("right")) if both_mean and c["known"] and verdicts is not None else None})
    kp = W.kappa(pairs)
    k_agreed = [r for r in rows if r["known"] and r["kind_right"] is not None]
    kinds = {"known_with_a_kind": sum(bool(r["known"] and r["kinds"]) for r in rows), "agreed": len(k_agreed),
             "right": sum(r["kind_right"] for r in k_agreed), "verdict": bar_c2(sum(r["kind_right"] for r in k_agreed), len(k_agreed))}
    if verdicts is None:
        meanings = {"verdict": "not judged yet"}
    else:
        m_agreed = [r for r in rows if r["known"] and r["same_meaning"]]
        meanings = {"agreed": len(m_agreed), "right": sum(r["meaning_right"] for r in m_agreed),
                    "verdict": bar_c2(sum(r["meaning_right"] for r in m_agreed), len(m_agreed))}
    listed = []
    if kinds["verdict"] == "met":
        for r in rows:
            if not r["known"] and r["same_kind"]:
                with_meaning = meanings["verdict"] == "met" and r["same_meaning"]
                listed.append({"code": r["code"], "part": r["part"], "kind": r["same_kind"]} | ({"proposal": r["meanings"][0]} if with_meaning else {}))
    return {"bars": BARS_C2, "codes": len(rows), "known": sum(r["known"] for r in rows), "answered_by_both": len(pairs),
            "kappa_kinds": None if kp is None else round(kp, 4), "kinds": kinds, "meanings": meanings,
            "both_give_a_meaning": sum(r["meanings"] is not None for r in rows), "listed": listed, "rows": rows}


def count():
    """Gate C2. The pairs of meanings are written for the judge; the meanings' bar is counted once the judge's
    verdicts stand in count-verdicts.json, one for every pair."""
    key = read("key.json")
    ans = answers_of(key, HOME / "answers")
    pairs = pairs_of(key, ans)
    write("count-pairs.json", pairs)
    verdicts = read("count-verdicts.json") if (HOME / "count-verdicts.json").exists() else None
    if verdicts is not None:
        missing = [p["code"] for p in pairs if not isinstance(verdicts.get(p["code"]), dict) or "same" not in verdicts[p["code"]]]
        if missing:
            raise SystemExit(f"no verdict for {', '.join(missing[:10])}: every pair of count-pairs.json needs one")
        unjudged = [p["code"] for p in pairs if p["key"] is not None and verdicts[p["code"]]["same"] and "right" not in verdicts[p["code"]]]
        if unjudged:
            raise SystemExit(f"no \"right\" for {', '.join(unjudged[:10])}: a known part whose two meanings are the same needs one")
    out = counted(key, ans, verdicts)
    write("count.json", out)
    print(json.dumps({k: v for k, v in out.items() if k not in ("rows", "listed")}, ensure_ascii=False, indent=1))
    print("listed:", len(out["listed"]), "| pairs for the judge:", len(pairs), "| verdicts:", "none yet" if verdicts is None else len(verdicts))


# ---------------------------------------------------------------------------------------------------- the figures

def figures():
    """What the page reports, from the local files as far as they stand: counts only, no letter of a name or of a
    part. The names are counted again from the map; the cutter's figures are those `learn` wrote, and its parts
    must still be those the cutter learns; the gates are read from their files."""
    rows = the_rows()
    tuning = tuning_figures(rows)
    cutter = {k: v for k, v in read("parts.json").items() if k != "parts"}
    if len(learn_parts(names_of(rows, "tuning"))) != cutter["parts_in_three_names"] or cutter["thresholds"] != learned_thresholds():
        raise SystemExit("parts.json is not what the cutter learns now: run `learn` again")
    out = {"names": totals_of(rows) | {"layers": list(LAYERS)},
           "tuning": {k: v for k, v in tuning.items() if k != "taken_off"} | {"sites": len(tuning["sites"]), "different_ends_taken_off": len(tuning["taken_off"])},
           "cutter": cutter}
    if (HOME / "held.json").exists():
        out["gate_c1"] = {k: v for k, v in read("held.json").items() if k != "rows"}
    if (HOME / "key.json").exists():
        key = read("key.json")
        known = [c for c in key["codes"].values() if c["known"]]
        out["packs"] = {"codes": len(key["codes"]), "packs": [len(v) for v in key["packs"].values()], "known": len(known),
                        "known_with_a_kind": sum(bool(c["kinds"]) for c in known),
                        "known_by_kind": dict(collections.Counter(k for c in known for k in c["kinds"]).most_common())}
    if (HOME / "count.json").exists():
        c = read("count.json")
        out["gate_c2"] = {k: v for k, v in c.items() if k not in ("rows", "listed")} | {
            "listed": len(c["listed"]), "listed_by_kind": dict(collections.Counter(x["kind"] for x in c["listed"]).most_common()),
            "listed_with_a_proposal": sum("proposal" in x for x in c["listed"])}
    return out


def public():
    figs = figures()
    PUBLIC.write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", PUBLIC, sorted(figs))


COMMANDS = {"names": names, "learn": learn, "held": held, "packs": packs, "count": count, "public": public}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        raise SystemExit(__doc__)
    COMMANDS[sys.argv[1]]()
