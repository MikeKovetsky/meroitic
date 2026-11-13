"""F4, the rounds: ways of translating whole texts compared on the pilot's five texts, then scored once on the
renderings held back (NEXT_STEPS.md, step 25; the pilot is src/f4.py, whose texts, lexicon and scoring this reuses).

  python3 -I src/f4r.py split            the splitter's packs, one per rendered text (the five and the held ones)
  python3 -I src/f4r.py handbook         the checkers' verdicts applied to the compiled handbook
  python3 -I src/f4r.py packs r1         the writer's and the translators' packs of a round
  python3 -I src/f4r.py editors r1       the editors' packs, once the three translators have answered
  python3 -I src/f4r.py judges r1        the judges' packs and the key, once every reading and the units are in
  python3 -I src/f4r.py count r1         the scores against the bars, printed
  python3 -I src/f4r.py public r1        the same, written to data/discovery/f4_rounds_figures.json (counts only)
  python3 -I src/f4r.py show r1 [text]   the readings of a round side by side (local, for the eye)

Each command refuses to write packs again once an agent has answered them. Everything read or written but the
figures file is local (data/sources/f4r/, data/sources/f4/): Millet's edition and Rilly's lexicon are in copyright
and the agents' answers quote them. The answers are untrusted data: only their named fields are read.

What a round compares (data/discovery/f4_rounds.md says it in prose; set before any agent of the round answered):

1. "pilot": the pilot's translator, its answers as they are (src/f4.py), judged again on the new units.
2. "glosses": the map's reading of every word, word by word, with every gloss the translators see (the pilot's
   baseline showed "?" for a word the map counts as unknown though its analyst glossed a part of it).
3. "writer": one agent per text that sees only the map's readings with a status for each word and the handbook,
   and writes them as sentences. It may not depart from the map.
4. "translator": one agent per text with the pilot's materials, and three more: instructions that keep every
   meaning the materials hold (a vague gloss stays a vague gloss, a disputed word shows both readings), the
   handbook (data/sources/f4r/handbook.md, compiled from the sources in hand without Millet), and parallels: the
   other places of the corpus where a word of the text stands, with the map's readings around it.
5. "panel": three such translators, each on its own, and an editor that makes one text of the three.
6. "decoy": a translation of another inscription (the pilot's pages sample), which no judge should accept.

The units: every rendering is cut again, by one splitter per text, with the pilot's instructions but for one
rule: a unit is open only when all of it is untranslated; a phrase that joins a translated part to a Meroitic
word left as it is, is cut in two. The judges, two per text, see the readings in an order of their own; they
may use their own knowledge for one thing only, whether two names are the same place; where a reading gives two
meanings for a word they judge the first. The score is the pilot's: (given + half of partly) / scored units.
"""
import collections
import json
import pathlib
import random
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "experts")]
import f4 as F                                         # noqa: E402
import lexicon as X                                    # noqa: E402
import prepare as P                                    # noqa: E402

OUT = ROOT / "data/sources/f4r"                        # local only
HANDBOOK = OUT / "handbook.md"                         # the handbook the packs hold: the compiled one after its check
COMPILED = OUT / "handbook_compiled.md"                # as its compiler wrote it
CHECK = OUT / "handbook_check"                         # the checkers' verdicts, one file per part, and the counts
PUBLIC = ROOT / "data/discovery/f4_rounds_figures.json"

SEED = "f4 rounds"
CHUNK = 20                       # the most units one judge's pack holds
PANEL = 3                        # translators of the panel; the reading "translator" is the first of them
COMMON = 25                      # a word standing in more texts than this gets no parallels, only its count
PARALLELS, WIDTH = 3, 3          # parallels shown per word, and the words shown on each side
LETTERS = "ABCDEFGH"
ROUNDS = {
    # the five texts of the pilot: every design side by side
    "r1": {"texts": "dev", "readings": ("pilot", "glosses", "writer", "translator", "panel", "decoy")},
}
REFERENCE = "glosses"            # the reading every other is compared with
# Set on 2026-11-13, before any agent of round one answered (the judging's bars are the pilot's).
BARS = dict(F.BARS)
EXPECTED = {"glosses": (0.55, 0.70), "pilot": (0.50, 0.68), "writer_under_glosses": 0.03,
            "translator_lead": 0.05, "panel_over_translator": 0.0, "wrong": 0.05}
# The rule for what is carried to the held texts, set with them: the reading with the best pooled score among
# those whose share of wrong units is at most WRONG_OVER above the glosses'; a lead under LEAD over the glosses
# is no lead, and then the writer is carried if it is within WRITER_LOSS of the glosses, else the glosses.
LEAD, WRONG_OVER, WRITER_LOSS = 0.05, 0.02, 0.03
STATUS_ORDER = ("agreed", "stated by one", "disputed", "proposed")
# subagent tokens of each agent, from the task notifications, by hand after a run
TOKENS = {"all:splitters": 1169212}     # 18 agents, one per rendered text, 13 November 2026


def name_of(tid):
    return tid.replace(" ", "")


