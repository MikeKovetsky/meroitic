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
2. **303 inscriptions are machine-readable under an open licence, 237 of them missing from the public corpus.**
   Griffith's printed Meroitic type read at
   95.6% sign accuracy against FHN (482 of 504 signs, 12 texts; 99.6% against Griffith's print;
   `data/expansion/printed_type_test.md`); 152 inscriptions transcribed, 86 new, +5% words (`src/expand.py`).
   The test covered cursive type only; the 48 rows in hieroglyphic type were not scored.
   Hand copies: 88.8% on their own (`hand_copy_test.md`), below the bar; 97.7% (639 of 654 signs, four texts)
   once each reading is checked against the words Griffith prints in type in the same book, so the 151 Karanòg
   and Shablûl inscriptions are transcribed too, all of them new, +15% words (Day three, below).
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
   war (as Rilly 2014); no "new" reading survived the adversarial check (`data/discovery/verification.md`). A
   search by sound alone for Egyptian sources gives nothing above chance for the pieces without a meaning, and
   finds 4 of 14 known borrowed titles, nouns and verbs (Day four, afternoon, below).

8. **About 62% of the running words can be translated today, word by word.** After four corrections, 13,613 of
   the 21,977 words of `corpus_v5` are a name, a number or a word that Rilly's 2003 lexicon holds as established
   or probable (61.6% with near-copies counted once); every legible word is translated in 107 of 605 texts. As
   first built the map gave 13,292 words (60.5%) and 82 texts; the difference is words it counted wrongly, not
   meanings found (Day four, below; `data/discovery/coverage.md`).
9. **A search by letters finds the entry of a hidden spelling variant 77% of the time, and its test still missed
   the bar.** 187 of 242 variants listed in Rilly's lexicon come back to their own entry as the single best
   match, but only 105 (43%, the bar was half) with a match that stands out from made-up words: no word of three
   or four letters can. On the pieces without a meaning the letters alone decide nothing; two blind checkers
   confirmed 48 of the 105 matches under the bar, 29 of them new, and 26 would move 59 running words of the
   coverage map, to 60.7%, or 54 without two whose packs showed a word with their own letters glossed (Day four,
   evening, below; `data/discovery/variants.md`).

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
(issues 6 to 30, 1971 to 2003); 185 of them were counted as not in the corpus (188 since a correction to the
duplicate check on 2026-11-10; the tests here ran on the 185). The readings come from articles in copyright, so
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
   16,440 signs and 2,911 words. The check changed 2,405 of the 16,759 signs first read (14.4%).
2. **Corpus** (`src/expand.py`): all 151 are new by the duplicate test, and `data/corpus_v5.jsonl` has 899
   texts and 21,977 words (+15%); `corpus_v3` is unchanged. The test at first held back three short texts
   (Kar. 63, Kar. 66, Sh. 17) that share their closing formulae with an older text; it now leaves the letter
   groups of the formulae out of the comparison for these rows.
3. **A second reader** (the same evening; section 6 of the Karanòg page): eleven of the 53 pages, the seven most
   damaged, three drawn at random and the page of Kar. 77, were read again by a reader who saw nothing of the
   first reading. After the check the two agree on 3,180 of 3,254 signs (97.7%; 97.0% on the damaged pages, 99.1%
   on the random ones; 86.0% from the hand copies alone). Weighted by the pages each group stands for, that is
   98.8% for all 53 pages, the 46 ordinary ones resting on three pages. The second reader then settled the 56
   differing places against the copy and the type: 26 for the first reading, 17 for its own, 2 for neither, 11
   left open. That changed 26 signs of the rows (0.8%). On Kar. 77 both readers differ from FHN at the same six
   places, at five of them with what Griffith prints: two readers who agree have recovered Griffith's reading,
   not necessarily the stone.
