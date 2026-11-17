"""The grammar-first pilot (data/discovery/grammar_pilot.md): rules of the grammar found on one part of the texts
and tested on the other.

The 548 texts are dealt by lot into a tuning set and a held-back set. Rule finders (fresh agents, one angle each)
see the tuning texts only and propose rules, each with its count written as a function (runs/grammar/). The
functions are committed, and only then are they run on the held-back texts, against bars set beforehand. Two
readers then search the sources in hand for each rule that passed: a rule is a finding of the project's own only
if both find it in none. A second round does the same on the texts that are not epitaphs.

Everything is read and written under data/sources/grammar/ (local only: the tables carry the map's glosses, the
readers' answers quote the sources), except the tests in runs/grammar/ and `public`.

  python3 -I src/grammar.py split        the texts dealt into the two sets (split.json; drawn once)
  python3 -I src/grammar.py dump         the tuning texts as tables for the finders (tuning.tsv, tuning_nf.tsv)
  python3 -I src/grammar.py briefs       what each finder of the first round is given (briefs/)
  python3 -I src/grammar.py tuning       each test on the tuning texts, against its finder's counts
  python3 -I src/grammar.py held-dump    the held-back texts' table (only once the tests are in git)
  python3 -I src/grammar.py held         each test on the held-back texts, the bars (result.json)
  python3 -I src/grammar.py packs        the rules that passed, for two readers (novelty/)
  python3 -I src/grammar.py count        the readers compared (novelty/result.json)
  python3 -I src/grammar.py briefs2 | tuning2 | held2 | packs2 | count2     the same for the second round
  python3 -I src/grammar.py parse        the long texts cut by the rules that passed (parse/, local)
  python3 -I src/grammar.py public       data/discovery/grammar_pilot_figures.json

What the finders and the readers were given is in runs/prompts/GRAMMAR_finders.md and GRAMMAR_round2.md.
"""
import collections
import csv
import importlib.util
import json
import pathlib
import random
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts"), str(ROOT / "src" / "v6")]
import recurring as W                                   # noqa: E402
import themap as M                                      # noqa: E402

HOME = ROOT / "data/sources/grammar"
PUBLIC = ROOT / "data/discovery/grammar_pilot_figures.json"
TESTS = ROOT / "runs/grammar"                            # the frozen tests, one file a finder: L<k>.py, M<k>.py
SEED = 20261116 + 12                                     # the split
SEED_READERS = 20261116 + 13                             # the order of the rules in the readers' packs
LAYERS = ("recurring", "rare_sure", "rare_later", "unnamed", "rare_millet", "leftover")   # the map when the pilot was set
HELD = 0.40                                              # the share of each stratum that is held back
LONG = 100                                               # words: a long text
BARS = {"cases": 20, "rate": 0.80, "margin": 0.30}      # on the held-back texts
OURS_NEEDED = 3                                          # the pilot's verdict: findings of ours, over both rounds
VERDICTS = ("stated", "partly", "not found")             # what a reader says of a rule
OPEN = ("hypothesis", "kind", "unknown")                 # the map's levels of a word without a meaning
COLUMNS = ["text", "kind", "words_in_text", "n", "form", "level", "parts", "gloss"]
# A round: its letter (rule ids and test files), its folders and files under HOME, the table its finders saw, the
# number of readers' packs and their letter, and the commit that froze its tests. The tests were first committed
# on a branch of their own, `grammar`, so that the branch then under review was not touched: "first" is that
# commit, which the results name; "here" is the same commit as it stands in this branch's history (the same files,
# the same author's time).
ROUNDS = {
    1: {"letter": "L", "finders": 8, "rules": "rules", "result": "result.json", "table": "tuning.tsv", "briefs": "briefs",
        "novelty": "novelty", "packs": 2, "pack": "N", "tokens": ("tokens.json", "novelty/tokens.json"),
        "frozen": {"first": "604c379", "here": "8b011a7", "at": "19:15:35"}},
    2: {"letter": "M", "finders": 6, "rules": "rules2", "result": "result2.json", "table": "tuning_nf.tsv", "briefs": "briefs2",
        "novelty": "novelty2", "packs": 1, "pack": "P", "tokens": ("tokens2.json", "novelty2/tokens.json"),
        "frozen": {"first": "6c974f3", "here": "81a043e", "at": "19:30:39"}},
}
# When each thing was done (2026-11-16, Pacific time): the commits and their times are git's; the split, the rules,
# the held-back table, the results and the answers are the local files' times; the launches are the session's
# clock, read when the agents were started (to the minute where it was not read to the second).
WHEN = {
    "split_drawn": "19:08:03",
    1: {"set_in": "b5093e6", "set": "19:09:13", "finders_started": "19:09:47", "first_rules": "19:12:45", "last_rules": "19:14:11",
        "tests_frozen": "19:15:35", "held_table_written": "19:15:45", "tested": "19:15:46", "readers_started": "19:16",
        "first_answer": "19:19:35", "last_answer": "19:20:40"},
    2: {"set_in": "bd9a68e", "set": "19:22:34", "finders_started": "19:23", "first_rules": "19:27:21", "last_rules": "19:30:03",
        "tests_frozen": "19:30:39", "tested": "19:30:39", "readers_started": "19:31", "first_answer": "19:33:15",
        "last_answer": "19:33:24"},
}

# ------------------------------------------------------------------------------------- what the agents are given

BRIEF = """# Find rules of Meroitic grammar in 329 texts

Meroitic is written in a script that can be read aloud, but most of its words are not understood. You are given
329 of its texts as a table, one word a line:

    /Users/mike/repos/mike/meroitic/data/sources/grammar/tuning.tsv

(tab-separated, with a header: text, kind, words_in_text, n, form, level, parts, gloss), and the same texts as
running text in `tuning_texts.md` beside it.

- `form` is the word as written (`S` is the sign s, `s` is se, `N` is ne, `X` is ẖ, `x` is ḫ).
- `parts` is how a word-by-word map of the corpus cuts the word: `letters=entry` for each part, where the entry
  is a headword of a dictionary (an entry with a hyphen is an ending, a prefix or a particle); `?` where the map
  names no entry; `ending`, `NAME` and `NUMBER` are the map's own marks.
- `level` is what the map knows of the word: `meaning` or `grammar` (it is translated), `name`, `number`,
  `hypothesis`, `kind` or `unknown` (it is not), `lost` (signs are lost).
- `gloss` is the map's short reading of the word, where it has one.

**Your angle: <<ANGLE>>.** Find regularities of the grammar that hold across texts. Write and run your own
Python on the table; count before you believe.

For each rule you keep, give one JSON line in the file `data/sources/grammar/rules/L<<K>>.jsonl`, nothing else in it:

    {"id": "L<<K>>-1", "statement": "<one or two plain sentences>", "cases": "<exactly which places of the table are a case, in terms of its columns>", "holds": "<exactly what must be true at a case for the rule to hold>", "comparison": "<what is counted, in terms of the columns, to say how often that would be true if the rule were not there>", "tuning": {"cases": 57, "holds": 52, "comparison_rate": 0.31}, "why_grammar": "<at most 25 words: what the rule says about the language>", "known": "<what you know of published grammar on this point, or 'nothing'>"}

- **At most 8 rules, your best.** A later test on other texts needs at least 20 cases there, the rule holding in
  80% of them, 30 points above its comparison: prefer rules with many cases, a high rate and a wide margin.
- **A rule ties things together:** a word to its neighbours or to its place in the text, or a part of a word to
  another part or to the letters beside it. A statement that only repeats how the map cuts or labels one word is
  not a rule (the cuts follow a dictionary). A statement about what one word means is not a rule.
- **"cases", "holds" and "comparison" must be exact enough** for someone else to write the script from them,
  using the table's columns alone.
- Use only those two files. Other texts are held back for the test: do not open any other file of the
  repository, do not search the web, do not spawn agents, and write no file but your answers file. Run your
  Python from standard input (`python3 - <<'EOF'`), not from a file.

When the file is written, reply in at most ten lines: how many rules, and for each its id, a few words on what
it says, and its counts.
"""

