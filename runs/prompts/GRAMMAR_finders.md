# The grammar-first pilot: what the rule finders are given

Written on 2026-11-16 at 19:09, before any finder was started. The rules and the bars are in
[`data/discovery/grammar_pilot.md`](../../data/discovery/grammar_pilot.md). Each of the eight finders gets the brief
below with its own angle and its own answers file (`data/sources/grammar/rules/L<k>.jsonl`).

## The brief

    # Find rules of Meroitic grammar in 329 texts

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

    **Your angle: <the finder's angle>.** Find regularities of the grammar that hold across texts. Write and run your own
    Python on the table; count before you believe.

    For each rule you keep, give one JSON line in the file `<answers>`, nothing else in it:

        {"id": "L3-2", "statement": "<one or two plain sentences>", "cases": "<exactly which places of the table are a case, in terms of its columns>", "holds": "<exactly what must be true at a case for the rule to hold>", "comparison": "<what is counted, in terms of the columns, to say how often that would be true if the rule were not there>", "tuning": {"cases": 57, "holds": 52, "comparison_rate": 0.31}, "why_grammar": "<at most 25 words: what the rule says about the language>", "known": "<what you know of published grammar on this point, or 'nothing'>"}

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