def sets(chosen=None):
    """The texts: "dev" the pilot's five, "held" the other renderings corpus_v6 holds, "pages" the pilot's
    pages sample (the decoys of round one)."""
    chosen = chosen or json.loads((F.OUT / "texts.json").read_text(encoding="utf-8"))
    dev = list(chosen["pilot"])
    return {"dev": dev, "held": sorted(c["id"] for c in chosen["candidates"] if c["id"] not in dev),
            "pages": list(chosen["pages"])}


def materials():
    """What the packs are built from, Millet taken out as in the pilot (src/f4.py, packs())."""
    lex = {e["headword"]: e for e in X.entries_of()}
    st = F.blind_statuses(lex.values(), X.verdicts_of(), F.millet_free_editors())
    ours = {h: ("" if F.MILLET.search(m) else m) for h, m in X.our_meanings().items()}
    return {"rows": F.rows_of(), "gl": F.glosses_of(), "entries": F.rendered(), "lex": lex, "st": st, "ours": ours,
            "withheld": F.millet_heads(lex)}


# ----------------------------------------------------------------------------------------- the map, word by word

def word_reading(g, withheld=frozenset()):
    """The reading "glosses" of one word: the pilot's baseline (f4.word_reading), but a word the map counts as
    unknown shows its analyst's gloss of a part of it, marked unsure, as the translators' packs show it."""
    gloss = F.blind_gloss(g, withheld).strip()
    if g["level"] == "unknown" and gloss not in ("", "?", F.WITHHELD):
        return f"[{g['form']}: {gloss.strip('[]')} (?)]"
    return F.word_reading(g, withheld)


def glosses(gs, withheld=frozenset()):
    return " · ".join(word_reading(g, withheld) for g in gs)


def weakest(statuses):
    """The weakest of F2's statuses in STATUS_ORDER; a status not among them is "proposed"."""
    ranks = [STATUS_ORDER.index(s) if s in STATUS_ORDER else len(STATUS_ORDER) - 1 for s in statuses]
    return STATUS_ORDER[max(ranks)] if ranks else "proposed"


def f2_status(h, st, lex):
    """One entry's status in the translator's terms: F2's ("agreed by two scholars" is "agreed"), or, for an entry
    F2 did not rate, "stated by one" when Rilly calls it established or probable and "proposed" otherwise."""
    s = st.get(h)
    if s:
        return "agreed" if s.startswith("agreed") else s if s in STATUS_ORDER else "proposed"
    e = lex.get(h)
    return "stated by one" if e and (e.get("status") or "") in ("established", "probable") else "proposed"


def map_status(g, st, lex, withheld=frozenset()):
    """The status of a word as the map reads it, by script: one of f4.STATUSES. A word whose gloss is withheld,
    or of which only the kind is known, is open."""
    level = g["level"]
    if level in ("lost", "name", "number"):
        return level
    if F.blind_gloss(g, withheld) == F.WITHHELD or level in ("unknown", "kind"):
        return "open"
    if level == "hypothesis":
        return "proposed"
    return weakest([f2_status(h, st, lex) for h in F.heads_of(g)])


# ------------------------------------------------------------------------------------------------ the parallels

def index_of(gl):
    """{form: [(text, position)]} over the corpus, in the order of the texts."""
    out = collections.defaultdict(list)
    for tid in sorted(gl):
        for i, g in enumerate(gl[tid]):
            out[g["form"]].append((tid, i))
    return out


def parallels(tid, gl, rows, withheld=frozenset(), index=None):
    """The lines of a pack's section of parallels: for each word of the text that is not a number and stands in
    other texts too, up to PARALLELS of those places with WIDTH words on each side and the map's reading of
    each; a word standing in more than COMMON other texts gets its count only. Millet is not named (label())."""
    index = index or index_of(gl)
    lines, seen = [], set()
    for g in gl[tid]:
        form = g["form"]
        if form in seen or g["level"] in ("number", "lost") or len(form) < 3:
            continue
        seen.add(form)
        places = [(t, i) for t, i in index.get(form, []) if t != tid]
        others = sorted({t for t, _ in places})
        if not places:
            continue
        if len(others) > COMMON:
            lines.append(f"- `{form}`: in {len(others)} other texts (a word of the formulae).")
            continue
        lines.append(f"- `{form}`: in {len(others)} other text{'s' if len(others) != 1 else ''}.")
        shown = set()
        for t, i in places:
            if t in shown or len(shown) == PARALLELS:
                continue
            shown.add(t)
            span = gl[t][max(0, i - WIDTH): i + WIDTH + 1]
            words = " ".join(f"**{x['form']}**" if x["form"] == form else x["form"] for x in span)
            lines.append(f"  - {label(t, rows)}: {words} = " + " · ".join(word_reading(x, withheld) for x in span))
    return lines


def label(tid, rows):
    """A text as a pack names it: its id and site; a text or a site that names Millet (the phrases his thesis of
    1968 quotes are rows of the corpus) is named without him."""
    if F.MILLET.search(tid):
        return "a phrase quoted in a study of 1968"
    site = rows[tid].get("site") or ""
    return f"{tid} ({site})" if site and not F.MILLET.search(site) else tid


# ---------------------------------------------------------------------------------------------------- the packs

