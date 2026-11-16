# Distinct words translated: the north star

Status on 2026-11-16: done, and corrected in review the same day (section 6). Figures: `distinct_words_figures.json`.
Script: `src/words.py`. Checks: `tests/test_words.py`.

**In short.** The corpus holds about 1,375 distinct words (between 1,117 and 1,452), and 160 of them have a
meaning: 11.6% (between 11.0% and 14.3%). Before the project it was the same: each of the 160 has its meaning in
the lexicon of 2003, and the project has added no meaning. The number of distinct words is an estimate: 445 are
words of the dictionary, the rest comes from a sample of the stems the map could not name, judged by two checkers.
68 of the 445 are endings, prefixes and particles that stand as a written word of their own (section 7).

## 1. What was asked

Mike, 2026-11-16, in his words:

- "why dont we have Distinct wrords translated? this sounds like a north star metric if we want the entire
  language translatable?"
- "anything we can do to know how to calc our north star metric?" The plan he was then given: "remove names and
  cut pieces, strip the known endings so forms of one word fall together, then have two checkers judge a sample".
- "do it and add to the table as the first row"
- After the first count, which gave a plain lookup of the lexicon as "before us": "“Before us” should really
  equal “Now”, 11.6%."

Requirements, one line each:

| | Requirement | State |
|---|---|---|
| R1 | "Distinct words translated": how many different words the corpus holds and how many of them have a meaning, the forms of one word counted once, names and cut pieces not counted as words. | In part: sections 3 to 6 count the dictionary words and estimate the other words from a sample, with a range, and names are not counted; but the endings and particles that stand as a written word of their own count as words, which the plan's "strip the known endings" does not do (section 7). |
| R2 | "know how to calc": the way of counting written down, run again by a script, with what it cannot show. | MET: sections 3, 4 and 7, `src/words.py` and its checks. |
| R3 | "add to the table as the first row": the value now, before the project, and after the next step. | MET: section 5. |
| R4 | Highest precision, toward the meaning of all words: nothing reported beyond the counts and the rules set beforehand, and plain about whose each meaning is. | MET: every figure here is in the figures file, counted from the local results; what changed after the rules were set is said where it stands (sections 4 to 6); no meaning counted is the project's own. |
| R5 | "“Before us” should really equal “Now”": the translated words were translated before the project, and the project added none. | MET: section 5. What a plain lookup reaches is given as the reach of the map only. |

## 2. Why spellings are not words

The corpus has 4,793 different spellings. A spelling is one written form, and one word has many: with endings and
prefixes, in variant writings, cut in two by an edition. So the share of spellings with a meaning (598 of the 2,955
that need one, 20.2%) is not the share of words with a meaning. For a spelling without a meaning nobody can say
offhand which word it belongs to.

## 3. How the words are counted

Every running word of the map of `corpus_v6` that needs a meaning (no name or numeral by the map's level, no lost
sign) is one of three things, by the pieces the map cuts it into:

- a **dictionary word**: it is built on an entry of the lexicon of 2003 that is no name. Its word is that entry,
  so all the spellings of one entry are one word, and a spelling built on two stems counts for both. The endings
  and prefixes beside a stem are no word of their own, and neither is a piece beside it that the map could not
  name (section 7). A word made only of endings and particles counts for those entries;
- a **name**: it is built on a name and on no stem. A name needs no meaning and is not counted;
- an **unnamed stem**: the map found no stem the lexicon has. What is left (the longest piece the map could not
  name, or the whole spelling) is the stem.

The dictionary words can be counted, and so can those whose meaning the lexicon calls established or probable:
these are the **translated** ones. 445 dictionary words are in use, and 160 of them are translated. There are
1,107 unnamed stems, under 1,350 running words; 975 of them stand in one place. The unnamed stems cannot be
counted as they stand. Some are names, pieces of longer words, forms of dictionary words the map missed, or one
word under two stems; most stand in one place.

## 4. The sample of the unnamed stems (bar set before the checkers are started)

