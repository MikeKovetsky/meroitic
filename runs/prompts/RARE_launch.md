# The open spellings in one or two texts: the line each agent was started with

Every agent of `src/rare.py` was a fresh subagent (`general-purpose`, model `opus`) started on 2026-11-16 with one
of the lines below and nothing else, as the session's log records them; five lines of the literature pass carried
one sentence more, given below. The task itself is in the pack the line names: the brief of the literature pass is
`runs/prompts/RARE_literature.md` (the readers read it as `data/sources/rare/g4/lit/BRIEF.md`, the same file byte
for byte); the brief of class A read twice is `VERIFY_BRIEF` of `src/recurring.py`; the briefs of the place passes
are in `runs/prompts/RARE_places.md`. Each brief stands at the head of its pack. The packs are local only (they
quote the lexicon of 2003 and the editions). `WHEN` in `src/rare.py` gives the time of each step's first launch.

## G4, the literature pass (27 agents, one a batch)

    Working directory: /Users/mike/repos/mike/meroitic. Read the brief `data/sources/rare/g4/lit/BRIEF.md` in
    full, then your batch file `data/sources/rare/g4/lit/packs/<batch>.md`, and do the task the brief sets for
    every item of that batch. Write your answer to `data/sources/rare/g4/lit/answers/<batch>.jsonl` and to no
    other file. Follow the brief's rules exactly: quotes copied character for character from the source files,
    nothing from your own knowledge of Meroitic, no web, no project scripts. Reply as the brief asks.

The lines of the batches `b23` to `b27` had this sentence before "Reply as the brief asks.":

    If you write helper files, keep them in a folder of your own named `<batch>` inside the scratchpad, because
    other readers share the scratchpad.

## G4, class A read twice (12 agents: six packs, two readers each)

    Working directory: /Users/mike/repos/mike/meroitic. Read the file
    `data/sources/rare/g4/lit/verify/packs/A<n>_v<1|2>.md` and do exactly what it says. Open only the files it
    names in its statements. Write your answer to the file it names and to no other file. Reply with the one line
    it asks for.

## G2 and G4, the place passes (16 and 32 agents: two checkers a pack)

The line given in `runs/prompts/RARE_places.md`, with `g2` or `g4`.

## G4, the place pass, second reading (32 agents: two checkers a pack)

    Read the file /Users/mike/repos/mike/meroitic/data/sources/rare/g4/places2/packs/P<nn>_c<1|2>.md in full and
    do exactly what it asks: write one JSON line per place to the answers file it names (the path is relative to
    /Users/mike/repos/mike/meroitic/), then reply in one line as it says. Work alone: do not read any other file
    under data/sources/rare/g4/places/, data/sources/rare/g4/places2/ or data/sources/rare/g4/lit/verify/, do not
    spawn agents, and do not change any file other than your answers file.

The first twelve of these launches (the packs P01 to P06, at 13:27:31 to 13:27:54) did not run: the session's
permission check gave no verdict. The same twelve were started again from 13:29:11 on; the 32 agents that ran are
the ones counted.
