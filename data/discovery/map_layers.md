# The map as it stands: the base and its layers

Status on 2026-11-16: six layers are laid. Figures: `map_figures.json`. Script: `src/themap.py`. Checks:
`tests/test_themap.py`.

**In short.** What six steps resolved is now part of the map, as layers over the analysts' map:
[the recurring open spellings](recurring_words.md) (385 places),
[the rare spellings](rare_spellings.md) that hang on an entry of the lexicon (109 and 159 places),
[the spellings the lexicon does not hold](unnamed_spellings.md) that are names or pieces (118 places),
[the rare spellings whose entry Millet or Lipiński gives a meaning or calls a name](leftover_parts.md) (17 places) and
[the rare spellings whose unnamed part is an ending or a known word](leftover_parts_2.md) (32 places),
each place with its source or its reason. With them, 4,185 of the 7,099 running words that need a meaning are
translated (59.0%, from 50.1%), and 160 of about 1,284 distinct words (12.5%). Every one of these meanings is a
scholar's: the project has still added none of its own. The analysts' map itself is not changed, and the studies that were run on it keep their
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
| With the layers | 4,185 of 7,099 | 59.0% | 840 of 2,798 | 30.0% | 59.9% |

- "Of" counts the words that need a meaning: no name, no numeral, no lost sign. A word is translated when the
  map gives it a meaning or a grammatical function.
- A spelling has the level it has most often.
- The last column is the measure of [the coverage pages](v6_readers.md): names and numerals count as translated,
  and the share is of all 10,290 running words.
- The plain lookup is the lexicon of 2003 looked up word by word, with none of the project's analysts or
  corrections. It is the status table's "Before us" for the first two columns.

**The north star.** On the map with its layers, 160 of about 1,284 distinct words, 12.5% (between 11.8% and
15.6%), have a meaning: 127 by the lexicon of 2003 and 33 by a later source (Rilly's work of 2016 and 2021:
9 through the layer `recurring`, 20 through `rare_later` and 2 through `leftover`; Lipiński 2011: 2 through
`rare_millet`). Before the project it was the same, since all 160 meanings were published before it. How the words are counted is on
[the page of the distinct words](distinct_words.md). A word counts when a layer lays one of its places as a
translated word for the reason "stated". The layers `rare_sure` and `unnamed` add none: the words of the first
had a meaning, and the second gives none.

The count of distinct words adds, to the 377 words of the dictionary in use, an estimate of how many of the stems the
map cannot name are words of their own. That page drew it from a sample of 240 of the 1,107 stems the base could
not name. The layers make 41 of those stems names, so 1,066 are left. A place that a layer translates keeps its
stem in this count, because the count reads the parts of a word and a layer changes only its level and meaning:
the 5 pieces of translated words that `unnamed` lays are such places. While the layers took at most 2% of
the stems, the estimate was carried as it was drawn (the north star with the first three layers, 11.9%, used it).
The layer `unnamed` takes more, so the estimate is made again from the 230 sampled stems that are still unnamed, by
that page's own rule: about 907 of the 1,066 are words of their own (between 646 and 979). The rule was written
down before the layer was counted ([unnamed_spellings.md](unnamed_spellings.md), section 9). The reporting rules
had named a new sample instead; asked whether to keep the recount or draw a new sample, Mike answered on
2026-11-16 at 14:49: "why do you need my approval to recount? this is obvious you need to recount to show the up
to date result?". So that step of the north star, from 11.9% to 12.1%, is a correction of the count of words:
no word got a meaning by it. The fifth and the sixth layer, `rare_millet` and `leftover`, take no stem out of the
unnamed ones, and the 2 words each gives a meaning bring the north star from 12.1% to 12.3% and then to 12.5%.
The script stops if a layer adds a stem the sample was not drawn from.

Each share on this page is divided from its counts and rounded once. With four layers, 156 of 1,284 is 12.1495%;
the figures file holds the share rounded to four places, 0.1215, and rounding that again gives 12.2%, the figure
first given for the north star with the layer `unnamed`.

## 4. The layers

| Layer | Laid | Places | Stated by a later source | Form of a word the lexicon calls sure | Piece of a word or name | Name | Running words translated after it | From |
|---|---|---|---|---|---|---|---|---|
| `recurring` | 2026-11-16 | 385 | 273 | 0 | 66 | 46 | 53.9% | [recurring_words.md](recurring_words.md) |
| `rare_sure` | 2026-11-16 | 109 | 0 | 103 | 6 | 0 | 55.3% | [rare_spellings.md](rare_spellings.md) |
| `rare_later` | 2026-11-16 | 159 | 141 | 0 | 18 | 0 | 57.4% | [rare_spellings.md](rare_spellings.md) |
| `unnamed` | 2026-11-16 | 118 | 0 | 0 | 7 | 111 | 58.4% | [unnamed_spellings.md](unnamed_spellings.md) |
| `rare_millet` | 2026-11-16 | 17 | 14 | 0 | 1 | 2 | 58.5% | [leftover_parts.md](leftover_parts.md) |
| `leftover` | 2026-11-16 | 32 | 18 | 14 | 0 | 0 | 59.0% | [leftover_parts_2.md](leftover_parts_2.md) |

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

**`unnamed`** (step G3). The open spellings that stand in one or two texts and hang on no entry of the lexicon.
Two checkers judged each place from the place alone, with places of known answer mixed in. The layer holds the
places both call a name (111) and the pieces whose whole word both name and the map holds (7).
5 places become translated words and 113 names; all 118 were open. These names are names by their place in
the text, not by a source.

