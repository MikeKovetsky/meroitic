# Karanòg: Griffith's hand copies, read and checked against his own printed type

Work of 2026-11-10 by Claude Opus 5.5 readers. Source: F. Ll. Griffith, *Karanòg: The Meroitic Inscriptions of
Shablûl and Karanòg* (1911, public domain),
[archive.org `karangmeroitic00grifuoft`](https://archive.org/details/karangmeroitic00grifuoft). It follows
[`../hand_copy_test.md`](../hand_copy_test.md), where one reader got 88.8% of signs from the hand copies alone.

## 1. Answer first

1. **All 151 inscriptions that have a hand copy are read:** Kar. 1 to 132 and Sh. 1 to 19, with 16,440 signs and
   2,915 words (Griffith gives no copy of Sh. 20). They are in [`griffith_karanog.jsonl`](griffith_karanog.jsonl).
   `src/expand.py` adds all 151 to the corpus as `corpus_v5`: 899 texts and 21,981 words, against 748 and
   19,066 in `corpus_v3`, which stays as it was. Its duplicate test used to hold back three short texts (Kar. 63,
   Kar. 66, Sh. 17) that share half their letter groups with an older text through the closing formulae; for
   these rows it now leaves out the groups of six letters that 20 or more corpus texts share, and finds no copy.
2. **Measured accuracy: 97.7% of signs** on the four Karanòg texts that FHN III prints (Kar. 47, 77, 78 and the
   spout of 121), read by fresh readers who could not see FHN. From the hand copies alone the same readers had
   89.0%, as the first test's single reader had 88.8%. The bar set in `NEXT_STEPS.md` was 95%. The measure is the
   first test's: the signs right are FHN's signs less the edit distance, so a sign the reading has and FHN has not
   counts against it too.

| Text | Signs in FHN | Hand copy alone | After the check |
|---|---|---|---|
| Kar. 47 (REM 0247) | 268 | 243 (90.7%) | 268 (100%) |
| Kar. 77 (REM 0277) | 134 | 115 (85.8%) | 128 (95.5%) |
| Kar. 78 (REM 0278) | 206 | 186 (90.3%) | 202 (98.1%) |
| Kar. 121, spout (REM 0321) | 46 | 38 (82.6%) | 41 (89.1%) |
| All four | 654 | 582 (89.0%) | 639 (97.7%) |

3. **A second edition agrees.** Against Carrier's readings of Kar. 47, 77 and 78 (*Meroitic Newsletter* 28,
   2001; in copyright, kept locally, so only the count is given) the checked readings have 598 of 609 signs right
   (98.2%), by the same measure.
4. **What made the difference** is that Griffith printed most words of every inscription a second time, in clean
   type, in the same book. The check against those pages changed 2,405 of the 16,759 signs first read (14.4%; a
   lost sign counts as one).
5. **Two readers agree on 97.7% of signs.** Eleven of the 53 pages (31 inscriptions) were read again by a second
   reader who saw nothing of the first reading. After the check the second reading has 3,180 of the first
   reading's 3,254 signs (97.7%): 97.0% on the seven most damaged pages and 99.1% on three pages drawn at random.
   From the hand copies alone the two agree on 86.0%. The 56 places where they differed were then settled against
   the copy and the type, which changed 26 signs of the first reader's rows (0.8%); section 6. This figure and the
   97.7% of point 2 are two measures that happen to come out alike: this one says how far a second reader gets the
   same signs, that one how far a reading matches a modern edition.
6. **The rows are uniform where Griffith decides:** the closing formulae are divided into words as his formula
   tables divide them in every row, and the title `slẖs` has one spelling (section 5).

## 2. The method

Griffith gives the Karanòg and Shablûl texts only as hand copies (pp. 129 to 181). But four other parts of the
book print their words in Meroitic type, each with the number of the inscription it comes from:

| Part of the book | Printed pages | What it prints |
|---|---|---|
| Chapter V, the terminal formulae | 42 to 53 | each inscription's own wording of the closing formulae A to J, in tables |
| Table of names and parentage | 87 to 94 | the name of the deceased (column A), of the mother (B) and of the father (C) |
| Indexes A and B | 95 to 109 | titles and descriptive phrases, by first word and by last word |
| Index C | 110 to 122 | single words and groups |

