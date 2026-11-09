# Meroitic overnight: what Opus 5.5 can and can't do

Night of 2026-11-08/09, 22:54 to about 01:00 PST, Opus 5.5 subagents. Every number names the run it comes from;
answers are in `runs/answers/`, keys in `runs/keys/`, the task file each run saw in `runs/tasks/`, the code in `src/`
(reviewed: `review-fix`, full tier, CLEAN at `7404ee8`, with 15 tests in `tests/test_harness.py`).

## Answer first

1. **Opus 5.5 already knows the published Meroitic vocabulary.** Matching 35 accepted words to their 35 meanings,
   it scored 35/35 from memory alone (`M_f0`, `M_f1`), and 35/35 with the corpus (`R_f0`, `R_f1`). Asked openly,
   with no options, it answered 52 of 82 published words (50 right; 1 partly right, `beloloke` "an official title"
   for "priest (a rank)"; 1 wrong, `yireqe` "east" for "south") and said "unknown" to 30 (`F_recall`).
2. **So a blind test on real Meroitic is impossible.** A letter-swap re-spelling hides nothing: given a 17-word
   glossary and no texts, it broke the cipher and scored 35/35 (`S0_f0`, `S0_f1`). With only the scrambled corpus,
   no meanings and neutral line ids, it recognised the opening `ryuq uyatsq` as Wos-i Sorey-i, "O Isis, O Osiris",
   and read the script from there (`K2_morph`, which says so).
3. **On a language it can't know, it infers meaning from context.** On a synthetic corpus of the same size and
   style (1,003 texts, 16k words, invented vocabulary and endings), it matched 41 of 52 usable test words where
   chance is about 2; all 24 answers at confidence 4–5 were right (`Y_f0`, `Y_f1`, `src/synth.py score`; 4 of the
   56 original items dropped by the review because the corpus doesn't show them). On the same language's grammar,
   blind, it found all 8 invented endings and every formula slot; it named 2 functions right, 4 partly (vocative,
   imperative and determiner only as a second reading or a hedged guess, genitive as "at/of"), and got 2 wrong
   (plural, copula) (`YK_morph`, `runs/yk_morph_scored.json`).
4. **The texts fill gaps in its memory.** For the 17 published words it could not recall, reading the corpus took
   it to the published meaning on the first guess for 13 and within three guesses for 16 (`N_open`, judged by an
   independent agent in `runs/natural_open_judge.json`; my own looser call in `runs/natural_open_scored.json` gave
   14, the difference being "booty" for "plunder").
5. **It restores lost words better than an n-gram restorer, also where nothing can be copied.** Of 120 masked words
   in 60 held-out inscriptions it restored 84 on the first guess; an n-gram restorer counting the same texts got 35
   (exact McNemar p ≈ 3×10⁻¹³). On the 62 masks with no parallel in the task (no run of 12+ letters around the word,
   spaces and case ignored, occurs anywhere else in it), it restored 30 (48%) against 16 (26%), p ≈ 0.001
   (`C3_cloze`, `src/cloze_families.py copies`). The task let it use what it knows about the language, which
   includes the published vocabulary (item 1).
6. **About 15 new, checkable leads for specialists**, each labelled after a literature search
   (`data/discovery/`). None is a decipherment.

## The corpus

- Otten & Anastasopoulos's public corpus (ALP 2025) has 18,090 lines, but each text repeats with person names
  swapped from two pools (178 private, 11 royal; `src/pool.py`). Undoing that, masking names as NAME/RNAME and
  removing the narratives' second copies leaves 662 texts and about 18,100 words (`src/dedup.py`,
  `src/collapse.py`, `src/clean_v2.py`). `C2_cloze`, `N_open`, `K2_morph` and `C3_cloze` ran on the corpus before
  that last step and before starred words were kept whole: 665 texts, about 19,700 words
  (`data/corpus_v2_c3_snapshot.jsonl`). The funerary study counts 442 distinct funerary texts in 306 families.
- Three blind runs found padding my cleanup had missed (multi-word names, name tails such as `mokelowi`), and two
  restoration runs won by exploiting it. Those runs are reported as void.

## Tests

