# What the texts alone cannot tell: the project's negative results

Written on 2026-11-16. Mike, asked whether to draft a letter to a scholar or to write up the results: "Write up
the results". This page is that write-up. Every number on it is read from a figures file that a script in `src/`
writes, or, where no script writes one (the earlier trial in section 2, the comparison in section 4), quoted
from the page named beside it; each section links the page that holds the detail.

## In short

Meroitic can be read aloud, but most of its words are not understood. This project built a word-by-word map of
548 inscriptions (10,290 running words), merged into it the published meanings it could find and apply to the
texts, and then asked one question three ways: **can a careful reader get beyond what scholars have published,
from the texts alone?** The reader here is a language model, used as many independent readers, and every test
had its bar committed in git before it was run.

| Question | Test | Result |
|---|---|---|
| Can a word's meaning be told from the words around it? | A blind choice among four meanings, three runs | No. Readers agree on a wrong meaning for about one word in five whose true meaning is not offered. |
| Can new grammar be found and tested? | 73 rules, each tested on texts it was not found in | Not on this much text. 53 rules hold, and the sources already state or partly state 52 of them. |
| Do related languages help? | Word lists of ten Northern East Sudanic languages, Nubian among them, against 2,000 shuffles | No resemblance beyond the word series the family was argued from (p = 0.49 on words held out). |

The project has found no meaning of its own. What it has is the map, the tests, and a measured answer to why
the texts alone do not give more.

## 1. Where the map stands

- **Running words:** of the 7,077 running words that need a meaning (no name, no numeral, no lost sign), 4,186
  are translated: 59.1%. A plain lookup of the lexicon of 2003, word by word, gives 35.9%.
- **Distinct words:** 160 of about 1,283 distinct words have a meaning: 12.5% (between 11.8% and 15.6%, because
  the count of words is an estimate).
- **Whose meanings they are:** all of them were published by scholars. 127 come from Rilly's lexicon of 2003 and
  33 from later works that the project read and merged in. Meanings found by the project: 0.

Details: [map_layers.md](data/discovery/map_layers.md), [distinct_words.md](data/discovery/distinct_words.md).

## 2. A meaning cannot be told from the contexts

**The test.** A word is hidden behind a code. A reader sees up to twelve places where it stands, six words on
each side in the map's readings, and four meanings to choose from, or "none of these". Five readers answer each
word on their own. Beside the open words stand words whose meaning is accepted: two in three are shown with
their true meaning among the four, one in three without it. The second kind is the trap: there the right answer
is "none".

**The bars, set beforehand.** Where the true meaning is offered and the readers choose a meaning, at least 80% of
those choices must be right, on at least 8 words. Where it is not offered, at most 10% of the words may get a
meaning chosen ("none of these" is the right answer there).

| Run | Accepted words | A choice needs | Right, with the meaning offered | Wrongly chosen, without it |
|---|---|---|---|---|
| First | 38 | four of five readers | 13 of 17 (76.5%) | 2 of 11 (18.2%) |
| Second | 43 | all five | 16 of 17 (94.1%) | 3 of 13 (23.1%) |
| Third | 83 | all five | 36 of 37 (97.3%) | 6 of 27 (22.2%) |

The second bar was missed in every run, so no proposal for an open word was ever labelled as favoured.

**What it shows.**

- **With the right meaning on the table, five readers who agree are nearly always right.** That part works.
- **Without it, they agree on a wrong one about one time in five.** An open word is in that position whenever
  its true meaning is not among the proposals on record, and nobody knows when that is. So agreement cannot tell
  a right proposal from a wrong one. In the second run all five readers chose "silver" for a word where it is
  the proposal on record, and all five chose "silver" for the word for "god", where it was a filler.
- **A figure read off a test after the count is worth little.** After the first run, the stricter rule "all
  five agree" showed no wrong choice among 11 words. Set beforehand in the second run, it gave 3 of 13.
- **Context gives the kind of word, not the meaning.** In an earlier trial 27 words of known meaning were judged
  from their contexts alone, by one reader who was not blind: the kind of word came out right 26 times, the
  meaning 4 times, each time for a word that stands opposite a known partner (north and south, mother and
  father). It measures the method's reach, not a result ([REPORT.md](REPORT.md), day four, night).

Details: section 6 of [recurring_words.md](data/discovery/recurring_words.md),
[blind_test_2.md](data/discovery/blind_test_2.md), [blind_test_83.md](data/discovery/blind_test_83.md).

## 3. New grammar cannot be tested on this much text

**The test.** The 548 texts were dealt by lot into 329 for finding rules and 219 held back. Fresh agents, each
with one angle (the noun phrase, the verb, the clause, the endings, counting, the epitaph, the long texts,
spelling, in the first round), proposed rules from the first set. Each rule's count was written as a function and
committed before it was run on the held-back texts. A rule passed when it had at least 20 cases there, held in at least 80% of
them, and stood 30 points above the rate expected without it. A rule that passed counted as a finding of the
project only if two readers, each on their own, found it stated in none of the sources the project holds. The
bar for going on was 3 such findings.

| Over two rounds | Rules |
|---|---|
| Proposed | 73 |
| Passed on the held-back texts | 53 |
| Stated or partly stated in a source in hand | 52 |
| A finding of the project | 1 |

