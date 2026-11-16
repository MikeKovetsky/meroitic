# The recurring open words

Status on 2026-11-14: done, not applied to the map. Since 2026-11-16 the 385 resolved places are the map's first
layer ([map_layers.md](map_layers.md)); the numbers of this page are unchanged. Every bar was set before the agents it binds were started:
committed for the place pass and the test of the open words; for class A written in the working script, and in
git only with its result (section 9 gives the commits and the times). The results were counted on 2026-11-13.
Figures: `recurring_words_figures.json`. Script: `src/recurring.py`. Checks: `tests/test_recurring.py`.

**In short.** Of the 1,108 running words these 154 spellings cover, 273 take a meaning that Rilly states in 2016
or 2021, 192 are pieces of a longer word or name, 425 are words of their own that stay open, and 218 are unclear
or not agreed. Laid over the map, that moves the share of running words with a meaning from 50.1% to 53.9%. None
of it is a reading of this project. The test of the proposals on record for the open words missed both of its
bars, so no proposal gets a label.

## 1. What was asked

Mike, 2026-11-13, in his words:

- "ok, our goal is to decipher the meaning of all words. how far are we from it?"
- "did we collect all data we need to start working on recurring words with highest precision?"
- "make sure to index all the data we have in the doc"
- "start working on the 154 recurring words"
- Earlier the same day, on how to run the work: "optimize for quality and speed of iterations, not for tokens".

Requirements, one line each:

| | Requirement | State |
|---|---|---|
| R1 | Work on the 154 open spellings that stand in three texts or more. | MET: all 154 spellings and all 1,108 places went through sections 3 to 5; the 65 items that stay open went to section 6. |
| R2 | Highest precision: nothing is called a meaning on one reader's word. | MET: every step that can give a meaning, a piece or a label has two readers or more, each on its own, under a bar set before they were started (section 9); a place counts only where both agree. The literature pass, which only collects, had one reader a batch, and every quote it gave was checked by script. Limit: all readers are one model (section 8). |
| R3 | The aim is the meaning of the words, so a result says what is a meaning and what is not. | MET: a meaning a scholar states, a piece of another word, a name, and an open word are kept apart, and nothing is called a meaning of ours. |
| R4 | Index all the data we have. | MET: [the data index](../INDEX.md) lists every folder, the one of this work (`data/sources/recurring/`) and every source the literature pass read among them. |
| R5 | Quality and speed over tokens. | MET: two checkers for each of the 1,108 places, two readers for each item of class A and each open item, five for each word of the blind test, and a fresh agent for every pack: 101 in all (section 9). |

## 2. The 154 spellings are 121 items

The map of `corpus_v6` (548 inscriptions, 10,290 running words) holds 2,357 distinct spellings without an accepted
meaning. 154 of them stand in three texts or more and cover 1,108 running words. Spellings that the lexicon of 2003
files under one entry are one item (`pSixrkete`, `pSxrkte`, `xrkete`... are the verb `ḫr`): 121 items.

## 3. What the sources in hand say (the literature pass)

Ten readers, one per batch of items, collected the statements they found about each item in the sources in hand
(the lexicon of 2003; Rilly 2016 and 2021; FHN II to IV; Griffith's Karanòg, Meroitic Inscriptions and Meroitic
Studies; Meroe 1911; Millet 2005; Lipiński 2011; this project's own pages; all in
[the data index](../INDEX.md)). Each statement carries a quote, and a script looked for each quote in the file
named: 792 statements, 792 quotes found, for 120 of the 121 items. The brief is
`runs/prompts/RECURRING_literature.md`.

By rule, three classes (the rule sorts the readers' answers, so it was written after them; section 9):

| Class | Rule | Items | Spellings | Running words |
|---|---|---|---|---|
| A | A statement of Rilly 2016 or 2021 with the stance "accepts" or "probable". | 29 | 53 | 531 |
| B | No such statement, and the reader calls the spelling a piece of another word or of a name in some or all uses. | 52 | 58 | 370 |
| C | The rest. | 40 | 43 | 207 |

## 4. Class A read twice

The bar, written in the working script before the readers were started: an item counts as "stated by a later
source" only when two readers, each on its own, give "accepts" or "probable" for the same source; an item whose
two meanings share no content word was to go to a third reader. No item had such meanings. The meaning kept is
the first reader's.

Result: 26 of the 29 items pass. The three that do not: `sete` (both readers accept "mother", each names a
different work of Rilly as the firmest), `yini` (one reader finds only a proposal, and no meaning of the verb),
`ek` (no meaning stated; a piece of a verb in one text).

The readers also said, per spelling, whether the places shown (six an item, or one for each spelling of an item
that has more than six) hold the word the source speaks of. Taking the lower of the two answers, of the 520
running words of the 26 items: 251 "all", 164 "some", 105 "none". A meaning stated for a word is not a meaning
for every place its spelling stands. So every place is checked (section 5).

These 26 meanings are Rilly's readings of 2016 and 2021 (the benediction verbs "eat", "present, serve", "give";
the causative prefix; the plural optative ending; "prince", "brother", "life", "health", "take control"; the
emphatic particle after the copula; the case ending of the object). The map is open on them because it rests on the
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