SPLIT = F.SPLIT.replace(
    '- "open": true when Millet leaves the Meroitic untranslated (he writes the Meroitic word itself in the\n'
    '  rendering, or leaves a gap).',
    '- "open": true only when Millet leaves ALL of the unit untranslated: the unit is nothing but a Meroitic word\n'
    '  kept as it is, or a gap. When a phrase joins something he translates to a Meroitic word he keeps ("chief of\n'
    '  the *arebetke*", "the mother of ...", "Isis, the *wetneyineqeli*"), cut it in two units: the translated part,\n'
    '  with the kept word in round brackets after it for the reader ("chief (of the arebetke)", open false), and\n'
    '  the kept word or the gap alone (open true).').replace(
    'Below are {n} entries of N. B. Millet,', 'Below is {n} entry of N. B. Millet,').replace(
    'as the text layer of a PDF: for each, the transliteration', 'as the text layer of a PDF: the transliteration')
assert SPLIT.count("ALL of the unit") == 1 and "Below is {n} entry" in SPLIT

RULES = """How to read the materials, and what the translation must keep:

1. Lose nothing the materials hold. Where the map or the lexicon gives only a vague meaning or the kind of a
   word ("a title", "a relative", "a verb of offering"), write the Meroitic word with that meaning: "the smlo (a
   title)", "a relative (mde) of". Never put "[?]" where the materials say something, however little.
2. Where the status of a word is "disputed", or the lexicon records a second reading by another scholar, write
   the reading the materials support best and the other in brackets: "nephew or niece (or: relative)". The
   reading you write first is the one you stand by.
3. Build sentences the way the handbook says these texts are built: who is named, whose mother and father, to
   whom the dead is related and through which title in which place, and what is wished. A phrase of the
   description is one sentence about one relative.
4. Places: write the Meroitic name, and the name known today in brackets where the materials give it: "in
   Atiye (Sedeinga)".
5. Personal names are written as they stand, with a capital, in the letters of the transliteration.
6. What is open stays open: write the Meroitic word in square brackets. A guess is not a reading: mark it "(?)".
   A wrong meaning is worse than an open word."""

ANSWER = """Write your answer to the file `{answers}` as one JSON line, nothing else in the file:

    {{"text": "<its id>", "words": [{{"n": 1, "form": "<the word as in the table>", "reading": "...", "status": "...", "note": ""}}], "phrases": [{{"from": 1, "to": 3, "english": "..."}}], "translation": "...", "left_open": "one sentence: what stays open, and why"}}

Every word of the text must be in "words" once, in order, with its number and its form as the table gives them.
The statuses: "agreed", "stated by one", "disputed", "proposed", "context" (you infer the meaning from the word's
place in the text or from a parallel; say why in the note), "own" (from your own knowledge of Meroitic, not from
this pack; say what), "name", "number", "open", "lost". A word built on entries of different statuses takes the
weakest of them.

Use only this file. Do not open other files of the repository, and do not search the web. When the file is
written, reply with one line: what you could not do, or "done"."""

TRANSLATE = """# One Meroitic inscription: a translation built from the project's materials

Meroitic, the language of the kingdom of Kush (in today's Sudan, about 300 BC to AD 350), is written in a script
that can be read aloud, but the language is understood only in part: some words have an accepted meaning, many
have only a proposal, and many have none. Below is one inscription of the project's corpus, with:

- its words in order and what the project's word-by-word map holds for each;
- the entries of the lexicon those words are built on (Rilly 2003), each with a status from the project's own
  check (does a second scholar give the same meaning?) and what other scholars proposed;
- the other places in the corpus where its words stand, with the map's readings around them;
- a handbook of what the sources in hand say about the grammar and about how such texts are built.

Your task: translate the inscription as a whole, as a careful scholar would from these materials. Give every
word its reading and status, cut the text into phrases, and write one running English translation.

{rules}

The map's levels: "meaning" and "grammar": the lexicon gives the word an established or probable meaning; "name"
and "number"; "hypothesis": the lexicon has only a proposal, or the map's analyst was unsure of the cut; "kind":
only the kind of word is known; "unknown": nothing is known; "lost": signs are lost. The map reads word by word
and makes mistakes: a name read as a word, a word cut wrongly, a gloss that does not fit. You may depart from it
where the handbook, the lexicon or a parallel supports you; say so in the note. "+i", "+lowi" and the like in a
gloss are endings the map cut off and did not translate.

Spelling: S is the sign s, s the sign se, N the sign ne, X the sign ẖ, x the sign ḫ; a dot is a lost sign.

{answer}
"""

WRITE = """# One Meroitic inscription: the map's readings written as sentences

Meroitic, the language of the kingdom of Kush (in today's Sudan, about 300 BC to AD 350), is understood only in
part. Below is one inscription with the reading the project's word-by-word map gives each word and the status
of that reading, and a handbook of how such texts are built.

Your task: write the map's readings as one running English translation that a reader can follow. You are a
writer, not a translator: you may order the words into sentences as the handbook says such texts are built, and
you may not change what a word means. Do not add a meaning the table does not give, and do not drop one.

{rules}

Spelling: S is the sign s, s the sign se, N the sign ne, X the sign ẖ, x the sign ḫ; a dot is a lost sign.

Write your answer to the file `{answers}` as one JSON line, nothing else in the file:

    {{"text": "<its id>", "phrases": [{{"from": 1, "to": 3, "english": "..."}}], "translation": "..."}}

Use only this file. Do not open other files of the repository, and do not search the web. When the file is
written, reply with one line: what you could not do, or "done".
"""