4. **Uniform rows** (section 5 of the same page): the closing formulae are divided into words as Griffith's
   formula tables divide them (144 word boundaries added in 77 rows, 7 gaps closed in 4), but for a few rows where
   the stone has a divider or the typed table differs in a sign, and the title `slẖs` has one spelling.
5. **The Meroitic Newsletter** (`data/expansion/newsletter_reading.md`, `src/mnl/`): 256 texts typed on 2026-11-09,
   188 of them new (185 as first counted), kept locally because the articles are in copyright. 97.6% of signs on
   clean print, 94% to 97% on the 1971 printout. Lined up with other editions of the same inscriptions, 96.2% of
   9,571 signs agree; of 42 differences checked on the scans, 3 were typing errors.
6. **Tests on those texts** (section 5 of the same page): the two leads (above); a held-out grammar test (cutting
   new words into known stems and endings works no better than on made-up words; predictions from pairs of endings
   came true 53 times in about 1,600, where about 9.5 were expected); nine oracular decrees read blind (12 of 14
   published points of structure, 8 of 20 of meaning); Meeks's 1973 word list against Rilly 2003 (41 of 50 "best
   established" meanings unchanged, 8 of 66 doubtful ones).
7. **Review:** five more full reviews, two of the Newsletter tools and three of the Karanòg scripts and rows. Among
   their fixes: a scorer that let extra signs go free (97.7%, not 98.2%), page numbers and footnote marks read as
   inscription numbers, an editor's "(sic)" counted as two signs, and formula words that the uniform rows still
   divided two ways (Griffith's one word left parted at a gap, and pairs he prints apart for five to nineteen
   inscriptions left run together).

## Day four (2026-11-11): how much can be translated

`src/coverage.py`, `tests/test_coverage.py`; the page is [`data/discovery/coverage.md`](data/discovery/coverage.md).

1. **The figure.** Every word of the 899 texts was glossed from Rilly's 2003 lexicon. 13,292 of 21,977 words
   (60.5%) are translated: 6,955 have an accepted meaning, 1,968 an accepted function, 4,106 are names and 263
   numbers. 3,704 (16.9%) have a proposal only, 2,099 (9.6%) are known by their kind only, 2,620 (11.9%) are
   unknown and 262 have a lost sign. With near-copies counted once (608 texts, 8,786 words) it is 59.9%.
2. **By part:** the older corpus 59.3%, Karanòg and Shablûl 74.1%, Griffith's other volumes 41.9%. By different
   words instead of running words: 1,105 of 3,160 (35.0%).
3. **Texts:** of the 608 texts, 605 have a word that is not lost; every such word is translated in 82 of them and
   one piece is missing in 124 more; the median text has 68.8% of its legible words translated.
4. **How:** the lookup alone translates 11,374 words (51.8%) and leaves 1,887 different words. Nineteen analysts
   cut and classified those (2.63 million subagent tokens), which adds 1,918 words. No answer failed the script's
   check that the parts spell the word and the entries exist.
5. **Two analysts** on 230 of the most frequent leftover words (the 52 left last, `Sklte` and `mokelowi` among
   them, had one): the same level for 194 (84%), the same on translated or not for 218 (95%). Of the 66 the first
   called translated the second did so for 58.
6. **What blocks:** 1,336 pieces have no accepted meaning: 302 headwords of the lexicon (126 with a proposal, 157
   known by kind, 19 with neither) and 1,034 letters that no entry explains (777 unknown pieces, 257 words cut into
   known parts by an analyst who was not sure of the cut); 670 have a kind. The verbs of the benedictions lead:
   `ḫr` stands in 116 texts and alone blocks 11, `ẖol` in 70. 96 pieces stand in five texts or more.
7. **Checked against a later source:** of the 39 words Rilly's 2016 overview lists as translated, the typed lexicon
   holds 34 at an accepted level; counting the other four it has (`pqr`, `wide`, `nbr`, `sr`) as accepted would
   move 186 words, to 61.3%.
