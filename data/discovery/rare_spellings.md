# The open spellings that stand in one or two texts (steps G4 and G2)

Status on 2026-11-16: both steps are counted, and what they resolve is laid in the map as two layers
([map_layers.md](map_layers.md)). Figures: `rare_spellings_figures.json`. Script: `src/rare.py`, which reuses the
steps of `src/recurring.py` in a folder of its own. Checks: `tests/test_rare.py`. Sections 2 to 5 are the rules as
they were set before the agents of each step were started; the additions made on the way say when they were made.
The results are in sections 6 to 10.

**In short.** Two checkers judged 1,061 places of rare spellings that hang on an entry of the lexicon. 268 of
them now carry a meaning or a name in the map: 109 where the spelling is a form of a word the lexicon calls sure
(G2), 159 where Rilly's work of 2016 or 2021 gives the entry a meaning or the "word" is a piece of a word the map
holds (G4). The running words translated go from 53.9% to 57.4%, and 20 more words of the lexicon have a meaning
(136 to 156 of about 1,307, 10.4% to 11.9%). Every one of these meanings is a scholar's. Both checkers recognised
the word at 182 more places that are not laid, because the map leaves a part of the spelling unnamed.

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
| R1 | G4: for the entries the lexicon of 2003 holds without an accepted meaning and whose open spellings stand in one or two texts, find what the later sources state, and check it place by place. | MET: section 7. |
| R2 | G2: for the open spellings filed under a stem or ending the lexicon calls sure, have two checkers say for each place whether it holds the lexicon's word. | MET: section 6. |
| R3 | The rules of the recurring open words (point 18): two readers on every judgment that is counted, each bar committed before its readers are started, counts that follow from a figures file, nothing called a meaning of ours. | MET, with what section 9 says: the bars of both steps were committed before their agents were started; two of the four additions of section 5 were made for G2 after its checkers had answered, one of them after its count, and both only lower its figure. No meaning here is the project's. |

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

**One rule added on 2026-11-16 at 13:20,** after G2's checkers had answered and before their answers were
counted, and before any checker of G4's places was started. 26 of G2's 116 entries and 36 of G4's 323 are endings
or particles: the map files a spelling under such an entry when it finds no stem of the lexicon in it. For these
entries "stated" says only that the ending in the spelling is that ending; the stem beside it still has no
meaning. So:

- A stated place of an entry that is an ending or a particle counts as translated only where the map names every
  part of the spelling, so that the ending or particle is written as a word of its own (as `wi` is among the
  recurring words). Where a part of the spelling is unnamed, the place stays open and is counted apart, as
  "ending recognised".
- For the entries that are stems the rule above stands. The count of the stated places where the map names every
  part of the spelling is given beside it, as the stricter figure.

This is stricter than the rule above: it can take translated words away and cannot add one.

**A second rule, added on 2026-11-16 at 13:22,** before any checker of G4's places was started, and after G2's
places had been counted (so for G2 it is a correction made with the count in view; it only lowers G2's figure).
G2's count showed what "stated" covers when the map leaves a part of the spelling unnamed: of the 68 such
places of stem entries, about half join the lexicon's word to a name or to an unknown word (a god's name
inside a personal name, a title after an unknown noun). The word as a whole is then not translated. So, for
both steps:

- **What is laid in the map.** A stated place is laid as translated only where the map names every part of the
  spelling with an entry of the lexicon. A stated place with an unnamed part is counted apart, as "the word
  recognised, a part of the spelling unnamed", and stays as the map has it.
- **Names.** Where the entry of a stated place is a name by the lexicon (a god, a person, a place), the place is
  laid as a name, which needs no meaning, not as a translated word.
- **Both figures are reported:** the stated places by the rule of sections 3 and 4, and those laid in the map.

**Two points more, added on 2026-11-16 at 13:26,** before G4's places were counted (two of its 32 checkers
were still at work):

- **Every stem must have a meaning.** A stated place is laid as translated only where each stem among the
  spelling's parts has one: the lexicon calls it established or probable, a later source states it (it passed
  the bar of class A here or among the recurring words), or it is a name. An ending the lexicon is not sure of
  does not keep a word out.
- **The north star counts what is laid.** An entry of G4 is a dictionary word that a later source gives a
  meaning only when one of its stated places is laid in the map as translated. The entries with a stated place
  but none laid are given beside it.