EDIT = """# One Meroitic inscription: three translations made into one

Meroitic, the language of the kingdom of Kush (in today's Sudan, about 300 BC to AD 350), is understood only in
part. Three translators, each on their own, translated the inscription below from the same materials, which
follow: the map's reading of every word, the entries of the lexicon, the parallels and the handbook. Their
answers come first.

Your task: make the one translation that the materials support best.

- Go through the text word by word. Where the three agree, keep the reading. Where they differ, take the reading
  the materials support best and say in the note which translators gave it (T1, T2, T3) and why it is the better.
- Do not add a meaning that none of the three gives. Drop a reading marked "own" unless a second translator gives
  it too or the materials support it.
- Then write the running translation anew from your words, by the same rules as theirs:

{rules}

{answer}
"""

JUDGE = """# A printed rendering beside other readings of the same Meroitic inscription, unit by unit

Below you get:

- the rendering into English of one inscription printed by a scholar, N. B. Millet (2005), and {units} numbered
  units of meaning cut from it;
- {n} other readings of the same inscription, "Reading A" to "Reading {last}", in no particular order. They were
  made in different ways: some may be poor, some may be lists of word-by-word glosses, and some may not fit the
  inscription at all.

For every unit and every reading, give one verdict:

- "given": the reading states the unit's meaning. The wording may differ. A person must have the same name in
  the same role; names are spelled differently (Millet writes them in an English form with vowels, the readings
  in the letters of the transliteration, where S is s, s is se, N is ne, X is h and x is kh). A relation, title,
  place or wish must be the same.
- "partly": the reading states something that overlaps but differs in a way that matters: the right name in
  another role, a kin term of another degree, a title of another rank, a meaning much vaguer or much narrower
  than the unit's, the right wish with another object.
- "wrong": the reading gives this part of the inscription another meaning.
- "missing": the reading says nothing for this unit: it leaves the word open ("[?]", the Meroitic word in
  brackets with no meaning), has a gap, or leaves it out.

Three rules:

1. A meaning the reading marks as unsure ("?", "perhaps") still counts: judge the meaning it gives.
2. Where a reading gives two meanings for one word ("nephew or niece (or: relative)"), judge the first. If only
   the second states the unit's meaning, the verdict is "partly".
3. Judge only by what the rendering and the reading say. Do not use your own knowledge of Meroitic, and do not
   decide which of them is right. One exception: you may use what you know to tell whether two names are the
   same place (a place has a Meroitic name and a modern one); the same place under another name is the same place.

Write to the file `{answers}` as JSON lines, one line per unit and reading, in the order of this file (unit by
unit, and for each unit the readings A to {last}), nothing else in the file:

    {{"text": "{text}", "unit": "U01", "reading": "A", "verdict": "given", "note": "at most twelve words"}}

Every unit gets exactly {n} lines. Use only this file. Do not open other files of the repository, and do not
search the web. When the file is written, reply with one line: how many lines you wrote, and anything that could
not be judged.
"""


def sourced(line):
    """Whether a line of the handbook ends in its source, in square brackets."""
    return bool(re.search(r"\]\s*$", line))


def apply_check(text, verdicts):
    """(the handbook after its check, the counts). Each line that ends in a source takes its checker's verdict,
    the first given for its number: confirmed, it stays; corrected, the checker's line stands in its place, if
    that is one line that ends in a source and does not name Millet, and else the line is dropped; unsupported,
    it is dropped. A sourced line without a verdict stays and is counted. Verdicts on other lines are not read."""
    lines, by = text.split("\n"), {}
    for v in verdicts:
        n = v.get("line")
        if isinstance(n, int) and not isinstance(n, bool) and v.get("verdict") in ("confirmed", "corrected", "unsupported"):
            by.setdefault(n, v)
    out, c = [], collections.Counter()
    for n, line in enumerate(lines, 1):
        if not sourced(line):
            out.append(line)
            continue
        c["sourced"] += 1
        v = by.get(n)
        if v is None:
            c["unchecked"] += 1
            out.append(line)
        elif v["verdict"] == "confirmed":
            c["confirmed"] += 1
            out.append(line)
        elif v["verdict"] == "unsupported":
            c["unsupported"] += 1
        else:
            new = str(v.get("text") or "").strip("\n")
            if new.strip() and "\n" not in new and sourced(new) and not F.MILLET.search(new):
                c["corrected"] += 1
                out.append(new)
            else:
                c["corrected_without_a_line"] += 1
    return "\n".join(out), dict(c)


def check_handbook():
    """The command "handbook": the checkers' verdicts applied to the compiled handbook, kept beside it."""
    if not COMPILED.exists():
        if not HANDBOOK.exists():
            raise SystemExit(f"{HANDBOOK} is missing: the handbook has to be compiled first")
        COMPILED.write_text(HANDBOOK.read_text(encoding="utf-8"), encoding="utf-8")
    verdicts = [v for f in sorted(CHECK.glob("part*.jsonl")) for v in F.jsonl(f)]
    text, counts = apply_check(COMPILED.read_text(encoding="utf-8"), verdicts)
    counts["words"] = len(text.split())
    HANDBOOK.write_text(text, encoding="utf-8")
    write(CHECK / "counts.json", json.dumps(counts, indent=1) + "\n")
    print(counts)


