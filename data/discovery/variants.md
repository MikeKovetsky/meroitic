# Which pieces without a meaning are spellings of known words?

Built on 2026-11-11 with `src/variants.py`. The [coverage map](coverage.md) lists 1,336 pieces of Meroitic without
an accepted meaning. A scorer that knows only letters compared each of them with the words of Claude Rilly's 2003
lexicon, to find the pieces that are another spelling of a known word, or a known word with an ending. It was
tested first on the spelling variants that the lexicon itself lists, each hidden in turn. The numbers below are
checked by `tests/test_variants.py`.

## 1. Answer first

1. **The test missed its bar.** The bar was set before the first run and has two parts. The search brings 187 of
   the 242 hidden variants back to their own entry as the single best match (77%; the bar was two thirds, so this
   part is reached). But only 105 of the 242 (43%) come back with a match that stands out from made-up words (the
   bar was half, so this part is not reached).
2. **Why: a short word cannot stand out.** None of the 93 hidden variants of three or four letters beats the
   made-up words, although 61 of them come back to the right entry. Of 1,000 made-up words of three letters, 350
   are a spelling of the lexicon letter for letter, so no match of a real word can be rarer than that. From five
   letters up, 105 of 149 hidden variants come back and stand out (70%).
3. **As a ranking the search is good.** The right entry is among the three best for 232 of the 242 (96%). When a
   match beats the made-up words, it is the right entry 105 times in 118 (89%), and 12 of the other 13 went to
   an entry that the lexicon itself links with the right one, or tied with it.
4. **On the pieces without a meaning, the letters alone do not decide.** 1,210 pieces were searched. 70 are
   headwords that the lexicon links with their best match itself. Of the other 1,140, 82 beat the 5% bar where
   the made-up words predict 57 (chance alone gives as many 0.08% of the time). But real words that the lexicon
   links with nothing beat the same bar 8 times in 76, and 6 times in 24 from seven letters up: at their rate
   about 104 pieces would beat it. Different words that share a part (two royal names ending in `-demni`, a word
   and its genitive) look as close as two spellings of one word.
5. **Two blind checkers confirm 48 of the 105 matches that beat the bar, 29 of them new.** Each match was read
   by two independent checkers who saw the piece's contexts and the candidates, and no other reader's guess. Both
   said "the same word" and named the same candidate for 48. 19 of those are among the 23 pairs that the lexicon
   links itself; the other 29 are new, and for 26 of them the word has an accepted meaning. For two of the new
   ones, `mXeyot` and `yetmetl`, the pack showed a word that holds the piece's letters, with the gloss the map gives
   it (section 5); without them 46 are confirmed.
6. **The check is careful and misses a lot.** Mixed into the packs were 24 listed variants whose answer is known.
   Of the 12 shown with all their candidates, both checkers named the right entry for 6. Of the 12 shown with
   the right entry taken out, both accepted a look-alike for 1. So a confirmation is fairly safe, and a "no"
   says little.
7. **The 26 would move 59 running words of the coverage map** (section 6): from 13,292 to 13,351 of 21,977, which
   is 60.5% to 60.7%, and with near-copies counted once from 59.9% to 60.4%. Five more texts would be complete.
   Without `mXeyot` and `yetmetl` it is 54 running words, still 60.7%. The map's own numbers are not changed here.
8. **The largest candidate is not confirmed.** `smlowi` stands in 81 running words. Both checkers take it for a
   known word, but one reads `sem` with `-lowi` and the other the title `smlo` with `-wi`.
9. **What the listed variants show about Meroitic spelling** (section 3): almost all of it is vowels. An `e` is
   left out or added (133 times in 307 variants), `e`, `i` and `o` stand for one another (73 times), and the
   vowel at the start comes and goes (`Amni`, `Mni`: 42 times). Among consonants the listed variants show
   `l` for `n`, `t` for `s` and `d`, `q` for `w` and `k` for `ḫ`, four or five times each. They never show `r`
   for `l`, which is why the search does not rate `prSn` as a spelling of `plsn` (section 4).

## 2. The test on the hidden variants

**The bar, set before the first run.** The test counts every variant that Rilly lists under a word of the lexicon
proper, that has three letters or more as the search writes it, and that is not spelled like its own headword.
The test succeeds only if both parts hold:

1. The search brings at least two thirds of them back to their own entry as the single best match. A tie with
   another entry is a miss.
