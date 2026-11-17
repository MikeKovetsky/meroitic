# Faras: Griffith's funerary texts of 1922, typed from his hand copies

Work of 2026-11-17 by Claude Opus 5.5 readers. Source: F. Ll. Griffith, "Meroitic funerary inscriptions from
Faras, Nubia", in *Recueil d'études égyptologiques dédiées à la mémoire de Jean-François Champollion* (Paris 1922),
pp. 565-600, public domain, [archive.org `bibliothquedel234ecol`](https://archive.org/details/bibliothquedel234ecol)
(PDF pages 601 to 648). Step 8 of [`NEXT_STEPS.md`](../../../NEXT_STEPS.md), section B.

## 1. Answer first

1. **All 46 texts are typed and in `corpus_v6` as open readings of REM 0501 to 0546.** 3,865 signs and 762 words
   (in the corpus spelling, with 388 lost signs and 231 query marks), in 217 rows of the copies. The run stopped
   at the line of 2.5 million subagent tokens after Faras 1 to 23; Mike's word ("Yes, both picks": type 24 to 46
   only if 1 to 23 met their bar) started the second half once the bar was met. Cost: 4,988,040 subagent tokens
   in all (section 7).
2. **What the article prints.** 46 texts. For each: a description of the object, Griffith's hand copy of the text
   in Meroitic cursive, and his English rendering, which spells the names, titles and formula words in Latin letters
   ("O Wêsh! O Ashêri! The qêreñ-akarêrê Malêwitar : begotten of Anashayi : born of Shayêkeli. (Formulae A B.)").
   Notes on the formulae close the article (pp. 599-600, PDF 647-648), with variants by text number in his
   transliteration. Plates VIII to XI are photographs, Plates XII and XIII Mrs. Griffith's sketches of the other
   monuments. There is **no transliteration of whole texts and no index** like Karanòg's: every sign is read from
   the hand copies, and his Latin letters check only the names, titles and formula words. The texts are altars
   with one to three lines round the border and stelae of four to eighteen lines (section 3).
3. **The typing measured: the bar is met.** Five texts drawn by lot before typing (Faras 2, 10, 13, 14, 15;
   [`BAR.md`](BAR.md), committed first) were typed again by a fresh reader who saw nothing of the first typing. After
   each reader's check against Griffith's Latin letters the two agree on **373 of 382 signs (97.6%)**; the bar was
   95%. Before the check they agreed on 331 of 376 (88.0%), much as two readers of Karanòg's copies did before their
   check (86.0%).
4. **Against the modern readings the corpus holds** (letters spelled alike, section 4): Faras 43 agrees with
   Millet's reading on 75 of 83 letters (90.4%); Faras 44 with Carrier's in the *Meroitic Newsletter* 28 on 253 of
   305 (83.0%) and with Millet's on 204 of 284 (71.8%); eleven quotations of parts in Millet's thesis (of Faras 7,
   11, 21, 34 and 43) on 184 of 186 letters. Faras 44's lower half is scaled away, and Griffith's copy gives 64 of
   its signs as lost.
5. **What the corpus already held.**
   - By REM number: **Faras 44** (REM 0544), in Millet's reading (Otten's file), Carrier's (Newsletter 28) and FHN 271.
   - **Faras 43** (REM 0543) is a text of Millet's thesis that the corpus counted as "not identified": his example
     line 286 (pp. 238-240) is the same text word for word, Tasamerekh's archaic altar, where the corpus page had
     guessed Meroë 28. The matching rule calls the pair doubtful (49% and 53% of their own runs, under the 60% of a
     sure match), and a verdict of 2026-11-12 had set the line apart from the candidates then (Meroë 27 and 28);
     two fresh readers, each on its own, now named Faras 43 as the whole text (sure 5 of 5, both), and the line is
     a reading of REM 0543 ([`verdicts.jsonl`](verdicts.jsonl)).
   - **Faras 21** (REM 0521) is quoted by seven of Millet's example lines; one of them, line 414 (ll. 26-28 of the
     copy), also stood as an inscription not identified and is now a phrase of REM 0521. Faras 7, 11, 34 and 43 take
     one phrase each, and **Faras 38** the line 779 (`pesto mXes pesto n.....`), which waited for readers and which
     both new readers gave to it (sure 3 and 4).
   - Faras 2 shares its title chain with Griffith's *Inscr.* 129 (REM 0129), the British Museum stela of the same
     man, Malêwitar, and Faras 4 its extended invocation with REM 1062 of the Newsletter: two monuments each, not
     one text ([`comparison.json`](comparison.json)).
