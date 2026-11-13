# A second scholar for every meaning: the first pass of F2

**Of the 10,290 running words of the clean corpus, 5,419 (52.7%) are translated by one lexicon, Rilly's of 2003;
3,873 (37.6%) rest only on meanings that a second scholar gives too.** Names and numbers count in both figures.
Of the 3,676 words the map translates as a meaning or a grammar word, 2,130 (57.9%) are built only on entries that
a second scholar reads the same way. This is the second figure that step 23 of [`NEXT_STEPS.md`](../../NEXT_STEPS.md)
(F2) asked for; the first figure is the map's ([`corpus_v6_readers.json`](corpus_v6_readers.json)).

Counted on 12 November 2026 by [`src/lexicon.py`](../../src/lexicon.py); figures in
[`lexicon_figures.json`](lexicon_figures.json), and every entry with its status in
[`lexicon_statuses.tsv`](lexicon_statuses.tsv) (headwords, statuses and the scholars cited; no meaning, since the
meanings are Rilly's and in copyright).

## 1. What was asked

"Translated" in the map means that one lexicon accepts the meaning. The check against two printed editions
([`experts.md`](experts.md)) found that two other scholars agree for most words and differ on a few. F2 asks the
same of every entry the map leans on: does a second scholar give the same meaning?

## 2. The entries and the evidence

The map of the clean corpus with the analysts' answers uses 594 entries of the lexicon; 177 of them stand behind
the words it translates as a meaning or a grammar word. Two kinds of evidence of a second scholar were already in
hand:

1. **The proposals the lexicon records.** For most entries Rilly's lexicon says what other scholars proposed
   (Griffith, Hofmann, Hintze, Millet, Priese and others): 131 of the 177 entries have at least one such proposal.
2. **The editors' readings.** The check against Millet 2005 and FHN III has the editors' verdict on words built on
   101 of the 177 entries.

## 3. The judges

Every proposal on an entry that Rilly states (established or probable) went to two judges, beside the lexicon's
meaning and without the scholar's name: 407 proposals. They said "same", "partly", "other" or "no meaning". Each
judge saw 41 decoys on lines of their own: another entry's meaning in place of the proposal, from outside the
line's field of meaning.

| | Bar, set before the judges answered | Result |
|---|---|---|
| Agreement of the two judges on "same or not" (kappa) | 0.6 or more | 0.92 |
| Decoys called "same" or "partly", first judge | at most 10% | 2 of 41 |
| Decoys called "same" or "partly", second judge | at most 10% | 0 of 41 |

On the 325 lines both judges saw with the real proposal, they gave the same verdict on 303 (kappa 0.91 on the four
verdicts). Both bars are met.

## 4. The statuses

The rules were committed before the judges answered. An entry Rilly states is "agreed by two scholars" when a
proposal is called "same" by both judges or an editor reads a word built on it the same way; "disputed" when it is
not agreed and a proposal is called "other" by both, or an editor reads it otherwise; "stated by one" otherwise. An
entry Rilly gives only as a hypothesis, or without a meaning, is "proposed".

| Status | Entries | Uses in translated words |
|---|---|---|
| agreed by two scholars | 70 | 3,114 |
| disputed | 23 | 504 |
| stated by one | 59 | 587 |
| proposed | 25 | 635 |

1. **Agreed:** 22 entries by both the judges and the editors, 23 by the judges alone, 25 by the editors alone. 26
   of the 70 also have a dissent: a proposal both judges call "other", or an editor who reads a word otherwise.
   `yetmde` is one: agreed through the editors' reading of 6 words, while they read 49 others only partly the
   same, and three scholars proposed a social bond rather than kinship.
2. **Disputed:** `qo` (123 uses), `l` "to give" (117), `mlo` (113) and `mte` (34) lead; `qo` and `mte` were
   already the differences of the check against the editions.
3. **Proposed:** pieces of the benediction formulas and endings the map leans on without an accepted meaning:
   `-wi` (273 uses), `ps-` (149), `-te` (66), `-kete` (45). A word built on one of them is translated by the
   map and not agreed.

## 5. Limits

1. **The proposals reach us through Rilly.** His lexicon records who proposed what; that record is the source,
   not the scholars' own texts. Section 6 checks a sample of it.
2. **A decoyed line has one real verdict.** The rule asks for both judges, so the 82 lines that carried a decoy
   for one judge cannot count. Had each kept its one real verdict, 11 entries would change status and the second
   figure would be 4,103 (39.9%), not 3,873.
3. **"Agreed" is the agreement of two scholars, not proof.** The scholars read the same few texts and often
   followed one another. And one editor's "agree" on one word is enough under the rule, however many other words
   the editor reads only partly the same (`yetmde`, item 1 of section 4). One entry, `-o` (246 uses), is agreed
   only through a view the lexicon records without a scholar's name.
4. **Some meanings are only a kind.** 21 of the 177 entries are titles or epithets whose meaning in the lexicon
   is "a priestly title" or the like; agreement on them is agreement on the kind.
5. **Not done yet:** the meanings worded anew, so that the table can carry them under CC BY. The table holds the
   headwords, the statuses and the scholars cited.

## 6. The check of the record against Griffith's own words

A sample of 20 of the proposals the lexicon gives to Griffith, drawn from those that cite a text of his we hold
(Karanòg, 1911; the Meroitic Studies, 1916-17), went to a reader with Griffith's own text. Bars, set before it was
read: found for 10 or more, and as stated for 90% or more of those found.

| As stated | Otherwise | Not found |
|---|---|---|
| 15 | 0 | 5 |

Both bars are met: 15 found, all as the lexicon states them. The 5 not found are a remark on two forms of `wi`, a
reading the scan's text layer garbles, a Coptic comparison from Griffith's later work, a remark that a woman could
hold an office, and a reading in his edition of Faras, which we do not hold. On 4 of the 15 the evidence is weaker:
for `yetmde` Griffith has "kinsman" and "related to" but not "cousin", and three rest on words the text layer
garbles. The record is faithful where it can be checked; this sample cannot speak for the other scholars.

## Reproduce

```
python3 -I src/lexicon.py layout     # needs data/rilly2003/ and the local gloss file of the clean corpus
python3 -I src/lexicon.py packs      # refuses once a judge has answered
python3 -I src/lexicon.py check      # the sample given to Griffith; refuses once answered
python3 -I src/lexicon.py public
python3 -I tests/test_lexicon.py
```

**Cost,** from the task notifications, by hand: four judges' packs 388,896 subagent tokens (99,371 and 101,866 for
the first judge, 98,363 and 89,296 for the second), about five minutes each; the check against Griffith's text
250,976, about ten minutes.
