# G3, the open spellings the lexicon does not hold: what the checkers are given

Written on 2026-11-16, before any checker was started. The rules and the bars are in
[`data/discovery/unnamed_spellings.md`](../../data/discovery/unnamed_spellings.md). Each pack begins with the
brief below and then lists its places. `{places}` is the number of places in the pack and `{answers}` the file
the checker writes.

## The launch line (one fresh agent for each pack and checker, Opus)

    Read the file /Users/mike/repos/mike/meroitic/data/sources/g3/<pilot|full>/packs/P<nn>_c<1|2>.md in full and
    do exactly what it asks: write one JSON line per place to the answers file it names (the path is relative to
    /Users/mike/repos/mike/meroitic/), then reply in one line as it says. Work alone: open no other file, do not
    spawn agents, and do not change any file other than your answers file.

## The brief

    # Decide, place by place, what {places} Meroitic spellings are

    The project's word-by-word map of the Meroitic corpus has no accepted meaning for the spellings below, and the
    dictionary of Meroitic does not hold them. Many such "words" are not words of their own: the edition's word
    division has cut a longer word or a name in two, or the spelling is a personal, place or divine name, which needs
    no meaning. Your task is to decide, for every place listed, what the spelling in bold is **in that place**.

    For every place give one JSON line, in the order of this file, in the file `{answers}`, nothing else in it:

        {{"place": "Q017", "case": "piece", "whole": "woSi", "why": "<at most twenty words>"}}

    - "case" is one of:
      - "name": a personal name, a place name or a god's name (or a part of one that is itself only a name). Say so
        only when the place shows it: it stands where the formulae of this kind of text put a name (the deceased
        after the opening invocation of an epitaph, a parent before a word of filiation, a person after a title or
        before a title in a list of relatives, a place before a locative ending, a god in an invocation), or the words
        around it are names of the same kind.
      - "piece": no word of its own: a part of a longer word (or name) whose other part stands right before or right
        after it, cut off by the word division. Put the whole word, joined, in the project's letters, in "whole" (for
        `wo` before `Si`: "woSi").
      - "word": a word of its own (a noun, a verb, a title, an epithet, a particle) whose meaning nobody has. This is
        the case when nothing in the place shows a name or a cut.
      - "unclear": signs are lost in or around it, or the context shown is too thin to decide.
    - Decide each place on what is shown for it: the words around it and the map's reading of each. A reading in
      square brackets is a word the map has no accepted meaning for: `[form: ?]` when it knows nothing of it,
      `[form: a guess (?)]` when an analyst made a guess. The word to judge is always shown as `[form: ?]`. Do not open any file, do not look the spelling up, do
      not use what you may know of Meroitic beyond what is shown, and do not search the web.
    - Some places are put in on purpose: their answer is known. They look like the others.
    - "whole" is empty unless the case is "piece".

    Letters: the project writes `S` for the sign s, `s` for se, `N` for ne, `X` for ẖ, `x` for ḫ.

    This pack lists {places} places: your file must have {places} lines, one for each place, none left out. When the
    file is written, count its lines against that number, then reply in one line: how many places, and how many of
    each case.

## The second pilot and the full pass (added on 2026-11-16 at 14:03, before any of their checkers was started)

The packs are under `data/sources/g3/pilot2/` (then `data/sources/g3/full/`), and the launch line names that
folder. One bullet is added to the brief, before the bullet "Some places are put in on purpose":

    - Under some places a script's note says that the word, joined with the word before or after it, gives a
      spelling the map holds. The note is a fact about letters, not a judgment: say "piece" only if the place fits it.

Such a place carries the line "A script's note: joined with a word beside it, this gives `<the joined spelling>`,
a spelling the map holds."

