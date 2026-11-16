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
2. **304 inscriptions are machine-readable under an open licence, 237 of them missing from the public corpus.**
   Griffith's printed Meroitic type read at
   95.6% sign accuracy against FHN (482 of 504 signs, 12 texts; 99.6% against Griffith's print;
   `data/expansion/printed_type_test.md`); 152 inscriptions transcribed, 86 new, +5% words (`src/expand.py`).
   The test covered cursive type only; the 48 rows in hieroglyphic type were not scored. REM 1003, the longest
   text, is open too: Griffith printed all of it in 1917 in his transliteration of the time; typed from page
   images and mapped to today's signs, 278 of its 337 words (82.5%) agree with Millet's closed reading
   (`src/akinidad.py`, `data/expansion/jea/`).
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

8. **About 62% of the running words can be translated today, word by word.** After four corrections, 13,618 of
   the 21,977 words of `corpus_v5` are a name, a number or a word that Rilly's 2003 lexicon holds as established
   or probable (61.6% with near-copies counted once); every legible word is translated in 106 of 605 texts. As
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
   the older corpus (`moke` falls from 27 texts to 6, which hold its four real passages and excerpts of them), a
   stem of two signs (`smlowi`, "is the wife of", 81 words), a word written apart (65 places), and the spellings
   of known words that two blind checkers confirmed (57 words; for `mXeyot` and `yetmetl`, 5 of them, the pack
   showed a word with their letters), with three forms of "sister" that the kin reader read so (4 words). 326
   words move: 13,292 to 13,618 of 21,977 (60.5% to 62.0%; with near-copies counted once 59.9% to 61.6%), 82 to
   106 complete texts, 1,336 to 1,304 pieces without an accepted meaning. The 94 words of the first rule are
   names recognised, not meanings found.
5. **Two earlier claims of this project do not hold** and carry a note where they stand: that the w and q at
   the head of the two divine epithets tend to match within a text is not shown (5 of 9 texts with near-copies
   counted once; `data/discovery/funerary.md`), and `womnise` as the title "prince of Takompso" does not fit the
   place its holder has it in (`data/discovery/philae.md`, H7).
6. **Not checked against the literature, so not claimed:** that the relatives of an epitaph are listed in order
   of generation; that `tḫ` is "receive" rather than "give"; that a suffix -(t)k marks nouns counted together.
7. **Cost of the corrections:** no analysts; the review took 525,377 subagent tokens and 54 minutes, against
   about 0.5 million and one hour estimated.

## Day five (2026-11-12): the map against two printed editions

1. **Two sources fetched** and kept locally, both in copyright: Millet's "The Meroitic Inscriptions from Gebel
   Adda" (JSSEA 32, 2005; 46 entries, 20 with a rendering into English) and *Fontes Historiae Nubiorum* III
   (1998; twelve entries on Meroitic texts, and 22 Demotic graffiti in translation, some of them by Wayekiye and
   his family, whose Meroitic epitaphs it prints too). 31 of their inscriptions are texts of our corpus, most of
   them under masked names.
2. **The question:** the coverage map takes every meaning from Rilly's 2003 lexicon. How often do two other
   scholars, reading the same inscriptions, give a word the same meaning?
3. **The answer** ([`data/discovery/experts.md`](data/discovery/experts.md)): of the 537 words the map counts as
   translated in those texts, the edition gives a meaning to 397 and the map's meaning to 276 (69.5%); the two
   overlap in part for 62 and differ for 59. Names agree for 90.6%, words with a meaning for 65.6%, grammar words
   for 37.8%. On 140 words (26.1%) the edition is silent or lacks the word.
4. **Two words carry most of the gap:** `yetmde` (Rilly's "nephew, niece", both editions' "relative"; 54 places
   judged "partly") and `qo` (Rilly's "this one", Millet's "the noble"; 22 places). Outside them the map agrees
   on 259 of 304 words (85.2%). These are differences between scholars: both editions are older than or apart
   from the lexicon, and the check cannot say who is right.
5. **Errors of ours that it found:** in the epitaph of Makheye (REM 0544) the numeral 1 after each prince's name
   is typed as the letter `l` in the older corpus, where the text stands four times, and the map read it as a
   word; eleven names or pieces of words were read as words; `mlo` is only "adjective" in the map where both
   editions read "good". Where our copy has `mete l` or `mokelowi` after a masked name the editions have only a
   name, which supports the first of the map's corrections.
6. **Meanings the map lacks:** two readers listed 167 different meanings the editions give. For 64 the map has no
   accepted meaning for the word (26 stated as sure, mostly titles left untranslated, phrases whose words the map
   reads the same way, or proposals the lexicon holds; among the others `selele`, "cataract" for FHN after
   Griffith, a place name in the lexicon), and for 41 it translates the word otherwise by the judges' verdict (22
   stated as sure): `yetmde`, `qo`, `peseto` and `ant` again, `mete` ("child" in the map, "little" for Millet),
   and proposals Millet marks as unsure (`dime` "day", `xlbi` "month").
7. **How far to trust it:** the judges accepted 1 of the 22 first-run decoys the editions give a meaning for
   (a near-synonym of our real reading) and none of the 30 of the second design. Two judges gave the same verdict
   on 361 of 372 words; they are the same model, so that is stability, not proof. One judge read two thirds of
   the words.