1. **The 48 pages were typed** by twelve readers, four pages each, from three strips a page cut from the
   archive.org PDF: 2,718 typed objects ([`refs/typed/`](refs/typed/), the brief is
   [`refs/BRIEF_typing.md`](refs/BRIEF_typing.md)). Page 42, the first of chapter V, ties no form to an
   inscription, so its file is empty. `src/karanog_refs.py` adds the 4 names cells where the second typing
   (section 3) differs from the first, 2,722 objects in all ([`refs/all_refs.jsonl`](refs/all_refs.jsonl)), works
   out which inscriptions each object names and writes one table per inscription
   ([`refs/by_inscription/`](refs/by_inscription/)): 3,550 entries, at least two for each of the 152 inscriptions.
2. **Step 1, the copy alone.** A reader gets one or two page scans, Griffith's sign table and the notes on the
   hand from the first test, and reads every inscription sign by sign from enlarged crops. The file is then made
   read-only ([`readings/BRIEF_step1.md`](readings/BRIEF_step1.md)). No typed reference was in a reader's folder
   during this step (for the first five packs the references did not exist yet).
3. **Step 2, the check.** The same reader gets its inscriptions' entries and the printed pages. Where an entry
   and the reading differ, it looks at the copy and at the type again. The type usually wins, because it is
   Griffith's considered reading of the same signs; where the copy clearly shows something else, the copy is
   kept and the place is listed ([`readings/BRIEF_step2.md`](readings/BRIEF_step2.md)).
4. **The rows.** `src/karanog.py` turns the checked readings into rows like the other
   `data/expansion/griffith_*.jsonl` files: `text_std` as read (with line numbers, `?`, `[.]` and Griffith's
   `(sic)`), `text_corpus` in the corpus spelling (section 5), and notes that say what the check did and give the
   measured accuracy. For the 31 inscriptions read twice the row holds the settled reading (section 6).

Blindness: every reader worked in a folder of its own and was told to open nothing else and not to use the web.
FHN's texts were on the machine and are in this repo; nothing but the instruction kept a reader from them.

## 3. How well the type was typed

One further reader typed four of the 48 pages a second time without seeing the first typing
(`runs/work/karanog/compare_typings.py` compares the two).

| Page | Signs compared | The same | |
|---|---|---|---|
| Formula A table (p. 43) | 780 | 766 (98.2%) | 13 of the 14 are one row printed "(as the last)", which one typist filled in and the other left empty |
| Names, first page (p. 87) | 398 | 389 (97.7%) | see below |
| Index A (p. 97) | 646 | 643 (99.5%) | |
| Index C (p. 114) | 568 | 565 (99.5%) | |

- **The names table is the weak part.** Its type joins i to the sign before it. The first typist of the names of
  Kar. 1 to 71 typed a joined b and i as "ii" (corrected by rule in `src/karanog_refs.py`: Griffith's own English
  forms, Sharbiye and Trebiñti, show the b) and took m for ẖ in places. The second half of the table (Kar. 72 to
  Sh. 20) was typed once only, and its typist marked many p/k and 3-shaped signs as unsure.
- **The readers checked the type themselves** where it mattered: in step 2 they recorded 66 typed entries that
  the printed page does not bear out (`ref_corrections.jsonl` in each pack), among the 3,468 entries they placed.
  Most are a 3-shaped sign (m, ẖ or s) in a name.