2. For at least half of them, the own entry is the single best match and at most 5% of made-up words of the same
   length get a match as good.

**The result.** 194 entries of the lexicon list 311 variants. 4 are spelled like their headword once marks and
capitals are set aside, which leaves 307 pairs of a variant and its headword: 268 under words and 39 under
endings and prefixes. All 307 train the model. Those under words that have three letters or more are 242
different spellings, and those are the hidden variants. Each was struck from the whole lexicon (an entry that has
it as its headword goes too), the model was trained on the rest, and the variant was searched among the 655
matches of the pool (section 7).

| Hidden variants | How many | Own entry is the single best match | Own entry among the three best | The best match beats the 5% bar | Both: single best match and beats the bar |
|---|---|---|---|---|---|
| All | 242 | 187 (77%) | 232 (96%) | 118 | 105 (43%) |
| 3 or 4 letters | 93 | 61 | 86 | 0 | 0 |
| 5 or 6 letters | 92 | 77 | 89 | 64 | 59 |
| 7 letters or more | 57 | 49 | 57 | 54 | 46 |
| Marked as uncertain by Rilly (`mle (?)`) | 26 | 15 | 23 | 6 | 5 |
| Not marked | 216 | 172 | 209 | 112 | 100 |
| Stricter: the entry's other variants hidden too | 242 | 178 | 223 | 109 | 92 |

Against the bar: part 1 needed 162 and has 187, so it is reached. Part 2 needed 121 and has 105, so it is not
reached. The test as a whole did not succeed.

A variant's chance counts the variant itself among the made-up words (section 7, point 6), as in the Egyptian
search. So `Atwete`, a variant of `Twete` that 50 of the 1,000 made-up words equal, counts as not standing out.
By the bar's own words (at most 5% of made-up words as good) it stands out, and part 2 has 106, still short of 121.

1. **The length decides.** Letters are counted as the search writes them: the consonants, the written vowels
   `e`, `i` and `o`, and one mark for a vowel at the start. No hidden variant of three or four letters beats the
   bar, and it could not: 350 of the 1,000 made-up words of three letters and 63 of those of four letters are a
   spelling of the lexicon letter for letter (467 and 244 when an ending may follow), and no match is better
   than that. Of five letters it is 18 (100 with an ending), of six letters 1 (27).
2. **The 55 misses.** 24 went to an entry that the lexicon itself links with the right one, or tied with it:
   the lexicon gives many variants an entry of their own (`asente` says "see `snte`"), and the search found that
   entry. This count was made after the run and is not part of the bar. The other 31 are mostly short
   (`mke` for `mk` went to `meke`, `tre` for `tr` to `Atri`).
3. **The stricter row** hides every other variant of the entry as well and leaves its pairs out of the training,
   so the variant has only the headword to come back to: 178 of 242 (74%).
4. **One shortcut.** The made-up words were searched once, in the whole pool with the model trained on all 307
   pairs, not once for each hidden variant in the pool without it. For a sample of 30 hidden variants the made-up
   words were searched again as the variant itself was (`python3 -I src/variants.py sample`): the chance is the
   same for 21, differs by at most 0.011 for the other 9 (11 made-up words in 1,000), and no variant changes
   sides of the 5% bar.

## 3. What the listed variants show

The model starts flat: a letter stays with a chance of 0.80, drops with 0.10, and the other 0.10 is spread evenly
over all other letters. It holds no groups of like letters. What it then counts on the 307 aligned pairs (1,484
letters of the headwords, and 132 letters added in the variants):

| The variant has | Times | Out of |
|---|---|---|
| no `e` where the headword has one | 67 | 342 `e` |
| an `e` that the headword does not have | 66 | 132 added letters |
| no vowel at the start where the headword has one (`Mni` for `Amni`) | 21 | 58 |
| a vowel at the start that the headword does not have (`asr` for `sr`) | 21 | 132 added letters |
| `e` for `i` | 21 | 99 `i` |
| `o` for `e` | 19 | 342 `e` |
| an `i` that the headword does not have | 19 | 132 added letters |
| no `i` where the headword has one | 15 | 99 `i` |
| `i` for `e` | 14 | 342 `e` |
| a vowel at the start for `y` (`esebe` for `yesebe`) | 14 | 47 `y` |
| `e` for `o` | 11 | 88 `o` |
| no `o` where the headword has one | 7 | 88 `o` |
| `i` for `o` | 7 | 88 `o` |
| `l` for `n` | 5 | 79 `n` |
| `t` for `s` | 5 | 77 `s` |
| `t` for `d` | 4 | 63 `d` |
| `q` for `w` | 4 | 36 `w` |
| `k` for `ḫ` | 4 | 39 `ḫ` |

