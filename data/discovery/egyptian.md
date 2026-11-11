# Can a search by sound find the Egyptian word behind a Meroitic one?

Built on 2026-11-11 with `src/egyptian.py`. A scorer that knows only letters searched two open word lists, the
lemmata of the TLA's Demotic sentences and the Comprehensive Coptic Lexicon, for the source of Meroitic words: first
for the loans whose source is known, each one hidden in turn, then for the pieces of the
[coverage map](coverage.md) that have no accepted meaning. The numbers below are checked by
`tests/test_egyptian.py`.

## 1. Answer first

1. **For titles and nouns, no.** The bar was set before the run: the true source among the five best candidates
   for most of the 14 known loans that are titles, nouns or verbs. The search reached it for 4 of the 14 (6 are
   among the ten best), and 3 of the 14 have no source in the two lists at all.
2. **For the names of gods and places, yes.** When a name is searched among the Demotic names of its own kind,
   the true source is among the three best for all 10 names that have one there, and first for 7.
3. **A good match in sound does not tell a loan from a look-alike.** The best match of a known title or noun is
   better than the best match of 95% of made-up Meroitic words for 2 of 11 loans in the wide pool and for none in
   the narrow one. A real loan mostly looks no more Egyptian than a made-up word does.
4. **No piece without a meaning has an Egyptian candidate that stands above chance.** Of the 383 pieces searched,
   22 (narrow pool) and 26 (wide pool) beat the 5% bar, where 19 are expected by chance, and none passes the bar
   that allows for 383 tries. Two independent checkers read the 33 best matches blind, mixed with 12 decoys: they
   found no new source, rejected every decoy and agreed on all 45.
5. **What the search did find is old.** 16 pieces of the list are spellings or forms of words that the lexicon
   already links to Egyptian, as a loan or as a proposal (`prSn` for `plsn`, `petmoS` for `pelmos`, `amn` for
   `Amni`), and the Demotic list holds graffiti of Meroitic officials at Philae that spell Meroitic titles in
   Demotic (`qrny` for `qorene`, `ꜣrbtgꜥyꜣ` for `arebetke`).
6. **Not done.** The step named two more Egyptian parallels. The oracular decrees were not compared, because
   neither list holds Egyptian texts of that kind. The people whom the Philae graffiti and the Meroitic texts both
   name were not matched, because the Demotic file comes as single sentences without their texts and the older
   Meroitic corpus masks its names.

## 2. The test on the known loans

The answer key is the 35 entries of Rilly's 2003 lexicon that he holds as established or probable and that two
independent readers both took as borrowings into Meroitic: 14 titles, nouns and verbs and 21 names. For 24 of
them the source word stands in the lists (11 and 13). Each was searched with a model trained on the other loans
only. "Place" is the number of candidates that score as well as the true source or better, so ties count
against it. "Narrow" is the pool of the word's own kind, "wide" adds the neighbouring kinds (section 5).

| Meroitic | Kind | Source in the lists | Place, narrow | Place, wide | Place, all 16,943 |
|---|---|---|---|---|---|
| `plsn` | title | Demotic `mr-šn`, Coptic ⲗⲁϣⲁⲛⲉ | 7 of 310 | **1** of 9,405 | 1 |
| `ḫrpḫe` | verb | Demotic `ḫrp` | **1** of 3,683 | **1** of 3,683 | 4 |
| `pelmos` | title | Demotic `mr-mšꜥ`, Coptic ⲗⲉⲙⲏⲏϣⲉ | **4** of 310 | **3** of 9,405 | 4 |
| `kisri` | title | Coptic ⲕⲁⲓⲥⲁⲣ, Demotic `Gysrs` | not a title there | **4** of 9,405 | 4 |
| `tewiseti` | noun | Coptic ⲟⲩⲁϣⲧⲉ, ⲟⲩⲱϣⲧ | 6 of 9,095 | 6 of 9,405 | 13 |
| `ant` | title | Demotic `ḥm-nṯr`, Coptic ϩⲟⲛⲧ | 9 of 310 | 7 of 9,405 | 12 |
| `qelile` | noun | Coptic ⲕⲗⲁⲗ | 15 of 9,095 | 15 of 9,405 | 18 |
| `perite` | title | Demotic `rd`, Coptic ⲣⲏⲧ | not a title there | 24 of 9,405 | 38 |
| `apote` | title | Demotic `wp(y)ṱ` | not a title there | 101 of 9,405 | 162 |
| `yirewke` | noun | Coptic ⲉⲓⲟⲟⲣ, ⲉⲓⲉⲣⲟ, Demotic `yr` | 213 of 9,095 | 222 of 9,405 | 434 |
| `peseto` | title | Demotic `sꜣ-nsw` | 43 of 310 | 3,121 of 9,405 | 5,424 |
| `adb`, `atẖe`, `ḫrpḫne` | noun, noun, title | not in the lists | | | |

Among the five best: 2 of 14 in the narrow pool, 4 of 14 in the wide pool. Among the ten best: 5 and 6.

