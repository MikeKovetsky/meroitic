# The leftover parts, and the meanings Millet and Lipiński state (a follow-up to G2 and G4)

Status on 2026-11-16: both parts are counted. **The first reading of part 1 is not taken:** one bar was missed
by one answer (section 6), so no place of it is laid. **The second reading of part 1 met its bars**
([leftover_parts_2.md](leftover_parts_2.md)) and is the map's sixth layer, `leftover`: 32 places, 27 of them
translated words and 5 names. **Part 2 met its bars** (section 7) and is the map's fifth layer, `rare_millet`:
17 places, 13 of them names and 4 translated words. **The step in all:** 49 places are laid, 31 of them as
translated words and 18 as names, and 4 words of the dictionary get a meaning, each from one scholar; it took 20
agents and 1,854,110 tokens. Figures: `leftover_parts_figures.json`. Script: `src/leftover.py`. Checks:
`tests/test_leftover.py`. What the checkers of part 1 were given:
[`runs/prompts/G8_parts.md`](../../runs/prompts/G8_parts.md).

## 1. What was asked

Mike, 2026-11-16, to "Start the leftover-parts step and G6 once G3 and G5 are pushed?": "Yes, both". The step as it
was put to him:

> **The leftover parts (small, sure).** At 182 places both checkers recognised the word, but the map leaves a few
> letters of the spelling unnamed, so the place stayed open. Two checkers name those leftover parts. This can add
> up to about 2.5 points of running words. The first review also found that Millet 2005 firmly states a meaning
> for 8 entries that G4 skipped because it only counted Rilly; those go in the same step.

Two of those numbers were wrong, and are corrected here before anything is counted:

- **96 places, not 182.** At the other 86 the entry is an ending or a particle, and the unnamed part is the stem
  itself: naming it would be deciphering it. So the most this part can add is 96 running words, about 1.3 points.
- **15 entries, not 8.** For 13 entries of G4 without a meaning from Rilly's later work, Millet 2005 states one with
  the stance "accepts" or "probable", and Lipiński 2011 for 2 more. They stand at 56 places.

| | Requirement | State |
|---|---|---|
| R1 | "Two checkers name those leftover parts." | Set: sections 2 and 3. |
| R2 | The meanings Millet 2005 states firmly for entries that G4 skipped "go in the same step". | Set: section 4. |
| R3 | The rules of section G: two readers a place, each bar committed before its readers are started, counts from a figures file, nothing called a meaning of ours. | The bars are in this page, committed before any agent of the step is started. |

## 2. Part 1: the places and what a checker sees

- **The places:** the 96 places of [the rare spellings](rare_spellings.md) that both checkers called a form of a
  stem's entry and that were not laid, because the map leaves a part of the spelling unnamed (68 of G2, 28 of
  G4; at one of them the reason is another stem without a meaning).
