# The REM pilot: can a reader read the plates of the *Répertoire d'épigraphie méroïtique*?

Step 7 of section B of [`NEXT_STEPS.md`](../../NEXT_STEPS.md), and the lever named under G7: more texts. The
REM (Leclant and others, 2000) is [online at Persée](https://www.persee.fr/issue/rem_0000-0000_2000_num_1_1) in
three volumes, REM 0001 to 1278. `corpus_v6` holds 548 inscriptions. If a Claude reader could read the REM's
plates well enough, the corpus could grow towards the REM's size, and some of the 2,013 open spellings that now
stand in one text only would recur and could be tested.

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
machine. The counts over the three volumes are in section 5, from the text layers of all their pages.

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

<!-- results: below this line once the readers are in -->
