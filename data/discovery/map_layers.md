# The map as it stands: the base and its layers

Status on 2026-11-16: three layers are laid. Figures: `map_figures.json`. Script: `src/themap.py`. Checks:
`tests/test_themap.py`.

**In short.** What three steps resolved is now part of the map, as layers over the analysts' map:
[the recurring open spellings](recurring_words.md) (385 places) and
[the rare spellings](rare_spellings.md) that hang on an entry of the lexicon (109 and 159 places), each place with
its source. With them, 4,149 of the 7,230 running words that need a meaning are translated (57.4%, from 50.1%),
and 156 of about 1,307 distinct words (11.9%). Every one of these meanings is a scholar's: the project has still
added none of its own. The analysts' map itself is not changed, and the studies that were run on it keep their
numbers.

## 1. What was asked

Mike, in his words: 2026-11-13, "our goal is to decipher the meaning of all words"; 2026-11-15, "define next
steps"; 2026-11-16, "Yes, start G1 and G4, queue G2". G1 is the first step of section G of
[`NEXT_STEPS.md`](../../NEXT_STEPS.md), as it stood when he said yes:

> **G1. Put the overlay into the map.** The 385 places of point 18 (273 stated by Rilly in 2016 or 2021, 66
> pieces of a word or name the map reads, 46 places of seven names) become a layer of the map's build, each with
> its source. Done when the map's own figure is 53.9%, the pages that count from the map (coverage, the
> translations' baseline, the lexicon's statuses) are rebuilt from the same file, and the checks and the review
> pass. No agents but the review.

Requirements, one line each:

| | Requirement | State |
|---|---|---|
| R1 | "The 385 places of point 18 [...] become a layer of the map's build, each with its source." | MET: sections 2 and 4. `src/themap.py` lays the layer's 385 lines over the base; each changed word carries its source, the reason and the level it had. |
| R2 | "Done when the map's own figure is 53.9%" | MET: section 4. With the layer `recurring` the script's count is 3,916 of 7,265, and it equals the count the recurring-words study made itself (`tests/test_themap.py`). The two layers laid after it the same day move it on (section 3). |
| R3 | "the pages that count from the map (coverage, the translations' baseline, the lexicon's statuses) are rebuilt from the same file" | NOT MET as written, on purpose, and waived by Mike on 2026-11-16 at 13:52, asked whether the three pages could keep their numbers and point here: "Yes, waive it." Section 5 gives the reasons. The figure of the coverage measure is counted from the map with its layers (section 3) and the three pages point here; their own numbers are not counted again. |
| R4 | "the checks and the review pass" | MET: the checks pass, and the review of section 7 left nothing open after its fixes. |
| R5 | "No agents but the review." | MET: no agent was run for this step. |

## 2. What a layer is

The base is the analysts' map of `corpus_v6`: for each of the 548 inscriptions, every running word with its
level, its meaning and the lexicon entries it is built on. It stays as the analysts left it.

A layer is a file of lines, one for each running word it changes: the text, the word's number in it, its
spelling, the new level and meaning, the reason, and the source. The script lays the layers over the base in
their order, each time it runs; nothing is written back.

1. **A layer only resolves.** A line gives a word a meaning, a grammatical function, or says it is a name or a
   numeral. A layer cannot make a word open.
2. **Four reasons are allowed:** a later source states the word's meaning at that place ("stated"); the word is
   a form of a word whose meaning the lexicon calls sure ("form"); it is a piece of a word or name that the map
   holds ("piece"); it is a name by the sources ("name").
3. **A layer that does not fit stops the build.** A line that names a text, a place or a spelling the map does
   not have there, two lines for one place, a place that an earlier layer changed, a level it had that is not the
   map's, or a level or reason outside the lists, ends the run with the line named.
4. **Each changed word says where it comes from:** the layer, the source, the reason, and the level it had.
5. **The lines are local.** They hold meanings taken from the sources, so the layers' files are kept out of the
   repository like the map itself. What is public is this page and the counts.

## 3. The map, counted

| | Running words translated | Share | Distinct spellings translated | Share | Translated or named, of all words |
|---|---|---|---|---|---|
| Plain lookup of the lexicon | 2,816 of 7,847 | 35.9% | 325 of 3,189 | 10.2% | 39.3% |
| The base | 3,676 of 7,331 | 50.1% | 598 of 2,955 | 20.2% | 52.7% |
| With the layers | 4,149 of 7,230 | 57.4% | 814 of 2,917 | 27.9% | 58.2% |

- "Of" counts the words that need a meaning: no name, no numeral, no lost sign. A word is translated when the
  map gives it a meaning or a grammatical function.
- A spelling has the level it has most often.
- The last column is the measure of [the coverage pages](v6_readers.md): names and numerals count as translated,
  and the share is of all 10,290 running words.
- The plain lookup is the lexicon of 2003 looked up word by word, with none of the project's analysts or
  corrections. It is the status table's "Before us" for the first two columns.

**The north star.** On the map with its layers, 156 of about 1,307 distinct words, 11.9% (between 11.3% and
14.9%), have a meaning: 127 by the lexicon of 2003 and 29 by a later source (Rilly's work of 2016 and 2021:
9 through the layer `recurring`, 20 through `rare_later`). Before the project it was the same, since all 156
meanings were published before it. How the words are counted is on
[the page of the distinct words](distinct_words.md). A word counts when a layer lays one of its places as a
translated word for the reason "stated"; the layer `rare_sure` adds none, because its words had a meaning.

The count of distinct words is carried over from that page. It rests on a sample of the 1,107 stems the base
could not name. The layers make 2 of them names, so 1,105 are left; the estimate (about 930 of them are words)
is kept as it was drawn, which changes no figure here at one decimal. The script stops if the layers ever take
more than 2% of those stems, or add any: a new sample is then due.

