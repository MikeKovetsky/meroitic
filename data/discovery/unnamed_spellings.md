# The open spellings the lexicon does not hold (step G3)

Status on 2026-11-16, 14:03: the first pilot missed two of its bars and is not taken (section 6); a second pilot with
other places and corrected controls is set (section 7), and none of its checkers has answered yet. Working
script (local until the step is counted): `data/sources/g3/run.py`. What the checkers are given:
[`runs/prompts/G3_places.md`](../../runs/prompts/G3_places.md).

## 1. What was asked

Mike, 2026-11-16, to "Start G3's pilot and G5 now, while the review runs?": "Yes, both". The step, as section G of
[`NEXT_STEPS.md`](../../NEXT_STEPS.md) has it:

> **G3. The spellings that are not in the lexicon** (kind c: 1,225 running words, most of them standing once).
> [...] So first a pilot on 100 places drawn by a fixed seed: a script proposes the joins with the neighbouring
> words that give a form the map reads, two checkers decide (a piece, a name, a word of its own, unclear), and
> the bar is set beforehand. A name or a piece of a name needs no meaning; a piece of a word the map reads takes
> that word's. This step deciphers nothing: it corrects the count of what is left to decipher.

| | Requirement | State |
|---|---|---|
| R1 | "a pilot on 100 places drawn by a fixed seed" | Set: section 3. |
| R2 | "a script proposes the joins with the neighbouring words that give a form the map reads" | Counted before the pilot and found empty: section 2. The checkers name the whole word themselves. |
| R3 | "two checkers decide (a piece, a name, a word of its own, unclear), and the bar is set beforehand" | Set: sections 3 and 4. |

## 2. The places, and what a script can do

On the map with its three layers, 1,107 spellings that stand in one or two texts have no accepted meaning and
hang on no entry of the lexicon. They stand at 1,225 open places.

The step planned to let a script propose joins. Counted first: joining such a spelling with the word before it,
the word after it, or both gives a spelling the map holds as translated or named at 11 of these places. A script
can therefore propose next to nothing. The checkers decide from the place itself and, for a piece, name the whole
word.

## 3. The pilot

- **The places:** 100 of the 1,225, drawn by a fixed seed (20261116).
- **What a checker sees for each place:** the text's number, kind and site; the word and five words on each side;
  the map's reading of each of those words. The word to judge is shown as a word the map knows nothing of, also
  where an analyst had made a guess, so that no guess leads the checker.
- **The four cases:** a name; a piece of a longer word or name whose other part stands beside it (the checker
  names the whole); a word of its own; unclear. The checker opens no file and looks nothing up.
- **Controls:** 50 places whose answer the map holds, mixed among the real ones and shown the same way:
  20 translated words (the answer: a word of its own), 15 names that the analysts recognised and that are no
  entry of the lexicon (a name), and 15 translated or named spellings of six letters or more that the script cuts
  in two at a place drawn by lot (a piece of that spelling). The words are taken from the texts of the real places
  where there are enough.
- **The checkers:** two for each of 3 packs of 50 places, each a fresh agent (Opus).

## 4. The bars, set before any checker is started

1. Every place of a pack is answered by both of its checkers.
2. Cohen's kappa of the two checkers over the four cases, on the real places, is 0.6 or more.
3. Each checker calls at most 10% of the control words a name or a piece (2 of 20 in the pilot).
4. Each checker calls at least 70% of the control names a name (11 of 15), and gives at least 70% of the cut
   spellings as a piece of the right whole (11 of 15).
5. If a bar is missed, nothing is taken: the brief is corrected and fresh checkers read the same packs once. If it
   is missed again, the step stops and is reported as not done this way.

**If the pilot meets its bars,** the other places go to two checkers a pack with the same brief, with controls
that make up a tenth of the places (two thirds of them words, the rest names and cuts in equal parts), under the
same bars. The pilot's places are not judged again.

**What a place then is** (the pilot lays nothing in the map; the full pass does):

