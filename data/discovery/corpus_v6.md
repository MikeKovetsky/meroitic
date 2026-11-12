# corpus_v6: one inscription once

Built on 2026-11-12. This is piece F1 (step 22) of [`NEXT_STEPS.md`](../../NEXT_STEPS.md): a corpus keyed by
inscription, with real names and a source for every reading. Every number on this page is written by
`src/v6/public.py` into the tables of section 4, and the text quotes them from there.

**The result in three sentences.** The 899 texts of `corpus_v5` are 289 inscriptions; more than half of its
words were copies of a reading with a name swapped. `corpus_v6` holds 548 inscriptions, each once, with real
names, and 303 of the 563 inscriptions in the table have a reading under an open licence. Counted on it, the
coverage map translates 60.0% of the words of the inscriptions that were already in the corpus (62.0% on
`corpus_v5`), and 51.3% with the Newsletter's texts, which no analyst has read yet.

## 1. What was wrong with `corpus_v5`

Every figure of the project was counted on `corpus_v5`, and 659 of its 899 texts come from Otten's file
`mero-corpus.txt`, which is padded: each example was repeated with one name swapped for another. The older
scripts (`src/pool.py`, `src/dedup.py`, `src/collapse.py`, `src/clean_v2.py`) undid the padding from the padded
file alone, by masking the swapped names. That left four faults, all found in later work: copies whose swapped
name had several words, so that its rest stood behind the mask as a word; names masked and so lost; no way to
tell an inscription from a phrase quoted in a grammar; and no link from a text to an edition.

## 2. How `corpus_v6` was built

1. **Otten's padding undone from his own files** (`src/v6/otten.py`). His repository also holds the examples
   before padding, in per-scholar files (`Data/MilletExamples.txt` and three others), with the real names,
   Millet's brackets, and the page of Millet's 1968 thesis for every line. Of the 17,995 different lines of the
   padded file, 340 are a line of those files letter for letter and 17,446 are such a line with one stretch
   swapped; 206 more differ in a second small place. So each text of the older corpus has a source line, and
   the source line gives the reading with its names. The names are marked as names where Otten's files tag
   them (`ANTHROPONYM`, `ROYAL NAME`).
2. **Every reading held, in one list** (`src/v6/readings.py`): Griffith's printed texts and the checked Karanòg
   copies (public domain, the rows CC BY 4.0), the texts typed from the *Meroitic Newsletter*, the entries of
   Millet 2005 and of *Fontes Historiae Nubiorum* III (text layers, in copyright, used as witnesses and not as
   typed readings), Otten's three narrative files and his source lines.
3. **Numbers first.** Two readings that share a number of one numbering (REM, Millet's GA numbers, Griffith's)
   are one inscription. Two readings with two different numbers of one numbering are two inscriptions, however
   alike their letters: 13 pairs of rows of `corpus_v6` look alike in this way, among them a stela and an
   offering table of one person at Karanòg. FHN names the REM numbers of each of its entries, and prints two
   texts in two pieces under two numbers each; those are joined.
4. **Letters for what has no number:** the narratives and the source lines. A text is reduced to bare letters in
   one spelling and compared by its runs of five letters, leaving out the runs that 8 or more edition texts hold
   (the formulae). The rule is in section 3.
5. **What a source line is.** A line that matches one inscription surely, and holds half of its own runs or is
   half as long, is a reading of it. A line that holds less, or whose letters stand whole in a held text, is an
   example phrase from a grammar. A line of 40 letters or more that matches nothing is an inscription not
   identified, kept under the page of Millet's thesis. The rest are example phrases whose source is not held.
   A text of `corpus_v5` is what its source line is; when it is not the first text of that line, it is a copy
   with a name swapped.