No variant has `r` for `l` or `l` for `r` (64 `l` and 89 `r` in the headwords), and none has `t` for `l`.

**Endings.** A piece may be an entry with one of the 25 endings of `lexique.SUFFIXES`. How often each stands was
counted on the 654 different words of the corpus that the coverage map's lookup explains as an entry or as an
entry with an ending: 402 are bare, 34 have `-l`, 27 `-li`, 24 `-lowi`, 22 `-te`, 20 `-lo`, 16 `-leb`, 15 `-se`
and the other 17 endings 94 together.

## 4. The pieces without a meaning

Of the 1,336 pieces, 126 were not searched: 124 have one or two letters, so anything fits them, and 2 hold a
digit or a lost sign. Of the 1,210 searched, 963 are letters that no entry explains and 247 are headwords of the
lexicon without an accepted meaning. A headword is compared with every word but itself and the entries spelled
like it.

**Set aside: 70 headwords that the lexicon links with their best match itself.** One of the two entries lists a
spelling of the other, or sends to it in its text ("variant of", "see"). 23 of them beat the bar. They are no
finds, but they go to the checkers with the rest.

| The other 1,140 pieces | Searched | Beat the 5% bar | Expected by the made-up words (5%) | Expected at the rate of real words (below) |
|---|---|---|---|---|
| 3 or 4 letters | 443 | 2 | 22 | 0 |
| 5 or 6 letters | 398 | 29 | 20 | 29 |
| 7 letters or more | 299 | 51 | 15 | 75 |
| All | 1,140 | 82 | 57 | 104 |

1. **Against made-up words there is an excess:** 82 where 57 are expected, which chance alone gives 0.08% of the
   time. None passes the bar that allows for 1,140 tries (Benjamini and Hochberg, a fifth of the passes allowed
   to be chance): it asks for six pieces at the smallest chance there is, 1 in 1,001.
2. **Against real words there is none.** 91 words of the lexicon have an accepted meaning, list no variant, send
   to no other entry and share no spelling with one. For 15 of them the lexicon still links the word with its
   best match. Of the other 76, 8 beat the 5% bar where 4 are expected: none of 25 with three or four letters, 2
   of 27 with five or six, and 6 of 24 with seven or more. These are different words that share a part: the royal
   names `Tkidemni` and `Tktidmni`, `Teqoridemni` and `Tmelọrdeamni`, or `Amniterese` beside `Amnitore`. At their
   rate the 1,140 pieces would give about 104, more than the 82 found. 24 words are few to take a rate from, so
   the last column is rough, but it says what the checkers have to tell apart: one word spelled two ways, and two
   words built alike.
3. **What the 82 are:** 70 are letters and 12 are headwords; 43 would carry an ending; for 46 the best match has
   an accepted meaning, so a confirmed piece would count as translated. The 82 pieces stand in 375 running
   words.
4. **The examples that started this step** (the pieces that the checkers of the
   [Egyptian search](egyptian.md) recognised by eye). `pertese` beats the bar as `perite` with the ending `-se`
   and an `i` left out. `prSn` and `petmoS` have the right entry, `plsn` and `pelmos`, as their best match, but
   do not beat the bar: no listed variant has `r` or `t` for `l`, and `prSn` has four letters. `amn` has `Amni`
   as its best match and three letters. `menote` beats the bar with another word first and `Amnote`, the word
   those checkers named, second. `stol` is the end of a longer word, which a search for spellings does not look
   for.

Every searched piece is in [`variants_candidates.tsv`](variants_candidates.tsv) with its best match, the ending,
the letters that differ and the share of made-up words that do as well. Read it as a list of look-alikes ranked
by letters, not as a list of finds.

## 5. The check of the best matches

All 105 pieces whose best match beats the bar went to the checkers: the 82, and the 23 that the lexicon links
itself. They were mixed with 24 items whose answer is known, unmarked, which makes 129 items in three packs. Each
pack was read by two Claude Opus 5.5 checkers, each on its own, in a folder that held the pack and
[the brief](variants_brief.md) and nothing else.

