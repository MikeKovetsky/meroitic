# The blind test with all 83 accepted words

Status on 2026-11-16: the test is counted and **no label is given**: one bar held and one was missed, as in
the run with 43 accepted words (section 6). Figures: `blind_test_83_figures.json`. Script: `src/blind2.py` (the
commands that end in `-83`). Checks: `tests/test_blind2.py`. The run with 43 accepted words is on
[blind_test_2.md](blind_test_2.md). What the readers were given:
[`runs/prompts/G6_choice_83.md`](../../runs/prompts/G6_choice_83.md).

## 1. What was asked

The plan of step G6 named "the 83 lexicon entries the map reads in three texts or more as accepted words,
instead of 38". The run of 15:42 took 43 of them and left 40 out (section 2 of
[blind_test_2.md](blind_test_2.md)). Mike, 2026-11-16, asked "G6 ran with 43 accepted words, not the 83 I had
planned, because only 5 of the 45 extra entries have a meaning that can be offered. Do you waive that
requirement, so the review can pass?": "No, do not waive". So the test is run again with all 83.

| | Requirement | State |
|---|---|---|
| R1 | "The 83 lexicon entries the map reads in three texts or more as accepted words, instead of 38." | Set: all 83 (section 2). |
| R2 | "The bar set beforehand at 'all five readers agree'." | Set: section 3. |
| R3 | "Fillers worded like the candidates." | Set: as in the run with 43 (section 2). |
| R4 | "If the bars hold, a proposal on record ... can be called favoured by the contexts." | Set: section 4. |
| R5 | The rules of section G: every bar committed before its readers are started, counts from a figures file, nothing called a meaning of ours. | The bars are in this page, committed before any reader is started. |

## 2. The words and what a reader sees

**The accepted words: 83.** The 43 of the last run, and the 40 it left out, each now with the meaning the lexicon
gives it, however coarse:

| The 40 | Entries | The meaning offered |
|---|---|---|
| A title of which only the kind of office is known | 20 | "a priestly title" (12), "an administrative title" (3), "an official under the viceroy" (2), "a household official of the ruler" (2), "a title, the office not known" (1) |
| A form or a variant of a word of the test | 15 | that word's meaning, in the form's shape ("viceroy", "the ruler", "of the ruler", "to bear (a child)", "chief envoy"); for the variants of two epithets, "a byname of Isis" and "a byname of Osiris"; for one, "a title, the office not known" |
| No meaning of its own in the lexicon, or not of the four kinds | 3 | what the lexicon says of it: "favourable", "a blessing", "all the way, from one place to another" |
| Also an open word of the test | 2 | "to give", "brother": the places where the map translates them; the open places stay an open word |

- **Offered and absent,** as before: in each kind every third accepted word by lot is shown without its true
  meaning: 27 of the 83. The other 56 are shown with it.
- **The open words: 33,** the same, with the places the map with its six layers still holds open.
- **Four options a word,** filled up by lot from one pool as in the last run: the accepted meanings and the
  proposals of the open words, those of the word's kind first, never two near meanings. Five groups of near
  meanings are added for the new words.
- **A coarse meaning is never a filler.** "A priestly title" would be true of any priestly title it stood beside.
  The five coarse meanings stand only as the true meaning of their own words.
- **What a reader sees,** the brief and the count of lines: as in the last run. The readings shown are those of
  the map with its six layers.
- **The readers:** five for each of 8 packs (116 words), each a fresh agent (Opus): 40. Seed 20261126.

*Corrected after the count, in wording only.* As first committed, this section gave three of the 40 meanings in
the wording of the packs. That wording, and that of a fourth meaning, follows the project's English of the
lexicon for four words in a row, which no public file of the project may do. They are given here and in the
figures in other words: "a household official of the ruler", "a byname of Isis", "a byname of Osiris" and, for
the predicate form of the word for ruler, "the ruler, as a predicate". What the readers saw is unchanged and
local (`data/sources/g6b/pack_wording.json`).

## 3. The bars, set before any reader is started

The bars of the last run, unchanged:

1. Every reader answers every word of its pack.
2. A choice needs all five readers: the same option from each ("none of these" is one).
3. Of the accepted words shown with their true meaning for which the readers make a choice other than "none",
   at least 80% are right, and there are at least 8 such words.
4. Of the accepted words shown without their true meaning, at most 10% get a choice other than "none" (of 27:
   two at most).
5. If a bar is missed, no label is given.

The bars are counted on all 83 words, as the plan says. The result is also given for each sort of word apart
(the 38 of the first test, the 5 of the last run, and the four sorts of the table above).

## 4. What an open word then is

As in the last run: **favoured by the contexts** when the bars hold and all five readers pick the same proposal;
**chosen, no label** when they do but a bar is missed; otherwise none of the four, a filler chosen, or no choice.
A label is not a translation: the map and the counts of the scoreboard stay as they are.

## 5. What has to be said beforehand

- **This is the third run of the test, and the first two each missed a bar.** A pass now would rest on one run
  of three. If a label is given, it carries that sentence wherever it stands.
- **Half of the new words are weak test items.** A reader can pick "a priestly title" from the gods named
  around a word without knowing anything of the word; and the forms and variants are the same words a second
  time. Counted with the rest they can lift both bars. That is why the result is given by sort.