**G4's first reading of the places is not taken** (noted on 2026-11-16 at 13:27, when it was counted). The 32
checkers agreed well (Cohen's kappa 0.93), but one of the 695 places has one checker's answer only: a checker's
file has 40 lines for a pack of 41 places. By point 4 of the bar nothing is taken. The brief's last line is
corrected to name the number of places in the pack and to ask the checker to count its lines against it
([`runs/prompts/RARE_places.md`](../../runs/prompts/RARE_places.md)), and 32 fresh checkers read the same 16 packs
again. The first reading is kept and reported beside the second.

The recurring open words had no such condition: 41 of their 273 stated places have a part the map leaves
unnamed (forms of four words in fixed phrases). They stay as that study's rule, set beforehand, had them.

The briefs the checkers of both place passes are given, and their launch line, are in
[`runs/prompts/RARE_places.md`](../../runs/prompts/RARE_places.md), committed before any of them was started.

What the runs cannot show: the readers and checkers are one model, so their agreement shows that a judgment can
be repeated, not that it is right; they see five words on each side, not the stone.

## 6. G2: the result

16 checkers, two for each of 8 packs, answered all 366 places. Their Cohen's kappa is 0.70 (bar 0.6), so the pass
is taken.

| Both checkers say the spelling is | Places |
|---|---|
| the word the header names (stated) | 245 |
| a piece of another word or of a name | 28 |
| a word of its own that stays open | 18 |
| unclear | 24 |
| not agreed | 51 |

- **Of the 245 stated places, 103 are laid.** 170 stand under a stem: the map names every part of the spelling at
  102 of them and leaves a part unnamed at 68. 75 stand under an ending or a particle: 1 with every part
  named, 74 with a part unnamed (the ending is recognised, the stem beside it has no meaning).
- **What the laid places become:** 80 a meaning, 22 a name (the entry is a god, a person or a place), 1 a grammar
  word.
- **Pieces:** of the 28 places both call a piece, 6 are laid, because the whole word they name is translated or
  named in the map; for the other 22 it is open or no spelling of the map.
- **By entry:** 89 of the 116 entries have a stated place; 43 have one laid as a translated word, 14 only as a
  name, 32 none.
- G2 gives no word of the dictionary a meaning: its entries had one already.

## 7. G4: the result

**The literature pass.** 27 readers collected 1,659 statements about the 323 entries; a script found every quote in
the file named. By the rule, 60 entries are of class A (Rilly states a meaning in 2016 or 2021), 104 of class B
(a reader calls the spelling a piece) and 159 of class C (nothing to check: they stay open).

**Class A read twice.** For 57 of the 60 entries both readers find the meaning stated firmly, by the same source, in
words that share a content word: 49 by Rilly 2021, 8 by Rilly 2016; 41 are stems and 16 endings or
particles. 3 are not stated firmly and count as open.

**The place pass**, on the 695 places of the 164 entries of class A and B. The first reading is not taken: its
kappa was 0.93, but one place had one checker's answer only (section 5). The second reading, by 32 fresh
checkers on the same packs, has every place answered by both and a kappa of 0.93 (bar 0.6); it is the one
that counts.

| Both checkers say the spelling is | First reading (not taken) | Second reading |
|---|---|---|
| the word the later source speaks of (stated) | 188 | 181 |
| a piece of another word or of a name | 105 | 113 |
| a word of its own that stays open | 320 | 327 |
| unclear | 45 | 35 |
| not agreed | 36 | 39 |
| answered by one checker only | 1 | 0 |

- **Of the 181 stated places, 141 are laid:** 132 under a stem and 9 under an ending or a particle, where
  the map names every part of the spelling. Not laid: 27 under a stem and 12 under an ending with a part unnamed, and
  1 where another stem of the spelling has no meaning.
- **What the laid places become:** 125 a meaning, 9 a grammar word, 7 a name.
- **Pieces:** of the 113 places both call a piece, 18 are laid; for 54 the whole word is no spelling of the map,
  for 41 it is open there.
- **By entry:** 40 entries have a stated place; 29 have one laid as a translated word, 3 only as a name, 8
  none. The other 17 entries that passed class A have no place that both checkers call stated.

**The words of the dictionary that get a meaning.** 25 of the entries laid as translated words are words of the
dictionary (no name, no ending); 20 of them are new to the map, and these move the north star. The meanings are
Rilly's, given here in a few words of ours:

| Entry | Meaning | Source | Places laid | New to the map |
|---|---|---|---|---|
| `Aqedise` | the Moon-god | Rilly 2021, p. 67 | 1 | yes |
| `abrse` | each man | Rilly 2021, p. 31 | 1 | yes |
| `anese` | donkey | Rilly 2021, p. 15 | 4 | yes |
| `aqebese` | their, a variant spelling | Rilly 2021, p. 11 | 2 | yes |
| `asr` | meat, animal | Rilly 2016, p. 11 | 3 | yes |
| `bqo` | to take control | Rilly 2021, p. 38 | 3 | no, the recurring words gave it |
| `erk` | I took | Rilly 2021, p. 37 | 2 | yes |
| `kb` | to seize | Rilly 2021, p. 39 | 5 | yes |
| `kdke` | Candace, the queen-mother | Rilly 2016, p. 11 | 2 | yes |
| `mreke` | horse | Rilly 2021, p. 31 | 2 | yes |
| `pl (2)` | to give, offer | Rilly 2021, p. 82 | 1 | yes |
| `plete` | to give, offer | Rilly 2021, p. 82 | 2 | yes |
| `pqr` | prince | Rilly 2016, p. 10 | 2 | no, the recurring words gave it |
| `pso` | causative prefix before 'drink' | Rilly 2021, p. 12 | 1 | yes |
| `pẖo` | causative prefix before 'present' | Rilly 2021, p. 42 | 1 | yes |
| `sr` | meat, animal | Rilly 2016, p. 11 | 3 | yes |
| `tk (1)` | to seize | Rilly 2021, p. 31 | 1 | yes |
| `tk (3)` | to seize | Rilly 2021, p. 24 | 1 | yes |
| `tlt` | talent, a weight | Rilly 2021, p. 8 | 1 | yes |
| `tḫ (1)` | to present a meal | Rilly 2021, p. 45 | 25 | no, the recurring words gave it |
| `wese` | his, her | Rilly 2021, p. 41 | 1 | yes |
| `yel` | to give | Rilly 2021, p. 47 | 1 | yes |
| `yerki` | I took | Rilly 2021, p. 37 | 2 | yes |
| `ḫr` | to eat | Rilly 2021, p. 42 | 41 | no, the recurring words gave it |
| `ẖol` | to present, serve | Rilly 2021, p. 44 | 17 | no, the recurring words gave it |

## 8. The map after both steps

| | Running words translated | Share | Distinct spellings translated | Share |
|---|---|---|---|---|
| Before (the recurring words laid) | 3,916 of 7,265 | 53.9% | 626 of 2,944 | 21.3% |
| With G2's layer | 4,002 of 7,242 | 55.3% | 700 of 2,926 | 23.9% |
| With G4's layer too | 4,149 of 7,230 | 57.4% | 814 of 2,917 | 27.9% |

The north star: 156 of about 1,307 distinct words have a meaning, 11.9% (between 11.3% and 14.9%); before the
project the same, because each meaning was published before it. The counts are those of
[map_layers.md](map_layers.md), from `map_figures.json`. The spellings move more than the running words because
each of these spellings stands once or twice.

## 9. What this does not show

- **No meaning is the project's own.** G2 applies the lexicon of 2003, G4 Rilly's work of 2016 and 2021. No second
  scholar confirms the meanings of G4.
- **The 20 new words are 20 entries of the lexicon, not 20 words of the language.** As the two readers read him,
  Rilly now takes several as forms or variants of one another or of known words: `sr` and `asr`; `tk (1)` and
  `tk (3)`; `erk` and `yerki`; `pl (2)` and `plete`; `pso` and `pẖo` as a prefix before a verb; `abrse` as a noun
  with an ending; `aqebese` and `wese` as variant spellings of possessives; `yel` as a form of a verb the lexicon
  has. The north star counts entries, as it did for the 127 of the lexicon; counted as words, the gain is smaller.
- **182 places were recognised and not laid.** Both checkers found the lexicon's word or the later source's there,
  but the map leaves a part of the spelling unnamed. They wait for a step that names those parts (G3).
- **The rule for what is laid was tightened on the way** (section 5). For G4 every addition was written down before
  its places were counted. For G2 two were made after its checkers had answered, one after its count; they only
  lower its figure (245 stated places by the first rule, 103 laid).
- **G4's place pass was read twice.** The first reading missed the bar on one unanswered place and is not taken;
  its numbers stand beside the second's in section 7.
- **G2's checkers agree less** (kappa 0.70) than those of G4 (0.93) or of the recurring words (0.91): 51 of
  366 places are not agreed and stay open.
- **159 entries of G4 were not judged** (class C): the readers found no statement of Rilly's later work and no
  sign of a piece. One reader a batch collected the statements, so a statement can have been missed.
- The readers and checkers are one model: their agreement shows that a judgment can be repeated, not that it is
  right; they see five words on each side, not the stone.

## 10. Cost, and how to run it again

119 agents (Opus, each a fresh one), 13,892,589 subagent tokens, from the task notifications: G4's literature pass
5,713,974 (27 readers), class A read twice 1,287,161 (12), its places 2,784,088 and 2,782,223 (two
readings, 32 checkers each); G2's places 1,325,143 (16). From the first reader to the last count: 12:59 to
13:33 on 2026-11-16.

```
python3 -I src/rare.py g4 items          # then batches, quotes, verify-packs, verify, place-packs, places
python3 -I src/rare.py g4 place-packs2   # the second reading; then places2
python3 -I src/rare.py g2 items          # then place-packs, places
python3 -I src/rare.py layers            # the lines for the map; then python3 -I src/themap.py
python3 -I src/rare.py public            # rare_spellings_figures.json
python3 -I tests/test_rare.py
```

The commands need the local files (the map, the lexicon, the text layers of the sources, the agents' answers). The
packs go to agents by hand, one fresh agent a pack, with the lines of `runs/prompts/RARE_*.md`.