def handbook():
    if not (CHECK / "counts.json").exists():
        raise SystemExit("the handbook has not been checked: python3 -I src/f4r.py handbook")
    if not HANDBOOK.exists():
        raise SystemExit(f"{HANDBOOK} is missing: the handbook has to be compiled first")
    text = HANDBOOK.read_text(encoding="utf-8")
    if F.MILLET.search(text):
        raise SystemExit(f"{HANDBOOK} names Millet: it may not")
    return text.strip()


def table(tid, m):
    """A text's words as the translators' packs show them (f4.translator_pack's table), and the entries used."""
    r, gl, lex, st = m["rows"][tid], m["gl"], m["lex"], m["st"]
    lines = [f"## {tid}\n\nSite: {r['site']}. Kind: {r['kind']}. Words: {len(gl[tid])}.\n\n"
             "| n | word | level | the map's reading | built on (F2 status) | the analyst's note |\n|---|---|---|---|---|---|\n"]
    used = []
    for n, g in enumerate(gl[tid], 1):
        heads = F.heads_of(g)
        used += [h for h in heads if h in lex and h not in used]
        note = F.scrub(g.get("evidence") or "") if g.get("by") == "analyst" else ""
        built = " + ".join(f"{h} ({F.part_status(h, st, lex) or 'not in the lexicon'})" for h in heads)
        cells = (str(n), g["form"], g["level"], F.blind_gloss(g, m["withheld"]), built, X.C.short(note, 160))
        lines.append("| " + " | ".join(c.replace("|", "/") for c in cells) + " |\n")
    return "".join(lines), used


def materials_text(tid, m, book, index=None):
    """The part of a pack the translators and the editor share: the table, the entries, the parallels, the
    handbook."""
    words, used = table(tid, m)
    ours = {h: x for h, x in m["ours"].items() if h not in m["withheld"]}
    par = parallels(tid, m["gl"], m["rows"], m["withheld"], index)
    return (f"\n---\n\n{words}\n---\n\n## The entries of the lexicon\n\n"
            + "\n".join(F.entry_block(h, m["lex"][h], m["st"], ours) for h in used)
            + "\n---\n\n## Other places in the corpus where these words stand\n\n"
            + ("\n".join(par) if par else "None.") + "\n\n---\n\n## The handbook\n\n" + book + "\n")


def translator_pack(tid, m, book, answers, index=None):
    return (TRANSLATE.format(rules=RULES, answer=ANSWER.format(answers=answers))
            + materials_text(tid, m, book, index))


def writer_pack(tid, m, book, answers):
    lines = [WRITE.format(rules=RULES, answers=answers), f"\n---\n\n## {tid}\n\nSite: {m['rows'][tid]['site']}. "
             f"Kind: {m['rows'][tid]['kind']}.\n\n| n | word | the map's reading | status |\n|---|---|---|---|\n"]
    for n, g in enumerate(m["gl"][tid], 1):
        cells = (str(n), g["form"], word_reading(g, m["withheld"]), map_status(g, m["st"], m["lex"], m["withheld"]))
        lines.append("| " + " | ".join(c.replace("|", "/") for c in cells) + " |\n")
    lines.append("\n---\n\n## The handbook\n\n" + book + "\n")
    return "".join(lines)


def answer_text(a):
    """One translator's answer as the editor reads it."""
    lines = ["| n | word | reading | status | note |\n|---|---|---|---|---|\n"]
    for w in a.get("words") or []:
        cells = (str(w.get("n")), str(w.get("form")), str(w.get("reading")), str(w.get("status")),
                 X.C.short(str(w.get("note") or ""), 200))
        lines.append("| " + " | ".join(c.replace("|", "/").replace("\n", " ") for c in cells) + " |\n")
    return "".join(lines) + f"\nTranslation: {a.get('translation') or ''}\n\nLeft open: {a.get('left_open') or ''}\n"


def editor_pack(tid, m, book, three, answers, index=None):
    parts = [EDIT.format(rules=RULES, answer=ANSWER.format(answers=answers))]
    for k, a in enumerate(three, 1):
        parts.append(f"\n---\n\n## Translator T{k}\n\n{answer_text(a)}")
    return "".join(parts) + materials_text(tid, m, book, index)


def splitter_pack(tid, entries, answers):
    translit, rend = F.sections(entries[(name_of(tid),)])
    return (SPLIT.format(n=1, answers=answers) + f"\n---\n\n## {name_of(tid)}\n\n### Transliteration\n\n```\n{translit}\n```\n\n"
            f"### Rendering\n\n```\n{rend}\n```\n")


def order_of(rnd, judge, text, readings):
    """{letter: reading} for one judge and one text of a round, from a Random of its own."""
    return dict(zip(LETTERS, random.Random(f"{SEED} {rnd} order judge{judge} {text}").sample(list(readings), len(readings))))


