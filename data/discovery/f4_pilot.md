# Whole texts translated and scored: the pilot of F4

Step 25 of [`NEXT_STEPS.md`](../../NEXT_STEPS.md) (F4) asks for whole inscriptions translated from the project's
readings and scored against a scholar's printed rendering. This pilot does it for five texts, to size the full
run. The script is [`src/f4.py`](../../src/f4.py), its checks [`tests/test_f4.py`](../../tests/test_f4.py).

**The results are not in yet.** This page was committed with the design, the bars and the expected scores before
any agent answered; the results follow in a later commit.

## 1. The texts

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

## 2. The design

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
   withheld from the translator is withheld here too. It shows what the translator adds to the map.
4. **The splitter** is one agent that sees only Millet's transliteration and rendering of the five texts. It
   cuts each rendering into units of meaning (a person with a role, a relation, a title, a place, an invocation,
   a wish), each with the Meroitic it renders, its kind, Millet's doubt, and whether Millet leaves it
   untranslated ("open").
5. **The judges** are two agents. Each gets every text's rendering, its units that are not open, and three
   readings in an order of its own: the translator's, the baseline, and a decoy, which is the translator's
   reading of a text of the second sample. Each unit and reading gets one verdict: given, partly, wrong or
   missing. The decoys are assigned so that they share as few content words with the rendering as can be; a
   unit counts in the decoy measure only when its decoy shares no content word with it.
6. **The score** of a reading is (given + half of partly) divided by the scored units, pooled over the five
   texts, the mean of the two judges. The scored units are the units the judges get whose Meroitic stands in
   our copy; a figure with all units is given beside it.

## 3. The bars and the expected scores, set before any agent answered

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

## 4. Files

| File | What it holds | Where |
|---|---|---|
| `src/f4.py` | the choice of texts, the packs, the baseline, the count | public |
| `tests/test_f4.py` | the method on made-up texts and answers, and the numbers of this page | public |
| `data/sources/f4/` | the packs, the agents' answers, the key of the judges' orders and decoys | local |

```
python3 -I src/f4.py choose
python3 -I src/f4.py packs      # refuses once a translator or the splitter has answered
python3 -I src/f4.py judges     # refuses once a judge has answered
python3 -I src/f4.py count
python3 -I tests/test_f4.py
```