- The 43 words of the last run are the same words again, with fresh readers and new lots.
- The other limits of [blind_test_2.md](blind_test_2.md), section 5, hold here too: accepted words are the easy
  ones, a proposal is favoured over three fillers only, and the readers are one model.
- No meaning found here is the project's own.

## 6. The result (counted at 18:02, no label given)

**The launch was interrupted.** The first 32 readers were started from 16:49, after the commit with the bars
(16:49:38); their answers came between 16:50 and 16:51. Then the session's usage limit stopped the launch. The
last 8 readers (three of pack 7 and the five of pack 8) were started at 18:01, 72 minutes after the commit, when
the limit was lifted; their answers came at 18:01. Nothing was changed in between: the 40 packs and the key were
written at 16:49:40 and not again. Every reader answered every word of its pack (116 words, five readers each).

| Bar | Result | |
|---|---|---|
| Every reader answers every word | 580 of 580 answers | met |
| Accepted words shown with their meaning: of those with a choice, at least 80% right, at least 8 such words | 36 of 37 right (97.3%) | met |
| Accepted words shown without their meaning: at most 10% get a choice | **6 of 27 (22.2%)** | **missed** |

By rule 5 of section 3 no label is given: no proposal is called favoured by the contexts.

**The accepted words, one by one.**

| | Shown with their meaning (56) | Shown without it (27) |
|---|---|---|
| All five pick the true meaning | 36 | (not offered) |
| All five pick a wrong meaning | 1 | 6 |
| All five say "none of these" | 4 | 5 |
| No choice (the five differ) | 15 | 16 |

- **The one wrong choice with the meaning offered:** "wife" was taken for "mother's kin".
- **The six wrong choices without it:** "general" was taken for "governor", "to plunder" for "to send", "small,
  young" for "great, elder", "a favourable sacrifice" for "life", "an administrative title" for "chief envoy",
  and "a priestly title" for "temple administrator". In each case all five readers agreed.

**By sort of word.**

| Sort of accepted word | Words | With the meaning: right, of those chosen | Without it: wrongly chosen |
|---|---|---|---|
| One of the 38 of the first test | 38 | 12 of 13 | 3 of 14 |
| One of the five that the run with 43 added | 5 | 3 of 3 | 0 of 1 |
| A title of which only the kind of office is known | 20 | 11 of 11 | 2 of 7 |
| A form or a variant of a word of the test | 15 | 8 of 8 | 1 of 2 |
| No meaning of its own, or not of the four kinds | 3 | 1 of 1 | 0 of 2 |
| Also an open word of the test | 2 | 1 of 1 | 0 of 1 |

The 40 words that are new here did what section 5 said they might: shown with their meaning, they were right
every time the readers chose (21 of 21). The miss does not come from them alone: among the 38 words of the first
test, 3 of 14 got a wrong choice.

**The open words (33), had the bars held.**

| | Words |
|---|---|
| All five pick the same proposal (no label) | 8 |
| All five pick a filler | 2 |
| All five say "none of these" | 3 |
| No choice | 20 |

The eight are `pl` (lord of), `wse` (of the country), `penn` (year), `mlowi` (health), `pqrtr` (great prince),
`yed` (silver), `wi` (brother) and `qomlise` (good god). They carry no label. Six of them had all five readers
of the run with 43 too; `ẖol`, chosen then, got no choice now. The two fillers chosen: "a great meal" for `attḫ`
and "priest of Amun" for `amero`.

**The three runs side by side.**

| | A choice needs | With the meaning offered: right, of those chosen | Without it: wrongly chosen |
|---|---|---|---|
| The first test | four of five | 13 of 17 (76.5%) | 2 of 11 (18.2%) |
| The run with 43 accepted words | all five | 16 of 17 (94.1%) | 3 of 13 (23.1%) |
| This run, with 83 | all five | 36 of 37 (97.3%) | 6 of 27 (22.2%) |

**What this shows.**

- **The pattern of the run with 43 held with 83 words.** With the right meaning among the four, five readers who
  agree are nearly always right. Without it, they agree on a wrong one about one time in four or five.
- **This is the method's third miss.** More accepted words did not mend the second bar; the easy ones among them
  only lifted the first.
- So no proposal on record can be called favoured by the contexts by this method. The eight proposals that all
  five chose stand as they stood: proposals.

**One pack showed one hidden spelling.** Pack 5 hid the word for "nephew, niece" (shown without its meaning) and
the word for "child" (shown with it). In one place the two are joined in one word, and the pack showed the letters
of the second as a piece cut off the first, as it shows any piece. A check found it after the count; no other
pack of this run, and none of the run with 43, shows a hidden spelling. It moved neither bar: all five readers
said "none of these" of the first and made no choice for the second, so neither word is among the choices
counted.

**A note on one entry.** The run with 43 filed `kroro` as a form or a variant of a word of the test. The lexicon
calls it a variant of `akroro`, which is not in the test and which the lexicon data in hand does not hold. That
run's table stands as it was committed; here the word is offered as "a title, the office not known".

Cost: 40 readers. 31 of them reported 2,406,801 tokens together (typed from the task notifications into
`data/sources/g6b/tokens.json`, local). The other nine wrote their complete answer files and were then cut off by
the usage limit before their last reply, so no count was reported for them, and none is estimated here.
