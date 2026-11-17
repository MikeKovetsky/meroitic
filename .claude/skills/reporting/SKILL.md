---
name: reporting
description: How to report the status of the Meroitic project. Use whenever Mike asks for a status, where things stand, progress, the scoreboard or the north star, at the end of a milestone, and before quoting any of the project's headline numbers (distinct words translated, running words translated, distinct spellings translated, our own meanings, translation score). It fixes the table's shape, what each number means, where it is read or how it is counted, and what "Before us" is for each row.
---

# Reporting: the scoreboard and how each number is measured

Mike, 2026-11-16: "we need to develop an easier repeatable format of status sharing. 2-3 metrics we optimize for",
then "note down all into reporting.md skill in repo with how we measure each number to make sure we have
consistent ways of measuring across compactions and sessions".

This file is the single place for both. If a session's memory, a summary or an earlier message says something
else about a number, this file wins; if this file is wrong, change it here, with the date and Mike's words.

## 1. The shape of a status

A status is this table and three lines, and little else:

| Metric | Before us | Now | Since last status | Next target |
|---|---|---|---|---|
| Distinct words translated (north star) | | | | |
| Running words translated | | | | |
| Distinct spellings translated | | | | |
| Our own meanings | | | | |
| Translation score | | | | |

- **Done since last status:** one line.
- **Next:** one line, the next step by its name in `NEXT_STEPS.md` (section G).
- **Needs you:** one line, or "nothing".

Rules of shape, each from Mike's words on 2026-11-16:

1. The rows stand in this order, the north star first ("do it and add to the table as the first row").
2. The column "Before us" stays ("add a column "status before us". to see our progress from the start").
3. Short by default, but formatted: a bold lead line, the table, a few bullets. Never half a page, never a wall of
   text ("answer shorter by default. 1 paragraph"; "when i meant "paragraph" i meant shortness, not a wall a wall
   of text without formatting").
4. Under the table give the north star's range in one line, because its count of words is an estimate.
5. Say "provisional" beside any number whose work is still in review or not yet on main.

## 2. Words

- **Translated**, never "read". Every Meroitic sign can be read aloud; what is counted is whether the meaning is
  known ("why "read"? what does it even mean?"). A word is translated when the map gives it an accepted meaning or
  grammatical function (the map's levels `meaning` and `grammar`).
- **A word that needs a meaning** is every running word that is no name, no numeral and has no lost sign (the
  map's levels `name`, `number` and `lost` are left out of every share below).
- **A spelling** is one written form, exactly as it stands in a text. One dictionary word has many: with endings
  and prefixes, in variant writings, cut in two by an edition. Say "written form" if the word is unclear.
- **A dictionary word** is an entry of Rilly's lexicon of 2003 that is no name. All spellings built on one entry
  are that one word. An ending or a particle of the lexicon (a headword with a hyphen that is a function word)
  written as a word of its own is a piece of a word, not a dictionary word.
- **Our own meaning** is a meaning this project found, not one a scholar published.
- The public coverage page says "translated" for a wider count (names and numerals included, of all running
  words: 52.7% on the analysts' map, `current.running.of_all` of the map's figures file with the layers). If both
  appear, name the difference.

## 3. The rows

The corpus is `corpus_v6` (548 inscriptions, 10,290 running words). The map is the analysts' map
(`data/sources/v6/analysts/glosses.jsonl`, local) with the layers that later steps have laid over it
(`src/themap.py`, page `data/discovery/map_layers.md`; seven layers since 2026-11-16: the recurring open spellings
of step G1, the rare spellings of steps G2 and G4, the names and pieces of step G3, the entries Millet 2005 or
Lipiński 2011 give a meaning or call a name, the rare spellings whose unnamed part two checkers call an ending
or a known word, and those whose unnamed stem they call a name or an ending). `python3 -I src/themap.py` counts
it and writes `data/discovery/map_figures.json`: the first three rows are read from that file. Read a number from
its figures file or count it with the command given; never quote it from memory, from this file's log, or from an
earlier message.

### Distinct words translated (the north star)

- **What it is:** of the different words the corpus holds, the share that has a meaning. Mike: "this sounds like
  a north star metric if we want the entire language translatable".
- **How it is counted** (`src/words.py`, page `data/discovery/distinct_words.md`): every running word that needs
  a meaning is a dictionary word, a piece (an ending or a particle written as a word of its own), a name, or a
  stem the map could not name; pieces and names are not counted. Translated words are the dictionary
  words in use whose meaning the lexicon calls established or probable, and those to which a layer of the map
  gives a meaning that a later source states (`src/themap.py`). Distinct words are the dictionary words
  in use plus an estimate of how many of the unnamed stems are words of their own, from a sample of 240 stems
  judged by two checkers (bar: their kappa at least 0.6).
- **Now:** `data/discovery/map_figures.json`: `north_star.translated` over `north_star.distinct_words.point`, the
  share in `north_star.star.point`, its range in `north_star.star.low` and `north_star.star.high`. The count on
  the analysts' map alone, with no layer, stays in `data/discovery/distinct_words_figures.json` (`translated`
  over `distinct_words.point`, `star.point`, `star.low` and `star.high`): it was the figure of the first status.
  Give the share to one decimal as the command of section 4 prints it, divided from the counts: `star.point` is
  rounded to four places already, and rounding it again can put the tenth one too high (0.1215 is 156 of 1,284,
  12.1495%: 12.1%, not 12.2%).
- **Before us: the same as Now.** Mike, after asking three times how this row could rise without a meaning of
  ours: "“Before us” should really equal “Now”, 11.6%." (11.6% was the first count; the review of the same day
  took the endings and particles written as words for pieces, section 7. Before us is now, whatever the count
  gives.) The translated words were translated by scholars before the project, and the project has added none;
  the figures files give it so (`north_star.before_us` is `north_star.star`; in the distinct-words file
  `star_before` is `star`). A plain lookup of the lexicon finds fewer of them in the texts (112
  of 127 on 2026-11-16), `lookup.translated` in the distinct-words file; that is a fact about our matching and
  never the starting point of this row.
  **Confirmed on 2026-11-16 in the evening.** Mike first called the rule senseless ("“Before us” is set equal to
  “Now” - lol. this makes no sense"), was offered the plain lookup of the lexicon of 2003 as the starting point
  instead, and answered "anyones cares about 2003 dictionary? if new meanings arrived after it? why is it such a
  big deal?", then "ok, change to 12.5". So the rule stands, and the cell says why: write it as the share of the
  day with the words "all from scholars; ours: 0". When this row has risen within the project (it stood lower at
  the first count than that evening), say in one bullet that the project caught up with what scholars had
  published, and that this is no gain on the language. The lexicon of 2003 alone is never this row's starting
  point.
- **Next target:** the gain the next step's page gives, once that step's bar is met; "not known yet" until then.
  (`next.star.point` of the distinct-words file was the target for the first layer; G1 reached it.)
- **What moves it:** a dictionary word getting a meaning (a scholar's, from a source, or our own), or the count of
  distinct words being corrected. **What does not:** recognising one more spelling of a word that is already
  translated.
- **Counting again:** after a layer is added, run `python3 -I src/themap.py`: it counts the dictionary words again
  on the map with its layers. The estimate of the unnamed stems rests on the sample of 240 stems drawn on
  2026-11-16 from the 1,107 stems the analysts' map could not name. While the layers have taken at most 2% of
  those stems out of the unnamed ones, the estimate is carried as it was drawn. Past that (step G3 took more),
  the script makes it again from the sampled stems that are still unnamed, by the same rule of counting
  (`north_star.unnamed_stems` says how many of the sample are left and their verdicts). It stops if a layer adds
  a stem the sample was not drawn from: then draw and judge a new sample with its bar set beforehand
  (`src/words.py`: `population`, `packs`, `count`, `public`).
  **This replaces an earlier line of this file,** which said to draw and judge a new sample whenever a step
  changes which stems are unnamed. The new rule was written down on 2026-11-16 before step G3 was counted
  (`data/discovery/unnamed_spellings.md`, section 9). Asked whether to keep that recount or draw a new sample,
  Mike answered the same day at 14:49: "why do you need my approval to recount? this is obvious you need to
  recount to show the up to date result?". The recount stands; the north star is not provisional for it
  (section 6).

### Running words translated

- **What it is:** of the running words that need a meaning, the share that is translated. It shows how much of
  what scholars already know we can apply to the texts.
- **Now:** `current.running.share` of `data/discovery/map_figures.json` (`current.running.translated` over
  `current.running.need`); the command of section 4 prints it as the line "as it stands".
- **Before us:** the lexicon of 2003 looked up word by word, with none of the project's analysts or corrections:
  `lookup.running.share` of the same file, the command's line "plain lookup". It was 2,816 of 7,847, 35.9%, and
  does not change unless the corpus or the typed lexicon changes. It is a machine's baseline: a scholar reading
  the texts recognises more than a lookup.
- **Next target:** the gain the next step's page gives, once that step's bar is met; "not known yet" until then.
- **What moves it:** recognising a spelling as a known word; a meaning from a later source; showing that an open
  "word" is a name or a piece of one (it then needs no meaning).

### Distinct spellings translated

- **What it is:** the same, with each different spelling counted once, by the level it has most often in the map.
- **Now:** `current.spellings.share` of `data/discovery/map_figures.json`. **Before us:** `lookup.spellings.share`
  of the same file; it was 325 of 3,189, 10.2%. **Next target:** as for the running words. The command of
  section 4 prints each as the second number of its line.
- It stands far under the running words because the common words are the translated ones.

### Our own meanings

- **What it is:** the number of meanings this project found that (1) no source in hand states, (2) passed a test
  whose bar was committed before the test ran, (3) survived an independent check and the review, and (4) stand on
  a page of `data/discovery/`.
- **Now:** 0. **Before us:** 0.
- **What does not count:** a scholar's proposal that a test of ours favours (it is the scholar's); a meaning a
  later source states; a spelling recognised as a known word; a reading no test has passed.
- This is the only row that measures decipherment.

### Translation score

- **What it is:** on texts held back from tuning, the share of a scholar's units of meaning that our translation
  gives (a unit given counts one, a unit partly given a half), judged by two judges with decoys.
- **Now:** `data/discovery/f4_rounds_figures.json`: `held.score.translator` (one translator with rules, a handbook
  and parallels, on 13 renderings of Millet's, 218 units). The panel's higher score is not shown to beat it and
  is not the row's value.
- **Before us:** `held.score.glosses`: the map read word by word on the same texts. No machine translation
  existed; this is the earliest thing measured, and it already uses our map.
- **What moves it:** a better way of translating, or a better map. It can rise with no new word translated,
  because turning word-by-word readings into sentences is most of the gain.
- Its scale is not that of the rows above: a few epitaphs from one site, not the corpus.

## 4. The command for the first three rows

Run from the repository's root (it needs the local files: the map, the lexicon and the layers):

```bash
python3 -I src/themap.py
```

It writes `data/discovery/map_figures.json` and prints four lines. On 2026-11-16, with seven layers, it printed:

```
plain lookup: running words translated 2816 of 7847 = 35.9%; distinct spellings translated 325 of 3189 = 10.2%
base: running words translated 3676 of 7331 = 50.1%; distinct spellings translated 598 of 2955 = 20.2%
as it stands: running words translated 4186 of 7077 = 59.1%; distinct spellings translated 841 of 2781 = 30.2%
north star: 160 of about 1283 = 12.5% (11.8% to 15.6%)
```

"plain lookup" is Before us for the second and third rows, "as it stands" is Now, "base" is the analysts' map
with no layer (what Now was before G1). The page `data/discovery/map_layers.md` gives the figure after each
layer. `python3 -I tests/test_themap.py` checks the file against the local
count, against this skill and against the page `data/discovery/map_layers.md`.

## 5. Giving a status, step by step

1. Run the command of section 4 and read the figures files named in section 3. If a local file is missing,
   say which number could not be counted instead of quoting an old one.
2. Open `STATUS_LOG.md` beside this file and take its last row: "Since last status" is the difference from it, in
   points for the shares ("+3.8 points") and in units for the count of our own meanings, or "no change", or "new
   row".
3. Write the table and the three lines of section 1.
4. Add a row to `STATUS_LOG.md` with the date and the numbers given, and commit it with the docs.
5. If a number changed for a reason that is not obvious from the row's name, say in one bullet what moved it, in
   the terms of "what moves it" above. Mike asked this of three rows in a row on 2026-11-16.

## 6. Changing a measure

A row's definition, its "Before us" or its source changes only on Mike's word. Record the change in section 7 with
the date and his words, change section 3, and say in the next status that the row is measured differently, so
that a jump is not read as progress. A new row gets its "Before us" counted before it is first shown.

Counting a number again so that it is up to date after the map changes is no change of measure and needs no ask
(Mike, 2026-11-16, 14:49: "why do you need my approval to recount? this is obvious you need to recount to show the
up to date result?"). Recount, give the new number, and say in one bullet what moved it (section 5, item 5). What
still changes only on his word is what a row means, its "Before us" and its source.

## 7. Decisions, in Mike's words (all 2026-11-16)

- The format: "Template A: scoreboard. But add a column "status before us". to see our progress from the start".
- The spellings row: "let's have spelling in the table, too".
- The word "translated": "why "read"? what does it even mean? does it mean "we can read, not not translate the
  word"?".
- The north star: "why dont we have Distinct wrords translated? this sounds like a north star metric if we want
  the entire language translatable?"; "do it and add to the table as the first row".
- Its "Before us": "“Before us” should really equal “Now”, 11.6%."
- Its "Before us", again in the evening: "“Before us” is set equal to “Now” - lol. this makes no sense"; "anyones
  cares about 2003 dictionary? if new meanings arrived after it? why is it such a big deal?"; "ok, change to 12.5".
  It stays equal to Now and is written with its reason: "all from scholars; ours: 0".
- Its endings: the plan he answered "do it and add to the table as the first row" to was "remove names and cut
  pieces, strip the known endings so forms of one word fall together, then have two checkers judge a sample". The
  first count still took the endings and particles written as a word of their own for words (11.6%); the review
  made them pieces the same day (9.7%), as the plan and the checkers' case "piece" have it. Measured so since.
- Length: "answer shorter by default. 1 paragraph"; "when i meant "paragraph" i meant shortness, not a wall a wall
  of text without formatting".
- This file: "note down all into reporting.md skill in repo with how we measure each number to make sure we have
  consistent ways of measuring across compactions and sessions".
- The layers: "Yes, start G1 and G4, queue G2". G1 put the recurring-words results into the map as a layer, as
  sections 3 and 4 had announced; G2, G4 and G3 each added one the same day, and the leftover parts two more.
  Since then the first three rows are read from `data/discovery/map_figures.json`. No row's definition or "Before
  us" changed with it. The three dated pages that G1 named to be rebuilt (the coverage of the clean corpus, the
  lexicon's statuses, the translations' baseline, which is the last row's "Before us") keep their numbers: "Yes,
  waive it." (13:52).
- The recount of the north star after G3, from the old sample's stems still unnamed (section 3, "Counting
  again"), asked as "Accept the north star recount from the old sample, or draw a new sample?": "are you saying we
  need a new sample?", then "why do you need my approval to recount? this is obvious you need to recount to show
  the up to date result?" (14:48 and 14:49). No new sample was drawn; recounting needs no ask (section 6).

Offered and not taken up: the translation row could give way to "words whose meaning two scholars agree on"
(39.9%, `data/discovery/lexicon.md`); the column "Before us" could be named "Plain lookup".