**`rare_millet`** (the follow-up to G2 and G4). The entries of G4 that Rilly's later work gives no meaning and for
which Millet 2005 or Lipiński 2011 states one. Two readers read each statement and said what it gives: a name, a
meaning in full, or a meaning that leaves a Meroitic word as it is. Two checkers judged each place. The layer
holds the places where both find the word the source speaks of and the map names every part of the spelling (14:
10 of entries the lexicon files as place names, 4 of the two words Lipiński gives a meaning in full), 2 places of
two entries that both readers say Millet calls a personal name, and 1 piece of a name the map holds.
4 places become translated words and 13 names; all 17 were open. The first reading of the other part of that
step, the unnamed parts of spellings, is not taken and lays nothing; the second is the layer `leftover`.

**`leftover`** (the second reading of the leftover parts). The 96 places of steps G2 and G4 that `rare_sure` and
`rare_later` left open: both checkers of those steps recognised the word, but the map leaves a part of the spelling
unnamed. Two fresh checkers said what the unnamed part is, with places of known answer mixed in. The layer holds
the places where both call it an ending, or a known word of the lexicon and the same one, and no other stem of the
spelling is without a meaning: 14 forms of a word the lexicon calls sure and 18 places of a word for which Rilly
states a meaning.
27 places become translated words and 5 names; all 32 were open. A place both checkers call a name is not laid.

## 5. What keeps the base, and why

Three pages count from the map and were named in the step as pages to rebuild. They are not counted again, and
Mike waived that part of the step on 2026-11-16 at 13:52 ("Yes, waive it."):

1. **[The coverage of the clean corpus](v6_readers.md)** (52.7%) reports one run of the analysts on 2026-11-12,
   before and after. Its measure on the map as it stands is the last column of section 3: 59.9%.
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
- **The 432 stated places of `recurring`, `rare_later` and `leftover` rest on Rilly's readings of 2016 and 2021.**
  Step G5 set each of Rilly's 66 later meanings, those behind these places among them, beside what other scholars
  say: 33 are stated by another scholar too (15 with a dissent), 13 are disputed and 20 rest on Rilly alone
  ([second_scholar_later.md](second_scholar_later.md)). The layers do not change with it. The 14 stated places of
  `rare_millet` rest on Millet 2005 (10, all of them names of places) and on Lipiński 2011 (4).
- **The north star counts entries of the lexicon.** Several of the entries that `rare_later` gives a meaning are,
  by the same later source, forms or variants of one another or of known words
  ([the page of the rare spellings](rare_spellings.md), section 9).
- **"Translated" at a place means two checkers agreed that the source's statement applies there;** in `unnamed`,
  that both called the place a name, or a piece of the same whole word. Their agreement beyond chance (Cohen's
  kappa) was 0.91 for `recurring`, 0.70 for `rare_sure`, 0.93 for `rare_later`, and 0.80 and 0.79 for the two
  readings behind `unnamed`, and 0.97 for `rare_millet` and 0.66 for `leftover`, against a bar of 0.6; the places
  they did not agree on are in no layer.
- **The spellings count is coarse:** a spelling translated in most of its places counts as translated.

## 7. Reproduce

```
python3 -I src/themap.py          # needs the local map, lexicon and layers; writes map_figures.json
python3 -I tests/test_themap.py   # the method on made-up words; the figures, this page and the status skill
```

A new layer is one more entry of `LAYERS` in `src/themap.py` and one more row of section 4. The lines of the two
layers of the rare spellings are written by `python3 -I src/rare.py layers`, those of `unnamed` by
`python3 -I src/unnamed.py layer`, those of `rare_millet` by `python3 -I src/leftover.py layer`, those of
`leftover` by `python3 -I src/leftover.py layer-again`.

Review (2026-11-16): an independent reviewer (Opus 5.5, a fresh agent that saw the change and the task, not the
reasoning) checked this step with G2 and G4 and changed:

1. The coverage measure of section 5: 58.2% on the map with the three layers of that review (55.6% was the map
   with the first layer alone).
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

Review of the fourth layer (2026-11-16, with steps G3 and G5): an independent reviewer (Opus 5.5, a fresh agent
that saw the change and the task, not the reasoning) changed:

1. The north star with four layers is 12.1%, not 12.2%: 156 of 1,284 is 12.1495%, and 12.2% came from rounding the
   rounded share 0.1215 again. `src/themap.py` now divides each share it prints from its counts (`star_pct`), and
   the checks hold the pages to that.
2. `src/themap.py` stops on any unnamed stem the sample was not drawn from, as this page, the README and the
   reporting skill said; before, it only compared the number of stems, so a layer that added one stem and took
   another out would have passed.
3. The layers make 41 stems names, not "names or pieces": a piece laid as part of a translated word keeps its stem
   in the count (section 3). Each layer's figures now give the stems left after it (`north_star.unnamed_stems`).
4. Mike's answer on the recount is recorded in his words (section 3), and section 6 gives the result of G5.

Review of the fifth and sixth layers (2026-11-16, with the leftover parts and G6): an independent reviewer (Opus
5.5, a fresh agent that saw the change and the task, not the reasoning) changed:

1. Section 4 called the places of `leftover` "the 96 places of `rare_sure` and `rare_later`"; they are places of
   steps G2 and G4 that those two layers left open.
2. Section 6 no longer reads as if step G5 had judged the meanings behind the stated places of `rare_millet`: G5
   judged Rilly's 66 later meanings, not Millet's or Lipiński's. A check holds every stated place of the layers to
   the source that section names.
