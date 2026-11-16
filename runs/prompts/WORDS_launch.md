# Distinct words: the line each checker was started with

The checkers of `src/words.py` were fresh subagents (`general-purpose`, model Opus 5.5), started on 2026-11-16
with the line below and nothing else: 20 for the first reading and 20 others for the second. The task is the
constant `BRIEF` of the script for the first reading and `BRIEF2` (the same with the rules of `RULES2`) for the
second, written at the head of each pack. The packs are local only (they quote the lexicon of 2003).

    Read the file /Users/mike/repos/mike/meroitic/data/sources/words/packs/S<nn>_c<1|2>.md in full and do exactly
    what it asks: write one JSON line per item to the answers file it names (the path is relative to
    /Users/mike/repos/mike/meroitic/), then reply in one line as it says. Work alone: do not read any other file
    under data/sources/words/ or data/sources/recurring/, do not spawn agents, and do not change any file other
    than your answers file.

For the second reading the path is `data/sources/words/r2/packs/S<nn>_c<1|2>.md`, and the line names `r2` among
the folders not to read:

    Read the file /Users/mike/repos/mike/meroitic/data/sources/words/r2/packs/S<nn>_c<1|2>.md in full and do
    exactly what it asks: write one JSON line per item to the answers file it names (the path is relative to
    /Users/mike/repos/mike/meroitic/), then reply in one line as it says. Work alone: do not read any other file
    under data/sources/words/ or data/sources/recurring/, do not spawn agents, and do not change any file other
    than your answers file.
