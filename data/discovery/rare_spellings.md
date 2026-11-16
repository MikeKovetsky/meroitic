# The open spellings that stand in one or two texts (steps G4 and G2)

Status on 2026-11-16: started. The items are built and the rules below are set; no reader has answered yet.
Working script (local until the runs are counted): `data/sources/rare/run.py`, which reuses the steps of
`src/recurring.py` in a folder of its own.

## 1. What was asked

Mike, 2026-11-16: "Yes, start G1 and G4, queue G2". The steps are those of `NEXT_STEPS.md`, section G, which he
had asked for with "define next steps" (2026-11-15):

- G4: "The later sources on the rest of the lexicon's open entries ... The literature pass, the two readers and
  the place pass of point 18 again."
- G2: "The spellings under a sure stem ... The place pass of point 18 again: two checkers say for each place
  whether it holds the lexicon's word."

Requirements, one line each:

| | Requirement | State |
|---|---|---|
| R1 | G4: for the entries the lexicon of 2003 holds without an accepted meaning and whose open spellings stand in one or two texts, find what the later sources state, and check it place by place. | In work. |
| R2 | G2: for the open spellings filed under a stem or ending the lexicon calls sure, have two checkers say for each place whether it holds the lexicon's word. | Queued behind G4. |
| R3 | The rules of the recurring open words (point 18): two readers on every judgment that is counted, each bar committed before its readers are started, counts that follow from a figures file, nothing called a meaning of ours. | The bars of both steps are in this page, committed before any reader was started. |

## 2. The items

The map of `corpus_v6` leaves 2,203 spellings without an accepted meaning that stand in one or two texts. By the
entry the map files a spelling under:

| Kind | Step | Entries | Spellings | Running words |
|---|---|---|---|---|
| a. A stem or ending the lexicon calls established or probable | G2 | 116 | 312 | 366 |
| b. An entry the lexicon holds without an accepted meaning | G4 | 323 | 784 | 1,033 |
| c. No entry of the lexicon | G3, not started | | 1,107 | |

One running word of kind b more than `NEXT_STEPS.md` counted (1,032): that count left out the places the
recurring-words results would resolve, and this one takes every place of the spellings.

## 3. G4: what the later sources state (rules set before any reader is started)

**The literature pass.** 27 readers, one for each batch of twelve entries, collect every statement about each
entry from the sources in hand (the same sources and the same brief as for the recurring open words, with a new
introduction: `runs/prompts/RARE_literature.md`). Each batch file gives, for each entry, a line of leads: the
pages of Rilly 2016 and of Rilly 2021 on which a script finds the headword. A statement counts only when a script
finds its quote in the file named. This step has one reader a batch, as it had for the recurring open words: a
reader can miss a statement, and the leads are there to make that rarer for the two later works.

**The classes**, by rule, as before:

- A: a statement of Rilly 2016 or 2021 with the stance "accepts" or "probable";
- B: no such statement, and the reader calls the spelling a piece of another word or of a name in some or all
  uses;
- C: the rest.

**Class A read twice.** Two readers, each on its own, read the statements of each class A entry in their place.
The bar: an entry counts as "stated by a later source" only when both give the stance "accepts" or "probable" for
the same source and their meanings share a content word.

**The place pass.** Every place of the class A and class B entries goes to two checkers, each on its own, with
the four cases of the recurring open words (stated, piece, open, unclear). The bar:

1. A place is **stated** only when both checkers say so, and only for an entry that passed the bar of class A.
2. A place is a **piece** only when both say so and name the same whole word.
3. A place is **open** or **unclear** only when both say so; every other place is **not agreed** and stays as the
   map has it.
4. If Cohen's kappa of the two checkers over all the places is under 0.6, or a place is not answered by both,
   nothing is taken: the brief is corrected and fresh checkers read again.
5. A checker's file counts only for the places of its own pack.

The places of class C entries are not judged: no source states anything for them, and they stay open.

## 4. G2: the spellings under a sure stem (rules set before any checker is started)

Every place of the 312 spellings goes to two checkers, each on its own. A pack gives, for each entry, the
lexicon's line (its meaning and its status) and every place with five words on each side and the map's reading
of each. The four cases are those of the place pass, with one changed:

- **stated**: the spelling here is a form of the lexicon's word that the header names, in a use its meaning
  covers (that word with endings, in a variant writing, or in a compound);
- **piece**, **open**, **unclear**: as above.

The bar is that of section 3's place pass, points 2 to 5, with this first point: a place is **stated** only when
both checkers say so. A stated place takes the lexicon's meaning of that entry.

## 5. What will be counted

- Running words translated and distinct spellings translated: a stated place is translated; a piece takes the
  level of the whole word both checkers name, where the map reads that word.
- Distinct words translated (the north star): an entry of G4 with one stated place or more is a dictionary word
  that a later source gives a meaning, as in the count of distinct words. G2 does not move it: its entries are
  translated already.
- In every count the meanings are the sources', not the project's.

The briefs the checkers of both place passes are given, and their launch line, are in
[`runs/prompts/RARE_places.md`](../../runs/prompts/RARE_places.md), committed before any of them was started.

What the runs cannot show: the readers and checkers are one model, so their agreement shows that a judgment can
be repeated, not that it is right; they see five words on each side, not the stone.
