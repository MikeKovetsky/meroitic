# The leftover parts: what the checkers are given

Written on 2026-11-16 at 15:23, before any checker was started. The rules and the bars are in
[`data/discovery/leftover_parts.md`](../../data/discovery/leftover_parts.md). Each pack begins with the brief below
and then lists its places. `{places}` is the number of places in the pack and `{answers}` the file the checker
writes.

## The launch line (one fresh agent for each pack and checker, Opus)

    Read the file /Users/mike/repos/mike/meroitic/data/sources/g8/packs/P<nn>_c<1|2>.md in full and do exactly what
    it asks: write one JSON line per place to the answers file it names (the path is relative to
    /Users/mike/repos/mike/meroitic/), then reply in one line as it says. Work alone: you may search the lexicon
    under data/rilly2003/ as the file says, open no other file, do not spawn agents, and do not change any file
    other than your answers file.

## The brief

    # Say what the unnamed part of {places} Meroitic spellings is

    In each place below, the project's map of the Meroitic corpus cuts the spelling in bold into parts and ties some
    of them to entries of the dictionary of Meroitic (Rilly's lexicon of 2003). One part or more is left **unnamed**.
    Your task is to say, for every place, what the unnamed part is.

    For every place give one JSON line, in the order of this file, in the file `{answers}`, nothing else in it:

        {{"place": "Q017", "case": "ending", "entry": "", "why": "<at most twenty words>"}}

    - "case" is one of:
      - "ending": the unnamed part is nothing but endings, prefixes or particles of the word (one or several), or
        letters of a variant writing of the named part. With it the spelling is still the named word and no other.
      - "known": the unnamed part is another word that the lexicon holds with a meaning it calls established or
        probable. Put that entry's headword in "entry".
      - "name": the unnamed part is a personal, place or divine name (the spelling joins a name to the named word).
      - "unknown": the unnamed part is a word or a run of letters that nothing in hand explains. Say this also when
        the part could be cut into endings only by taking it letter by letter, with nothing in the place to show it.
      - "unclear": signs are lost in it, or the place is too thin to decide.
    - You may search the lexicon (`data/rilly2003/`, JSON lines) for the unnamed part or for pieces of it. The lexicon
      writes ḫ where the project writes `x`, ẖ for `X`, s for `S`, se for `s`, and ne or ñ for `N`. Open no other
      file, do not search the web, and do not use what you may know of Meroitic beyond the lexicon and what is shown.
    - Some places are put in on purpose: their answer is known. They look like the others.
    - "entry" is empty unless the case is "known".

    This pack lists {places} places: your file must have {places} lines, one for each place, none left out. When the
    file is written, count its lines against that number, then reply in one line: how many places, and how many of
    each case.
