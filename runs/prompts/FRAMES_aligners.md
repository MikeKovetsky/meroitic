# Track B, the royal texts beside the Kushite kings' Egyptian texts: what the aligners are given

Written on 2026-11-16 at 22:02, before any aligner was started, and rewritten the same evening with the answers
the page added at about 22:15, still before any aligner was started. The rules and the bars are in
[`data/discovery/outside_evidence.md`](../../data/discovery/outside_evidence.md), section 3. The packs, their key,
the briefs and the digest of the frames are written by [`src/frames.py`](../../src/frames.py) (`packs`); the
brief below is its `ALIGNER_BRIEF`, word for word.

There are 10 packs in each of the two folds. Each pack of a fold goes to four fresh agents: two with the frames
(arm `frames`) and two with the pack alone (arm `plain`), 80 agents in all. Each agent has a file of its own,
`data/sources/frames/briefs/<arm>/<pack>_<a|b>.md`: the brief of its arm with its pack (`f<fold>_p<NN>`), its
answers file (`data/sources/frames/answers/<arm>/<pack>_<a|b>.jsonl`) and the number of codes of its pack
filled in. No agent is given the key (`data/sources/frames/packs/key.json`). The brief does not say that some codes
are known words (the page's answer 6).

The arm with the frames reads one file, `data/sources/frames/frames_digest.md`: the frames of the six files of the
frame builders, each with its id, name, place in a text and monuments, and each slot with its number, meaning,
wording and whether it may be left out or repeated, without the sources' passages and notes (the page's answer 4).
A meaning that names no frame and slot of the digest is counted as "none", and the number of such answers is
reported (answer 6).

## The launch line (one fresh agent for each brief)

    Read the file /Users/mike/repos/mike/meroitic/data/sources/frames/briefs/<arm>/<pack>_<a|b>.md in full and do
    exactly what it asks: write one JSON line for each code to the answers file it names (the path is relative to
    /Users/mike/repos/mike/meroitic/), then reply in one line as it says. Work alone: open no file but those it
    names, do not search the web, do not spawn agents, and write no file but your answers file.

## The brief

One brief for both arms. It differs in five places, marked `<<...>>`; what stands there in each arm follows the
brief. `<pack>`, `<n>` and `<a|b>` are the agent's pack, the number of its codes and which of the two aligners
it is.

    # Give each code of a pack of Meroitic texts a meaning, or "none"

    Meroitic is written in a script that can be read aloud, but most of its words are not understood. The pack

        /Users/mike/repos/mike/meroitic/data/sources/frames/packs/<pack>.md

    holds royal and temple texts, oracular decrees and long texts of the Meroitic corpus, word by word. Every word
    stands in its place, one word a token. A word is shown either by its reading in English, as a word-by-word map of
    the corpus has it, or by a code (`W012`). You never see how a word is written. The head of the pack explains
    the marks.

    A code stands for one word: the same code is the same word wherever it stands, in this pack and in the others. A
    code may be any kind of word: a noun, a verb, a title, an epithet, an adjective, a particle.

    <<what the aligner is given>>

    **Your task.** Give every code of the pack a meaning in a few English words, or "none".

    - "none" is a full answer. Never guess for the sake of an answer: give a meaning only where the places of the code
      give a reason for it<<what a reason is>>.
    - A code that stands in several places has one meaning: weigh all its places.
    - The pack lists its codes at its end and states their number: <n>. Give one line for each of them, none left out
      and none twice: your file must have exactly <n> lines.

    Write the lines to the file

        data/sources/frames/answers/<arm>/<pack>_<a|b>.jsonl

    (the path is relative to /Users/mike/repos/mike/meroitic/), nothing else in it, one JSON line a code:

        <<the line>>

    - "meaning": a few English words, or "none".
    <<the frame and the slot>>
    - "why": one short sentence: what in the text decides it; for "none" it may be empty.

    Work alone and use only <<what it may use>>. Do not open any other file of the repository, do not search the web,
    do not spawn agents, and write no file but your answers file. You may not look up the inscription: do not try to
    work out which inscription a text is, and do not use what you may know of published translations of Meroitic
    texts.

    When the file is written, count its lines against <n>, then reply in one line: how many codes, and how many of
    them you gave a meaning.

## With the frames (arm `frames`)

`<<what the aligner is given>>`:

    You are also given a digest of frames:

        /Users/mike/repos/mike/meroitic/data/sources/frames/frames_digest.md

    The frames were built from the Egyptian texts of the kings of Kush (8th to 1st century BC) in their editors'
    English, by readers who saw no Meroitic text. A frame is a run of slots in a fixed order that stands in at least
    three of those texts. A frame of the digest has an id (`K3`), a name, where it stands in a text and on which
    monuments; then its slots in order, each with its number, its meaning, the wording of the translation, and
    whether it may be left out or repeated. Read the digest first. Then read each text of the pack against it: where
    the readings, the names and the numbers of a Meroitic text follow a frame, a code that stands in one of the
    frame's slots may have that slot's meaning.

`<<what a reason is>>`, after "give a reason for it":

    : a frame that the words around it follow, with the code in one of its slots

`<<the line>>`:

    {"code": "W012", "meaning": "a few English words, or none", "frame": "K3", "slot": 2, "why": "one short sentence"}

`<<the frame and the slot>>`:

    - "frame" and "slot": the frame the meaning rests on, by its id in the digest, and the number of its slot.
      Every meaning you give rests on one: a meaning without a frame and a slot of the digest counts as "none".
      Give null for both where you give "none".

`<<what it may use>>`: the pack and the digest of frames.

## With the pack alone (arm `plain`)

`<<what the aligner is given>>`:

    You are given the pack alone. Read each text for what the readings, the names, the numbers and the order of
    the words say about the codes among them.

`<<what a reason is>>`: nothing.

`<<the line>>`:

    {"code": "W012", "meaning": "a few English words, or none", "why": "one short sentence"}

`<<the frame and the slot>>`: nothing (the line has no frame and no slot).

`<<what it may use>>`: the pack.
