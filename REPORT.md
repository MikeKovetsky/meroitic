# Meroitic with Opus 5.5: results

Night of 2026-11-08/09, 22:54 to about 01:00 PST, Opus 5.5 subagents. Every number names the run it comes from;
answers are in `runs/answers/`, keys in `runs/keys/`, the task file each run saw in `runs/tasks/` (local-only, as
the tasks embed the corpus: README, Data), the code in `src/` (reviewed: README, Methods 13; checks in `tests/`).

## Did we find anything new?

**We did not decipher anything.** No new reading of Meroitic survived checking (0 of 14 claimed, two partial leads
open). What is new, with the run behind each claim:

1. **The public corpus is mostly copies.** Otten & Anastasopoulos's released file is their name-swap augmentation
   (the paper: 871 example texts and phrases swapped up to 17,257; the repository does not say the file is that
   version): each text or phrase repeated with only a person's name changed (the label `tdxe mlEqErebr qEret ___` appears 198 times,
   once per name). 18,090 lines, 662 distinct texts (about 27 copies each), 442 distinct funerary texts in 306 families; some
   titles are counted about 100 times too often (`src/pool.py`, `src/dedup.py`, `src/collapse.py`,
   `src/clean_v2.py`; `data/discovery/funerary.md` for the families).
2. **303 inscriptions are machine-readable under an open licence, 234 of them missing from the public corpus.**
   Griffith's printed Meroitic type read at
   95.6% sign accuracy against FHN (482 of 504 signs, 12 texts; 99.6% against Griffith's print;
   `data/expansion/printed_type_test.md`); 152 inscriptions transcribed, 86 new, +5% words (`src/expand.py`).
   The test covered cursive type only; the 48 rows in hieroglyphic type were not scored.
   Hand copies: 88.8% on their own (`hand_copy_test.md`), below the bar; 97.7% (639 of 654 signs, four texts)
   once each reading is checked against the words Griffith prints in type in the same book, so the 151 Karanòg
   and Shablûl inscriptions are transcribed too, 148 of them new, +14% words (Day three, below).
   Photographs: almost nothing (`data/discovery/vision.md`).
3. **Scrambled-script blind tests fail on a frontier model.** From a 17-word glossary of letter-swapped Meroitic and
   no texts it matched 35 of 35 meanings by breaking the cipher (`S0_f0`, `S0_f1`); from the scrambled corpus with
   neutral labels it recognised "O Isis, O Osiris" and read the script (`K2_morph`).
4. **A leak-free test, and its result.** Synthetic twin language: 41 and 43 of 52 meanings on two runs, chance about
   2 (`Y_f0`, `Y_f1`, `runs/answers_rep/`). Recall-then-corpus on Rilly's lexicon: 27 of 65 from memory; for the
   rest, 13 of 35 from the corpus on the first guess, 20 within three (`runs/lexique_judge.json`, independent judge,
   leaked items removed).
5. **A calibrated confidence filter.** Every answer at confidence 4–5 was right, 74 of 74 across the tests (46
   synthetic, 7 and 19 recall-then-corpus, 2 corpus after leak removal); about a third at confidence 1–2.
6. **Restoration beats statistics.** On the 62 masks with no parallel anywhere in the task, 30 restored (48%) against
   16 (26%) for an n-gram model, exact McNemar p ≈ 0.001 (`C3_cloze`, `src/cloze_families.py copies`).
7. **Negative results.** No Meroitic–Nubian lexical signal with open word lists beyond the words Rilly's sound laws
   were built from (held-out p = 0.49, `src/cognates_rules.py`); REM 1003 holds nothing checkable against the Roman
   war (as Rilly 2014); no "new" reading survived the adversarial check (`data/discovery/verification.md`).

The night's first answers, kept as run: the model already knows the published vocabulary (35/35 matching from
memory, `M_f0/1`); asked openly it answered 52 of 82 published words (50 right, 1 partly right, 1 wrong) and said
"unknown" to 30 (`F_recall`); a natural experiment on the 17 it could not recall got 13 right on the first guess
and 16 within three (`N_open`, independent judge).

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

1. WEAKENED further on unseen texts (see below). `wi` before a numeral marks a total. FHN II (p. 722) reports that
   Hofmann 1981 found `wi 3348` on REM 1003 to be the sum of the men and women; the Tanyidamani case (`mk lte wi 12`
   after exactly twelve items counted "1") may be new. Check Hintze 1960.
2. OPEN, and confirmed on unseen texts (see below). Rilly published one vocative `-i` after the pair "Isis +
   Osiris" (Rilly 2007 p. 297; Dotawo 7). The extension to "god + epithet" (Osiris never `Soreyi` before an epithet,
   11 texts) may be new, but Isis keeps her `-i` before an epithet in one family. Check Rilly & de Voogt 2012 p. 155
   and Heyler 1964.
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

### Leads 1 and 2 on texts they had never seen

On 2026-11-09, after the leads were written down, 256 texts were typed from the scans of the *Meroitic Newsletter*
(issues 6 to 30, 1971 to 2003); 185 of them are not in the corpus. The readings come from articles in copyright, so
they are kept on the author's machine and are not in this repository. Both leads were then tested on those texts,
with the predictions written first, and a second count was made independently. The two counts gave the same
verdicts (details: `data/discovery/verification.md`, claims 3 and 6).

**Lead 1, `wi` before a numeral marks a total: weaker.**