8. **Flaws of the method:** decoys drawn by kind of word let near-synonyms through (the first run kept them, the
   second design does not); a decoy shown beside its real row can be told by the repeated word; and a draw and a
   shuffle from one random seed put every decoy at the end of the table. The last two were found before or by
   the review of the local scripts and fixed before the judges of the second pass started. The review of the
   published scripts found a fourth: Millet prints one commentary for the fragments GA55 and GA56, after the
   text of GA56, and the packs gave it with GA56 only, so the judge of GA55 read that text without it (all
   "silent").
9. **Cost:** eight agent runs and four rounds of a reviewer on the local scripts, about 1.02 million subagent
   tokens and 35 minutes of running, against quotes of about 0.5 and 0.2 million for the two passes (up to 0.8
   and 0.3).
10. **The review of the published scripts and pages:** one fresh reviewer at the full tier, 500,972 subagent
    tokens and 37 minutes, against about 0.4 million quoted. It corrected facts the pages had wrong (Millet's
    article has 46 entries, not 49; the epitaph of Makheye stands four times in the older corpus, not eight; the
    eleven misread words are four names and seven pieces of words; eight agent runs, not nine), made the draw of
    the packs the same in every run, found the shared commentary of GA55 and GA56, and added nine checks to the
    26, among them checks that rebuild the local files byte for byte and that pin the numbers of the summary
    pages.

## Day five, afternoon (2026-11-12): one inscription once

The first of the four builds of `NEXT_STEPS.md`, section F ([`data/discovery/corpus_v6.md`](data/discovery/corpus_v6.md)).
The table, the map and the corpus were built without an agent; two readers then read the doubtful matches.

1. **Otten's padding can be undone exactly.** His repository holds the examples before padding in per-scholar
   files, with real names and the page of Millet's 1968 thesis. Of the 17,995 different lines of the padded file,
   340 are a line of those files letter for letter, 17,446 are such a line with one stretch swapped, and 206 more
   differ in a second small place. The 659 texts of the older corpus come from 329 source lines.
2. **What `corpus_v5` was:** 289 of its 899 texts stand for an inscription (30.0% of its 21,977 words); 207 are
   copies of a reading with a name swapped (54.5% of the words), 273 are example phrases from a grammar or
   word-list entries and 123 more are copies of those; 4 are second readings; 3 are not settled. One Gebel Adda
   text, GA 28, stood 86 times (6,284 words, from 2 of Millet's lines).
3. **`corpus_v6`:** 548 inscriptions, each once, with real names; 289 were in `corpus_v5` and 259 are new (209 of
   the Newsletter's texts and 50 of Griffith's rows that `corpus_v5` left out). The table holds 563 inscriptions:
   441 with a REM number, 64 with readings from two editions or more, 304 with a reading under an open licence, 8
   quoted by Millet and not identified.
4. **The bar for the matching rule was missed:** the right partner is the best match for 45 of 54 known pairs
   (83.3%; the bar was 90%), and 4 of the 151 Karanòg texts have a sure match to another Karanòg number, a
   second monument of the same person. So a number decides before letters do, a sure match stands only when it
   is the only one, and 17 doubtful matches went to two readers.
5. **The readers passed their bar:** each named the right text for 12 of 12 known lines and answered "none" for
   12 of 12 lines whose text had been taken out. On the 17 open lines they gave the same answer for 15. 13 of
   their matches are taken (one more was a guess for both and is left out), one line matches nothing, and 3
   lines are not settled.
6. **A check caught one of the readers' matches:** a line they placed in the fragment GA 13+16 also holds a
   passage of a long epitaph quoted on the same pages of the thesis, because Otten's line runs two quotations
   together. It is set aside, so that no text stands in two rows.
7. **The numeral fault is repaired where another edition shows it:** 13 lone `l` are read as the numeral 1, 10
   in the epitaph of Makheye (REM 0544; 4 after Newsletter 28 and 6 by analogy in the same list) and 3 in REM 0101
   after Griffith's print.
8. **The coverage map counted again:** 60.0% of the words of the inscriptions that were in `corpus_v5` (62.0% on
   `corpus_v5`, 61.6% with near-copies once). With the new inscriptions it is 51.3%, because 966 of their words
   are spellings no analyst has seen.
9. **The check against the two editions counted again:** of the 1,115 judged rows, 1,005 still stand in
   `corpus_v6`; on those the editions give the map's meaning for 71.4% of the words they translate (267 of 374;
   it was 276 of 397, 69.5%).
10. **Cost:** the two readers took 253,065 subagent tokens together and the review 523,726 (65 min 28 s), 776,791
    in all, against a quote of about 300,000 and 500,000. The estimate in `NEXT_STEPS.md` was 2 to 4 million
    for this piece.
11. **What the review changed:** a second printing of one Newsletter text had been lost under the key of the
    first, Millet's segmented analysis of REM 0101 had been taken for its reading, the 15 texts of FHN no. 267
    were missing from the table, a name with a lost sign inside had been matched to two whole words, and "two
    readings or more" had counted the fragments of one edition apart. The figures above are counted after those
    fixes.

## Day five, evening (2026-11-12): the unread spellings, and the same people in Demotic

1. **Analysts on the spellings of the clean corpus that none had read**
   ([`data/discovery/v6_readers.md`](data/discovery/v6_readers.md)). 930 spellings (1,038 running words) went
   to seven analysts, and the 110 most frequent to an eighth. 125 got a translated level (68 names, 55 meanings,
   2 grammar words), 194 a proposal of the lexicon, 61 their kind and 550 nothing. 139 running words more are
   translated: 5,419 of 10,290, 52.7% from 51.3%; the Newsletter's texts go from 36.2% to 39.8%.
