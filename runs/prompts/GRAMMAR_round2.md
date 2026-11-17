# The grammar-first pilot: the second round's finders, and the readers of both rounds

The first round's brief is in [`GRAMMAR_finders.md`](GRAMMAR_finders.md). The rules and the bars are in
[`data/discovery/grammar_pilot.md`](../../data/discovery/grammar_pilot.md): the second round was set there in its
section 9, committed before its finders were started. Both briefs below are the texts `src/grammar.py` holds
(`BRIEF2` and `READERS_BRIEF`); `tests/test_grammar.py` compares them with this file.

## The second round: the launch line (one fresh agent for each angle, Opus)

    Read the file /Users/mike/repos/mike/meroitic/data/sources/grammar/briefs2/M<k>.md in full and do exactly what
    it asks. Work alone: open only the one table the brief names, do not search the web, do not spawn agents, and
    write no file but the two files the brief names.

## The second round: the six angles

1. the royal and temple texts: the order of words, and what opens and what closes a sentence;
2. the documents (ostraca, papyri, vessels): numbers, what is counted, items and lists;
3. the graffiti and the oracular decrees: the frames they share, and what varies inside them;
4. the endings within a word: which ending follows which, which stand last, and what kind of word they attach to;
5. names and titles: what stands before and after a name or a title, and which endings they carry;
6. frames that repeat: pairs or runs of words that come back in the same order within a text or across texts, and what varies inside them.

## The second round: the brief

`<<ANGLE>>` is the finder's angle and `<<K>>` its number.

    # Find rules of Meroitic grammar in 168 texts that are not epitaphs

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

## The readers of both rounds: the launch line (one fresh agent for each pack and reader, Opus)

    Read the file /Users/mike/repos/mike/meroitic/data/sources/grammar/<novelty|novelty2>/packs/<pack>_r<1|2>.md in
    full and do exactly what it asks: write one JSON line per rule to the answers file it names (the path is
    relative to /Users/mike/repos/mike/meroitic/), then reply in one line as it says. Work alone: use only the
    source files the pack lists, do not search the web, do not spawn agents, and write no file but your answers
    file.

## The readers of both rounds: the brief

`<<N>>` is the number of rules in the pack and `<<ANSWERS>>` the reader's answers file. Under the brief each pack
lists its rules: the finder's statement, what counts as a case, when the rule holds, and its count on the
held-back texts.

    # Does a source state this rule of Meroitic grammar? <<N>> rules

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
