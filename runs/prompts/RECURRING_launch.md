# The recurring open words: the line each agent was started with

Every agent of `src/recurring.py` was a fresh subagent (`general-purpose`, model Opus 5.5) started on
2026-11-13 with one of the lines below and nothing else, as the session's log records them; two lines of the
literature pass carried one sentence more, given below. The task itself is in the pack the line names: the brief
of the literature pass is `runs/prompts/RECURRING_literature.md`; the briefs of the other steps are the constants
`VERIFY_BRIEF`, `PLACE_BRIEF`, `CAND_BRIEF` and `CHOICE_BRIEF` of the script, written at the head of each pack.
The packs are local only (they quote the lexicon of 2003 and the editions).

## The literature pass (ten agents, one a batch)

    Working directory: /Users/mike/repos/mike/meroitic. Read the brief `data/sources/recurring/lit/BRIEF.md` in
    full, then your batch file `data/sources/recurring/lit/packs/<batch>.md`, and do the task the brief sets for
    every item of that batch. Write your answer to `data/sources/recurring/lit/answers/<batch>.jsonl` and to no
    other file. Follow the brief's rules exactly: quotes copied character for character from the source files,
    nothing from your own knowledge of Meroitic, no web, no project scripts. Reply as the brief asks.

The lines of the batches `pieces_a` and `pieces_b` had this sentence after "every item of that batch.":

    Most items of this batch are spellings the lexicon does not hold, so the field "piece" matters most: for
    each, open every text it stands in (`data/corpus_v6.jsonl`) and say whether it is a word of its own or a piece
    of a neighbouring word or name.

## Class A read twice (six agents: three packs, two readers each)

    Working directory: /Users/mike/repos/mike/meroitic. Read the file
    `data/sources/recurring/lit/verify/packs/A<n>_v<1|2>.md` and do exactly what it says. Open only the files it
    names in its statements. Write your answer to the file it names and to no other file. Reply with the one line
    it asks for.

## The place pass (52 agents: 26 packs, two checkers each)

    Read the file /Users/mike/repos/mike/meroitic/data/sources/recurring/places/packs/P<nn>_c<1|2>.md in full and
    do exactly what it asks: write one JSON line per place to the answers file it names (the path is relative to
    /Users/mike/repos/mike/meroitic/), then reply in one line as it says. Work alone: do not read any other file
    under data/sources/recurring/places/ or data/sources/recurring/lit/verify/, do not spawn agents, and do not
    change any file other than your answers file.

## The choice test, step 1: the candidates (eight agents: four packs, two readers each)

    Read the file /Users/mike/repos/mike/meroitic/data/sources/recurring/choice/cand_packs/C<n>_r<1|2>.md in full
    and do exactly what it asks: write one JSON line per item to the answers file it names (the path is relative
    to /Users/mike/repos/mike/meroitic/), then reply in one line as it says. Work alone: do not read any other
    file under data/sources/recurring/choice/, data/sources/recurring/places/ or
    data/sources/recurring/lit/verify/, do not spawn agents, and do not change any file other than your answers
    file.

## The choice test, step 2: the blind choice (25 agents: five packs, five readers each)

    Read the file /Users/mike/repos/mike/meroitic/data/sources/recurring/choice/packs/K<n>_r<1..5>.md in full and
    do exactly what it asks: write one JSON line per word to the answers file it names (the path is relative to
    /Users/mike/repos/mike/meroitic/), then reply in one line as it says. Work alone: read no other file, do not
    search, do not spawn agents, and write no file other than your answers file.