8. **Limits:** word by word is not understanding: verb endings are mostly unexplained. No specialist has checked
   a line, the analysts are one model family, and the lexicon is the state of 2003.

## Day four, afternoon (2026-11-11): Egyptian sources by sound

`src/egyptian.py`, `tests/test_egyptian.py`; the page is [`data/discovery/egyptian.md`](data/discovery/egyptian.md).

1. **The question:** can a scorer that knows only letters find the Egyptian word behind a Meroitic one in two open
   word lists (5,660 Demotic lemmata of the TLA's sentences, 11,283 entries of the Comprehensive Coptic Lexicon)?
2. **The test on known loans, each hidden in turn.** The key is 35 accepted borrowings of Rilly's lexicon (14
   titles, nouns and verbs, 21 names); the source of 24 stands in the lists. Titles, nouns and verbs: the true
   source is among the five best candidates for 4 of 14 when titles and nouns are searched together (`plsn`,
   `ḫrpḫe`, `pelmos`, `kisri`; 2 among the words of their own kind alone) and among the ten best for 6; the bar
   set before the run was most of the 14. Names: among the three best for all 10 that have a source among the
   Demotic names of their kind, first for 7.
3. **Against chance:** the best match of a known title or noun beats the best matches of 95% of made-up words for
   2 of 11 loans (wide pool) and for none (narrow pool). A match in sound does not tell a loan from a look-alike.
4. **The unknown pieces:** of 383 searched, 22 and 26 beat the 5% bar (narrow and wide pool) where 19 are expected
   by chance, and chance alone gives as many or more 28% and 7% of the time. None passes the bar for 383 tries,
   but with 300 made-up words no chance is below 1 in 301, so that bar could pass a piece only with six others at
   that floor.
5. **The check:** two blind checkers read the 33 best matches with 12 unmarked decoys and agreed on all 45: no new
   source, every decoy rejected, five matches are forms of loans already known (`prSn`, `petmoS`, `pertese`,
   `stol`, `menote`) and one (`aribet`) is the Meroitic title `arebetke` as a Philae graffito spells it.
6. **By-products:** at least 16 pieces of the coverage map's list are forms of words the lexicon already links to
   Egyptian (11 spelled like one, 5 more that the checkers recognised); the Demotic list holds graffiti of
   Meroitic officials (`qrnyꜣ` for `qorene`, `ꜣrbtgꜥyꜣ` for `arebetke`), and the search puts both first among the
   titles.
7. **Not done:** the oracular decrees (neither list holds Egyptian texts of that kind) and the people named in
   both the graffiti and the Meroitic texts (the Demotic file is single sentences, and the older corpus masks
   names).
8. **Limits:** the source entries of the 24 loans were picked by hand; the Demotic list is the vocabulary of a
   sample of sentences, not a dictionary; the key, its readers and the checkers go back to one lexicon and one
   model family. Cost: about 0.62 million subagent tokens before the review (364,923 for the key's two readers,
   249,072 for the two checkers, about 8,000 for a web check).