6. **One preferred reading** (`src/v6/build.py`), taken in this order from the typed readings that give the
   whole text (four fifths of the longest one's letters): Otten's narrative file, Otten's source line (Millet
   1968), Griffith's print or the Karanòg copy, the Newsletter in print, the Newsletter's printout of 1971. This
   keeps the reading that earlier results were counted on and repairs it; the open reading stands beside it in
   the table (`open_text`) wherever there is one. Two typed readings of one inscription that share nothing are
   two parts of it (two sides, two pieces) and are joined.
   - **Numerals.** A lone `l` is read as a numeral where a later edition of the same inscription has a numeral
     after the same word, and where the same list goes on. This sets 10 numerals in the epitaph of Makheye
     (REM 0544), 4 from Newsletter 28 and 6 by analogy. An earlier edition does not overrule a later one:
     Griffith's numeral 1 against Millet's `l` in REM 0101 is left as Millet has it.
   - **Word division, one rule.** A word is what the edition prints between dividers or spaces. An editor's
     hyphens, which cut a word into morphemes, join. A lost sign stays a dot in the word it breaks, so that a
     broken word is one broken word and not two whole ones. The Karanòg rows keep the division of
     `src/karanog.py`. Nothing else is made uniform (section 7).
7. **The kind of text** comes from a rule, and the row says which: an epitaph opens with the names of Isis and
   Osiris, an oracular decree with `wteli pkeli`, and otherwise the description of the object decides.

## 3. The bar, set before the run, and what came of it

The bar was written at 12:03 PST, before the open match was scored and before any reader. Two things had been
seen by then, and the bar says so: that the right entry is the best match for the 31 pairs of the expert check,
and how many source lines fall in each band.

1. **The rule.** Two texts are a sure match when 60% or more of the own runs of one stand in the other and they
   share at least 12 own runs; a doubtful one from 30%; below 30% none.
2. **Bar A:** at least 90% of the known pairs come out sure or doubtful with the partner as the best match, and
   none has a sure match to another text. The known pairs are the 31 of the expert check, the three Karanòg
   texts that Newsletter 28 and FHN print, the Newsletter rows that an earlier test found in the corpus, and
   the Newsletter's second editions: 53 in all.
3. **Bar B:** the share of the 151 Karanòg texts, which are 151 different inscriptions, that have a sure match to
   another Karanòg number is reported.
4. **Bar C (the readers):** each of two readers names the right text for at least 10 of 12 known lines and
   answers "none" for at least 10 of 12 lines whose text was taken out of the candidates.

**Bar A was missed.** The partner is the best match for 44 of the 53 pairs (83.0%). In some of the nine the best
match is another line of the same text, which Otten's files give more than once; the rest are fragments of a
few words, which share too few runs to be matched by letters at all. Three pairs have a sure match to another
text. So the rule alone does not find every pair, and this build does not rely on it alone: numbers decide
wherever there are numbers; a sure match stands only when no second inscription shares half as many runs; the
pairs read side by side for the expert check stand as read; and every other match that could make a line a
reading, or leave a long line without a home, went to two readers.

**One thing was added after the first build,** before any reader ran: a doubtful match needs 6 shared own runs.
Without that floor an edition text of ten letters made every long line "doubtful". The table of section 4 gives
bar A both ways. A long line that matches nothing still went to the readers with its best candidates under the
floor.

**Bar B:** 4 of the 151 (2.6%), two pairs. Letters cannot tell two monuments of one person apart, which is why a
number decides before letters do.

**Bar C was passed by both readers:** each named the right text for all 12 known lines and answered "none" for
all 12 lines whose text was taken out. Every item had three candidates, the rule's own filled up with the
nearest other texts, so that a known line, a decoy and an open line looked alike. Of the 17 open lines the two
gave the same answer for 15. They named the same candidate for 14, and both answered "none" for 1.

**Two things were added after the answers were in,** both on the cautious side, and the tables count what each
did:

1. An answer the two readers share is used only when both give it a sureness of 3 or more of 5. One line had
   the same candidate from both at 2, each noting that the name in it differs; it is not merged.
2. A line that the readers took for the whole text of an inscription is set aside when the rule matches it
   surely with a line that is an inscription of its own. This happened once: a line that the readers placed in
   the fragment GA 13+16 holds, in its first half, a passage of the long epitaph quoted on the same pages of the
   thesis. Otten's line runs two quotations together. The readers saw the editions' candidates, not that
   epitaph. The check that found it counts every pair of rows that the rule matches across two numberings.

So 13 of the readers' matches are taken, 4 as the whole text and 9 as a part; of the 4, one is set aside, and
3 lines became readings of an inscription. 3 lines are not settled.

