# The recurring open words

Status on 2026-11-13: in work. Sections 1 to 6 are written; the place pass of section 5 is counted in the log; the test of section 6 is
running.

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

## 6. The test of the words that stay open (bars set before any reader answers)

Earlier work in this project found that the words around an open word give its kind (a title, a verb, a name) and
seldom its meaning, and no reading of our own has held. So this test does not ask readers to invent meanings. It
asks a narrower question that can be scored: **can the contexts of a word tell the meaning a scholar has proposed
for it from other meanings of the same kind?** It is measured first on words whose meaning is accepted.

**The items.** Every item with three or more places that section 5's pass calls "open".

**Step 1, the candidates.** Two readers, each on its own, list for each item the meanings on record: a word or a
short phrase a source in the statements gives for the item in the use of its open places (not a kind such as "a
title"), three at most; and whether the sources accept the item as a proper name (of a place, a god, a person).
Rules, set beforehand: a candidate is kept only when both readers list it (their wordings share a content word);
an item counts as "a name by the sources" only when both say so with the stance "accepts" or "probable". An item
with no candidate kept does not enter step 2.

**Step 2, the choice, blind.** Each word is shown as a code. Its spelling, the spellings of the words around it and
the number of the text are not shown: a place is six readings on each side, as the map has them (an accepted
meaning, a name, a number; an unsure reading marked "(?)"; a word without a reading as `[?]`), with the endings the
map cuts off the word. Twelve places a word at most, drawn by a fixed seed. Under each word stand four meanings of
the same kind and "none of these". Five readers answer each pack, each on its own, with the meanings in an order of
its own; a reader sees one pack only, and the words of a pack are not shown as readings anywhere in that pack.

Three sorts of word are mixed, and a reader cannot tell which is which:

- **open words**: the options are the candidates kept in step 1, filled up to four with accepted meanings of other
  words of the same kind;
- **words with an accepted meaning, the meaning offered** (the lexicon of 2003 calls it established or probable
  and the map reads it): the options are the true meaning and three others of the same kind;
- **words with an accepted meaning, the meaning not offered**: four other meanings of the same kind. The right
  answer is "none of these".

The readers' **choice** for a word is the option that four or five of the five pick; otherwise there is no choice.

**The bars**, set on 2026-11-13 before any reader answered:

1. Among the accepted words with the meaning offered for which the readers make a choice other than "none", the
   choice is the true meaning for at least 80%, and there are at least 8 such words.
2. Among the accepted words with the meaning not offered, the readers choose a meaning (a wrong one) for at most
   10%.
3. Only if both hold: a candidate of an open word that is the readers' choice is called **favoured by the
   contexts**. The page gives beside it the share of accepted words whose true meaning was the choice, so that
   the number of true proposals the test would miss is plain.
4. Each favoured candidate then goes to two checkers who see everything (the spelling, every place, the
   statements) and look for a place or a statement that contradicts it. If both name the same contradiction the
   label is withdrawn.
5. Nothing from this test enters the map as an accepted meaning. A favoured candidate is "a proposal of its
   source, favoured by the contexts", no more.
6. A reader's file counts only for the words of its own pack.

**Added on 2026-11-13 after step 1 was counted and before any reader of step 2 answered:**

- Left out of step 2: the items that are names by the sources (a name has no meaning to choose), and the items
  whose first candidate is an ending or a numeral (the test has no accepted words of that kind to set beside
  them).
- Three candidates that leave a Meroitic word untranslated ("great womnise", "ate of Primis", "great paqar") are
  taken out: they are not meanings, and they would show the hidden word's spelling. A candidate whose content
  words an earlier candidate of the same item already has ("his brother" after "brother") is dropped.
- A reading of a neighbouring word that spells out a hidden word of the same pack is shown as withheld, and what
  stands in round brackets in a neighbour's reading is cut (such remarks name spellings and guesses).
- Each accepted word is one in three "meaning not offered", drawn by the fixed seed within its kind.

What the test cannot show: the readers are language models that may know published readings of Meroitic texts;
hiding the spellings and the text numbers lowers that risk and does not remove it. The accepted words are on
average commoner and stand in more fixed phrases than the open ones, so their score is an upper bound for what
contexts can do on the open words.