6. **`corpus_v6` now:** 606 inscriptions (563 before: 45 new numbers, two fewer "not identified"), 350 with an open
   reading (304), 591 texts and 10,962 words (548 and 10,290).
7. **What recurs now: little.** The map holds 1,681 open spellings that stand in one of its texts (1,678 with
   Millet's lines 286 and 414 left out, which are Faras 43 and a part of Faras 21). **5 of them now stand in a new
   Faras text too** (`anSyi`, `ete`, `qoredeklo`, `wyekite`, `yeqo`), and 5 open spellings reach three texts (`md`,
   `mesn`, `mkl`, `mleyos`, `tes`); `ete`, `yeqo` and `tes` are pieces the readers' word division left, not words.
   Of the 313 distinct spellings of the 44 texts new to the map (a word with a lost sign left out; no name is
   marked in these rows), 128 are on the map already, 29 of them open; 185 are new to it, and 2 of those stand in
   two Faras texts. The map is unchanged: it holds the 548 texts the analysts glossed, and its studies and its
   plain lookup ("before us" on the scoreboard) read those texts, not the grown `corpus_v6` (section 5).

## 2. The method

1. **The page images.** The PDF's scans are 2756 x 4515 px a page (JPX); the pages were rendered at 400 dpi with a
   small Swift tool on CoreGraphics (no PDF library is installed),
   [`runs/work/faras/pdfpng.swift`](../../../runs/work/faras/pdfpng.swift).
   The text layer of the PDF drops the Meroitic altogether and the marks of his Latin letters; nothing was typed
   from it.
2. **The copies cut out.** Each copy was placed on its page by its ink lines (`pdfpng lines`: the copy starts under
   the heading "N° n" and ends before the first line that fills the printed measure; placed by eye from the lines
   where the heading runs into the first row, [`locate.py`](../../../runs/work/faras/locate.py)) and cut into an
   overview at 0.65 of the scan, pieces enlarged 1.5 times (each at most 950 x 330 px of the scan, with 50 px of
   its neighbours to either side and 30 above and below), and a context crop at half size with the description,
   rendering and notes, [`cut2.py`](../../../runs/work/faras/cut2.py), which holds every position. The first pack
   (Faras 1 to 4) had whole pages and cut its own crops.
3. **The readers.** One reader (a fresh Claude Opus 5.5 subagent) a pack of four to seven texts, eight packs (A to
   H) in two waves, in a folder of its own, told to open nothing else and not to use the web:
   [`readings/BRIEF.md`](readings/BRIEF.md) (the first pack's brief, before the copies were cut out, is
   `BRIEF_pack_A.md`; packs E to H had `BRIEF_packs_E_to_H.md`, which names the pages of the formula notes). For each
   text, two steps:
   - `first`: the copy alone, sign by sign;
   - `final`: checked against his Latin letters (the rendering, his notes on the text and his notes on the
     formulae). His Latin letters usually win where the copy's sign is ambiguous; where the copy clearly shows
     something else the copy is kept and the place listed (`kept`, 69 places).
   Every reader also lists the signs it could not settle (`unsure`, 238 places), which go into each row's `doubts`.
4. **His letters and today's** ([`readings/latin_key.md`](readings/latin_key.md), the key the first wave had; packs E
   to H had
   `latin_key_packs_E_to_H.md`, with Griffith's plain s as the se sign). In his
   notes: ê `o`, tê `to`, š the s sign, s the se sign, ñ, z `d`, h with a line below `ẖ`, h with a curve below `ḫ`.
   In his English renderings: sh the s sign, kh `ẖ`, ch `ḫ`, ê `o`, z `d`, and an a between consonants that the
   script does not write (Pakharas is `pẖrse`, charapachañ `ḫrpḫñ`). Checked on the corpus: `pXrs` and `xrpxN`.
5. **The blind second typing.** The five texts drawn by lot went to a fifth reader with the same kit and brief and
   none of the first readings (pack X, [`second/X/`](second/X/)).
6. **Settling.** Where the two typings of a drawn text differ, the place was settled against the page and
   Griffith's notes ([`settled.jsonl`](settled.jsonl)): 12 places, 3 of them only in word division. One sign of the
   first readers' rows changed: Faras 15 `psẖte` is `psmte`, as his note on formula A says ("in nos 9, 15, 19, 22,
   mte for ẖte"). Where neither the page nor his notes decide, the first reading stays, marked doubtful.
7. **The rows.** [`src/faras.py`](../../../src/faras.py) writes [`griffith_faras.jsonl`](griffith_faras.jsonl): one
   row per text, shaped like the other Griffith rows. `text_std` is the reading as written (line numbers `(N)`,
   `?`, `[.]` for a lost sign, `[x]` for his restorations, `(sic)`); `text_corpus` is the corpus spelling (the s sign
   `S`, se `s`, ñ `N`, ḫ `x`, ẖ `X`; a lost or restored sign is `.`; a numeral of the stone, the 1 after each
   prince of Faras 44, is a word of its own). Two things make the division uniform, as in the Karanòg rows: a gap
   of the copy inside a word is closed where the parts together spell a word that stands in three or more of the
   other public Griffith rows (`so (2) reyi` is `Soreyi`, `a(6) t` is `at`: 21 gaps in 9 texts; a divider is
   never crossed, and nor is a word end that a formula pair parts again: `ato mẖe` stays two words, though three
   of those rows write `atomẖe`), and the closing formulae are parted by the 17 pairs Griffith's Karanòg formula
   tables print apart five times or more (`ato mẖe`, `at mẖe`, `mẖe psḫrkete`). `rendering` keeps his English
   rendering, `doubts` the reader's unsure places, `notes` what the check changed and, for the drawn texts, the
   agreement of the two typings.
8. **REM numbers.** Faras n is REM 05nn, as Karanòg n is REM 02nn: three passages of the *Meroitic Newsletter*
   agree ("Atpil (REM 0503/3)", the second name of Faras 3, in REM's l. 3 and Griffith's l. 2; the extended
   invocation "at Faras (REM 0534, 0538, 0544)", Griffith's nos. 34, 38 and 44; and "REM 0501 & 0546"), and
   corpus_v6's REM 0544 is the epitaph of Makheye that Griffith prints as no. 44.
9. **Into `corpus_v6`.** [`src/v6/readings.py`](../../../src/v6/readings.py) reads this folder like the folder of REM
   1003 (`../jea/`): texts an article prints, with a REM number, no number of Griffith's and no row of `corpus_v5`.
   `src/expand.py` does not read sub-folders, so `corpus_v3` and `corpus_v5` are as they were.

## 3. The texts

| Text | REM | Pack | What Griffith says of the writing | Rows of the copy | Signs | Words | Lost | Changed by the check |
|---|---|---|---|---|---|---|---|---|
| Faras 1 | 0501 | A | two lines of late writing | 4 | 40 | 7 | 1 | 1 |
| Faras 2 | 0502 | A | one line of late writing | 3 | 83 | 15 | 0 | 0 |
| Faras 3 | 0503 | A | ten lines of late writing, the first seven between rules | 7 | 153 | 23 | 0 | 4 |
| Faras 4 | 0504 | A | fifteen horizontal lines between rules | 6 | 171 | 24 | 0 | 0 |
| Faras 5 | 0505 | B | one line of late writing round the edge | 4 | 39 | 9 | 37 | 8 |
| Faras 6 | 0506 | B | one line of late writing round edge, worn | 3 | 65 | 14 | 5 | 19 |
| Faras 7 | 0507 | B | two lines of late inscription round the border | 4 | 88 | 18 | 5 | 15 |
| Faras 8 | 0508 | B | one line of late inscription on border | 4 | 58 | 12 | 15 | 16 |
| Faras 9 | 0509 | B | one line and part of a second, round the border | 4 | 67 | 14 | 0 | 10 |
| Faras 10 | 0510 | B | nine lines of late writing between rules | 7 | 137 | 25 | 0 | 51 |
| Faras 11 | 0511 | B | eight lines of late writing | 4 | 56 | 12 | 18 | 12 |
| Faras 12 | 0512 | C | a line round the border, partly doubled | 3 | 59 | 11 | 0 | 3 |
| Faras 13 | 0513 | C | small late characters on the spout and the border | 3 | 69 | 14 | 6 | 2 |
| Faras 14 | 0514 | C | one line of late inscription on the border | 2 | 26 | 3 | 3 | 4 |
| Faras 15 | 0515 | C | a line of late writing round the border | 4 | 67 | 13 | 0 | 7 |
| Faras 16 | 0516 | C | four lines of late writing | 3 | 34 | 6 | 3 | 4 |
| Faras 17 | 0517 | C | two lines of late writing round the border | 5 | 123 | 21 | 5 | 11 |
| Faras 18 | 0518 | C | seven lines of neat late writing | 2 | 66 | 9 | 0 | 12 |
| Faras 19 | 0519 | D | one to two lines of late transitional writing | 5 | 81 | 16 | 0 | 9 |
| Faras 20 | 0520 | D | two to three lines of transitional writing | 4 | 86 | 13 | 2 | 11 |
| Faras 21 | 0521 | D | three lines on the border, four in the field | 15 | 321 | 56 | 15 | 26 |
| Faras 22 | 0522 | D | one to two lines of late writing on border | 4 | 60 | 12 | 1 | 1 |
| Faras 23 | 0523 | D | one line of late inscription round the border | 6 | 85 | 15 | 1 | 5 |
| Faras 24 | 0524 | E | one line of late writing round border carried into sunk field | 7 | 92 | 22 | 7 | 17 |
| Faras 25 | 0525 | E | one line of late writing round the border continued on the field | 4 | 63 | 15 | 0 | 13 |
| Faras 26 | 0526 | E | one line round the border, continued in the field and spout | 5 | 90 | 22 | 0 | 13 |
| Faras 27 | 0527 | E | round the border one line of late writing and part of a second line | 3 | 70 | 15 | 2 | 14 |
| Faras 28 | 0528 | E | two lines of late inscription round the border | 5 | 126 | 30 | 4 | 58 |
| Faras 29 | 0529 | E | one line of late inscription round border and in spout | 3 | 62 | 13 | 0 | 4 |
| Faras 30 | 0530 | F | round the border one line of late inscription | 3 | 77 | 13 | 1 | 14 |
| Faras 31 | 0531 | F | two lines of late inscription round the border | 3 | 63 | 14 | 11 | 13 |
| Faras 32 | 0532 | F | one line in small late characters round the border, worn away in places | 3 | 60 | 13 | 17 | 12 |
| Faras 33 | 0533 | F | inscribed with eight lines of late writing | 3 | 63 | 15 | 20 | 8 |
| Faras 34 | 0534 | F | inscription of two lines of late writing round the border | 11 | 183 | 30 | 1 | 25 |
| Faras 35 | 0535 | F | inscription of one line of late writing round the border | 5 | 95 | 16 | 1 | 12 |
| Faras 36 | 0536 | G | one line of late writing round the border | 4 | 63 | 13 | 2 | 2 |
| Faras 37 | 0537 | G | two lines of late writing between incised lines | 6 | 89 | 15 | 20 | 4 |
| Faras 38 | 0538 | G | remains of three lines of late inscription round the border | 5 | 44 | 13 | 24 | 7 |
| Faras 39 | 0539 | G | one line of late inscription round the border | 2 | 27 | 6 | 0 | 1 |
| Faras 40 | 0540 | G | eight lines in red ink, faint; the copy is from a conventionalised reading | 3 | 56 | 13 | 0 | 1 |
| Faras 41 | 0541 | G | six lines much worn and portions of others, running obliquely | 7 | 91 | 18 | 73 | 8 |
| Faras 42 | 0542 | H | one line of late writing round the border, much defaced | 2 | 35 | 9 | 5 | 1 |
| Faras 43 | 0543 | H | one line of archaic writing round the border, two more beneath Anubis | 5 | 78 | 17 | 4 | 30 |
| Faras 44 | 0544 | H | eighteen lines between rules, the lower half much injured by scaling | 19 | 255 | 66 | 64 | 54 |
| Faras 45 | 0545 | H | one line round the border, a second round the edge of the field | 2 | 38 | 9 | 15 | 2 |
| Faras 46 | 0546 | H | (not stated) | 1 | 11 | 3 | 0 | 0 |
| **All** | | | | **217** | **3,865** | **762** | **388** | **544 (14.4%)** |

Signs, words and lost signs are counted on the rows by `src/faras.py` (`se`, `te` and `to` are one sign each; a word
has a letter or is a numeral); "changed by the check" is counted between `first` and `final` as in the Karanòg rows
(the longer side of each stretch that differs), over the 3,788 signs first read. The description of a text is
Griffith's, shortened where it is long; Faras 46 is a fragment he does not describe.

## 4. The typing measured

| Text | Signs of the first typing | Agree, after the check | Agree, before the check |
|---|---|---|---|
| Faras 2 | 83 | 83 | 74 of 83 |
| Faras 10 | 137 | 132 | 107 of 132 |
| Faras 13 | 69 | 68 | 67 of 68 |
| Faras 14 | 26 | 25 | 24 of 26 |
| Faras 15 | 67 | 65 | 59 of 67 |
| **All five** | **382** | **373 (97.6%)** | **331 of 376 (88.0%)** |

The measure is the Karanòg readers': the signs of the first typing less the edit distance between the two, lost
signs and line numbers left out ([`measure.json`](measure.json), `python3 -I src/faras.py measure`). Where they
differ: a 3-shaped sign (q against s, ẖ against m), e against l, d against ñ, se against s and a, a stroke or an e
that only one reader takes for a sign, and how many signs a hatched stretch held. What it does not measure: both
readers had the same copies and the same Latin letters, so a sign Griffith miscopied is wrong in both.

**Against modern readings** ([`comparison.json`](comparison.json), `python3 -I src/faras.py compare`; letters spelled
alike: o and e, s and se, n and ne, ḫ and ẖ):

| Text | Modern reading the corpus holds | Its letters | Agree with the typing |
|---|---|---|---|
| Faras 43 | Millet 1968, line 286 of Otten's file (the whole text) | 83 | 75 (90.4%) |
| Faras 44 | Carrier, *Meroitic Newsletter* 28 (2001) | 305 | 253 (83.0%) |
| Faras 44 | Millet 1968, line 629 of Otten's file | 284 | 204 (71.8%) |
| Faras 7, 11, 21, 34, 43 | Millet's quotations of parts (eleven lines) | 186 | 184 |
| Faras 38 | Millet's line 779, a part | 27 | 17 |

The whole texts are scored as the Karanòg readings were against FHN (the other's letters less the edit distance);
a quotation against its best stretch of the typed text. The two readings of Faras 44 differ from each other too,
and the typing gives 64 of its signs as lost where the editions restore or read them. The one sign the quotations
of Faras 21 miss is lost in Griffith's copy (`aẖrr[.]`, his akhararab), and Faras 7's doubtful `lḫ?` is `lẖ` in
Millet: the rows keep what the readers typed, since a closed reading does not correct an open one.

## 5. What adding them changed in `corpus_v6`

Two builds compared, the same code without the Faras rows and with all 46 and the two new verdicts
(`python3 -I src/v6/build.py`, 2026-11-17):

- **Inscriptions** 563 to 606, with a REM number 441 to 486, with an open reading 304 to 350, with readings from
  two editions or more 64 to 65, funerary 268 to 310, "not identified" 8 to 6. `corpus_v6` 548 to 591 texts,
  10,290 to 10,962 words.
- **Source lines of Otten's files** (1,159): 16 changed what they are or which inscription they belong to; 126 more
  only how they are placed (the number of held texts their letters stand whole in, their shares, shared runs or the
  reading they are compared with). Of the 16: Millet's lines 286 (Faras 43, now a reading) and 414 (Faras 21), which
  stood as inscriptions not identified; seven more quotations of Faras 21 and one each of Faras 7, 11, 34, 38 and
  43; line 580 now stands whole in REM 0084; lines 852 (`bedewitel`) and 1172 (`tketore`) now stand whole in two
  or three held texts and so belong to none. Line 1368 (the name `kditrye`, Faras 11) also stands in the text of
  line 489; the rule's choice, not checked. The three readings waiting for two readers are the same three.
- **The rule's measures moved**: a run of five letters that eight edition texts hold is formula, and 45 more
  funerary texts make a few more runs formula. On the pairs already known, the rule as written finds 29 sure (30
  before) and 16 doubtful (15); with the floor 31 and 14 (32 and 13). The pairs across numberings are one, Faras 43
  with Meroë 28, whose benedictions alone Griffith printed (formula only); one pair of rows with two numbers of one
  numbering (REM 0051 and REM 0052) is no longer a sure match: 12 such pairs where there were 13.
- **The coverage recount** (`src/v6/recount.py`) counts the new texts with the rest: 51.3% of all words translated
  as before (5,626 of 10,962); the inscriptions new to the corpus 38.2% (35.9% before). The inscriptions that were
  in `corpus_v5` are one fewer (288; line 414's inscription is a part of Faras 21 now).
- **The map** (`src/themap.py`) is unchanged: it holds the 548 texts the analysts glossed, and the Faras texts are
  not glossed. Its studies and its **plain lookup**, the scoreboard's "before us" for the running words and the
  spellings, read those 548 texts as the analysts glossed them (`lexicon.MAPPED`,
  `data/sources/v6/analysts/corpus.jsonl`, a copy of `corpus_v6` as it stood before the Faras rows), and F4's
  sizing reads F1's table as it stood then (`lexicon.MAPPED_TABLE`), so they stand as they were: the lookup
  translates 2,816 of 7,847 running words (35.9%) and 325 of 3,189 spellings (10.2%). Glossing the new texts, which
  would put them on the map, is not done.
- **What recurs** (`python3 -I src/faras.py recur`, [`recur.json`](recur.json)): section 1, point 7.

## 6. Faults and limits

- **Blindness.** The first readings are not all blind to the renderings: pack A cut its own crops from whole
  pages; pack X opened page previews before reading Faras 14 and 15; pack D read the notes on Faras 21 and the
  rendering of 22 before their copies; packs G and H read the formula notes (PDF pp. 647-648) during the check of
  their first text, so their later first readings knew them, and that page also carries the copy and rendering of
  Faras 46; the overviews of Faras 14 and 44 show the first line of their renderings. Each reader says so in the
  notes of the text. The bar compares the readings after the check, which see the renderings by design.
- **Pack C** took the formula notes for missing from its folder; they were there. Its formula words rest on the
  copies alone. The one place the second typing tested (Faras 15, `psẖte`) was settled by those notes. The second
  wave's brief names the pages.
- **The page numbers.** The brief told the readers that the printed page number is 36 lower than the PDF's; that
  holds only before the first plate, since each plate and its blank back carry no number (PDF p. 609 is p. 571).
  The readers give PDF pages only, and `src/faras.py` counts the printed page across the plates.
- **The key** of the first wave gave Pakharas as `pẖrs` with the s sign and did not say that his plain s in English
  is the se sign; the corpus writes `pXrs` and `pesto` with se. No typed text took the wrong sign from it (every
  Pakharas is read `pẖrse`); the second wave (packs E to H) had the key corrected.
- **Word division** follows each reader where the stone has no divider; the copies of the altars leave gaps almost
  everywhere, and pack E set spaces round Griffith's raised numbers. `text_corpus` closes a gap inside a word the
  other Griffith rows spell whole and parts the formula pairs; what is left are pieces such as `ete`, `yeqo`,
  `tes` (Faras 24 to 28) and `Stmd espesto` where Millet has `Stmdes pesto` (Faras 44). A restoration of his that
  runs over a word end (Faras 5, `terike[li teri]kelowi`) is parted there.
- **Names are not masked** and not marked: the Griffith rows carry no tags of names, so the lookup counts a name as
  an open word, as for the other Griffith rows.
- **Signs he doubts** are not all marked: a "?" he prints over a sign is typed `?`, but his renderings' "(?)" by a
  word is in `rendering` only.
- **The two new verdicts** rest on two readers each, on two items and with none of the known lines and decoys of
  the readers of 2026-11-12, who passed 12 of 12 of each.
- Readers cut far more crops than the brief allowed (pack D 102, pack H 119), which is where the tokens went.

## 7. Files, commands and cost

| File | What |
|---|---|
| [`BAR.md`](BAR.md) | the bar and the lot, committed before any reader ran |
| `readings/<pack>/readings.jsonl` | the first typing, packs A to H (Faras 1-4, 5-11, 12-18, 19-23, 24-29, 30-35, 36-41, 42-46) |
| `second/X/readings.jsonl` | the blind second typing of the five drawn texts |
| [`settled.jsonl`](settled.jsonl) | the drawn texts as settled where the two typings differ, with the reason for each place |
| [`verdicts.jsonl`](verdicts.jsonl) | two readers' verdicts on Millet's lines 286 (Faras 43) and 779 (Faras 38) |
| [`griffith_faras.jsonl`](griffith_faras.jsonl) | the rows |
| [`measure.json`](measure.json), [`comparison.json`](comparison.json), [`recur.json`](recur.json) | the measure of the typing; the matches to held readings and the agreement with the modern readings (counts and keys only); what recurs |

```
python3 -I src/faras.py               # the rows
python3 -I src/faras.py measure       # the two typings of the drawn texts
python3 -I src/faras.py verdicts      # the two verdicts into the build's verdicts (local), before the rebuild
python3 -I src/faras.py compare       # the matches to what corpus_v6 holds (local, after the rebuild)
python3 -I src/faras.py recur         # after the rebuild: what recurs on the map (local)
python3 -I tests/test_faras.py
```

**Merging this branch.** Three local steps, before the main checkout rebuilds `corpus_v6` with the Faras rows:

1. `cp data/corpus_v6.jsonl data/sources/v6/analysts/corpus.jsonl` while `data/corpus_v6.jsonl` is still the
   548-text build (the map's texts; the studies of the map read this copy, `lexicon.MAPPED`).
2. `git show 1e55987:data/inscriptions.jsonl > data/sources/v6/analysts/inscriptions.jsonl` (F1's table as it
   stood with the map; F4's sizing reads it, `lexicon.MAPPED_TABLE`).
3. `python3 -I src/faras.py verdicts` (the two verdicts into `data/sources/v6/readers/verdicts.jsonl`).

Then the rebuild: `python3 -I src/faras.py && python3 -I src/akinidad.py && python3 -I src/v6/build.py &&
python3 -I src/v6/recount.py && python3 -I src/v6/public.py && python3 -I src/themap.py && python3 -I src/faras.py
compare && python3 -I src/faras.py recur`.

**Cost:** 4,988,040 subagent tokens. Readers 4,339,767: pack A 535,784, B 494,108, C 458,865, D 535,444 (the
first wave, with X), E 487,874, F 477,019, G 412,724, H 510,781, and the blind second typing X 427,168; 2,102 tool
calls, about 45 minutes a pack, four packs at once. The two readers of Millet's lines 135,256; the full review of
the first half 513,017. About 1,000 tokens a sign of the first typing (3,912,599 for 3,865 signs). The estimate
before the first pack was 1 to 2 million for all 46 texts. No download.
