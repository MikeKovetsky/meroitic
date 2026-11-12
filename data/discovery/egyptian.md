# Can a search by sound find the Egyptian word behind a Meroitic one?

Built on 2026-11-11 with `src/egyptian.py`. A scorer that knows only letters searched two open word lists, the
lemmata of the TLA's Demotic sentences and the Comprehensive Coptic Lexicon, for the source of Meroitic words: first
for the loans whose source is known, each one hidden in turn, then for the pieces of the
[coverage map](coverage.md) that have no accepted meaning. The numbers below are checked by
`tests/test_egyptian.py`.

## 1. Answer first

1. **For titles and nouns, no.** The bar was set before the run: the true source among the five best candidates
   for most of the 14 known loans that are titles, nouns or verbs. The search reached it for 4 of the 14 when
   titles and nouns are searched together (the wide pool) and for 2 among the words of their own kind alone (6 and
   5 are among the ten best), and 3 of the 14 have no source in the two lists at all.
2. **For the names of gods, places and people, yes.** When a name is searched among the Demotic names of its own
   kind, the true source is among the three best for all 10 names that have one there (seven gods, two places and
   a person), and first for 7.
3. **A good match in sound does not tell a loan from a look-alike.** The best match of a known title or noun is
   better than the best match of 95% of made-up Meroitic words for 2 of 11 loans in the wide pool and for none in
   the narrow one. A real loan mostly looks no more Egyptian than a made-up word does.
4. **No piece without a meaning has an Egyptian candidate that stands above chance.** Of the 383 pieces searched,
   22 (narrow pool) and 26 (wide pool) beat the 5% bar, where 19 are expected by chance: chance alone gives as
   many or more 28% and 7% of the time. None passes the bar that allows for 383 tries, but that bar could hardly
   pass one: with 300 made-up words no chance is below 1 in 301, while the bar asks the best piece for 1 in 1,915,
   so a piece could pass it only with six others at that floor. Two independent checkers read the 33 best matches
   blind, mixed with 12 decoys: they found no new source, rejected every decoy and agreed on all 45.
5. **What the search did find is old.** At least 16 pieces of the list are spellings or forms of words that the
   lexicon already links to Egyptian, as a loan or as a proposal: 11 are spelled like such a word (`amn` for
   `Amni`), and the checkers recognised 5 more among the 33 they read (`prSn` for `plsn`, `petmoS` for `pelmos`).
   And the Demotic list holds graffiti of Meroitic officials at Philae that spell Meroitic titles in Demotic
   (`qrnyꜣ` for `qorene`, `ꜣrbtgꜥyꜣ` for `arebetke`).
6. **Comparing the vowels too ranks better and decides nothing new** (section 5, added after the question whether
   spelling would do more than consonants). On the Coptic entries, the true source is among the five best for 7 of
   the 13 loans that have a Coptic source, against 4 by consonants alone, and for 6 of the 14 titles, nouns and
   verbs of the bar. But the best match of a known loan still does not stand out from made-up words (1 of 11),
   and the pieces without a meaning stay at chance.
7. **Not done.** The step named two more Egyptian parallels, and both are still open. The oracular decrees were
   not compared, because neither list holds Egyptian texts of that kind. The people whom the Philae graffiti and
   the Meroitic texts both name were not matched, because the Demotic file comes as single sentences without their
   texts and the older Meroitic corpus masks its names. An earlier run set six groups of Meroitic texts from Philae
   and the Dodecaschoenus beside Demotic and Greek ones, from the editions and the literature
   ([`philae.md`](philae.md)); this search adds nothing to that.

## 2. The test on the known loans

The answer key is the 35 entries of Rilly's 2003 lexicon that he holds as established or probable and that two
independent readers both took as borrowings into Meroitic: 14 titles, nouns and verbs and 21 names. For 24 of
them the source word stands in the lists (11 and 13). Each was searched with a model trained on the other loans
only. "Place" is the number of candidates that score as well as the true source or better, so ties count
against it. "Narrow" is the pool of the word's own kind, "wide" adds the neighbouring kinds (section 6).

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
best scores of 300 made-up words of the same length (section 6). A loan "beats the bar" when at most 5% of the
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
- **Meroitic words written in Egyptian letters.** 30 entries are Meroitic names, titles and nouns that Egyptian
  texts spell. Three of those spellings stand in the pools, and the search puts all three among the five best
  (`ꜣrbtgꜥyꜣ` for `arebetke` and `qrnyꜣ` for `qorene` are first among the titles).

## 3. The pieces without a meaning

The coverage map lists 1,336 pieces without an accepted meaning. 608 of them have a kind that the pools know (a
title, a noun, a name, a verb, an adjective). 166 of those were not searched: 165 have fewer than three letters as
the search writes them (consonants, and one mark for a vowel at the start), so that anything fits them, and one
(`2w`) is a number with a letter. Of the 442 searched, 59 are set aside: 48 are entries of the lexicon that
mention Egyptian, Demotic, Coptic, Greek or Latin (as a source, a proposal, a spelling in Egyptian letters, a
rejected link or for another reason), and 11 are spelled like an entry that the lexicon links to Egyptian. That
leaves 383.

