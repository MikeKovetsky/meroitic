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

## 5. The result of round one

Not run yet.

## 6. Files and commands

| File | What it holds | Where |
|---|---|---|
| `src/f4r.py` | the packs, the count, the rule | public |
| `f4_rounds_figures.json` | every number of this page; no edition text, no lexicon text | public |
| `data/sources/f4r/` | the handbook, the packs, the agents' answers, the keys | local |

```
python3 -I src/f4r.py split        # the splitters' packs, all 18 rendered texts
python3 -I src/f4r.py packs r1     # the writer's and the translators' packs
python3 -I src/f4r.py editors r1   # the editors' packs, once the translators have answered
python3 -I src/f4r.py judges r1    # the judges' packs and the key
python3 -I src/f4r.py count r1
python3 -I src/f4r.py public r1    # writes f4_rounds_figures.json
```

The packs go to agents by hand: one agent per pack, told to read only that file and to write its answers file.