def chunks(units, size=CHUNK):
    """The units a judge gets (those not open), in packs of at most size, of sizes as equal as can be."""
    judged = [u["unit"] for u in units if not u["open"]]
    if not judged:
        return []
    n = -(-len(judged) // size)
    step = -(-len(judged) // n)
    return [judged[i: i + step] for i in range(0, len(judged), step)]


def judge_pack(tid, rend, units, chunk, order, readings, answers):
    """One judge's pack for one text and one chunk of its units. order: {letter: name}; readings: {name: text}."""
    last = LETTERS[len(order) - 1]
    parts = [JUDGE.format(units=len(chunk), n=len(order), last=last, answers=answers, text=name_of(tid)),
             f"\n---\n\n## {name_of(tid)}\n\n### The printed rendering\n\n```\n{rend}\n```\n\n"
             "### The units to judge\n\n| unit | kind | the rendering's words |\n|---|---|---|\n"]
    by = {u["unit"]: u for u in units}
    for name in chunk:
        parts.append(f"| {name} | {by[name]['kind']} | {by[name]['english'].replace('|', '/')} |\n")
    for letter, name in order.items():
        parts.append(f"\n### Reading {letter}\n\n{readings[name]}\n")
    return "".join(parts)


# -------------------------------------------------------------------------------------------- answers of a round

def folder(rnd):
    return OUT / rnd


def units_all(ids):
    """{text: [unit]} from the splitters' files, one file per text."""
    out = {}
    for tid in ids:
        out.update(F.units_of(OUT / "split" / "answers" / f"{name_of(tid)}.jsonl", [tid]))
    return out


def one_answer(path, tid, gl=None):
    """(the answer of a file that holds one text's answer, its faults). With gl the answer is checked as a
    translator's (f4.check_translation); without, only for a running translation."""
    rows = [a for a in F.jsonl(path) if F.text_id(a.get("text"), [tid])]
    if not rows:
        return None, ["not answered"]
    a = rows[0]
    faults = F.check_translation(a, gl[tid]) if gl is not None else (
        [] if (a.get("translation") or "").strip() else ["no running translation"])
    return a, faults


def readings_of(rnd, ids, m, pages=None):
    """({text: {reading name: text}}, {(reading, text): faults}) of a round: every reading the judges get but the
    decoy, which judges() adds."""
    names = [n for n in ROUNDS[rnd]["readings"] if n != "decoy"]
    out, faults = {t: {} for t in ids}, {}
    pilot = F.translations(F.OUT / "answers" / "translator_pilot.jsonl", ids, m["gl"])[0] if "pilot" in names else {}
    for t in ids:
        for n in names:
            if n == "glosses":
                out[t][n] = glosses(m["gl"][t], m["withheld"])
                continue
            if n == "pilot":
                a, f = pilot.get(t), ([] if t in pilot else ["not answered"])
            else:
                sub = {"writer": "writer", "translator": "translator1", "panel": "editor"}[n]
                a, f = one_answer(folder(rnd) / "answers" / sub / f"{name_of(t)}.jsonl", t,
                                  None if n == "writer" else m["gl"])
            if f:
                faults[(n, t)] = f
            if a:
                out[t][n] = (a.get("translation") or "").strip()
    return out, faults


def verdicts_of(rnd, key, judge):
    """{(text, unit, reading name): verdict} of one judge over all its packs of a round (f4.verdicts_of each)."""
    out = {}
    for path in sorted((folder(rnd) / "answers" / f"judge{judge}").glob("*.jsonl")):
        for k, v in F.verdicts_of(path, key, judge).items():
            out.setdefault(k, v)
    return out


# ---------------------------------------------------------------------------------------------------- the count

def rank(v):
    return {"given": 3, "partly": 2, "missing": 1, "wrong": 0}.get(v)


def compare(v, units, name, other=REFERENCE):
    """How a reading's verdicts stand to another's on the same units, for one judge: better, worse, same."""
    c = collections.Counter()
    for t, u in units:
        a, b = rank(v.get((t, u, name))), rank(v.get((t, u, other)))
        if a is not None and b is not None:
            c["better" if a > b else "worse" if a < b else "same"] += 1
    return dict(c)


def carried(score, wrong, names):
    """The reading carried to the held texts by the rule set beforehand (LEAD, WRONG_OVER, WRITER_LOSS). The
    differences are rounded to four places, as the scores are, so that 0.60 - 0.57 is 0.03."""
    if score.get(REFERENCE) is None:
        return None
    ok = [n for n in names if n not in ("decoy", "pilot", REFERENCE, "writer") and score.get(n) is not None
          and round(wrong[n] - wrong[REFERENCE], 4) <= WRONG_OVER]
    best = max(ok, key=lambda n: (score[n], -names.index(n))) if ok else None
    if best and round(score[best] - score[REFERENCE], 4) >= LEAD:
        return best
    if score.get("writer") is not None and round(score[REFERENCE] - score["writer"], 4) <= WRITER_LOSS:
        return "writer"
    return REFERENCE


def count(rnd):
    """Every figure of a round: the units, each reading's score with its share of given and of wrong units, its
    lead over the glosses, unit by unit against the glosses, by text and by kind, the judges' agreement, the
    decoys, the bars, and the reading carried on."""
    key = json.loads((folder(rnd) / "key.json").read_text(encoding="utf-8"))
    ids, names = key["texts"], key["readings"]
    real = [n for n in names if n != "decoy"]
    units = units_all(ids)
    judged = [(t, u["unit"]) for t in ids for u in units.get(t, []) if not u["open"]]
    scored = [(t, u) for t, u in judged if key["units"][t][u]["in_copy"]]
    v = {j: verdicts_of(rnd, key, j) for j in (1, 2)}
    every = [u for t in ids for u in units.get(t, [])]
    figs = {"round": rnd, "texts": ids, "readings": names,
            "units": {"all": len(every), "open": sum(u["open"] for u in every), "judged": len(judged),
                      "not_in_copy": len(judged) - len(scored), "scored": len(scored),
                      "open_with_a_translated_part": sum(u["open"] and F.translated_part(u) for u in every),
                      "by_kind": dict(collections.Counter(key["units"][t][u]["kind"] for t, u in scored)),
                      "per_text": {t: sum(x == t for x, _ in scored) for t in ids}},
            "scores": {}}
    for j in (1, 2):
        figs["scores"][str(j)] = {}
        for n in names:
            c = F.tallies(v[j], scored, n)
            figs["scores"][str(j)][n] = {**{x: c.get(x, 0) for x in F.VERDICTS + ("unanswered",)}, "score": F.score(c),
                                         "given_share": round(c.get("given", 0) / len(scored), 4) if scored else None,
                                         "wrong_share": round(c.get("wrong", 0) / len(scored), 4) if scored else None}
    for what, field in (("score", "score"), ("given", "given_share"), ("wrong", "wrong_share")):
        figs[what] = {n: F.mean([figs["scores"][j][n][field] for j in ("1", "2")]) for n in names}
    figs["lead"] = {n: round(figs["score"][n] - figs["score"][REFERENCE], 4) for n in real
                    if n != REFERENCE and None not in (figs["score"][n], figs["score"].get(REFERENCE))}
    figs["unit_by_unit"] = {str(j): {n: compare(v[j], scored, n) for n in real if n != REFERENCE} for j in (1, 2)}
    figs["per_text"] = {t: {n: F.mean([F.score(F.tallies(v[j], [(x, u) for x, u in scored if x == t], n)) for j in (1, 2)])
                            for n in real} for t in ids}
    figs["per_text_mean"] = {n: F.mean([figs["per_text"][t][n] for t in ids]) for n in real}
    figs["by_kind"] = {k: {n: F.mean([F.score(F.tallies(v[j], [(t, u) for t, u in scored
                                                                if key["units"][t][u]["kind"] == k], n)) for j in (1, 2)])
                           for n in real} for k in sorted(figs["units"]["by_kind"])}
    figs["agreement"] = F.judges_agreement(v[1], v[2], scored, names=tuple(real))
    figs["decoys_measure"] = {}
    for j in (1, 2):
        c = collections.Counter(v[j].get((t, u, "decoy"), "unanswered") for t, u in scored if key["units"][t][u]["clean"])
        figs["decoys_measure"][str(j)] = {"clean_units": sum(c.values()), "accepted": c["given"] + c["partly"],
                                          "verdicts": dict(c)}
    figs["bars"] = F.bars_of(figs["agreement"]["kappa"], figs["decoys_measure"])
    figs["bars_set"], figs["expected"] = BARS, EXPECTED
    figs["rule"] = {"lead": LEAD, "wrong_over": WRONG_OVER, "writer_loss": WRITER_LOSS}
    figs["carried"] = carried(figs["score"], figs["wrong"], names)
    counts = CHECK / "counts.json"
    figs["handbook"] = json.loads(counts.read_text(encoding="utf-8")) if counts.exists() else {}
    figs["tokens"] = {k: v for k, v in TOKENS.items() if k.startswith(rnd + ":") or k.startswith("all:")}
    return figs


# -------------------------------------------------------------------------------------------------- the commands

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def split():
    """The splitters' packs, one per rendered text. Refuses once a splitter has answered."""
    if any((OUT / "split" / "answers").glob("*.jsonl")):
        raise SystemExit("a splitter has answered: not writing the splitters' packs again")
    s, entries = sets(), F.rendered()
    for tid in s["dev"] + s["held"]:
        write(OUT / "split" / "packs" / f"{name_of(tid)}.md",
              splitter_pack(tid, entries, f"data/sources/f4r/split/answers/{name_of(tid)}.jsonl"))
    (OUT / "split" / "answers").mkdir(exist_ok=True)
    print("splitter packs:", len(s["dev"] + s["held"]), "| dev:", s["dev"], "| held:", s["held"])


def packs(rnd):
    """The writer's and the translators' packs of a round. Refuses once one of them has answered."""
    base = folder(rnd)
    if any((base / "answers").glob("*/*.jsonl")):
        raise SystemExit(f"{base}/answers holds answers: not writing the packs again")
    ids, m, book = sets()[ROUNDS[rnd]["texts"]], materials(), handbook()
    index = index_of(m["gl"])
    rel = f"data/sources/f4r/{rnd}/answers"
    for tid in ids:
        n = name_of(tid)
        write(base / "packs" / f"writer_{n}.md", writer_pack(tid, m, book, f"{rel}/writer/{n}.jsonl"))
        for k in range(1, PANEL + 1):
            write(base / "packs" / f"translator{k}_{n}.md",
                  translator_pack(tid, m, book, f"{rel}/translator{k}/{n}.jsonl", index))
    for sub in ["writer", "editor"] + [f"translator{k}" for k in range(1, PANEL + 1)] + ["judge1", "judge2"]:
        (base / "answers" / sub).mkdir(parents=True, exist_ok=True)
    for f in sorted((base / "packs").glob("*.md")):
        print(f.name, f.stat().st_size, "bytes")


def editors(rnd):
    """The editors' packs, once the three translators of every text have answered. Refuses once an editor has."""
    base = folder(rnd)
    if any((base / "answers" / "editor").glob("*.jsonl")):
        raise SystemExit("an editor has answered: not writing the editors' packs again")
    ids, m, book = sets()[ROUNDS[rnd]["texts"]], materials(), handbook()
    index = index_of(m["gl"])
    for tid in ids:
        n, three = name_of(tid), []
        for k in range(1, PANEL + 1):
            a, f = one_answer(base / "answers" / f"translator{k}" / f"{n}.jsonl", tid, m["gl"])
            if f:
                raise SystemExit(f"translator {k} on {tid}: {f}")
            three.append(a)
        write(base / "packs" / f"editor_{n}.md",
              editor_pack(tid, m, book, three, f"data/sources/f4r/{rnd}/answers/editor/{n}.jsonl", index))
        print(f"editor_{n}.md", (base / "packs" / f"editor_{n}.md").stat().st_size, "bytes")


def judges(rnd):
    """The judges' packs and the key, once every reading and the units are in. Refuses once a judge has answered."""
    base = folder(rnd)
    if any((base / "answers").glob("judge*/*.jsonl")):
        raise SystemExit("a judge has answered: not writing the judges' packs again")
    s, m = sets(), materials()
    ids, names = s[ROUNDS[rnd]["texts"]], list(ROUNDS[rnd]["readings"])
    units = units_all(ids)
    readings, faults = readings_of(rnd, ids, m)
    if faults or set(units) != set(ids):
        raise SystemExit(f"answers incomplete: {faults or 'readings ok'}; splitters' texts {sorted(units)}")
    renderings = {t: F.sections(m["entries"][(name_of(t),)])[1] for t in ids}
    tp, f2 = F.translations(F.OUT / "answers" / "translator_pages.jsonl", s["pages"], m["gl"])
    if f2:
        raise SystemExit(f"the decoys' translations: {f2}")
    decoys, shared = F.assign_decoys(renderings, {p: tp[p]["translation"] for p in s["pages"]})
    for t in ids:
        readings[t]["decoy"] = tp[decoys[t]]["translation"]
    ours = {t: P.reduced_ours(m["rows"][t]["text"].split()) for t in ids}
    key = {"round": rnd, "texts": ids, "readings": names, "decoys": decoys, "decoy_shared_words": shared,
           "order": {str(j): {t: order_of(rnd, j, t, names) for t in ids} for j in (1, 2)},
           "chunks": {t: chunks(units[t]) for t in ids},
           "units": {t: {u["unit"]: {"kind": u["kind"], "open": u["open"], "doubt": u["doubt"],
                                     "in_copy": F.in_copy(u["meroitic"], ours[t]),
                                     "clean": F.clean(u["english"], readings[t]["decoy"])} for u in units[t]} for t in ids}}
    lines = 0
    for j in (1, 2):
        for t in ids:
            for c, chunk in enumerate(key["chunks"][t], 1):
                rel = f"data/sources/f4r/{rnd}/answers/judge{j}/{name_of(t)}_{c}.jsonl"
                write(base / "packs" / f"judge{j}_{name_of(t)}_{c}.md",
                      judge_pack(t, renderings[t], units[t], chunk, key["order"][str(j)][t], readings[t], rel))
                lines += len(chunk) * len(names)
    write(base / "key.json", json.dumps(key, ensure_ascii=False, indent=1) + "\n")
    print("units:", sum(len(units[t]) for t in ids), "| judged:", sum(len(c) for t in ids for c in key["chunks"][t]),
          "| packs per judge:", sum(len(key["chunks"][t]) for t in ids), "| lines for both judges:", lines,
          "| decoys:", decoys, "| shared words:", shared)


def show(rnd, only=None):
    s, m = sets(), materials()
    ids = [t for t in s[ROUNDS[rnd]["texts"]] if not only or name_of(t) == name_of(only)]
    readings, faults = readings_of(rnd, ids, m)
    for t in ids:
        print(f"\n===== {t}")
        for n, text in readings[t].items():
            print(f"\n--- {n}\n{text}")
    if faults:
        print("\nfaults:", faults)


def main(argv):
    cmd, args = (argv[1:2] or [""])[0], argv[2:]
    if cmd == "split" and not args:
        return split()
    if cmd == "handbook" and not args:
        return check_handbook()
    if cmd in ("packs", "editors", "judges") and len(args) == 1 and args[0] in ROUNDS:
        return {"packs": packs, "editors": editors, "judges": judges}[cmd](args[0])
    if cmd in ("count", "public") and len(args) == 1 and args[0] in ROUNDS:
        figs = count(args[0])
        print(json.dumps(figs, ensure_ascii=False, indent=1))
        if cmd == "public":
            old = json.loads(PUBLIC.read_text(encoding="utf-8")) if PUBLIC.exists() else {}
            old[args[0]] = figs
            PUBLIC.write_text(json.dumps(old, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        return
    if cmd == "show" and args and args[0] in ROUNDS:
        return show(args[0], args[1] if len(args) > 1 else None)
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
