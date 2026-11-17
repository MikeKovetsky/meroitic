# The leftover stems (the 86 places the leftover-parts step did not give to checkers)

Status on 2026-11-16: the step is counted and **every bar is met** (section 6): 23 of the 86 places are laid,
22 as names and 1 as a word of grammar. No stem was recognised as a word the lexicon knows. The 23 places are the
map's seventh layer, `leftover_stems`. Figures: `leftover_stems_figures.json`. Script: `src/leftover.py` (its
third part). Checks: `tests/test_leftover.py`. The step it follows is on [leftover_parts.md](leftover_parts.md)
and [leftover_parts_2.md](leftover_parts_2.md). What the checkers were given:
[`runs/prompts/G9_stems.md`](../../runs/prompts/G9_stems.md).

## 1. What was asked

The plan of the leftover parts named 182 places where "both checkers recognised the word, but the map leaves a
few letters of the spelling unnamed". Checkers were given 96 of them. At the other 86 the entry both checkers
recognised is an ending or a particle, and what the map leaves unnamed is the stem itself; the page said that
naming it "would be deciphering it". The review answered that a checker could still recognise such a stem as a
word the lexicon knows. Mike, 2026-11-16, asked "Should I give the 86 skipped leftover places to two
checkers?": "run it and document everything in our doc".

| | Requirement | State |
|---|---|---|
| R1 | "Give the 86 skipped leftover places to two checkers": "run it". | Set: sections 2 and 3. |
| R2 | "Document everything in our doc." | This page, and with the result the report, the README, the next steps and the index. |
| R3 | The rules of section G: two checkers a place, every bar committed before the checkers are started, counts from a figures file, nothing called a meaning of ours. | The bars are in this page, committed before any checker is started. |

## 2. The places and what a checker sees

- **The places:** the 86 places of [the rare spellings](rare_spellings.md) that both checkers called a form of
  an ending's or a particle's entry and that no layer of the map has laid (74 of G2, 12 of G4), on the map with
  its six layers.
- **What a checker sees, and the brief:** word for word those of the leftover parts: the place, five words on
  each side with the map's reading of each, the spelling's parts as the map cuts them, each named part with its
  entry, each unnamed part marked so. The five cases are the same (ending, known word, name, unknown, unclear),
  and the checker may search the lexicon.
- **Controls: 80 places of known answer,** 20 of each kind, mixed in and shown the same way:

| Kind | What is shown | The answer |
|---|---|---|
| A hidden stem | a translated word of one stem and endings, the stem (three letters or more) shown as unnamed | a known word, that entry |
| Hidden endings | such a word with its endings shown as unnamed | ending |
| A name | a name with endings, the name shown as unnamed: the 9 personal names with endings that the map holds, and 11 names the lexicon holds, by lot | name |
| Letters by lot | such a translated word with its stem's letters replaced by as many letters drawn by lot (three at least) and shown as unnamed | none of the three: no name stands there, and the letters are no word |

  Each kind takes 20 different entries of the lexicon, so that the two commonest words do not fill it.
- **The checkers:** two for each of 4 packs (166 places), each a fresh agent (Opus): 8. Seed 20261127.

## 3. The bars, set before any checker is started

For every verdict:

1. Every place of a pack is answered by both of its checkers.
2. Cohen's kappa of the two checkers over the five cases, on the real places, is 0.6 or more.

**Each verdict then stands on its own bars.** A verdict whose bars are missed is not laid; the others still are.

| Verdict | It is found (each checker, at least 14 of 20) | It is not said wrongly (each checker, at most 2 of 20) |
|---|---|---|
| A known word | the hidden stems, named with their entry | the letters by lot called a known word |
| Ending | the hidden endings called ending | the letters by lot called ending |
| A name | the names called a name | the letters by lot called a name; the hidden stems called a name |

If bar 1 or 2 is missed, nothing is taken, and the step stops until Mike has seen why.

**What a place then is:**

- **a translated word** when both checkers call the unnamed part a known word and name the same entry, which
  the lexicon calls established or probable, and the spelling has one unnamed part;
- **a name** when both call it a name and the spelling has one unnamed part;
- **a word of grammar** when both call every unnamed part an ending: the spelling is then endings or particles
  only;
- **open,** as it is, in every other case, and wherever another stem of the spelling has no meaning.

## 4. Why a name can be laid here, and was not in the second reading

The second reading of the leftover parts laid no name, because its only control for names was letters drawn by
lot put where a name stands, which any reader calls a name. That control could not tell a good judgment from a
bad one. Here the name has controls that can: real names that must be found, and two sorts of place where no
name stands (a known word in its own place, with its real letters or with letters by lot) where a name must not
be said. Step G3 laid names on bars of the same kind.

## 5. What the step cannot show