9. **With the vowels compared too** (added the same day, on the Coptic entries only, since Demotic writes no
   vowels): the true source is among the five best of 7,139 Coptic nouns for 7 of the 13 loans that have a Coptic
   source, against 4 by consonants in the same pool; nine loans move up and three down. Of the 14 titles, nouns
   and verbs of the bar, 6 have their source among the five best with vowels (4 by consonants; 8 in the five best
   of both searches together, which is ten candidates a loan). Against chance nothing changes: the best match of
   a known loan beats 95% of made-up words for 1 of 11, and of 241 pieces without a meaning 13 beat the 5% bar,
   where the made-up words predict 12 and the rate of 64 native words in each piece's pool predicts 8. For seven
   of the 13 the first checkers had already been shown the best match; two more blind checkers read the other six
   with six decoys and said no to all 12. A first run of this item left out the e of the sign ne (18 pieces under
   the bar, a checkers' pass of 15 items, all "no"); the review found it, and the numbers here are after the fix.
   Cost: 139,936 subagent tokens for the first run's checkers, 508,760 for the review in two rounds and 133,211
   for the corrected run's checkers: about 0.78 million, against about 0.5 million estimated.

## Day four, evening (2026-11-11): spellings of known words among the unknown pieces

`src/variants.py`, `tests/test_variants.py`; the page is [`data/discovery/variants.md`](data/discovery/variants.md).

1. **The question:** which of the 1,336 pieces without an accepted meaning are another spelling of a word of
   Rilly's lexicon, or such a word with an ending? The pool is the lexicon's 688 words (655 different headword
   spellings, 1,067 letter strings with the listed variants), small enough for a search by letters.
2. **The model counts and assumes nothing.** It starts flat and counts the alternations on the 307 variants the
   lexicon lists: an `e` left out or added 133 times, one vowel for another 73 times, the vowel at the start
   coming or going 42 times; among consonants `l` for `n` and `t` for `s` five times each, `t` for `d`, `q` for
   `w` and `k` for `ḫ` four times each. No listed variant has `r` for `l`.
3. **The bar, set before the first run:** at least two thirds of the hidden variants come back to their own entry
   as the single best match, and at least half do so with a match that at most 5% of made-up words of the same
   length equal.
4. **The test missed it.** Of 242 hidden variants, 187 (77%) come back as the single best match, so the first
   part is reached, and 232 (96%) are among the three best. But 105 (43%) stand out as well, so the second part
   is not reached. By length: none of 93 with three or four letters, 59 of 92 with five or six, 46 of 57 with
   seven or more. Of 1,000 made-up words of three letters, 350 are a spelling of the lexicon letter for letter.
   With the entry's other variants hidden too, 178 come back (74%).
5. **When a match stands out it is right:** 105 times in 118, and 12 of the other 13 went to an entry that the
   lexicon itself links with the right one, or tied with it (counted after the run).
6. **The unknown pieces:** 1,210 searched (126 are too short or hold a lost sign). 70 are headwords that the
   lexicon links with their best match itself. Of the other 1,140, 82 beat the 5% bar where the made-up words
   predict 57 (chance gives as many 0.08% of the time); none passes the bar for 1,140 tries.
7. **A second yardstick takes the excess away.** Of 76 words with an accepted meaning that the lexicon links
   with nothing, 8 beat the same bar (6 of the 24 with seven letters or more): different words that share a part,
   such as two royal names in `-demni`. At their rate the 1,140 pieces would give about 104.
8. **The examples that started the step:** `pertese` beats the bar as `perite` with `-se`; `prSn` and `petmoS`
   have the right entry as their best match and do not beat the bar (`r` and `t` for `l` are in no listed
   variant); `amn` has three letters.
9. **The check.** All 105 matches under the bar (the 82 and the 23 among the 70) went to two blind checkers,
   in three packs, with 24 listed variants whose answer is known: 12 with the right entry among the candidates
   and 12 decoys with it taken out. The checkers gave the same verdict on 116 of the 129 items. Both said "the
   same word" and named one candidate for 48 matches: 19 of the 23 pairs that the lexicon links itself, and 29
   new ones. For two of the new ones (`mXeyot`, `yetmetl`) the pack showed a word that holds the piece's letters,
   which the map cuts otherwise and counts as translated, with its gloss, and for `yetmetl` both checkers cite
   it; without them 46 are confirmed.
10. **How far to trust it.** Both checkers named the right entry for 6 of the 12 controls (7 and 8 each), and
    both accepted a look-alike for 1 of the 12 decoys (`amnpte` as `Amnp` with `-te`). A confirmation is fairly
    safe; a "no" says little.
11. **What it would move.** 26 of the 29 new pieces are a word with an accepted meaning. They would move 59
    running words of the coverage map, from 13,292 to 13,351 of 21,977 (60.5% to 60.7%; with near-copies counted
    once 59.9% to 60.4%), and complete five more texts; without `mXeyot` and `yetmetl`, 54 words, still 60.7%.
    The largest are `tedxli` for `te-dḫe-l` (13 words),
    `bedewitel` for `Medewi` with `-tel` (7) and `beke` (5). The map's own numbers are not changed.
12. **Not confirmed:** `smlowi`, which stands in 81 running words. Both checkers take it for a known word, one
    for `sem` with `-lowi` and one for the title `smlo` with `-wi`.
13. **A first pass was set aside.** Its packs could show, under a word that holds the piece, the guess of the
    coverage map's analyst (in 17 of the 105 items, and for 15 more under the same word in another item), and
    each item named the kind of word. It confirmed 53 matches, `smlowi` among them. The packs were repaired and
    six fresh checkers read all 129 items again; 45 pieces are confirmed in both passes.
14. **Limits:** one scholar's list of variants is both the training and the test; the model counts from the
    headword to the variant only; letters cannot judge a short piece; the checkers' error rates rest on 12
    controls and 12 decoys; a pack hides the words the map finds a piece in, not every word that holds its letters
    (three items); no specialist has read a confirmed piece.
15. **Cost:** 1,269,219 subagent tokens for the checkers in two passes (657,132 and 612,087), against about 0.7
    million quoted for one pass with a second allowed for, and 425,616 for the review (about 0.45 million
    quoted): 1,694,835 in all.

## Day four, night (2026-11-11): six ways of finding meanings, and the map corrected

1. **Six agents dug into six ways of finding meanings from the local data**: testing the proposals that exist,
   kin terms through the families of Karanòg, the blessings against the Egyptian funerary wishes, titles through
   the Demotic graffiti, counted nouns by their numbers, and a consistency search for the frequent pieces. None
   found a meaning that is not already in Rilly's lexicon or its listed proposals (2.27 million subagent tokens;
   the reports are local).
