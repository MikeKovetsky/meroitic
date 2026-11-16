# Distinct words: the line each checker was started with

The 20 checkers of `src/words.py` were fresh subagents (`general-purpose`, model Opus 5.5), started on 2026-11-16
with the line below and nothing else. The task is the constant `BRIEF` of the script, written at the head of each
pack. The packs are local only (they quote the lexicon of 2003).

    Read the file /Users/mike/repos/mike/meroitic/data/sources/words/packs/S<nn>_c<1|2>.md in full and do exactly
    what it asks: write one JSON line per item to the answers file it names (the path is relative to
    /Users/mike/repos/mike/meroitic/), then reply in one line as it says. Work alone: do not read any other file
    under data/sources/words/ or data/sources/recurring/, do not spawn agents, and do not change any file other
    than your answers file.
