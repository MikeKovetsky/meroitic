# The place pass of the open spellings that stand in one or two texts: what the checkers are given

Written on 2026-11-16, before any checker of either step was started. The rules and the bars of both steps are in
[`data/discovery/rare_spellings.md`](../../data/discovery/rare_spellings.md) (sections 3 and 4). Each pack begins
with one of the two briefs below and then lists its items, each with a header and its places. `{n}` is the
number of items in the pack and `{answers}` the file the checker writes. Both briefs are the place brief of
the recurring open words (`PLACE_BRIEF` of `src/recurring.py`) with the changes named here.

## The launch line (one fresh agent for each pack and checker, Opus)

    Read the file /Users/mike/repos/mike/meroitic/data/sources/rare/<g2|g4>/places/packs/P<nn>_c<1|2>.md in full
    and do exactly what it asks: write one JSON line per place to the answers file it names (the path is relative
    to /Users/mike/repos/mike/meroitic/), then reply in one line as it says. Work alone: do not read any other
    file under data/sources/rare/<g2|g4>/places/ or data/sources/rare/g4/lit/verify/, do not spawn agents, and do
    not change any file other than your answers file.

## G2: the spellings under an entry the lexicon calls sure

Changed against the recurring words' brief: the introduction, and the case "stated", which here means a form of
the lexicon's own word. In each item's header the line of the statement reads "The lexicon's own entry, which it
calls sure".

    # Decide, place by place, what {n} spellings of Meroitic are

    The project's word-by-word map of the Meroitic corpus holds no accepted meaning for the spellings below, although it files each under an
    entry of the lexicon of 2003 whose meaning that lexicon calls established or probable. Each stands in one or
    two texts. Your task is to decide, for every place listed, what the spelling is **in that
    place**.

    For every place give one JSON line, in the order of this file, in the file `{answers}`, nothing else in it:

        {{"item": "<the item's name as given here>", "place": 3, "case": "piece", "whole": "woSi", "meaning": "Isis", "why": "<at most twenty words>"}}

    - "case" is one of:
      - "stated": the spelling here is a form of the word (or the ending) of the lexicon that the item's header names,
        in a use its meaning covers: that word with endings, in a variant writing, or in a compound. Put the
        lexicon's meaning, shortened to at most eight words of your own, in "meaning".
      - "piece": the spelling here is no word of its own: the edition's word division has cut a longer word or a name,
        and this is a part of it. Put the whole word, joined, in the project's letters, in "whole" (for `wo` before
        `Si`: "woSi"), and in "meaning" what the map, the lexicon of 2003 or a source in the header says of the whole
        (empty if nothing).
      - "open": the spelling here is a word (or an ending) of its own, and no source in the header states a meaning
        that applies to this place. A meaning that is only proposed, doubted, or stated for another use is "open".
      - "unclear": signs are lost around it, or the context shown is too thin to decide between the cases above.
    - Decide each place on what is shown for it: the words around it, the map's reading of each, the header's
      statements. The first pass's summary ("Said of it") is a claim to check, not a fact: it may be wrong for a place.
    - You may open the files named in the statements, and search the lexicon of 2003 (`data/rilly2003/`, JSON lines)
      for a joined word. Do not use your own knowledge of Meroitic, do not search the web, do not run the project's
      scripts, and write no other file.
    - "whole" is empty unless the case is "piece"; "meaning" is empty for "open" and "unclear".

    Letters: the project writes `S` for the sign s, `s` for se, `N` for ne, `X` for ẖ, `x` for ḫ; Rilly 2021 writes h
    for ẖ and x for ḫ, and cuts words with hyphens. In a place, the spelling is in bold; `[...]` in the readings marks
    a word the map has no accepted meaning for. The repository's root is /Users/mike/repos/mike/meroitic.

    When the file is written, reply in one line: how many places, and how many of each case.

## G4: the spellings under an entry without an accepted meaning

Changed against the recurring words' brief: "three texts or more" reads "one or two texts".

    # Decide, place by place, what {n} spellings of Meroitic are

    The project's word-by-word map of the Meroitic corpus holds no accepted meaning for the spellings below. Each
    stands in one or two texts. A first pass collected what the sources say about each item, with quotes that a
    script has found in the files. Your task is to decide, for every place listed, what the spelling is **in that
    place**.

    For every place give one JSON line, in the order of this file, in the file `{answers}`, nothing else in it:

        {{"item": "<the item's name as given here>", "place": 3, "case": "piece", "whole": "woSi", "meaning": "Isis", "why": "<at most twenty words>"}}

    - "case" is one of:
      - "stated": the spelling here is the word (or the ending) of which the later source named in the item's header
        speaks, in the use it describes. Only possible when the header has a line "A later source states". Put that
        meaning in "meaning".
      - "piece": the spelling here is no word of its own: the edition's word division has cut a longer word or a name,
        and this is a part of it. Put the whole word, joined, in the project's letters, in "whole" (for `wo` before
        `Si`: "woSi"), and in "meaning" what the map, the lexicon of 2003 or a source in the header says of the whole
        (empty if nothing).
      - "open": the spelling here is a word (or an ending) of its own, and no source in the header states a meaning
        that applies to this place. A meaning that is only proposed, doubted, or stated for another use is "open".
      - "unclear": signs are lost around it, or the context shown is too thin to decide between the cases above.
    - Decide each place on what is shown for it: the words around it, the map's reading of each, the header's
      statements. The first pass's summary ("Said of it") is a claim to check, not a fact: it may be wrong for a place.
    - You may open the files named in the statements, and search the lexicon of 2003 (`data/rilly2003/`, JSON lines)
      for a joined word. Do not use your own knowledge of Meroitic, do not search the web, do not run the project's
      scripts, and write no other file.
    - "whole" is empty unless the case is "piece"; "meaning" is empty for "open" and "unclear".

    Letters: the project writes `S` for the sign s, `s` for se, `N` for ne, `X` for ẖ, `x` for ḫ; Rilly 2021 writes h
    for ẖ and x for ḫ, and cuts words with hyphens. In a place, the spelling is in bold; `[...]` in the readings marks
    a word the map has no accepted meaning for. The repository's root is /Users/mike/repos/mike/meroitic.

    When the file is written, reply in one line: how many places, and how many of each case.

## G4, the second reading of the places (added on 2026-11-16 at 13:27, before its checkers were started)

The first reading was not taken: one place of 695 had one checker's answer only. The packs are the same; the
answers go to `data/sources/rare/g4/places2/`, and the launch line names that folder. The brief's last line,
"When the file is written, reply in one line: how many places, and how many of each case.", now reads (with the
pack's own number in the place of `{places}`):

    This pack lists {places} places: your file must have {places} lines, one for each place, none left out. When the
    file is written, count its lines against that number, then reply in one line: how many places, and how many of
    each case.
