# Whole texts translated: the rounds of F4

Step 25 of [`NEXT_STEPS.md`](../../NEXT_STEPS.md) (F4) asks for whole inscriptions translated and scored against a
scholar's printed rendering, and a page per text. [The pilot](f4_pilot.md) of 12 November scored one translator
on five texts and found that it added a readable text but no meaning over the map read word by word. This page
is what follows: several ways of translating compared on the same five texts, round by round, and then the best
of them scored once on the renderings that were held back. The script is [`src/f4r.py`](../../src/f4r.py).

The design, the bars, the expected scores and the rule for what is carried on were written here before any agent
of round one answered (13 November 2026).

## 1. What was asked

Mike's words on 13 November, and how each is taken up:

| # | His words | Taken as | State |
|---|---|---|---|
| 1 | "before we move to translating" | whole texts are translated, not single words glossed | round one below |
| 2 | "optimize for quality" | the way of translating is chosen by its score and its errors, not by its cost | sections 3 to 5 |
| 3 | "and speed of iterations" | one text per agent, all agents of a round side by side, one command per step | section 3 |
| 4 | "not for tokens" | no design is left out or cut down to save tokens; the cost is reported, not minimised | section 8 |

What F4 itself asks (step 25, written on 12 November): each inscription translated line by line from the lexicon
with a status for every word, the open words left open; scored against Millet's renderings and Griffith's own
translations; a page per text for the inscriptions whose source is in the public domain.

## 2. What the pilot left to fix

1. **The units:** the pilot's splitter marked a unit open whole where Millet translates a part of it (17 of 38
   open units), so those parts were never scored. Every rendering is cut again by a splitter with the same
   instructions but for that rule: a unit is open only when all of it is untranslated, and a phrase that joins a
   translated part to a Meroitic word left as it is, is cut in two.
2. **The judges** could not know that two names are one place (Atiye and Sedeinga). They may now use what they
   know for that one thing.
3. **The baseline** showed "?" for a word the map counts as unknown though its analyst glossed a part of it, a
   gloss the translator saw. The reading "glosses" below shows every gloss the translators see.

## 3. The design of a round

One text per agent, so that all agents of a step run side by side. The readings of round one, on the pilot's
five texts (GA47, GA41, GA28, GA53, GA37):

1. **pilot:** the pilot's translator, its answers of 12 November as they are, judged again on the new units.
2. **glosses:** the map's reading of every word, word by word (the pilot's baseline, with item 3 above fixed).
3. **writer:** one agent that sees only the map's reading of each word with its status, and the handbook, and
   writes them as sentences. It may not change what a word means.
4. **translator:** one agent with the pilot's materials (the map's readings, the lexicon's entries with F2's
   statuses and the other scholars' proposals), and three things more:
   - **rules that keep what the materials hold:** a vague gloss stays a vague gloss beside the Meroitic word
     ("the smlo (a title)") where the pilot's translator left the word open; a disputed word shows both
     readings, the one stood by first; a phrase of the description is one sentence about one relative;
   - **a handbook:** what the sources in hand say about the endings, about how an epitaph is built and about
     the recurring titles, gods and places, each line with its source and page. It is compiled by one agent
     from Rilly's lexicon, Rilly 2021, the *Fontes Historiae Nubiorum*, Griffith 1911 and 1912, Lipiński 2011 and
     the project's own pages, and then checked line by line against those pages by a second agent. Neither may
     open Millet's edition or the project's files that hold it;
   - **parallels:** the other places of the corpus where a word of the text stands, with the map's readings of
     the words around it.
5. **panel:** three such translators, each on its own, and an editor that makes one translation of the three;
   the editor may not add a meaning that none of the three gives.
6. **decoy:** the pilot translator's reading of another inscription (the pilot's pages sample), assigned as in
   the pilot.