- The one sum that can be checked fails. On REM 1003 the six counts of men and women add up to 648 (747 at most,
  allowing for one doubtful count), and the number after `wi` is 3348. Griffith 1917 (JEA 4), Heyler's 1971
  transcription (Newsletter 6) and FHN II all print these numbers, so Hofmann's addition rests on readings none of
  them gives. Otten's file of the stela lacks the line with 3348.
- No new text has a whole list before `wi` + numeral, so no new sum could be tested.
- In the accounts from Tabo (REM 1347, Jacquet-Gordon, Newsletter 29) `wi` stands before a numeral on line after
  line, once before a count of 1 (`wi 1`), and once it is written as one word with its noun (`seb[e]wi 270`).
  Rilly's edition of the Obelisk of Meroë (REM 1361, Newsletter 29) also writes `abrwi` as one word before the
  men's 1032(?), and the women's count after it has no `wi`. This fits `wi` as a copula, "X are N" (Hallof 2022,
  for REM 1138), better than "total".
- The Tanyidamani sum stands as arithmetic, but small numbers beside runs of 1s add up by chance about as often:
  the texts with three or more numbers hold 10 such sums, against 8.7 expected when each text's numbers are
  shuffled.

**Lead 2, the vocative at the end of "god + epithet": holds, 9 of 9.**

- In the texts new to the corpus, 9 invocations have the Osiris epithet, all after `Sori` or `aSori` and none after
  `Soreyi`. 12 have the Isis epithet, all after `woS` and none after `woSi`. All 40 cases of `woSi` stand before
  Osiris without an epithet.
- Two texts put `mklX` in the place of Osiris before the epithet (REM 1062, REM 1067), which the lead does not
  cover.
- The count cannot tell a moved vocative from two fixed formulas, one short and one long, each copied whole.

## Corrections found along the way

- Rilly withdrew "arme = Rome" in 2014; the Romans are `Tmey` in REM 1039, and `Arome` is 3rd century.
- The corpus file called the Hamadab stela is REM 1003 (BM EA 1650, the Akinidad stela).
- On the war stela, `kdise` is "each woman", not "sister", and `wi` before a number is not "brother".

## What would move this forward

1. A clean digital corpus (Hallof 2024, REM) with REM numbers, lines and doubtful signs.
2. The model as an analyst whose high-confidence readings go to a specialist, low-confidence ones not.
3. A cognate test with Rilly's sound correspondences over his 2003 thesis appendix (about 200 series).
4. The leads above sent to Claude Rilly, Jochen Hallof, Solange Ashby or Joshua Otten.


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
   (`data/expansion/hand_copy_test.md`). Karanòg was therefore not transcribed that day; it was on the next, by
   another method (Day three, below).
9. **Corpus expansion** (`data/expansion/griffith_*.jsonl`, `src/expand.py`): 152 inscriptions transcribed from
   *Meroitic Inscriptions* I–II and *Meroë*; 29 are partial (left out), 37 were already in the corpus or repeat
   another Griffith text, 86 are new: `data/corpus_v3.jsonl` has 748 texts and 19,066 words (+5%). The duplicate
   test is strict (a short label inside a longer text counts as present), so the gain is a lower bound.
10. **Review:** the review of `src/lexique.py` and `src/expand.py`, stopped partway on Mike's word to push, was
    finished before the repo was shared; `tests/test_lexique.py` checks both files, and none of the numbers above
    changed.

## Day three (2026-11-10): Karanòg, and tests on the Newsletter texts

1. **Karanòg and Shablûl** (`data/expansion/karanog/README.md`, `src/karanog_refs.py`, `src/karanog.py`): Griffith
   prints most words of every inscription a second time in type (a table of names, three indexes and tables of the
   closing formulae: 48 pages, typed by twelve readers, 3,550 entries). Each hand copy was read on its own and then
   checked against its entries. On the four texts FHN prints, fresh readers who could not see FHN reached 639 of
   654 signs (97.7%), and 582 (89.0%) before the check. All 151 inscriptions that have a hand copy are read:
   16,437 signs and 2,775 words. The check changed 2,405 of the 16,759 signs first read (14.4%).
2. **Corpus** (`src/expand.py`): 148 of the 151 are new by the duplicate test, and `data/corpus_v5.jsonl` has 896
   texts and 21,818 words (+14%); `corpus_v3` is unchanged. The three held back (Kar. 63, Kar. 66, Sh. 17) share
   their formulae with an older text and are not copies of it.
3. **The Meroitic Newsletter** (`data/expansion/newsletter_reading.md`, `src/mnl/`): 256 texts typed on 2026-11-09,
   185 of them new, kept locally because the articles are in copyright. 97.6% of signs on clean print, 94% to 97%
   on the 1971 printout. Lined up with other editions of the same inscriptions, 96.2% of 9,571 signs agree; of 42
   differences checked on the scans, 3 were typing errors.
4. **Tests on those texts** (section 5 of the same page): the two leads (above); a held-out grammar test (cutting
   new words into known stems and endings works no better than on made-up words; predictions from pairs of endings
   came true 53 times in about 1,600, where about 9.5 were expected); nine oracular decrees read blind (12 of 14
   published points of structure, 8 of 20 of meaning); Meeks's 1973 word list against Rilly 2003 (41 of 50 "best
   established" meanings unchanged, 8 of 66 doubtful ones).
5. **Review:** four more full reviews, two of the Newsletter tools and two of the Karanòg scripts and rows. Among
   their fixes: a scorer that let extra signs go free (97.7%, not 98.2%), page numbers and footnote marks read as
   inscription numbers, and an editor's "(sic)" counted as two signs.