**What a checker saw.** The piece and the number of texts it stands in; up to three contexts, with what is known
of each word under it; the lexicon's entry when the piece is itself a headword; and the three best candidates,
each with its entries, the letters that differ, how often the listed variants show each change, and up to two
contexts of the candidate word. Under a word a pack shows only what the coverage map counts as translated or
what the lookup took from the lexicon. A reading that an analyst of the map only guessed at shows as `?`, and so
does every word that the map finds the piece in, and every word that is a spelling of a control or a decoy, bare
or as the first part of a word the map cuts. No item says what kind of word the piece is.

**Three items showed a word with their own letters, glossed.** That rule goes by how the map cuts a word, so a word
that holds the piece's letters, but that the map cuts otherwise and counts as translated, kept its gloss. Beside
`mXeyot` the pack showed `mXeyotowi`, which the map cuts as `mẖeyose` with two endings; neither checker cites it.
In a candidate's context for `yetmetl` it showed `yetmetlXl`, which the map reads as the name Yetmet with `lẖ` and
`-l`; both checkers cite it. Beside the decoy `ateqi` it showed `yetmdelowiateqi`, whose gloss names `ateqi`. No
other item shows a gloss under a word that holds its own letters. This was found after the packs were read, so
they stay as they were, and the counts below give both: `mXeyot` and `yetmetl` are among the 48 confirmed.

**The items with a known answer.** All 24 are listed variants that stand in the texts, shown as if they were
pieces, with the candidates the search gave when they were hidden. The 12 controls keep those candidates, so the
entry that lists the variant is among them when the search found it. The 12 decoys have that entry taken out,
and every entry the lexicon links with it, so that whatever candidate a checker accepts for a decoy is a
look-alike.

| | Checker 1 | Checker 2 | Both |
|---|---|---|---|
| The 105 matches: the same word as a candidate | 51 | 55 | 48 with one candidate, 1 with two |
| The 105 matches: another known word | 2 | 1 | 1 |
| The 105 matches: no | 52 | 49 | 46 |
| The 12 controls: the right entry named | 7 | 8 | 6 |
| The 12 decoys: a look-alike accepted | 1 | 1 | 1 |
| The 12 decoys: the true word named all the same | 4 | 5 | 4 |

The two checkers gave the same verdict on 116 of the 129 items, and on 96 of the 105 matches.

1. **Confirmed: 48.** A piece is confirmed when both checkers say it is the same word and name entries of one
   candidate. For 8 of the 48 that candidate is the search's second or third, not its first. Without `mXeyot` and
   `yetmetl` (above) it is 46, and 24 of the new ones have an accepted meaning.
2. **19 of the 48 are pairs the lexicon links itself** (`arebetke` and `arbetke`, `pkrtr` and `pqrtr`). They
   show that the checkers read the entries; they are no finds, and none of them has an accepted meaning.
3. **29 are new.** 26 are a word with an accepted meaning (the table in section 6). Three are a word without
   one, so two unknowns become one: `mlNtel` is `mlne` with `-tel`, `tmNte` is `Tmne` with `-te`, and the
   headword `yeroteke` is `yerote` with `-ke`.
4. **The controls.** Both checkers named the right entry for 6 of 12. For a seventh, `qetNyiNli`, both named
   `qetneyineqeli`, an entry that the lexicon itself gives as a variant of the right one. The other five have thin
   contexts, and at least one checker said so and answered no. So each checker named the right entry for 7 or 8
   of the 12 true spellings, and both together for 6.
5. **The decoys.** Both checkers accepted one look-alike: `amnpte` as `Amnp` with the ending `-te`, where the
   lexicon lists `Amnpte` as a spelling of `Mnpte`. For four decoys both named the true word although it was not
   among the candidates. The checkers have read the literature, as every model has, and for one of the four,
   `ateqi`, the pack showed the word by name (above).
6. **`smlowi` is the one piece on which both say "the same word" and differ on which:** `sem` with `-lowi`, or
   the title `smlo` with `-wi`. It is not counted as confirmed. Two other readers of this project, who worked from
   the texts the same day and did not see these packs, read it as `sem` with `-lowi` (their reports are kept
   locally). That is support from outside this check; the check itself leaves the choice open.

