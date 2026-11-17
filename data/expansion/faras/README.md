# Faras: Griffith's funerary texts of 1922, typed from his hand copies

Work of 2026-11-17 by Claude Opus 5.5 readers. Source: F. Ll. Griffith, "Meroitic funerary inscriptions from
Faras, Nubia", in *Recueil d'études égyptologiques dédiées à la mémoire de Jean-François Champollion* (Paris 1922),
pp. 565-600, public domain, [archive.org `bibliothquedel234ecol`](https://archive.org/details/bibliothquedel234ecol)
(PDF pages 601 to 648). Step 8 of [`NEXT_STEPS.md`](../../../NEXT_STEPS.md), section B.

## 1. Answer first

1. **Cut, said first: 23 of the 46 texts are typed (Faras 1 to 23); Faras 24 to 46 are not.** The readers cost
   about 1,100 subagent tokens a sign, and the first 23 texts brought the run to 2,451,369 tokens, at the line of
   2.5 million set for this step. The other 23 would take about 2.3 million more (about 2,300 signs at the first
   typing's 995 tokens a sign); they wait for Mike's word. Their
   copies are cut and their packs are ready (section 7).
2. **What the article prints.** 46 texts. For each: a description of the object, Griffith's hand copy of the text
   in Meroitic cursive, and his English rendering, which spells the names, titles and formula words in Latin letters
   ("O Wêsh! O Ashêri! The qêreñ-akarêrê Malêwitar : begotten of Anashayi : born of Shayêkeli. (Formulae A B.)").
   Notes on the formulae close the article (pp. 599-600, PDF 647-648), with variants by text number in his
   transliteration. Plates VIII to XI are photographs, Plates XII and XIII Mrs. Griffith's sketches of the other
   monuments. There is **no transliteration of whole texts and no index** like Karanòg's: every sign is read from
   the hand copies, and his Latin letters check only the names, titles and formula words.
3. **Typed: 23 texts, 2,034 signs, 365 words** (in the corpus spelling, with 117 lost signs and 82 query marks), in
   106 rows of the copies. The texts are altars with one to three lines round the border and stelae of four to
   fifteen lines (section 3 lists what Griffith says of each).
4. **The typing measured: the bar is met.** Five texts drawn by lot before typing (Faras 2, 10, 13, 14, 15;
   [`BAR.md`](BAR.md), committed first) were typed again by a fresh reader who saw nothing of the first typing. After
   each reader's check against Griffith's Latin letters the two agree on **373 of 382 signs (97.6%)**; the bar was
   95%. Before the check they agreed on 331 of 376 (88.0%), much as two readers of Karanòg's copies did before their
   check (86.0%).
5. **What the corpus already held.** By REM number, Faras 44 (REM 0544, not typed yet). By letters, as the corpus
   build matches them: **Faras 21** (REM 0521), which Millet's thesis quotes in seven of the example lines of Otten's
   file; one of them, line 414 (ll. 26-28 of the copy, word for word), stood in `corpus_v6` as an inscription not
   identified, and is now a phrase of REM 0521. Faras 7 and Faras 11 each take one more phrase of Millet's. Faras 2
   shares its title chain with Griffith's *Inscr.* 129 (REM 0129), the British Museum stela of the same man,
   Malêwitar: a doubtful match, two monuments, not one text.
6. **Added to `corpus_v6`** as open readings of REM 0501 to 0523 (public domain, the rows CC BY 4.0): 585
   inscriptions where there were 563 (23 new numbers, one fewer "not identified"), 327 with an open reading (304
   before), `corpus_v6` 570 texts and 10,648 words (548 and 10,290).
7. **What recurs now: little.** The map holds 1,678 open spellings that stand in one of its texts. **3 of them now
   stand in a new Faras text too** (`anSyi`, `qoredeklo`, `wyekite`), and 2 open spellings reach three texts (`mkl`,
   `mleyos`). Of the 247 distinct spellings of the new texts (names and lost signs left out), 92 are on the map
   already, 17 of them open; 155 are new to it, and none of those stands in two Faras texts. The map itself is
   unchanged (it holds the 548 texts the analysts glossed); its plain lookup, "before us" on the scoreboard, now
   reads the 570 texts (section 6).

## 2. The method

1. **The page images.** The PDF's scans are 2756 x 4515 px a page (JPX); the pages were rendered at 400 dpi with a
   small Swift tool on CoreGraphics (no PDF library is installed), [`runs/work/faras/pdfpng.swift`](../../../runs/work/faras/pdfpng.swift).
   The text layer of the PDF drops the Meroitic altogether and the marks of his Latin letters; nothing was typed
   from it.
2. **The copies cut out.** Each copy was placed on its page by its ink lines (`pdfpng lines`: the copy starts under
   the heading "N° n" and ends before the first line that fills the printed measure; placed by eye from the lines
   where the heading runs into the first row, [`locate.py`](../../../runs/work/faras/locate.py)) and cut into an
   overview at 0.65 of the scan, pieces enlarged 1.5 times (at most 950 x 330 px of the scan each), and a context
   crop at half size with the description, rendering and notes, [`cut2.py`](../../../runs/work/faras/cut2.py),
   which holds every position. The first pack (Faras 1 to 4) had whole pages and cut its own crops.
3. **The readers.** One reader (a fresh Claude Opus 5.5 subagent) a pack of four to seven texts, in a folder of its
   own, told to open nothing else and not to use the web: [`readings/BRIEF.md`](readings/BRIEF.md) (the first pack's
   brief, before the copies were cut out, is `BRIEF_pack_A.md`). For each text, two steps:
   - `first`: the copy alone, sign by sign;
   - `final`: checked against his Latin letters (the rendering, his notes on the text and his notes on the
     formulae). His Latin letters usually win where the copy's sign is ambiguous; where the copy clearly shows
     something else the copy is kept and the place listed (`kept`, 26 places).
   Every reader also lists the signs it could not settle (`unsure`, 122 places), which go into each row's `doubts`.
4. **His letters and today's** ([`readings/latin_key.md`](readings/latin_key.md), the key the readers had). In his
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
   `S`, se `s`, ñ `N`, ḫ `x`, ẖ `X`; a lost or restored sign is `.`). The closing formulae are parted as the
   Karanòg rows part them, by the 17 pairs Griffith's Karanòg formula tables print apart five times or more (`ato
   mẖe`, `at mẖe`, `mẖe psḫrkete`). `rendering` keeps his English rendering, `doubts` the reader's unsure places,
   `notes` what the check changed and, for the drawn texts, the agreement of the two typings.
8. **REM numbers.** Faras n is REM 05nn, as Karanòg n is REM 02nn: three passages of the *Meroitic Newsletter*
   agree ("Atpil (REM 0503/3)", the second name of Faras 3, l. 3; the extended invocation "at Faras (REM 0534,
   0538, 0544)", Griffith's nos. 34, 38 and 44; and "REM 0501 & 0546"), and corpus_v6's REM 0544 is the epitaph of
   Makheye that Griffith prints as no. 44.
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
| Faras 5 | 0505 | B | one line of late writing round the edge | 4 | 39 | 8 | 37 | 8 |
| Faras 6 | 0506 | B | one line of late writing round edge, worn | 3 | 65 | 14 | 5 | 19 |
| Faras 7 | 0507 | B | two lines of late inscription round the border | 4 | 88 | 18 | 5 | 15 |
| Faras 8 | 0508 | B | one line of late inscription on border | 4 | 58 | 12 | 15 | 16 |
| Faras 9 | 0509 | B | one line and part of a second, round the border | 4 | 67 | 14 | 0 | 10 |
| Faras 10 | 0510 | B | nine lines of late writing between rules | 7 | 137 | 26 | 0 | 51 |
| Faras 11 | 0511 | B | eight lines of late writing | 4 | 56 | 12 | 18 | 12 |
| Faras 12 | 0512 | C | a line round the border, partly doubled | 3 | 59 | 12 | 0 | 3 |
| Faras 13 | 0513 | C | small late characters on the spout and the border | 3 | 69 | 14 | 6 | 2 |
| Faras 14 | 0514 | C | one line of late inscription on the border | 2 | 26 | 3 | 3 | 4 |
| Faras 15 | 0515 | C | a line of late writing round the border | 4 | 67 | 13 | 0 | 7 |
| Faras 16 | 0516 | C | four lines of late writing | 3 | 34 | 8 | 3 | 4 |
| Faras 17 | 0517 | C | two lines of late writing round the border | 5 | 123 | 21 | 5 | 11 |
| Faras 18 | 0518 | C | seven lines of neat late writing | 2 | 66 | 9 | 0 | 12 |
| Faras 19 | 0519 | D | one to two lines of late transitional writing | 5 | 81 | 16 | 0 | 9 |
| Faras 20 | 0520 | D | two to three lines of transitional writing | 4 | 86 | 13 | 2 | 11 |
| Faras 21 | 0521 | D | three lines on the border, four in the field | 15 | 321 | 56 | 15 | 26 |
| Faras 22 | 0522 | D | one to two lines of late writing on border | 4 | 60 | 12 | 1 | 1 |
| Faras 23 | 0523 | D | one line of late inscription round the border | 6 | 85 | 15 | 1 | 5 |
| **All** | | | | **106** | **2,034** | **365** | **117** | **231 (11.5%)** |

Signs, words and lost signs are counted on the rows by `src/faras.py` (`se`, `te` and `to` are one sign each; a word
has a letter); "changed by the check" is counted between `first` and `final` as in the Karanòg rows (the longer
side of each stretch that differs), over the 2,009 signs first read.

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
differ: a 3-shaped sign (q, s, m or ẖ), e against l, d against ñ, a stroke one reader takes for a sign, and how many
signs a hatched stretch held. What it does not measure: both readers had the same copies and the same Latin letters,
so a sign Griffith miscopied is wrong in both. No modern edition of Faras 1 to 23 is held to score them against
(the one held is of Faras 44).

## 5. What adding them changed in `corpus_v6`

Two builds compared, the same code with and without the rows (`python3 -I src/v6/build.py`, 2026-11-17):

- **Inscriptions** 563 to 585, with a REM number 441 to 464, with an open reading 304 to 327, funerary 268 to 291.
  `corpus_v6` 548 to 570 texts, 10,290 to 10,648 words.
- **Source lines of Otten's files** (1,159): 12 changed what they are or which inscription they belong to, 59 only
  their shares or the reading they are compared with. Of the 12: seven are Millet's quotations of Faras 21 (lines
  56, 58, 414, 764, 765, 985, 1248), one of Faras 7 (787), one of Faras 11 (1368, the name `kditrye`, which also
  stands in the inscription of line 489: the rule's choice, not checked); line 580 now stands whole in REM 0084;
  lines 852 (`bedewitel`) and 1172 (`tketore`) now stand whole in two or three held texts and so belong to none.
  The three readings waiting for two readers are the same three.
- **The rule's measures moved**: a run of five letters that eight edition texts hold is formula, and 23 more
  funerary texts make a few more runs formula. On the pairs already known, the rule as written finds 29 sure (30
  before) and 16 doubtful (15); with the floor 31 and 14 (32 and 13). One twin pair across numberings (Meroë 27
  with Millet's line 286) is no longer found.
- **The coverage recount** (`src/v6/recount.py`) counts the new texts with the rest: 51.3% of all words translated
  as before (5,458 of 10,648); the inscriptions new to the corpus 37.1% (35.9% before). The inscriptions that were
  in `corpus_v5` are one fewer (288; line 414's inscription is Faras 21 now).
- **The map** (`src/themap.py`) is unchanged: it holds the 548 texts the analysts glossed, and the Faras texts are
  not glossed. Its **plain lookup moves**, because it reads `corpus_v6`: running words translated 2,919 of 8,145
  (35.8%; it was 2,816 of 7,847, 35.9%), spellings 331 of 3,311 (10.0%; 325 of 3,189, 10.2%). That line is the
  scoreboard's "before us" for those two rows, which now stands on 570 texts while "now" stands on 548. Not
  settled here: glossing the new texts, or reading the lookup on the map's texts only, is the main session's call.
- **What recurs** (`python3 -I src/faras.py recur`, [`recur.json`](recur.json)): section 1, point 7. The map's
  text "Millet 1968 p. 321 (MilletExamples.txt line 414)" is left out of the count: it is ll. 26-28 of Faras 21.

## 6. Faults and limits

- **Blindness.** The first readings are not all blind to the renderings: pack A cut its own crops from whole
  pages, pack X opened page previews before reading Faras 14 and 15, pack D read the notes on Faras 21 and the
  rendering of 22 before their copies, and the overview of Faras 14 shows the first line of its rendering. Each
  reader says so in the notes of the text. The bar compares the readings after the check, which see the renderings
  by design.
- **Pack C** took the formula notes (pp. 647-648) for missing from its folder; they were there. Its formula words
  rest on the copies alone. The one place the second typing tested (Faras 15, `psẖte`) was settled by those notes.
- **The key** the readers had gave Pakharas as `pẖrs` with the s sign and did not say that his plain s in English
  is the se sign; the corpus writes `pXrs` and `pesto` with se. No typed text took the wrong sign from it (every
  Pakharas is read `pẖrse`); the key is corrected for the packs still waiting.
- **Word division** follows each reader where the stone has no divider; the copies of the altars leave gaps almost
  everywhere. Only the formula pairs are made uniform.
- **Names are not masked** and not marked: the Griffith rows carry no tags of names, so the lookup counts a name as
  an open word, as for the other Griffith rows.
- **Signs he doubts** are not all marked: a "?" he prints over a sign is typed `?`, but his renderings' "(?)" by a
  word is in `rendering` only.
- Readers cut far more crops than the brief allowed (pack D 102), which is where the tokens went.

## 7. Files, commands and cost

| File | What |
|---|---|
| [`BAR.md`](BAR.md) | the bar and the lot, committed before any reader ran |
| `readings/<pack>/readings.jsonl` | the first typing, packs A to D (Faras 1-4, 5-11, 12-18, 19-23) |
| `second/X/readings.jsonl` | the blind second typing of the five drawn texts |
| [`settled.jsonl`](settled.jsonl) | the drawn texts as settled where the two typings differ, with the reason for each place |
| [`griffith_faras.jsonl`](griffith_faras.jsonl) | the rows |
| [`measure.json`](measure.json), [`comparison.json`](comparison.json), [`recur.json`](recur.json) | the measure of the typing; the matches to held readings (counts and keys only); what recurs |

```
python3 -I src/faras.py               # the rows
python3 -I src/faras.py measure       # the two typings of the drawn texts
python3 -I src/faras.py compare       # the matches to what corpus_v6 already holds (local)
python3 -I src/faras.py recur         # after the rebuild: what recurs on the map (local)
python3 -I tests/test_faras.py
```

**Cost:** 2,451,369 subagent tokens for five readers (pack A 535,784; B 494,108; C 458,865; D 535,444; X 427,168),
1,175 tool calls, about 45 minutes a pack with four packs at once; no download. The estimate before the first pack
was 1 to 2 million for all 46 texts; the measured rate, about 1,100 tokens a sign, puts all 46 at about 5 million.

**Not done: Faras 24 to 46** (23 texts, about 2,300 signs: their copies are cut into 160 pieces, against 142 for
the 2,034 signs of Faras 1 to 23). Their packs E to H are cut and briefed in the scratch folder, with the key
corrected; typing them is about 2.3 million tokens and 45 minutes (no second typing: the bar is measured).