ANGLES = {
    1: 'the noun phrase: the order of noun, adjective, determiner and genitive, and what closes a phrase',
    2: 'the verb: which prefixes and endings go together on a verb, and with what around the verb (the number of persons named, the endings of the words before it)',
    3: 'the clause: where a clause begins and ends, and the order of its members (who, to whom, what, the verb)',
    4: 'the endings of place, source and direction (such as -te, -k, -ke, -w, -yte): what they attach to and in which frames they stand',
    5: 'counting: numerals, what is counted, the order of the counted word and its number, and lists',
    6: 'the epitaph: the order and the form of the clauses of filiation and relation and of the titles in them, and how they change with one or several persons',
    7: 'the long texts (those with 100 words or more, and the royal or temple texts): frames that repeat from sentence to sentence, and the words or endings that link or close sentences',
    8: 'writing: how a stem and an ending change where they meet (which letters are dropped, doubled or changed, and after which letters)',
}

BRIEF2 = """# Find rules of Meroitic grammar in 168 texts that are not epitaphs

Meroitic is written in a script that can be read aloud, but most of its words are not understood. You are given
168 of its texts as a table, one word a line:

    /Users/mike/repos/mike/meroitic/data/sources/grammar/tuning_nf.tsv

(tab-separated, with a header: text, kind, words_in_text, n, form, level, parts, gloss). They are royal and temple
texts, documents (ostraca, papyri, vessels), graffiti, oracular decrees, and texts whose kind is not known: 2,210
words. No epitaph is among them.

- `form` is the word as written (`S` is the sign s, `s` is se, `N` is ne, `X` is ẖ, `x` is ḫ).
- `parts` is how a word-by-word map of the corpus cuts the word: `letters=entry` for each part, where the entry
  is a headword of a dictionary (an entry with a hyphen is an ending, a prefix or a particle); `?` where the map
  names no entry; `ending`, `NAME` and `NUMBER` are the map's own marks.
- `level` is what the map knows of the word: `meaning` or `grammar` (it is translated), `name`, `number`,
  `hypothesis`, `kind` or `unknown` (it is not), `lost` (signs are lost).
- `gloss` is the map's short reading of the word, where it has one.

**Your angle: <<ANGLE>>.** Find regularities of the grammar that hold across texts. Write and run your own Python on
the table; count before you believe.

**Not wanted:** the grammar of the epitaph (the invocation of Isis and Osiris, the naming in -qowi, the clauses of
filiation, the offering formulas with ato and at). It is known, and a first round has already tested it. If a
rule's cases are mostly such formulas quoted in these texts, drop it.

**1. The rules.** For each rule you keep, give one JSON line in the file `data/sources/grammar/rules2/M<<K>>.jsonl`
(the path is relative to /Users/mike/repos/mike/meroitic/), nothing else in it:

    {"id": "M<<K>>-1", "statement": "<one or two plain sentences>", "cases": "<exactly which places of the table are a case, in terms of its columns>", "holds": "<exactly what must be true at a case for the rule to hold>", "comparison": "<what is counted, in terms of the columns, to say how often that would be true if the rule were not there>", "tuning": {"cases": 57, "holds": 52, "comparison_rate": 0.31}, "why_grammar": "<at most 25 words: what the rule says about the language>", "known": "<what you know of published grammar on this point, or 'nothing'>"}

- **At most 6 rules, your best.** A later test on other texts of the same kinds (about 1,800 words) needs at least
  20 cases there, the rule holding in 80% of them, 30 points above its comparison: prefer rules with many cases, a
  high rate and a wide margin. A rule with fewer than about 30 cases here will not reach 20 there.
- **A rule ties things together:** a word to its neighbours or to its place in the text, or a part of a word to
  another part or to the letters beside it. A statement that only repeats how the map cuts or labels one word is
  not a rule (the cuts follow a dictionary). A statement about what one word means is not a rule.
- **"cases", "holds" and "comparison" must be exact enough** for someone else to write the script from them,
  using the table's columns alone.

**2. The tests.** Then write each rule's count as a Python function in the file
`/Users/mike/repos/mike/meroitic/runs/grammar/M<<K>>.py`: `def test_M<<K>>_1(rows):` and so on, one a rule.

- `rows` is a table as a list of dicts in the table's order, one word each, with the keys text, kind,
  words_in_text (an int), n (an int), form, level, parts (the string exactly as the table writes it), gloss. It may
  be these 168 texts or any other set of texts with the same columns.
- Each function returns a tuple `(cases, holds, comparison_rate)`, counted on `rows` alone exactly as the rule's
  "cases", "holds" and "comparison" say; the comparison rate is a number between 0 and 1.
- Pure functions: no file is read or written inside them, only the standard library is imported, and nothing
  depends on these 168 texts (no list of text names, no count taken from them). Where a comparison shuffles, use
  `random.Random(20261128)`.
- Check that each function, run on the table (csv.DictReader with delimiter tab and quoting=csv.QUOTE_NONE, n and
  words_in_text turned into ints), gives the rule's "tuning" counts.

Use only that one table. Other texts are held back for the test: do not open any other file of the repository,
do not search the web, do not spawn agents, and write no file but your two files. Run your Python from standard
input (`python3 - <<'EOF'`), not from a file.

When both files are written, reply in at most ten lines: how many rules, and for each its id, a few words on what
it says, and the three numbers its function gives on the table.
"""

ANGLES2 = {
    1: 'the royal and temple texts: the order of words, and what opens and what closes a sentence',
    2: 'the documents (ostraca, papyri, vessels): numbers, what is counted, items and lists',
    3: 'the graffiti and the oracular decrees: the frames they share, and what varies inside them',
    4: 'the endings within a word: which ending follows which, which stand last, and what kind of word they attach to',
    5: 'names and titles: what stands before and after a name or a title, and which endings they carry',
    6: 'frames that repeat: pairs or runs of words that come back in the same order within a text or across texts, and what varies inside them',
}

