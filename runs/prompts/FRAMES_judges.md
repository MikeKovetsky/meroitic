# Track B, the royal texts beside the Kushite kings' Egyptian texts: what the judges are given

Written on 2026-11-16 at 22:02, before any aligner or judge was started. The rules and the bars are in
[`data/discovery/outside_evidence.md`](../../data/discovery/outside_evidence.md), section 3. The judges' packs are
written by [`src/frames.py`](../../src/frames.py); the two briefs below are its `JUDGE_BRIEF` and `OPEN_BRIEF`,
word for word.

Two judges read the same rows, each alone. The rows are cut into packs of at most 120; each pack goes to two
fresh agents, one for each judge. A pack opens with the brief, with the number of its rows and the judge's answers
file filled in; the rows follow it. No judge is given a key.

## The launch line (one fresh agent for each pack and judge)

    Read the file /Users/mike/repos/mike/meroitic/data/sources/frames/<judge|open>/packs/<pack>_j<1|2>.md in full
    and do exactly what it asks: write one JSON line for each row to the answers file it names (the path is
    relative to /Users/mike/repos/mike/meroitic/), then reply in one line as it says. Work alone: open no other
    file, do not search the web, do not spawn agents, and write no file but your answers file.

## The brief for the hidden words (`judge-packs`, once every aligner has answered)

A row pairs an answer for a hidden word with a meaning: the meaning of its word, or the meaning of another hidden
word of the fold, its decoy. Every answer stands in both kinds of row. The rows are shuffled, and a pair of texts
stands once, whichever arm, pack or aligner it comes from: a row names none of them. The answers file is
`data/sources/frames/judge/answers<1|2>/J<NN>.jsonl`.

    # Does an answer give the meaning of a word? <n> rows

    Each row below pairs two short texts. The answer is what a reader took a word of a text to mean, from the text
    around it; the reader did not see the word. The meaning is what is known of a word. For each row say whether the
    answer gives that meaning.

    - "same": the answer names what the meaning names: the same thing, person, deed or quality, in the same or in
      other words ("sovereign" for "king, ruler"; "to slay" for "to kill, slaughter"). Where the meaning lists several
      senses, one of them is enough. Words of doubt in either text ("probably", "(?)") do not count.
    - "partly": the answer is wider or narrower than the meaning, or names something close to it of the same field
      ("an official" for "viceroy"; "a relative" for "nephew or niece"; "an offering" for "bread").
    - "another": anything else: another meaning, or a meaning that does not say what the word means.

    Many rows pair an answer with a meaning that is not its word's: you are not told which rows, and you are not told
    who gave an answer or what the reader was given. Judge each row on its own, by the two texts alone.

    For each row give one JSON line, in the order of this file, in the file `<answers>` (the path is relative to
    /Users/mike/repos/mike/meroitic/), nothing else in it:

        {"row": "R0001", "verdict": "same"}

    Work alone: open no other file, do not search the web, do not spawn agents, and write no file but your answers
    file. This file lists <n> rows: your file must have <n> lines. When it is written, count its lines against that
    number, then reply in one line: how many rows, and how many of each verdict.

## The brief for the open words (`open-packs`, only once `count` says that gate B is met)

A row pairs the two answers that the two aligners with the frames gave one open word in one pack, where both gave
a meaning. The answers file is `data/sources/frames/open/answers<1|2>/O<NN>.jsonl`.

    # Do two answers give the same meaning? <n> rows

    Each row below pairs two short answers. Two readers, each alone, said what a word of a text means, from the text
    around it; they did not see the word. For each row say whether the two answers give the same meaning.

    - "same": both name the same thing, person, deed or quality, in the same or in other words ("sovereign" and
      "king, ruler"; "to slay" and "to kill"). Words of doubt in either ("probably", "(?)") do not count.
    - "partly": one is wider or narrower than the other, or they name close things of the same field ("an official"
      and "viceroy"; "an offering" and "bread").
    - "another": anything else.

    For each row give one JSON line, in the order of this file, in the file `<answers>` (the path is relative to
    /Users/mike/repos/mike/meroitic/), nothing else in it:

        {"row": "P0001", "verdict": "same"}

    Work alone: open no other file, do not search the web, do not spawn agents, and write no file but your answers
    file. This file lists <n> rows: your file must have <n> lines. When it is written, count its lines against that
    number, then reply in one line: how many rows, and how many of each verdict.