### Result of the place pass

52 checkers answered all 1,108 places. Their Cohen's kappa is 0.91 (bar 0.6), so the pass is taken.

| Verdict | Places | In class A items | In class B items | In class C items |
|---|---|---|---|---|
| stated | 273 | 273 | 0 | 0 |
| piece | 192 | 55 | 137 | 0 |
| open | 425 | 106 | 117 | 202 |
| unclear | 139 | 49 | 88 | 2 |
| not agreed | 79 | 48 | 28 | 3 |

"unclear" is the places both checkers call unclear: lost signs, or too little context to decide. The bar puts them
among the places not agreed; they are counted apart here, and both stay as the map has them.

The 26 items of section 4, with the meaning as the first reader worded what Rilly states, and how many of the
item's places both checkers call "stated". Nine meanings in the figures file (four of this table, five candidates
of section 6) are given in our words where the reader's wording followed the lexicon of 2003 or Rilly's for four
words in a row; the packs and the answers, which are local, keep the readers' wording:

| Item | What the later source states | Source | Uses | Places stated |
|---|---|---|---|---|
| `-wi (5)` | particle of emphasis, optional, that follows the copula -o of the singular | Rilly 2021, p. 8 | 103 | 49 |
| `ḫr` | verb stem 'eat'; with the causative prefix, 'make eat' | Rilly 2021, p. 12 | 91 | 87 |
| `ẖol` | verb 'present, offer, serve' (a meal) in benedictions C and D | Rilly 2021, p. 42 | 77 | 64 |
| `ye- (2)` | eroded noun yet- 'person' in filiation terms, not a verbal prefix | Rilly 2021, p. 36 | 70 | 1 |
| `pqr` | prince, a title | Rilly 2016, p. 11 | 27 | 25 |
| `ps-` | prefix that makes a benediction verb causative ('make' drink, eat) | Rilly 2021, p. 43 | 19 | 3 |
| `-kete` | optative ending, 2nd person plural (-ke plural + -te) | Rilly 2021, p. 43 | 16 | 7 |
| `-w (1)` | objective (accusative/dative) case ending after noun phrases, variant of -xe | Rilly 2021, p. 27 | 14 | 1 |
| `wte` | life, lifetime | Rilly 2021, p. 57 | 12 | 5 |
| `l (2)` | to give | Rilly 2021, p. 13 | 10 | 4 |
| `wse` | 'his/her', a possessive (singular, third person), another form of qo-se | Rilly 2021, p. 41 | 10 | 2 |
| `mlowi` | health | Rilly 2021, p. 56 | 9 | 3 |
| `pl (2)` | verb 'to give, offer' in funerary benediction D | Rilly 2021, p. 82 | 8 | 0 |
| `-ketese` | plural optative ending -kete plus an optional emphatic particle -se | Rilly 2021, p. 43 | 6 | 5 |
| `yet (2)` | noun 'person', first element of yetmde 'nephew/niece' | Rilly 2021, p. 36 | 6 | 0 |
| `-i (2)` | vocative suffix -i ('O Isis!') | Rilly 2016, p. 10 | 5 | 0 |
| `wi (1)` | brother (wide, which becomes wi- when the article follows) | Rilly 2016, p. 11 | 5 | 0 |
| `-lowi` | article -l, singular copula -o and emphatic -wi: '(he/she) was' | Rilly 2016, p. 10 | 4 | 0 |
| `-se (1)` | genitive suffix, here with article and copula: 'it is of X' | Rilly 2021, p. 8 | 4 | 4 |
| `mde` | the mother's family, in a matrilineal society | Rilly 2021, p. 36 | 4 | 0 |
| `wide` | brother | Rilly 2021, p. 52 | 4 | 3 |
| `yiroẖe` | take under one's protection; also take control | Rilly 2021, p. 57 | 4 | 0 |
| `Stqo` | these feet: st 'foot/feet' with demonstrative qo | Rilly 2021, p. 9 | 3 | 3 |
| `ato` | water | Rilly 2016, p. 11 | 3 | 3 |
| `bqo` | take control (of) | Rilly 2021, p. 38 | 3 | 1 |
| `tḫ (1)` | present (a meal); with causative prefix, have someone presented | Rilly 2021, p. 42 | 3 | 3 |