READERS_BRIEF = """# Does a source state this rule of Meroitic grammar? <<N>> rules

Each rule below is a regularity that was counted in Meroitic texts. Your task is to find out, for each rule,
whether one of the sources listed here states it.

The sources, all under /Users/mike/repos/mike/meroitic/ :

- `data/rilly2003/*.jsonl`: Rilly's lexicon of 2003, one JSON line an entry (words, endings, prefixes, particles);
- `data/sources/rilly2016-text/` and `data/sources/dotawo-text/` (Rilly 2016 and Rilly 2021);
- `data/sources/fhn-text/`, `data/sources/fhn2-text/`, `data/sources/fhn4-text/` (Fontes Historiae Nubiorum);
- `data/sources/jssea-text/` (Millet 2005) and `data/sources/lipinski2011-text/` (Lipinski 2011);
- `data/sources/karanog-text/`, `data/sources/meroe1911-text/`, `data/sources/griffith-jea-text/`,
  `data/sources/griffith-mi1-text/`, `data/sources/griffith-mi2-text/`, `data/sources/laaa7-text/` (Griffith);
- `data/sources/survey-text/` and `data/sources/champollion1922-text/`.

For each rule give one JSON line, in the order of this file, in the file `<<ANSWERS>>`, nothing else in it:

    {"id": "L3-2", "verdict": "stated", "source": "<the work>", "file": "<the file you quote from>", "quote": "<the words that state it, copied exactly, at most forty words; empty for 'not found'>", "note": "<at most thirty words; for 'not found': what you searched for>"}

- "stated": a source says this regularity, in its own words: the same fact, even where it stands inside the
  description of a formula or in the entry of an ending.
- "partly": a source states a part of it, or a wider or a narrower fact that covers some of it.
- "not found": you searched and found no statement of it.
- Search before you answer: grep the files for the Meroitic forms the rule names (the lexicon writes ḫ for `x`,
  ẖ for `X`, s for `S`, se for `s`, ne for `N`) and for the English or French words a statement would use, and
  read around what you find.
- A quote is needed for "stated" and for "partly". What you know of Meroitic from elsewhere does not count.
- Use only these files. Do not search the web, do not open other files of the repository, do not spawn agents,
  and write no file but your answers file.

This file lists <<N>> rules: your file must have <<N>> lines, one for each rule. When it is written, count its lines
against that number, then reply in one line: how many rules, and how many of each verdict.
"""

# A rule's statement in the figures where the finder's wording shares four words in a row with the lexicon of 2003
# or with Rilly 2016 and 2021 (the rule of src/lexicon.py, COPIED; mostly a run of small words such as "at the end
# of"): the same statement reworded. tests/test_grammar.py checks every statement of the figures; the finders'
# own wording stays in the local rule files and in the readers' packs.
STATEMENTS = {
    "L1-5": "A filiation word (terike-, tedxe- 'begotten by', 'born of') comes directly after the parent's noun phrase, which is a name or "
            "else ends in -li or -ye.",
    "L1-6": "The relation word yetmde- ('relative of') comes directly after the noun phrase it governs, closed by a determiner -l/-leb "
            "(or -li, -ye) or being a name.",
    "L2-6": "The first offering formula ('ato mXe' + verb) has before it a word ending in -i, mostly the filiation predicate in "
            "-lowi/-qowi or the vocative Soreyi.",
    "L2-7": "When several persons are named (the last filiation word before the verb ends in -bkwi), the benediction verb carries the "
            "plural marker -bx(e)- (-bḫe-) before its ending.",
    "L3-1": "The vocative invocation woSi (or wiSi) opens the text as its first word.",
    "L3-2": "The second vocative, Soreyi (Osiris), comes right after the invocation of Isis: among the three words before it stands "
            "woS/woSi/wiS/wiSi.",
    "L3-8": "Benediction verbs (ending in -kete, -kte, -kes, -ketes) stand in their text's latter half.",
    "L4-2": "Words with the verbal ending -kete stand in their text's final third: the benediction formulas close the inscription.",
    "L4-5": "A word beginning with the causative prefix ps- (pS, piS) carries a verbal ending -te, -ke, -kes or -to, on itself or on the "
            "next word when the verb is written in two pieces.",
    "L5-1": "Words standing directly beside a numeral carry no suffix: both the counted word in front and the following word are bare "
            "stems, without article, case or predicate endings.",
    "L5-3": "Each item of the offering list, 'ato' or 'at', has after it a word beginning with m (mostly mXe).",
    "L5-4": "The quantity word mXe/mxe in a list item has after it a verb beginning with p (the causative/verbal prefix p-, mostly pS- "
            "or piS-).",
    "L5-6": "A list item 'at' starts right where the previous item ends: the preceding word is a verb beginning with p or ending in -te "
            "or -s.",
    "L6-1": "The word that names the dead person (ending in -qo or -qowi) comes before every filiation and relation clause of the "
            "epitaph.",
    "L6-2": "The word just before a filiation predicate (tedxe-lowi 'born of', terike-lowi 'begotten by') names a person: the parent's "
            "name stands immediately before the verb of filiation.",
    "L7-1": "The word after mXe in the offering formula is a prefixed verb: it begins with p, b or y.",
    "L8-2": "Where a glide joins two vowels and the later vowel is e or o, that glide is y, not w (w appears mainly in o-w-i).",
    "M1-1": "After a word ending in -se comes a short word of at most three letters, mostly a determiner written apart (l, li, lw or "
            "lke) or the copula wi; the -se phrase is closed right after it.",
    "M1-2": "A word that ends in the letter b has e just before it (-leb, -teb, -seb): the -b that marks the plural follows the vowel e, "
            "not another letter.",
    "M2-1": "The sign a stands word-initially only; word-internally and word-finally this sign never writes a vowel.",
    "M2-2": "Two vowel signs never stand side by side: inside a word, e, i or o always has a consonant sign after it.",
    "M2-5": "Inside a word the sign N (ne) has a consonant sign after it, never a vowel sign.",
    "M4-1": "Word-final copula -wi comes after the vowel o or e: words end in -owi (-lowi, -towi, -qowi) or -ewi, rarely in a consonant "
            "plus -wi.",
    "M4-3": "After a word ending in -se comes a short word of at most three letters, mostly a free-standing ending or particle such as "
            "l, li, lw, wi or lke.",
    "M6-3": "A word written more than once in a text tends to come back inside the same frame: at least one of its neighbours (the word "
            "before or the word after) recurs at another of its occurrences.",
}


def brief_of(rnd, k):
    """The brief of finder k of a round: the round's brief with the finder's angle and files."""
    return (BRIEF if rnd == 1 else BRIEF2).replace("<<ANGLE>>", (ANGLES if rnd == 1 else ANGLES2)[k]).replace("<<K>>", str(k))


