# The leftover stems (the 86 places the leftover-parts step did not give to checkers)

Status on 2026-11-16, 18:42: the places, the controls and the bars are set; no checker has been started. Working
script (local until the step is counted): `data/sources/g9/run.py`. The step it follows is on
[leftover_parts.md](leftover_parts.md) and [leftover_parts_2.md](leftover_parts_2.md). What the checkers are
given: [`runs/prompts/G9_stems.md`](../../runs/prompts/G9_stems.md).

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