- A sign note for future typists: two typists report that in this type ñ is the plain caret and d the λ with a
  hooked foot (Griffith's table, rows 11 and 23), and that the description of the two in
  `../printed_type_test.md` reads the other way round. No typist's output shows the swap: all write `yetmde`,
  `akiñ`, `pedeme` and `kdi` as they should be.

## 4. What the check did, by pack

| Pack | Inscriptions | Signs first read | Signs changed | Printed entries placed | Copy kept against the type | Typed entries corrected |
|---|---|---|---|---|---|---|
| C01 | Kar. 1 to 7 | 572 | 75 | 123 | 9 | 3 |
| C02 | Kar. 8 to 10 | 385 | 36 | 78 | 1 | 6 |
| P03 | Kar. 11 to 16 | 599 | 97 | 122 | 6 | 3 |
| P04 | Kar. 17 to 20 | 562 | 51 | 114 | 9 | 3 |
| P05 | Kar. 21 to 24 | 602 | 101 | 118 | 14 | 1 |
| P06 | Kar. 25 to 29 | 700 | 105 | 137 | 8 | 1 |
| P07 | Kar. 30 to 35 | 599 | 96 | 115 | 7 | 2 |
| P08 | Kar. 36 to 40 | 668 | 117 | 128 | 9 | 3 |
| P09 | Kar. 41 to 46 | 585 | 62 | 100 | 4 | 2 |
| C09 | Kar. 47, 48 | 347 | 37 | 94 | 8 | 3 |
| P10 | Kar. 49 to 54 | 697 | 106 | 155 | 9 | 1 |
| P11 | Kar. 55 to 60 | 753 | 209 | 142 | 13 | 0 |
| P12 | Kar. 61 to 66 | 630 | 47 | 118 | 8 | 3 |
| P13 | Kar. 67 to 72 | 799 | 140 | 187 | 8 | 1 |
| P14 | Kar. 73 to 75 | 312 | 56 | 63 | 8 | 3 |
| C14 | Kar. 76 to 79 | 618 | 74 | 143 | 9 | 1 |
| P15 | Kar. 80 to 85 | 526 | 92 | 99 | 11 | 0 |
| P16 | Kar. 86 to 90 | 672 | 89 | 127 | 5 | 0 |
| P17 | Kar. 91 to 97 | 756 | 75 | 156 | 7 | 1 |
| P18 | Kar. 98 to 102 | 680 | 102 | 137 | 10 | 2 |
| P19 | Kar. 103 to 110 | 557 | 150 | 145 | 8 | 2 |
| P20 | Kar. 111 to 117 | 572 | 49 | 126 | 7 | 1 |
| P21 | Kar. 118 to 120 | 282 | 32 | 49 | 5 | 2 |
| C21 | Kar. 121 to 123 | 273 | 15 | 54 | 6 | 1 |
| P22 | Kar. 124 to 128 | 734 | 119 | 190 | 13 | 2 |
| P23 | Kar. 129 to 132, Sh. 1 to 3 | 679 | 97 | 142 | 8 | 6 |
| P24 | Sh. 4 to 7 | 523 | 41 | 104 | 5 | 2 |
| P25 | Sh. 8 to 13 | 532 | 68 | 95 | 8 | 8 |
| P26 | Sh. 14 to 19 | 545 | 67 | 107 | 7 | 3 |
| All | 151 | 16,759 | 2,405 (14.4%) | 3,468 | 230 | 66 |

Signs first read count a lost sign as one; the signs changed are, for each stretch where the two readings differ,
the longer side (`changed()` in `src/karanog.py`).

The changes are the confusions the first test listed: the 3-shaped signs (m, ẖ, s and the bowl of q), p against
k, e against l, te against o + l, and d against ñ. The 230 places where the copy was kept are mostly small: a
divider the type leaves out, `-lo` in the copy where an index prints `-lowi`, `pqorl` against `pqrl`. Several
are places where Griffith's indexes disagree with each other and one of them agrees with the copy.

## 5. One word division and one spelling

`text_std` is the reading as the reader wrote it and is never changed. `text_corpus` is made uniform by
`src/karanog.py` in two things that Griffith himself decides:

1. **The closing formulae are divided as his formula tables divide them.** The stones often run the words of a
   formula together (`atomẖe`), and one reader kept that while another took the division from the type
   (`ato mẖe`). Where the formula tables print two words of an inscription's own formula apart and the reading
   has them as one, the row parts them. A pair that the tables print apart for 20 inscriptions or more is parted
   in every row: `ato mẖe` (97 inscriptions), `at mẖe` (83) and `mẖe psḫrkete` (21). This adds 141 word
   boundaries in 77 rows; no row now has `atomẖe` or `atmẖe` (91 and 90 rows have the two words). The indexes are
   not used for this, because there Griffith also sets endings apart from their words (`pesto l`), which is
   analysis and not word division. A pair that he prints as one word anywhere for that inscription is left alone.
2. **The title `slẖs` has one spelling.** Two rows (Kar. 11 and Kar. 84, three words) had `slms`, where the hand's
   3-shaped signs cannot be told apart. Griffith's catalogue writes the title "shalkhash" thirteen times and never
   with m, and Indexes B and C print ẖ, so these are written `slẖs` like the other rows.

Each row whose `text_corpus` differs from its reading in this way says so in its notes, with the counts. What is
not made uniform: word division outside the closing formulae (`yidotedikte` is one word in four rows and
`yidote dikte` in two, as the copies have it), the count of lost signs in a hatched stretch, and `pqrl` against
`pqorl`, which is Griffith's own variation.

## 6. Eleven pages read twice

**How the pages were chosen** ([`second_reading/pick.json`](second_reading/pick.json)): the seven pages with the
most lost signs and query marks in the rows; three of the other 46 drawn at random with a fixed seed; and the
page of Kar. 77, which FHN III prints, as a control. Each page went to a new reader with the briefs and files of
the first run and none of its results: step 1 from the copy alone, step 2 the check against the type
([`second_reading/<pack>/`](second_reading/), pack S and the leaf number).

**The measure** is the one used against FHN: the signs of the first reading less the edit distance between the
two readings, so a sign only one reader has counts against it. Lost signs are left out and counted apart
(`runs/work/karanog/compare_readers.py`).

| Pages | Inscriptions | Signs of the first reading | Second reader has, hand copy alone | Signs, after the check | Second reader has, after the check |
|---|---|---|---|---|---|
| The seven most damaged | 22 | 2,036 | 1,708 (83.9%) | 2,061 | 1,999 (97.0%) |
| Three at random | 7 | 926 | 823 (88.9%) | 948 | 939 (99.1%) |
| Control (Kar. 76, 77) | 2 | 244 | 226 (92.6%) | 245 | 242 (98.8%) |
| All eleven | 31 | 3,206 | 2,757 (86.0%) | 3,254 | 3,180 (97.7%) |

- Ten of the 31 inscriptions came out the same sign for sign after the check; none did from the copies alone.
- The weakest are short, badly hatched texts: Kar. 80 (20 of 27 signs), Kar. 43 (47 of 59) and Kar. 81 (86 of 98).
- The readers count lost signs alike in the sum (198 and 195) but differently in 15 of the 31 inscriptions.

**Settling** ([`readings/BRIEF_step3.md`](readings/BRIEF_step3.md)). The second reader then received the first
reading and the list of the 56 places where the two checked readings differ in a sign (in 21 inscriptions), looked
at the copy and the type again at each, and gave a verdict:

| Verdict | Places |
|---|---|
| The first reading is right | 26 |
| The second reading is right | 17 |
| Neither is right | 2 |
| The copy and the type do not decide (the first reading stands, with a `?`) | 11 |

The evidence was the copy alone at 25 places, the type alone at 6 and both at 25. The settled readings
(`settled.jsonl`, with `decisions.jsonl` for each place) are the rows of these 31 inscriptions. They differ from
the first reader's checked readings in 26 of 3,254 signs (0.8%). One of the 26 is the disputed sign of the
formula word `yidotedikte` in Kar. 100, d and not n, so that every row now has d.

**What this says about the other 120 inscriptions.** Where two readers differed and the place could be decided,
the first reader was wrong at 19 places of 45. On the three random pages the two readings differ at 9 places in
948 signs: five went to the first reader, one to the second and three stayed open. So a second reading of an
ordinary page would change few signs of a row; on a badly hatched page it changes more (on the seven damaged
pages the readings differ at 45 places, of which 18 went against the first reader and 8 stayed open). It says
nothing of signs that both readers get wrong in the same way.

**The control shows that limit.** Against FHN the first reader has 128 of the 134 signs of Kar. 77 right, the
second reader 127, and the settled reading 128: settling changed nothing there. Both readers differ from FHN in
the same three signs, and each time they have what Griffith prints in type (`smede(?)li`, `ps(?)te`, `ḫblol`)
where the modern edition reads otherwise (`Smedtli`, `ph̲te`, `ḫ*mlol`). Two readers who agree have recovered
Griffith's reading, not necessarily the stone.

## 7. Limits

1. **Four texts and 654 signs** carry the accuracy figure, and FHN prints no other Karanòg text. Kar. 47, the
   longest of the four, has no closing formulae and is covered by 79 printed entries; a text with a long
   unparalleled name is covered less.
2. **Agreement with FHN mostly measures how well Griffith's reading was recovered.** FHN and Carrier follow his
   copies, with their own corrections. Where Griffith misread the stone, so do these rows.
3. **The notes on the hand** given to the readers were written during the first test on these same four texts,
   so the "hand copy alone" column is not fully independent. The check against the type is.
4. **One reader for 120 of the 151 texts.** Thirty-one were read twice (section 6); the 147 texts without an FHN
   edition have no outside check at all. The weakest are the heavily hatched ones (among them Kar. 30, 36, 45,
   102, 112, Sh. 2 and Sh. 17), where the number of lost signs is a reader's estimate.
5. **The second reading is not a second opinion on Griffith.** Both readers checked against the same typed
   pages, so an error in the typing that neither caught is in both readings. And the reader who settled the
   differences was the second reader itself, not a third: it decided for the first reading more often than for
   its own (26 against 17), but it was no neutral judge.
6. **Word division outside the closing formulae follows each reader's judgment** (section 5).
7. **Names are not masked** (no name list exists for these texts), as in the other Griffith files.
8. **Shablûl rows will have no REM number** until the numbering is checked; Karanòg N is REM 0200 + N (FHN III).
9. **Readers did not all check alike.** The brief says to look at the printed strip wherever an entry and the
   copy differ. Several readers report that they did so for the names table only and took index and formula
   entries as typed. The two signs that readers had settled differently are now the same in every row: d in the
   formula word `yidotedikte` (the typed formula tables have n there, which the readers who looked at the strips
   corrected) and ẖ in the title `slẖs` (sections 5 and 6).
10. **Outages.** The machine lost its network three times during the second day's run. Every reader was cut off at
   least once and went on from its own record of the work; no reading was redone.
11. **One line left out.** The first line of Kar. 113 is an Egyptian name in Demotic, which Griffith gives in
    italics; its reader took it out of the Meroitic reading (`changes.jsonl` of pack P20).
12. **Two printed entries were checked by no reader,** the second readers included: Kar. 17 `sotnkel` and
    Kar. 111 `tewideqowi` (section 9). Their pages were not among the eleven.

## 8. Cost

About 14 million subagent tokens for the first run: 3.8 million for typing the 48 reference pages, 0.4 million
for the second typing of four of them, and about 10 million for the 53 pages of hand copies (about 190,000 a page
for both steps). A reader needs about an hour a page for step 1 and five to ten minutes for step 2. The second
reading of eleven pages took 3.4 million more (about 310,000 a page for the three steps).

## 9. Files, and how to rebuild

```
python3 -I src/karanog_refs.py     # refs/typed/ and refs/second_typing/ -> refs/by_inscription/, refs/all_refs.jsonl
python3 -I src/karanog.py          # readings/<pack>/ and second_reading/<pack>/ -> griffith_karanog.jsonl
python3 -I tests/test_karanog.py   # checks for the scripts, and the numbers in this file
python3 -I runs/work/karanog/score_fhn.py . "after the check" data/expansion/karanog/readings/C09/final.jsonl \
    data/expansion/karanog/readings/C14/final.jsonl data/expansion/karanog/readings/C21/final.jsonl
python3 -I runs/work/karanog/score_fhn.py . "hand copy alone" data/expansion/karanog/readings/C09/copy_only.jsonl \
    data/expansion/karanog/readings/C14/copy_only.jsonl data/expansion/karanog/readings/C21/copy_only.jsonl
python3 -I runs/work/karanog/compare_typings.py   # section 3
python3 -I runs/work/karanog/compare_readers.py   # section 6: the two readers, inscription by inscription
```

`score_fhn.py` scores against Carrier too where his texts are on the machine (`data/sources/mnl/`, kept locally).

- `refs/typed/<typist>/ref_pdfNNN.jsonl`: the typed pages (NNN is the PDF page, the printed page plus 16).
  `refs/second_typing/QA/`: the four pages typed twice.
- `readings/<pack>/`: `copy_only.jsonl` (step 1, frozen), `final.jsonl` (after the check), `changes.jsonl`,
  `kept_against_type.jsonl`, `unplaced.jsonl`, `ref_corrections.jsonl`.
- `second_reading/<pack>/`: the second reader's files of the same names for one page, and `settled.jsonl` (the
  first reader's objects with the settled places put in) and `decisions.jsonl` (one line a differing place: both
  readings, the signs chosen, the verdict, the evidence and why). `second_reading/pick.json` says how the pages
  were chosen.