- **What a checker sees:** the place as in step G3 (the word, five words on each side, the map's reading of each),
  and the spelling's parts as the map cuts them: each named part with its entry of the lexicon, each unnamed part
  marked so. The checker may search the lexicon for the unnamed part.
- **The five cases** for the unnamed part: nothing but endings, prefixes or particles, or letters of a variant
  writing ("ending"); another word the lexicon holds with a sure meaning ("known", with its headword); a name;
  a word or letters nothing explains ("unknown"); unclear.
- **Controls:** 40 places of known answer, mixed in and shown the same way: 20 translated words of one stem and
  endings, with the endings shown as unnamed (the answer: ending), and 20 translated words with three to five
  letters drawn by lot put before or after them as an unnamed part (the answer: unknown). The second kind is
  there because almost any run of letters can be cut into one-letter endings of the lexicon.
- **The checkers:** two for each of 3 packs, each a fresh agent (Opus).

## 3. Part 1: the bars, set before any checker is started

1. Every place of a pack is answered by both of its checkers.
2. Cohen's kappa of the two checkers over the five cases, on the real places, is 0.6 or more.
3. Each checker explains (as an ending, a known word or a name) at most 10% of the letters drawn by lot (2 of 20).
4. Each checker calls at least 70% of the hidden endings an ending (14 of 20).
5. If a bar is missed, nothing is taken, and the step stops until Mike has seen why.

**What a place then is:**

- **laid** when both checkers call the unnamed part an ending; or both call it a known word and name the same
  entry, which the lexicon calls established or probable; or both call it a name. Nothing in the spelling is then
  without a meaning. The place takes the level of its entry, as in the rare spellings (a name where the entry is
  one);
- **open,** as it is, in every other case.

For the north star the rule of the rare spellings holds: an entry of G4 counts as a word of the dictionary given
a meaning once one of its places is laid as a translated word.

## 4. Part 2: the entries for which Millet 2005 or Lipiński 2011 states a meaning

The rule of G4 again, with the source changed:

- **The entries:** the 15 entries of G4 that did not pass the bar of class A and for which the literature pass
  found a statement of Millet 2005 or of Lipiński 2011 with the stance "accepts" or "probable" (each quote found
  in its file by script).
- **Read twice.** Two readers, each on its own, read the statements of each entry in their place. An entry counts
  as stated by a later source only when both give the stance "accepts" or "probable" for the same source and
  their meanings share a content word.
- **The place pass.** Every place of these entries goes to two checkers with the four cases and the bar of G4
  (section 3 of [rare_spellings.md](rare_spellings.md)): a kappa of 0.6 or more, every place answered by both.
- **What is laid:** as in G4. A stated place only where the map names every part of the spelling and every stem
  among them has a meaning; an entry that is a name by the lexicon is laid as a name; a piece only where the
  whole word both checkers name is translated or named in the map.

These meanings rest on one scholar each, like those of G4.

**Added on 2026-11-16 at 15:35, before any reader of part 2 was started.** Looking at the 15 entries showed what
the rule above did not foresee: by Millet's reading most of them are names, three of them names of persons that
the lexicon does not file as names, and one statement renders a title with a Meroitic word left as it is. Counted
by the rule of G4 alone, such places would have come out as translated words. So:

- **Each reader also says what the statement gives:** a name (of a person, a place, a people or a god), a meaning
  in full, or a meaning that leaves a Meroitic word as it is.
- **A translated word** only when both readers say the source gives a meaning in full.
- **A name** when the lexicon calls the entry a name, or both readers say the source states a name.
- **Open, as it is,** in every other case: the meaning leaves a Meroitic word as it is, or the readers differ on
  what is given.
- **The source** both readers name must be Millet 2005 or Lipiński 2011; a statement of another source does not
  count here.
- **The place checkers' briefs name the number of lines** their pack expects, as in the second reading of G4.

The addition can only lower the count of translated words.

## 5. What the step cannot show

- The controls of part 1 are made by a script: letters drawn by lot are easier to see through than a real unknown
  word joined to a known one.
- The checkers are one model: their agreement shows that a judgment can be repeated, not that it is right.
- No meaning found here is the project's own.

## 6. Part 1: the result (counted at 15:30, nothing taken)

Six checkers (two for each of 3 packs) were started at 15:27, after the commit that set the bars (15:23:46); the
last answer came at 15:29.

| Bar | Result | |
|---|---|---|
| Every place answered by both | 136 of 136 (96 places, 40 controls) | met |
| Kappa of 0.6 or more on the real places | 0.77 | met |
| Each checker calls at least 14 of 20 hidden endings an ending | 20 and 20 | met |
| Each checker explains at most 2 of 20 runs of letters drawn by lot | **3** and 2 | **missed by one** |

By rule 5 of section 3 nothing is taken: no place of this reading is laid in the map.

**Why the bar was missed.** All five explanations were "a name"; neither checker called a run of lot letters an
ending or a known word. The five answers stand at three places: the letters had been put before `qo` ("this
one") once and before the word for "born of" twice, which is where a name stands in an epitaph. Both checkers
called the two before "born of" the mother's name; one called the one before `qo` the name of the dead. At the
other 17 places, where no name is expected, both said "unknown" every time.

**What the checkers said of the 96 real places** (not taken; given so that the miss can be judged):

| Both say | Places |
|---|---|
| ending | 40 |
| unknown | 28 |
| a name | 12 |
| a known word, the same entry | 1 |
| unclear | 1 |
| not agreed | 14 |

**What this shows, and what it does not.**

- The control did its work: it shows that "a name" is said of any letters that stand where a name is expected.
  The 12 places both checkers call a name rest on that same judgment, so they cannot be laid on this reading.
- The verdict "ending" came through its own two controls without a miss (40 of 40 hidden endings found, 0 of 40
  runs of lot letters called an ending). The bar, though, was set on all three explanations together, and a bar
  is not cut to fit after the count: the 40 places stay open on this reading.
- A second reading, with a bar set beforehand for each verdict and fresh checkers, is on its own page
  ([leftover_parts_2.md](leftover_parts_2.md)). It met its bars and lays 32 places.

Cost: 6 agents, 595,672 tokens (typed from the task notifications into `data/sources/g8/tokens.json`, local).

## 7. Part 2: the result (counted at 15:40, bars met)

**The statements, read twice.** Four readers (two for each of 2 packs) were started at 15:35, after the commit
with the added rule (15:35:28); their answers came between 15:36 and 15:37.

| Of the 15 entries | Entries |
|---|---|
| Stated by Millet 2005 or Lipiński 2011, by both readers | 12 |
| Not stated firmly by both | 3 |

| What the source gives, for the 12, by both readers | Entries |
|---|---|
| A name (five places, two persons) | 7 |
| A meaning that leaves a Meroitic word as it is | 3 |
| A meaning in full | 2 |

The two meanings in full are both from Lipiński 2011: "child" for `mse`, and "women who have not borne a child"
(our wording) for `kdimdḫe`. By the readers' notes Lipiński takes the first from a work of Rilly of 2010 and the
second from Millet. The lexicon of 2003 files `mse` as a title, with a question mark.

**The places.** Four checkers (two for each of 2 packs) were started at 15:38; their answers came between 15:39
and 15:40.

| Bar | Result | |
|---|---|---|
| Every place answered by both | 56 of 56 | met |
| Kappa of 0.6 or more | 0.97 | met |

| Both checkers say | Places |
|---|---|
| the word the source speaks of ("stated") | 24 |
| open | 20 |
| a piece of another word | 8 |
| unclear | 3 |
| not agreed | 1 |

**What can be laid: 17 places.**

| | Places |
|---|---|
| A name, of an entry the lexicon files as a place name | 10 |
| A name, of an entry both readers say the source calls a personal name | 2 |
| A piece of a word the map holds as a name | 1 |
| A translated word (`mse` three times in one text, `kdimdḫe` once) | 4 |

**What stays open:** 5 stated places where the map leaves a part of the spelling unnamed, 3 where the meaning
leaves a Meroitic word as it is, and 7 pieces whose whole word the map does not hold or holds open.

The gain is small, as the entries foretold: 4 running words and 2 words of the dictionary get a meaning, each
from one scholar, and 13 places leave the count of words that need one.

**The map with this layer** ([map_layers.md](map_layers.md)): 4,158 of the 7,104 running words that need a
meaning are translated (58.5%, from 58.4%), 817 of 2,802 distinct spellings (29.2%, from 29.0%) and 158 of about
1,284 distinct words (12.3%, between 11.7% and 15.4%, from 12.1%). Before the project the north star is the same:
both meanings were published before it.

Cost: 8 agents, 692,849 tokens (4 readers 368,724; 4 checkers 324,125).

## 8. Reproduce

```
python3 -I src/leftover.py public   # needs the local files; writes leftover_parts_figures.json
python3 -I src/leftover.py layer    # the lines of the layer `rare_millet` (local)
python3 -I tests/test_leftover.py   # the method on made-up words; the figures and both pages
```

`python3 -I src/leftover.py count`, `count-again`, `verify` and `places` count the answers again; the packs are
not written again once they are answered.
