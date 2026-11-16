# G5, a second scholar for Rilly's later meanings: what the judges are given

Written on 2026-11-16, before any judge was started. The rules and the bars are in
[`data/discovery/second_scholar_later.md`](../../data/discovery/second_scholar_later.md). Each pack begins with the
brief below and then lists its rows. `{rows}` is the number of rows in the pack and `{answers}` the file the
judge writes.

## The launch line (one fresh agent for each pack and judge, Opus)

    Read the file /Users/mike/repos/mike/meroitic/data/sources/g5/packs/J<nn>_j<1|2>.md in full and do exactly
    what it asks: write one JSON line per row to the answers file it names (the path is relative to
    /Users/mike/repos/mike/meroitic/), then reply in one line as it says. Work alone: open no other file, do not
    spawn agents, and do not change any file other than your answers file.

## The brief

    # Two statements about the meaning of a Meroitic word: do they give the same meaning?

    Each row below has a Meroitic word (an entry of a dictionary: a word, a stem, or an ending written with a
    hyphen), the meaning a recent work gives it, and what another scholar says about it (a quote, or a dictionary's
    report of that scholar's proposal, and a line on what it says). For each row, say whether the other scholar gives
    the same meaning as the recent work:

    - "same": the same meaning, perhaps in other words, a little wider or narrower, or with a different shade
      ("king" and "ruler"; "to give" and "to grant"; "genitive ending" and "possessive suffix");
    - "partly": the two overlap but are not the same meaning (one is a part or a kind of the other, or they share a
      field but name different things: "prince" and "king's son"; "water" and "libation");
    - "other": a different meaning;
    - "no meaning": the other scholar says nothing about the meaning (only about the word's form, reading, class or
      ending, or only prints the word), so that it can neither agree nor disagree. A statement that only rejects some
      meaning without giving its own is "no meaning", unless the meaning it rejects is the recent work's: then "other".

    Judge each row on its own, from the two statements alone; do not look anything up and open no other file. Some
    rows are wrong on purpose. Write one JSON object per row, in the order of this file, to `{answers}`:

    {{"row": "R0001", "verdict": "same", "why": "both say king"}}

    "why" is at most twelve words. This pack has {rows} rows: your file must have {rows} lines, one for each row, none
    left out. When the file is written, count its lines against that number, then reply in one line: how many rows,
    and how many of each verdict.