| Test | Run | Result | Reading |
|---|---|---|---|
| Matching, memory only | `M_f0/1` | 35/35 (p = 1.6e-16, 2.8e-15) | memory |
| Matching, real corpus | `R_f0/1` | 35/35 | memory |
| Matching, scrambled corpus | `S_f0/1` | 35/35 | not blind: the task files carried inscription names; runs said they decoded Meroitic |
| Matching, scrambled, no corpus | `S0_f0/1` | 35/35 | cipher broken from the glossary |
| Open recall, 82 words | `F_recall` | 50 right, 1 partial, 1 wrong, 30 unknown | memory |
| Natural experiment, 17 unrecalled words | `N_open` | 13/17 first guess, 16/17 top three (independent judge) | mostly clean |
| Synthetic language, matching | `Y_f0/1` | 41/52; confidence 4–5: 24/24 | clean |
| Synthetic language, grammar | `YK_morph` | 8/8 endings found; functions 3 right, 2 partly, 3 wrong | clean |
| Grammar, scrambled real corpus | `K_morph`, `K2_morph` | `K2_morph`: of 26 published grammar items, 14 right, 6 partly, 6 missed (`runs/k2_morph_scored.json`) | recognised Meroitic |
| Restoration v1, v2 | `C_cloze`, `C2_cloze` | 91/97, 82/88 vs n-gram 40/88 | void: copied from leftover padding |
| Restoration v3, 60 held-out families | `C3_cloze` | 84/120 vs n-gram 35/120; no parallel: 30/62 vs 16/62 | mostly clean: the task allowed what it knows of Meroitic |
| Nubian-family similarity | `src/cognates.py` | p = 0.004 with Rilly's reconstructions, 0.12 without | inconclusive: the reconstructions are partly circular |

### Natural experiment, item by item

| Word | Published meaning | First guess from the corpus | |
|---|---|---|---|
| kdite | sister | sister | right |
| mkdi | goddess | goddess | right |
| pXrs | Faras | Faras (Pakhoras) | right |
| tebwe | Abaton | the Abaton (Bigeh) | right |
| tbo | two | two, both | right |
| yireqw | south | south | right |
| xlbi | bull, ox | bull | right |
| mte | child | child | right |
| perite | agent | agent (official title) | right |
| kelw | and, also | also, likewise | right |
| are | take, receive | take, receive | right |
| asr | meat, animal | cattle, livestock | right |
| tkk | plunder | booty, goods (2nd: plunder) | top three (judge); right (my call) |
| tre | offer | give, offer | right |
| ar | boy, son | take, seize (2nd: boy) | top three |
| SSor | scribe | temple official (2nd: scribe) | top three |
| ns | sacrifice | each, every | wrong |

## Leads for specialists

From `data/discovery/philae.md` (14 items: 1 established, 6 published, 7 new), `funerary.md` (30: 8, 19, 3) and
`hamadab.md`. "New" means no prior proposal turned up in the searches listed there; Rilly 2007, Hintze 1979 and the
printed REM were not searchable.

1. NEW. The Faras stela REM 0129 gives the same title chain, in the same order, as the envoy Sasan in the Demotic
   graffito Ph. 416: `qoreñ`, `kroro`, "great envoy to Rome".
2. NEW. Bekemete's label REM 0098, "begotten by a general of the water", settles Ph. 417: the title is his father's.
3. NEW. `wi` before a numeral marks a total (Tanyidamani: `mk lte wi 12` after twelve items counted "1").
4. NEW. The closing totals 1,626 and 1,032 on REM 1003 count animals (`asr`), not people.
5. NEW. `plSn` ("high priest", Millet) may be Egyptian pꜣ mr-šn, the lesonis.
6. NEW. With an epithet, the vocative `-i` moves to the end of the god's phrase (Osiris is `Sori`, never `Soreyi`,
   in all 11 such texts).
7. NEW. `penn` is a counted time unit in datelines (numbers up to 34), not "day"; three runs reached this
   separately.
8. Published, supported here: `tebwe` is the Abaton; `ste` can name a man ("tutor").
9. Negative: REM 1003 has nothing checkable against the Roman war, as Rilly 2014 says (the war is in REM 1039).

## Corrections found along the way

- Rilly withdrew "arme = Rome" in 2014; the Romans are `Tmey` in REM 1039, and `Arome` is 3rd century.
- The corpus file called the Hamadab stela is REM 1003 (BM EA 1650, the Akinidad stela).
- On the war stela, `kdise` is "each woman", not "sister", and `wi` before a number is not "brother".

## What would move this forward

1. A clean digital corpus (Hallof 2024, REM) with REM numbers, lines and doubtful signs.
2. The model as an analyst whose high-confidence readings go to a specialist, low-confidence ones not.
3. A cognate test with Rilly's sound correspondences over his 2003 thesis appendix (about 200 series).
4. The leads above sent to Claude Rilly, Stefan Hallof, Henriette Ashby or Joshua Otten.
