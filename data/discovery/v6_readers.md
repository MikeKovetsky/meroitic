# The spellings of the clean corpus that no analyst had read

[The clean corpus](corpus_v6.md) was built with 1,013 of its words, in 912 spellings, that no analyst had seen
(its section 5). On 2026-11-12 the analysts of the coverage map read them (`src/v6/readers.py`): the 930
spellings (1,038 running words) that the lookup leaves on `corpus_v6` and that no pack of the first run holds
(912 and 1,013 are counted after the map's corrections), in seven packs, and the 110 most frequent of them a
second time in an eighth pack. The brief (with one sentence added on the names of the new rows), the lexicon
table and the rule for a word read twice are those of [the coverage map](coverage.md); words that the source of
a reading tags as a personal name were not sent. The numbers are in
[`corpus_v6_readers.json`](corpus_v6_readers.json) and are checked by `tests/test_v6_readers.py`.

| | Words | Translated | Share |
|---|---|---|---|
| `corpus_v6` before | 10,290 | 5,280 | 51.3% |
| `corpus_v6` with the new answers | 10,290 | 5,419 | 52.7% |
| the Meroitic Newsletter's texts, before and after | 3,578 | 1,295 and 1,424 | 36.2% and 39.8% |

"Translated" here means translated by one lexicon. The second figure, the words built only on meanings that a
second scholar gives too, is counted beside it on [the lexicon's page](lexicon.md).

1. **139 words more are translated:** 77 are names that the analysts recognised, 59 are words with a meaning and
   3 are grammar words.
2. **Of the 930 spellings, 125 got a translated level** (68 names, 55 meanings, 2 grammar words), 194 a proposal
   of the lexicon, 61 only their kind, and 550 nothing.
3. **Why so few.** Every analyst reported the same two things: many of these "words" are pieces of a word that
   the edition prints in two parts, and many stand once, in a broken or an obscure text (the royal texts
   REM 1039, 1333 and 1361 above all). Joining the pieces mechanically, by the rule of the map's third
   correction without its limit on length, would translate 11 words more; it was not done.
4. **The bar, written before the run:** the two analysts should put at least 85% of the words read twice on the
   same side, translated or not. They do for 105 of 110 (95.5%), and give 92 the same level. The gain told to
   the project's owner beforehand was 265 to 385 words; it is 139, about half the lower figure. The estimate
   took the share that the analysts translated on the older texts, which are mostly epitaphs.
5. **The figures on the clean corpus's page stay as built,** without the new answers, and the map of `corpus_v5` is
   rebuilt from the same answers as before: the new packs are kept in a folder of their own.

**Cost,** by hand from the task notifications: eight analysts, 1,012,556 subagent tokens (133,497, 125,907,
130,241, 119,048, 126,556, 127,513 and 121,712 on the seven packs, 128,082 on the second reading), three to four
minutes each.

**What the review changed:** the joining of pieces without the limit on length, given as 12 words by a count
made by hand, is counted by `src/v6/readers.py` and gives 11; and `count` wrote its figures over those of the
readers of the clean corpus's doubtful matches (`data/sources/v6/readers/`, local), whose folder it shared; it
writes to `data/sources/v6/analysts/` now.