The names:

| Meroitic | Kind | Source in the lists | Place, narrow | Place, wide (all names) |
|---|---|---|---|---|
| `Amni` | god | `Ꞽmn` | 1 of 251 | 1 of 1,777 |
| `Ar` | god | `Ḥr` | 1 of 251 | 2 of 1,777 |
| `Asori` | god | `Wsꞽr` | 1 of 251 | 7 of 1,777 |
| `Atri` | god | `Ḥ.t-ḥr` | 1 of 251 | 2 of 1,777 |
| `Ḫs` | god | `Ḫnsw` | 1 of 251 | 1 of 1,777 |
| `Mnp` | god | `Ꞽmn-ꞽpy` | 2 of 251 | 2 of 1,777 |
| `Wos` | god | `Ꜣs.t` | 3 of 251 | 8 of 1,777 |
| `Arome` | place | `Hrm(e)` | 1 of 277 | 1 of 1,777 |
| `Pilqe` | place | `Pr-ꞽw-lq` | 2 of 277 | 3 of 1,777 |
| `Pẖome` | person | `Pꜣ-ꜥẖm` | 1 of 1,249 | 1 of 1,777 |

Three more names have a source in the lists that is tagged there as a common noun (`Note`, `Beke`, `Bkeli`), and
eight have none (`Amnb`, `Amnbse`, `Amnote`, `Atiye`, `mkesemene`, `Sye`, `Tebwe`, `Beqe`).

Why the names work and the titles do not: a pool of 251 gods holds few look-alikes, a pool of 9,405 nouns and
titles holds many, and three or four consonants cannot single out one word among thousands. The titles also
changed more on the way: `peseto` and `sꜣ-nsw` share one consonant.

**Is the best match better than chance?** For each loan, the score of its best candidate was compared with the
best scores of 300 made-up words of the same length (section 5). A loan "beats the bar" when at most 5% of the
made-up words do as well.

| Group | Loans compared | Beat the bar, narrow | Beat the bar, wide |
|---|---|---|---|
| Titles, nouns, verbs | 11 | 0 | 2 (`pelmos`, `peseto`) |
| Names of three letters or more | 8 | 3 (`Amni`, `Arome`, `Pilqe`) | 1 (`Arome`) |

`peseto` beats the bar with a wrong word: its best match is not its source. So the search can rank the candidates
of a word that is known to be a loan, but it cannot say which words are loans.

Two smaller sets, not part of the bar:

- **Proposals of the literature.** 24 entries carry an Egyptian source that is proposed, not accepted. The
  proposed word's letters stand in the narrow pool for 8 of them and in the wide pool for 11, and the search puts
  it among the five best for 4 and for 2 (`amero` with the Demotic `ꜥmr`, a baker of Isis at Philae, is first
  among the titles). This says that the search often sees what a scholar's eye saw, not that the proposals are
  right.
- **Meroitic words written in Egyptian letters.** 30 entries are Meroitic names and titles that Egyptian texts
  spell. Three of those spellings stand in the pools, and the search puts all three among the five best
  (`ꜣrbtgꜥyꜣ` for `arebetke` and `qrnyꜣ` for `qorene` are first among the titles).

## 3. The pieces without a meaning

The coverage map lists 1,336 pieces without an accepted meaning. 608 of them have a kind that the pools know (a
title, a noun, a name, a verb, an adjective). 166 of those were not searched: 165 have fewer than three consonants,
so that anything fits them, and one (`2w`) is a number with a letter. Of the 442 searched, 59 are already linked to Egyptian in the lexicon (48 are entries that
mention it, 11 are spelled like such an entry), which leaves 383.

| | Narrow pool | Wide pool |
|---|---|---|
| Pieces whose best match beats the 5% bar | 22 | 26 |
| Expected by chance (5% of 383) | 19 | 19 |
| Pieces that pass the bar for 383 tries (Benjamini and Hochberg, a fifth of the passes allowed to be chance) | 0 | 0 |

The made-up words are a fair yardstick: the 64 Meroitic words that have an accepted meaning and no Egyptian link
beat the 5% bar 0 to 5 times, depending on the pool, where 3 are expected.

Every searched piece is in [`egyptian_candidates.tsv`](egyptian_candidates.tsv) with its best match in both pools
and the share of made-up words that do as well. Read it as a list of look-alikes, not of sources.

## 4. The check of the best matches

The 33 pieces that beat the bar in either pool went to two Claude Opus 5.5 checkers, each on its own, with the
piece's contexts, Rilly's entry and the three best candidates of each pool with their meanings or example
sentences ([the brief](egyptian_brief.md)). 12 decoys were mixed in unmarked: pieces whose best match at least
half of the made-up words equal.

| Verdict | Checker 1 | Checker 2 | Both |
|---|---|---|---|
| No candidate is supported | 27 | 27 | 27 |
| A form of a word whose Egyptian source is known | 5 | 5 | 5 |
| A candidate fits | 1 | 1 | 1 |
| Decoys accepted | 0 of 12 | 0 of 12 | |

