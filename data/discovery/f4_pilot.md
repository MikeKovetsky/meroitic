# Whole texts translated and scored: the pilot of F4

Step 25 of [`NEXT_STEPS.md`](../../NEXT_STEPS.md) (F4) asks for whole inscriptions translated from the project's
readings and scored against a scholar's printed rendering. This pilot does it for five texts, to size the full
run. The script is [`src/f4.py`](../../src/f4.py), its checks [`tests/test_f4.py`](../../tests/test_f4.py).

The design, the bars and the expected scores were committed (b990f42) before any agent answered; the run
followed the same evening, 12 November 2026. The numbers below are in
[`f4_pilot_figures.json`](f4_pilot_figures.json) and are checked by the tests.

## 1. Answer first

1. **The judging holds.** The two judges gave the same verdict on 112 of 114 lines (Cohen's kappa 0.97, bar
   0.6), and neither accepted any of its 56 clean decoy units (bar: at most a tenth).
2. **The translator does not beat the map read word by word.** Of Millet's 57 scored units of meaning, the
   translator gets 58.3% (given, and half of partly) and the baseline 60.5%: the translator trails by 2.2
   points. With each text weighing the same, a figure not set before the run, it leads by 4.0 (50.8% against
   46.8%). Either way the lead is under the 5 points set beforehand, so the translator adds no meaning that
   Millet's renderings can see.
3. **What the translator does add:** a text a reader can follow, the status of every word (14% of the words
   left open), and fewer errors: 3.5% of the units wrong, against 6.1% for the baseline.
4. **Where it loses:** it leaves open the words the map knows only vaguely, where the vague gloss earns half
   credit (`smlo`, "a title" in the map, Millet's "good person"), and it writes "nephew or niece" where Millet
   writes "related to" and the baseline's "relative" comes closer. Where it wins: places (`Skl` read as
   Sakala, once from a gloss of the map that the baseline did not show, section 8), and it drops the map's
   "this one is" where Millet reads "the noble one".
5. **The baseline beat its expectation by far:** 60.5% against 35% expected. An epitaph is a list in a fixed
   order, so glosses in order carry most of its meaning.
6. **The full run:** scoring Millet's 18 held renderings costs about 2.1 million subagent tokens at the pilot's
   rates (1.6 million for the 13 not in the pilot; with one judge, about 0.5 million less for the 18 and 0.4
   for the 13). Pages for the 303 inscriptions with an open reading would cost about 5.9 million with this
   translator, more than F4's whole estimate: by the rule set beforehand they should be built from the map's
   readings by a lighter step, which is not measured yet (section 7).
7. **Cost:** 560,981 subagent tokens for five agents, 1.6 times the 0.35 million expected, and 398,363 for the
   review: 959,344 in all (section 10).

## 2. The texts

N. B. Millet's "The Meroitic Inscriptions from Gebel Adda" (JSSEA 32, 2005) prints a rendering into English for 20
of its entries. `corpus_v6` holds 18 of them (not GA13 with GA16, nor GA15). By the object Millet describes,
14 are stelae (one of them two slabs), 3 offering tables and 1 a wooden label. The rule, fixed in `choose()`:

1. Of each kind but the stela, the entry whose copy in `corpus_v6` holds the largest share of Millet's text
   (runs of five letters, as the check against the editions counts them), then the longest: the label GA47 and
   the offering table GA41.
2. Of the stelae whose copy holds at least 85% of Millet's text (10 of 14), the longest, the lower median and
   the shortest by words in our copy: GA28 (85 words), GA53 (28) and GA37 (10).

The five hold 141 words. Our copies come from Millet's thesis of 1968, as Otten typed it; they differ from
the 2005 reading in places, most in GA47 (74% of Millet's runs are in our copy).

A second sample of five texts measures what a page of the 303 public-domain inscriptions costs: three epitaphs,
a temple text and a graffito, drawn by kind from the rows of `corpus_v6` whose reading is under an open licence,
of 8 to 60 words with at most a fifth lost (REM 0240, Meroe 27, REM 0209, REM 0405, REM 0091c; 82 words).

## 3. The design

1. **The translator** is one Claude Opus 5.5 agent per sample, blind to Millet's edition. Its pack holds the
   text of `corpus_v6`, the coverage map's reading of every word, every entry of Rilly's lexicon the words are
   built on with F2's status ([`lexicon.md`](lexicon.md)), the other scholars' proposals as the lexicon records
   them, and three sentences on the usual order of an epitaph. It gives every word a reading and a status
   (agreed, stated by one, disputed, proposed, from the context, from its own knowledge, name, number, open,
   lost), cuts the text into phrases, and writes one running translation in which what is open stays open.
2. **Millet is taken out of the pack.** Our copies are his reading of 1968, and his earlier proposals are in the
   lexicon. Left out: the 152 proposals in the lexicon that are his or speak of his, the lexicon's meanings and
   the analysts' notes that name him (in the pilot one meaning and one word's reading: `bqo`, the stem of `bqol`
   in GA53), and his weight in F2's statuses, which are counted again without his proposals and without the
   check against Millet 2005. That changes the status of 16 of the 177 entries: `qewi`, disputed through his reading, is stated by
   one; `t-dḫe`, agreed through it, is disputed.
