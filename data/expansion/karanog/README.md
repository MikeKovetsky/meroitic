# Karanòg: Griffith's hand copies, read and checked against his own printed type

Work of 2026-11-10 by Claude Opus 5.5 readers. Source: F. Ll. Griffith, *Karanòg: The Meroitic Inscriptions of
Shablûl and Karanòg* (1911, public domain),
[archive.org `karangmeroitic00grifuoft`](https://archive.org/details/karangmeroitic00grifuoft). It follows
[`../hand_copy_test.md`](../hand_copy_test.md), where one reader got 88.8% of signs from the hand copies alone.

## 1. Answer first

1. **19 of the 152 inscriptions are done:** Kar. 1 to 10, 47, 48, 76 to 79 and 121 to 123, with 2,170 signs and
   342 words. They are in [`griffith_karanog.jsonl`](griffith_karanog.jsonl), and none of them was in the corpus.
   The other 133 are not read yet: their page scans were not on disk.
2. **Measured accuracy: 98.2% of signs** on the four Karanòg texts that FHN III prints (Kar. 47, 77, 78 and the
   spout of 121), read by fresh readers who could not see FHN. From the hand copies alone the same readers had
   90.5%. The bar set in `NEXT_STEPS.md` was 95%.

| Text | Signs in FHN | Hand copy alone | After the check |
|---|---|---|---|
| Kar. 47 (REM 0247) | 268 | 247 (92.2%) | 268 (100%) |
| Kar. 77 (REM 0277) | 134 | 118 (88.1%) | 129 (96.3%) |
| Kar. 78 (REM 0278) | 206 | 187 (90.8%) | 203 (98.5%) |
| Kar. 121, spout (REM 0321) | 46 | 40 (87.0%) | 42 (91.3%) |
| All four | 654 | 592 (90.5%) | 642 (98.2%) |

3. **A second edition agrees.** Against Carrier's readings of Kar. 47, 77 and 78 (*Meroitic Newsletter* 28,
   2001; in copyright, kept locally, so only the count is given) the checked readings have 599 of 608 signs
   (98.5%).
4. **What made the difference** is that Griffith printed most words of every inscription a second time, in clean
   type, in the same book. The check against those pages changed 238 of the 2,194 signs first read (10.8%).

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
   archive.org PDF: 2,722 typed objects ([`refs/typed/`](refs/typed/), the brief is
   [`refs/BRIEF_typing.md`](refs/BRIEF_typing.md)). `src/karanog_refs.py` works out which inscriptions each
   object names and writes one table per inscription ([`refs/by_inscription/`](refs/by_inscription/)): 3,565
   entries, at least two for each of the 152 inscriptions.
2. **Step 1, the copy alone.** A reader gets one or two page scans, Griffith's sign table and the notes on the
   hand from the first test, and reads every inscription sign by sign from enlarged crops. The file is then made
   read-only ([`readings/BRIEF_step1.md`](readings/BRIEF_step1.md)). The typed references did not exist yet when
   this step ran.
3. **Step 2, the check.** The same reader gets its inscriptions' entries and the printed pages. Where an entry
   and the reading differ, it looks at the copy and at the type again. The type usually wins, because it is
   Griffith's considered reading of the same signs; where the copy clearly shows something else, the copy is
   kept and the place is listed ([`readings/BRIEF_step2.md`](readings/BRIEF_step2.md)).
4. **The rows.** `src/karanog.py` turns the checked readings into rows like the other
   `data/expansion/griffith_*.jsonl` files: `text_std` as read (with line numbers, `?` and `[.]`),
   `text_corpus` in the corpus spelling, and notes that say what the check did.

Blindness: every reader worked in a folder of its own and was told to open nothing else and not to use the web.
FHN's texts were on the machine and are in this repo; nothing but the instruction kept a reader from them.

## 3. How well the type was typed

One further reader typed four of the 48 pages a second time without seeing the first typing.

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
- **The readers checked the type themselves** where it mattered: in step 2 they recorded 14 typed entries that
  the printed page does not bear out (`ref_corrections.jsonl` in each pack), among the 492 entries they placed.
