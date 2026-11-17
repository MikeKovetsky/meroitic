# The leftover parts, read again (the second reading of part 1)

Status on 2026-11-16: the second reading is counted and **its bars are met** (section 5). It is the map's sixth
layer, `leftover`: 32 places, 27 of them translated words and 5 names. Figures: `leftover_parts_figures.json`
(under `part_1_again`). Script: `src/leftover.py`. Checks: `tests/test_leftover.py`. The first reading and the
step's other part are on [leftover_parts.md](leftover_parts.md). The 86 places that neither reading was given,
where the unnamed part is the stem itself, were judged afterwards, with bars for a name too
([leftover_stems.md](leftover_stems.md)). What the checkers were given:
[`runs/prompts/G8_parts_2.md`](../../runs/prompts/G8_parts_2.md).

## 1. What was asked

The first reading of part 1 missed one bar by one answer and was not taken (section 6 of
[leftover_parts.md](leftover_parts.md)). Mike, 2026-11-16, to "Should I read part 1 again with a separate bar for
each verdict?": "Yes, read again".

| | Requirement | State |
|---|---|---|
| R1 | "Read part 1 again." | Set: the same 96 places, fresh checkers, controls drawn anew (section 2). |
| R2 | "With a separate bar for each verdict." | Set: section 3. |
| R3 | The rules of section G: every bar committed before its checkers are started, counts from a figures file, nothing called a meaning of ours. | The bars are in this page, committed before any checker is started. |

## 2. What stays and what changes

**Stays:**

- **The places:** the same 96 (68 of G2, 28 of G4), on the map with the four layers laid when the step was set.
- **What a checker sees, and the brief:** word for word those of the first reading, with its five cases
  (ending, known word, name, unknown, unclear), so that the two readings can be laid side by side.
- **The kinds of control:** 20 translated words with their endings shown as unnamed (the answer: ending), and
  20 translated words with three to five letters drawn by lot put before or after them (the answer: unknown).

**Changes:**

- **Everything is drawn anew** with the seed 20261125: the 40 controls, the order of the places, the packs.
- **Six fresh checkers** (two for each of 3 packs, Opus), none of them from the first reading.
- **A name is no longer laid.** The first reading showed that letters which stand where a name is expected are
  called a name, whatever they are, and no control can tell a real name from that. A place both checkers call a
  name stays open.
- **The bar on the letters drawn by lot counts what can still be laid:** an ending or a known word.

## 3. The bars, set before any checker is started

1. Every place of a pack is answered by both of its checkers.
2. Cohen's kappa of the two checkers over the five cases, on the real places, is 0.6 or more.
3. **For "ending" and "known word":** each checker calls at most 2 of the 20 runs of letters drawn by lot an
   ending or a known word.
4. **For "ending":** each checker calls at least 14 of the 20 hidden endings an ending.
5. **For "a name":** no bar, because nothing rests on it any more.
6. If a bar is missed, nothing is taken, and there is no third reading.

**What a place then is:**

- **laid** when both checkers call the unnamed part an ending, or both call it a known word and name the same
  entry, which the lexicon calls established or probable; and no other stem of the spelling is without a
  meaning. The place takes the level of its entry, as in [the rare spellings](rare_spellings.md);
- **open,** as it is, in every other case.

## 4. What has to be said beforehand

- **The first reading's answers would have met these bars:** neither checker called a run of lot letters an
  ending or a known word, and both found all 20 hidden endings. That is the reason the bars are judged on a new
  reading by fresh checkers with new controls, and not on the first: a bar cut to fit answers already seen
  proves nothing.
- Letters drawn by lot are easier to see through than a real unknown word joined to a known one.
- The checkers are one model: their agreement shows that a judgment can be repeated, not that it is right.
- No meaning found here is the project's own: a place that is laid takes the meaning the lexicon or a later
  source already gives its entry.

## 5. The result (counted at 15:53, bars met)

The six checkers were started at 15:51, after the commit with the bars (15:51:18); their answers came between
15:52 and 15:53.

| Bar | Result | |
|---|---|---|
| Every place answered by both | 136 of 136 (96 places, 40 controls) | met |
| Kappa of 0.6 or more on the real places | 0.66 | met |
| Each checker calls at most 2 of 20 runs of lot letters an ending or a known word | 0 and 1 | met |
| Each checker calls at least 14 of 20 hidden endings an ending | 20 and 19 | met |

| Both checkers say, of the 96 places | Places |
|---|---|
| unknown | 37 |
| ending | 32 |
| a name (not laid) | 6 |
| a known word, the same entry | 1 |
| not agreed | 20 |

**What can be laid: 32 places.** 27 become translated words and 5 become names (their entry is a name by the
lexicon). One place both checkers call an ending stays open, because another stem of its spelling has no
meaning. The 6 places both call a name stay open, as the rule says.

**The two readings side by side** (the first was not taken):

| | First | Second |
|---|---|---|
| Kappa | 0.77 | 0.66 |
| Both say ending | 40 | 32 |
| Both say unknown | 28 | 37 |
| Both say a name | 12 | 6 |
| Not agreed | 14 | 20 |

The second reading agrees less and gives less, and it is the one that counts. Letters drawn by lot that stood
before "begotten of" were again called a name by both checkers, which is the reason a name is no longer laid.

**The map with this layer** ([map_layers.md](map_layers.md)): 4,185 of the 7,099 running words that need a
meaning are translated (59.0%, from 58.5%), 840 of 2,798 distinct spellings (30.0%, from 29.2%) and 160 of about
1,284 distinct words (12.5%, between 11.8% and 15.6%, from 12.3%). The 2 words of the dictionary that this layer
is the first to lay as translated words are `nbr` ("gold", by Rilly 2016) and `yiroẖe` ("to take control", our
wording, by Rilly 2021). Before the project the north star is the same: both meanings were published before it.

Cost: 6 agents, 565,589 tokens (typed from the task notifications into `data/sources/g8b/tokens.json`, local).

## 6. Reproduce

```
python3 -I src/leftover.py public        # needs the local files; writes leftover_parts_figures.json
python3 -I src/leftover.py layer-again   # the lines of the layer `leftover` (local)
python3 -I tests/test_leftover.py        # the method on made-up words; the figures and this page
```

`python3 -I src/leftover.py count-again` counts the answers again; the packs are not written again once they are
answered.