Millet is taken out of every pack as in the pilot (his proposals in the lexicon, the meanings and notes that
name him, his weight in F2's statuses).

**The judges:** two per text (Claude Opus 5.5, as in the pilot), each with the readings in an order of its own,
at most 20 units a pack. The pilot's four verdicts and its score, (given + half of partly) over the scored
units, pooled over the texts, the mean of the two judges. Two rules are new: where a reading gives two meanings
for one word, the first is judged, and if only the second is the unit's meaning the verdict is "partly"; and the
judges may tell that two names are one place.

**What is tuning and what is a result.** The five texts have been seen: the rules above answer what the pilot's
page says of them. Scores on them choose a design; they are not the result. The result is the score of the
design carried on, on the 13 renderings held back (GA04, GA07, GA19, GA21, GA22, GA24, GA25, GA29, GA30, GA31,
GA39, GA43, GA54), whose units are cut now and read by nobody but their splitters and judges until then.

## 4. The bars, the expected scores and the rule, set before any agent of round one answered

| | Bar or expectation |
|---|---|
| The two judges' agreement on the four verdicts (Cohen's kappa), over the five real readings | 0.6 or more |
| Clean decoy units a judge calls given or partly | at most 10%, for each judge |
| glosses | 55% to 70% (the pilot's baseline had 60.5% on the old units) |
| pilot | 50% to 68% (58.3% on the old units) |
| writer | at most 3 points under the glosses |
| translator | 5 points or more over the glosses |
| panel | not under the translator |
| Units the translator and the panel get wrong | at most 5% each |

**The rule for what is carried to the held texts:** the reading with the best pooled score among the translator
and the panel whose share of wrong units is at most 2 points above the glosses'. A lead under 5 points over the
glosses is no lead: then the writer is carried if it is within 3 points of the glosses, and the glosses
themselves if it is not. If a bar of the judging is missed, the judging is changed first.

## 5. Round one, first judging: the order of the readings is clear, the judges' bar is missed

Run on 13 November 2026. The handbook: 124 sourced lines; its four checkers confirmed 80, corrected 43, dropped
none, and one (the opening sentence) was outside their ranges. The five renderings were cut into 115 units; 38
are open (1 of them with a translated part, against 17 in the pilot), 77 went to the judges and 75 are scored
(2 render Meroitic that is not in our copy).

| Reading | Expected | Judge 1 | Judge 2 | Mean | Given only | Wrong | Over the glosses |
|---|---|---|---|---|---|---|---|
| pilot | 50% to 68% | 70.7% | 68.0% | 69.3% | 53.3% | 4.0% | +2.7 |
| glosses | 55% to 70% | 68.7% | 64.7% | 66.7% | 50.7% | 6.7% | |
| writer | at most 3 points under the glosses | 76.7% | 71.3% | 74.0% | 58.7% | 5.3% | +7.3 |
| translator | 5 points or more over the glosses | 82.7% | 79.3% | 81.0% | 66.7% | 2.0% | +14.3 |
| panel | not under the translator | 83.3% | 83.3% | 83.3% | 71.3% | 2.0% | +16.7 |
| decoy | | 0.0% | 0.0% | 0.0% | 0.0% | | |

1. **The decoys' bar is met:** neither judge called any of its 72 clean decoy units given or partly.
2. **The agreement's bar is missed:** Cohen's kappa on the four verdicts is 0.58, under the 0.6 set beforehand
   (the same verdict on 288 of 375 lines). So, by the rule of section 4, nothing is carried on from this
   judging.
3. **Where the judges part:** in one text and on one question. GA28 has 240 of the 375 lines and a kappa of
   0.32; the other four texts agree on 133 of 135 lines. In GA28 the units are "she was related to X", and every
   reading says "nephew or niece of X" (the lexicon's `yetmde`) where Millet says "related to". One judge of a
   pack calls that given for all five readings and the other partly, and in other packs the other way round:
   the instructions call "a kin term of another degree" partly, and say nothing of a kin term where the
   rendering names none. Of the 87 lines judged differently, 82 are given against partly; on credited (given or
   partly) against not, the judges' kappa is 0.94.
4. **Both judges put the readings in the same order:** glosses, pilot, writer, translator, panel. The question
   they part on touches every reading alike, so it moves the scores and not the order.

**The change to the judging, written before the second judges answered:** one rule more. Where the rendering
says only that two people are related and the reading names the relation ("nephew or niece of"), or the other
way round, the verdict is "partly": one of them says more than the other. Everything else stays: the same
readings, the same units, the same bars, the same rule for what is carried on; 14 new judges, each with an
order of its own. Expected: the kappa at 0.6 or more; every score lower than above, since those units become
"partly" for both judges; the same order of the readings.

## 6. Round one, second judging: the bars are met and the panel is carried on

The same readings and units, 14 new judges, the rule on kinship added (13 November 2026).

| Reading | Expected | Judge 1 | Judge 2 | Mean | Given only | Wrong | Over the glosses |
|---|---|---|---|---|---|---|---|
| pilot | 50% to 68% | 65.3% | 64.7% | 65.0% | 42.7% | 4.7% | +2.0 |
| glosses | 55% to 70% | 62.7% | 63.3% | 63.0% | 42.7% | 6.7% | |
| writer | at most 3 points under the glosses | 67.3% | 72.0% | 69.7% | 50.7% | 5.3% | +6.7 |
| translator | 5 points or more over the glosses | 74.0% | 76.7% | 75.3% | 54.7% | 1.3% | +12.3 |
| panel | not under the translator | 78.0% | 78.0% | 78.0% | 60.0% | 1.3% | +15.0 |
| decoy | | 0.0% | 0.0% | 0.0% | 0.0% | | |

1. **Both bars are met.** The judges gave the same verdict on 361 of 375 lines (Cohen's kappa 0.94; in GA28
   227 of 240, kappa 0.90), and neither called any of its 72 clean decoy units given or partly.
2. **Every expectation held, and the writer did better than expected:** it does not lose meaning against the
   glosses, it gains 6.7 points, because it orders the words into the sentences the handbook describes.
3. **The order is the first judging's,** and every score is lower, as expected: the units "she was related to
   X" are now partly for both judges.
4. **Unit by unit against the glosses** (first and second judge): the panel is better on 22 and 21 of the 75
   units and worse on 2 and 2; the translator better on 16 and 19, worse on 2 and 2; the writer better on 5 and
   11 and worse on none.
5. **Where the gain is:** titles (18 units: glosses 63.9%, panel 91.7%), places (8 units: 75% and 100%) and
   the three relations the new splitters marked as such (33% and 100%). On the 34 units that name a person in a
   role the readings are close (61.0% to 64.7%): most of them are the "related to" units.
6. **By the rule of section 4 the panel is carried on:** the best pooled score among the translator and the
   panel, 15.0 points over the glosses, with fewer wrong units (1.3% against 6.7%).

How far to trust it: these are five texts that had been seen, and the rules of section 3 answer what the pilot
said of them. The panel's lead over one translator, 2.7 points, is 3 to 5 units of 75. GA28 holds 48 of the 75
units. GA47 scores 0 for every reading (2 units; our copy of it differs from the reading Millet renders).

## 7. The held texts: the design, the bars and the expected scores, set before any of their agents answered

The 13 renderings held back (section 3) are the result. Their units are cut already (307, of which 233 go to
the judges), by the splitters of section 2; nobody but those splitters has read them.

1. **The readings:** glosses, writer, translator (the first of the panel's three) and panel, made exactly as in
   round one, from the same handbook and rules; and a decoy.
2. **The decoys** are translations, by one translator of round one's design, of 13 inscriptions drawn for this
   purpose from the rows of `corpus_v6` with an open reading that are not from Gebel Adda: nine epitaphs, two
   royal or temple texts and two graffiti, of 8 to 60 words with at most a fifth lost. Each held text gets one,
   assigned so that the renderings and their decoys share as few content words as can be.
3. **The judges:** two per text, the second judging's rules (the kinship rule included), at most 20 units a
   pack, each with an order of its own.

| | Bar or expectation |
|---|---|
| The two judges' agreement on the four verdicts (Cohen's kappa), over the four real readings | 0.6 or more |
| Clean decoy units a judge calls given or partly | at most 10%, for each judge |
| glosses | 50% to 68% |
| panel | 62% to 80% |
| The panel's lead over the glosses | 8 to 18 points; **the bar: 5 points or more** |
| The panel over the translator | 0 to 5 points |
| The writer's lead over the glosses | 2 to 10 points |
| Units the panel gets wrong | at most 5% |

What the result will say, decided now:

1. Both bars met and the panel 5 points or more over the glosses: the panel's way of translating gives meaning
   that Millet's renderings can see, on texts it was not tuned on, and F4's pages are built with it.
2. The bars met and the lead under 5 points: round one's lead was a property of the five texts. The pages are
   then built by the writer if it is within 3 points of the glosses, and the tuning starts again on other texts.
3. A bar missed: the judging is changed first, as in section 5, and that is said.

The expected scores are lower than round one's because the copies of some held texts hold less of Millet's
reading (GA19 56%, GA07 64%, GA43 70% of his runs of letters), and because nothing was tuned on them.

## 8. The result on the held texts: the lead holds on texts nothing was tuned on

Run on 13 November 2026. The 13 renderings were cut into 307 units; 74 are open (3 of them with a translated
part), 233 went to the judges and 218 are scored (15 render Meroitic that is not in our copy, 7 of them in
GA19).

| Reading | Expected | Judge 1 | Judge 2 | Mean | Given only | Wrong | Over the glosses |
|---|---|---|---|---|---|---|---|
| glosses | 50% to 68% | 59.2% | 57.8% | 58.5% | 43.6% | 9.2% | |
| writer | 2 to 10 points over the glosses | 70.0% | 68.6% | 69.3% | 53.7% | 4.4% | +10.8 |
| translator | | 74.1% | 73.6% | 73.9% | 59.2% | 2.8% | +15.4 |
| panel | 62% to 80%; 8 to 18 points over the glosses | 75.5% | 74.3% | 74.9% | 59.9% | 2.3% | +16.4 |
| decoy | | 6.9% | 7.3% | 7.1% | 6.4% | | |

1. **Both bars are met.** The judges gave the same verdict on 807 of 872 lines (Cohen's kappa 0.88), and each
   called 1 of its 186 clean decoy units given or partly (0.5%; the bar is 10%). The decoys score 7.1% over all
   218 units because nine of them are epitaphs: on the units that share a word with the decoy (an invocation
   of Isis, a wish for water) a judge is right to credit it, and those units are not in the decoy measure.
2. **The panel leads the glosses by 16.4 points, over the bar of 5 and inside what was expected.** By section
   7 this is the result: this way of translating gives meaning that Millet's renderings can see, on texts it
   was not tuned on. The lead on the five tuning texts was 15.0.
3. **Every expectation held but one:** the writer gained 10.8 points, a little more than the 2 to 10 expected.
4. **The errors fall with the score:** the glosses are wrong on 9.2% of the units, the writer on 4.4%, the
   translator on 2.8%, the panel on 2.3%.
5. **Unit by unit against the glosses** (first and second judge): the panel is better on 56 and 55 of the 218
   units and worse on 2 and 2; the translator better on 52 and 54, worse on 3 and 2; the writer better on 40
   and 40, worse on 1 and 2.
6. **Where the gain is:** places (23 units: glosses 44.6%, panel 87.0%), other statements (22: 25.0% and
   53.4%), persons in a role (58: 66.8% and 81.5%), titles (48: 54.7% and 69.8%), formulae (11: 84.1% and
   97.7%). Relations gain least (34: 45.6% and 52.9%), and the invocations of gods are given by every reading.
7. **With each text weighing the same:** glosses 63.5%, writer 73.1%, translator 75.0%, panel 76.1%. The panel
   is at or above the glosses in each of the 13 texts.

How far to trust it, and what it does not show:

1. **The panel is not shown to beat one translator.** Its lead over the first of its three translators is 1.0
   point: 2 to 4 units of 218, with four agents a text against one. What carries the result is the translator's
   design (the rules, the handbook, the parallels), not the editing of three into one.
2. **Most of the gain is the handbook and the order of a sentence.** The writer sees no lexicon entry and no
   parallel, only the map's reading of each word and the handbook, and gets 10.8 of the 16.4 points.
3. **One scholar, one site, one kind of text.** All 18 renderings are Millet's, of inscriptions from Gebel
   Adda, 14 of them stelae. A score against them measures agreement with Millet (`yetmde`, `qo`).
4. **Two judges of one model with one set of instructions** agree; that shows the verdicts are stable.
5. **Millet is out of the packs only as far as the project's files carry him** (the pilot's page, section 8,
   item 7). The handbook's compiler and checkers were told not to open his edition; the handbook does not name
   him, which a check in the script enforces, and it left out seven meanings that rest on him alone.
6. **Three of the 13 editors ended with an API error after writing their answers** (a usage limit). Their
   answers are complete and pass the same checks as the others; their tokens were not reported.
7. **Not done:** the two renderings `corpus_v6` lacks, Griffith's own translations as a second rendering, and
   the pages themselves.

## 9. Cost

Subagent tokens, from the task notifications: the splitters 1,169,212 (18 agents); the handbook 555,173 and its
check 1,015,037; round one 3,565,443 (writers 433,229, translators 1,639,408, editors 534,641, judges 958,165)
and its second judging 953,178; the held texts 10,621,434 without three editors (writers 1,162,767, the decoys'
translators 1,380,334, translators 4,378,027, ten editors 1,145,844, judges 2,554,462). In all 17,879,477.

Per text of the held round: one translator about 112,000 tokens, the panel with its editor about 450,000. An
agent that reads one pack costs about 60,000 tokens before it reads a word of it, which is most of a short
text's cost: the pilot's translator, five texts to an agent, took 29,000 a text.

## 10. Files and commands

| File | What it holds | Where |
|---|---|---|
| `src/f4r.py` | the packs, the count, the rule | public |
| `f4_rounds_figures.json` | every number of this page; no edition text, no lexicon text | public |
| `data/sources/f4r/` | the handbook, the packs, the agents' answers, the keys | local |

```
python3 -I src/f4r.py split        # the splitters' packs, all 18 rendered texts
python3 -I src/f4r.py packs r1     # the writer's and the translators' packs
python3 -I src/f4r.py editors r1   # the editors' packs, once the translators have answered
python3 -I src/f4r.py handbook    # the checkers' verdicts applied to the compiled handbook
python3 -I src/f4r.py judges r1    # the judges' packs and the key
python3 -I src/f4r.py count r1
python3 -I src/f4r.py public r1    # writes f4_rounds_figures.json
python3 -I src/f4r.py judges r1b   # the second judging of round one's readings; then count and public r1b
python3 -I src/f4r.py packs held   # then editors, judges, count and public held, as for r1
```

The packs go to agents by hand: one agent per pack, told to read only that file and to write its answers file.