| | Narrow pool | Wide pool |
|---|---|---|
| Pieces whose best match beats the 5% bar | 22 | 26 |
| Expected by chance (5% of 383) | 19 | 19 |
| How often chance alone gives as many or more | 28% | 7% |
| Pieces that pass the bar for 383 tries (Benjamini and Hochberg, a fifth of the passes allowed to be chance) | 0 | 0 |

The last row says little here. The chance of a piece cannot be smaller than 1 in 301 (it counts the piece among
300 made-up words), while that bar asks the best of 383 pieces for 1 in 1,915: a piece could pass it only together
with six others at that floor. The answer of section 1 rests on the row above it.

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

## 5. The same search with the vowels compared

Sections 2 to 4 compare consonants only. This run, made the same day, compares the written vowels too. The Demotic
list writes none, so it is on the Coptic entries alone: a Meroitic word keeps its e, i and o (a is written at the
start of a word only), a Coptic form keeps its vowels in four classes (ⲁ; ⲉ and ⲏ; ⲓ and ⲉⲓ; ⲟ, ⲱ, ⲟⲩ and ⲩ), and
the model counts a vowel like any other letter. The sign ne writes its e. The e of the sign se is compared only
where the spelling writes it as a letter of its own: a headword is taken in a spelling that writes se as s and e,
but in a piece taken from the texts the corpus's s is the sign se in the funerary texts and in Griffith's rows and
the plain s in the royal narratives, so it counts as s. The made-up words
are drawn as in section 6, from the headwords with their vowels: 300 of each length from 3 to 12 letters (12 and
more together), vowels counted, each with three consonants or more. A title or a noun is searched among the 7,139
Coptic nouns, a verb among the 2,946 verbs.

**The test.** 13 of the known loans have a Coptic source: 8 titles and nouns, and 5 names whose source the
lexicon lists as a noun. Each was hidden in turn, as before. "Consonants" is the same search in the same pool
without the vowels, with a model trained on the same 13 loans, so the two columns differ in the vowels only (and
differ from section 2, where the pool also holds the Demotic lemmata).

| Meroitic | Coptic source | Place by consonants | Place with vowels |
|---|---|---|---|
| `plsn` | ⲗⲁϣⲁⲛⲉ | 1 | 1 |
| `tewiseti` | ⲟⲩⲁϣⲧⲉ, ⲟⲩⲱϣⲧ | 2 | 1 |
| `Asori` | ⲟⲩⲥⲓⲣⲉ | 3 | 2 |
| `kisri` | ⲕⲁⲓⲥⲁⲣ | 4 | 3 |
| `ant` | ϩⲟⲛⲧ | 6 | 5 |
| `perite` | ⲣⲏⲧ | 13 | 5 |
| `qelile` | ⲕⲗⲁⲗ | 14 | 5 |
| `Beke` | ⲃⲏϭ | 11 | 6 |
| `Pẖome` | ⲁϩⲱⲙ | 17 | 8 |
| `Atri` | ϩⲁⲑⲱⲣ | 9 | 13 |
| `pelmos` | ⲗⲉⲙⲏⲏϣⲉ | 6 | 16 |
| `yirewke` | ⲉⲓⲟⲟⲣ, ⲉⲓⲉⲣⲟ | 159 | 35 |
| `Wos` | ⲏⲥⲉ | 108 | 192 |

Among the five best of 7,139 nouns: 4 of 13 by consonants, 7 of 13 with vowels. Among the ten best: 7 and 9. Nine
loans move up, three move down (`Atri`, `pelmos` and `Wos`, whose vowels changed on the way into Meroitic) and
one stays.

**Against the bar of section 1.** With vowels, 6 of the 14 titles, nouns and verbs have their source among the
five best; by consonants it was 4. The two searches find different loans: the five best of both together, up to
ten candidates a loan, hold the source for 8 of the 14. That is ten candidates and not five, so the bar is not
reached.

**Against chance.** The best match of a known loan beats the best matches of 95% of made-up words for 1 of the 11
loans compared (`pelmos`, with a word that is not its source). The made-up words are a fair yardstick at that
bar: of the 64 Meroitic words with an accepted meaning and no Egyptian link, 2 beat the 5% bar among the nouns
where 3 are expected. They are a little lenient further up, where 17 beat a 20% bar and 13 are expected.

**The pieces without a meaning.** 278 titles, nouns, verbs and adjectives were searched (names are left out: the
Coptic lexicon holds few). 37 are set aside as in section 3, which leaves 241.

| | With vowels, Coptic entries |
|---|---|
| Pieces whose best match beats the 5% bar | 13 |
| Expected by chance (5% of 241, by the made-up words) | 12 |
| Expected at the rate of the 64 native words in each piece's pool (2 of 64 among the nouns, 3 of 64 among the verbs) | 8 |
| How often chance alone gives 13 or more, by the made-up words | 43% |
| Pieces that pass the bar for 241 tries | 0 (it needs five pieces at the smallest chance) |