**What it shows.**

- **The grammar that can be tested is the grammar already described.** 90% of the cases of the first round's 41
  passed rules stand in epitaphs. Only the epitaph's formulas and the habits of the script come back 20 times in unseen texts, and
  Griffith described that frame in 1911.
- **Outside the epitaphs there are about 4,000 words.** A second round searched only those: its finders
  reported, each on its own, that the texts are too few and too broken for rules of word order.
- **The rules do not carry over to the long texts.** Applied to the seven texts of 100 words or more, the rules
  that passed speak of 51 of the 925 words without a meaning, and of 38 of those they say only that the word
  ends in `-eb`, like a plural.
- **The yield is small and real:** 53 rules that hold out of sample, 15 points where the count is sharper than
  what the sources in hand say, and one rule those sources do not state (inside a word the sign `q` is followed
  by o or e far more often than other consonants are). A grammar the project does not hold may state it.

Details: [grammar_pilot.md](data/discovery/grammar_pilot.md).

## 4. Related languages do not help with open word lists

Rilly placed Meroitic in the Northern East Sudanic family, beside Nubian. The project compared Meroitic words of
known meaning with the same meanings in word lists of ten languages of that family, first by plain likeness of
the letters and then by Rilly's 82 sound correspondences, against 2,000 shuffles of the Meroitic meanings. On
the words that were not used to build the correspondences the result is at chance (p = 0.49). The lexical case
for the family rests on the word series it was argued from, and open word lists add nothing a cognate search
could build on.

**How far this goes.** The test was small: 31 words that the correspondences were not built from, against lists
of a few hundred words a language (5,442 rows in all). It shows that short lists carry no signal that
generalises. Whole dictionaries were tried on 2026-11-17: the two of Nile Nubian, Reinisch 1879 and Lepsius
1880, typed whole, did no better (p = 0.598 against a shuffle within words of one length;
[outside_evidence.md](data/discovery/outside_evidence.md), section 2). Those of the other branches of the family
are fetched and not typed.

Details: [cognates_rules.md](data/discovery/cognates_rules.md).

## 5. Why

- **The corpus is small and formulaic.** 10,290 running words, most of them in epitaphs that repeat one frame.
- **Most spellings without a meaning stand alone.** Of the 2,357 distinct spellings without an accepted meaning
  on the first map, 154 stand in three texts or more. For the rest the texts give too few places to test a guess
  against.
- **Meanings in this field came from outside the texts:** a name written in two scripts, a loan from Egyptian,
  a parallel Egyptian formula, a related language. The project has read what it holds of that kind and merged
  what applied. It has no new evidence of that kind.

## 6. What went wrong on the way, for anyone who repeats this

- **Controls that tested the wrong thing.** Letters drawn by lot and put where a name stands were called a name,
  and rightly: in 5 of the 6 answers at the 3 such places of one reading. A control has to sit where the wrong
  answer is not the reasonable one.
- **Gains promised too high.** More than once the estimate of what a step would add ran well above what it
  added.
- **Plan items left out.** Three times a review found that a step had skipped a part of what was asked (the 86
  leftover places never given to checkers; the full list of accepted words; the parse of the long texts). All
  three were then done: the first laid 23 more places in the map (22 names and 1 word of grammar), the other two
  changed no result.

## 7. What would change the answer

- **More text.** The project holds 594 inscriptions (since 2026-11-17, with Griffith's 46 ostraca; the map is
  drawn on the 548 before them). Editions it does not hold contain more, and each new long text adds contexts for
  words that now stand alone.
- **Evidence from outside the texts:** a bilingual, or a published reading the project has not read.
- **A comparison with whole dictionaries of the related languages,** in the place of short word lists, with
  each meaning it proposes checked against the contexts. The two dictionaries of Nile Nubian did no better than
  the short lists (section 4); those of the other branches of the family are fetched and not typed.
- **Two more paths, tried since this page was written** ([outside_evidence.md](data/discovery/outside_evidence.md)):
  the Egyptian royal texts of the kings of Kush read beside the Meroitic ones, frame by frame, doubled the share
  of right meanings for hidden known words but stayed wrong three times in four (its bar missed); the personal
  names split into parts that come back in unseen names, but where a part stands did not tell readers its kind.
  The comparison with the two whole dictionaries of Nile Nubian missed its bar (p = 0.598). All three paths are
  set out in [NEXT_STEPS.md](NEXT_STEPS.md), section H.
- **The scholars' judgment** on 16 points of grammar and spelling: the 15 where the project's counts are
  sharper than its sources, and the one rule those sources do not state. And the grammars the project does not
  hold (Rilly 2007, Rilly and de Voogt 2012, Hintze 1979).

## 8. How to check this

Every test's rules were committed before its agents ran, and the commit times stand beside the answer files'
times on each page. `python3 -I src/themap.py`, `src/blind2.py` and `src/grammar.py` write the figures files;
`src/cognates_rules.py` prints the numbers of section 4, which its page gives; `tests/` holds a check for each
page's numbers. The corpus files, the lexicon and most of the agents' answers are not in the repository, because
they follow editions under copyright ([data/INDEX.md](data/INDEX.md) says which files are local and why); the
open readings of 396 inscriptions are.
