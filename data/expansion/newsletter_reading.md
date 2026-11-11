# Reading the *Meroitic Newsletter*: the method and its measured accuracy

Work of 2026-11-09 and 2026-11-10 by Claude Opus 5.5 readers. **The texts themselves are not in this repo.** The
scans of the *Meroitic Newsletter* (issues 1 to 30, October 1968 to 2003) are online at meroiticnewsletter.org
(a private site that serves plain HTTP), but the articles are in copyright, so the typed
readings stay on the author's machine, like the FHN readings. This page gives the method, the scripts and the
numbers, so that someone with the scans can repeat it and so that the counts used elsewhere in this repo can be
judged.

## 1. Answer first

1. **256 texts were typed** from the scans: 110 from Heyler's 1971 computer printout of REM 1001 to 1110
   (Newsletter 6) and 146 from the printed issues of 1977 to 2003 (Qasr Ibrim, Arminna, Shokan, Tabo, Sedeinga,
   Meroë and others).
2. **188 are new to the corpus**, 2,713 whole words. 7 were already in it, 10 are a second edition of another
   typed text, and 51 hold no whole word. With them the local corpus has 936 texts and 22,556 words, against
   748 and 19,066 in `corpus_v3`. The first count, on 2026-11-09, was 185: the duplicate check had joined three
   texts to texts they are not (section 6, item 8). The tests of section 5 and the test of the two leads ran on
   those 185.
3. **Measured accuracy:** 97.6% of signs on clean print and 94% to 97% on the 1971 printout, against other
   editions of the same inscriptions (section 3). A later check on the scans found that most of that gap is the
   editions' own disagreement: 0 of 21 checked differences in print and 3 of 21 in the printout were typing
   errors (section 4).
4. **No machine-readable copy of these texts was found online** on 2026-11-09 (GitHub, Hugging Face, Zenodo,
   web search). 218 of the 256 have a REM number, and Hallof's *Analytisches Wörterbuch des Meroitischen*,
   volume 7 (2024), prints the transliterations of REM 0001 to 2780 ([`NEXT_STEPS.md`](../../NEXT_STEPS.md),
   step 7).

## 2. The method

1. **Strips.** Each PDF page was rendered at four times the PDF's size and cut into overlapping strips: two a
   page for the printed issues, three for the printout.
2. **Typing.** Readers typed the texts from the strips and nothing else. They were told to copy what the page
   shows, to enlarge doubtful marks, and to mark their own doubt. The two briefs are in
   [`src/mnl/BRIEF_PRINTOUT.md`](../../src/mnl/BRIEF_PRINTOUT.md) and
   [`src/mnl/BRIEF_MODERN.md`](../../src/mnl/BRIEF_MODERN.md).
3. **The 1971 printout** uses capitals for the signs (Z for s, S for se, J for ñ, V for te, U for to, G and X for
   the two h signs), prints alternatives as `(A/B)` and marks restorations and gaps with brackets.
   `src/mnl/mnl_signs.py` reads that code. Its letters O and D both print like a C, and Q differs by a small
   tail: readers enlarge each line and go by shape, and `src/mnl/mnl_round.py` settles what is left with the
   spelling rules of the script and a 4-gram model of corpus words.
4. **Corpus spelling.** `src/mnl/mnl_build.py` turns the typing into the corpus spelling: dividers as spaces,
   lost signs as dots, numerals as digits, restorations kept as the corpus keeps them.
5. **Duplicates.** `src/mnl/mnl_dedupe.py` compares each text's distinctive letter 6-grams (formula 6-grams left
   out) with every corpus text and with Millet's example lines in Otten's repository, and marks second editions
   of one inscription. `src/mnl/mnl_corpus.py` writes the local corpus.

`python3 -I src/mnl/test_mnl.py` tests the scripts on made-up lines. `bash src/mnl/rebuild.sh <repo root>
[out dir]` rebuilds the three result files from the readers' typing, by default into `data/sources/mnl/`, which
`.gitignore` keeps out of the repo; it needs that local-only folder and stops with a message without it.
Where the typed texts are present, `python3 -I tests/test_newsletter.py` checks that the rebuild gives the files
this page counts, that this page's counts and accuracy figures come out of them, and that no typed line is in a
file git tracks.

## 3. The accuracy test, done before the harvest

Three inscriptions that Otten's files hold from other editions were typed blind and scored sign by sign:
`src/mnl/mnl_score.py millet` for Kharamadoye (against Otten's FHN file and his file of Millet's thesis),
`src/mnl/mnl_round.py test` with the list of the reading's pages for the printout (each page aligned on its own
against Otten's FHN file once the round letters are settled; `--quick` for the quick reader), and
`src/mnl/mnl_score.py pair` for the two careful readers.

| Text | Source | Reader | Agreement with the other edition |
|---|---|---|---|
| Kharamadoye (REM 0094) | Newsletter 30 (2003), clean print | one reader | 97.6% of 1,031 signs against FHN; 98.5% of 1,018 against Millet's thesis |
| Akinidad stela (REM 1003), 6 pages | 1971 printout | careful reader 1 | 95.4% of 1,634 signs |
| Akinidad stela, 2 of those pages | 1971 printout | careful reader 2 | 94.1% of 625 signs |
| Tanyidamani stela (REM 1044), 3 pages | 1971 printout | careful reader 2 | 97.0% of 900 signs |
| Tanyidamani stela, 8 pages | 1971 printout | quick reader | 93.7% of 2,172 signs |