So 13 is what chance gives. Every searched piece is in
[`egyptian_candidates_vowels.tsv`](egyptian_candidates_vowels.tsv).

**The check.** For seven of the 13, the first checkers had already been shown the word that is the best match
with vowels (`prSn`, `petmoS`, `pertese` and `stol` among them: the forms of known loans of section 4). The other
six went to two new checkers, blind, with six decoys: `lks`, `mtr`, `ponni`, `ptri`, `tereki` and `tmNte`. Both
answered "no candidate is supported" for all 12: no new source, no decoy accepted.

An earlier run of this section left out the e of the sign ne. It had 18 pieces under the bar, and its two
checkers said no to nine of them and to six decoys. The review found the slip; the numbers above are after the
fix, and the earlier pack and its answers are kept locally and counted nowhere.

## 6. Method

1. **The pools.** 5,660 lemmata of the TLA's 13,383 Demotic sentences, each with the kinds its tokens are tagged
   as (a tenth of the tokens or more: 310 titles, 251 gods, 277 places, 1,249 persons), and the 11,283 entries of
   the Comprehensive Coptic Lexicon, Greek loans in Coptic included. The Demotic lemmata have no meanings.
2. **One alphabet.** Every form is reduced to its consonants: a Meroitic word to its consonants and a mark for a
   vowel at the start; a Demotic lemma with and without its bracketed and dotted endings; a Coptic entry in each
   dialect form, with ϩ as h, ϣ as š and the glides read from ⲟⲩ and ⲉⲓ. Vowels are not compared (section 5
   compares them).
3. **The model.** An Egyptian word becomes a Meroitic one letter by letter: a letter is kept, changed or dropped,
   and a letter may be added. The chances start from a neutral table (a consonant most often stays what it is,
   h, ꜣ, y and w drop easily) and are counted again from the aligned known loans, three rounds. The Egyptian word
   may carry its article p or t; how often is counted from the same loans. What it counted from the 24 loans:
   Egyptian h and ḥ (one letter for the search) give the mark of a vowel at the start all 4 times, š gives s all
   3 times, n is dropped 2 times in 7, and 4 loans carry the article p and 1 the article t.
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

## 7. Files

| File | What | Where |
|---|---|---|
| `src/egyptian.py`, `tests/test_egyptian.py` | the search and its checks | public |
| [`egyptian_candidates.tsv`](egyptian_candidates.tsv) | the 442 searched pieces, best match and chance in both pools | public, CC BY-SA 4.0 (it holds lemma numbers and forms of the two lists) |
| [`egyptian_candidates_vowels.tsv`](egyptian_candidates_vowels.tsv) | the 278 pieces of the vowel search, best match and chance | public, CC BY-SA 4.0 (lemma numbers and forms of the Coptic lexicon) |
| [`egyptian_brief.md`](egyptian_brief.md) | the checkers' brief (the sentence on the second pack was added for its checkers) | public |
| the two word lists | `Comprehensive_Coptic_Lexicon-v1.2-2020.xml` from [KELLIA's dictionary](https://github.com/KELLIA/dictionary) and `train.jsonl` from [the TLA's Demotic sentences](https://huggingface.co/datasets/thesaurus-linguae-aegyptiae/tla-demotic-v18-premium), both CC BY-SA 4.0 | local, `data/sources/egyptian/` |
| the answer key, the result files, the checkers' two packs and their answers | drawn from Rilly's lexicon and the gloss file | local, `data/sources/egyptian/` |

A `ccl:` number opens in the [Coptic Dictionary Online](https://coptic-dictionary.org/entry/C1725) (the link is
the entry of ⲗⲁϣⲁⲛⲉ; put another number in its place). A `tla:` number opens as a lemma of the Thesaurus
Linguae Aegyptiae, without the `tla:`: [d2527 is `mr-šn`](https://thesaurus-linguae-aegyptiae.de/lemma/d2527) (the
site asks for a short browser check first).

To rebuild, with the local files in place: `python3 -I src/egyptian.py build` (about three minutes), then
`check` and `merge` for the checkers' pack and answers; `vowels` (about eleven minutes), then `check vowels` and
`merge vowels` for section 5. A pack whose folder holds the checkers' answers is not written again: `check`
compares it with what the build gives and stops if it would change.

## 8. Cost

The two readers of the answer key took 364,923 subagent tokens, the two checkers 249,072 and one web check about
8,000: about 0.62 million, against about 1 million estimated beforehand; its review took 401,989 more. The vowel
run of section 5 was estimated at about 0.5 million with its review and took more: 139,936 for the two checkers
of its first run, 446,695 for the review that found the slip in it, and 133,211 for the two checkers of the
corrected run, about 0.72 million before the reviewer's last look. The search itself is plain Python: three
minutes by consonants, eleven with vowels.