Seven of the 26 have no place stated (`pl (2)`, `yet (2)`, `-i (2)`, `wi (1)`, `-lowi`, `mde`, `yiroẖe`), and
`ye- (2)` has one in 70: the source speaks of the word, and in our corpus the checkers find the same spelling a
piece of another word, a word of its own in another use, or unclear, or do not agree.

A check by script, apart from the checkers, on the two largest groups: all 87 stated places of `ḫr` ("eat") have
a form of `at` (bread; `ato`, water, does not count) among the three words before them, and 54 of the 64 stated
places of `ẖol` ("present, serve") have a form of `ḫmlol` (a good meal) there. The script looks for one spelling
only; it does not say what the other 10 hold.

The 192 pieces: the whole word both checkers name is a word the map already reads for 35 places, a name the map
has for 31, a word the map holds open for 60, and no form of the map for 66.

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

### Result of step 1

65 items keep three or more open places (389 places). For 48 of them both readers list a candidate; for 17 they
list none. Seven are names by the sources: `Akine` and `Simlo` (places), `Aritene` and `Ms` (gods), `brtoye`,
`doke` and `yeseboẖe` (persons).

### Result of step 2

71 words went into five packs: 33 open words, 27 accepted words with the meaning offered, 11 with the meaning not
offered. 25 readers answered; every reader answered every word of its pack. Of the 48 items with a candidate, the
rules added before step 2 left out 15: 8 whose first candidate is a function word (an ending or a particle), 4
names by the sources, 2 whose first candidate is a numeral, and 1 with no candidate left after the removals
(`atepedemo`, "ate of Primis").

| | Words | The readers choose a meaning | The choice is right | The choice is "none" | No choice |
|---|---|---|---|---|---|
| Accepted, meaning offered | 27 | 17 | 13 | 0 | 10 |
| Accepted, meaning not offered | 11 | 2 (both wrong) | | 6 | 3 |

- **Bar 1 is missed.** Where the readers chose a meaning for an accepted word, it was the true one for 13 of 17
  (76.5%; the bar is 80%). The four wrong choices: `mlo` "good" read as "great, elder" and `perite` "agent" as
  "priest" and `ḫrpḫe` "to order, to command" as "to love, to revere" by all five readers, `kdise` "sister" as
  "direct descendant" by four.
- **Bar 2 is missed.** Where the true meaning was not offered, the readers still chose a meaning for 2 of 11
  (18.2%; the bar is 10%): `ḫmlol` "a good meal" as "life", `tre` "to give" as "to drink", four readers each.
- The true meaning was the readers' choice for 13 of the 27 accepted words that had it among the options
  (48.1%).

**So no candidate is called favoured by the contexts**, and step 4 (the two checkers of each favoured
candidate) did not run. What the readers did on the 33 open words, for the record and without a label:

- a candidate chosen, 13 words (the table below);
- a filler chosen, 2 words: `tiso` as "to love, to revere" (five readers) and `ado` as "direct descendant"
  (four). Both are wrong by construction: the fillers are meanings of other words;
- "none of the four", 5 words; no choice, 13 words.

| Open word | The candidate the readers chose | Who gives it (stance) | Readers |
|---|---|---|---|
| `penn` | year | Millet 2005 (proposes) | 5 of 5 |
| `wse` | of the country | Millet (proposes) | 5 of 5 |
| `ẖol` | to present | Rilly 2021 (accepts) | 5 of 5 |
| `mlomrse` | notable | Rilly 2003 (proposes) | 4 of 5 |
| `yeso` | written by | Priese (in Rilly 2003) (proposes) | 4 of 5 |
| `yed` | silver | Rilly 2003 (proposes) | 5 of 5 |
| `attḫ` | beneficial water offering | Abdalla (proposes) | 4 of 5 |
| `mlowi` | health | Rilly 2021 (accepts) | 5 of 5 |
| `pl (2)` | lord of | Meroe 1911 (proposes) | 4 of 5 |
| `amero` | temple bread administrator | Almagro (proposes) | 4 of 5 |
| `qomlise` | good god | Rilly 2003 (proposes) | 5 of 5 |
| `dete` | given | Priese (proposes) | 4 of 5 |
| `pqrtr` | great prince | Heyler-Leclant (proposes) | 5 of 5 |

