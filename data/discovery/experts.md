# The coverage map checked against two printed editions

Run on 2026-11-12 with the scripts in `src/experts/`. [The coverage map](coverage.md) counts 62.0% of the
corpus's running words as translated, every one of them from Claude Rilly's 2003 lexicon. This page asks how
often two other scholars, reading the same inscriptions in print, give a word the same meaning. The numbers below
are in [`experts_figures.json`](experts_figures.json) and are checked by `tests/test_experts.py`.

## 1. Answer first

1. **Where an expert gives a word a meaning, the map gives the same meaning for 276 of 397 words (69.5%).** These
   are the words the map counts as translated in the 31 texts that both we and the editions hold. The two overlap
   in part for 62 more and differ for 59.
2. **Two words carry most of the gap, and both are differences between scholars, not slips of the map.** Rilly's
   lexicon reads `yetmde` as "nephew, niece" where both editions read "relative"; it reads `qo` as "this one"
   where Millet reads "the noble". Outside those two, the map agrees on 259 of 304 words (85.2%).
3. **For a quarter of the words the check says nothing.** The expert gives no meaning, or does not have the word,
   for 140 of the 537 words the map counts as translated in these texts (26.1%).
4. **It found errors in our data.** In one epitaph the numeral 1 was typed as the letter `l` and read as a word;
   eleven names or pieces of words were read as words; and for `mlo` the map holds only "adjective" where both
   editions read "good".
5. **It found almost no new meaning.** Two readers listed 167 different meanings that the editions give. Those
   stated as sure on words the map has no accepted meaning for are mostly titles the editions leave untranslated
   too, phrases whose words the map reads the same way, and meanings Rilly holds as proposals (section 5).
6. **The editions are not a later authority than the lexicon.** One is of 1998, the other was printed in 2005
   from a manuscript its author left unfinished. Where they differ from Rilly 2003, this check cannot say who is
   right.

## 2. What was compared

- **The map:** every word of the corpus with the reading and the level `src/coverage.py` gives it after its four
  corrections ([section 7 of the coverage page](coverage.md)). A word counts as translated at the levels meaning,
  grammar, name and number.
- **The editions:**
  - N. B. Millet, "The Meroitic Inscriptions from Gebel Adda", *Journal of the Society for the Study of Egyptian
    Antiquities* 32 (2005), 1–66: 46 entries, most with a transliteration, a commentary and, for 20, a rendering
    into English.
  - *Fontes Historiae Nubiorum* III (Eide, Hägg, Pierce and Török, Bergen 1998): twelve entries on Meroitic
    texts, each a transliteration followed by László Török's comments, which translate what can be translated.
  Both are in copyright and are kept on the author's machine, like the lexicon. Nothing of them is printed here
  beyond single words.
- **The texts held by both:** 31 inscriptions, 23 of Millet's and 8 of FHN's. They were matched by shared
  runs of five letters, counted in both directions, and then read side by side; the table `HELD` in
  `src/experts/prepare.py` names each pair. The older part of the corpus holds padded copies of most of them, and
  one copy stands for each.
- **The words:** 1,174 in those texts. 1,115 were judged (589 against Millet, 526 against FHN); 46 masked names
  and 13 words with a lost sign were not.
- **The judges:** four Claude Opus 5.5 agents, each told to read its pack and nothing else. Three got one pack
  each, and a second judge got the third pack again. A pack holds, for each
  inscription, the edition's printed entry and beside it our words in order with our reading of each. The judge
  gives every word one verdict:

  | Verdict | What it means |
  |---|---|
  | agree | the edition gives the word the same meaning |
  | partly | the two overlap but differ in a way that matters |
  | differ | the edition gives it another meaning |
  | new | the edition gives a meaning, and the map none or only the kind of word |
  | silent | the word is in the edition's text, without a meaning |
  | absent | the word is not in the edition's text of the inscription |

- **Decoys:** 36 readings of level "meaning" were swapped for another word's reading before the packs were
  written, without a mark. They are left out of every figure and show how lenient a judge is (section 6).

## 3. The result

Words the map counts as translated, first judge, decoys left out:

| | Words | The edition gives a meaning | agree | partly | differ | new |
|---|---|---|---|---|---|---|
| all | 537 | 397 | 276 (69.5%) | 62 | 49 | 10 |
| level meaning | 326 | 241 | 158 (65.6%) | 57 | 17 | 9 |
| level grammar | 78 | 45 | 17 (37.8%) | 2 | 26 | 0 |
| level name | 128 | 106 | 96 (90.6%) | 3 | 6 | 1 |
| level number | 5 | 5 | 5 (100.0%) | 0 | 0 | 0 |
| against Millet 2005 | 307 | 243 | 156 (64.2%) | 49 | 30 | 8 |
| against FHN III | 230 | 154 | 120 (77.9%) | 13 | 19 | 2 |

The edition is silent on 125 of the 537 words, and 15 are not in its text. 19 of the 276 agreements are on a
meaning the edition itself marks as unsure.