- A name is judged by its place in the text. The bars show how often that judgment calls a word a name; they
  cannot show that a given unnamed stem is one.
- A hidden stem with its real letters can be looked up, an unknown word cannot: the bar "it is found" is easier
  than the real places are.
- The checkers are one model: their agreement shows that a judgment can be repeated, not that it is right.
- No meaning found here is the project's own: a place laid as a translated word takes the meaning the lexicon
  gives the entry both checkers name.

## 6. The result (counted at 18:44, every bar met)

The eight checkers were started at 18:42, after the commit with the bars (18:42:24); their answers came between
18:43 and 18:44.

| Bar for every verdict | Result | |
|---|---|---|
| Every place answered by both | 166 of 166 (86 places, 80 controls) | met |
| Kappa of 0.6 or more on the real places | 0.79 | met |

| Verdict | Found (at least 14 of 20) | Said wrongly (at most 2 of 20) | |
|---|---|---|---|
| A known word | 18 and 15 hidden stems named with their entry | 0 and 0 runs of lot letters called a known word | met |
| Ending | 20 and 20 | 0 and 0 runs of lot letters called ending | met |
| A name | 18 and 18 | 0 and 0 runs of lot letters, and 0 and 0 hidden stems, called a name | met |

| Both checkers say, of the 86 places | Places |
|---|---|
| unknown | 55 |
| a name | 22 |
| ending | 1 |
| a known word | 0 |
| not agreed | 8 |

**What can be laid: 23 places,** 22 as names and 1 as a word of grammar (its unnamed part is an ending inside the
word for "begotten of"). No place is left out for a second unnamed part or for another stem without a meaning.

**What this shows.**

- **The review's question has its answer: no.** At none of the 86 places did the two checkers recognise the
  unnamed stem as a word the lexicon knows, though both found such stems where they were hidden (18 and 15 of
  20). What the map leaves unnamed there is unknown to the lexicon too.
- **A quarter of the places are names.** By the checkers' reasons most are names of places before the locative
  ending, and names of persons before the word for "this one". They leave the count of words that need a
  meaning; they do not add a translated word.
- **The judgment by place is not steady.** One spelling stands at five places of one text: the two checkers call
  it a name at two, differ at two, and call it unknown at one. Only the two agreed places are laid.

**The map with this layer** ([map_layers.md](map_layers.md)): 4,186 of the 7,077 running words that need a
meaning are translated (59.1%, from 59.0%), 841 of 2,781 distinct spellings (30.2%, from 30.0%) and 160 of about
1,283 distinct words (12.5%, between 11.8% and 15.6%, from 12.5%). The layer gives no word of the dictionary a
meaning, so the north star does not move: the 22 names leave the count of words that need a meaning, and 1 of
the stems the map could not name is now a name.

Cost: 8 agents, 725,765 tokens (typed from the task notifications into `data/sources/g9/tokens.json`, local).

## 7. Reproduce

```
python3 -I src/leftover.py packs-stems    # needs the local map, lexicon and layers; refuses once answers exist
python3 -I src/leftover.py count-stems    # the checkers compared, the bars of each verdict
python3 -I src/leftover.py layer-stems    # the lines of the map's seventh layer
python3 -I src/leftover.py public         # writes leftover_stems_figures.json (and the step's other figures file)
python3 -I tests/test_leftover.py         # the method on made-up words; the figures, this page, the local files
```

The packs, the key, the checkers' answers, the result and the layer's lines are local (`data/sources/g9/`): they
show the texts and quote the lexicon. The script writes the key, the packs and the result again as they were.

Review (2026-11-16): an independent reviewer (Opus 5.5, a fresh agent that saw the change and the task, not the
reasoning) checked the script, the checks and this page against the local files. It corrects two statements of
sections 2 and 3, which stand as they were written before the checkers were started:

1. "Each kind takes 20 different entries of the lexicon." The hidden stems, the hidden endings and the letters by
   lot were drawn so. The names were not: they are the 9 personal names the map holds and 11 places of 7 names of
   the lexicon, drawn by place, so that four names stand twice. Counted once each, the 16 names were found by each
   checker 14 and 14 times, which still meets the bar of 70%.
2. "A word of grammar when both call every unnamed part an ending: the spelling is then endings or particles
   only." At the one place laid so it is not: the map names there the stem of the verb "to beget" (`-erike-`),
   which the lexicon writes with hyphens and the script takes for an ending. The place is a form of the word for
   "begotten of" with the genitive, as section 6 says, and counts as translated either way; its line in the map
   reads "endings or particles only".

Neither changes a bar, a verdict or a count. The rules were in git before the checkers were started (the time of
the commit in git's own log of the branch, the 8 launches in the session's log, one for each pack and checker, and
the answer files), and the tokens of the 8 checkers are those of their task notifications.
