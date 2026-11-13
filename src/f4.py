"""F4, the pilot: whole Meroitic texts translated and scored against a printed rendering (NEXT_STEPS.md, step 25).

  python3 -I src/f4.py choose     the texts of the pilot and of the pages sample, by the rules below
  python3 -I src/f4.py packs      the two translators' packs, the baselines and the splitter's pack
  python3 -I src/f4.py judges     the judges' packs, once the translators and the splitter have answered
  python3 -I src/f4.py count      the scores against the bars, printed
  python3 -I src/f4.py public     the same, written to data/discovery/f4_pilot_figures.json (counts only)

packs and judges refuse to write their packs again once an agent has answered them. Everything this script reads
or writes but the figures file is local (data/sources/f4/): Millet's edition and Rilly's lexicon are in copyright,
and the agents' answers quote them. The answers are untrusted data: only their named fields are read.

The design, set before any agent answered (data/discovery/f4_pilot.md says it in prose):

1. The texts. Millet 2005 prints a rendering into English for 20 of its entries; an entry is held when corpus_v6
   has a row "GA nn" for every inscription it names. Its kind is the object Millet's first lines describe: a
   stela (or slab), an offering table, a label. The pilot takes, of each kind but the stela, the entry whose
   copy holds the largest share of Millet's text (runs of five letters, as src/experts/prepare.py counts them),
   then the longest; and three stelae among those whose copy holds at least COVERED of Millet's text: the
   longest, the lower median and the shortest, by words in our copy (ties by id).
2. The pages sample: PAGES texts drawn from the rows of corpus_v6 whose reading is under an open licence, by
   kind, of MIN_WORDS to MAX_WORDS words with at most LOST_SHARE of them lost. Their translations measure what a
   page costs, and they are the decoys (item 6).
3. The translator: one agent per pack (the pilot's texts, the sample's texts), blind to Millet 2005. Its pack
   holds the text of corpus_v6, the map's reading of every word (the gloss file of F2), every entry of Rilly's
   lexicon the words are built on with F2's status, and a few lines of what the project knows of these texts.
   Millet is taken out of all of it: the other scholars' proposals that name him, the lexicon's meanings and
   the analysts' notes that name him, and his weight in F2's statuses, which are counted again without his
   proposals and without the verdicts of the check against Millet 2005 (blind_statuses).
4. The baseline: the map's reading of every word, word by word, and nothing else (baseline()).
5. The splitter: one agent, blind to every translation, cuts Millet's renderings of the pilot's texts into
   units of meaning, each with the Meroitic it renders, its kind, Millet's doubt, and whether Millet leaves the
   word untranslated ("open").
6. The judges: two agents. Each gets every pilot text's rendering, its units that are not open, and three
   readings in an order of its own: the translator's, the baseline and a decoy, which is the translator's
   reading of a text of the pages sample. The decoys are assigned so that they share as few content words with
   the rendering as can be (assign_decoys); a unit counts in the decoy measure only when its decoy shares no
   content word with it (clean()).
7. The score of a reading: (given + half of partly) / scored units, pooled over the pilot's texts, the mean of
   the two judges. Scored units are the units the judges get whose Meroitic stands in our copy (in_copy).
   The bars and the expected scores are BARS and EXPECTED, written before any agent answered.
"""
import collections
import itertools
import json
import pathlib
import random
import re
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts")]
import close as K                                      # noqa: E402
import lexicon as X                                    # noqa: E402
import prepare as P                                    # noqa: E402
import tally as T                                      # noqa: E402

CORPUS = ROOT / "data/corpus_v6.jsonl"
GLOSSES = X.GLOSSES                                    # the map of corpus_v6 with the analysts' answers (local)
OUT = ROOT / "data/sources/f4"                         # local only
PUBLIC = ROOT / "data/discovery/f4_pilot_figures.json"

COVERED = 0.85                  # a stela's copy must hold this share of Millet's runs of five letters
PAGES = {"funerary": 3, "royal or temple (stela, wall, cartouche, label)": 1, "graffito": 1}
MIN_WORDS, MAX_WORDS, LOST_SHARE = 8, 60, 0.2
SEED = "f4 pilot"               # every draw has a Random of its own, seeded with SEED and the draw's name
READINGS = ("translator", "baseline", "decoy")
LETTERS = "ABC"
VERDICTS = ("given", "partly", "wrong", "missing")
STATUSES = ("agreed", "stated by one", "disputed", "proposed", "context", "own", "name", "number", "open", "lost")
UNIT_KINDS = ("name", "relation", "title", "place", "god", "formula", "other")
MILLET = re.compile(r"(?i)\bmillet")
WITHHELD = "(withheld)"
# Set on 2026-11-12, before any agent answered.
BARS = {"kappa": 0.6,            # the judges' Cohen's kappa on the four verdicts, translator and baseline readings
        "decoys_accepted": 0.10}  # the most of its clean decoy units a judge may call given or partly
EXPECTED = {"translator": 0.50, "translator_range": (0.35, 0.65),
            "baseline": 0.35, "baseline_range": (0.20, 0.50),
            "lead": 0.10,         # translator minus baseline; under 0.05 the translator is not worth its tokens
            "translator_wrong": 0.15}
# subagent tokens of each agent, from the task notifications, by hand after the run (12 November 2026)
TOKENS = {"translator_pilot": 145118, "translator_pages": 104696, "splitter": 99501, "judge1": 107682, "judge2": 103984}


# ---------------------------------------------------------------------------------------------------- the texts

def rows_of(path=CORPUS):
    return {r["id"]: r for r in map(json.loads, path.read_text(encoding="utf-8").splitlines())}