- The page scans are not in the repo: leaves n144 to n196 of the archive.org item, 3132 x 4094 px. The PDF of the
  same item shows the hand copies too blurred for this (hatching and dots are lost); the type pages were read
  from it.
- The readers of the first five packs (C01 to C21) received `refs/by_inscription/` as it stood before two fixes
  to `src/karanog_refs.py` (it then took the numbers of ostraca, "form D 2", footnotes and the second page of
  "see pp. 45, 48" for inscription numbers). All 26 wrong entries this gave them are among the 39 they reported as
  not placeable. The other 24 packs received the corrected tables, which are the ones here but for five entries.
- Five index entries were added to the tables after the check, so no reader saw them: `src/karanog_refs.py`
  took no number from "Kar. 72, 75¹" (a footnote mark) or from "ib." (the inscription of the entry above). Three
  of the five words were in the readers' tables through another entry: Kar. 55 `sqdyeqowi` (names table),
  Kar. 75 `womnitẖ` (Index C) and Kar. 124 `smle` (Indexes A and B). Two were checked by no reader: Kar. 17
  `sotnkel` and Kar. 111 `tewideqowi` (the reader of Kar. 111 found no `tewide` in that copy either).
- The 4 names cells from the second typing were added to the tables after the check, so no reader saw them:
  Kar. 6 `tmiye` and `(mli)tmide`, Kar. 8 `ḫdokẖ(?)liqowi` and `ñbeyrosmi`. The readings have `tmiye`,
  `m(7)litmide` and `ñbeyrosmi`, and `ḫdokm?(3)liqowi` where the second typing has ẖ(?).