**An earlier pass, set aside.** The first packs were not blind. A context could show the map's analyst's guess
under a word that holds the piece itself, inside the item (17 of the 105 matches) or under the same word in
another item of the same pack (15 more), and each item named the kind of word: the analyst's label for a piece,
the true word's kind for a control or a decoy. That pass confirmed 53 matches, `smlowi` among them, with both
checkers citing the guessed gloss; both were right on 10 of 12 controls and accepted the same decoy. Its packs
and answers are kept locally and counted nowhere. 45 pieces are confirmed in both passes, and 104 of the 129
items got the same two verdicts both times.

## 6. What the confirmed pieces would move in the coverage map

A running word moves to "translated" when every piece that keeps it from being translated is confirmed as a word
with an accepted meaning. Counted on the map's gloss file, without changing the map:

| | Now | With the 26 confirmed pieces |
|---|---|---|
| Running words translated, all 899 texts | 13,292 of 21,977 (60.5%) | 13,351 (60.7%) |
| Running words translated, near-copies counted once | 5,266 of 8,786 (59.9%) | 5,303 (60.4%) |
| Texts with every legible word translated | 82 of 605 | 87 |

That is 59 running words, 37 with near-copies counted once. Without `mXeyot` and `yetmetl` (section 5) it is 54
and 35, still 60.7% of all running words and 60.3% with near-copies counted once, and the same five texts. The 26
pieces:

| Piece | The word, for both checkers | Ending | Letters that differ | Running words it would move |
|---|---|---|---|---|
| `tedxli` | `te-dḫe-l` | | e dropped | 13 |
| `bedewitel` | `Medewi` | -tel | b for m | 7 |
| `beke` | `Beke` | | | 5 |
| `akdiyetedxelowi` | `dḫe` | -lowi | k added, d added, i added, y added, t added, e added | 4 |
| `kditelewi` | `kdise` | -lowi | e for o | 4 |
| `mXeyot` | `mẖeyose` | | t for s | 4 |
| `eked` | `ked` | | 0 for y | 2 |
| `smlo` | `smlo (1)` | | | 2 |
| `SNmdet` | `snmdese` | | t for s | 1 |
| `SSimeleb` | `ssimete` | -leb | t dropped, e dropped | 1 |
| `Sirlmroke` | `siremroke` | | e dropped, l added | 1 |
| `Sorkxror` | `Sorkror` | | x added | 1 |
| `aberse` | `abr` | -se | e added | 1 |
| `dtedxelowi` | `te-dḫe-l` | -qowi | d added, q dropped | 1 |
| `ipxetelo` | `Ipḫe` | -teli | o for i | 1 |
| `kditebetowi` | `kdise` | -lowi | b for l, e added, t added | 1 |
| `mXeyeos` | `mẖeyose` | | e added | 1 |
| `mdewetye` | `Mdewe` | -ye | t added | 1 |
| `menote` | `Amnote` | | e added | 1 |
| `pXrse` | `Pẖrse` | | | 1 |
| `qoriti` | `Qoreti` | | i for e | 1 |
| `tedxellwi` | `te-dḫe-l` | -lowi | o dropped | 1 |
| `terekelo` | `t-erike-l` | | e for i, o added | 1 |
| `xrpeN` | `ḫrpḫne` | | e for x | 1 |
| `xrpxte` | `ḫrpḫe` | -te | e dropped | 1 |
| `yetmetl` | `yetmetne` | | l for n, e dropped | 1 |

1. **The ending and the letters are the search's, not the checkers'.** They say how the search lined the piece
   up with the word (`0` is the mark for a vowel at the start). A checker who confirms the word may cut the piece
   otherwise: both read `dtedxelowi` as `tedxelowi` with a stray `d` before it, where the search took the ending
   for `-qowi`, and both read `akdiyetedxelowi` as a mother's name written together with `tedxelowi`.
2. **Three pieces are spelled like an entry letter for letter** (`beke`, `smlo`, `pXrse`). The map's analysts had
   cut or read them otherwise, without being sure, so they stood on the list.
3. **All 48 confirmed pieces** are in [`variants_confirmed.tsv`](variants_confirmed.tsv), forms only.
4. **Not in the count:** `smlowi` (81 running words, section 5), and the true spellings that the check missed.
   By the controls that is about as many again.

## 7. Method