2. **The bar was met and the estimate was not.** The two analysts put 105 of the 110 words read twice on the same
   side (the bar was 85%; 92 at the same level). The gain expected beforehand was 265 to 385 words, taken from
   the share the analysts translated on the older texts. The unread words are another kind of word: pieces of
   words that an edition prints in two parts, and single words of broken or obscure texts.
3. **The same people in Demotic, Greek and Meroitic** ([`data/discovery/demotic.md`](data/discovery/demotic.md)),
   a part of step 17 (its oracular decrees stay open). Three readers went through the 24 Demotic and Greek
   entries and the nine Meroitic entries of *Fontes Historiae Nubiorum* III: 99 people, 21 of them in two entries
   or more, four with a title in Meroitic and in Demotic or Greek. Where the two texts give the same office, the
   titles line up with the lexicon: `perite` beside the Demotic "agent" twice and `peseto` beside "the king's
   son" and the Greek `psentes`, the words the lexicon derives them from, and `kroro` beside `3krre`, the same
   title of unknown meaning.
4. **The editors' equations:** 143 in the readers' lists, 125 without the names, 110 different lines. The map
   translates the word of 64; two judges agree with its reading on 36 of 58 and 41 of 57, and accepted none of
   their 17 decoys. On the list of what the map lacks are 69 lines, 46 of them on words without an accepted
   meaning, mostly titles the editors leave as titles too; 10 of those are words the map holds, spelled otherwise
   by the OCR, written by a reader as two spellings in one, or misprinted in FHN III and corrected in its index
   volume. More than the map has: `qoreñ` as a title built on
   `qore` "ruler", `arbetke` as a title of priests with economic duties, and "the great envoy to Rome" for
   `apote-lẖ Arome-li-s`. No meaning is both new and sure.
5. **Both bars of the Demotic step were met, and the hope of a meaning or two added was not:** the two readers
   list the same person in 72 of 74 lines (80% was asked), and both find four of the five known equations (the
   fifth, `ant`, is only in the Meroitic entries; one of the four, `qoreñ`, was the example line of their brief).
6. **Cost:** eight analysts 1,012,556 subagent tokens; three readers 384,658 and two judges 126,264 for the
   Demotic step; 1,523,478 together before the review, against 2.0 million quoted for the two with their review
   (1.5 for the first and 0.5 for the second).
7. **What the review changed:** the join of person lines had made one person of two namesakes (Hornakhtyotef I
   and II) and of two men of the first and the fourth generation of one family (Pshentsône and Sosen): 99
   people, not 97. The rule for the OCR's ñ had missed a phrase with a true "ri" in it (5 lines, not 4), and 4
   lines written as two spellings in one were not named. The joining without the limit on length gives 11 words,
   not the 12 counted by hand. And `src/v6/readers.py count` had written its figures over those of the readers of
   the clean corpus's doubtful matches, whose local folder it shared.

**The review of these two steps** (full tier) cost 533,937 subagent tokens and 37 minutes, by hand from its task
notification: 2,057,415 for the two steps with their review, against the 2.0 million quoted.

## Day five, night (2026-11-12): a second scholar for every meaning (F2, first pass)

1. **4,105 of the 10,290 running words of the clean corpus (39.9%) are built only on meanings that a second
   scholar gives too;** one lexicon translates 5,419 (52.7%). Names and numbers count in both. Of the 3,676 words
   the map translates as a meaning or a grammar word, 2,362 (64.3%) are built only on agreed entries. With the
   first round of judges alone it was 3,875 (37.7%): a second round closed the gap item 5 named.
2. **The statuses of the 177 entries behind translated words:** 84 agreed by two scholars, 22 disputed, 51 stated
   by one, 20 only proposed. `qo`, `mlo` and `mte` lead the disputed; endings and pieces of the benediction
   formulas (`-wi`, `ps-`, `-te`, `-kete`) the proposed. Round three (below) made the god `Mnp` agreed.
3. **In round one the judges met both bars set before they answered:** kappa 0.92 on "same or not" (0.6 asked),
   and 2 and 0 of 41 decoys accepted (a tenth allowed). They read 407 proposals that the lexicon records, without
   the scholars' names. In round two the second judge accepted 1 of its 4 decoys, which misses the decoy bar by
   its letter: "wife", called "partly" beside "woman".
4. **The lexicon's record of other scholars held where it could be checked:** of 20 of its citations of
   Griffith, 15 were found in his own texts, all as stated (bars: 10 found, 90% as stated). The 5 not found all
   cite "Griffith" without a year, which does not say which text: 15 of the 20 drawn do.
5. **Limits:** after round one the 82 lines that carried a decoy for one judge could not count under the rule;
   round two had that judge read them with the real proposal, and with round one alone the figure would be 3,875
   (37.7%). An ending that the map's lookup cuts off without naming its entry is not checked; held to the agreed
   endings, the figure would be 4,014 (39.0%), and without the editors' agreements on pieces of words (which make
   `-lowi` and `-to` agreed) 4,057 (39.4%). One editor's agreement on one word is enough, which makes `yetmde`
   agreed; and the editors were shown the map's short gloss, so their "good" for `mlo`, the lexicon's meaning,
   did not count as agreeing. A writer worded the 177 meanings anew for the public table; one that shared four
   words in a row with the lexicon's meaning was reworded by hand.