2. **Why:** read from their contexts alone, 27 words of known meaning gave the right kind of word 26 times and
   the meaning 4 times, each time for a word that stands opposite a known partner (north and south, mother and
   father). One reader, not blind; taken as a measure of the method's reach, not as a result.
3. **What they did show** and what was then checked on the corpus: `ḫr` takes bread and nothing else as its
   object; the prefix written ps- or y- stands on `ḫr` in 91 of 93 texts and on `ẖol` in 4 of 56 (which has a
   bare p- in 16); `dole` follows "the good sacrifice" in all 7 cases of the blessings; `atmi` stands before 12
   after "do 6" where two recipients are named. All are readings that the literature already holds.
4. **Errors in the coverage map**, corrected by four rules (`python3 -I src/coverage.py correct`; section 7 of
   [`data/discovery/coverage.md`](data/discovery/coverage.md)): the rest of a masked name left by the padding of
   the older corpus (`moke` falls from 27 texts to 5), a stem of two signs (`smlowi`, "is the wife of", 81
   words), a word written apart (65 places), and the spellings of known words that two blind checkers confirmed
   (52 words). 321 words move: 13,292 to 13,613 of 21,977 (60.5% to 61.9%; with near-copies counted once 59.9%
   to 61.6%), 82 to 107 complete texts, 1,336 to 1,309 pieces without an accepted meaning. The 98 words of the
   first rule are names recognised, not meanings found.
5. **Two earlier claims of this project do not hold** and carry a note where they stand: that the w and q at
   the head of the two divine epithets tend to match within a text is not shown (5 of 9 texts with near-copies
   counted once; `data/discovery/funerary.md`), and `womnise` as the title "prince of Takompso" does not fit the
   place its holder has it in (`data/discovery/philae.md`, H7).
6. **Not checked against the literature, so not claimed:** that the relatives of an epitaph are listed in order
   of generation; that `tḫ` is "receive" rather than "give"; that a suffix -(t)k marks nouns counted together.