240 of the unnamed stems, drawn by a fixed seed, each with the same chance, go to two checkers, each on its own,
in 10 packs of 24. A pack shows for each stem the spellings it was cut from, up to six places with six words on
each side and the map's reading of each, and the spellings that look like it, in the lexicon and among the other
unnamed stems.

A checker gives each stem one of six cases:

- **word**: a word of the language in its own right that no entry of the lexicon covers;
- **known**: a form of a word the lexicon has;
- **same**: the same word as another unnamed stem;
- **name**: a proper name or part of one;
- **piece**: no stem, but a piece of a longer word, or an ending or a sign alone;
- **unclear**: signs are lost, or too little is shown to decide.

The bar, set on 2026-11-16 before any checker was started (commit `845396b`):

1. A stem has a case only when both checkers give that case. Otherwise it is "not agreed".
2. If Cohen's kappa of the two checkers over the sampled stems is under 0.6, or a stem is not answered by both,
   nothing is taken: the brief is corrected and fresh checkers read again.
3. The number of distinct words among the unnamed stems is estimated from the sample. A stem that is the same
   word as another counts a half. The **point** takes the stems both checkers agree on and can decide: the share
   of them that are words, times the number of unnamed stems. The **low end** takes every stem that is unclear or
   not agreed as no word; the **high end** takes every one of them as a word; each end with the sample's 95%
   interval.
4. Distinct words are the dictionary words in use plus that estimate. The north star is the translated
   dictionary words over the distinct words, given as a point with its range.
5. "Before us" is counted on the same corpus with the lexicon looked up word by word and none of the project's
   analysts or corrections: the translated dictionary words that the lookup reaches, over the same number of
   distinct words (how many words the corpus holds does not depend on us).
6. A checker's file counts only for the stems of its own pack.

Point 5 was replaced after the first count, on Mike's word: before us is the same as now (section 5).

### The first reading missed the bar

20 checkers answered all 240 stems. Their Cohen's kappa is 0.53, under the bar of 0.6, so nothing is taken from
this reading. They agree on 169 stems and not on 71. Of the 71, 42 are "word" for one checker and "unclear" for
the other, 41 of them stems that stand in one place, most among words the map has no meaning for; 13 are "word"
against "name".

### The second reading: the same sample, the brief corrected (set before its checkers are started)

As point 2 of the bar says, the brief is corrected and fresh checkers read the same 240 stems again. Nothing else
changes: the sample, the packs' contents, the bar and the way of estimating are those above. The rules added to
the brief, set on 2026-11-16 before any checker of the second reading was started (commit `2d9a6a4`):

- A stem with no lost sign is a "word" unless something shown marks it as another case. That it stands once, or
  among words nobody understands, is no reason for "unclear": the edition wrote it as a word, and it counts as one
  until something shows otherwise.
- "Unclear" only when a sign is lost in the stem's own word or in the word right before or after it, or when the
  text has fewer than three words.
- "Name" only when the place gives a reason: the stem stands where names stand, or the map reads the word beside
  it as part of the same name.
- "Piece" only when the word beside it completes it to a spelling the lexicon has, or when the stem is one or two
  signs.
- "Known" and "same" only when the places support it, not on the look of the spelling alone.

These rules make the count cautious for the north star: a stem in doubt counts as a word, which makes the number
of distinct words larger and the share of them that is translated smaller.

### The second reading passed

20 other checkers answered all 240 stems. Their Cohen's kappa is 0.94 (bar 0.6), so this reading is taken.

| Case | First reading | Second reading |
|---|---|---|
| word | 99 | 158 |
| known | 1 | 3 |
| same | 7 | 5 |
| name | 8 | 3 |
| piece | 16 | 22 |
| unclear | 38 | 42 |
| not agreed | 71 | 7 |

So about two in three of the sampled stems are words of their own, one in eleven is a piece, one in six is
unclear (a sign lost in it or beside it, or a text of fewer than three words), and few are names or forms of a
word the lexicon has.

## 5. The north star