3. **The baseline** is the map's reading of every word, word by word, and nothing else; a word whose reading is
   withheld from the translator is withheld here too. It shows what the translator adds to the map. Found in
   the review, after the run: a word the map counts as unknown is "?" in the baseline even where the map's
   analyst glossed a part of it, a gloss the translator saw (section 8, item 9).
4. **The splitter** is one agent that sees only Millet's transliteration and rendering of the five texts. It
   cuts each rendering into units of meaning (a person with a role, a relation, a title, a place, an invocation,
   a wish), each with the Meroitic it renders, its kind, Millet's doubt, and whether Millet leaves it
   untranslated ("open"). The task asked the two judges to split the renderings themselves; one blind
   splitter does it here instead, so that both judges mark the same units and their agreement can be counted
   unit by unit.
5. **The judges** are two agents. Each gets every text's rendering, its units that are not open, and three
   readings in an order of its own: the translator's, the baseline, and a decoy, which is the translator's
   reading of a text of the second sample. Each unit and reading gets one verdict: given, partly, wrong or
   missing. The decoys are assigned so that they share as few content words with the rendering as can be; a
   unit counts in the decoy measure only when its decoy shares no content word with it.
6. **The score** of a reading is (given + half of partly) divided by the scored units, pooled over the five
   texts, the mean of the two judges. The scored units are the units the judges get whose Meroitic stands in
   our copy; a figure with all units is given beside it.

## 4. The bars and the expected scores, set before any agent answered

| | Bar or expectation |
|---|---|
| The two judges' agreement on the four verdicts (Cohen's kappa), translator and baseline readings | 0.6 or more |
| Clean decoy units a judge calls given or partly | at most 10%, for each judge |
| The translator's score | about 50% (35% to 65%) |
| The baseline's score | about 35% (20% to 50%) |
| The translator's lead over the baseline | about 10 points |
| Units the translator gets wrong | at most 15% |
| Subagent tokens of the pilot, review aside | about 0.35 million |

What the pilot then says about the full run, decided beforehand:

1. If both bars are met and the translator leads the baseline by 5 points or more, the full run translates the
   scored texts and the pages with the translator.
2. If the lead is under 5 points, the translator adds readability and not meaning: the pages can be built from
   the baseline and a light writer, at a fraction of the cost.
3. If a bar is missed, the judging is changed before the full run.

## 5. The result

Millet's renderings of the five texts were cut into 98 units of meaning. The splitter marked 38 of them open,
where Millet keeps a Meroitic word in the rendering or leaves a gap (17 of them only in part, section 8), so 60
went to the judges; 57 are scored, because 3 render Meroitic that is not in our copy. Scores are (given + half
of partly) over the 57, pooled over the texts:

| | Expected | Judge 1 | Judge 2 | Mean | Given only | Wrong |
|---|---|---|---|---|---|---|
| The translator | about 50% (35% to 65%) | 58.8% | 57.9% | 58.3% | 33.3% | 3.5% |
| The baseline (the map, word by word) | about 35% (20% to 50%) | 60.5% | 60.5% | 60.5% | 38.6% | 6.1% |
| The decoy (another text's translation) | | 0% | 0% | 0% | 0% | 100% |

With all 60 judged units, the three not in our copy too: 57.1% and 59.2%. The decoys: both judges called all 57
decoy lines "wrong", and none of the 56 clean ones given or partly.

By text (the mean of the two judges; not set before the run, like the mean of the texts):

| Text | Object | Scored units | The translator | The baseline |
|---|---|---|---|---|
| GA47 | wooden label | 1 | 0% | 0% |
| GA41 | offering table | 5 | 70.0% | 70.0% |
| GA28 | stela | 39 | 56.4% | 64.1% |
| GA53 | stela | 10 | 65.0% | 50.0% |
| GA37 | stela | 2 | 62.5% | 50.0% |
| mean of the texts | | | 50.8% | 46.8% |

By the kind of unit, as the splitter marked it:

| Kind | Scored units | The translator | The baseline |
|---|---|---|---|
| a person with a role | 6 | 100% | 100% |
| an invocation of a god | 2 | 100% | 100% |
| a wish | 2 | 100% | 100% |
| a relation | 29 | 45.7% | 56.9% |
| a title | 8 | 43.8% | 56.3% |
| a place | 8 | 75.0% | 37.5% |
| other | 2 | 25.0% | 25.0% |

The translator's statuses, over the 223 words of both samples: 55 names, 41 agreed by two scholars, 41 only
proposed, 21 stated by one, 12 disputed, 12 read from the context, 2 from the model's own knowledge, 31 left
open and 8 with lost signs.

## 6. Where the two readings part

The first judge's verdict on the translator is better than on the baseline for 7 of the 57 units and worse for 11
(the second judge: 6 and 11), in the order given, partly, missing, wrong. Read one by one:

1. **The translator is more careful, and the score punishes it.** It leaves `smlo` and `mde` open, where the map
   has "a title" and "relative (mde) of" and Millet "good person" and "descended(?) from": the judges call the
   map's vague glosses "partly" and the translator's open word "missing" (4 units).
2. **Two readings of `yetmde`.** In GA28 the translator makes the closing `aqebetowi` "their nephew or niece";
   the map's gloss of it, "it is their (relative)", comes closer to Millet's "related to" (6 units). The lexicon
   reads `yetmde` "nephew, niece", Millet and FHN "relative" (the check against the editions, section 4).
3. **The translator reads places better, in part from glosses the baseline did not show:** `Skl` as Sakala (2
   units: one through lost signs, by the parallel of the `Sklte` the map reads "in Skl"; one in a word the map
   counts as unknown and glosses "in Skl", which the baseline gave as "?"), and `bedewitel` as "in Meroe",
   where the map has only the word's form. Its one wrong place, "in Meroe (?)" for Millet's Makhatebede (GA53),
   is the map's own gloss of such a word, which it followed.
4. **`qowi`:** the map's "this one is" is wrong against Millet's "the noble one"; the translator folds it into
   "This is X" and is called "missing" (2 units).
5. **Two relations inside words the map cannot read** the translator reads in part: "nephew or niece of" where
   Millet has "related to" (GA53), from the map's own gloss of that unknown word, which the baseline gave as
   "?"; and "of the mothers" where he has "the sister of" (GA37), in a word with lost signs, by the parallel of
   the same ending earlier in the text (the first judge only).

## 7. What the pilot says about the full run

1. **The rule set beforehand says the translator adds readability and not meaning.** Its lead is under 5
   points whichever way the texts are weighed. Its translation is what a visitor can read, with the status of
   every word shown; the baseline is a list of glosses.
2. **Per text:** the pilot's translator took 29,024 subagent tokens a text and the pages' translator 20,939;
   a scored text, with the splitter and both judges, took 91,257. Per word they come to 1,029 and 1,277 tokens:
   the texts of the pages sample are shorter, and each pack has a fixed part.
3. **The scored run:** Millet prints 20 renderings and `corpus_v6` holds 18 (549 words of text, 1,627 words
   of rendering). At the pilot's rates (1,029 tokens a word for the translator, 294 a word of rendering for the
   splitter, 588 a line for each judge, 0.18 judged units a word of rendering) the 18 cost about 2.06 million
   subagent tokens: 0.57 for the translator, 0.48 for the splitter, 1.02 for the two judges. The 13 not in
   this pilot need about 1.6 million. The judges agreed on 112 of 114 lines, so a second judge on a sample only
   would save up to about 0.5 million on the 18 (0.4 on the 13). The two renderings `corpus_v6` lacks would
   have to be typed in first (F1).
4. **The pages:** 303 inscriptions of F1's table have a reading under an open licence, with 4,625 words. For
   286 of them (4,118 words) that reading is the row of `corpus_v6`, which the map reads; for the other 17 the
   row holds another reading, so the map has not read the open one. At the pages translator's rate, 1,277
   tokens a word, the 303 cost about 5.9 million subagent tokens and the 286 about 5.3, above F4's estimate of
   2 to 4 million for all of it. Part of the rate is each pack's fixed part (instructions and lexicon entries),
   which larger packs would share; that is not measured. By item 1, the pages can be built from the map's
   readings with a lighter step that writes them as sentences and keeps each word's status; its cost and its
   score need a pilot of their own, on the same five texts.