- **The five known words:** `prSn` is `plsn` (the temple administrator) with r for l, `petmoS` is `pelmos` (the
  general), `pertese` is `perite` (the agent) with the ending -se, `stol` is the second half of `pestol`, a form
  of `peseto` (the viceroy), and `menote` after `ant` is the priest's god, Amun of Thebes. The checkers knew
  these words from the contexts and from memory, not from the search: the true source was among the candidates
  shown for one of the five (`mr-šn` for `prSn`), and a compound of it for one more (`rd-(n-)Ꜣs.t`, the agent of
  Isis, for `pertese`).
- **The one fit:** `aribet`, a title, with the Demotic `ꜣrbtgꜥyꜣ`. Both checkers note that this is the Meroitic
  title `arebetke` as a graffito at Philae spells it, that Rilly's entry already gives Török's link between the
  two titles, and that it is no Egyptian source.

The checkers have read the literature, as every model has, so a "known" verdict leans on memory as well as on the
pack. What the decoys show is that they did not accept look-alikes.

## 5. Method

1. **The pools.** 5,660 lemmata of the TLA's 13,383 Demotic sentences, each with the kinds its tokens are tagged
   as (a tenth of the tokens or more: 310 titles, 251 gods, 277 places, 1,249 persons), and the 11,283 entries of
   the Comprehensive Coptic Lexicon, Greek loans in Coptic included. The Demotic lemmata have no meanings.
2. **One alphabet.** Every form is reduced to its consonants: a Meroitic word to its consonants and a mark for a
   vowel at the start; a Demotic lemma with and without its bracketed and dotted endings; a Coptic entry in each
   dialect form, with ϩ as h, ϣ as š and the glides read from ⲟⲩ and ⲉⲓ. Vowels are not compared.
3. **The model.** An Egyptian word becomes a Meroitic one letter by letter: a letter is kept, changed or dropped,
   and a letter may be added. The chances start from a neutral table (a consonant most often stays what it is,
   h, ꜣ, y and w drop easily) and are counted again from the aligned known loans, three rounds. The Egyptian word
   may carry its article p or t; how often is counted from the same loans. What it learned from the 24 loans:
   Egyptian h and ḥ give a Meroitic vowel at the start or nothing, š gives s, n drops in one case of five, and a
   fifth of the loans carry the article p.
4. **The test.** A loan is searched with a model trained without it and without any loan that shares its source.
5. **Pools by kind.** Narrow and wide: a title among the Demotic titles, then among titles and nouns; a god,
   place or person among the Demotic names of that kind, then among all names; a noun among nouns, then nouns and
   titles; a verb among verbs.
6. **Chance.** 300 made-up words of each length, built letter by letter as letters follow one another in the
   headwords of the lexicon (seed 17). The share of them whose best match is as good as a word's own, counting
   the word itself, is that word's chance.

**Limits.**

- The source entries of the 24 loans were picked by hand from the lists, each checked against the German
  translation of a sentence or the Coptic meaning (`key_sources.json`, local).
- The Demotic list is the vocabulary of one sample of sentences, not a dictionary: 11 of the 35 loans have no
  source in either list.
- The answer key, the two readers who labelled it and the checkers all go back to one lexicon and one model
  family.
- The scorer is simple. A better one might move single places; it would not change that a pool of thousands holds
  many words with the same three consonants.

## 6. Files

| File | What | Where |
|---|---|---|
| `src/egyptian.py`, `tests/test_egyptian.py` | the search and its checks | public |
| [`egyptian_candidates.tsv`](egyptian_candidates.tsv) | the 442 searched pieces, best match and chance in both pools | public, CC BY-SA 4.0 (it holds lemma numbers and forms of the two lists) |
| [`egyptian_brief.md`](egyptian_brief.md) | the checkers' brief | public |
| the two word lists | `Comprehensive_Coptic_Lexicon-v1.2-2020.xml` from [KELLIA's dictionary](https://github.com/KELLIA/dictionary) and `train.jsonl` from [the TLA's Demotic sentences](https://huggingface.co/datasets/thesaurus-linguae-aegyptiae/tla-demotic-v18-premium), both CC BY-SA 4.0 | local, `data/sources/egyptian/` |
| the answer key, the result files, the checkers' pack and answers | drawn from Rilly's lexicon and the gloss file | local, `data/sources/egyptian/` |

A `ccl:` number opens in the [Coptic Dictionary Online](https://coptic-dictionary.org/entry/C1725) (the link is
the entry of ⲗⲁϣⲁⲛⲉ; put another number in its place). A `tla:` number is a lemma of the
[Thesaurus Linguae Aegyptiae](https://thesaurus-linguae-aegyptiae.de/).

To rebuild, with the local files in place: `python3 -I src/egyptian.py build` (about four minutes), then
`check` and `merge` for the checkers' pack and answers.

## 7. Cost

The two readers of the answer key took 364,923 subagent tokens, the two checkers 249,072. The search itself is
plain Python and runs in four minutes.
