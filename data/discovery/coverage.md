# How much of the corpus can be translated today

Built on 2026-11-11 with `src/coverage.py`: every word of the 899 texts of `corpus_v5` was glossed from Claude
Rilly's 2003 lexicon, first by lookup and then, for the words the lookup leaves, by Claude Opus 5.5 analysts.
The numbers below are checked by `tests/test_coverage.py`.

## 1. Answer first

1. **About 60% of the running words can be translated today.** Of the corpus's 21,977 words, 13,292 (60.5%) are a
   name, a number or a word whose meaning or function Rilly's lexicon holds as established or probable. Counting
   near-copies of a text once, it is 5,266 of 8,786 words (59.9%).
2. **Another 17% have a proposal only, 10% are known by their kind only, and 12% are unknown.**
3. **Few texts are complete.** With near-copies counted once, 605 of the 608 texts have a word that is not lost.
   Every such word is translated in 82 of them, and one piece is missing in another 124. The median text has
   68.8% of its legible words translated.
4. **The gap is one long tail and a few frequent verbs.** 1,336 different pieces have no accepted meaning. The
   verbs of the benedictions stand first (`ḫr` blocks 116 texts, `ẖol` 70), 96 pieces stand in five texts or
   more, and 995 stand in a single text once near-copies are set aside.
5. **"Translated" here means word by word.** A text whose words are all translated is not thereby understood:
   the verb endings are mostly unexplained, and the count takes no account of syntax.

| Level | What it means | All 899 texts | Near-copies counted once |
|---|---|---|---|
| meaning | Rilly holds the meaning as established or probable | 6,955 (31.6%) | 2,720 (31.0%) |
| grammar | an ending or a function word with an accepted function | 1,968 (9.0%) | 1,013 (11.5%) |
| name | a person, a god, a place | 4,106 (18.7%) | 1,390 (15.8%) |
| number | a numeral | 263 (1.2%) | 143 (1.6%) |
| **translated** | **the four above** | **13,292 (60.5%)** | **5,266 (59.9%)** |
| hypothesis | Rilly gives a proposal only, or the analyst is unsure of the cut | 3,704 (16.9%) | 1,424 (16.2%) |
| kind | no meaning, but the kind of word is known (a title, a place, a verb of the benedictions) | 2,099 (9.6%) | 669 (7.6%) |
| unknown | neither | 2,620 (11.9%) | 1,165 (13.3%) |
| lost | a word with a lost sign | 262 (1.2%) | 262 (3.0%) |
| | all words | 21,977 | 8,786 |

By part of the corpus:

| Part | Texts | Words | Translated |
|---|---|---|---|
| The older corpus (Otten's, names masked) | 662 | 18,075 | 10,719 (59.3%) |
| Karanòg and Shablûl (Griffith 1911) | 151 | 2,911 | 2,158 (74.1%) |
| Griffith's other volumes | 86 | 991 | 415 (41.9%) |

Karanòg stands highest because its texts are epitaphs and because Griffith's own tables say which words are
names. Counted by different words instead of running words, 1,105 of 3,160 spellings (35.0%) are translated: the
frequent words are the known ones.

## 2. What blocks the most texts

The pieces without an accepted meaning, ranked by the texts they stand in (near-copies counted once). A piece is
a headword of Rilly's lexicon, or letters that no entry explains: an unknown piece of a word, or a whole word that
an analyst cut into known parts without being sure of the cut. "Alone" is the number of those texts in which the
piece is the only one still untranslated, so that its meaning would complete them. Names and function words are
left out of this table; the full list of 1,336 pieces is [`coverage_unknown.tsv`](coverage_unknown.tsv).

| Piece | Headword or letters | Kind | Level | Texts | Alone | Words | Spellings |
|---|---|---|---|---|---|---|---|
| `ḫr` | headword | verb | hypothesis | 116 | 11 | 183 | pSixrkes pSxrkete pSixrkete |
| `ẖol` | headword | verb | hypothesis | 70 | 4 | 84 | Xolkete pXolkete Xolkte |
| `pqr` | headword | title | hypothesis | 36 | 4 | 143 | pqr pqrleb terikelowipqr |
| `moke` | headword | kin term | unknown | 27 | 11 | 107 | mokelowi amXyemokelowi |
| `mde` | headword | verb | kind | 24 | 0 | 206 | mdetowi mde womsmdeto |
| `penn` | headword | noun | kind | 24 | 2 | 33 | penn penno penni |
| `tḫ (1)` | headword | verb | hypothesis | 23 | 0 | 52 | bSitkbxes txe txelo |
| `mr` | headword | noun | kind | 18 | 1 | 40 | mrs mr mlomrtowi |
| `s` | headword | noun | hypothesis | 18 | 1 | 24 | S swide Sleb |
| `yet (2)` | headword | noun | kind | 17 | 0 | 103 | yete yet yetete |
| `Si` | letters | unknown | unknown | 16 | 0 | 19 | Si dxeloSi qoreqoyeqoSi |
| `mlomrse` | headword | title | hypothesis | 16 | 0 | 16 | mlomrs mlomrsnlotelo mlomrtoxwi |
| `smlowi` | letters | kin term | hypothesis | 15 | 1 | 81 | smlowi |
| `teke` | headword | verb | hypothesis | 15 | 0 | 15 | teke ytekeS |
| `wetneyineqeli` | headword | epithet | hypothesis | 12 | 0 | 96 | wetNyiNqeli Nqeli wetNyi |
| `tbo` | headword | numeral or measure | hypothesis | 12 | 0 | 40 | tbo atbos tboyet |
| `temey (2)` | headword | noun | hypothesis | 12 | 1 | 19 | temey temeyye temeyli |
| `dole` | headword | adjective | kind | 12 | 0 | 18 | dole delekw doli |
| `yiroẖe` | headword | verb | hypothesis | 11 | 1 | 44 | yiroXetelowi yiroXetewi yiroXete |
| `trose` | headword | adjective | kind | 11 | 1 | 34 | tros ptros rot |

1. **Every piece has a kind where the texts show one:** 670 of the 1,336 pieces have a kind (title, noun, verb,
   name, epithet and so on), among them 29 of the first 30 in the list. A headword takes its kind from the
   lexicon, or, when the lexicon gives none, from the analysts (`moke`: a kin term). 144 of the 670 stay at the
   level unknown, because the analysts named their kind at confidence 3 or less in most of their words. The other
   666 mostly stand in a single text (539), 256 of them in the three royal texts (Tanyidamani, the Hamadab stela
   of Akinidad, Kharamadoye), where no formula places them.
2. **By level:** 302 pieces are headwords of the lexicon: 126 with a proposal in Rilly, 157 known by their kind
   only and 19 with neither. The other 1,034 are letters: 777 unknown pieces and 257 words that an analyst cut into
   known parts without being sure of the cut (the level hypothesis). A headword's level is the lexicon's, or that
   of the words it stands in when that is higher.
3. **The first two are the verbs of the bread and of the meal benedictions.** A meaning for `ḫr` alone would
   complete 11 texts.

## 3. How it was done

1. **The lookup** (`src/coverage.py`, `lookup`). A word that is a spelling of an entry of the lexicon takes that
   entry; so does a stem of three letters or more with one of 25 known endings, when Rilly gives the stem a
   meaning, a proposal or a name. A masked name is a name, and so is a word that Griffith's tables print as a name
   of its Karanòg inscription. The lookup alone translates 11,374 words (51.8%) and leaves 1,887 different words.
2. **The analysts.** Seventeen independent readers (Claude Opus 5.5) shared those words, about 115 each and the
   last 52, and two more read 230 of them a second time (point 4). Each got its words with up to four contexts,
   Rilly's entries as a table, and what Griffith prints about the word ([the brief](coverage_brief.md)). Each cut
   the word into parts (an entry of the lexicon, a name, a number or an unknown piece), named its kind and gave a
   confidence from 1 to 5. The script accepts an answer only if its parts spell the word and its entries exist:
   none of the 2,117 answers (1,887 and the 230 read again) failed.
3. **The level of a word.** A word counts as translated when every part that is a word of its own is a name, a
   number or an accepted entry, and the analyst's confidence is 4 or 5. An ending or a prefix whose function is
   open does not lower the level: `terikelowi` is "begotten by" whatever its `t-` does. The analysts add 1,918
   translated words (8.7%).
4. **A second analyst** read 230 words again without seeing the first: the most frequent of the first 1,835
   words the lookup left. The last 52, left once a stem needed a meaning before it could take an ending (among
   them `Sklte`, 213 times, and `mokelowi`, 103), were read once. Where the two differ in level, the lower level
   stands.
5. **Near-copies.** The older corpus holds families of near-copies (one family, the 86 texts that hold
   `aribet yete kemxr yetmdelowi`, is 6,284 of its 18,075 words). Going from the longest text down, a text is a
   copy when four fifths of its runs of three words stand in one text already kept. That leaves 608 of the 899
   texts.

An example, the first eleven words of Kar. 12 (13 of its 16 words are translated), as the gloss file has them:

| Word | Level | Gloss |
|---|---|---|
| `woSi` | name | Isis +i |
| `Soreyi` | name | O Osiris |
| `qo` | grammar | this one |
| `tbitolyeqowi` | name | this is Tbitolye |
| `pideyetedxelo` | meaning | is the child borne by Pideye |
| `yiboyeterikelo` | meaning | it is the one begotten of Yiboye |
| `mlN` | kind | administrative title tied to the viceroy's |
| `pestolito` | meaning | is (mlne) of the viceroy |
| `ato` | meaning | water |
| `mxe` | meaning | abundant |
| `piSoX` | meaning | may (he) give to drink |

The draft translation of a text is this line of glosses, word by word, not English prose.

## 4. How far to trust it

1. **The two analysts agree on the level of 194 of the 230 words read twice (84%),** and on the same cut as well
   for 178. On translated or not they agree for 218 (95%). Of the 66 words the first put at a translated level, the
   second did too for 58, and of the second's 62, the first for 58. So about one in ten of the words that one
   analyst alone called translated would not be confirmed by a second: 464 of the 13,292 translated words rest
   on one analyst.
2. **The lexicon's levels were checked against a later, independent source.** Rilly's 2016 overview
   ([UCLA Encyclopedia of Egyptology](https://escholarship.org/uc/item/3128r3sw)) lists 39 words with a
   translation. Our typed lexicon holds 34 of them at an accepted level. Four are proposals in the lexicon
   (`pqr` "prince", `wide` "brother", `nbr` "gold", `sr`/`asr` "meat, animal") and one (`ḫre` "meal") is not
   found. Counting the four as accepted would move 186 words, to 61.3%.
3. **What the figure leans on, among the 13,292 translated words:**
   - 1,376 have a spelling that two entries share, one of them without an accepted meaning (`s`, `li`, `te`): the
     figure takes the accepted one;
   - 995 are titles or epithets whose entry says no more than "a priestly title of …";
   - 694 are read through a spelling variant that the analyst asserts (`Sore` for `Sori`);
   - 910 have an ending or a prefix whose function is open: 840 in the analysts' cuts, and 70 that the lookup
     cut into a stem and an ending (`-ye`, `-w`, `-wi`, `-kete`) whose entries give it no accepted function;
   - 109 more take an ending that the lexicon has no suffix entry for (`-lis`, `-se`, `-yi`, `-tel`, `-teli`,
     `-b`, `-bx`), so whether its function is open is not known.
4. **What it cannot show.** No specialist has checked a line. The analysts are one model family, and the model
   has read the literature, though the brief forbids raising a confidence above 3 on memory alone. The lexicon is
   the state of 2003. A word with two accepted entries (`at`, bread or priest) is counted as translated without
   choosing between them. Word division in the older corpus is uneven, so some "words" are halves of words.

## 5. Files and rebuild

| File | What it holds | Where |
|---|---|---|
| `src/coverage.py` | the lookup, the packs for the analysts, the merge, the figures and the ranked list | public |
| `tests/test_coverage.py` | 18 checks: the method on a made-up lexicon, and the numbers and tables of this page | public |
| `data/discovery/coverage_brief.md` | the analysts' brief | public |
| `data/discovery/coverage_unknown.tsv` | the 1,336 pieces without an accepted meaning: headword or letters, kind, level, texts, words, spellings | public |
| `data/sources/coverage/glosses.jsonl` | every text word by word: gloss, level, confidence, source (Rilly's page), parts, and a draft line | local |
| `data/sources/coverage/packs/` | the analysts' packs and answers | local |

The gloss file and the analysts' answers lean on Rilly's lexicon, which has no open licence, so they stay on the
author's machine like the lexicon itself (README, Data). With those files in place:

```
python3 -I src/coverage.py first                                       # the lookup alone
python3 -I src/coverage.py build data/sources/coverage/packs --public  # the merge, the figures, the lists
python3 -I tests/test_coverage.py
```

## 6. Cost

Nineteen analyst runs took 2.63 million subagent tokens. Eighteen ran side by side on 2026-11-11, from about 10:33
until between 10:36 and 10:39; the last (the 52 words) ran from about 10:43 to 10:46. The whole build took about
25 minutes, from about 10:27 to the commit at 10:52, against a quote of about 2 hours and 2 to 3 million tokens.
The main session's own tokens are not counted here.
