# The recurring open words

Status on 2026-11-13: in work. Sections 1 to 5 are written; the place pass of section 5 is running; section 6
(the test of the words that stay open) is written before that test runs.

## 1. What was asked

Mike, 2026-11-13, in his words:

- "ok, our goal is to decipher the meaning of all words. how far are we from it?"
- "did we collect all data we need to start working on recurring words with highest precision?"
- "start working on the 154 recurring words"
- Earlier the same day, on how to run the work: "optimize for quality and speed of iterations, not for tokens".

Requirements, one line each:

| | Requirement | State |
|---|---|---|
| R1 | Work on the 154 open spellings that stand in three texts or more. | In work: all 154 are in the pass. |
| R2 | Highest precision: nothing is called a meaning on one reader's word. | In work: every step has two independent readers and a bar written before they answer. |
| R3 | The aim is the meaning of the words, so a result says what is a meaning and what is not. | In work: a meaning a scholar states, a piece of another word, and an open word are kept apart. |

## 2. The 154 spellings are 121 items

The map of `corpus_v6` (548 inscriptions, 10,290 running words) holds 2,357 distinct spellings without an accepted
meaning. 154 of them stand in three texts or more and cover 1,108 running words. Spellings that the lexicon of 2003
files under one entry are one item (`pSixrkete`, `pSxrkte`, `xrkete`... are the verb `ḫr`): 121 items.

## 3. What the sources in hand say (the literature pass)

Ten readers, one per batch of items, collected every statement about each item from the sources in hand (the
lexicon of 2003; Rilly 2016 and 2021; FHN I to IV; Griffith; Millet; Hofmann; Lipiński 2011 and the others in
[the data index](../INDEX.md)). Each statement carries a quote, and a script looked for each quote in the file
named: 792 statements, 792 quotes found.

By rule, three classes:

| Class | Rule | Items | Spellings | Running words |
|---|---|---|---|---|
| A | A statement of Rilly 2016 or 2021 with the stance "accepts" or "probable". | 29 | 53 | 531 |
| B | No such statement, and the reader calls the spelling a piece of another word or of a name in some or all uses. | 52 | 58 | 370 |
| C | The rest. | 40 | 43 | 207 |

## 4. Class A read twice

The bar, written in the script before the readers answered: an item counts as "stated by a later source" only
when two readers, each on its own, give "accepts" or "probable" for the same source, and their meanings share a
content word.

Result: 26 of the 29 items pass. The three that do not: `sete` (both readers accept "mother", each names a
different work of Rilly as the firmest), `yini` (one reader finds only a proposal, and no meaning of the verb),
`ek` (no meaning stated; a piece of a verb in one text).

The readers also said, per spelling, whether the places shown (six an item at most) hold the word the source
speaks of. Taking the lower of the two answers, of the 520 running words of the 26 items: 251 "all", 164 "some",
105 "none". A meaning stated for a word is not a meaning for every place its spelling stands. So every place is
checked (section 5).

These 26 meanings are Rilly's readings of 2016 and 2021 (the benediction verbs "eat", "present, serve", "give";
the causative prefix; the plural optative ending; "prince", "brother", "life", "health", "take control"; the
emphatic particle after the copula; the objective case ending). The map is open on them because it rests on the
lexicon of 2003. None of them is a finding of this project.

## 5. The place pass (bar set before the checkers answer)

Every one of the 1,108 places goes to two checkers, each on its own, in 26 packs of at most 50 places. A pack
gives, for each item, the lexicon's line, the later statement if it passed section 4's bar, the statements found,
and every place with five words on each side and the map's reading of each.

For each place a checker says one of four cases:

- **stated**: the spelling here is the word of which the later source speaks, in the use it describes;
- **piece**: the spelling here is no word of its own, but part of a longer word or name that the edition's word
  division has cut; the checker names the whole word;
- **open**: a word of its own here, and no source states a meaning that applies to this place;
- **unclear**: signs are lost, or the context is too thin to decide.

The bar, set on 2026-11-13 before any checker answered:

1. A place is **stated** only when both checkers say "stated" there, and only for an item that passed section 4's
   bar. The meaning is the one that passed there; no new meaning enters at this step.
2. A place is a **piece** only when both say "piece" and name the same whole word (compared without spaces and
   hyphens).
3. A place is **open** only when both say "open".
4. Every other place is **not agreed** and stays as the map has it.
5. If Cohen's kappa of the two checkers over all places (four cases) is under 0.6, nothing is taken: the brief is
   corrected and fresh checkers read again.
6. A checker's file counts only for the places of its own pack.

What the pass cannot show: the checkers see five words on each side, not the stone. A "piece" verdict says that
two readers, from the same pack, name the same whole word; it does not replace the edition.

## 6. The test of the words that stay open

To be written before it runs.