These 13 are what a test that missed its bars produced. They are no evidence for the candidates: on the accepted
words the same readers, agreeing as often, were wrong about one time in four, and the candidates differ in style
from the fillers beside them (a scholar's phrase among plain words), which a reader may pick up.

Seen after the count, so not a bar and not a result: on the words where all five readers picked the same
meaning, 12 of 15 accepted words were right and no wrong meaning was chosen where the true one was not offered. A
later round could set "all five" as its bar beforehand, with more accepted words.

## 7. What it changes in the count of words with a meaning

The map is not touched. `src/recurring.py recount` lays the results over it (local file `overlay.jsonl`) and
counts again. A running word "has a meaning" when the map reads it (a meaning or a grammatical function); names,
numerals and words with lost signs need none.

| Of the 10,290 running words | The map | With the overlay |
|---|---|---|
| have a meaning | 3,676 | 3,916 |
| names and numerals | 1,743 | 1,809 |
| open | 3,655 | 3,349 |
| signs lost | 1,216 | 1,216 |
| **Share with a meaning, of those that need one** | **50.1%** | **53.9%** |

The overlay holds 385 places: the 273 stated ones, 66 pieces of a word the map reads (35) or of a name (31), and
the 46 open places of the seven names. 79 of the 385 were already read or named in the map at that place (the
154 spellings were chosen by their most common level), so the count of open words falls by 306.

Of the 154 spellings, the overlay resolves every place of 27, more than half the places of 39 (the 27 among
them), and no place of 92.

## 8. Limits, and what was not done

- **Every reader and checker is one model** (Claude Opus 5.5, fresh agents). Two of them agreeing shows that a
  reading of the pack can be repeated, not that it is right. The quotes were checked by script against the files,
  and two groups of places against their formula (section 5); the rest rests on the agents.
- **The literature pass had one reader a batch.** A script checked its quotes, but a statement that reader did
  not find is missing from every later step: the checkers saw only the statements found, and only an item with
  a later statement found could have places "stated". The works not held ([the data index](../INDEX.md), section
  4: Hallof's dictionary, Rilly 2007 and 2010, Hofmann 1981, Hintze 1979) may state meanings for words that stay
  open here.
- **The stated meanings are one scholar's** (Rilly 2016, 2021). In the terms of the lexicon's check they are
  "stated by one", not "agreed by two scholars". `sete` shows the difference: Rilly reads "mother", and Millet
  2005 rejects that where the word is plural.
- **The overlay is not in the map.** The public figures of the coverage map and of the translations stand as they
  were. Applying it is a change to the map's build and its pages, with its own review.
- 79 places are not agreed and 139 are unclear: they stay as the map has them.
- The 2,203 open spellings that stand in one or two texts were not in this work.
- No meaning was looked for by a new method. Section 6 tested proposals already on record, and found that the
  contexts as the map shows them do not tell meanings of one kind apart well enough to label any.

## 9. Cost, when each bar was set, and how to run it again

101 fresh agents, 9,846,666 subagent tokens: the literature pass 2,411,497 (10 agents), the two readers of class
A 613,355 (6), the place checkers 4,146,199 (52), the candidate readers 780,535 (8), the blind readers 1,895,080
(25). The line each was started with is in `runs/prompts/RECURRING_launch.md`.

When each rule and bar was set, on 2026-11-13 (Pacific time). "Set" is the commit's time in git, or the time of
the working script's file (`data/sources/recurring/old_scripts/verify.py`, local) or of the session's command;
"started" is the step's first agent in the session's log; "first answer" is the earliest of the step's answer
files.

| Step | Set in | Set | Agents started | First answer |
|---|---|---|---|---|
| the classes (section 3) | the working session, not committed | 15:57:05 | 15:46:21 | 15:53:08 |
| class A read twice (section 4) | the working script, not committed | 15:58:05 | 15:58:10 | 15:59:59 |
| the place pass (section 5) | e3fdb9f | 16:06:33 | 16:06:41 | 16:07:27 |
| the choice test, step 1 (section 6) | 60f7bd8 | 16:14:24 | 16:15:12 | 16:16:01 |
| the choice test, step 2 (section 6) | fff9478 | 16:19:20 | 16:19:25 | 16:20:29 |

The classes sort the literature pass's answers, so their rule was written after those answers, and before the
readers of class A were started. The bar of class A went into git with its result, in e3fdb9f. The bars of step 2
are those of 60f7bd8; fff9478 adds what was fixed after step 1 was counted.

The commands are listed at the head of `src/recurring.py`. They need local files (the map, the lexicon of 2003,
the source texts, the agents' answers), so they do not run from a clone; `python3 -I tests/test_recurring.py`
does, on made-up data, and checks this page against the figures.