6. **Cost:** four judges' packs 388,896 subagent tokens, the check against Griffith 250,976: 639,872 before the
   review, against 1.4 to 1.8 million quoted with the review.
7. **What the review changed in the count:** the code had called "proposed" the five names inside translated
   words (Isis, Osiris twice, Napata, `Mnp`), against the rule, and had counted as an editor's dissent the words
   that the check against the editions found the map misreading (the numeral 1 typed as `l`, names read as
   words): the verb `l` "to give" was disputed only through them. As first counted: 70 agreed, 23 disputed, 59
   stated by one, 25 proposed, and 3,873 words (37.6%).

**The review of F2's first pass** (full tier) cost 459,019 subagent tokens and 44 minutes, by hand from its task
notification: 1,098,891 for the first pass with its review, against the 1.4 to 1.8 million quoted for all of F2.

**Round two of F2** (12 November, evening): the two judges read with the real proposal the 41 lines each where
they had seen a decoy (143,940 subagent tokens), and a writer worded the 177 meanings anew (100,947; both costs by
hand from the task notifications). The second judge called 1 of its 4 new decoys "partly", "wife" beside "woman",
a pair the list of fields does not keep apart: by the letter of the bar (a tenth), round two's decoys fail it.

**The review of round two** (full tier) cost 346,989 subagent tokens and 32 minutes, by hand from its task
notification. F2 so far: 1,690,767 subagent tokens with its two reviews, within the 1.4 to 1.8 million quoted. F2 is
not complete: each entry's spellings, the page of each scholar's statement and a status for the other entries the
map uses are still open (`NEXT_STEPS.md`, step 23).

**Round three of F2** (12 November, night): both judges read every proposal that rounds one and two had not sent,
109 on the 417 other entries the map uses and 25 on the names inside translated words, each beside 20 decoy lines
under new numbers; a decoy was a real proposal of another entry, far from the line in meaning (171,392 subagent
tokens, by hand from the task notifications). Both bars, set before they answered, were met: kappa 0.90 on "same or
not", and 0 of 20 decoys accepted by each judge. Of the 417 other entries, 30 are agreed, 4 disputed, 43 stated by
one and 340 proposed (Rilly gives them as a hypothesis, by their kind only or without a meaning); of all 594, 114
are agreed. The second figure stays at 4,105 words; under a stricter rule for the editors (at least two words read
the same, and most of them) it would be 3,715 (36.1%).

**Spellings and pages:** both tables now give Rilly's spellings of each entry and 33 of the 48 confirmed variants
of step 21, and pages where the sources in hand give them: the editions' entries for 100 entries, FHN IV's indexes
of gods, persons, royal names, titles, places and words for 113 (read from its page images), and Griffith's own
page for 10 of the 206 proposals both judges found the same or otherwise. Rilly's record gives a page for none of
them; the other scholars' pages are not in our sources, but for papers the Meroitic Newsletter may hold, which a
year alone does not point to without Rilly's bibliography. Left open: a meaning in our words for the 417 other
entries, and FHN IV's glosses as the statement of a second scholar.

**The review of round three** (full tier) cost 596,297 subagent tokens and 43 minutes, by hand from its task
notification. It fixed the count of the confirmed variants (a piece written as a headword is now compared in the
corpus's letters), added FHN IV's indexes of places, persons and royal names, made the figures file the same on
every run, and ran the guard against copied meanings before any local file is read. Round three with its review:
767,689 subagent tokens. F2 so far: 2,458,456 with its three reviews, within the 2 to 3 million that step 23 of
`NEXT_STEPS.md` quotes for it.

## Day five, late night (2026-11-12): whole texts translated and scored (the pilot of F4)

1. **The design came first.** Five of the 20 texts N. B. Millet renders into English in his Gebel Adda article
   (2005) were chosen by a rule (the label GA47, the offering table GA41, the stelae GA28, GA53 and GA37; 141
   words), and five texts under an open licence for the cost of a page. The bars and the expected scores were
   committed (b990f42) before any agent answered.
2. **The translator was blind to Millet.** Its pack held the map's reading of every word and the lexicon's
   entries with F2's statuses; the 152 proposals in the lexicon that are Millet's or speak of his, one meaning
   and one word's reading that name him, and his weight in F2's statuses (16 of 177 entries change) were left
   out. The baseline is the map's glosses in order, with the same reading withheld.
3. **The judging held:** the two judges gave the same verdict on 112 of 114 lines (kappa 0.97, bar 0.6), and
   called all 57 decoy lines wrong (bar: at most a tenth of the clean ones given or partly).
4. **The translator does not beat the map read word by word.** Of Millet's 57 scored units of meaning it gets
   58.3% (given, and half of partly) and the baseline 60.5%; with each text weighing the same, 50.8% and 46.8%.
   The lead is under the 5 points set beforehand either way. Expected: 50% and 35%. The translator gets 3.5% of
   the units wrong and the baseline 6.1%.
5. **Why:** the translator leaves open the words the map knows only vaguely, where the vague gloss earns half
   credit (`smlo`, `mde`), and makes `yetmde ... aqebetowi` "their nephew or niece" where Millet has "related
   to"; it reads places better (`Skl` as Sakala, "in Meroe") and drops the map's "this one is" where Millet has
   "the noble one". An epitaph is a list in a fixed order, so glosses in order carry most of it. Found in the
   review: the baseline gave "?" for the 4 of the 141 words that the map counts as unknown but its analyst
   glossed in part, glosses the translator saw; one `Skl` and the relation and wrong place of GA53 rest on them.
6. **For the full run:** scoring the 18 renderings the corpus holds costs about 2.1 million subagent tokens at
   the pilot's rates (1.6 million for the 13 left; with one judge about 0.5 million less for the 18, 0.4 for the
   13); pages for the 304 inscriptions with an open reading with this translator about 6.3 million (5.3 for the
   286 whose corpus row is that reading). By the rule set beforehand the pages should be built from the map's
   readings by a lighter step, not yet measured. The splitter's "open" marks, the judges' rule against outside
   knowledge and the baseline's glosses need fixing first
   ([`data/discovery/f4_pilot.md`](data/discovery/f4_pilot.md), sections 7 and 8).