5. **The scoring itself needs three changes before the full run:** the splitter should not mark a whole unit
   open when only a part of it is untranslated, the judges should be allowed to know that two names of a place
   are one place, and the baseline should get every gloss the translator gets (section 8, items 4, 6 and 9).

## 8. How far to trust it

1. **Five texts, one of them most of the units.** GA28 holds 39 of the 57 scored units. Pooled, the baseline
   leads by 2.2 points; with each text weighing the same, the translator leads by 4.0. The sign of the lead is
   not settled; its size is small either way.
2. **Two judges agreeing shows the verdicts are stable, not that they are right.** Both are the same model with
   the same instructions.
3. **The decoys were easy.** They were translations of other texts, with other names: they show that a judge
   does not credit a reading of another text, not how it weighs a vague reading of the right one, and "partly"
   is where the two readings part most.
4. **The splitter's "open" is coarse.** 17 of the 38 open units join a translated part to an untranslated word
   or a gap and are marked open whole, so they fall out for every reading: the invocations of Isis and of
   Osiris with their epithets in GA41 and GA53, a title of GA28 that Millet renders "chief" with the Meroitic
   word six times and another with "priest" three times, "the mother of ..." twice and the qorene "of Isis" in
   GA37, and one in GA53 (counted as the open units whose English holds a word that is not the Meroitic they
   render; before the review this item named four).
5. **The rule for units in our copy missed two of GA28's** (a name with lost signs, and `qowi`, spelled `qewi`
   in our copy). They count only in the figure with all 60 units.
6. **The judges could not use outside knowledge,** so both called "Sedeinga" wrong for Millet's "Atiye" (GA28,
   in both readings), and one called "Bedewi" wrong for "Meroe" (GA53, the baseline). These are the same places.
7. **Millet is out of the packs only as far as the project's files carry him.** Our copies are his reading of
   1968, and the translator is a model that may have read about these texts; it gave 2 of the 223 words a
   meaning from its own knowledge, and none of them is a unit it was credited for that the map lacks. The
   orchestrating session read some of the renderings while building the splitter's pack, after the
   translator's instructions were written.
8. **Millet's 2005 article is not a later authority than the lexicon:** where the two differ (`yetmde`, `qo`),
   a score against Millet measures agreement with Millet.
9. **The baseline did not get every gloss the translator saw** (found in the review, after the run). A word the
   map counts as unknown is "?" in the baseline even where the map's analyst glossed a part of it, and the
   translator's pack showed that gloss: 4 of the 141 words of the pilot, in GA28 and GA53. On such words the
   two readings part for one `Sklte` of GA28 ("in Skl": given to the translator, missing in the baseline) and
   for the relation and the place in GA53's `mxtebedetelyetmdelowi` ("nephew or niece of", partly, and "in
   Meroe (?)" for Millet's Makhatebede, wrong; the baseline missing both). On these units the comparison is
   not like for like: with those glosses the baseline could have earned the place and part of the relation,
   and been wrong on the other place as well. The full run should give both readings the same glosses.

## 9. Files

| File | What it holds | Where |
|---|---|---|
| `src/f4.py` | the choice of texts, the packs, the baseline, the count | public |
| `tests/test_f4.py` | the method on made-up texts and answers, and the numbers of this page | public |
| `f4_pilot_figures.json` | every number of this page but the review's cost; no edition text, no lexicon text | public |
| `data/sources/f4/` | the packs, the agents' answers, the key of the judges' orders and decoys | local |

```
python3 -I src/f4.py choose
python3 -I src/f4.py packs      # refuses once a translator or the splitter has answered
python3 -I src/f4.py judges     # refuses once a judge has answered
python3 -I src/f4.py count
python3 -I src/f4.py public     # writes f4_pilot_figures.json
python3 -I tests/test_f4.py
```

The packs go to agents by hand: one agent per pack, told to read only that file and to write its answers file.

## 10. Cost

Five agent runs, from the task notifications: the translator of the pilot 145,118 subagent tokens (about ten
minutes), the translator of the pages sample 104,696 (five), the splitter 99,501 (six), the judges 107,682 and
103,984 (six each). Together 560,981 tokens and about 32 minutes of running, in about 17 minutes of clock time,
since three and then two ran side by side. The review of the script and this page (full tier) took 398,363
subagent tokens and 34 minutes, by hand from its task notification: 959,344 in all, past the 0.8 million at which
the brief asked to check with Mike first. The review ended not clean on one line: the brief asked the judges to
split the renderings themselves, and one splitter did it (section 3, item 4).