- a **name** only when both checkers say so: it is laid as a name, which needs no meaning;
- a **piece** only when both say so and name the same whole word: it is laid only where the map holds that whole
  word as translated or named, and takes its level; a piece of a word the map does not hold stays open and is
  counted apart;
- a **word of its own** or **unclear** only when both say so; every other place is **not agreed**. These stay open.

The count of distinct words (the north star) rests on a sample of the stems the map cannot name. If this step
makes more than 2% of those stems names or pieces, the script of the map stops, and a new estimate is made by a
rule written down before it is counted.

## 5. What the pilot cannot show

- The controls are easier than the real places: a translated word is a common word, and the names the analysts
  recognised stand where the formulae put a name. A checker who passes the controls can still be wrong on a rare
  word in a broken text.
- The checkers are one model: their agreement shows that a judgment can be repeated, not that it is right; they
  see five words on each side, not the stone.
- A name found here is a name by its place in the text, not by a source.

## 6. The first pilot: not taken

Six checkers answered all 150 places. On the 100 real places their kappa is 0.85 (bar 0.6). On the controls:

| Control | Bar | First checker | Second checker |
|---|---|---|---|
| Translated words called a name or a piece | at most 2 of 20 | 3 | 3 |
| Names called a name | at least 11 of 15 | 12 | 13 |
| Cut spellings given as a piece of the right whole | at least 11 of 15 | 9 | 9 |

Two bars are missed, so nothing is taken from the pilot. What the checkers said of the real places is given for
the record only: 61 a word of its own, 15 a name, 15 unclear, 1 a piece, 8 not agreed.

Why the bars were missed, from the answers:

- **The cut spellings.** Where the script cut a word of a known formula, the checkers named the whole. Where it
  cut a word in a running text (six of the fifteen), both saw "nothing that marks a cut", and nothing does: two
  unknown halves side by side look like two unknown words. A cut of a word the map holds is found by joining the
  letters, which is a script's work, not a judgment from context.
- **The translated words.** Two of the three that both checkers called a piece are an ending or a particle written
  apart (`qowi` after a name, `lowi` after `terike`). By the project's own rule for counting words such a word is
  a piece, so the control's answer was wrong, not the checkers. The third (`mloye` in a list of relatives) both
  called a name.

By rule 5 the brief would now be corrected and the same packs read again. That is not done: the fault lies in the
controls, which a new brief does not change, and the same packs would miss the same bars. The step as first
designed stops here.

## 7. The second pilot (rules set on 2026-11-16 at 14:03, before any of its checkers is started)

What changes, and why:

- **Other places:** 100 places drawn by a fixed seed from those the first pilot did not use.
- **The script does the joins,** as the step first said: where joining the word with a word beside it gives a
  spelling the map holds as translated or named, the pack says so in a note under the place. The checker still
  decides whether the place fits.
- **Controls with a sure answer:** 20 translated words built on a stem of the lexicon that is no function word (a
  word of its own); 15 names the analysts recognised that are no entry of the lexicon (a name); 15 endings or
  particles written as a word of their own (a piece of the word beside them). No cut spellings.
- **The bars guard what will be laid.** A name is the only verdict that changes the map on a checker's judgment
  alone, so the bar on the control words is on names.

The bars:

1. Every place of a pack is answered by both of its checkers.
2. Cohen's kappa of the two checkers over the four cases, on the real places, is 0.6 or more.
3. Each checker calls at most 10% of the control words a name (2 of 20).
4. Each checker calls at least 70% of the control names a name (11 of 15).
5. What the checkers say of the 15 particles is reported and is under no bar.
6. If a bar is missed, nothing is taken, and the step stops until Mike has seen why.

**If the second pilot meets its bars,** the other places go to two checkers a pack with the same brief and notes,
with controls that make up a tenth of the places (two thirds words, one third names), under bars 1 to 4. What a
place then is, and what is laid, stays as section 4 has it: a name only when both checkers say so; a piece only
when both name the same whole and the map holds that whole as translated or named.

The brief is that of the first pilot with one bullet added on the script's note
([`runs/prompts/G3_places.md`](../../runs/prompts/G3_places.md)).