- A sign note for future typists: two typists report that in this type ñ is the plain caret and d the λ with a
  hooked foot (Griffith's table, rows 11 and 23), and that the description of the two in
  `../printed_type_test.md` reads the other way round. No typist's output shows the swap: all write `yetmde`,
  `akiñ`, `pedeme` and `kdi` as they should be.

## 4. What the check did, by pack

| Pack | Inscriptions | Signs first read | Signs changed | Printed entries placed | Copy kept against the type | Typed entries corrected |
|---|---|---|---|---|---|---|
| C01 | Kar. 1 to 7 | 572 | 75 | 123 | 9 | 3 |
| C02 | Kar. 8 to 10 | 385 | 36 | 78 | 1 | 6 |
| C09 | Kar. 47, 48 | 346 | 38 | 94 | 8 | 3 |
| C14 | Kar. 76 to 79 | 618 | 74 | 143 | 9 | 1 |
| C21 | Kar. 121 to 123 | 273 | 15 | 54 | 6 | 1 |
| All | 19 | 2,194 | 238 (10.8%) | 492 | 33 | 14 |

The changes are the confusions the first test listed: the 3-shaped signs (m, ẖ, s and the bowl of q), p against
k, e against l, te against o + l, and d against ñ. The 33 places where the copy was kept are mostly small: a
divider the type leaves out, `-lo` in the copy where an index prints `-lowi`, `pqorl` against `pqrl`. Several
are places where Griffith's indexes disagree with each other and one of them agrees with the copy.

## 5. Limits

1. **Four texts and 654 signs** carry the accuracy figure, and FHN prints no other Karanòg text. Kar. 47, the
   longest, has no closing formulae and is covered by 79 printed entries; a text with a long unparalleled name is
   covered less.
2. **Agreement with FHN mostly measures how well Griffith's reading was recovered.** FHN and Carrier follow his
   copies, with their own corrections. Where Griffith misread the stone, so do these rows.
3. **The notes on the hand** given to the readers were written during the first test on these same four texts,
   so the "hand copy alone" column is not fully independent. The check against the type is.
4. **One reader a text.** No inscription was read by two readers, and the 15 texts without an FHN edition have
   no outside check at all.
5. **Word division follows each reader's judgment.** Where a copy runs words together (`atomẖe`), one reader kept
   it and another took Griffith's division from the type (`ato mẖe`). The rows are not yet uniform in this.
6. **Names are not masked** (no name list exists for these texts), as in the other Griffith files.
7. **Shablûl rows will have no REM number** until the numbering is checked; Karanòg N is REM 0200 + N (FHN III).
8. **Not merged into `corpus_v3`.** The file sits in this folder, outside the pattern `src/expand.py` reads,
   until the other 133 inscriptions are done.

## 6. Cost

About 3.8 million subagent tokens for typing the 48 reference pages (once, for all 152 inscriptions), 0.4
million for the second typing of four of them, and about 1.7 million for the seven pages of hand copies read so far (about 240,000 a page for both steps, about an hour a
page for step 1 and five minutes for step 2). The remaining 46 pages would cost about 11 million tokens.

## 7. Files, and how to rebuild

```
python3 -I src/karanog_refs.py     # refs/typed/ and refs/second_typing/ -> refs/by_inscription/, refs/all_refs.jsonl
python3 -I src/karanog.py          # readings/<pack>/ -> griffith_karanog.jsonl
python3 -I tests/test_karanog.py   # checks for both scripts, on made-up lines
python3 -I runs/work/karanog/score_fhn.py . "after the check" data/expansion/karanog/readings/C09/final.jsonl \
    data/expansion/karanog/readings/C14/final.jsonl data/expansion/karanog/readings/C21/final.jsonl
```

- `refs/typed/<typist>/ref_pdfNNN.jsonl`: the typed pages (NNN is the PDF page, the printed page plus 16).
  `refs/second_typing/QA/`: the four pages typed twice.
- `readings/<pack>/`: `copy_only.jsonl` (step 1, frozen), `final.jsonl` (after the check), `changes.jsonl`,
  `kept_against_type.jsonl`, `unplaced.jsonl`, `ref_corrections.jsonl`.
- The page scans are not in the repo: leaves n144 to n196 of the archive.org item, 3132 x 4094 px. The PDF of the
  same item shows the hand copies too blurred for this (hatching and dots are lost); the type pages were read
  from it.
- The readers received `refs/by_inscription/` as it stood before one fix to `src/karanog_refs.py` (it then took
  the numbers of ostraca, "form D 2" and footnotes for inscription numbers). The 24 wrong entries this gave them
  are among the 39 they reported as not placeable; the tables here are the corrected ones.
