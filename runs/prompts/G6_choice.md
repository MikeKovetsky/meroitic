# The blind test again (G6): what the readers are given

Written on 2026-11-16 at 15:41, before any reader was started. The rules and the bars are in
[`data/discovery/blind_test_2.md`](../../data/discovery/blind_test_2.md).

## The launch line (one fresh agent for each pack and reader, Opus)

    Read the file /Users/mike/repos/mike/meroitic/data/sources/g6/packs/K<n>_r<r>.md in full and do exactly what it
    asks: write one JSON line per word to the answers file it names (the path is relative to
    /Users/mike/repos/mike/meroitic/), then reply in one line as it says. Work alone: open no other file, do not
    search the web, do not spawn agents, and do not change any file other than your answers file.

## The brief

The brief of the first test, `CHOICE_BRIEF` in [`src/recurring.py`](../../src/recurring.py), word for word but for
its last line, which now names the number of lines the pack expects:

    This pack lists {n} words: your file must have {n} lines, one for each word, none left out. When the file is
    written, count its lines against that number, then reply in one line: how many words, and how many of each pick.

Under each word of a pack stand its places and four meanings, A to D, in an order drawn by lot for each reader.