- The two careful readers agree with each other on 97.4% of 623 signs.
- The agreement counts the other edition's signs. Signs found only in our typing are left out of it: 51 for
  careful reader 1, 6 (Akinidad) and 32 (Tanyidamani) for careful reader 2, 158 for the quick reader.
- A quick reader could not tell the printout's round letters apart (76% right after the model's help); readers
  who enlarged each line got 91% to 96% of them right. The priors for what a typed round letter is, and the
  model's weight, were set on these same test pages, so for the printout the figures are not fully out of sample.
- The harvest used the careful way, except for the quick reader's eight Tanyidamani pages (PDF pages 23 to 30),
  which it kept: they hold REM 1042 to 1048, three of them new texts with 19 whole words.
- The Abratoye stela (REM 1333, Newsletter 28) was typed twice independently: the 1,293 characters agree when
  the two h signs count as one letter. The first typing wrote every h sign alike, so it does not check which
  h sign the second typing chose (25 ḫ and 33 ẖ).
- Not tested: the typewritten issues of 1977 to 1999 (18, 21, 22, 25, 26), which hold 37 of the new texts.

## 4. Editions compared, and how much of the difference is ours

On 2026-11-10 every inscription held in two or three editions was lined up sign by sign: 21 inscriptions, 35
pairs, 9,571 signs.

1. **The editions agree on 96.2% of signs** (9,206 of 9,571). Word division differs at 5.2% of junctions,
   mostly at the printout's line ends.
2. **Our typing errors, checked on the scans.** At 45 places where our typing stands alone against another
   edition, a reader looked at the page: 38 are what the page prints, 3 are our typing errors, 1 is a look-alike
   round letter of the printout and 3 cannot be read. In print that is 0 of 21; in the printout 3 of 21, all on
   the faint Tanyidamani pages typed by the quick reader, each a faint G taken for a round letter.
3. **Where three editions exist,** our typing is rarely the odd one. For Kharamadoye, FHN stands alone 17 times,
   Millet's thesis 12 times and our typing of Millet 2003 four times, and the page prints all four as typed.
4. **Signs exchanged outside the printout:** e and o (12 places), the second h and s (12, but 10 of them are
   our test reading of Griffith's Karanòg hand copies against FHN or Carrier), l and t (6), the two h signs (6),
   a and e (5).

Limits of this check: one reader looked at the scans; the printout figure rests on 21 places.

## 5. What the new texts were used for

These tests ran on the 185 texts of the first count.

- **Two leads tested out of sample** ([`../../REPORT.md`](../../REPORT.md), "Leads 1 and 2 on texts they had
  never seen").
- **A held-out grammar test.** The new texts hold 1,078 word forms the old corpus lacks. Cutting them into a
  known word plus one of the 30 commonest endings works for about 19%, but for about 21% of made-up words of
  the same shape, so that says nothing. Prediction does better: where many old stems take two endings, giving
  the second ending to stems seen only with the first predicts 107 to 127 forms, of which 4 occur in the new
  texts (0.5 to 0.7 expected by chance); with looser rules, chosen after that result, 53 of about 1,600 (about
  9.5 expected). The four are spelling pairs (`-t` and `-te`, `-is` and `-i`); the looser rules' hits are mostly
  the known determiner and predicate endings (`-lowi` and `-lo`, `-owi` and `-o`, `-leb` and `-l`). The counts
  vary a little from run to run: the test's script, kept locally, follows Python's hash order where it breaks
  a tie for the 30th ending and draws the controls. An independent recount gave the same verdicts.
- **A blind test on the oracular decrees.** Nine of the new texts open with one formula. A solver that saw
  them with every letter swapped found 12 of the 14 points of structure that Millet (1977), Edwards and Fuller
  (2000) and Rilly (2000) published, and 8 of 20 points of meaning: the same pattern as the other blind tests
  here.
- **Meeks's 1973 word list** (Newsletter 13, 177 entries) set against Rilly's 2003 lexicon: of the 50 comparable
  meanings Meeks marked as best established, 41 are the same thirty years later; of the 66 he marked doubtful, 8.

## 6. Limits

1. One reading a page, apart from the test pages and the Abratoye stela.
2. In the printout the scan cuts off the margin with the inscription number on many pages: 59 of the 110
   printout texts have a number worked out from the order of the printout.
3. Where the printout gives alternative readings, the first is taken.
4. Word division at line ends is uncertain where the edition prints no divider there.
5. Not typed: scraps of fewer than 6 letters, words quoted in commentary, and a few texts whose pages were missed.
6. Names are not masked in the new texts, unlike the older corpus, so word counts are not like for like.
7. Known faults not yet fixed: tally strokes read as numbers in six printout texts, a line label read as a
   number in REM 1019 and REM 1090, a lost last letter in REM 1062, and the three faint-G places of section 4.
8. The duplicate check had joined three texts to texts they are not: the collation of section 4 found that REM
   1051 and REM 1054, and REM 1059 and REM 1073, are two objects each, and that REM 1085 is not corpus text T0792.
   Since 2026-11-10 `src/mnl/mnl_dedupe.py` names these three pairs as exceptions, and the three texts count as
   new (188, not 185). The files of the first count are kept beside the new ones.
