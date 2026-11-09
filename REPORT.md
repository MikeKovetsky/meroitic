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
   style (1,003 texts, 16k words, invented vocabulary and endings), it matched 41 of 52 usable test words (43 on a second independent run, `runs/answers_rep/`) where
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
6. **Its "new" findings did not survive an adversarial check:** of 7 ideas the discovery runs called new, 2 were
   already published and 5 were weakened; two partial extensions remain open (`data/discovery/verification.md`).
   None is a decipherment.

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
| Synthetic language, grammar | `YK_morph` | 8/8 endings found; functions 2 right, 4 partly, 2 wrong | clean |
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

## Leads for specialists, after an adversarial check

The discovery runs (`data/discovery/philae.md`, `funerary.md`, `hamadab.md`) labelled 7 ideas NEW after their
searches. A separate run then tried to prove each wrong, with harder searches in English, French and German, the FHN
commentary and Millet's 1968 glossary (`data/discovery/verification.md`). None survived as a clean new finding:

1. OPEN, partly. `wi` before a numeral marks a total. Hofmann 1981 (via FHN II p. 722) already found that
   `wi 3348` on REM 1003 sums the men and women; the Tanyidamani case (`mk lte wi 12` after exactly twelve items
   counted "1") may be new. Check Hintze 1960.
2. OPEN, partly. Rilly published one vocative `-i` after the pair "Isis + Osiris" (Rilly 2007 p. 297; Dotawo 7).
   The extension to "god + epithet" (Osiris never `Soreyi` before an epithet, 11 texts) may be new, but Isis keeps
   her `-i` before an epithet in one family. Check Rilly & de Voogt 2012 p. 155 and Heyler 1964.
3. WEAKENED. REM 0129 and Sasan's titles (Ph. 416): a word masked as a name is the title `womnis`, so REM 0129
   lists five or more titles; FHN III p. 1008 already pairs the two; the order is ordinary rank order.
4. WEAKENED. Bekemete's father as "general of the water": Griffith 1911 (Karanòg p. 21) already set Ph. 417 beside
   REM 0098; Török 2009 p. 464 reportedly gives the father the title.
5. WEAKENED. 1,626 and 1,032 as animal counts: REM 1041 counts 1,032 men (`abr wi 1032`).
6. ALREADY PUBLISHED. `plSn` from pꜣ mr-šn, "the lesonis": FHN III p. 973 and Ashby 2016.
7. ALREADY PUBLISHED. `penn` as a numbered year: Millet 1968 reads `penn 34` "regnal year 34". Three runs reached
   it separately, which shows the pattern is plain in the texts.
8. Published, supported here: `tebwe` is the Abaton; `ste` can name a man ("tutor").
9. Negative: REM 1003 has nothing checkable against the Roman war, as Rilly 2014 says (the war is in REM 1039).

The lesson: the model finds real patterns, but where the key literature is print-only (Millet 1968, Hofmann 1981,
Rilly 2007, FHN commentary) it cannot tell a rediscovery from a discovery.

## Corrections found along the way

- Rilly withdrew "arme = Rome" in 2014; the Romans are `Tmey` in REM 1039, and `Arome` is 3rd century.
- The corpus file called the Hamadab stela is REM 1003 (BM EA 1650, the Akinidad stela).
- On the war stela, `kdise` is "each woman", not "sister", and `wi` before a number is not "brother".

## What would move this forward

1. A clean digital corpus (Hallof 2024, REM) with REM numbers, lines and doubtful signs.
2. The model as an analyst whose high-confidence readings go to a specialist, low-confidence ones not.
3. A cognate test with Rilly's sound correspondences over his 2003 thesis appendix (about 200 series).
4. The leads above sent to Claude Rilly, Stefan Hallof, Henriette Ashby or Joshua Otten.


## Waves 2 and 3 (2026-11-09 morning)

After "are you giving up?", four more lines of attack, then data.

1. **Calibrated readings of unknown words** (`runs/unknown/`, three independent runs, 29 words): 93 readings, 70 at
   confidence 3 or below. Readings agreed at 4+ by two runs are all structural: the Osiris and Isis epithets
   (`wetrri`, `wetNyiNqeli`, meaning unknown), `tmNteleb` "those in TmN", `mlolo` "was good", `brtoye` a name. The
   corpus shows what kind of word something is (title, kin term, place, counted item), almost never what it means.
2. **Sound-law cognate engine** (`src/cognates_rules.py`, reviewed; `data/discovery/cognates_rules.md`): on all
   accepted words p = 0.017, but that comes from the words Rilly built the rules from (p = 0.0005); on held-out
   words p = 0.49. No candidate cognates were earned.
3. **Reading inscriptions from photographs** (`data/discovery/vision.md`): 0 of about 80 signs on the worn Hamadab
   stela; on a clean British Museum stela, 3 of about 30 words. It can't check readings on stones.
4. **Tanyidamani stela REM 1044** (`data/discovery/tanyidamani.md`): an interlinear and a plain-English outline
   (titles, two campaigns, offerings to twelve gods, people and animals given to Amun). Its 7 NEW claims: 1 already
   published, 6 weakened (`data/discovery/verification.md`). With the first round, 0 of 14 "new" claims survived.
5. **Rilly's 2003 lexicon** (HAL tel-04793700) read from its 304 scanned pages by six agents: 937 entries
   (`data/rilly2003/`, private).
6. **Meaning test at scale against Rilly** (`src/lexique.py`, judged independently in `runs/lexique_judge.json`):
   - recall from memory: 27 of 65 SAME (as judged 28 of 68); all 19 answers at confidence 4–5 SAME;
   - from the corpus, for the words recall missed: first guess 13 of 35, any of three 20 of 35, after removing six
     targets the glossary gave away and three non-test items (as judged: 20 of 44 and 28 of 44);
   - `python3 -I src/lexique.py judged` prints both versions with the judge's borderline ranges.
7. **Calibration across all tests:** every answer given at confidence 4–5 was right: 46 of 46 on the synthetic
   language (two runs), 7 of 7 and 19 of 19 in recall-then-corpus tests, 2 of 2 corrected corpus answers.
8. **Reading Griffith's printed type** (`data/expansion/printed_type_test.md`): 95.6% sign accuracy against FHN on 12
   texts (482 of 504), 99.6% against what Griffith printed. Griffith's hand copies (Karanòg, about 150 epitaphs)
   fail the bar: 581 of 654 signs (88.8%; 91.1% on signs the copy shows clearly) on the four texts FHN prints, with
   the errors in names, rare titles and closing formulas, and most of them not flagged "?" by the reader
   (`data/expansion/hand_copy_test.md`). Karanòg was therefore not transcribed.
9. **Corpus expansion** (`data/expansion/griffith_*.jsonl`, `src/expand.py`): 152 inscriptions transcribed from
   *Meroitic Inscriptions* I–II and *Meroë*; 29 are partial (left out), 37 were already in the corpus or repeat
   another Griffith text, 86 are new: `data/corpus_v3.jsonl` has 748 texts and 19,066 words (+5%). The duplicate
   test is strict (a short label inside a longer text counts as present), so the gain is a lower bound.
10. **Review:** the review of `src/lexique.py` and `src/expand.py` was stopped partway on Mike's word to push; its
    edits are included and pass the tests.