Words the map does not count as translated (542):

| Level in the map | Words | The edition gives a meaning | agree | partly | differ | new |
|---|---|---|---|---|---|---|
| hypothesis (the lexicon has a proposal) | 234 | 114 | 73 (64.0%) | 17 | 17 | 7 |
| kind (only the kind of word is known) | 127 | 43 | 23 (53.5%) | 6 | 3 | 11 |
| unknown | 181 | 54 | 0 | 0 | 0 | 54 |

So where the lexicon has only a proposal, the editions side with it about as often as they side with its accepted
meanings. About half of the 54 "new" verdicts on unknown words are personal names that the map did not take for
names (section 5).

## 4. What the differences are

The 537 translated words fall into three groups by our reading:

| Group | Words | The edition gives a meaning | agree | partly | differ | new |
|---|---|---|---|---|---|---|
| `yetmde`: our "nephew, niece"; the editions "relative", "mde-relation" | 60 | 60 | 6 | 54 | 0 | 0 |
| `qo`, `qowi`: our "this one (is)"; Millet "the noble (one)" | 41 | 33 | 11 | 3 | 19 | 0 |
| every other word | 436 | 304 | 259 (85.2%) | 5 | 30 | 10 |

The groups are drawn by the wording of our reading (`group_of` in `src/experts/publish.py`). The 45
non-agreements of the last row, sorted by a rule on the judge's note (`difference_of`):

1. **The numeral 1 typed as the letter `l`: 8.** In the epitaph of Makheye (Faras 44, REM 0544, FHN 271) each
   prince's name is followed by the numeral 1; FHN's comment says so, and the scanned page shows it. Our copy of
   the older corpus has `l` there, and the map read it as a word. The text stands four times in that corpus.
   The count of translated words does not change, since a numeral counts as translated; the reading does.
2. **A name or a piece of a word read as a word: 11.** For example the names Atoye and Tareye, read as "water"
   and "to give" with an ending; the name Qoresemye, read as "wife of the king"; the first half of the name of
   Osiris, written apart, read as a genitive.
3. **The map has only the kind of word: 10.** `mlo` and `mlolowi` are "adjective" in the map; both editions read
   "good". The title `smlo` is "a title"; Millet reads "good person".
4. **Another meaning or identification: 16.** `tebwe` is the Abaton for the lexicon and Thebes for FHN (4
   places); `pilqoyte` "as far as Philae" against "from Philae" (2); `mete` "child" against Millet's "little" (2);
   `dime` "cow" against Millet's "day"; the place `nlote`, Karanòg for the lexicon and Aniba for FHN; and single
   cases.

The judges also found only a name where our copy has `mete l` or `mokelowi` after a masked name: the expert's
text has nothing there. That is independent support for the first of the map's corrections, which reads those
words as the rest of a name left by the corpus's padding.

## 5. Meanings the editions give that the map lacks

Two readers (Claude Opus 5.5 agents again) listed every meaning the editions give to a Meroitic word, ending or
phrase: one in the entries we do not hold, one in the comment sections of the 31 entries we do. Together 180
lines, 167 different after merging by edition, word and meaning. Each word was then looked up as the map looks a
word up.

| How the map holds the word | Lines |
|---|---|
| translated | 103 |
| a proposal only (hypothesis) | 24 |
| the kind only | 13 |
| unknown | 5 |
| not in the map | 22 |

For the 146 lines where the map has any reading, two judges compared the two meanings, with decoys of another
design (section 6). On the 103 lines whose word the map translates, the first judge agrees with our reading on 55
of 90 and the second on 57 of 92 (each judge's own decoyed lines left out). What goes on the list of what the map
lacks:

| | Lines | Stated as sure by the edition |
|---|---|---|
| the map has no accepted meaning for the word | 64 | 26 |
| the map translates the word and both judges say the edition reads it otherwise | 29 | 15 |
| the same, on the word of the one judge who saw our reading | 9 | 4 |
| the same, one judge of two | 3 | 3 |
| all | 105 | 48 |

What is in it:

1. **The same differences of school:** `yetmde` and `qo` again, `peseto` (our "viceroy"; the editions "prince",
   "King's Son") and `ant` (our "priest"; FHN "prophet, hont-priest").
2. **`mete`:** "child" in the map; "little" for Millet, who renders two brothers as Big Taraqa and Little Taraqa,
   and "second, junior" for FHN, with a question mark.
3. **`selele`:** "cataract" for FHN, after Griffith 1912; the lexicon holds it as a place name of disputed
   location.
4. **Proposals of Millet's that contradict our reading, each marked by him as unsure:** `dime` "day" (ours
   "cow"), `xlbi` "month" or "moon" (ours "bull"), `ste` "follower" (ours "mother").
5. **Most of the 26 sure meanings on words without an accepted meaning** are titles the edition leaves
   untranslated too ("great womnis"), phrases whose words we read the same way, or meanings the lexicon holds as
   proposals (`ari` "heaven", `pqr` "prince").