def briefs(rnd=1):
    folder = HOME / ROUNDS[rnd]["briefs"]
    folder.mkdir(parents=True, exist_ok=True)
    for k in (ANGLES if rnd == 1 else ANGLES2):
        (folder / f"{ROUNDS[rnd]['letter']}{k}.md").write_text(brief_of(rnd, k), encoding="utf-8")
    print(len(ANGLES if rnd == 1 else ANGLES2), "briefs in", folder.relative_to(HOME))


# --------------------------------------------------------------------------------------- the split and the tables

def the_map():
    """The map with the layers it had when the pilot was set."""
    names = tuple(l["name"] for l in M.LAYERS)
    if names[:len(LAYERS)] != LAYERS:
        raise SystemExit(f"the layers are no longer {LAYERS}")
    return M.current(upto=len(LAYERS))


def split_of(gl, rows, seed=SEED):
    """Every text by lot into tuning or held-back: HELD of each stratum (kind of text, long or short) is held back."""
    strata = collections.defaultdict(list)
    for t in sorted(gl):
        strata[(rows[t].get("kind") or "not known", len(gl[t]) >= LONG)].append(t)
    rnd = random.Random(seed)
    held = []
    for key in sorted(strata):
        ts = strata[key]
        rnd.shuffle(ts)
        held += ts[:round(HELD * len(ts))]
    held = sorted(held)
    return {"seed": seed, "held": held, "tuning": sorted(t for t in gl if t not in set(held))}


def split():
    if (HOME / "split.json").exists():
        raise SystemExit("the split is drawn: not drawn again")
    gl = the_map()
    out = split_of(gl, W.corpus_rows())
    HOME.mkdir(parents=True, exist_ok=True)
    (HOME / "split.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print({k: (len(out[k]), sum(len(gl[t]) for t in out[k])) for k in ("tuning", "held")})


def the_split():
    return json.loads((HOME / "split.json").read_text(encoding="utf-8"))


def lines_of(texts, gl, rows):
    """One line a word, in the texts' order: the columns of the table."""
    for t in texts:
        for n, g in enumerate(gl[t], 1):
            parts = " ".join(f"{p.get('form') or ''}={p.get('entry') or '?'}" for p in g.get("parts") or [])
            gloss = " ".join((g.get("gloss") or "").split())[:70]
            yield [t, rows[t].get("kind") or "not known", str(len(gl[t])), str(n), g["form"], g["level"], parts, gloss]


def table(lines):
    return "\n".join("\t".join(r) for r in [COLUMNS] + list(lines)) + "\n"


def dump():
    """The tuning texts for the finders: a table of all of them, the same as running text, and the table of those
    that are not funerary (the second round). Nothing of the held-back texts is written here."""
    gl, rows, sp = the_map(), W.corpus_rows(), the_split()
    lines = list(lines_of(sp["tuning"], gl, rows))
    (HOME / "tuning.tsv").write_text(table(lines), encoding="utf-8")
    (HOME / "tuning_nf.tsv").write_text(table(r for r in lines if r[1] != "funerary"), encoding="utf-8")
    text = []
    for t in sp["tuning"]:
        text.append(f"## {t} ({rows[t].get('kind') or 'kind not known'}, {len(gl[t])} words)\n")
        text.append(" ".join(g["form"] for g in gl[t]) + "\n")
    (HOME / "tuning_texts.md").write_text("\n".join(text), encoding="utf-8")
    print("tuning:", len(sp["tuning"]), "texts;", len(lines), "words;", sum(r[1] != "funerary" for r in lines), "of them not funerary")


def rows_of(path):
    """A table as a list of words, in its order: the columns as strings (parts as the table writes them), with n
    and words_in_text as numbers. This is what a test function is given."""
    with open(path, encoding="utf-8", newline="") as f:
        return [r | {"n": int(r["n"]), "words_in_text": int(r["words_in_text"])}
                for r in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)]


# ---------------------------------------------------------------------------------------- the rules and their tests

