# A second scholar for every meaning (F2)

**Of the 10,290 running words of the clean corpus, 5,419 (52.7%) are translated by one lexicon, Rilly's of 2003;
4,105 (39.9%) are names, numbers or words built only on entries that a second scholar reads the same way.** Names
and numbers count in both figures. Of the 3,676 words the map translates as a meaning or a grammar word, 2,362
(64.3%) are built only on such entries. Every one of the 594 entries the map uses has a status: 114 are agreed
by two scholars, 26 disputed, 94 stated by one and 360 only proposed (sections 4 and 5). This is the second figure
that step 23 of [`NEXT_STEPS.md`](../../NEXT_STEPS.md) (F2) asked for; the first figure is the map's
([`corpus_v6_readers.json`](corpus_v6_readers.json)). It stands on three rounds of judges (section 3); with the
first round alone it was 3,875 (37.7%). The review of the first round corrected two things after the judges had
answered (section 9): as first counted, the second figure was 3,873 (37.6%). Held to a stricter rule for the
editors' readings it would be 3,715 (36.1%) (section 6, item 4).

Counted on 12 November 2026 by [`src/lexicon.py`](../../src/lexicon.py) and
[`src/lexicon_refs.py`](../../src/lexicon_refs.py); figures in [`lexicon_figures.json`](lexicon_figures.json).
Every entry behind a translated word is in [`lexicon_statuses.tsv`](lexicon_statuses.tsv) (headwords, their
meaning in words of our own, statuses, the scholars cited and the editors' verdicts counted, spellings and pages),
and every other entry the map uses in [`lexicon_other_statuses.tsv`](lexicon_other_statuses.tsv) (the same, with
what Rilly gives for it and without a meaning in our words). The lexicon's own wording, which is in copyright, is
never copied (section 10).

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
2. **The editors' readings.** The check against Millet 2005 and FHN III judged words built on 97 of the 177
   entries; on 66 of them the editors give such a word a meaning, on the others they are silent or lack the word.
   The words that check found the map misreading (the numeral 1 typed as the letter `l`, names or pieces of words
   read as words) are left out: they are not built on the entry the map named (section 9).

The other 417 entries stand behind names, or behind words the map does not translate. Rilly states 77 of them as a
name, a meaning or a grammar word; 49 of these have a proposal of another scholar, and the editors read words built
on 23. The other 340 he gives as a hypothesis, by their kind only, or without a meaning.

## 3. The judges

Every proposal on an entry that Rilly states (established or probable) as a meaning or a grammar word went to two
judges, beside the lexicon's meaning and without the scholar's name: 407 proposals. They said "same", "partly",
"other" or "no meaning". Each judge saw 41 decoys on lines of their own: another entry's meaning in place of the
proposal, from outside the line's field of meaning. The proposals on names were not sent in rounds one and two: a
word that is a name counts in both figures. Round three sent them.

| | Bar, set before the judges answered | Result |
|---|---|---|
| Agreement of the two judges on "same or not" (kappa) | 0.6 or more | 0.92 |
| Decoys called "same" or "partly", first judge | at most 10% | 2 of 41 |
| Decoys called "same" or "partly", second judge | at most 10% | 0 of 41 |

On the 325 lines both judges saw with the real proposal, they gave the same verdict on 303 (kappa 0.91 on the four
verdicts). Both bars are met.

**Round two.** Under the rule a line counts when both judges read its real proposal, so the 82 lines that carried
a decoy for one judge could not count after round one. In round two that judge read them with the real proposal,
beside 4 decoys of its own on lines it had already read with the real one. Every proposal now has two real
verdicts: on all 407 lines the judges gave the same verdict on 373 (kappa 0.89 on the four verdicts, 0.90 on
"same or not"). The first judge called its 4 decoys "other"; the second called 3 "other" and 1 "partly": "wife"
beside the lexicon's "woman", two words of one field that the list of fields (kin, rank, gods) does not hold. The
verdict is fair, but by the letter of the bar (at most a tenth) round two's decoys fail it; 4 decoys a judge are
too few to weigh much, and the judges' attention rests on round one's 82.

**Round three.** Every proposal on an entry Rilly states that rounds one and two did not send went to two judges in
one round: 109 on the other entries and 25 on the names inside translated words (`Wos`, `Mnp`, `Asori`, `Npte`).
Each judge read all 134 real lines, so that every proposal has two real verdicts, and 20 lines more, each with a
decoy: the headword and meaning of a real line beside the text of a real proposal on another entry, one that both
judges of rounds one and two had read as its own entry's meaning, far from the line's meaning (a field for persons
added, after round two's "wife"). Every line had a new number, so a decoy line looked like any other. Round three's
proposals seldom quote a bare meaning, so the quoted meanings of rounds one and two would have stood out. The judges
read round one's instructions, told that a word may be a name.

| | Bar, set before the judges answered | Result |
|---|---|---|
| Agreement of the two judges on "same or not" (kappa), round three | 0.6 or more | 0.90 |
| Decoys called "same" or "partly", first judge, round three | at most 10% | 0 of 20 |
| Decoys called "same" or "partly", second judge, round three | at most 10% | 0 of 20 |

On the 134 real lines the judges gave the same verdict on 124 (kappa 0.89 on the four verdicts). Both bars are
met: each judge called all its decoys "other".

## 4. The statuses

The rules were committed before the judges of each round answered. An entry Rilly states is "agreed by two
scholars" when a proposal is called "same" by both judges or an editor reads a word built on it the same way;
"disputed" when it is not agreed and a proposal is called "other" by both, or an editor reads it otherwise; "stated
by one" otherwise. An entry Rilly gives only as a hypothesis, or without a meaning, is "proposed".

| Status | Entries | Uses in translated words |
|---|---|---|
| agreed by two scholars | 84 | 3,383 |
| disputed | 22 | 384 |
| stated by one | 51 | 445 |
| proposed | 20 | 628 |

1. **Agreed:** 22 entries by both the judges and the editors, 33 by the judges alone, 29 by the editors alone. 27
   of the 84 also have a dissent: a proposal both judges call "other", or an editor who reads a word otherwise.
   `yetmde` is one: agreed through the editors' reading of 6 words, while they read 49 others only partly the
   same, and 4 scholars proposed a social bond rather than kinship.
2. **Disputed:** `qo` (123 uses), `mlo` (113), `mte` (34) and `-so` (19) lead; `qo` and `mte` were already
   differences of the check against the editions. `mlo` is disputed through a remark of Griffith's that both judges
   read as another meaning, a comparison with the Egyptian epithet "justified"; both editions read it as the
   lexicon does (section 6, item 5).
3. **Proposed:** pieces of the benediction formulas and endings the map leans on without an accepted meaning:
   `-wi` (273 uses), `ps-` (149), `-te` (66), `-kete` (45). A word built on one of them is translated by the
   map and not agreed.
4. **Round three** made one of the 177 agreed: the god `Mnp` (2 uses), whose meaning two of its proposals give as
   the lexicon does and one otherwise. With rounds one and two alone it was stated by one; the second figure does
   not move.

## 5. The other entries

Round three gives each of the 417 other entries the map uses a status, by the same rules.

| Status | Entries | Uses |
|---|---|---|
| agreed by two scholars | 30 | 201 |
| disputed | 4 | 28 |
| stated by one | 43 | 202 |
| proposed | 340 | 1,803 |

1. **Proposed:** the entries Rilly gives as a hypothesis (134), by their kind only (182) or without a meaning (24),
   among them the verbs of the benedictions `ḫr` (151 uses) and `ẖol` (104) and the title `pqr` (40). The editors
   read words built on 18 of them as the lexicon does (`ḫr`, `pqr`, `Akine`): a second scholar for a hypothesis,
   which the rule leaves proposed.
2. **Agreed:** 30, nearly all names: 15 by the judges alone, 9 by the editors alone, 6 by both; 11 of them also
   have a dissent. Horus (`Ar`, 31 uses), Philae (`Pilqe`, 20), Sedeinga (`Atiye`, 18) and Faras (`Pẖrse`, 16)
   lead.
3. **Disputed:** `Tebwe` (12 uses), the Abaton for the lexicon, Thebes for Török and in the editors' readings;
   `Nlote` (8), `yeto` (7) and `Brebri` (1).
4. **Stated by one:** 43, nearly all names, for which the record holds no second statement of the meaning or the
   judges found none the same. Amun (`Amni`, 45 uses) is one: its proposals are about its form, and no edition of
   the check reads it. FHN IV's index gives the name as Amûn, but the rules do not use FHN IV (section 7).
5. Without round three, 15 of the 417 would be agreed, 2 disputed and 60 stated by one.

## 6. Limits

1. **The proposals reach us through Rilly.** His lexicon records who proposed what; that record is the source,
   not the scholars' own texts. Section 8 checks a sample of it.
2. **Round two closed the gap of the decoyed lines.** The rule asks for both judges, so the 82 lines that carried
   a decoy for one judge could not count after round one (section 3). With round one alone, 12 entries had
   another status and the second figure was 3,875 (37.7%).
3. **An ending the lookup leaves unnamed is not checked.** The map's lookup cuts some known endings off a word
   without naming their entry; the rule leaves such a part out, as the map does, so only the rest of the word is
   checked. 432 of the 2,362 words carry one, and for 91 of them no agreed ending or function word is spelled like
   it (`-li`, `-leb` and `-lebkwi` lead). Held to those, the second figure would be 4,014 (39.0%).
4. **"Agreed" is the agreement of two scholars, not proof.** The scholars read the same few texts and often
   followed one another. And one editor's "agree" on one word is enough under the rule, however many other words
   the editor reads only partly the same (`yetmde`, item 1 of section 4). Held to a stricter rule, under which the
   editors must read at least two words built on an entry the same way, and more of them the same than partly or
   otherwise, 72 of the 177 would be agreed (12 entries change) and the second figure would be 3,715 (36.1%).
   One entry, `-o` (246 uses), is agreed only through a view the lexicon records without a scholar's name.
5. **The editors were shown the map's reading, not the lexicon's.** Their verdicts compare an edition with the
   map's short gloss of a word. Where that gloss gives only the kind of word, an edition that reads the lexicon's
   meaning counts as "new" there, not as "agree", and makes no entry agreed: `mlo` was "adjective" in that check
   (its section 4), and both editions read "good".
6. **An agreement can rest on a piece of a word.** The rule counts an editor's "agree" on any word built on the
   entry, also on one that the map or the editor reads as a piece of another word. `-lowi` and `-to` are agreed
   only so: the map read `elowi` as the end of `terikelowi` written apart, and the editor read `to` as a part of
   `peseto`. Without such agreements the second figure would be 4,057 (39.4%).
7. **Some meanings are only a kind.** 21 of the 177 entries are titles or epithets whose meaning in the lexicon
   is "a priestly title" or the like; agreement on them is agreement on the kind.
8. **Round three's decoys are another kind** than those of rounds one and two: real proposals of other entries,
   not quoted meanings, under new numbers like the real lines. They are not quite like them: each quotes a gloss,
   which most of round three's real lines do not. None was accepted; the two rates are not one measure.
9. **Not done yet:** a meaning in our words for the 417 other entries (their table gives none); the pages of most
   scholars' statements (section 7); and FHN IV's glosses as the statement of a second scholar.

## 7. Spellings and pages

Both tables give each entry's spellings, and the pages of the statements on its meaning where the sources in hand
give them ([`src/lexicon_refs.py`](../../src/lexicon_refs.py)).

1. **Spellings:** the headword as Rilly spells it, then the variants he lists, for every entry; 176 entries have
   variants. Beside them, the pieces of the corpus that both checkers of step 21 confirmed as a spelling or form of
   a word ([`variants_confirmed.tsv`](variants_confirmed.tsv)): 33 of the 48 go to 29 entries the map uses; 14
   are already a spelling of the entry they name, and 1 names an entry the map does not use. A piece that is a
   headword is in Rilly's letters; the others are in the corpus's (`x` and `X` for ḫ and ẖ, `s` for the sign se,
   `S` for s, `N` for ne), so `smlo` beside `smlo (1)` is a spelling with se.
2. **Rilly's page** of every entry has a column of its own.
3. **The scholars' own pages:** of the 206 proposals both judges found the same or otherwise, Rilly's record gives
   a page for none; it gives the author and the year, or the author alone. For 10 of them the table gives
   Griffith's own page, the printed page of Karanòg or of the Meroitic Studies where the check against his texts
   (section 8) found the statement.
4. **The editions' pages:** for 100 entries, the entries of Millet 2005 and FHN III that hold a word built on the
   entry which the editor reads the same way or otherwise, with their pages. The check against the editions
   recorded each word's entry in the edition, not its line, so the page is that of the entry.
5. **FHN IV's index:** for 113 entries, FHN IV's indexes of gods, persons, royal names, Meroitic titles, places
   and Meroitic words give the page where the term is indexed and the pages of FHN it lists or the name it sends
   to (137 references, read from the page images, since the text layer garbles some terms). The indexes of places,
   persons and royal names give the names among them: `Pedeme`, `Atiye`, `Tebwe` and the other places FHN prints in
   their Meroitic spelling, and rulers such as `Ntkmni`. These glosses are FHN's own statements of the meaning;
   they were not judged, so they make no entry agreed.
6. **Not in hand:** the pages of the other scholars (Hintze, Hofmann, Priese, Zyhlarz, Millet's earlier papers
   and others). Their works are not among our sources, but for papers that may be in the Meroitic Newsletter,
   whose scans we hold: the record gives a year at most, and without Rilly's bibliography, which we do not hold, a
   year does not say which paper is meant, so the Newsletter was not searched for them.

## 8. The check of the record against Griffith's own words

The lexicon gives 52 of the proposals the judges read to Griffith's Karanòg (1911) or his Meroitic Studies
(1916-17), the texts of his we hold, or to "Griffith" without a year. A sample of 20 of them went to a reader with
those texts. The sample was meant to cite texts we hold, but 34 of the 52 give no year, which does not say which
text, and 15 of the 20 drawn are among them. Bars, set before it was read: found for 10 or more, and as stated for
90% or more of those found.

| As stated | Otherwise | Not found |
|---|---|---|
| 15 | 0 | 5 |

Both bars are met: 15 found, all as the lexicon states them. The 5 not found all cite Griffith without a year: a
remark on two forms of `wi`, a reading the scan's text layer garbles, a Coptic comparison from Griffith's later
work, a remark that a woman could hold an office, and a reading in his edition of Faras, which we do not hold. The
evidence is weaker for `yetmde`, where Griffith has "kinsman" and "related to" but not "cousin", and for
`pelmos`, `at` and `atẖe`, whose words the text layer garbles. The record is faithful where it can be checked;
this sample cannot speak for the other scholars.

## 9. What the review changed

The review of 12 November, after the judges had answered, corrected two things. Neither touches the judges'
verdicts, and the figures file keeps the first count (`as_first_counted`).

1. **The names.** The rule rates every entry Rilly states; the code rated meanings and grammar words only, and
   called "proposed" the names that stand inside a translated word: Isis (`Wos`), Osiris (`Sori`, `Asori`),
   Napata (`Npte`) and the god `Mnp`. Rated as the rule says, the first four are agreed through the editors'
   readings and `Mnp` was stated by one (round three made it agreed, section 4).
2. **The words the map misread.** The check against the editions sorts its differences by a rule of its own
   (`difference_of` in [`src/experts/publish.py`](../../src/experts/publish.py)): the numeral 1 typed as the
   letter `l`, a name or a piece of another word read as a word, the kind of word only, another meaning. A word
   of the first two kinds is not built on the entry the map named, so it no longer counts as an editor reading
   that entry otherwise. Only such non-agreements are left out, never an agreement, so this can only move an
   entry from disputed to stated by one. `l` "to give" (117 uses) and `-so` were disputed only through such
   words and were stated by one after round one (round two makes `l` agreed and `-so` disputed, each through a
   proposal both judges read so); others keep their status and lose an editor's dissent (`mẖe`, `ato`, `kdi`
   among them). The check's rule sorts non-agreements only, so an agreement on such a word still counts; item 6
   of section 6 gives the figure without them.

As first counted: 70 agreed, 23 disputed, 59 stated by one and 25 proposed (16 entries change against the
count with both rounds), and a second figure of 3,873 (37.6%).

## 10. The meanings in our own words

A writer worded the meaning of each of the 177 entries anew, in at most eight words, from the lexicon's meaning
and the proposals the judges of round one found the same; 7 are empty, where the lexicon gives no meaning. A
check counts the words a meaning shares in a row with the lexicon's meaning and its proposals: one shared four
with the lexicon's meaning (`ye-`) and was reworded here (`REWORDED` in the script); none does now, and `public`
refuses to write a table in which one does. The table carries these meanings, under the licence of the data
([`LICENSE-DATA.md`](../../LICENSE-DATA.md)).

## Reproduce

```
python3 -I src/lexicon.py layout     # needs data/rilly2003/ and the local gloss file of the clean corpus
python3 -I src/lexicon.py packs      # refuses once a judge has answered
python3 -I src/lexicon.py check      # the sample given to Griffith; refuses once answered
python3 -I src/lexicon.py round2     # round two's packs and the writer's; refuses once answered
python3 -I src/lexicon.py round3     # round three's packs; refuses once answered
python3 -I src/lexicon.py public
python3 -I tests/test_lexicon.py
```

**Cost,** from the task notifications, by hand: four judges' packs 388,896 subagent tokens (99,371 and 101,866 for
the first judge, 98,363 and 89,296 for the second), about five minutes each; the check against Griffith's text
250,976, about ten minutes; round two's two judges 143,940 (71,296 and 72,644), about two minutes each; the writer
100,947, about four minutes; round three's two judges 171,392 (86,127 and 85,265), about three minutes each.
