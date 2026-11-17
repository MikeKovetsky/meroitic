# The REM pilot: can a reader read the plates of the *Répertoire d'épigraphie méroïtique*?

Step 7 of section B of [`NEXT_STEPS.md`](../../NEXT_STEPS.md), and the lever named under G7: more texts. The
REM (Leclant and others, 2000) is [online at Persée](https://www.persee.fr/issue/rem_0000-0000_2000_num_1_1) in
three volumes, numbered from REM 0001 to 1278. `corpus_v6` holds 548 inscriptions. If a Claude reader could read
the REM's plates well enough, the corpus could grow towards the REM's size, and some of the 2,013 open spellings
that now stand in one text only would recur and could be tested.

**The answer, on 4 inscriptions (2026-11-17): no.** A blind reader read 426 of 555 signs right against Griffith
(76.8%) and 43 of 103 words (41.7%), below the bar's lowest tier (85%), at 158,438 subagent tokens an inscription,
four times the quote. The REM holds 917 inscriptions, not 1,278: 473 are new to the corpus, about 4,600 words.
Reading them all this way would cost about 28 to 75 million tokens, and about 44 of the 2,013 open spellings that
stand in one text would then recur in a word read right. The pilot stopped after its first pack of 4, of the 20
planned, on Mike's word, because that pack alone used most of the budget (section 4). Every number below is in
[`rem_pilot_figures.json`](rem_pilot_figures.json), written by the script. The review corrected the count of
the REM and of what it would add (section 8). Since the merge of 2026-11-17, `corpus_v6` also holds 46 of the
47 ostraca of REM 0551 to 0597 (Griffith's of 1925, all but F.O. 38), typed from his print, and the 46 Faras texts
of REM 0501 to 0546 (Griffith's of 1922), typed from his hand copies. The pilot counts against the 548 texts the
map is drawn on, as the open spellings are, so those texts are among the 473 counted new (all but REM 0544, which
was held); they are typed, but not yet in the map. One of them, REM 0543, turned out to be a text the 548 hold:
Millet's line 286, which the corpus had not identified; the counts here keep the numbering they were made with.
Signs a word moved from 5.31 to 5.29, because REM 0544, a text of the map, now has an open reading.

The REM is in copyright. Its pages, its plates and every reading taken from them stay on the author's machine
(`data/sources/rem/`); this page and its figures file give counts only. The script is
[`src/rem_pilot.py`](../../src/rem_pilot.py), its checks [`tests/test_rem_pilot.py`](../../tests/test_rem_pilot.py).

## 1. The question

Can a reader agent, blind to the editions, read the REM's plates into the corpus spelling accurately enough to add
the inscriptions the corpus does not hold? Measured on about 20 inscriptions that both the REM shows and an edition
in hand prints in transliteration.

## 2. What an entry of the REM holds

Seen on the first pages of volume I before the rule below was written (the plate of REM 0001 was opened; it is not
in the pick). An entry is two pages or more:

1. **A plate page** headed with the REM number: one or more figures, each with a caption that says what it shows
   and where it was first printed ("Fac-similé de l'inscription M. I. 1 (Griffith 1911c, pl. XVI)"). The figures are
   photographs of the object or the scene and drawings (facsimiles, copies, Lepsius's plates), most of them
   reprinted from the first edition.
2. **A catalogue page:** where the object is now (*Localisation actuelle*), its first designation, the monument,
   its measurements, a description of the inscription (the script, hieroglyphic or cursive; the number of lines or
   columns; the state) and the bibliography.

**No transliteration.** The catalogue quotes a name now and then; the text of the inscription is not printed.
Persée serves each page as an image of 1621 by 2292 pixels (196 dots to the inch) and a text layer read by
machine. The counts over the three volumes are in section 5, from the text layers of all their 2,081 pages.

## 3. The rule, the bar and what we expect (written before any reader ran)

Written on 2026-11-17 and committed at 08:34 PST, before any reader opened a plate.

### The rule that chose the inscriptions

1. **The pool** (`pool()`): the rows of [`data/inscriptions.jsonl`](../inscriptions.jsonl) with one REM number
   within the three volumes and an open reading of an edition in hand: Griffith's printed type (*Meroitic
   Inscriptions* I and II, *Meroë*), the Karanòg copies checked against his type, and Griffith 1917 for REM 1003.
   Left out: rows with two REM numbers (their parts stand on two entries), rows of fewer than 3 words (too short to
   score) and of more than 150 (REM 0094 and REM 1003: too long for this pilot's cost). 233 inscriptions.
2. **Strata** by kind (funerary; royal or temple; graffito; other) and by the words of the open reading (S 3 to 9,
   M 10 to 29, L 30 to 150; graffiti of M and L are one stratum). The places, 20 in all: funerary S 2, M 4, L 3;
   royal or temple S 3, M 2, L 2; graffito S 2, M and L 1; other S 1.
3. **One seeded order** (seed 20261117) over the pool. First, up to two entries of volumes II and III are taken
   (most texts new to the corpus are in those volumes; the pool's six there are all Meroë City texts of 1911).
   Then each stratum is filled in that order, the entries with a modern reading typed from FHN III's page images
   first (15 are held, in `runs/work/`), but no more of them than half the stratum's places, rounded up.
4. **An entry the REM shows no plate for is passed over** and the next one taken.

### What the readers get

One reader agent for a pack of four inscriptions, blind to every edition, in a folder of its own: the figures of
each plate cut out of the page (no heading, no caption, no REM number); for each inscription the object, the
script and the number of lines as the catalogue states them, with any letters the catalogue quotes left out;
Griffith's two sign tables (*Karanòg*, pp. 18 and 19, public domain) with the value of each row in the corpus
spelling, and the key to the Karanòg hand from the first test. The reader writes the corpus spelling: `S` the sign
s, `s` the sign se, `N` the sign ne, `x` ḫ, `X` ẖ, `o` the sign o, `te` and `to` one sign each. The first pack
runs alone, to count its tokens before the rest are started. A second reader reads two of the packs again, for
the agreement between readers; that is reported and is not part of the bar.

### The pick (by the rule, before any reader)

Drawn at 08:48 PST against the index of the volumes' text layers; no entry was passed over for want of a plate.
The packs take the picks in turn (the first pick to P1, the second to P2, and so on); the second reader reads P1
and P3 again.

| Inscription | Stratum | Words (open reading) | Scored against | What the REM shows | Pack |
|---|---|---|---|---|---|
| REM 0412 | royal M | 15 | Griffith | 1 photograph, 1 drawing | P1 |
| REM 0410 | royal M | 25 | Griffith | 1 photograph, 1 drawing | P2 |
| REM 0304 | funerary S | 8 | Griffith | 1 photograph, 1 drawing | P3 |
| REM 0080 | funerary S | 3 | Griffith | 1 photograph, 1 drawing | P4 |
| REM 0277 | funerary M | 22 | FHN III | 1 photograph, 1 drawing | P5 |
| REM 0256 | funerary M | 20 | Griffith | 1 photograph, 1 drawing | P1 |
| REM 0213 | funerary M | 18 | Griffith | 1 photograph, 1 drawing | P2 |
| REM 0211 | funerary M | 25 | Griffith | 1 photograph, 1 drawing | P3 |
| REM 0247 | funerary L | 46 | FHN III | 1 photograph, 1 drawing | P4 |
| REM 0278 | funerary L | 34 | FHN III | 1 photograph, 1 drawing | P5 |
| REM 0327 | funerary L | 33 | Griffith | 1 photograph, 1 drawing | P1 |
| REM 0105 | royal S | 4 | FHN III | 1 photograph, 1 drawing | P2 |
| REM 0106 | royal S | 4 | FHN III | 1 photograph, 1 drawing | P3 |
| REM 0099 | royal S | 6 | Griffith | 1 photograph, 1 drawing | P4 |
| REM 0101 | royal L | 68 | Griffith | 1 photograph, 2 drawings | P5 |
| REM 0409 | royal L | 35 | Griffith | 1 photograph, 1 drawing | P1 |
| REM 0124 | graffito S | 7 | Griffith | 1 photograph, 1 drawing | P2 |
| REM 0120 | graffito S | 8 | Griffith | 1 photograph, 1 drawing | P3 |
| REM 0112 | graffito M | 12 | Griffith | 1 photograph, 1 drawing | P4 |
| REM 0065 | other S | 6 | Griffith | 1 photograph, 1 drawing | P5 |

Two things the pick shows before any reading, which narrow what the pilot can say:

1. **Every plate holds a drawing** beside its photograph (the drawings are Griffith's facsimiles and hand copies,
   reprinted). So the readers read drawings with a photograph to check against, and the expectation for
   photographs alone (about 50%) cannot be measured on this sample.
2. **All 20 are in cursive**, by the catalogue. The seed drew no hieroglyphic text, so hieroglyphs are not tested.

Added at 08:51 PST, while the first reader was at work and before any reading was in: **a pack of photographs
alone** (PH), the photographs of pack P2's four inscriptions given to a fresh reader who sees no drawing, to measure
what a plate without a drawing allows. It is reported beside the bar, not part of it, and runs only if the first
pack's tokens leave room under the pilot's budget.

The figures were cut by eye on small previews of each page; the script widens their sides to the page's frame and
moves the edges of a drawing out to the first blank row or column, so that no line of signs is cut.

### How a reading is scored

Against FHN III's text where one is typed (the modern reading), else against Griffith's open reading; against
both where both are held. As the corpus pages score a reading:

- **Signs right** (the Karanòg page): the edition's signs less the edit distance between the two, so a sign only
  the reading has counts against it too. Lost signs are left out on both sides; FHN's restorations count, as on
  the Karanòg page.
- **Words that agree** (the Akinidad page, on signs and with nothing folded): a word of the edition agrees when
  every one of its signs is matched by an equal sign of the reading. Word division is not scored.

### The bar

On the 20 pooled (the signs right of all, over the signs of all their editions):

| Signs right, pooled | Verdict | What it would allow |
|---|---|---|
| 95% or more | GO | REM readings go into the corpus as rows, as the Karanòg rows did (97.7%, bar 95%) |
| 85% to 95% | LAYER | a local layer used only to look for recurrences, each hit checked on the plate before it counts |
| below 85% | NO-GO | not used |

The same tiers are read on the inscriptions whose plate holds a drawing; if drawings alone reach a tier that the
pool does not, the recommendation is to read only the entries with a drawing.

### What we expect

- **Signs right, pooled: about 75%**, below the bar: about 85% on drawings (the Karanòg copies alone gave 89%, from
  larger scans) and about 50% on photographs. So we expect NO-GO for the pool, and drawings near the LAYER line.
- **Words that agree:** about 50%; formula words right, names and rare words wrong.
- **Tokens:** about 40,000 subagent tokens an inscription.
- The faults we expect: the 3-shaped signs (m, ẖ, s, q), p against k, te against o + l; photographs too small to
  read at 196 dots to the inch; hieroglyphs better than cursive.

The script's first commit held one constant for this, 0.85 "pooled"; the page beside it gave 75% pooled and 85% on
drawings. The page is what was written down, and the constant now repeats it (`EXPECTED`).

## 4. What came of it

### Stopped after the first pack, on Mike's word

The first pack (P1: REM 0412, 0256, 0327 and 0409) ran alone, as planned, to count its tokens: **633,753 subagent
tokens for 4 inscriptions**, 352 tool calls and 46 minutes. At that rate the other 16 inscriptions, the two second
readers and the pack of photographs (7 of the 8 readers' folders) would have taken about 4.4 million more, far past
the pilot's 1.5 million line.
Asked through the main session, Mike chose on 2026-11-17 to stop at 4 inscriptions, write up and review ("Yes,
both picks", to the pick "REM pilot: stop at 4 inscriptions, write up and review").

So this page measures less than section 3 set out to:

1. **4 inscriptions, not 20:** 555 signs of the edition, two Karanòg texts and two Meroë texts, all four royal or
   funerary. No graffito, no Philae text, no short text.
2. **No modern edition:** none of the four is among the texts typed from FHN III, so all four are scored against
   Griffith's reading of the same drawings (his print, and the Karanòg copies checked against his type).
3. **No second reader** (the agreement between readers is not measured) and **no pack of photographs alone.**
4. The bar was set on the 20 pooled; it is read here on the 4.

### The scores

| Inscription | Plate | Signs right | Share | Words that agree | Signs marked `?` |
|---|---|---|---|---|---|
| REM 0412 (Meroë, stela, three parts) | photograph, the facsimile of *Meroë* (1911) | 53 of 77 | 68.8% | 3 of 15 | 27 |
| REM 0256 (Karanòg, stela) | photograph, Griffith's hand copy | 110 of 131 | 84.0% | 11 of 20 | 12 |
| REM 0327 (Karanòg, offering table) | photograph, Griffith's hand copy | 133 of 172 | 77.3% | 16 of 33 | 37 |
| REM 0409 (Meroë, statue base, four faces) | photograph, the facsimile of *Meroë* (1911) | 130 of 175 | 74.3% | 13 of 35 | 40 |
| **All four** | | **426 of 555** | **76.8%** | **43 of 103 (41.7%)** | 116 |

**Verdict: NO-GO** (below 85%). Against what we expected: below the 85% expected on drawings, which every plate
held, and near the 75% expected for a pool that would have mixed in photographs; words below the 50% expected;
tokens four times the 40,000 quoted. The four lie between 68.8% and 84.0%; no tier above NO-GO is within that range.

### What it fails on

1. **The photographs give nothing.** The reader marked all four photographs "not legible" and read from the
   drawings alone: at 196 dots to the inch the signs of a halftone photograph are a few pixels high. A REM entry
   without a drawing is, for this reader, an entry without a text.
2. **The signs that look alike, as in the Karanòg test.** Of the 129 signs wrong (97 read as another sign, 18 that
   only the reading has, 14 missed), the 3-shaped signs m, s, ẖ and q account for 27 of the 97, e against l for
   12, p against k for 7 and d against ne for 6. The commonest single fault is the sign s written for m (13).
3. **The hand matters.** The best score is the Karanòg stela (84.0%), in the hand that the reader's sign key
   describes; the worst is the small facsimile of the Meroë stela (68.8%), in another hand, in three parts whose
   order and line count the reader had to guess (the drawing shows part c in four lines, the catalogue says two).
4. **The reader's own doubts find half of its errors.** Of the 115 signs it wrote wrong (read as another sign, or
   only in the reading), 55 carry its `?`; of its 116 marks, 61 sit on signs that are right. Checking only the
   marked signs would leave about half the errors in.
5. **Words fail faster than signs.** A word agrees only when every sign is right, so 76.8% of signs gives 41.7% of
   words. Most of the words that agree are words of the formulae (`woSi`, `Soreyi`, `tedxelowi`, `yetmdelowi`,
   `ato mXe`); the names and the rare words mostly do not, and they are what the corpus would gain. Of the words
   whose spelling is open and stands in one text of `corpus_v6` (by the analysts' map), the kind the recurrences of
   section 5 are made of, it read 12 of 41 right (29.3%).

## 5. What reading all the REM would cost and add

### What the REM holds

The text layers of all 2,081 pages, indexed by the script: the REM gives **917 numbers in nine sections**, not 1,278
(the numbering leaves gaps between sections), as 962 entries with their lettered parts. Every number has a page of
plates and a catalogue page. The annexes, bibliography and indexes at the end of volume III name numbers of every
section; the index leaves them out.

| Section | Numbers | New to the corpus | Words new (estimate) |
|---|---|---|---|
| *Meroitic Inscriptions* (Griffith), 0001 to 0137 | 137 | 18 | 167 |
| Other texts published before, 0138 to 0150 | 13 | 13 | 117 |
| Karanòg and Shablul, 0201 to 0387 | 187 | 36 | 349 |
| Meroë, 0401 to 0451 | 51 | 19 | 174 |
| Faras, 0501 to 0546 | 46 | 45 | 651 |
| Ostraca of several sites, 0551 to 0597 | 47 | 47 | 342 |
| Kawa, 0601 to 0707 | 107 | 107 | 927 |
| Royal cemeteries of Kush, 0801 to 0851 | 51 | 51 | 410 |
| Texts published singly since 1911, 1001 to 1278 | 278 | 137 | 1,510 |
| **All** | **917** | **473** | **4,647** |

- **444 of the 917 are in `corpus_v6`; 473 are new** to it: the corpus would go from 548 to about 1,021
  inscriptions, not to about 1,280. 44 of the 444 are Griffith's Meroë and Shablul texts that the corpus names by
  his numbers, without a REM number (`Meroe 13`, `Sh. 1`); the REM's catalogue gives each the same designation.
  92 of the 473 are the Faras texts and the ostraca, which two other sessions typed from Griffith's own editions.
  Both joined `corpus_v6` on 2026-11-17 (46 of the 47 ostraca, all 46 Faras texts), not the map, so they stay
  counted here.
- **Words:** about 4,600 new words, under half the corpus's 10,290. Each new number's catalogue states its lines,
  bands or columns (394 of the 473 do); the words a unit are the median over the numbers held by one row (2.0 a
  cursive line, 8.67 a cursive band, 1.33 a hieroglyphic column). The mean gives 6,198, the high end.
- **Script of the new:** 401 cursive, 39 hieroglyphic, 33 not stated.
- **Plates:** every new number has a plate page; for 322 of the 473 a caption names a drawing. That is a floor:
  on the 20 picks the captions named a drawing for 17 of the 20 that have one.

### What it would cost

At the first pack's rate, **1,142 tokens a sign of the edition**, and 5.29 signs a word: **about 28 million
subagent tokens** for the 473 (37 million at the mean count of words). By the inscription, 158,438 each, it would be
**75 million**; the new texts are shorter (about 52 signs each, against 139 in the pack), and part of a reader's
cost (the brief, the sign tables, cutting crops) does not shrink with the text, so the cost lies between the two.
That is for one reader; a checked reading (two readers and a settling pass, as for Karanòg) costs more.

### What it would add

How often an open spelling that stands in one text recurs when texts are added, measured on `corpus_v6` itself:
draw k of its inscriptions, take the open spellings that stand in exactly one of them, and count how many stand in
the next m inscriptions; 200 draws for each k from 120 to 210, with m/k equal to the share the REM would add, and
the share carried to k = 548 along a straight line in log k.

| The share added | Recur in a new text | Reach three texts | Recur and read right (29.3%) | At 41.7%, the share of all words |
|---|---|---|---|---|
| By words, median (0.45) | 152 of 2,013 (7.5%) | 26 | 44 | 63 |
| By words, mean (0.60) | 189 (9.4%) | 40 | 55 | 79 |
| By inscriptions (0.86) | 248 (12.3%) | 70 | 73 | 104 |

The words are the fair measure: the new texts are about half as long as the corpus's. So reading all the REM
plates would give about 150 of the 2,013 a second text if every word were read right, and about 26 of them the
three texts that the recurring-words work needs. With the words this reader gets right it would give about 44:
a recurrence counts only where the new text's word is read right, and of the words of this kind in the four texts
(open, and in one text of the corpus) the reader got 12 of 41 right (29.3%), fewer than its 41.7% of all words.
Four texts are a small sample for that share. The count assumes the new texts are like those of the corpus and
that the share keeps growing with the corpus as it does from 120 to 210 inscriptions.

## 6. Recommendation

**Do not read the REM plates this way.** The readings are below the bar where the plates are best (Griffith's own
drawings), the photographs give nothing, and the full read would cost 28 to 75 million tokens for about 44
spellings with a second text. The faults are the known ones of hand copies, and the reader's doubts find only half
of them, so a cheap check does not rescue it.

What the pilot leaves that is of use:

1. **The REM's own size:** 917 inscriptions, 473 of them not in the corpus, by section, with the script and the
   lines of each (`data/sources/rem/index.jsonl`, local). The goal of a corpus of about 1,280 should read about
   1,021.
2. **A typed source beats a read plate.** Every text the corpus holds came from a print in transliteration or from
   hand copies checked against one. Hallof's volume 7 (2024) prints the transliteration of REM 0001 to 2780, and
   reading print costs a fraction of this (about 7 million tokens by the Newsletter's rate, for five times the
   texts). It is a purchase, parked by Mike's word of 12 November.
3. **Sections with a print of their own:** Faras and the ostraca are typed from Griffith; Kawa (107 new) and
   the royal cemeteries (51 new) were published by Macadam and Dunham, whose editions are not held and were not
   looked for here.

## 7. Files, commands and cost

| File | What | Where |
|---|---|---|
| `src/rem_pilot.py` | the index, the rule, the packs, the scores, the estimate, the figures | public |
| `tests/test_rem_pilot.py` | the checks, on made-up texts and pages and on the public table | public |
| `data/discovery/rem_pilot_figures.json` | every count on this page | public |
| `data/sources/rem/text/` | the text layers of the 2,081 pages (Persée, 2,081 files, 5.4 MB) | local |
| `data/sources/rem/pages/` | the 22 plate pages of the 20 picks and the plate of REM 0001 (23 images, 7.9 MB) | local |
| `data/sources/rem/web/` | the volumes' and documents' pages on Persée (3.7 MB) | local |
| `data/sources/rem/index.jsonl` | one row per entry: plate pages, captions, script, lines, state | local |
| `data/sources/rem/pilot/` | the kit, the spec of the crops, the packs, the key, the reading, the scores, the estimate | local |

```bash
python3 -I src/rem_pilot.py index      # the volumes' text layers into the index (local)
python3 -I src/rem_pilot.py pick       # the rule's 20
python3 -I src/rem_pilot.py packs      # the readers' folders (writes only those not yet written)
python3 -I src/rem_pilot.py score && python3 -I src/rem_pilot.py estimate && python3 -I src/rem_pilot.py public
python3 -I tests/test_rem_pilot.py
```

All but the tests need the local files. Downloaded on 2026-11-17 from Persée, all within this pilot's approval: the
text layers of every page, and the images of the plate pages of the 20 picks and of REM 0001; no PDF.

**Cost.** Written by hand from the task notifications, as are the tool calls and minutes in section 4; with the
sizes of the local folders above, the only numbers on this page that the pilot's script does not count.

<!-- cost: by hand, from the task notifications -->

| Run | Subagent tokens | Running time |
|---|---|---|
| Reader of pack P1 (4 inscriptions) | 633,753 | 46 min 12 s |

Quoted before the run: about 40,000 an inscription, 0.5 to 1 million for the pilot. Not run: packs P2 to P5, the
second readers of P1 and P3, the pack of photographs alone.

<!-- end of the cost -->

**A fault of the run.** At 08:52 the pack builder, run to add the pack of photographs, wrote P1's folder again
while its reader was at work, which emptied the reader's own crops; its figures, list and brief were the same files
as before, the reader was told and cut its crops again. The builder now writes only folders that do not exist.

## 8. What the review corrected

The review of 2026-11-17 found four faults in the count of section 5 and corrected them in the script; the scores
of section 4 did not change. Before it, this page gave 517 new inscriptions, about 5,300 words, 32 to 82 million
tokens and about 70 spellings read right with a second text.

1. **The index filed pages under the wrong number.** It filed the annexes, bibliography and indexes at the end of
   volume III under the numbers they name, took two catalogue pages for section title pages because their
   commentary names a range of documents (those of REM 1016 and REM 1059), filed four catalogue pages under a number
   they cite before their running head (those of REM 0066 and 0067, and of REM 1003 and 1039, each under the other)
   and one under a footnote's number (REM 1034's, under 1045). It now files a page by its running head, stops at the
   annexes and leaves out the blank pages; every number has its catalogue page.
2. **The catalogue's counts above twenty were not read** ("vingt-quatre", "vingt et une", "quarante deux"), so the
   longest texts took the median of their script; they are now read, as is "au moins trois".
3. **44 texts the corpus holds were counted as new:** Griffith's Meroë and Shablul texts that the corpus names by
   his numbers, without a REM number. The REM's catalogue gives each the same designation (`Meroe 13` is REM 0413,
   `Sh. 1` REM 0368), and the script now matches them by it.
4. **"Read right" took the reader's share of all words** (41.7%) for the spellings that stand in one text; it reads
   those worse (29.3%), and the recurrences read right are now counted at that share.