def rules(rnd=1):
    """{rule id: the finder's line}, in the order of the finders' files."""
    out = {}
    for f in sorted((HOME / ROUNDS[rnd]["rules"]).glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                out[r["id"]] = r
    return out


def tests(rnd=1, folder=None):
    """{rule id: its test function}, from the round's files in runs/grammar/: test_L3_2 tests the rule L3-2."""
    letter, out = ROUNDS[rnd]["letter"], {}
    for f in sorted((folder or TESTS).glob(f"{letter}*.py")):
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for name in dir(mod):
            if name.startswith(f"test_{letter}"):
                out[name[5:].replace("_", "-", 1)] = getattr(mod, name)
    return out


def measure(fn, rows):
    cases, holds, comparison_rate = fn(rows)
    return {"cases": cases, "holds": holds, "rate": round(holds / cases, 4) if cases else None,
            "comparison_rate": None if comparison_rate is None else round(comparison_rate, 4)}


def verdict_of(m):
    """A rule's verdict on the held-back texts by the bars: at least 20 cases, holding in at least 80% of them, at
    least 30 points above its comparison rate there."""
    short = m["cases"] < BARS["cases"]
    low = m["cases"] > 0 and m["rate"] < BARS["rate"]
    near = m["cases"] > 0 and (m["comparison_rate"] is None or m["rate"] - m["comparison_rate"] < BARS["margin"])
    why = [w for w, bad in (("fewer than 20 cases", short), ("holds in under 80%", low), ("under 30 points above its comparison", near)) if bad]
    return "passed" if not why else "not passed: " + "; ".join(why)


def same_as_finder(m, t):
    return (m["cases"], m["holds"]) == (t["cases"], t["holds"]) and abs((m["comparison_rate"] or 0) - (t.get("comparison_rate") or 0)) < 0.005


def tuning(rnd=1):
    """Each test on the table its finder saw: it must give the finder's own counts."""
    rows, rs, ts = rows_of(HOME / ROUNDS[rnd]["table"]), rules(rnd), tests(rnd)
    same = 0
    for rid, r in rs.items():
        if rid not in ts:
            print(rid, "NO TEST")
            continue
        m = measure(ts[rid], rows)
        same += same_as_finder(m, r["tuning"])
        print(rid, "same as the finder's counts" if same_as_finder(m, r["tuning"]) else f"DIFFERS: test {m}, finder {r['tuning']}")
    return same


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def frozen(rnd=1):
    """Every test file of the round must be, byte for byte, the file of the commit that froze it, before the
    held-back texts are written or read. Gives the commit as the results name it, with its time."""
    fz, files = ROUNDS[rnd]["frozen"], sorted(TESTS.glob(f"{ROUNDS[rnd]['letter']}*.py"))
    if not files:
        raise SystemExit("no test file")
    for f in files:
        rel = str(f.relative_to(ROOT))
        if git("hash-object", rel) != git("rev-parse", f"{fz['here']}:{rel}"):
            raise SystemExit(f"{rel} is not the file committed in {fz['here']}")
    return f"{fz['first']} {fz['at']}"


def held_dump():
    print("tests frozen in", frozen(1))
    gl, rows, sp = the_map(), W.corpus_rows(), the_split()
    (HOME / ".held").mkdir(exist_ok=True)
    (HOME / ".held/held.tsv").write_text(table(lines_of(sp["held"], gl, rows)), encoding="utf-8")
    print("held back:", len(sp["held"]), "texts")


def held_rows(rnd=1):
    """The held-back words a round's tests are run on: all of them, or (second round) those not in a funerary text."""
    rows = rows_of(HOME / ".held/held.tsv")
    return rows if rnd == 1 else [r for r in rows if r["kind"] != "funerary"]


def result_of(rs, ts, rows):
    """{rule id: its counts on `rows`, its finder's tuning counts and its verdict}; a rule without a test is dropped."""
    out = {}
    for rid, r in rs.items():
        if rid not in ts:
            out[rid] = {"verdict": "dropped: no test could be written from its wording"}
            continue
        m = measure(ts[rid], rows)
        out[rid] = m | {"tuning": r["tuning"], "verdict": verdict_of(m)}
    return out


def held(rnd=1):
    """The frozen tests on the held-back texts. The second round's result also says how many words its tests saw."""
    commit, rows = frozen(rnd), held_rows(rnd)
    out = result_of(rules(rnd), tests(rnd), rows)
    res = {"tests_frozen_in": commit, "bars": BARS} | ({"words": len(rows)} if rnd == 2 else {}) | {"rules": out}
    (HOME / ROUNDS[rnd]["result"]).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for rid, v in out.items():
        print(rid, v["verdict"], {k: v.get(k) for k in ("cases", "holds", "rate", "comparison_rate")})
    print(sum(v["verdict"] == "passed" for v in out.values()), "of", len(out), "rules passed")


def the_result(rnd=1):
    return json.loads((HOME / ROUNDS[rnd]["result"]).read_text(encoding="utf-8"))


# ------------------------------------------------------------------------------------------------- the readers

def passed(rnd=1):
    res, rs = the_result(rnd)["rules"], rules(rnd)
    return [(rid, rs[rid], v) for rid, v in res.items() if v["verdict"] == "passed"]


def packs(rnd=1):
    R = ROUNDS[rnd]
    folder, n_packs, letter = HOME / R["novelty"], R["packs"], R["pack"]
    if any(folder.glob("answers*/*.jsonl")):
        raise SystemExit("answers exist: the packs are not written again")
    ps = passed(rnd)
    random.Random(SEED_READERS + rnd - 1).shuffle(ps)
    groups = [ps[i::n_packs] for i in range(n_packs)]
    (folder / "packs").mkdir(parents=True, exist_ok=True)
    for n, g in enumerate(groups, 1):
        body = "\n".join(
            f"## Rule `{rid}`\n\n{r['statement']}\n\n- A case: {r['cases']}\n- It holds when: {r['holds']}\n"
            f"- Counted on texts it was not found in: {v['holds']} of {v['cases']} cases.\n" for rid, r, v in g)
        for c in (1, 2):
            (folder / f"answers{c}").mkdir(exist_ok=True)
            head = READERS_BRIEF.replace("<<N>>", str(len(g))).replace("<<ANSWERS>>", f"data/sources/grammar/{R['novelty']}/answers{c}/{letter}{n}.jsonl")
            (folder / f"packs/{letter}{n}_r{c}.md").write_text(head + "\n---\n\n" + body, encoding="utf-8")
    (folder / "groups.json").write_text(json.dumps([[rid for rid, _, _ in g] for g in groups], indent=1) + "\n", encoding="utf-8")
    print(len(ps), "rules in", n_packs, "packs:", [len(g) for g in groups])


def answers(rnd=1):
    """(the packs' rules, {(reader, rule id): the reader's line}): a reader's file counts only for the rules of its
    own pack, the first line a rule, and only with one of the three verdicts."""
    R = ROUNDS[rnd]
    groups = json.loads((HOME / R["novelty"] / "groups.json").read_text(encoding="utf-8"))
    ans = {}
    for c in (1, 2):
        for n, g in enumerate(groups, 1):
            f = HOME / R["novelty"] / f"answers{c}/{R['pack']}{n}.jsonl"
            for line in f.read_text(encoding="utf-8").splitlines() if f.exists() else []:
                try:
                    a = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(a, dict) and a.get("id") in g and a.get("verdict") in VERDICTS:
                    ans.setdefault((c, a["id"]), a)
    return groups, ans


def ours(a, b):
    """A rule is a finding of the project's own only when both readers answered and both found it in no source."""
    return bool(a and b and a["verdict"] == b["verdict"] == "not found")


def count(rnd=1):
    groups, ans = answers(rnd)
    out = {}
    for g in groups:
        for rid in g:
            a, b = ans.get((1, rid)), ans.get((2, rid))
            out[rid] = {"one": a and a["verdict"], "two": b and b["verdict"], "ours": ours(a, b),
                        "sources": sorted({x["source"] for x in (a, b) if x and x.get("source") and x["verdict"] != "not found"})}
    (HOME / ROUNDS[rnd]["novelty"] / "result.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(dict(collections.Counter((v["one"], v["two"]) for v in out.values())))
    print("answered by both:", sum(bool(v["one"] and v["two"]) for v in out.values()), "of", len(out), "| ours:", sorted(k for k, v in out.items() if v["ours"]))


def the_readers(rnd=1):
    return json.loads((HOME / ROUNDS[rnd]["novelty"] / "result.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------------------------------- the figures

# The work a reader names, by a word of its name: the figures give the work, not the reader's wording of it.
WORKS = (("Karanog", "Griffith 1911 (Karanog)"), ("Meroitic Studies", "Griffith, Meroitic Studies"), ("Dotawo", "Rilly 2021"),
         ("2021", "Rilly 2021"), ("2016", "Rilly 2016"), ("2003", "Rilly 2003"), ("FHN", "Fontes Historiae Nubiorum"),
         ("Millet", "Millet 2005"), ("Lipinski", "Lipinski 2011"), ("Griffith", "Griffith"))
PAIRS = {("stated", "stated"): "stated by both", ("partly", "stated"): "stated by one, partly by the other",
         ("partly", "partly"): "partly stated by both", ("not found", "not found"): "not found by both"}


def work(source):
    for word, name in WORKS:
        if word in source:
            return name
    raise SystemExit(f"a source the figures do not know: {source!r}")


def readers_of(v):
    """How the two readers stand on a rule, in the page's four cases."""
    return PAIRS.get(tuple(sorted((v["one"] or "no answer", v["two"] or "no answer"))), "another pair")


def why_not(verdict):
    """The first bar a rule missed, in the bars' order."""
    return verdict.removeprefix("not passed: ").split("; ")[0]


def set_of(rows):
    by_kind, texts = collections.defaultdict(lambda: [set(), 0]), collections.Counter(r["text"] for r in rows)
    for r in rows:
        by_kind[r["kind"]][0].add(r["text"])
        by_kind[r["kind"]][1] += 1
    nf = [r for r in rows if r["kind"] != "funerary"]
    return {"texts": len(texts), "words": len(rows), "long_texts": sum(n >= LONG for n in texts.values()),
            "not_funerary": {"texts": len({r["text"] for r in nf}), "words": len(nf)},
            "by_kind": {k: {"texts": len(v[0]), "words": v[1]} for k, v in sorted(by_kind.items())}}


def round_figures(rnd, tuning_rows, held_all):
    R, rs, res, rd, ts = ROUNDS[rnd], rules(rnd), the_result(rnd), the_readers(rnd), tests(rnd)
    seen = tuning_rows if rnd == 1 else [r for r in tuning_rows if r["kind"] != "funerary"]
    rows = []
    for rid, r in rs.items():
        v, n = res["rules"][rid], rd.get(rid)
        rows.append({"id": rid, "finder": rid.split("-")[0], "statement": STATEMENTS.get(rid, r["statement"]), "tuning": r["tuning"],
                     "held": {k: v.get(k) for k in ("cases", "holds", "rate", "comparison_rate")}, "verdict": v["verdict"],
                     "readers": n and [n["one"], n["two"]], "works": n and sorted({work(s) for s in n["sources"]}),
                     "ours": bool(n and n["ours"])})
    ok = [x for x in rows if x["verdict"] == "passed"]
    return {"finders": R["finders"], "rules": len(rows), "by_finder": dict(collections.Counter(x["finder"] for x in rows)),
            "tests_with_the_finders_counts": sum(same_as_finder(measure(ts[rid], seen), r["tuning"]) for rid, r in rs.items() if rid in ts),
            "tests_frozen_in": res["tests_frozen_in"], "tests_frozen_in_this_history": R["frozen"]["here"],
            "held_words": len(held_all if rnd == 1 else [r for r in held_all if r["kind"] != "funerary"]),
            "passed": len(ok), "not_passed": dict(collections.Counter(why_not(x["verdict"]) for x in rows if x["verdict"] != "passed")),
            "not_passed_also_under_the_margin": sum("holds in under 80%; under 30 points" in x["verdict"] for x in rows),
            "readers": {"rules": len(rd), "answered_by_both": sum(bool(v["one"] and v["two"]) for v in rd.values()),
                        **{name: sum(readers_of(v) == name for v in rd.values()) for name in PAIRS.values()}},
            "ours": sorted(x["id"] for x in rows if x["ours"]),
            "works": dict(collections.Counter(w for x in ok for w in x["works"]).most_common()),
            "the_rules": rows}


def long_texts(tuning_rows, held_all, fns):
    """A round's rules that passed, applied to each long text: how many have a case there, and how the cases come
    out. It counts the rules' reach; it does not cut a text into clauses or give a word a kind or a role."""
    by = collections.defaultdict(list)
    for r in tuning_rows + held_all:
        by[r["text"]].append(r)
    held = {r["text"] for r in held_all}
    out = []
    for t, rs in sorted(by.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        if len(rs) < LONG:
            continue
        got = [fn(rs) for fn in fns]
        out.append({"text": t, "kind": rs[0]["kind"], "set": "held back" if t in held else "tuning", "words": len(rs),
                    "open_words": sum(r["level"] in OPEN for r in rs), "rules_with_a_case": sum(c > 0 for c, _, _ in got),
                    "cases": sum(c for c, _, _ in got), "holds": sum(h for _, h, _ in got)})
    return out


def cases_by_kind(rows, fns):
    """Where the cases of the first round's passed rules stand, by kind of text (each kind's texts counted alone)."""
    out = {}
    for k in sorted({r["kind"] for r in rows}):
        rs = [r for r in rows if r["kind"] == k]
        out[k] = sum(fn(rs)[0] for fn in fns)
    total = sum(out.values())
    return {"cases": dict(sorted(out.items(), key=lambda kv: -kv[1])), "all": total,
            "share": {k: round(v / total, 4) for k, v in sorted(out.items(), key=lambda kv: -kv[1])}}


# ------------------------------------------------------------------------------- the long texts, cut by the rules
#
# Section 6 of the page set this part before any finder ran: each long text cut into clauses and phrases by the
# rules that passed, and for each word without a meaning what the rules make of it. It is a description, with no
# bar. Nothing here is taken from outside the rules: a mark of an end stands only where a rule that passed puts
# one, and a rule about the epitaph's fixed words marks only where those words stand.

VERB_ENDS = ("te", "ke", "kes", "to")                    # the endings of a ps- verb, by rule L4-5
MXE = ("mXe", "mxe", "mX", "mXo")                        # the word after the noun of an offering, by rule L1-3
WHOLE_PARTS = re.compile(r"(\S+?)=(.+?)(?= \S+?=|$)")     # a word's parts with their whole entry, as rule L4-1 reads them
COPULA = re.compile(r"^[lqt]?o(w|wi)?$|^lw$")            # the copula's letters, by rule M5-2


def readable(r):
    return r["level"] != "lost" and "." not in r["form"]


def at(rs, i):
    return rs[i] if 0 <= i < len(rs) else None


def end_address(rs, i, passed):
    n = at(rs, i + 1)
    if rs[i]["form"] in ("woSi", "wiSi") and n and readable(n) and n["form"].startswith(("Sor", "aSor")) and n["form"].endswith("i"):
        return i + 1


def end_naming(rs, i, passed):
    return i if rs[i]["form"].endswith("qowi") else None


def end_wi(rs, i, passed):
    f = rs[i]["form"]
    return i if len(f) >= 4 and "." not in f and f.endswith("owi") else None


def end_before_water(rs, i, passed):
    n = at(rs, i + 1)
    return i - 1 if rs[i]["form"] == "ato" and i > 0 and n and n["form"].lower() == "mxe" else None


def end_before_bread(rs, i, passed):
    return i - 1 if rs[i]["form"] == "at" and i > 0 and rs[i - 1]["level"] != "lost" else None


def end_verb(rs, i, passed):
    v = at(rs, i + 1)
    if rs[i]["form"] in MXE and v and readable(v) and v["form"][:1] in ("p", "b", "y"):
        two = at(rs, i + 2)
        in_two = "L4-5" in passed and re.match(r"^p(i)?S", v["form"]) and not v["form"].endswith(VERB_ENDS) and two \
            and two["form"].endswith(VERB_ENDS)
        return i + 2 if in_two else i + 1


# The marks of an end: the rules that give each (one of them that passed is enough), the rules that say the same
# or shape it, where it can stand, and whether the rule's own count is about that place ("its count") or only its
# wording names the end ("its wording": the count was of something else, as the page says).
MARKS = [
    {"id": "address", "gives": ("L1-4",), "with": ("L3-2", "L7-4"), "where": "at the epitaph's fixed words", "from": "its count",
     "what": "after woSi or wiSi, the word for Osiris in -i closes the address to the two gods", "at": end_address},
    {"id": "naming", "gives": ("L7-4", "L3-3"), "with": ("L6-1",), "where": "at any word", "from": "its wording",
     "what": "a word in -qowi closes the naming of the dead", "at": end_naming},
    {"id": "wi", "gives": ("L7-5",), "with": ("L8-4", "M3-1", "M6-1"), "where": "at any word", "from": "its wording",
     "what": "a word in -owi carries the ending -wi, which the rule calls the last of a sentence", "at": end_wi},
    {"id": "before water", "gives": ("L7-3", "L2-6"), "with": (), "where": "at the epitaph's fixed words", "from": "its count",
     "what": "the word before `ato mXe` closes a sentence", "at": end_before_water},
    {"id": "before bread", "gives": ("L5-6",), "with": (), "where": "at the epitaph's fixed words", "from": "its count",
     "what": "the word before `at` closes the item of the offering list that comes before it", "at": end_before_bread},
    {"id": "verb", "gives": ("L3-7", "L1-3"), "with": ("L7-1", "L5-4", "L4-5"), "where": "at the epitaph's fixed words", "from": "its count",
     "what": "the verb right after mXe closes the phrase of noun, mXe and verb; a ps- verb in two pieces closes with the second",
     "at": end_verb},
]


def given(table, passed):
    """The marks (or the statements) of a table that a rule that passed gives."""
    return [m for m in table if set(m["gives"]) & set(passed)]


def cuts(rs, passed):
    """{index of a word: the marks of an end it carries}, for one text's words in their order."""
    out = collections.defaultdict(list)
    for m in given(MARKS, passed):
        for i in range(len(rs)):
            j = m["at"](rs, i, passed)
            if j is not None and m["id"] not in out[j]:
                out[j].append(m["id"])
    return {j: v for j, v in sorted(out.items()) if v}


def is_parent(rs, i, ends):
    n = at(rs, i + 1)
    return bool(n and readable(rs[i]) and n["form"].startswith(("terik", "tedx")))


def is_governed(rs, i, ends):
    n = at(rs, i + 1)
    return bool(n and readable(rs[i]) and n["form"].startswith("yetmde"))


def is_ps_verb(rs, i, ends):
    f, n = rs[i]["form"], at(rs, i + 1)
    return bool(re.match(r"^p(i)?S", f) and readable(rs[i]) and (f.endswith(VERB_ENDS) or (n and n["form"].endswith(VERB_ENDS))))


def is_offering_verb(rs, i, ends):
    p = at(rs, i - 1)
    return bool(p and p["form"] in MXE and readable(rs[i]) and rs[i]["form"][:1] in ("p", "b", "y"))


def is_kete_verb(rs, i, ends):
    if not any(e == "-kete" for _, e in WHOLE_PARTS.findall(rs[i]["parts"] or "")):
        return False
    before = [at(rs, i - 1), at(rs, i - 2)]
    return any(b and ("mX" in b["form"] or "mx" in b["form"] or "mlo" in b["form"] or b["form"].startswith("at")) for b in before)


def is_copula(rs, i, ends):
    f = rs[i]["form"]
    return len(f) >= 4 and "." not in f and f.endswith("owi") and f[-4] in "lqt"


def is_common_copula(rs, i, ends):
    if rs[i]["level"] == "lost":
        return False
    ps = [tok.split("=", 1) for tok in rs[i]["parts"].split(" ") if "=" in tok]
    for (l1, e1), (l2, e2) in zip(ps, ps[1:]):
        stem = e1 not in ("?", "ending", "NUMBER", "") and not e1.startswith("-") and not e1.endswith("-")
        if stem and (e2 == "ending" or e2.startswith("-")) and l1 and l2 and not (e1 == "NAME" or e1[:1].isupper()) \
                and COPULA.match(l2) and (l2.startswith("l") or l1.endswith("l")):
            return True
    return False


def is_place(rs, i, ends):
    ps = WHOLE_PARTS.findall(rs[i]["parts"] or "")
    return any(e == "-te (2)" and n[0][:1] == "l" for (_, e), n in zip(ps, ps[1:]))


def is_plural(rs, i, ends):
    f = rs[i]["form"]
    return len(f) >= 3 and "." not in f and not f.isdigit() and f.endswith("eb")


def is_closing(rs, i, ends):
    return bool(ends)


# What the rules make of a word without a meaning: the first statement that fits, in this order. Each names the
# rules that give it; one that passed is enough.
SAYS = [
    {"id": "parent", "gives": ("L1-5", "L6-2"), "what": "it stands right before a word of filiation, where a parent's name is due", "is": is_parent},
    {"id": "governed", "gives": ("L1-6",), "what": "it stands right before yetmde-, where the noun that word governs is due", "is": is_governed},
    {"id": "verb", "gives": ("L4-5",), "what": "a verb, by the prefix ps- and a verbal ending", "is": is_ps_verb},
    {"id": "verb", "gives": ("L3-7", "L1-3"), "what": "a verb, by its place right after mXe", "is": is_offering_verb},
    {"id": "verb", "gives": ("L4-3",), "what": "a verb in -kete, with its object within two words before it", "is": is_kete_verb},
    {"id": "copula", "gives": ("L8-4", "M3-1", "M6-1"), "what": "it carries the copula in -owi after l, q or t", "is": is_copula},
    {"id": "copula", "gives": ("M5-2",), "what": "a common noun with the article and the copula", "is": is_common_copula},
    {"id": "place", "gives": ("L4-1",), "what": "a place in -te, closed by the article or the copula", "is": is_place},
    {"id": "plural", "gives": ("M1-2", "M3-3", "M4-2"), "what": "it ends in -eb, the mark of the plural", "is": is_plural},
    {"id": "closes", "gives": tuple(r for m in MARKS for r in m["gives"]), "what": "it closes a clause or a sentence", "is": is_closing},
]
NOTHING = "none"                                         # no rule speaks of the word


def said_of(rs, i, passed, ends=()):
    """(the statement's id, the rules that give it) for a word, or (NOTHING, [])."""
    for s in given(SAYS, passed):
        if s["is"](rs, i, ends):
            return s["id"], sorted(set(s["gives"]) & set(passed))
    return NOTHING, []


def parse_of(rs, passed):
    """One text's words as the rules that passed cut them: each word with the marks of an end it carries and, for
    a word without a meaning, what the rules make of it."""
    ends = cuts(rs, passed)
    out = []
    for i, r in enumerate(rs):
        w = {"n": r["n"], "form": r["form"], "level": r["level"], "ends": ends.get(i, [])}
        if r["level"] in OPEN:
            w["says"], w["by"] = said_of(rs, i, passed, ends.get(i, []))
        out.append(w)
    return out


def parse_counts(words):
    """A parsed text in numbers: the cuts, the stretches between them, and the words without a meaning by what
    the rules make of them."""
    cut = [i for i, w in enumerate(words) if w["ends"]]
    stretches = [b - a for a, b in zip([-1] + cut, cut + [len(words) - 1]) if b > a]
    opened = [w for w in words if w["level"] in OPEN]
    return {"words": len(words), "open_words": len(opened), "cuts": len(cut),
            "words_up_to_the_last_cut": cut[-1] + 1 if cut else 0,
            "share_up_to_the_last_cut": round((cut[-1] + 1) / len(words), 4) if cut else 0.0,
            "longest_stretch": max(stretches) if stretches else 0,
            "marks": dict(collections.Counter(m for w in words for m in w["ends"]).most_common()),
            "open_words_by_what_is_said": dict(collections.Counter(w["says"] for w in opened).most_common()),
            "open_words_a_rule_speaks_of": sum(w["says"] != NOTHING for w in opened)}


def passed_ids():
    return sorted(rid for rnd in ROUNDS for rid, _, _ in passed(rnd))


def long_rows():
    """{long text: (its words in their order, the set it was dealt to)}, the longest first."""
    held_all = rows_of(HOME / ".held/held.tsv")
    held, by = {r["text"] for r in held_all}, collections.defaultdict(list)
    for r in rows_of(HOME / "tuning.tsv") + held_all:
        by[r["text"]].append(r)
    return {t: (rs, "held back" if t in held else "tuning")
            for t, rs in sorted(by.items(), key=lambda kv: (-len(kv[1]), kv[0])) if len(rs) >= LONG}


def parse_file(text):
    return HOME / "parse" / (text.replace(" ", "_") + ".jsonl")


def parse():
    """Write each long text's parse (local: it holds the spellings) and print its counts."""
    ids = passed_ids()
    (HOME / "parse").mkdir(exist_ok=True)
    for t, (rs, _) in long_rows().items():
        words = parse_of(rs, ids)
        parse_file(t).write_text("".join(json.dumps(w, ensure_ascii=False) + "\n" for w in words), encoding="utf-8")
        c = parse_counts(words)
        print(t, {k: c[k] for k in ("words", "open_words", "cuts", "longest_stretch", "open_words_a_rule_speaks_of")}, c["marks"])


# How a stretch of a parsed text is shown on the page: no spelling, each word by what the rules or the map know.
FIXED = (("woSi", "Isis, addressed"), ("wiSi", "Isis, addressed"), ("ato", "water"), ("at", "bread")) \
    + tuple((f, "abundant") for f in MXE)
SAID = {"parent": "name due", "governed": "noun due", "verb": "verb", "copula": "copula", "place": "place", "plural": "plural",
        "closes": "closes", NOTHING: "nothing said"}


def shown(w):
    f = w["form"]
    if dict(FIXED).get(f):
        return dict(FIXED)[f]
    if f.startswith(("Sor", "aSor")):
        return "Osiris, addressed"
    if f.startswith("tedx"):
        return "born of"
    if f.startswith("terik"):
        return "begotten of"
    if w["level"] in OPEN:
        return f"[open: {SAID[w['says']]}]"
    return {"name": "(name)", "number": "(number)", "lost": "(lost)"}.get(w["level"], "(translated)")


def stretch(words, lo, hi):
    """Words lo to hi of a parsed text (counted from 1), a double bar after each word that closes."""
    return " · ".join(shown(w) + (" ‖" if w["ends"] else "") for w in words[lo - 1: hi])


def parse_figures():
    ids = passed_ids()
    texts = []
    for t, (rs, where) in long_rows().items():
        texts.append({"text": t, "kind": rs[0]["kind"], "set": where} | parse_counts(parse_of(rs, ids)))
    said = collections.Counter()
    for x in texts:
        said.update(x["open_words_by_what_is_said"])
    return {"rules_that_passed": len(ids),
            "marks": [{k: m[k] for k in ("id", "what", "where", "from")} | {"gives": [r for r in m["gives"] if r in ids], "with": list(m["with"])}
                      for m in given(MARKS, ids)],
            "statements": [{"id": s["id"], "what": s["what"], "gives": [r for r in s["gives"] if r in ids]} for s in given(SAYS, ids)],
            "texts": texts,
            "all": {"words": sum(x["words"] for x in texts), "open_words": sum(x["open_words"] for x in texts),
                    "cuts": sum(x["cuts"] for x in texts), "open_words_by_what_is_said": dict(said.most_common()),
                    "open_words_a_rule_speaks_of": sum(x["open_words_a_rule_speaks_of"] for x in texts)}}



def cost():
    out = {}
    for rnd, R in ROUNDS.items():
        for name, f in zip(("the finders", "the readers"), R["tokens"]):
            t = next(v for v in json.loads((HOME / f).read_text(encoding="utf-8")).values() if isinstance(v, dict))
            out[f"round {rnd}, {name}"] = {"agents": len(t), "tokens": sum(t.values())}
    return out | {"all": {"agents": sum(v["agents"] for v in out.values()), "tokens": sum(v["tokens"] for v in out.values())}}


def figures():
    """What the page reports, from the local files: counts, the rules in our agents' wording, no text of a source."""
    tuning_rows, held_all = rows_of(HOME / "tuning.tsv"), rows_of(HOME / ".held/held.tsv")
    for rnd in ROUNDS:
        frozen(rnd)
    rounds = {str(rnd): round_figures(rnd, tuning_rows, held_all) for rnd in ROUNDS}
    one, two = tests(1), tests(2)
    fns = [one[x["id"]] for x in rounds["1"]["the_rules"] if x["verdict"] == "passed"]
    fns2 = [two[x["id"]] for x in rounds["2"]["the_rules"] if x["verdict"] == "passed"]
    passed_all = sum(r["passed"] for r in rounds.values())
    mine = sum(len(r["ours"]) for r in rounds.values())
    return {
        "split": {"seed": SEED, "held_share": HELD, "long_from_words": LONG, "layers": list(LAYERS),
                  "tuning": set_of(tuning_rows), "held": set_of(held_all)},
        "bars": BARS, "ours_needed": OURS_NEEDED,
        "rounds": rounds,
        "both": {"rules": sum(r["rules"] for r in rounds.values()), "passed": passed_all,
                 "stated_or_partly_stated": passed_all - mine, "ours": mine, "bar_met": mine >= OURS_NEEDED,
                 "partly_stated_by_both": sum(r["readers"]["partly stated by both"] for r in rounds.values())},
        "long_texts": long_texts(tuning_rows, held_all, fns),
        "long_texts_round_2": long_texts(tuning_rows, held_all, fns2),
        "cases_by_kind": cases_by_kind(tuning_rows + held_all, fns),
        "parse": parse_figures(),
        "cost": cost(),
        "when": {"split_drawn": WHEN["split_drawn"]} | {str(k): v for k, v in WHEN.items() if k != "split_drawn"},
    }


def public():
    figs = figures()
    PUBLIC.write_text(json.dumps(figs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", PUBLIC.relative_to(ROOT), figs["both"])


COMMANDS = {"split": split, "dump": dump, "briefs": briefs, "tuning": tuning, "held-dump": held_dump, "held": held, "packs": packs,
            "count": count, "briefs2": lambda: briefs(2), "tuning2": lambda: tuning(2), "held2": lambda: held(2),
            "packs2": lambda: packs(2), "count2": lambda: count(2), "parse": parse, "public": public}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        raise SystemExit(__doc__)
    COMMANDS[sys.argv[1]]()
