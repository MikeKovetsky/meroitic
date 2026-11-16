# Distinct words translated: the north star

Status on 2026-11-16: the count of the dictionary words is done; the first reading of the sample missed its bar;
the second reading is with its checkers. Script: `src/words.py`. Checks: `tests/test_words.py`.

## 1. What was asked

Mike, 2026-11-16, in his words:

- "why dont we have Distinct wrords translated? this sounds like a north star metric if we want the entire
  language translatable?"
- "anything we can do to know how to calc our north star metric?"
- "do it and add to the table as the first row"

Requirements, one line each:

| | Requirement | State |
|---|---|---|
| R1 | A way to count distinct words translated, the share of the different words of the corpus that have a meaning. | In work. |
| R2 | The count itself, to stand as the first row of the status table, with what it was before the project. | In work. |

## 2. Why spellings are not words

The corpus has 4,793 different spellings. A spelling is one written form, and one word has many: with endings and
prefixes, in variant writings, cut in two by an edition. So the share of spellings with a meaning is not the share
of words with a meaning. For a spelling without a meaning nobody can say offhand which word it belongs to.

## 3. How the words are counted

Every running word of the map of `corpus_v6` that needs a meaning (no name or numeral by the map's level, no lost
sign) is one of three things, by the pieces the map cuts it into:

- a **dictionary word**: it is built on an entry of the lexicon of 2003 that is no name. Its word is that entry,
  so all the spellings of one entry are one word. A word made only of endings and particles counts for those
  entries;
- a **name**: it is built on a name and on no stem. A name needs no meaning and is not counted;
- an **unnamed stem**: the map found no stem the lexicon has. What is left (the longest piece the map could not
  name, or the whole spelling) is the stem.

The dictionary words can be counted, and so can those whose meaning the lexicon calls established or probable:
these are the **translated** ones. The unnamed stems cannot be counted as they stand. Some are names, pieces of
longer words, forms of dictionary words the map missed, or one word under two stems; most stand in one place.

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

The bar, set on 2026-11-16 before any checker was started:

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

### The first reading missed the bar

20 checkers answered all 240 stems. Their Cohen's kappa is 0.53, under the bar of 0.6, so nothing is taken from
this reading. They agree on 169 stems and not on 71. Of the 71, 42 are "word" for one checker and "unclear" for
the other, most of them stems that stand once among words nobody understands; 13 are "word" against "name".

### The second reading: the same sample, the brief corrected (set before its checkers are started)

As point 2 of the bar says, the brief is corrected and fresh checkers read the same 240 stems again. Nothing else
changes: the sample, the packs' contents, the bar and the way of estimating are those above. The rules added to
the brief, set on 2026-11-16 before any checker of the second reading was started:

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

What the count cannot show: the checkers are one model, so their agreement shows that a judgment can be repeated,
not that it is right; they see six words on each side, not the stone; and the corpus is what survives, so "all
words" means the words of these 548 inscriptions, not of the language.