def glosses_of(path=GLOSSES):
    return {r["id"]: r["glosses"] for r in map(json.loads, path.read_text(encoding="utf-8").splitlines())}


def v6_id(number):
    """corpus_v6's id of a Gebel Adda inscription: "GA04" -> "GA 04"."""
    return "GA " + number[2:]


def object_kind(block):
    """The object an entry of Millet 2005 is written on, from its first lines."""
    head = " ".join(block.split())[:160].lower()
    if re.search(r"offering[ -]table", head):
        return "offering table"
    if re.search(r"\blabel\b", head):
        return "label"
    if re.search(r"\bstela|\bslab", head):
        return "stela"
    return "other"


def text_letters(block):
    """The letters of an entry's numbered lines of transliteration, as prepare.millet_letters reads them, also
    where a line number follows a side ("recto 1:") or a part ("A 1:")."""
    cut = re.search(r"^(COMMENTARY|RENDERING)", block, re.M)
    part = block[:cut.start()] if cut else block
    numbered = re.compile(r"^(?:recto |verso |[A-Z] )?\d{1,2}:\s")
    lines = [numbered.sub("", l) for l in part.split("\n") if numbered.match(l)]
    return P.reduced_expert(" ".join(lines))


def rendered(entries=None):
    """{(numbers of an entry with a rendering): the entry's text}, its parts joined (GA13 & GA16 is one entry)."""
    out = collections.OrderedDict()
    for numbers, block in P.millet_parts(entries if entries is not None else P.millet_entries()):
        out.setdefault(tuple(sorted(numbers)), []).append(block)
    return {k: "\n\n".join(v) for k, v in out.items() if re.search(r"^RENDERING", "\n".join(v), re.M)}


def candidates(entries, rows):
    """The entries with a rendering that corpus_v6 holds, each with its kind, words and the share of Millet's
    text its copy holds."""
    out = []
    for numbers, block in entries.items():
        if len(numbers) != 1 or v6_id(numbers[0]) not in rows:
            continue
        tid = v6_id(numbers[0])
        g, o = P.runs(text_letters(block)), P.runs(P.reduced_ours(rows[tid]["text"].split()))
        out.append({"id": tid, "kind": object_kind(block), "words": len(rows[tid]["text"].split()),
                    "covered": round(len(g & o) / len(g), 4) if g else 0.0})
    return out