7. **Cost:** five agents, 560,981 subagent tokens (translators 145,118 and 104,696, splitter 99,501, judges
   107,682 and 103,984), against 0.35 million expected, before the review.

**The review of the pilot** (full tier) cost 398,363 subagent tokens and 34 minutes, by hand from its task
notification: 959,344 for the pilot with its review, past the 0.8 million at which the brief asked to check with
Mike first. It stated on the page that the baseline hid the analysts' glosses of 4 words the translator saw, counted
the sizing in the script, and ended not clean on one line: the brief asked the two judges to split Millet's
renderings themselves, and one blind splitter did it. Mike waived that line the same evening (21:14), and the
reviewer, with his words, re-checked and marked a410dae: 28,262 subagent tokens more and about four minutes, 987,606
for the pilot with its review.

## Day six (2026-11-13): ways of translating compared, and the best scored on held texts (F4)

The pilot of the day before left three faults in its scoring and one question: can a translation carry more of a
scholar's meaning than the map's glosses in order? The page is
[`data/discovery/f4_rounds.md`](data/discovery/f4_rounds.md); the design, the bars, the expected scores and the
rule for what is carried on were committed before the agents of each step answered.

**What changed.** Every one of the 18 renderings was cut again, by a splitter of its own that marks a unit open
only when all of it is untranslated (on the pilot's five texts 1 open unit has a translated part, against 17).
The judges may tell that two names are one place. The glosses show every gloss the translators see. And the
translator got three things: rules that keep what the materials hold (a vague gloss stays, a disputed word shows
both readings), a handbook, and parallels from the corpus. The handbook was compiled by one agent from Rilly's
lexicon, Rilly 2021, the *Fontes Historiae Nubiorum*, Griffith 1911 and 1912, Lipiński 2011 and the project's
pages, without Millet's edition: 124 lines with a source and a page. Four checkers read each against its page:
80 confirmed, 43 corrected, none dropped, 1 outside their ranges.

**Round one, on the pilot's five texts (75 units).** Five readings and a decoy: the pilot's translation, the
glosses, a writer that only makes sentences of the glosses, one translator, and a panel of three translators
with an editor. The first judging missed its bar: the judges' kappa was 0.58, because in GA28 Millet writes "she
was related to X" where every reading says "nephew or niece of X", and one judge called that given and the other
partly. By the rule set beforehand nothing was carried on. One rule was added (a kin term where the rendering
names none is "partly") and 14 new judges read the same readings: kappa 0.94, no decoy accepted, glosses 63.0%,
pilot 65.0%, writer 69.7%, translator 75.3%, panel 78.0%. The panel was carried on.

**The held texts (13 renderings, 218 units), the result.** Both bars met: kappa 0.88, and each judge accepted 1
of 186 clean decoy units. The glosses get 58.5%, the writer 69.3%, one translator 73.9% and the panel 74.9%; they
are wrong on 9.2%, 4.4%, 2.8% and 2.3% of the units. The panel's lead over the glosses, 16.4 points, is over the
bar of 5 set beforehand and inside the 8 to 18 expected. Unit by unit the panel is better than the glosses on 56
and 55 units and worse on 2 and 2. The gain is largest in places (44.6% to 87.0%) and smallest in relations
(45.6% to 52.9%); the invocations of gods are given by every reading.

**What it does not show.** The panel leads one translator by 1.0 point: unit by unit it is better on 5 and 2 of
the 218 units and worse on 1 and 1, so the editing of three into one is not shown to add anything. The writer,
who sees no lexicon entry and no parallel, gets 10.8 of the 16.4 points: most of the gain needs neither. All 18
renderings are one scholar's, from one site. The pages for the 304 open inscriptions are not built, and
Griffith's own translations are not yet a second rendering.

**Cost.** 17,879,477 subagent tokens for the day's rounds without three editors whose tokens were not reported:
the splitters 1,169,212, the handbook 555,173 and its check 1,015,037, round one 3,565,443 and its second
judging 953,178, the held texts 10,621,434. One translator costs about 112,000 tokens a text and the panel about
450,000, most of it each agent's fixed cost.

**The review of the rounds** (full tier) cost 440,752 subagent tokens and 33 minutes, from its task notification.
It recounted every figure from the local files with a script of its own, rebuilt every pack from the answers, and
checked the commits of the designs against the times of the first answers. It ended clean after ten fixes: the
rule no longer carries anything from a judging that misses a bar; a judge's file counts only for its own pack;
README's headline gave the panel's 74.9% to one translator; two claims said more than the counts show ("most of
the gain is the handbook and the order of a sentence": the writer had the rules and each word's status too); the
next step in NEXT_STEPS weighed cost against the rule set beforehand, which builds the pages with the panel; and
the compiler's and the checkers' instructions were not in the repository (`runs/prompts/`).

## Day six, afternoon (2026-11-13): the unread spellings that recur

Asked that day: "our goal is to decipher the meaning of all words", then "start working on the 154 recurring
words". Of the 7,331 running words of `corpus_v6` that need a meaning the map reads 3,676 (50.1%). 154 spellings
without an accepted meaning stand in three texts or more; they cover 1,108 running words and fall into 121 items
by the lexicon entry they are filed under. Page: [`data/discovery/recurring_words.md`](data/discovery/recurring_words.md);
script `src/recurring.py`. Every bar below was set before the agents it binds were started: committed for the
place pass and the blind test, written in the working script for class A (the page's section 9 gives the commits
and the times).

**What the sources say.** Ten readers collected 792 statements about the items from the sources in hand, each
with a quote; a script found all 792 quotes in the files named. For 29 items the first reader found a statement of
Rilly's work of 2016 or 2021 that accepts a meaning or calls it probable; two more readers each read those
statements in their place, and 26 items pass (both find the meaning stated firmly in the same source). The map
does not have these meanings because it rests on the lexicon of 2003.

**Every place, twice.** A meaning stated for a word is not a meaning for every place its spelling stands, so two
checkers decided each of the 1,108 places on their own (kappa 0.91, bar 0.6): 273 hold the word the later source
speaks of, 192 are pieces of a longer word or name that the edition's word division cut, 425 are words of their
own that stay open, 139 are unclear and 79 not agreed. A script, apart from the checkers, finds bread among the
three words before all 87 stated places of the verb "eat".

**The count.** Laid over the map, which is not changed, the results move the share of running words with a
meaning from 50.1% to 53.9% (3,916 read, 306 fewer open). Every one of these meanings is Rilly's or the map's own
reading of a rejoined word; none is a reading of this project.

**The open words.** 65 items keep three or more open places. For 48 both readers list a meaning the sources
propose, and seven items are names by the sources. A blind test then asked whether the contexts can tell a
proposed meaning from other meanings of the same kind: 71 words shown only as a code among the map's readings of
the words around them, four meanings under each, five readers a word. On the 27 accepted words that had their
true meaning among the four, the readers chose a meaning for 17 and were right for 13 (76.5%; the bar was 80%);
on the 11 whose true meaning was not offered they still chose one for 2 (18.2%; the bar was 10%). Both bars are
missed, so no proposal for an open word is labelled, and the check of labelled proposals did not run. The readers
confused meanings of one kind: "good" with "great", "agent" with "priest", "sister" with "direct descendant".

**Limits.** All readers and checkers are one model, so their agreement shows that a reading can be repeated, not
that it is right. The literature pass had one reader a batch, so a statement it missed is missing from every later
step. The stated meanings are one scholar's. The 2,203 open spellings that stand in one or two texts were not in
this work.

**Cost.** 101 fresh agents, 9,846,666 subagent tokens: the literature pass 2,411,497, the two readers of the
stated meanings 613,355, the place checkers 4,146,199, the readers of the proposals 780,535, the blind readers
1,895,080.

**The review** (full tier) cost 497,794 subagent tokens and 36 minutes, from its task notification. It recounted
every figure from the local files with a script of its own, rebuilt every pack and result byte for byte in a
copy, and set the times of the bars against the times the agents were started. It ended clean after 13 fixes.
The main ones: the pages said every bar was committed before its agents answered, but the bar of the stated
meanings stood only in a local script, written five seconds before its readers were started; the literature pass
has one reader a batch, not two; the 139 unclear places were called damaged, and about 45 of them have no lost
sign; README's headline said more than the blind test showed; the script's check of the formula took water for
bread (the counts did not change); and the packs can no longer be written again once they are answered. After
the review, nine meanings that followed a source's wording for four words in a row were put in our own words in
the public files; the packs and the answers keep the readers' wording.

**A second review**, of the one commit made after the first (the nine meanings put in our own words), cost
373,318 subagent tokens and 24 minutes, from its task notification, and ended clean after six fixes. The table of
rewordings held the readers' wordings as its keys, so they still stood in a tracked file; the check for copied
wording read only the lexicon entries the map uses, and missed words in which the text layer of Rilly 2021 has
lost a ligature; one of the new wordings itself followed another entry for four words. It also noted that the
copied wordings still stood in the branch's earlier commits, which a later commit cannot take out.

**Before the push.** On Mike's word of 2026-11-15 the six commits from the work itself to the second review's
cost were made one, with the same files, so none of the nine wordings reached GitHub. A check of that squash
(210,173 subagent tokens, 12 minutes, from its task notification) found the files unchanged and no local-only
file in any commit. It also found that the three commits kept as they were, because their times show when the
bars were set, each hold one run of four words of Rilly 2021: the name of the case ending of `-w (1)` in section
4 of the page, which the head says in other words. Mike waived that one phrase on 2026-11-16. The same reviewer
then checked the squash again with the waiver (286,998 subagent tokens, 8 minutes), corrected two sentences of
the new section G of NEXT_STEPS, and marked the commit. The work is on main since 2026-11-16.

## Day nine (2026-11-16): distinct words, the north star

Asked that day: "why dont we have Distinct wrords translated? this sounds like a north star metric if we want the
entire language translatable?", then "do it and add to the table as the first row". Page:
[`data/discovery/distinct_words.md`](data/discovery/distinct_words.md); script `src/words.py`.

**Why it was missing.** A spelling is one written form, and a word has many. For a spelling without a meaning
nobody can say offhand which word it belongs to, so the words could not be counted, only the spellings (20.2% of
those that need a meaning are translated) and the running words (50.1%).

**The count.** Every running word of the map that needs a meaning is a word of the lexicon (377 in use, 127 of
them with an established or probable meaning), a piece (an ending or a particle written as a word of its own), a
name, or a stem the map could not name (1,107, of which 975 stand in one place). Two checkers judged a sample of
240 of those stems, drawn by a fixed seed. The first reading missed its bar (kappa 0.53: "a word" against
"unclear" for stems that stand once), so by the rule set beforehand the brief was corrected and other checkers
read the same sample: kappa 0.94. About two in three of the sampled stems are words of their own; the rest are
pieces, words with lost signs, names or forms of known words.

**The result.** About 1,307 distinct words (between 1,049 and 1,384), of which 127 are translated: 127 of about
1,307, or 9.7% (between 9.2% and 12.1%). Before the project it was the same: each of the 127 has its meaning in
the lexicon of 2003, and the project has added no meaning. The first count had given as "before us" what a plain
lookup of the lexicon reaches (112 of the 127); Mike answered "“Before us” should really equal “Now”, 11.6%.",
since the lookup measures the reach of the map, as the rows of running words and of spellings do. With the
recurring-words results in the map it would be 136 (10.4%), with Rilly's meanings of 2016 and 2021, which are
older than the project too.

**The review.** The first count also took the endings and particles written as a word of their own for words
(68 entries, 33 of them translated), which the checkers' case "piece" does not do among the unnamed stems and the
plan's "strip the known endings" does not do either, and one name of the kind "name" for a word: 160 of about
1,376, 11.6%, the figure in Mike's answer above. The review made them pieces and a name, on the side of the
dictionary only, so the sample and its estimate stay as they were.

**Cost.** 40 fresh agents, 3,012,391 subagent tokens for the two readings. The review (full tier) cost 562,088
subagent tokens and 49 minutes, from its task notification. Mike kept the review's count on 2026-11-16 ("Yes, 9.7%
and push"). How the status table is built and each of its numbers measured is in
`.claude/skills/reporting/SKILL.md`.

## Day nine, afternoon (2026-11-16): the map takes its first layer (G1)

Asked that day: "Yes, start G1 and G4, queue G2". Page:
[`data/discovery/map_layers.md`](data/discovery/map_layers.md); script `src/themap.py`.

**What was built.** The 385 places that the recurring open spellings resolved had been counted over the map but
were no part of it. They are now a layer: a file of lines, one for each running word, with the new level and
meaning, the reason and the source. The script lays the layers over the analysts' map each time it runs and
stops if a line does not fit the map. The analysts' map is not changed.

**The map as it stands.** 3,916 of the 7,265 running words that need a meaning are translated (53.9%, from 50.1%);
626 of the 2,944 distinct spellings (21.3%, from 20.2%); 136 of about 1,307 distinct words (10.4%, between 9.8%
and 13.0%, from 9.7%). The nine words more are Rilly's meanings of 2016 and 2021, published before the project, so
the north star's "before us" is 10.4% too. Of the layer's 385 places, 79 were translated or named already and
take the later reading; 306 were open. Two of the 1,107 stems the map could not name become names; the estimate
of the words among those stems is carried over, and the script stops if layers ever take more than 2% of them.

**What was not built as the step said.** The step named three pages to be rebuilt from the same file: the
coverage of the clean corpus, the lexicon's statuses and the translations' baseline. They are not counted again.
Each reports dated work on the analysts' map; the lexicon's statuses and the baseline rest on judges who never
saw what the layer adds; and the baseline is the status table's "Before us", which changes only on Mike's word.
The new page counts the coverage measure on the map with this layer (55.6% of all running words translated or
named, from 52.7%), and the three pages point to it. Mike waived this cut on 2026-11-16 at 13:52, asked whether
the three pages could keep their numbers and point to the new page: "Yes, waive it."

**The status table** reads its first three rows from `data/discovery/map_figures.json` since this step
(`.claude/skills/reporting/SKILL.md`).

## Day nine, afternoon (2026-11-16): the rare spellings under an entry of the lexicon (G4 and G2)

Asked that day: "Yes, start G1 and G4, queue G2". Page:
[`data/discovery/rare_spellings.md`](data/discovery/rare_spellings.md); script `src/rare.py`. The rules of both
steps were committed at 12:58, before any agent was started; G2 ran beside G4 as soon as agents were free.

**G4, the entries without an accepted meaning** (323 entries, 784 spellings, 1,033 places). 27 readers collected
1,659 statements, each quote found in its file by script. For 57 of the 60 entries of class A two readers agree
that Rilly states a meaning in 2016 or 2021. The 695 places of the entries of class A and B went to two
checkers. The first reading was not taken: the checkers agreed (kappa 0.93), but one place had one answer
only, and the bar set beforehand takes nothing then. The brief got one line naming the number of places in the
pack, and 32 fresh checkers read the same packs: every place answered, kappa 0.93, 181 places stated,
113 pieces, 327 open.

**G2, the spellings under an entry the lexicon calls sure** (116 entries, 366 places). Two checkers a place,
kappa 0.70: 245 places hold a form of the lexicon's word, 28 are pieces, 51 are not agreed.

**What goes into the map.** Looking at G2's stated places showed that "a form of the word" is not "the word is
translated": 74 stand under an ending whose stem nobody knows, and about half of the 68 stem places with an
unnamed part join the lexicon's word to a name or an unknown word. So a stated place is laid only where the map
names every part of the spelling and every stem among them has a meaning, and an entry that is a name is laid as
a name (a piece, as before, only where the map translates or names the whole word). These rules were written into the page as they were made, with the time: before G4's places were counted,
but for G2 partly after its count, where they only lower the figure. Laid: 109 places of G2 and 159 of G4;
182 recognised places stay open.

**The map as it stands.** 4,149 of the 7,230 running words that need a meaning are translated (57.4%), 814 of 2,917 distinct spellings (27.9%) and 156 of about 1,307 distinct words (11.9%, between 11.3% and 14.9%). After G1 the
map stood at 53.9% of the running words and 10.4% of the distinct words. 20 entries of the lexicon are new with a
meaning, all Rilly's; by his own later analysis several are forms of one another (`sr` and `asr`, `erk` and
`yerki`, the two `tk`), so the gain in words is smaller. Our own meanings: still none.

**Cost.** 119 fresh agents, 13,892,589 subagent tokens, from the task notifications; 34 minutes from the first
reader to the last count.

**The review of G1, G2 and G4** (full tier, a fresh Opus agent at the highest effort): 19 corrections in two
commits, among them the coverage figure on the map's page (58.2%, not the 55.6% of the first layer alone), the
pieces among the places laid, the times at which three of the rules were added, and a check that runs every step
of G2 and G4 again and gets the same packs and results. Cost: 531,129 subagent tokens and 42 minutes, from its
task notification. Mike's word on the three older pages of G1, 13:52: "Yes, waive it."

## Day nine, afternoon (2026-11-16): names among the unknown spellings (G3), and a second scholar for the later meanings (G5)

Asked that day, to "Start G3's pilot and G5 now, while the review runs?": "Yes, both". Pages:
[`data/discovery/unnamed_spellings.md`](data/discovery/unnamed_spellings.md) and
[`data/discovery/second_scholar_later.md`](data/discovery/second_scholar_later.md); scripts `src/unnamed.py` and
`src/second_later.py`.

**G3.** 1,107 rare spellings hang on no entry of the lexicon (1,225 open places). The step had planned a script that
proposes joins with the neighbouring words; counted first, it finds one at 11 places, so the checkers decide from
the place. The first pilot (100 places, 50 controls) missed two bars and is not taken: the checkers could not see
a word cut in two in running text, which nothing in a context shows, and the two known words they both called
pieces were particles written apart, which the project's own counting rule calls pieces (the third known word
they missed, both called a name). The faults were in the controls. A second pilot with other places, controls
with a sure answer and a bar on what is laid (a known word called a name) met its bars, and so did the full pass:
kappa 0.79; 4 of 75 known words called a name by each checker; 30 and 29 of 37 known names found. Of the 1,225
places 828 are words of their own, 111 names, 41 pieces, 128 unclear and 117 not agreed.