6. **Two artefacts of this table, not errors of the map:** an ending looked up by itself gets the wrong entry
   (`-te`, four lines, three of them the editions' "in", which the map does read inside words), and one reading
   reached the judges cut short.

In the 31 texts themselves the first judge found a meaning from the edition for 58 words the map leaves without
one. Sorted by a rule on the judge's note (`kind_of` in `src/experts/missing.py`), they are 30 personal names, 8
pieces of other words, 6 places or peoples and 14 words, 12 of them proposals the edition marks as unsure. The
lists with the meanings are local, because they hold the lexicon's glosses and the editions' wording;
[`experts_words.tsv`](experts_words.tsv) gives every word of the 31 texts with its level and the verdicts,
without them.

## 6. How far to trust it

1. **The judges were not lenient.** In the first run the first judge found the edition giving a meaning for 22 of
   the 36 decoys and marked 20 "differ", 1 "partly" and 1 "agree"; in that one the decoy meant nearly the same as
   our real reading ("their mother" for "of the mothers"). The second judge saw 9, found a meaning for 7 and marked
   all 7 "differ". In the table of meanings each judge saw 15 decoys of its own in place of our reading, on
   different lines, and accepted none of the 30.
2. **The first run's decoys were weaker than they should be.** They were drawn by kind of word, which let two
   near-synonyms through, and only from words of level meaning: leniency on grammar, names and proposals is not
   tested there. The second design draws a decoy that shares no content word with our reading or with the
   edition's meaning.
3. **Two judges agree, which shows the verdicts are stable, not that they are right.** On the 372 words both
   read they gave the same verdict on 361 (Cohen's kappa 0.96); on the 79 lines of the meanings table both saw
   with our reading, on 74 (0.89). Both are the same model with the same instructions.
4. **One judge for two thirds of the words.** Only the third pack had a second judge.
5. **The editions reached the judges as text layers,** one of them an OCR of a scan with misread letters. A
   judge could mark a word absent that is there.
6. **One commentary did not reach its judge.** Millet prints one commentary for the two fragments GA55 and GA56,
   after the text of GA56, and the packs gave it with GA56 only. The words of GA55 were judged without it, and
   the judge marked every one "silent"; the commentary takes `abrlo`, "man" in the map, for the father's name.
7. **Each list of meanings comes from one reader,** so its completeness is not measured, and the judges of the
   meanings table compared the reader's wording of the edition, not the print.
8. **Small and of one kind:** 31 texts, most of them epitaphs. The inscription of Kharamadoye is 234 of the
   1,115 words, and FHN translates little of it.

## 7. Files and rebuild

| File | What it holds | Where |
|---|---|---|
| `src/experts/prepare.py` | the match of entries to corpus texts, the judges' packs with decoys, the first reader's pack | public |
| `src/experts/tally.py` | the count of the verdicts, the two-judge comparison, the local lists | public |
| `src/experts/missing.py` | an edition's word in our spelling, looked up as the map looks it up | public |
| `src/experts/close.py` | the second reader's pack, the table of meanings with each judge's decoys, the list of what the map lacks | public |
| `src/experts/publish.py` | the two public files below | public |
| `tests/test_experts.py` | the method on made-up rows and answers, and the numbers of this page | public |
| `experts_figures.json` | every number of this page but the costs | public |
| `experts_words.tsv` | 694 lines: each word form of the 31 texts with its level and the first judge's verdicts; no readings | public |
| `data/sources/expert/` | the packs, the answers, the rows with the decoy keys, the lists with readings and meanings | local |
| `data/sources/jssea/`, `data/sources/fhn/` and `data/sources/jssea-text/`, `data/sources/fhn-text/` | the two editions and their text layers | local |

```
python3 -I src/experts/prepare.py match        # the scores behind the table HELD, counted both ways
python3 -I src/experts/prepare.py packs        # refuses once a judge has answered
python3 -I src/experts/prepare.py extra        # refuses once the reader has answered
python3 -I src/experts/tally.py
python3 -I src/experts/missing.py
python3 -I src/experts/close.py reader         # refuses once the reader has answered
python3 -I src/experts/close.py table          # refuses once a judge has answered
python3 -I src/experts/close.py count
python3 -I src/experts/publish.py
python3 -I tests/test_experts.py
```

The packs go to agents by hand: one agent per pack, told to read only that file and to write its answers file.

## 8. Cost

Eight agent runs and one reviewer of the local scripts: two readers (101,743 and 115,377 subagent tokens), four
judges of the packs (104,505, 119,963, 119,956 and 117,195), two judges of the meanings table (66,846 and
66,858) and a reviewer that had reached 210,918 after four rounds. Together about 1.02 million tokens and about
35 minutes of running, in two passes. The review of this page and of the scripts as published is counted in
[`REPORT.md`](../../REPORT.md).