1. **The pool.** The lexicon proper has 804 entries: 688 words and 116 endings, prefixes and infixes. The pool is
   the 688 words. An ending is too short to search for, and a word's level in the coverage map does not hang on
   its endings. Entries whose headwords have the same letters are one match (`tk (1)` to `tk (4)`), since letters
   cannot tell them apart: that gives 655 matches with 1,067 letter strings (headwords and listed variants; the
   signs se and ne are read both ways).
2. **The letters.** Consonants, the written vowels `e`, `i` and `o`, and one mark for a vowel at the start, as in
   the vowel run of the Egyptian search. An `a` inside a word is not written in Meroitic.
3. **The model** is the Egyptian search's (`egyptian.model`, `train`, `score`, the trie search), with Meroitic
   letters on both sides and the flat starting table of section 3. A headword's spelling becomes the variant's
   letter by letter: a letter stays, changes or drops, and a letter may be added. Three rounds of aligning and
   counting.
4. **An ending** is to an entry what the article is to an Egyptian word in that search: letters of the source that
   are not the word's own. Every word is read from its end, so that the ending comes first.
5. **Hiding.** A hidden variant is struck from every variant list, and an entry that has it as its headword goes
   with all it lists. The model is trained without every pair that has the hidden spelling on either side.
6. **Chance.** 1,000 made-up words of each length from 3 to 12 letters (12 and more together), built letter by
   letter as letters follow one another in the pool's headwords (seed 17). A word's chance is the share of the
   made-up words of its length whose best match is as good as its own, counting the word itself.
7. **A match with an accepted meaning.** The entry's level in the coverage map is a translated one. An entry whose
   meaning makes it a variant of another entry, or sends to one ("variant of ...", "see ..."), counts only when
   that entry counts, also when the meaning says more (`mloyose`, `Dk`).

**Limits.**

- The test set and the training set are one scholar's list of what is a variant. A change that Rilly never lists
  (`r` for `l`) is unknown to the model.
- The model counts in one direction, from the headword to the variant. Which of two spellings is the headword is
  the lexicon's choice.
- Letters cannot judge a short piece: 124 pieces were too short to search, and the 443 of three or four letters
  could be searched but hardly stand out.
- The made-up words are too easy a yardstick for long words (section 4, point 2).
- The checkers and the analysts of the coverage map are one model family, and the model has read the literature.
- The checkers' error rates rest on 12 controls and 12 decoys. One decoy more or less changes them a good deal.
- A pack hides the words that the map finds a piece in, not every word that holds its letters (section 5: three
  items).
- No specialist has read a confirmed piece.

## 8. Files

| File | What | Where |
|---|---|---|
| `src/variants.py`, `tests/test_variants.py` | the search and its checks | public |
| [`variants_candidates.tsv`](variants_candidates.tsv) | the 1,210 searched pieces: best match (headword and spelling), ending, letters that differ, chance | public (forms, no gloss) |
| [`variants_confirmed.tsv`](variants_confirmed.tsv) | the 48 pieces that both checkers confirmed, each with the word it is a spelling or a form of | public (forms, no gloss) |
| [`variants_brief.md`](variants_brief.md) | the checkers' brief | public |
| Rilly's lexicon, the gloss file of the coverage map | the pool and the contexts | local, `data/rilly2003/`, `data/sources/coverage/` |
| the result files, the checkers' packs, their answers and the key; the first pass that was set aside | drawn from the lexicon and the gloss file | local, `data/sources/variants/` |

To rebuild, with the local files in place: `python3 -I src/variants.py build` (about nine minutes the first time,
most of it the 10,000 made-up words; under a minute afterwards, while the kept scores still fit the pool and the
model), then `check` for the packs and `merge` for the checkers' answers. Packs whose folder holds answers are
not written again: `check` stops if it would change them.

## 9. Cost

The search itself is plain Python and used no subagent. The checkers took 1,269,219 subagent tokens in two
passes of six runs each, about three minutes a run: 657,132 for the first pass, which was set aside, and 612,087
for the second. The quote was about 0.7 million for one pass, with a second pass allowed for. The independent
review took 425,616 subagent tokens and 38 minutes, against about 0.45 million quoted; it found the three items of
section 5 and changed no result. That is 1,694,835 subagent tokens in all, against about 1.15 million quoted for
one pass and the review and about 1.8 million once the second pass was agreed.