By the bar's rule the sample gives about 930 distinct words among the unnamed stems (between 672 and 1,007). With
the 445 dictionary words that makes about 1,375 distinct words in all (between 1,117 and 1,452).

| | Dictionary words translated | Share of the distinct words | Range |
|---|---|---|---|
| Now | 160 | 11.6% | 11.0% to 14.3% |
| Before us | 160 | 11.6% | 11.0% to 14.3% |
| With the recurring-words results in the map | 175 | 12.7% | 12.0% to 15.7% |

- **Now** is the map as it stands.
- **Before us** is the same, as Mike set it after the first count: each translated word has its meaning in the
  lexicon of 2003, so before the project these words were translated already, and the project has added no
  meaning. A plain lookup of the lexicon, word by word, reaches 351 of the 445 dictionary words and 136 of the
  160 translated ones; the other 24 stand in the corpus only in spellings the lookup does not know, and the
  project's map recognises them there. That is the reach of the map, which the rows of running words and of
  spellings measure, not a meaning added.
- **With the recurring-words results** ([the recurring open words](recurring_words.md)) 15 more dictionary words
  count as translated: those for which Rilly's work of 2016 or 2021 states a meaning that two checkers found to
  hold in at least one place. Those meanings are Rilly's and older than the project, so they would raise now and
  before us alike. The names and pieces of words that work found would change the count of words a little, and
  are not counted in.

The share moves when the map holds a meaning for one more dictionary word, a scholar's or one day the project's
own, or when the count of words is corrected. Recognising one more spelling of a word that is already translated
does not move it, which is why it stands so far under the share of running words translated (50.1%: 3,676 of the
7,331 that need a meaning).

## 6. What the review corrected

The count of section 5 is the first count with one correction, made in review after both readings: one entry of
the kind "name" counted as a dictionary word, because the script's list of the kinds of names was shorter than
the map's; it is a name now. It changes the dictionary side only (`counted()` in the script, over `identity()` as
it was set), so the sample, the checkers' answers and the estimate of the unnamed words stand as the bar set them.
The first count gave 160 of about 1,376 distinct words (11.6%, between 11.0% and 14.3%).

## 7. Limits and cost

- The number of distinct words is an estimate from 240 of 1,107 stems. The range takes the stems the checkers
  call unclear or do not agree on at both extremes, all words and no word, each with the sample's 95% interval, so
  it is wide on their account. It does not carry the errors below, which no sample measures.
- A word made only of endings and particles counts for those entries: 68 endings, prefixes and particles of the
  lexicon that stand as a written word of their own count as dictionary words, 33 of them translated. Among the
  unnamed stems the checkers' case "piece" takes an ending standing alone as no word, so the two sides of the
  count differ here, and the plan stripped the known endings. Counted as pieces, they would make the share 9.7%.
- By the second reading's rules a stem in doubt counts as a word, which makes the number of words larger and the
  share smaller. Another choice pushes the other way: a piece the map could not name in a word built on a stem of
  the lexicon is not counted (75 different pieces in 104 running words; 42 of them have three signs or more and
  are no unnamed stem anywhere). Were all 42 words, the share would be 11.3%.
- A word of the dictionary counts as one word even where the lexicon files two words under one spelling or one
  word under two entries.
- A stem the checkers judge the same word as another counts a half, which is exact only when the other is judged
  so too; and a stem judged a form of a word of the lexicon counts as no word even when the map uses no spelling
  of that word. Both are rules of the bar, kept as set.
- "Translated" is the lexicon's own judgment of 2003 (established or probable). A second scholar agrees for only
  part of these ([the lexicon's statuses](lexicon.md)).
- The two readings cost 40 fresh agents, 3,012,391 subagent tokens: 1,504,282 for the first reading and 1,508,109 for
  the second. The line each was started with is in `runs/prompts/WORDS_launch.md`.

What the count cannot show: the checkers are one model, so their agreement shows that a judgment can be repeated,
not that it is right; they see six words on each side, not the stone; and the corpus is what survives, so "all
words" means the words of these 548 inscriptions, not of the language.