**What it changes.** The 111 names and 7 pieces are the map's fourth layer: 4,154 of the 7,117 running words that need a meaning are translated (58.4%), 815 of 2,813 distinct spellings (29.0%) and 156 of about 1,284 distinct words (12.1%, between 11.5% and 15.2%).
No word got a new meaning. The running words rise because 113 words no longer need one and 5 pieces take the
meaning the map gives their whole word; the north star rises because the count of distinct words fell from about
1,307 to about 1,284. That recount was made from the 230 sampled stems still unnamed, by a rule written down before
the full pass was counted; the reporting rules had named a new sample instead. Asked whether to keep the recount,
Mike answered at 14:49: "why do you need my approval to recount? this is obvious you need to recount to show the up
to date result?". The north star with this layer was first given as 12.2%, from its share rounded twice: 156 of
1,284 is 12.1495%.

**G5.** For the 66 entries with a meaning stated by Rilly in 2016 or 2021, two judges compared it with 260
statements of other scholars and 26 decoys (kappa 0.95; one decoy taken for the same by each judge, none for
"partly"). 33 meanings are agreed by two scholars (15 with a dissent), 13 are disputed, 20 rest on Rilly alone. One
of the disputed, `tk (3)`, is disputed only through a proposal the lexicon gives without a scholar's name. Unlike
F2's judges, these saw the name of each statement's scholar.

**Cost.** G3: 62 agents, 4,715,110 subagent tokens. G5: 10 agents, 704,095. From the task notifications.

**Review.** An independent reviewer (Opus 5.5, a fresh agent) checked both steps against their answers, the times of
their rules and the session's record of every agent launched, and changed: the north star with four layers to
12.1% (the map's script now divides each share it prints from its counts); the map's script stops on any unnamed
stem the sample was not drawn from, as the pages said, where it had only compared their number; "names or pieces"
to "names" for the stems that leave the count; the account of the first pilot's missed controls; the scholars the
lexicon reports for G5, the decoys called "partly", and the one status that rests on a proposal without a scholar's
name; Mike's answer on the recount, recorded on every page that had called it unapproved.

