# Names cut into parts: what the readers of gate C2 are given

Written on 2026-11-16 at 22:05, with the script (`src/names.py`), before the script was run on the held-back
names and before any reader was started. The rules and the bars are in
[`data/discovery/outside_evidence.md`](../../data/discovery/outside_evidence.md), section 4. `python3 -I
src/names.py packs` writes the packs, once gate C1 has been run: every part that stands in at least five names
under a code, in packs of about 40. The codes are numbered by lot; the known parts and the others are dealt evenly
over the packs by a second draw, apart from the numbering, and a pack lists its codes in their order, so nothing in
it says which are known (the key, `key.json`, stays apart). The review of 2026-11-16 made the deal a draw of its
own: dealt in the order of the codes, the gaps between a pack's numbers would have shown its known codes.
Each pack goes to two readers, who do not see each other's answers; each gets the brief below with the
number of codes of its pack and its own answers file (`data/sources/names/answers/<pack>_<a|b>.jsonl`), and after
it the codes with their numbers. A reader sees no letter of a name or of a part.

## The brief

    # What kind of part is it? <the number of codes> parts of Meroitic personal names, shown by numbers only

    Meroitic is written in a script that can be read aloud, but most of its words are not understood. A script has cut
    the personal names of the Meroitic texts (about 600 names, most of them from epitaphs) into the strings of letters
    that come back from name to name. Each such part stands here under a code. You are not shown its letters, and you
    are not shown any name: only where the part stands and with what. Some of the parts are words or gods' names whose
    meaning is known, and your answers for those will be checked; you are not told which they are.

    The parts were found by a count, not by a grammar: a part is any string of two letters or more that comes back in
    several names. So one part can be a piece of another, and some are only letters that happen to stand together.

    For each code the pack gives, always as a number of different names:

    - **names**: in how many names the part stands;
    - **place**: how many names it begins (first), how many it stands inside (middle), how many it ends (last), and
      how many it is the whole of (a name in which it stands twice can count twice);
    - **with gods**: the gods whose names stand in the same names, apart from it, by the god's English name;
    - **whose names**: in how many names of mothers, of fathers and of the dead (the person an epitaph is for) the
      part stands, as far as the text shows whose name it is; the other names are other people's, or the text does
      not show it;
    - **sites**: where the texts with these names were found;
    - **beside**: the other codes that most often stand right before it or right after it in a name.

    **How names are built in the two naming traditions nearest to these people.** You may lean on this, and on nothing
    else you know or believe about Meroitic.

    - Egyptian names of these centuries are very often a god's name with a short statement about the god or about the
      bearer: that the god gave the child, that the god is content, strong or alive, that the bearer belongs to the
      god or is the god's son, daughter or servant. The god's name can stand first or last; what goes with it is a
      deed, a quality, a kin word or a word for a person. Other Egyptian names are a quality of the bearer alone, a
      kin word, a title, or a thing or an animal.
    - Nubian names, as far as the later Nubian languages show them, are more often a word for a person, a kin word or
      a quality, alone or with a second word after it that says what the bearer is like, and names that call the
      bearer the servant of a god or a saint.
    - In both traditions short endings that only mark a word as a name, or as a man's or a woman's name, are common.

    For each code give one JSON line, in the order of this file, in the file `<answers>`, nothing else in it:

        {"code": "P017", "kind": "<one of the kinds below>", "meaning": "<a few English words, or none>", "why": "<one short sentence>"}

    - "kind" is one of: "god" (a god's name), "quality" (what the bearer or the god is like), "thing or person" (a
      noun that is none of the other kinds), "deed" (a verb: something done), "kin word" (a word for a relative),
      "title" (an office or a rank), "ending" (no meaning of its own: it marks a name, or a man's or a woman's name),
      "unclear".
    - "meaning" is what you think the part means, in a few English words, only if the numbers give you a reason to say
      it; otherwise "none". A kind without a meaning is a full answer.
    - **"unclear" and "none" are full answers,** and for most parts they are the right ones. A guess that the numbers
      do not carry counts against you.
    - Use only this file. Do not open any other file of the repository, do not search the web, do not spawn agents,
      and write no file but your answers file.

    This pack lists <the number of codes> codes: your file must have <the number of codes> lines, one for each code. When it is written, count its lines
    against that number, then reply in one line: how many codes, and how many of each kind.

## A code in a pack

    ## P017

    - names: 12
    - place: first 9, middle 2, last 1, whole name 0
    - with gods: Amun 3, Isis 1
    - whose names: mothers 4, fathers 1, the dead 3
    - sites: Karanog 6, site not known 3, Shablul 2
    - beside: P003 4, P041 2, P120 2

The numbers of this example are made up.