def choose(cands, covered=COVERED):
    """The pilot's texts (item 1 of the module's docstring): of each kind but the stela, the best covered and
    then the longest; then the longest, the lower median and the shortest of the stelae covered enough."""
    out = []
    for kind in sorted({c["kind"] for c in cands} - {"stela"}):
        out.append(sorted((c for c in cands if c["kind"] == kind), key=lambda c: (-c["covered"], -c["words"], c["id"]))[0]["id"])
    stelae = sorted((c for c in cands if c["kind"] == "stela" and c["covered"] >= covered), key=lambda c: (c["words"], c["id"]))
    for c in (stelae[-1], stelae[(len(stelae) - 1) // 2], stelae[0]) if stelae else ():
        if c["id"] not in out:
            out.append(c["id"])
    return out


def pages_sample(rows, gl, seed=SEED):
    """The pages sample (item 2): per kind, a draw of its own from the open rows of the right size."""
    out = []
    for kind, n in PAGES.items():
        pool = sorted(i for i, r in rows.items() if r.get("open") and r["kind"] == kind and i in gl
                      and MIN_WORDS <= len(gl[i]) <= MAX_WORDS
                      and sum(g["level"] == "lost" for g in gl[i]) <= LOST_SHARE * len(gl[i]))
        out += random.Random(f"{seed} pages {kind}").sample(pool, n)
    return out


def texts(entries=None, rows=None, gl=None):
    """(the pilot's ids, the pages sample's ids, the candidates)."""
    entries = rendered() if entries is None else entries
    rows, gl = rows or rows_of(), gl or glosses_of()
    cands = candidates(entries, rows)
    return choose(cands), pages_sample(rows, gl), cands


# ------------------------------------------------------------------------------------ the translator's materials

def millet_free_editors(folder=X.EXPERT):
    """The editors' verdicts of F2 (lexicon.editors) without those of the check against Millet 2005."""
    return X.editors(folder, leave_out=lambda r, a: X.misread(r, a) or r["source"] == "millet")


def names_millet(p):
    """Whether a proposal the lexicon records is Millet's or speaks of his."""
    return bool(MILLET.search(p.get("author") or "") or MILLET.search(p.get("proposal") or ""))


def without_millet(e, editors):
    return {**e, "editors": dict(editors.get(e["headword"], {})),
            "proposals": [p for p in e["proposals"] if not names_millet(p)]}


def blind_statuses(entries, verdicts, editors):
    """F2's status of every entry behind a translated word, counted by lexicon.status without Millet's proposals
    and without the verdicts of the check against Millet 2005."""
    return {e["headword"]: X.status(without_millet(e, editors), verdicts) for e in entries if e["uses_translated"]}


def scrub(text):
    """A text of the lexicon or the map as the translator may see it: withheld when it names Millet."""
    return WITHHELD if MILLET.search(text or "") else (text or "")


def millet_heads(entries):
    """The entries whose meaning in the lexicon names Millet: the map's gloss of a word built on one of them is
    that meaning cut short, which may no longer name him ("would mean to control"), so it is withheld too."""
    return frozenset(h for h, e in entries.items() if MILLET.search(e.get("meaning") or ""))


def heads_of(g):
    return [p.get("entry") for p in g.get("parts") or [] if p.get("entry") and p.get("entry") not in X.PSEUDO]


def blind_gloss(g, withheld=frozenset()):
    """The map's gloss of a word, or WITHHELD when it names Millet or rests on an entry of millet_heads()."""
    gloss = (g.get("gloss") or "").strip()
    return WITHHELD if set(heads_of(g)) & withheld else scrub(gloss)


def word_reading(g, withheld=frozenset()):
    """The baseline's reading of one word: the map's gloss, marked by its level; a gloss withheld from the
    translator (blind_gloss) is withheld here too, as an unknown word."""
    level, form = g["level"], g["form"]
    gloss = blind_gloss(g, withheld)
    if gloss == WITHHELD:
        return f"[{form}: ?]"
    if level == "lost":
        return f"[{form}: signs lost]"
    if level == "unknown" or gloss in ("", "?"):
        return f"[{form}: ?]"
    if level == "name" and gloss in P.MASKED:
        return f"{form[:1].upper()}{form[1:]} (a name)"
    if level == "kind":
        return f"[{form}: {gloss.strip('[]')}]"
    if level == "hypothesis":
        return gloss if gloss.endswith("(?)") else f"{gloss} (?)"
    return gloss


def baseline(gs, withheld=frozenset()):
    """The baseline (item 4): the map's readings, word by word, with the translator's glosses withheld."""
    return " · ".join(word_reading(g, withheld) for g in gs)


def part_status(h, st, entries):
    if h in st:
        return st[h]
    e = entries.get(h)
    return f"not rated by F2; Rilly: {e['status'] or 'no status'}" if e else ""


CONTEXT = """Most inscriptions of the corpus are epitaphs, on stelae and offering tables. Since Griffith (1911) their
order has been read as: an invocation of Isis and Osiris; the name of the dead; the mother and the father; the
relatives of the dead, each with titles and places; and wishes for the dead, with verbs of offering. The verbs of
those wishes are among the words the map knows least (data/discovery/coverage.md). Other texts are royal or
temple inscriptions, graffiti, and documents written on ostraca or wood."""

TRANSLATE = """# Whole Meroitic texts: a translation built from the project's readings

Meroitic, the language of the kingdom of Kush (in today's Sudan, about 300 BC to AD 350), is written in a
script that can be read aloud, but the language is understood only in part: some words have an accepted
meaning, many have only a proposal, and many have none. Below are {n} inscriptions of the project's corpus.
For each you get its words in order and what the project's word-by-word map holds for each word. After the
texts come the entries of the lexicon those words are built on (Rilly 2003), each with a status from the
project's own check: does a second scholar give the same meaning?

Your task, for each inscription: translate it as a whole, as a careful scholar would from these materials.

1. Give every word, in order, its reading and one status:
   - "agreed": its meaning rests only on entries of F2 status "agreed by two scholars";
   - "stated by one": it rests on an entry of F2 status "stated by one", or on an entry not rated by F2 that
     Rilly states as established or probable;
   - "disputed": it rests on an entry of F2 status "disputed"; say in the note which reading you take;
   - "proposed": the lexicon gives only a proposal (F2 "proposed", or Rilly's "hypothesis");
   - "context": you infer the meaning from the word's place in the text or from a parallel in this pack; say why;
   - "own": you take the meaning from your own knowledge of Meroitic, not from this pack; say what;
   - "name" or "number";
   - "open": no meaning can be given;
   - "lost": the word has lost signs and cannot be read.
   A word built on entries of different statuses takes the weakest of them.
2. Cut the text into phrases (a run of words that belong together: a name with its title, one wish) and render
   each into English.
3. Write the whole text as one running English translation, as a reader would read it. What is open stays open:
   write the Meroitic word in square brackets, or [?]. A guess is not a reading: mark it with "(?)".

The map's levels: "meaning" and "grammar": the lexicon gives the word an established or probable meaning;
"name" and "number"; "hypothesis": the lexicon has only a proposal, or the map's analyst was unsure of the cut;
"kind": only the kind of word is known (a title, a verb); "unknown": nothing is known; "lost": signs are lost.
The map reads word by word and makes mistakes: a name read as a word, a word cut wrongly, a gloss that does not
fit. You may depart from it; say so in the note. "+i", "+lowi" and the like in a gloss are endings the map cut
off and did not translate.

Spelling: S is the sign s, s the sign se, N the sign ne, X the sign ẖ, x the sign ḫ; a dot is a lost sign.
Personal names are written as they stand; give them a capital, in the same letters.

What the project knows of these texts beyond the map:

{context}

Use only this file. Do not open other files of the repository, and do not search the web.

Write your answers to the file `{answers}` as JSON lines, one line per inscription, in the order of this pack,
nothing else in the file:

    {{"text": "<its id>", "words": [{{"n": 1, "form": "<the word as in the table>", "reading": "...", "status": "...", "note": ""}}], "phrases": [{{"from": 1, "to": 3, "english": "..."}}], "translation": "...", "left_open": "one sentence: what stays open, and why"}}

Every word of the text must be in "words" once, in order, with its number and its form as the table gives them.
When the file is written, reply with one line: how many inscriptions you wrote, and anything you could not do.
"""


def entry_block(h, e, st, ours):
    """The translator's view of one entry of the lexicon: its kind, Rilly's page and status, its meaning, F2's
    status and meaning in our words, and the other scholars' proposals; Millet left out."""
    props = [p for p in e["proposals"] if not names_millet(p)]
    lines = [f"### {h}", "",
             f"- {e['kind'] or 'kind not given'}; Rilly 2003, p. {e['page']}, {e['status'] or 'no status'}",
             f"- meaning in the lexicon: {X.C.short(scrub(e['meaning']), 240) or '(none)'}",
             f"- F2: {part_status(h, st, {h: e})}" + (f"; in our words: {ours[h]}" if ours.get(h) else "")]
    if props:
        lines.append("- other scholars, as the lexicon records them: " + "; ".join(
            f"{p['author']}: {X.C.short(p['proposal'], 160)}" for p in props[:6]) + ("; ..." if len(props) > 6 else ""))
    return "\n".join(lines) + "\n"


def translator_pack(ids, rows, gl, entries, st, ours, answers):
    """The text of a translator's pack, and how many texts of the lexicon or the map it withheld."""
    parts = [TRANSLATE.format(n=len(ids), context=CONTEXT, answers=answers)]
    used, withheld, heads_withheld = [], 0, millet_heads(entries)
    for tid in ids:
        r = rows[tid]
        parts.append(f"\n---\n\n## {tid}\n\nSite: {r['site']}. Kind: {r['kind']}. Words: {len(gl[tid])}.\n\n"
                     "| n | word | level | the map's reading | built on (F2 status) | the analyst's note |\n"
                     "|---|---|---|---|---|---|\n")
        for n, g in enumerate(gl[tid], 1):
            heads = heads_of(g)
            used += [h for h in heads if h in entries and h not in used]
            note = scrub(g.get("evidence") or "") if g.get("by") == "analyst" else ""
            gloss = blind_gloss(g, heads_withheld)
            withheld += (gloss == WITHHELD) + (note == WITHHELD)
            built = " + ".join(f"{h} ({part_status(h, st, entries) or 'not in the lexicon'})" for h in heads)
            cells = (str(n), g["form"], g["level"], gloss, built, X.C.short(note, 160))
            parts.append("| " + " | ".join(c.replace("|", "/") for c in cells) + " |\n")
    parts.append("\n---\n\n## The entries of the lexicon\n\n")
    for h in used:
        withheld += bool(MILLET.search(entries[h]["meaning"] or ""))
        parts.append(entry_block(h, entries[h], st, ours) + "\n")
    return "".join(parts), withheld


# --------------------------------------------------------------------------------------------------- the splitter

def sections(block):
    """(transliteration, rendering) of an entry: each section TEXT up to its notes or commentary, and each
    section RENDERING up to the next section; the running heads of the journal's pages left out."""
    block = P.clean(re.sub(r"^(?:JSSEA 32 \(2005\) \d+|\d+ Studies Millet)\s*$\n?", "", block, flags=re.M))
    heads = r"^(?:TEXT|NOTES?:?|COMMENTARY|RENDERING)\s*$"
    text = [m.group(1).strip() for m in re.finditer(r"^TEXT\s*$(.*?)(?=%s|\Z)" % heads, block, re.M | re.S)]
    rend = [m.group(1).strip() for m in re.finditer(r"^RENDERING\s*$(.*?)(?=%s|\Z)" % heads, block, re.M | re.S)]
    return "\n\n".join(text), "\n\n".join(rend)


SPLIT = """# Cut printed renderings of Meroitic inscriptions into units of meaning

Below are {n} entries of N. B. Millet, "The Meroitic Inscriptions from Gebel Adda", Journal of the Society for
the Study of Egyptian Antiquities 32 (2005), as the text layer of a PDF: for each, the transliteration
(numbered lines; the dots under doubtful letters and some letters may have fallen onto lines of their own) and
the rendering into English.

Cut each rendering into units of meaning: the smallest pieces a reader learns something from, so that another
translation of the same inscription can later be checked against it unit by unit.

- Each person named, with their role in the text ("the deceased is X", "his mother is Y"), is one unit: the
  name and the role together.
- Each relation between two people that is not already such a role ("X is a relative of Y") is one unit.
- Each title, office or rank is one unit, and the place it is held in is another.
- Each invocation of a god is one unit, and each wish or formula ("may he drink water") is one unit.
- Each other statement is one unit.
- Leave nothing of the rendering out, and add nothing it does not say.

For each unit give:

- "english": the rendering's own words for it, at most fifteen;
- "meroitic": the word or words of the transliteration it renders, as printed; "" when it renders no one word;
- "kind": "name" (a person with a role), "relation", "title", "place", "god", "formula" or "other";
- "doubt": true when Millet marks it as unsure ("?", "perhaps");
- "open": true when Millet leaves the Meroitic untranslated (he writes the Meroitic word itself in the
  rendering, or leaves a gap).

Write to the file `{answers}` as JSON lines, one line per unit, the entries in the order of this file and the
units in the order of the rendering, numbered from U01 in each entry, nothing else in the file:

    {{"text": "GA41", "unit": "U01", "english": "...", "meroitic": "...", "kind": "...", "doubt": false, "open": false}}

Use only this file. Do not open other files of the repository, and do not search the web. When the file is
written, reply with one line: how many units you wrote for each entry.
"""


def splitter_pack(ids, entries, answers):
    parts = [SPLIT.format(n=len(ids), answers=answers)]
    for tid in ids:
        number = tid.replace(" ", "")
        translit, rend = sections(entries[(number,)])
        parts.append(f"\n---\n\n## {number}\n\n### Transliteration\n\n```\n{translit}\n```\n\n"
                     f"### Rendering\n\n```\n{rend}\n```\n")
    return "".join(parts)


# ----------------------------------------------------------------------------------------------------- the judges

def stems(text):
    return K.content(text or "")


def assign_decoys(renderings, decoys):
    """{pilot text: pages text}: each pages text used once, the assignment with the fewest content words shared
    between a rendering and its decoy in all (the first such in the order of the permutations). renderings and
    decoys map ids to text; there must be as many decoys as renderings or more."""
    pilot, pages = sorted(renderings), sorted(decoys)
    r = {t: stems(renderings[t]) for t in pilot}
    d = {t: stems(decoys[t]) for t in pages}
    shared = {(a, b): len({x for x in r[a] if K.shares({x}, d[b])}) for a in pilot for b in pages}
    best = min(itertools.permutations(pages, len(pilot)), key=lambda p: sum(shared[a, b] for a, b in zip(pilot, p)))
    return dict(zip(pilot, best)), {a: shared[a, b] for a, b in zip(pilot, best)}


def clean(unit_english, decoy_text):
    """Whether a unit counts in the decoy measure: its decoy shares no content word with it."""
    return not K.shares(stems(unit_english), stems(decoy_text))


def order_of(judge, text, seed=SEED):
    """{letter: reading} for one judge and one text, from a Random of its own."""
    return dict(zip(LETTERS, random.Random(f"{seed} order judge{judge} {text}").sample(READINGS, len(READINGS))))


def in_copy(meroitic, ours):
    """Whether the Meroitic a unit renders, as Millet prints it, stands in our copy (bare letters, as
    prepare.reduced_expert and reduced_ours give them): as a run, or half of its runs of four letters. A unit
    that names no word counts as in our copy."""
    m = P.reduced_expert((meroitic or "").replace("ḫ", "x").replace("ẖ", "h"))
    if not m:
        return True
    if m in ours:
        return True
    runs = P.runs(m, 4)
    return bool(runs) and len(runs & P.runs(ours, 4)) >= len(runs) / 2


JUDGE = """# A printed rendering beside other readings of the same Meroitic inscriptions, unit by unit

For each of {n} inscriptions below you get:

- the rendering into English printed by a scholar, N. B. Millet (2005), and the same rendering cut into
  numbered units of meaning;
- three other readings of the same inscription, "Reading A", "Reading B" and "Reading C", in no particular
  order. They were made in different ways: some may be poor, some may be lists of word-by-word glosses, and some
  may not fit the inscription at all.

For every unit and every reading, give one verdict:

- "given": the reading states the unit's meaning. The wording may differ. A person must have the same name in
  the same role; names are spelled differently (Millet writes them in an English form with vowels, the readings
  in the letters of the transliteration, where S is s, s is se, N is ne, X is h and x is kh). A relation, title,
  place or wish must be the same. Where the unit keeps a Meroitic word untranslated, the reading gives it when it
  keeps the same word as the same kind of word.
- "partly": the reading states something that overlaps but differs in a way that matters: the right name in
  another role, a kin term of another degree, a title of another rank, a meaning much vaguer or much narrower
  than the unit's, the right wish with another object.
- "wrong": the reading gives this part of the inscription another meaning.
- "missing": the reading says nothing for this unit: it leaves the word open ("[?]", the Meroitic word in
  brackets), has a gap, or leaves it out.

A meaning the reading marks as unsure ("?", "perhaps") still counts: judge the meaning it gives. Judge only by
what the rendering and the reading say. Do not use your own knowledge of Meroitic, and do not decide which of
them is right: the question is only whether the reading says what the unit says.

Write to the file `{answers}` as JSON lines, one line per unit and reading, in the order of this file (for each
inscription, unit by unit, and for each unit readings A, B and C), nothing else in the file:

    {{"text": "GA41", "unit": "U01", "reading": "A", "verdict": "given", "note": "at most twelve words"}}

Every unit of every inscription gets exactly three lines. Use only this file. Do not open other files of the
repository, and do not search the web. When the file is written, reply with one line: how many lines you wrote,
and anything that could not be judged.
"""


def judge_pack(judge, ids, entries, units, readings, answers):
    """The text of one judge's pack. units: {text: [unit]}; readings: {text: {reading name: text}}."""
    parts = [JUDGE.format(n=len(ids), answers=answers)]
    for tid in ids:
        number = tid.replace(" ", "")
        _, rend = sections(entries[(number,)])
        parts.append(f"\n---\n\n## {number}\n\n### The printed rendering\n\n```\n{rend}\n```\n\n"
                     "### Its units\n\n| unit | kind | the rendering's words |\n|---|---|---|\n")
        for u in units[tid]:
            if not u["open"]:
                parts.append(f"| {u['unit']} | {u['kind']} | {u['english'].replace('|', '/')} |\n")
        for letter, name in order_of(judge, tid).items():
            parts.append(f"\n### Reading {letter}\n\n{readings[tid][name]}\n")
    return "".join(parts)


# -------------------------------------------------------------------------------------------- answers and checks

def text_id(s, ids):
    """The id of ids an answer names, spaces aside ("GA41" is "GA 41"), or None."""
    compact = str(s or "").replace(" ", "")
    return next((i for i in ids if i.replace(" ", "") == compact), None)


def jsonl(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()] if path.exists() else []


def check_translation(a, gs):
    """The faults of one translator's answer against the text's words: [] when it gives every word once, in
    order, with a known status, and a running translation."""
    faults = []
    words = a.get("words") or []
    if [w.get("form") for w in words] != [g["form"] for g in gs]:
        faults.append("the words are not the text's words in order")
    if [w.get("n") for w in words] != list(range(1, len(gs) + 1)):
        faults.append("the words are not numbered 1 to n")
    bad = sorted({str(w.get("status")) for w in words} - set(STATUSES))
    if bad:
        faults.append("unknown statuses: " + ", ".join(bad))
    if not (a.get("translation") or "").strip():
        faults.append("no running translation")
    return faults


def translations(path, ids, gl):
    """{text: answer} of a translator's file, and the faults found; a text answered twice keeps its first."""
    out, faults = {}, {}
    for a in jsonl(path):
        t = text_id(a.get("text"), ids)
        if t and t not in out:
            out[t] = a
            faults[t] = check_translation(a, gl[t])
    for t in ids:
        if t not in out:
            faults[t] = ["not answered"]
    return out, {t: f for t, f in faults.items() if f}


def units_of(path, ids):
    """{text: [unit]} of the splitter's file: the units of the pilot's texts, with a known kind, each once."""
    out = collections.defaultdict(list)
    seen = set()
    for u in jsonl(path):
        t = text_id(u.get("text"), ids)
        key = (t, u.get("unit"))
        if t and key not in seen and (u.get("english") or "").strip():
            seen.add(key)
            out[t].append({"unit": u["unit"], "english": u["english"].strip(), "meroitic": u.get("meroitic") or "",
                           "kind": u.get("kind") if u.get("kind") in UNIT_KINDS else "other",
                           "doubt": u.get("doubt") is True, "open": u.get("open") is True})
    return dict(out)


def verdicts_of(path, key, judge):
    """{(text, unit, reading name): verdict} of one judge, mapped through the key's order; unknown verdicts and
    lines for units or readings not in the pack are left out, and a line given twice keeps its first."""
    out = {}
    order = key["order"][str(judge)]
    for a in jsonl(path):
        t = text_id(a.get("text"), list(order))
        name = order.get(t, {}).get(a.get("reading"))
        k = (t, a.get("unit"), name)
        if name and a.get("unit") in key["units"].get(t, {}) and a.get("verdict") in VERDICTS and k not in out:
            out[k] = a["verdict"]
    return out


# ---------------------------------------------------------------------------------------------------- the count

def score(counts):
    """(given + half of partly) / units, or None without units."""
    n = sum(counts.get(v, 0) for v in VERDICTS)
    return round((counts.get("given", 0) + 0.5 * counts.get("partly", 0)) / n, 4) if n else None


def tallies(verdicts, units, name):
    """Counter of a judge's verdicts on one reading over the given units [(text, unit)]."""
    return collections.Counter(verdicts.get((t, u, name), "unanswered") for t, u in units)


def judges_agreement(one, two, units, names=("translator", "baseline")):
    pairs = [(one[k], two[k]) for t, u in units for n in names for k in [(t, u, n)] if k in one and k in two]
    return {"pairs": len(pairs), "same": sum(a == b for a, b in pairs), "kappa": T.kappa(pairs),
            "kappa_given_or_not": T.kappa([(a == "given", b == "given") for a, b in pairs])}


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(statistics.mean(xs), 4) if xs else None


def count(out=OUT, rows=None, gl=None, entries=None):
    """Every figure of the pilot but the costs' sizing: the scores, the agreement, the decoys, the bars."""
    rows, gl = rows or rows_of(), gl or glosses_of()
    key = json.loads((out / "key.json").read_text(encoding="utf-8"))
    ids, pages = key["pilot"], key["pages"]
    units = units_of(out / "answers" / "splitter.jsonl", ids)
    judged = [(t, u["unit"]) for t in ids for u in units.get(t, []) if not u["open"]]
    scored = [(t, u) for t, u in judged if key["units"][t][u]["in_copy"]]
    v = {j: verdicts_of(out / "answers" / f"judge{j}.jsonl", key, j) for j in (1, 2)}
    figs = {"pilot": ids, "pages": pages, "decoys": key["decoys"], "decoy_shared_words": key["decoy_shared_words"]}
    every = [u for t in ids for u in units.get(t, [])]
    figs["units"] = {"all": len(every), "open": sum(u["open"] for u in every), "judged": len(judged),
                     "not_in_copy": len(judged) - len(scored), "scored": len(scored),
                     "doubt_scored": sum(u["doubt"] for t in ids for u in units.get(t, [])
                                         if (t, u["unit"]) in set(scored)),
                     "by_kind": dict(collections.Counter(key["units"][t][u]["kind"] for t, u in scored)),
                     "per_text": {t: sum(x == t for x, _ in scored) for t in ids}}
    figs["scores"] = {}
    for j in (1, 2):
        figs["scores"][str(j)] = {}
        for name in READINGS:
            c = tallies(v[j], scored, name)
            figs["scores"][str(j)][name] = {**{x: c.get(x, 0) for x in VERDICTS + ("unanswered",)},
                                            "score": score(c), "given_share": round(c.get("given", 0) / len(scored), 4)
                                            if scored else None,
                                            "wrong_share": round(c.get("wrong", 0) / len(scored), 4) if scored else None}
    figs["score"] = {n: mean([figs["scores"][j][n]["score"] for j in ("1", "2")]) for n in READINGS}
    figs["given"] = {n: mean([figs["scores"][j][n]["given_share"] for j in ("1", "2")]) for n in READINGS}
    figs["wrong"] = {n: mean([figs["scores"][j][n]["wrong_share"] for j in ("1", "2")]) for n in READINGS}
    figs["lead"] = (round(figs["score"]["translator"] - figs["score"]["baseline"], 4)
                    if None not in (figs["score"]["translator"], figs["score"]["baseline"]) else None)
    figs["with_units_not_in_copy"] = {n: mean([score(tallies(v[j], judged, n)) for j in (1, 2)]) for n in READINGS}
    figs["per_text"] = {t: {n: mean([score(tallies(v[j], [(x, u) for x, u in scored if x == t], n)) for j in (1, 2)])
                            for n in ("translator", "baseline")} for t in ids}
    # not set before the run: each text weighs the same (GA28 holds most of the pilot's units)
    figs["per_text_mean"] = {n: mean([figs["per_text"][t][n] for t in ids]) for n in ("translator", "baseline")}
    # not set before the run: on how many units the translator's verdict is better than the baseline's, or worse,
    # in the order given, partly, missing, wrong (leaving a unit open is better than getting it wrong)
    rank = {"given": 3, "partly": 2, "missing": 1, "wrong": 0}
    figs["unit_by_unit"] = {str(j): dict(collections.Counter(
        "better" if rank[a] > rank[b] else "worse" if rank[a] < rank[b] else "same"
        for t, u in scored for a, b in [(v[j].get((t, u, "translator")), v[j].get((t, u, "baseline")))] if a and b))
        for j in (1, 2)}
    figs["by_kind"] = {k: {n: mean([score(tallies(v[j], [(t, u) for t, u in scored if key["units"][t][u]["kind"] == k], n))
                                    for j in (1, 2)]) for n in ("translator", "baseline")}
                       for k in sorted(figs["units"]["by_kind"])}
    figs["agreement"] = judges_agreement(v[1], v[2], scored)
    figs["decoys_measure"] = {}
    for j in (1, 2):
        c = collections.Counter(v[j].get((t, u, "decoy"), "unanswered") for t, u in scored if key["units"][t][u]["clean"])
        figs["decoys_measure"][str(j)] = {"clean_units": sum(c.values()), "accepted": c["given"] + c["partly"],
                                          "verdicts": dict(c)}
    k = figs["agreement"]["kappa"]
    figs["bars"] = {"kappa": k is not None and k >= BARS["kappa"],
                    "decoys_accepted": all(d["accepted"] <= BARS["decoys_accepted"] * d["clean_units"]
                                           for d in figs["decoys_measure"].values())}
    figs["bars_set"], figs["expected"] = BARS, EXPECTED
    tr, _ = translations(out / "answers" / "translator_pilot.jsonl", ids, gl)
    tp, _ = translations(out / "answers" / "translator_pages.jsonl", pages, gl)
    st = collections.Counter(w.get("status") for a in list(tr.values()) + list(tp.values()) for w in a["words"])
    figs["translator"] = {"words": sum(st.values()), "statuses": dict(st.most_common()),
                          "words_pilot": sum(len(gl[t]) for t in ids), "words_pages": sum(len(gl[t]) for t in pages)}
    figs["blind"] = key["blind"]
    return figs


def sizing(figs, tokens, rows, gl, entries=None):
    """What the full run would cost at the pilot's rates: the scored run (every rendering of Millet held in
    corpus_v6) and the pages (every open row of corpus_v6). Rates per word of text for the translators, per word
    of rendering for the splitter, per line of verdict for the judges."""
    if not tokens:
        return {}
    entries = rendered() if entries is None else entries
    held = [c["id"] for c in candidates(entries, rows)]
    rend_words = lambda ids: sum(len(sections(entries[(t.replace(" ", ""),)])[1].split()) for t in ids)   # noqa: E731
    pilot, pages = figs["pilot"], figs["pages"]
    per_word_pilot = tokens["translator_pilot"] / figs["translator"]["words_pilot"]
    per_word_pages = tokens["translator_pages"] / figs["translator"]["words_pages"]
    per_rend_word = tokens["splitter"] / rend_words(pilot)
    lines = 3 * figs["units"]["judged"]
    per_line = (tokens["judge1"] + tokens["judge2"]) / (2 * lines)
    units_per_rend_word = figs["units"]["judged"] / rend_words(pilot)
    open_rows = [i for i, r in rows.items() if r.get("open")]
    held_words, open_words = sum(len(gl[t]) for t in held), sum(len(gl[t]) for t in open_rows)
    scored_run = {"texts": len(held), "words": held_words, "rendering_words": rend_words(held),
                  "translator": round(per_word_pilot * held_words), "splitter": round(per_rend_word * rend_words(held)),
                  "judges": round(per_line * 2 * 3 * units_per_rend_word * rend_words(held))}
    scored_run["total"] = scored_run["translator"] + scored_run["splitter"] + scored_run["judges"]
    pages_run = {"texts": len(open_rows), "words": open_words, "translator": round(per_word_pages * open_words)}
    scored_tokens = tokens["translator_pilot"] + tokens["splitter"] + tokens["judge1"] + tokens["judge2"]
    per_text = {"translator_pilot": round(tokens["translator_pilot"] / len(pilot)),
                "translator_pages": round(tokens["translator_pages"] / len(pages)),
                "scored_text": round(scored_tokens / len(pilot))}
    return {"per_text": per_text,
            "rates": {"translator_per_word_pilot": round(per_word_pilot), "translator_per_word_pages": round(per_word_pages),
                      "splitter_per_rendering_word": round(per_rend_word), "judge_per_line": round(per_line, 1),
                      "units_per_rendering_word": round(units_per_rend_word, 4)},
            "pilot_total": sum(tokens.values()), "scored_run": scored_run, "pages_run": pages_run}


# -------------------------------------------------------------------------------------------------- the commands

def packs(out=OUT):
    """The two translators' packs, the baselines and the splitter's pack, and the first part of the key. Refuses
    once a translator or the splitter has answered."""
    if any((out / "answers" / f).exists() for f in ("translator_pilot.jsonl", "translator_pages.jsonl", "splitter.jsonl")):
        raise SystemExit(f"{out}/answers holds a translator's or the splitter's answers: not writing the packs again")
    rows, gl, entries = rows_of(), glosses_of(), rendered()
    ids, pages, cands = texts(entries, rows, gl)
    lex = {e["headword"]: e for e in X.entries_of()}
    editors = millet_free_editors()
    st = blind_statuses(lex.values(), X.verdicts_of(), editors)
    first = {e["headword"]: X.status(e, X.verdicts_of()) for e in lex.values() if e["uses_translated"]}
    ours = {h: ("" if MILLET.search(m) else m) for h, m in X.our_meanings().items()}
    (out / "packs").mkdir(parents=True, exist_ok=True)
    (out / "answers").mkdir(exist_ok=True)
    withheld = {}
    for name, group in (("pilot", ids), ("pages", pages)):
        text, withheld[name] = translator_pack(group, rows, gl, lex, st, ours,
                                               f"data/sources/f4/answers/translator_{name}.jsonl")
        (out / "packs" / f"translator_{name}.md").write_text(text, encoding="utf-8")
    (out / "packs" / "splitter.md").write_text(splitter_pack(ids, entries, "data/sources/f4/answers/splitter.jsonl"),
                                               encoding="utf-8")
    (out / "baseline.jsonl").write_text("".join(json.dumps({"text": t, "baseline": baseline(gl[t], millet_heads(lex))},
                                                           ensure_ascii=False)
                                                + "\n" for t in ids + pages), encoding="utf-8")
    blind = {"statuses_changed": sorted(h for h in st if st[h] != first[h]),
             "proposals_left_out": sum(names_millet(p) for e in lex.values() for p in e["proposals"]),
             "withheld_in_packs": withheld}
    (out / "texts.json").write_text(json.dumps({"pilot": ids, "pages": pages, "candidates": cands, "blind": blind},
                                               ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for f in sorted((out / "packs").glob("*.md")):
        print(f.name, f.stat().st_size, "bytes")
    print("pilot:", ids, "| pages:", pages, "| statuses changed without Millet:", len(blind["statuses_changed"]),
          "| proposals naming Millet left out:", blind["proposals_left_out"], "| withheld in the packs:", withheld)


def judges(out=OUT):
    """The judges' packs and the key, once the translators and the splitter have answered. Refuses once a judge
    has answered."""
    if any((out / "answers").glob("judge*.jsonl")):
        raise SystemExit(f"{out}/answers holds a judge's answers: not writing the judges' packs again")
    rows, gl, entries = rows_of(), glosses_of(), rendered()
    chosen = json.loads((out / "texts.json").read_text(encoding="utf-8"))
    ids, pages = chosen["pilot"], chosen["pages"]
    tr, f1 = translations(out / "answers" / "translator_pilot.jsonl", ids, gl)
    tp, f2 = translations(out / "answers" / "translator_pages.jsonl", pages, gl)
    units = units_of(out / "answers" / "splitter.jsonl", ids)
    if f1 or f2 or set(units) != set(ids):
        raise SystemExit(f"answers incomplete: translator {f1 or 'ok'}, pages {f2 or 'ok'}, "
                         f"splitter's texts {sorted(units)}")
    renderings = {t: sections(entries[(t.replace(" ", ""),)])[1] for t in ids}
    decoys, shared = assign_decoys(renderings, {p: tp[p]["translation"] for p in pages})
    withheld = millet_heads({e["headword"]: e for e in X.entries_of()})
    readings = {t: {"translator": tr[t]["translation"], "baseline": baseline(gl[t], withheld),
                    "decoy": tp[decoys[t]]["translation"]} for t in ids}
    ours = {t: P.reduced_ours(rows[t]["text"].split()) for t in ids}
    key = {"pilot": ids, "pages": pages, "decoys": decoys, "decoy_shared_words": shared, "blind": chosen["blind"],
           "order": {str(j): {t: order_of(j, t) for t in ids} for j in (1, 2)},
           "units": {t: {u["unit"]: {"kind": u["kind"], "open": u["open"], "doubt": u["doubt"],
                                     "in_copy": in_copy(u["meroitic"], ours[t]),
                                     "clean": clean(u["english"], readings[t]["decoy"])} for u in units[t]} for t in ids}}
    for j in (1, 2):
        (out / "packs" / f"judge{j}.md").write_text(
            judge_pack(j, ids, entries, units, readings, f"data/sources/f4/answers/judge{j}.jsonl"), encoding="utf-8")
    (out / "key.json").write_text(json.dumps(key, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n = sum(not u["open"] for t in ids for u in units[t])
    print("units:", sum(len(units[t]) for t in ids), "| judged:", n, "| lines per judge:", 3 * n,
          "| decoys:", decoys, "| shared words:", shared)
    for j in (1, 2):
        f = out / "packs" / f"judge{j}.md"
        print(f.name, f.stat().st_size, "bytes")


def main(argv):
    if argv[1:] == ["choose"]:
        ids, pages, cands = texts()
        for c in sorted(cands, key=lambda c: (c["kind"], c["words"], c["id"])):
            print(f"  {c['id']}  {c['kind']:15} {c['words']:3} words  covered {c['covered']:.2f}"
                  + ("   <- pilot" if c["id"] in ids else ""))
        print("pilot:", ids)
        print("pages:", pages)
        return
    if argv[1:] == ["packs"]:
        return packs()
    if argv[1:] == ["judges"]:
        return judges()
    if argv[1:] in (["count"], ["public"]):
        rows, gl = rows_of(), glosses_of()
        figs = count(rows=rows, gl=gl)
        figs["tokens"], figs["sizing"] = TOKENS, sizing(figs, TOKENS, rows, gl)
        print(json.dumps(figs, ensure_ascii=False, indent=1))
        if argv[1] == "public":
            PUBLIC.write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        return
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