## 4. The layers

| Layer | Laid | Places | Stated by a later source | Form of a word the lexicon calls sure | Piece of a word or name | Name | Running words translated after it | From |
|---|---|---|---|---|---|---|---|---|
| `recurring` | 2026-11-16 | 385 | 273 | 0 | 66 | 46 | 53.9% | [recurring_words.md](recurring_words.md) |
| `rare_sure` | 2026-11-16 | 109 | 0 | 103 | 6 | 0 | 55.3% | [rare_spellings.md](rare_spellings.md) |
| `rare_later` | 2026-11-16 | 159 | 141 | 0 | 18 | 0 | 57.4% | [rare_spellings.md](rare_spellings.md) |

**`recurring`.** Two checkers judged every place of the 154 open spellings that stand in three or more texts.
The layer holds the places where both agreed that a meaning Rilly states in 2016 or 2021 applies (273), that
the "word" is a piece of a word or name the map holds (66), or that it is one of seven names (46).

- 307 places become a meaning, 77 a name, 1 a grammatical function.
- 79 of its 385 places were translated or named in the base already (26 with a meaning, 42 as a grammar word, 11
  as a name): the layer gives them the later reading. The other 306 were open.
- So 240 running words more are translated, and 66 more are names, which need no meaning: 7,331 words that need
  one become 7,265.
- By distinct spellings the gain is smaller (598 to 626), because these are few spellings in many places.

**`rare_sure`** (step G2). The open spellings that stand in one or two texts and that the map files under a
stem or an ending the lexicon calls established or probable. Two checkers judged each place; the layer holds the
places where both call the spelling a form of that word and the map names every part of the spelling, each stem
among them with a meaning (103), and the pieces of a word the map holds (6). 86 places become translated words and
23 names; all 109 were open.

**`rare_later`** (step G4). The same kind of spellings under an entry the lexicon holds without an accepted
meaning. The layer holds the places where both checkers find the word for which Rilly states a meaning in 2016
or 2021 and the map names every part of the spelling, each stem among them with a meaning (141), and the pieces of
a word the map holds (18). 147 places become translated words and 12 names; all 159 were open.

Both layers leave out the places where the checkers recognise the word but the map leaves a part of the spelling
unnamed, or another stem in it has no meaning; [the page of the rare spellings](rare_spellings.md) counts them.

## 5. What keeps the base, and why

Three pages count from the map and were named in the step as pages to rebuild. They are not counted again, and
Mike waived that part of the step on 2026-11-16 at 13:52 ("Yes, waive it."):

1. **[The coverage of the clean corpus](v6_readers.md)** (52.7%) reports one run of the analysts on 2026-11-12,
   before and after. Its measure on the map as it stands is the last column of section 3: 58.2%.
2. **[The lexicon's statuses](lexicon.md)** rest on judges who compared what scholars say about each entry behind
   a translated word. The layer puts entries behind translated words that those judges never saw. Counting the
   page again would need new judges.
3. **[The translations' baseline](f4_rounds.md)** (58.5%) is a score two judges gave on held texts, and it is the
   "Before us" of the status table's last row. It cannot be recomputed without judges, the held texts are spent,
   and a "Before us" changes only on Mike's word.

Each of the three pages now points here for the map as it stands. The other dated studies (the check against
Millet and FHN III, the sample behind the count of distinct words, the recurring words themselves) also keep the
base they were run on. What is counted from now on, and the steps that follow, read the map with its layers.

## 6. What this does not show

- **No meaning here is the project's own.** A layer applies what scholars have published. The row "Our own
  meanings" of the status table stays at 0.
- **The 414 stated places rest on one scholar.** They are Rilly's readings of 2016 and 2021; no second scholar
  confirms them (step G5).
- **The north star counts entries of the lexicon.** Several of the entries that `rare_later` gives a meaning are,
  by the same later source, forms or variants of one another or of known words
  ([the page of the rare spellings](rare_spellings.md), section 9).
- **"Translated" at a place means two checkers agreed that the source's statement applies there.** Their
  agreement beyond chance (Cohen's kappa) was 0.91 for `recurring`, 0.70 for `rare_sure` and 0.93 for
  `rare_later`, against a bar of 0.6; the places they did not agree on are in no layer.
- **The spellings count is coarse:** a spelling translated in most of its places counts as translated.

## 7. Reproduce

```
python3 -I src/themap.py          # needs the local map, lexicon and layers; writes map_figures.json
python3 -I tests/test_themap.py   # the method on made-up words; the figures, this page and the status skill
```

A new layer is one more entry of `LAYERS` in `src/themap.py` and one more row of section 4. The lines of the two
layers of the rare spellings are written by `python3 -I src/rare.py layers`.

Review (2026-11-16): an independent reviewer (Opus 5.5, a fresh agent that saw the change and the task, not the
reasoning) checked this step with G2 and G4 and changed:

1. The coverage measure of section 5: 58.2% on the map as it stands (55.6% was the map with the first layer alone).
2. `src/themap.py` stops on a line whose former level is not the map's, since the figures count what the layers
   moved from it.
3. One rule for a word of the dictionary that a layer gives a meaning (`given()`), used by the north star and by
   the page of the rare spellings, which had a rule of its own.
4. Mike's waiver of R3 is recorded here and in the summaries, and the cut is said wherever the step is told.
5. On [the page of the rare spellings](rare_spellings.md) and in the summaries, counts and times corrected: the
   pieces among the places laid, the one place kept out for a stem without a meaning, the additions made after
   G2's checkers had answered, the entries of class C. `src/rare.py` was shown to write the run's packs and results
   again byte for byte; the agents' launch lines and the times of each step's rules, launches and answers are
   recorded, with checks.