## 4. The figures

<!-- tables: written by src/v6/public.py -->

### The counts the text uses

- Otten's padded file: 18,090 lines, 17,995 of them different. Equal to a line of his per-scholar files: 340. Such a line with one stretch swapped: 17,446. Near one, with a second small difference: 206. From no such line: 3 (the three narratives, which have files of their own).
- Source lines in the per-scholar files: 1,159. The 659 texts of the older corpus come from 329 of them.
- The most copied line: MilletExamples.txt line 433 (GA 28), 52 texts and 4,540 words of `corpus_v5`.
- Readings held besides Otten's lines: 152 rows of Griffith's print, 151 Karanòg rows, 256 Newsletter rows, 34 texts of Millet 2005, 11 entries of FHN III, 3 narrative files.
- Source lines by what they are: 47 readings of an inscription, 906 example phrases, 195 word-list entries, 8 inscriptions not identified, 3 with a doubtful match that is not settled.
- The example phrases: 311 are a part of one held text or stand whole in it, 166 stand whole in several, 34 have a doubtful match that was not read, 1 was taken by the readers for a text of one inscription and is set aside because the rule matches it surely with another, and 394 match nothing held.
- Doubtful matches read by two readers: 17 lines. Both gave the same answer for 15 and differ on 2. Both named the same candidate for 14: 13 are used, 4 as the whole text and 9 as a part of it, and 1 is not, because both marked it as a guess. Both answered "none" for 1. Not settled: 3 lines, behind 3 texts and 28 words of `corpus_v5`.
- The lines the readers settled, as they stand in the build: 3 are readings of an inscription, 9 are example phrases from one, 1 is set aside, and 1 matches nothing and is an inscription of its own.
- A lone `l` read as a numeral: 10 (4 by a later edition, 6 by analogy), in 1 inscription(s): REM 0544.
- Words marked as a personal name by Otten's own tags: 90.
- Inscriptions whose text is in two or more parts: 9.
- Pairs of rows of `corpus_v6` that the rule takes for a sure match and that carry two different numbers of one numbering: 13 (in 20 rows). Pairs of rows numbered in two different ways (a REM number and a number of Griffith's, Millet's or the Newsletter's, or none) that the rule matches at all: 2, of them surely 0: Meroe 27 and Millet 1968 p. 238-240 (MilletExamples.txt line 286); Meroe 28 and Millet 1968 p. 238-240 (MilletExamples.txt line 286).

### The measures

| Measure | Count | Share of the inscriptions |
|---|---|---|
| Inscriptions | 563 | |
| with a REM number | 441 | 78.3% |
| with a typed reading (the rows of `corpus_v6`) | 548 | 97.3% |
| with real names in the preferred reading | 548 | 97.3% |
| with two readings or more | 70 | 12.4% |
| with a reading under an open licence | 303 | 53.8% |
| with an open reading of the whole text | 274 | 48.7% |
| whose preferred reading is the open one | 286 | 50.8% |
| held only as a text layer of Millet 2005 (not typed) | 9 | 1.6% |
| typed, without a legible word | 6 | 1.1% |
| quoted by Millet 1968 and not identified | 8 | 1.4% |

### What the texts of `corpus_v5` turned out to be

| What | Texts | Words | Share of the words |
|---|---|---|---|
| A name-swapped copy of a reading | 207 | 11,967 | 54.5% |
| A name-swapped copy of an example phrase | 123 | 1,599 | 7.3% |
| A second reading of an inscription already counted | 4 | 144 | 0.7% |
| An example phrase or a word-list entry | 273 | 1,616 | 7.4% |
| Not settled by two readers | 3 | 28 | 0.1% |
| Stands for its inscription | 289 | 6,623 | 30.1% |
| All of `corpus_v5` | 899 | 21,977 | |

### The kinds of text

| Kind | Inscriptions |
|---|---|
| Funerary | 269 |
| Not known | 112 |
| Royal or temple (stela, wall, cartouche, label) | 86 |
| Document (ostracon, papyrus, wood, vessel) | 53 |
| Graffito | 36 |
| Oracular decree | 7 |

### The preferred reading, by source

| Source | Inscriptions |
|---|---|
| The Meroitic Newsletter (typed by the model, in copyright) | 210 |
| Griffith's Karanòg hand copies, checked against his type (open) | 150 |
| Griffith's printed type (open) | 136 |
| Millet 1968 as Otten typed it, with real names | 49 |
| Otten's three narrative files | 3 |

### The rule on the pairs already known

| | As the bar was written | With the floor of six shared runs |
|---|---|---|
| Known pairs | 53 | 53 |
| The partner is the best match, sure or doubtful | 44 (83.0%) | 44 (83.0%) |
| of them sure | 29 | 31 |
| of them doubtful | 15 | 13 |
| Counting another line of the same text as right | 45 (84.9%) | 46 (86.8%) |
| Pairs with a sure match to another text | 3 | 3 |

Bar B: 4 of the 151 Karanòg texts have a sure match to another Karanòg number (2.6%).

### The two readers (bar C)

| | Reader 1 | Reader 2 |
|---|---|---|
| Known lines: the right text named | 12 of 12 | 12 of 12 |
| Lines with the text taken out: "none" answered | 12 of 12 | 12 of 12 |
| Passes the bar | yes | yes |

### The coverage map, counted again

| Counted on | Texts | Words | Translated | Share |
|---|---|---|---|---|
| `corpus_v5`, every text (the old figure) | 899 | 21,977 | 13,618 | 62.0% |
| `corpus_v5`, near-copies counted once (the old figure) | 608 | 8,786 | 5,413 | 61.6% |
| `corpus_v6`, the inscriptions that were in `corpus_v5` | 289 | 6,573 | 3,942 | 60.0% |
| `corpus_v6`, the inscriptions new to the corpus | 259 | 3,704 | 1,330 | 35.9% |
| `corpus_v6`, all | 548 | 10,277 | 5,272 | 51.3% |

| Level | `corpus_v5` | `corpus_v6`, were in `corpus_v5` | `corpus_v6`, new | `corpus_v6`, all |
|---|---|---|---|---|
| meaning | 6,981 | 2,228 | 707 | 2,935 |
| grammar | 1,956 | 421 | 254 | 675 |
| name | 4,418 | 1,210 | 216 | 1,426 |
| number | 263 | 83 | 153 | 236 |
| hypothesis | 3,512 | 937 | 340 | 1,277 |
| kind | 2,073 | 436 | 142 | 578 |
| unknown | 2,512 | 885 | 1,050 | 1,935 |
| lost | 262 | 373 | 842 | 1,215 |

Texts with a legible word: 507 of 538 in `corpus_v6` (605 of 608 in `corpus_v5`, near-copies once); every legible word translated in 42 (106); one piece missing in 92 (122). Words whose spelling no analyst has seen: 1,026 in 925 spellings. Words that are a name by the source's own tag: 90.

### The check against the two editions, counted again

| | On `corpus_v5` | On the words that still stand in `corpus_v6` |
|---|---|---|
| Judged rows | 1,115 | 1,004 |
| Words the map counts as translated | 537 | 489 |
| of them given a meaning by the edition | 397 | 373 |
| of them with the map's meaning | 276 (69.5%) | 267 (71.6%) |

Not carried over: 111 of the 1,115 judged rows (95 because the word is spelled or divided otherwise in the preferred reading; 16 because the map's level is name).

<!-- end of the tables -->

## 5. What the recount shows

1. **More than half of the words of `corpus_v5` were copies.** The words of the texts that stand for an
   inscription are 30.1% of its 21,977 words. One Gebel Adda text, GA 28, stood 52 times.
2. **The coverage map loses two points on the same inscriptions, and this is the honest figure.** On the 289
   inscriptions that were in `corpus_v5` it translates 60.0% of the words, against 62.0% on `corpus_v5` and
   61.6% with near-copies counted once. Masked names counted as translated in every copy; a broken word now
   counts as one lost word where its pieces were read as words; and the rest of a swapped name is gone.
3. **The inscriptions new to the corpus are at 35.9%,** because no analyst has read their words: 1,026 words in
   925 spellings have only the lookup. This is what the build left undone on purpose, not a finding about the
   texts.
4. **The check against the two editions holds:** on the 1,004 judged rows that still stand in `corpus_v6`, the
   editions give the map's meaning for 71.6% of the words they translate (69.5% on `corpus_v5`). 111 judged
   rows are not carried over, most of them pieces of broken words and rests of swapped names.

## 6. What `corpus_v6` is not

- It is not complete: it holds what is in hand. Hallof's volume 7 would give the texts of REM 0001 to 2780.
- The Newsletter's texts and Otten's lines are in copyright or without a licence, so `data/corpus_v6.jsonl` is
  local. The public table (`data/inscriptions.jsonl`) gives every inscription with its numbers, site, kind and
  readings, and the text only of the open readings.
- The 34 texts of Millet 2005 and the 11 of FHN III are text layers, not typed readings: they confirm matches
  and are never the preferred reading. Nine Gebel Adda inscriptions are held in no other way and are in the
  table without a row in the corpus.

## 7. What is left open

1. **Three doubtful matches are not settled:** the readers differ on two and both guessed on one. The 3 texts of
   `corpus_v5` behind them are in no row.
2. **Eight texts quoted by Millet 1968 are not identified,** two of them long epitaphs (pp. 362 to 370 of the
   thesis). They are inscriptions of their own in the corpus until an edition is found that holds them. One of
   them may be Griffith's Meroë 27 or 28: Griffith printed only the benedictions of those two, the line has the
   same benedictions, and the readers could not say from that. These are the 2 pairs across numberings in the
   tables.
3. **Example phrases are out of the corpus.** A phrase quoted in a grammar is not an inscription. Where its
   source is not held (394 of the 906 match nothing held), its words are in no row. They stay in the local list
   of source lines, with Millet's translations where Otten typed them.
4. **Word division is one rule, not one practice.** Millet's spaces inside a group of words are partly line ends
   of the stone; the Newsletter sets some texts out by sense units. The coverage map joins 106 words written
   apart by its own rule; the corpus does not.
5. **The kind of text is not known for 112 inscriptions,** most of them from the 1971 printout, which gives only
   REM numbers. The reader quoted for this did not run.
6. **Names are marked only where Otten's files tag them:** 90 words. The names of the Karanòg rows are known to
   the coverage map from Griffith's tables, as before; the Newsletter's texts and Griffith's other volumes have
   no list of names.
7. **Site and kind are taken from the first source that states them;** two sources that differ (Newsletter 28
   and FHN on REM 0544) are both in the readings of the row.
8. **One thing the readers showed about Otten's files:** a line can hold two quotations. The build checks this
   only for the lines the readers placed.

## 8. Files, commands and cost

| File | What | Where |
|---|---|---|
| `data/inscriptions.jsonl` | every inscription: numbers, site, kind, readings with source and licence; texts of open readings only | public |
| `data/inscriptions_map.tsv` | every id of `corpus_v5`: what it is, its inscription, the shares both ways, who settled it | public |
| `data/discovery/corpus_v6_figures.json` | the counts | public |
| `data/corpus_v6.jsonl` | one row per inscription with a typed reading | local |
| `data/sources/v6/` | the table with all texts, the source lines, the readers' pack, key and answers, the recount | local |

```bash
python3 -I src/v6/build.py && python3 -I src/v6/recount.py && python3 -I src/v6/public.py
python3 -I src/v6/readings.py test
python3 -I src/v6/packs.py merge
python3 -I tests/test_corpus_v6.py
```

The first three lines need the local files (README, Data). The tests run on made-up rows and on the public
files, and skip the checks that read local ones.

**Cost.** The table, the map, the corpus and both recounts were built without an agent. The figures below are
the subagent tokens and running times that the task notifications report; they are written by hand, and they
are the only numbers on this page that no script counts.

<!-- cost: by hand, from the task notifications -->

| Run | Subagent tokens | Running time |
|---|---|---|
| Reader 1 of the doubtful matches | 126,699 | 1 min 11 s |
| Reader 2 of the doubtful matches | 126,366 | 1 min 8 s |
| Both readers | 253,065 | |

Quoted before the runs: about 300,000 for the two readers, 100,000 for a reader of kind and site (not run) and
500,000 for the review.

<!-- end of the cost -->
