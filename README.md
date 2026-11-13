# Meroitic with Opus 5.5

**Did we decipher anything? No.** No new reading of the Meroitic language survived checking. What is new is about
the data and the method: the public corpus turned out to be mostly copies, 303 inscriptions are now machine-readable
under an open licence (237 of them missing from that corpus), the obvious way to blind a test of AI on an
undeciphered script (scramble the letters) turned out not to work, and we built a test that does.

## What's new

1. **The public Meroitic corpus is mostly copies.** The only machine-readable corpus
   ([Otten & Anastasopoulos, ALP 2025](https://aclanthology.org/2025.alp-1.11/)) is a file of 18,090 lines that holds
   662 different texts or phrases: each one is repeated, about 27 times on average, with only a person's name
   changed. For example, the short label `tdxe mlEqErebr qEret ___` appears 198 times, once with each of 198 names
   (`…aplXye`, `…pqebete`, `…msxte trEbit`, …). Anyone counting words in the file counts the same text over and over:
   some titles come out about 100 times more frequent than they are. The paper says so itself: it collected 871
   example texts and phrases (those quoted in Millet 1968 and Rilly 2007, Lobban's word list and three royal
   narratives) and swapped names to make 17,257 for training word vectors. What the paper does not say is that the
   file on GitHub, `mero-corpus.txt`, is that padded version (it has the 1,868 word forms the paper reports): the
   repository has no note saying so, and it holds the unpadded examples only in the per-scholar files the corpus was
   built from, with translations and page notes (`Data/MilletExamples.txt` and others), not as one corpus file. Our
   662 is lower than the paper's 871, probably because, with names masked, examples that differ only in a name count
   once; that was not checked. `src/pool.py` recovers the two swap pools (178 private and 11 royal names) from the
   data alone, and `src/dedup.py`, `src/collapse.py`, `src/clean_v2.py` undo it.
2. **303 inscriptions are now machine-readable under an open licence, 237 of them missing from the public corpus.**
   The model reads the Meroitic cursive type printed in Griffith's 1911–12 editions at 95.6% sign accuracy against
   the modern edition (99.6% against what Griffith printed), measured on 12 texts. The test covered cursive type
   only: about a third of the rows (48) are in hieroglyphic type, read with Griffith's sign table and not scored.
   It transcribed 152 inscriptions (29 only in part, as
   Griffith printed them) from *Meroitic Inscriptions* I–II and *Meroë*, public-domain editions, each row with its
   source page, site and object, and 127 with a REM number (`data/expansion/`, CC BY 4.0:
   [`LICENSE-DATA.md`](LICENSE-DATA.md)); 86 are not in the public corpus (+5% words). Griffith's hand copies it
   reads at 89% on their own, which is not enough. But his Karanòg volume prints most words of every inscription
   again in type, and with each reading checked against those pages it reaches 97.7% on the four texts that have a
   modern edition: 151 more inscriptions ([`data/expansion/karanog/`](data/expansion/karanog/README.md)), none of
   them in the public corpus (+15% words). A second reader of eleven of the 53 pages got 97.7% of the same signs.
   It can't read photographs of the stones (almost nothing).
3. **Scrambled-script "blind" tests don't work on a frontier model.** Given only a 17-word glossary of Meroitic
   re-spelled with a random letter swap, it broke the cipher and matched all 35 test words to their meanings; given the
   scrambled corpus with neutral labels, it recognised the opening formula "O Isis, O Osiris" and read the script from
   there. A test of AI decipherment on a known-but-undeciphered script has to assume the model has read the
   literature.
4. **A test that does work, and what it measures.** A synthetic twin language (same size and texture, every word
   invented): it recovered 41 and 43 of 52 meanings on two independent runs, where chance is about 2. And a
   recall-then-corpus test on Rilly's lexicon: of the words it could not recall, reading the corpus got it to the
   published meaning for 13 of 35 (20 within three guesses), scored by an independent judge.
5. **Its confidence is a usable filter.** Across every test, all 74 answers it gave at confidence 4 or 5 were right;
   at confidence 1 or 2, about a third were.
6. **It restores lost words better than statistics.** Where a masked word has no parallel anywhere in the texts, it
   restored 48% on the first guess against 26% for an n-gram model.
7. **Negative results worth knowing.**
   - With open word lists, Meroitic words show no resemblance to their Nubian-family equivalents beyond the about 20
     word series Rilly built his sound laws from (held-out p = 0.49): the lexical case for the family rests on those.
   - None of the 14 "new" readings the discovery runs proposed survived an adversarial literature check. Of the two
     partial leads left open, one got weaker and one held when tested on texts typed afterwards
     ([`REPORT.md`](REPORT.md)). Where the key books are print-only, the model can't tell a
     rediscovery from a discovery.
   - The British Museum's Hamadab stela (REM 1003) holds nothing checkable against the Roman war, as Rilly said in 2014.
   - A search by sound alone does not find the Egyptian word behind a Meroitic title or noun. Tested on the known
     loans, each hidden in turn, it puts the true source among the five best candidates for 4 of 14 titles, nouns
     and verbs, though for all 10 names of gods, places and people that have a source among the Demotic names of
     their kind it is among the three best. For the 383 pieces without a meaning it gives nothing above chance, and
     two blind checkers found no new source among its 33 best matches
     ([`data/discovery/egyptian.md`](data/discovery/egyptian.md)). Comparing the written vowels too, on the Coptic
     entries, ranks the true source better (among the five best for 7 of 13 loans, against 4) and leaves both
     answers as they are. Of the step's two other Egyptian parallels, the oracular decrees are not done yet; the
     people the Philae graffiti name in Demotic are (item 13).
8. **About 62% of the corpus's running words can be translated today, word by word.** Every word of the 899 texts
   was glossed from Rilly's 2003 lexicon, by lookup and then by analysts. After four corrections made the same day,
   13,618 of 21,977 words (62.0%) are a name, a number or a word with an accepted meaning or function (61.6% with
   near-copies counted once); 16% have a proposal only, 9% are known by their kind only and 11% are unknown.
   Every legible word is translated in 106 of 605 texts. The 1,304 pieces without an accepted meaning are listed
   with their kind and the texts they block. The map as first built gave 60.5%, 82 texts and 1,336 pieces; the
   difference is words it counted wrongly, not meanings found
   ([`data/discovery/coverage.md`](data/discovery/coverage.md)).
9. **A search by letters ranks the spellings of a known word well, and cannot say by itself which unknown pieces
   are one.** Each of the 242 spelling variants that Rilly's lexicon lists under a word was hidden in turn. The
   search brings 187 (77%) back to their own entry as the single best match and 232 (96%) among the three best.
   The bar set before the run also asked half of them to stand out from made-up words, and only 105 (43%) do:
   a word of three or four letters cannot, since a made-up word that short is too often a word of the lexicon
   letter for letter. So the test missed its bar. Of the 1,140 pieces without a meaning that the lexicon does
   not already link to a word, 82 beat the made-up words where 57 are expected, but known words that are nobody's
   variant beat them as often, so two blind checkers read all 105 matches under the bar, the 23 that the lexicon
   links itself included. Both confirmed 48, and 29 of those are new. 26 are a word with an accepted meaning and
   would move 59 running words of the coverage map, from 60.5% to 60.7% (54 words, still 60.7%, without the two
   whose packs showed a word with the piece's letters and its gloss). The check is careful and misses a lot:
   of 12 listed variants shown as if they were unknown, both checkers named the right entry for 6, and of 12
   shown with the right entry taken out, both accepted a look-alike for 1
   ([`data/discovery/variants.md`](data/discovery/variants.md)).
10. **Two printed editions give the map's meaning for 70% of the words they translate, and for 85% outside two
    words on which scholars differ.** The coverage map takes every meaning from one lexicon. For the 31
    inscriptions that Millet's article on Gebel Adda (2005) or *Fontes Historiae Nubiorum* III (1998) also
    print, independent judges compared our reading of each word with the edition's. Of the 537 words the map
    counts as translated there, the edition gives a meaning to 397 and the map's meaning to 276 (69.5%). Most of
    the gap is two words: `yetmde`, "nephew, niece" in the lexicon and "relative" in both editions, and `qo`,
    "this one" against Millet's "the noble". Outside them it is 259 of 304 (85.2%). On a quarter of the words the
    editions are silent. The check found a numeral typed as a letter in the older corpus and eleven names or
    pieces of words read as words, and almost no meaning that the map lacks: of 167 meanings the editions give,
    the sure ones on words without an accepted meaning in the map are mostly titles left untranslated, phrases
    whose words the map reads the same way, and proposals the lexicon already holds
    ([`data/discovery/experts.md`](data/discovery/experts.md)).
11. **The corpus keyed by inscription: 899 texts held 289 inscriptions.** Otten's padded file can be undone
    exactly from his own per-scholar files: of its 17,995 different lines, 340 are a line of those files and
    17,446 are such a line with one name swapped. Traced that way, 54.5% of the words of `corpus_v5` are copies of
    a reading with a name swapped, and the texts that stand for an inscription hold 30.0% of them. `corpus_v6`
    has one row per inscription, with the real names: 548 inscriptions, 259 of them new to the corpus (209 of the
    Newsletter's texts, kept locally, and 50 of Griffith's rows that `corpus_v5` left out). The table of all 563
    inscriptions is public, with every reading's source and licence and the text of the open ones: 441 have a REM
    number, 64 readings from two editions or more, 303 a reading under an open licence. Counted again on the
    inscriptions that were already in the corpus, the coverage map translates 60.0% of the words (62.0% before),
    and the two editions give its meaning for 71.4% of the words they translate (69.5% before). The matching rule
    missed the bar set for it (the right partner for 45 of 54 known pairs, where 90% was asked), so numbers
    decide before letters, and the 17 doubtful matches went to two readers. Both passed their own test (12 of 12 known lines, 12 of 12 decoys); 13 of their matches are taken,
    one line matches nothing and 3 are not settled ([`data/discovery/corpus_v6.md`](data/discovery/corpus_v6.md)).
12. **Analysts on the spellings nobody had read add 1.4 points, half of what was expected.** The clean corpus
    had 930 spellings (1,038 running words) that only the lookup had seen, most of them in the Newsletter's
    texts. Eight analysts read them, 110 of them twice: 125 spellings got a translated level (68 names, 55
    meanings, 2 grammar words), and 550 got nothing. 139 running words more are translated, 5,419 of 10,290
    (52.7%, from 51.3%). The two analysts put 105 of the 110 words read twice on the same side, above the bar of
    85%. The gain expected beforehand was 265 to 385 words: the unread words turned out to be pieces of words
    printed in two parts, and single words of broken or obscure texts
    ([`data/discovery/v6_readers.md`](data/discovery/v6_readers.md)).
13. **The same people in Demotic, Greek and Meroitic: four of them carry titles in two languages, and where the
    two texts give the same office the titles line up with the lexicon.** *Fontes Historiae Nubiorum* III prints
    22 Demotic graffiti and two Greek inscriptions from Philae, Dakka and Maharraqa, among them those of the
    families whose Meroitic epitaphs the corpus holds. Three readers listed the people (99, 21 of them in two
    entries or more) and the 125 places where the editors set a Meroitic word beside a word of another language or
    give it a meaning. `perite` stands where the Demotic has "agent" for two people and `peseto` where it has "the
    king's son" and the Greek `psentes` for one, the words the lexicon derives them from; `kroro` stands where the
    Demotic writes the same title, of unknown meaning, as `3krre` for one. Two judges agree with the map's reading
    on 36 of 58 and 41 of 57 of the lines whose word it translates. No meaning is both new and sure; what the map
    lacks is mostly titles the editors leave as titles too ([`data/discovery/demotic.md`](data/discovery/demotic.md)).
14. **A second scholar for 70 of the 177 entries the map leans on: 3,873 of the 10,290 running words (37.6%) rest
    only on meanings two scholars share.** Rilly's lexicon records what other scholars proposed for most of its
    entries. Two judges set 407 such proposals beside the lexicon's meaning, without the scholar's name and with
    decoys (kappa 0.92 on "same or not"; 2 of 82 decoys accepted); with the editors' readings of item 10, 70
    entries are agreed by two scholars, 23 disputed (`qo`, `l` "to give", `mlo` and `mte` lead), 59 stated by one
    and 25 only proposed. One lexicon translates 5,419 of the running words (52.7%); names and numbers count in
    both figures. A sample of the lexicon's citations of Griffith, checked against his own texts, held for all 15
    found. The meanings are not yet worded anew for a public table
    ([`data/discovery/lexicon.md`](data/discovery/lexicon.md)).

## The question

Meroitic, the language of the kingdom of Kush (Sudan, about 300 BC to 400 AD), can be read aloud since Griffith
(1909–11), but most of it is not understood: there is no long bilingual text, and its relatives in the Northern East
Sudanic family split from it long before it was written. This repo is a two-day experiment (2026-11-08/09), with
a third day of reading and testing (2026-11-10): can a
frontier language model (Claude Opus 5.5, run as about 60 independent subagents) find real patterns in Meroitic and
make it more understandable?

Results, with every number traced to its run: [`REPORT.md`](REPORT.md). What to do next: [`NEXT_STEPS.md`](NEXT_STEPS.md).
The illustrated summary page: <https://mikekovetsky.github.io/meroitic/> (source: `docs/report.html`). This file
describes the data and the methods.

## Data

Data without an open licence is not in this repo, apart from the readings and glosses the tests are scored against
(the Rilly and FHN rows below): it stays on the author's machine, listed in `.gitignore`, and the scripts rebuild
what can be rebuilt.

| Source | What | In this repo |
|---|---|---|
| Otten & Anastasopoulos, ALP 2025, [Meroitic-Corpus](https://github.com/Joshua-Otten/Meroitic-Corpus) | the only machine-readable corpus (18,090 lines): example texts and phrases quoted in Millet 1968 and Rilly 2007, Lobban's word list and three royal narratives, padded with name-swapped copies | not committed (no licence stated): clone it to `data/otten/`; the cleaned corpora (`data/corpus*.jsonl`) and the task files that embed them (`runs/tasks/`) are rebuilt locally, not committed |
| Griffith, *Meroitic Inscriptions* I–II (1911–12) and Garstang/Sayce/Griffith, *Meroë* (1911), archive.org | printed Meroitic type, public domain | `data/expansion/griffith_*.jsonl`, read by the model |
| Griffith, *Karanòg: The Meroitic Inscriptions of Shablûl and Karanòg* (1911), [archive.org](https://archive.org/details/karangmeroitic00grifuoft) | 151 funerary texts as hand copies, public domain; most of their words printed again in type in the same book | `data/expansion/karanog/`: the texts read by the model and checked against that type (`griffith_karanog.jsonl`), the 48 typed reference pages, and [how it was done and measured](data/expansion/karanog/README.md) |
| *Meroitic Newsletter* 1–30 (1968–2003), scans at meroiticnewsletter.org | printed transliterations with REM numbers: 256 texts typed, 188 of them new to the corpus; the articles are in copyright | not committed: the method, the scripts (`src/mnl/`) and the measured accuracy are in [`data/expansion/newsletter_reading.md`](data/expansion/newsletter_reading.md) |
| Rilly 2003, *Lexique méroïtique* (thesis vol. II, HAL [tel-04793700](https://hal.science/tel-04793700)) | the fullest open lexicon, 937 entries | not committed (copyrighted): extracted from the scans for private analysis; `src/lexique.py` needs it in `data/rilly2003/`. The lexicon test's answer key (`runs/keys/lexique_*.json`, `runs/lexique_judge.json`) gives 68 of its glosses in English paraphrase |
| The TLA's [Demotic sentences](https://huggingface.co/datasets/thesaurus-linguae-aegyptiae/tla-demotic-v18-premium) and the [Comprehensive Coptic Lexicon](https://github.com/KELLIA/dictionary) v1.2, both CC BY-SA 4.0 | 5,660 Demotic lemmata with their word classes and 11,283 Coptic entries with meanings: the pools of the Egyptian search | not committed: download them to `data/sources/egyptian/demotic/train.jsonl` and `data/sources/egyptian/coptic/Comprehensive_Coptic_Lexicon-v1.2-2020.xml`; the list of candidates (`data/discovery/egyptian_candidates.tsv`, CC BY-SA 4.0) holds lemma numbers and forms |
| Rilly, Hintze, Griffith, Millet and others via web sources | the answer key: 82 accepted meanings, 26 grammatical endings, each sourced | `data/gold_lexicon.json`, `data/gold_morphology.json` |
| Starostin's GLD (no licence stated), IDS, ASJP, numerals (CC BY), Rilly 2003 vol. I (HAL) | Nubian, Nara, Taman, Nyima word lists; Rilly's 82 sound correspondences | not committed: `data/nes/README.md` lists every source and how the lists were built; `meroitic_wiktionary.tsv` (CC BY-SA) is included |
| *Fontes Historiae Nubiorum* II–III (Bergen, all rights reserved) | modern transliterations used as ground truth | the readings of about twenty short texts the reading tests are scored against, each with its REM number (`data/expansion/pilot.jsonl`, `printed_type_test.md` and `hand_copy_test.md` there, the scoring scripts in `runs/work/`); otherwise short excerpts |
| Millet, "The Meroitic Inscriptions from Gebel Adda", JSSEA 32 (2005), [the society's PDF](https://news.thessea.org/images/SSEA_assets/journals/JSSEA_32.pdf); *Fontes Historiae Nubiorum* III as a whole, [the copy on Zenodo](https://zenodo.org/records/821860) (the book says all rights reserved, the record CC BY 4.0) | 46 and 12 entries on inscriptions, with comments: the second witness in the check of the coverage map; and FHN III's Demotic and Greek graffiti, read beside its Meroitic texts | not committed (in copyright): `data/sources/jssea/`, `data/sources/fhn/` and their text layers (`data/sources/jssea-text/`, `data/sources/fhn-text/`), the judges' packs and answers in `data/sources/expert/`, and the readers' and judges' packs and answers of the Demotic step in `data/sources/demotic/`; `data/discovery/experts_figures.json` and `experts_words.tsv` hold counts and word forms only, `demotic_figures.json` counts and five title words |

Since 2026-11-12 the readings are also listed by inscription: [`data/inscriptions.jsonl`](data/inscriptions.jsonl)
has one row for each of the 563 inscriptions the project holds a reading of, with its REM or edition number, site,
kind and every reading's source and licence, and the text of the readings that are open;
[`data/inscriptions_map.tsv`](data/inscriptions_map.tsv) says what each of the 899 texts of `corpus_v5` is.
`data/corpus_v6.jsonl`, one row per inscription with real names, is local like the corpora before it.

## Methods

### 1. Cleaning the corpus

The public corpus repeats each text many times with person names swapped from two pools (data augmentation for
embeddings). `src/pool.py` finds the pools from one-slot differences between lines (a clique of 178 private names
and 11 royal names); `src/dedup.py` masks them as `NAME` / `RNAME` and collapses identical skeletons;
`src/collapse.py` merges copies that differ only where a multi-word name filled a `NAME` slot; `src/clean_v2.py`
masks the leftover multi-word names. `src/corpus.py` normalises Millet's spelling (`E` → `o`; capitals that only mark
uncertain readings lowered; `x`, `X` for the two h signs, `S` for the s sign, lowercase `s` for the se sign, `N` for
ñ) and adds the three royal narratives once. Result: 18,090 lines → 662 texts, about 18,100 words
(`data/corpus_v2.jsonl`). Several blind runs found leftovers of the padding; each finding fed the next cleanup.

### 2. Blind tasks and how leaks were caught

Every test is a task file in a folder under `/private/tmp/claude-501/blind/` (copies in `runs/tasks/`, local-only),
solved by a fresh subagent told to read only that file, with no web access; answers go to `runs/answers/`, keys to
`runs/keys/`. Agents report the tools they used, and several runs were asked afterwards whether they recognised the
language. Builders refuse to overwrite a folder a run has used, and `src/build_extra.py check` and
`src/cloze_families.py baseline` rebuild later tasks byte for byte from the repo and the local corpus snapshot
(Reproduce, below).

Leaks found and fixed along the way, each worth knowing for anyone repeating this:
- inscription names used as line labels in a "blind" file (the model recognised them);
- the corpus's own padding, which two restoration runs exploited to score 94% and 93%;
- a glossary plus the model's memory, which together break any letter substitution.

### 3. Step 0: can it recover held-out meanings? (`src/build_tasks.py`, `src/score.py`)

35 words with accepted meanings, split into two folds. Each task gives a glossary of one fold and asks the solver to
match the other fold's words to their meanings, one to one. Four conditions: memory only (M), real corpus (R),
corpus re-spelled with a random letter derangement (S, `src/scramble.py`), and re-spelled words with no corpus (S0).
Scored with an exact permutation p-value (the chance that a random matching gets as many right). All conditions
scored 35/35, and S0 shows why: the glossary lets a model that knows Meroitic invert the cipher.

### 4. A language it can't know (`src/synth.py`)

A generated corpus with the real corpus's scale and texture (1,003 texts, 16k words): funerary formulas, votive
texts, ration lists, labels and three royal annals; invented stems and endings; endings written fused or split;
masked names; lost signs. The same matching task, 52 usable test words over two folds (four dropped by review: absent,
too rare, or spelled like an ending), run twice independently. A blind grammar task on the same corpus is scored
against the generator's eight endings.

### 5. Natural experiments: what memory lacks

Open recall first ("unknown" allowed, no options), then the corpus task only for the words recall missed, so the
corpus has to supply what memory can't. Run twice: 17 words from the answer key (`N_open`), and 68 words glossed as
established or probable in Rilly's 2003 lexicon that occur in 2+ texts (`src/lexique.py`: names, gods, endings,
cross-references and ambiguous spellings excluded). Answers are scored by an independent judge agent against the
published meaning: SAME, TYPE (right kind of word only), WRONG, UNKNOWN (`runs/lexique_judge.json`). A late check
(`python3 -I src/lexique.py judged`) found that the corpus tasks' glossary gave six targets away (`qore` "ruler" listed
while `qor-o`, `qorise`, `qorene` and `qorode` were targets; `mk`, glossed "god, and very probably goddess", for
`mkdi`; `mlo` for `smlo`) and that three items shouldn't have been test words; the report gives the corrected
numbers, and the builder now leaves out of the glossary any word that gives a target away.

### 6. Restoration (`src/cloze.py`, `src/cloze_families.py`)

Mask words in held-out texts and restore them, against an n-gram restorer (2+2 context with backoff) that sees the
same texts as the solver, masks included. Version 3 groups texts into families of near-copies (shared word
trigrams, union-find), holds out 60 small families whole, and scores separately the masks with no parallel anywhere
in the task (no 12+ letter run around the word occurs elsewhere, spaces and case ignored). Compared with an exact
McNemar test.

### 7. Grammar, Kober-style (`src/build_morph.py`, `src/unscramble.py`)

The solver gets a corpus and no meanings and must find the recurring formulas, the bound morphemes, their functions
and the word classes. Run on the scrambled real corpus (scored against the 26 published endings) and on the
synthetic language (scored against the generator).

### 8. Is Meroitic visibly related to Nubian? (`src/cognates.py`, `src/cognates_rules.py`)

Do Meroitic words resemble same-meaning words in 10 Northern East Sudanic word lists more than chance? Raw string
similarity first, then an engine that scores alignments by Rilly's 82 sound correspondences. Validated against 2,000
shuffles of the Meroitic meanings, with Rilly's reconstructions and the words his rules were built from kept out of
the held-out test, because both were made with Meroitic in view. Candidate cognates for unknown words were allowed
only if the held-out test passed; it didn't.

### 9. Discovery runs and adversarial verification

Discovery agents read a text group (funerary formulas, the Hamadab stela REM 1003, the Philae near-bilinguals, the
Tanyidamani stela REM 1044) with web access, proposed hypotheses with evidence, alternatives and a test, and labelled
each ESTABLISHED, PUBLISHED HYPOTHESIS or NEW after a literature search. A separate agent was then told to prove each
NEW claim wrong: harder searches in English, French and German, FHN commentary, Millet's glossary, theses, and a
corpus check for counterexamples (`data/discovery/verification.md`).

### 10. Calibrated readings of unknown words (`runs/unknown/`)

Three independent runs read 29 frequent words of unknown meaning from the corpus, each answer with a strict 1–5
confidence and with evidence from the corpus kept apart from anything recalled. A reading counts only if two runs
agree at confidence 4 or more.

### 11. Reading the script from images (`data/discovery/vision.md`, `data/expansion/`)

Photographs of inscriptions (Wikimedia), Griffith's printed type and Griffith's hand copies. Each reading was written
down, with a timestamp, before the modern transliteration (FHN) was opened, then scored sign by sign; misreadings
are separated from places where Griffith's 1911 reading differs from the modern one.

### 12. Growing the corpus (`src/expand.py`)

Five agents transcribed Griffith's printed inscriptions sign by sign into standard transliteration and the corpus
spelling, marking uncertain signs, with the REM number where there is one (REM 0001–0137 follow Griffith's
numbers). `src/expand.py` drops texts already in the corpus or repeating an earlier Griffith text (half or more of a
text's letter 6-grams occur in one such text, or one with masked names or lost signs spells all of it, both spelled
alike first) and writes `data/corpus_v3.jsonl`. Griffith printed only part of 29 of the 152 texts; those are left
out.

Griffith gives the Karanòg and Shablûl inscriptions only as hand copies, which one reader gets 89% right. But
the same book prints most of their words a second time in type: a table of names, three indexes and tables of the
closing formulae. Readers typed those 48 pages, read each hand copy on its own, and then checked the reading
against the printed entries for that inscription (`src/karanog_refs.py`, `src/karanog.py`,
[`data/expansion/karanog/README.md`](data/expansion/karanog/README.md)). On the four texts FHN prints, fresh
readers who could not see FHN reached 97.7% of signs. Eleven pages (31 inscriptions) were then read again by a
second reader: the two checked readings agree on 97.7% of signs there (98.8% for all 53 pages, weighting the
seven most damaged and the three drawn at random by the pages they stand for), and the 56 places where they
differ were settled against the copy and the type. `src/karanog.py` divides the closing formulae into words as
Griffith's tables do, but for a few rows where the stone has a divider or the typed table differs in a sign.
`src/expand.py` tests the 151 texts against `corpus_v3` but not against each other, as they are separate
inscriptions that share their formulae, and leaves the letter groups of those formulae out of the comparison. It
finds all 151 new and writes them with `corpus_v3` as `data/corpus_v5.jsonl` (899 texts, 21,977 words);
`corpus_v3` itself is left as it was.

### 13. Review

Code changes were reviewed by a fresh Opus 5.5 reviewer that saw the diff and a context pack, never the author's
reasoning, and fixed what it found (four full reviews; the fourth, of `src/lexique.py` and `src/expand.py`, was
stopped partway on Mike's word so the repo could be pushed, and finished before it was shared). They found and fixed
answer leaks, a Monte Carlo p-value printed as 0.0, a baseline that saw less than the solver, a corpus bug that split
words at doubtful-sign marks, a copy detector that missed copies, and rules applied outside the positions Rilly gives
them; each fix changed a reported number, and the report shows the corrected one. Five more full reviews followed
on 2026-11-09 and 10, two of the Newsletter tools and three of the Karanòg scripts and rows; they fixed, among other
things, a scorer that let extra signs go free, references misread as inscription numbers, an editor's "(sic)"
counted as two signs, and formula words that the uniform rows still divided two ways. Tests: `tests/`.

### 14. How much can be translated today (`src/coverage.py`)

Every word of `corpus_v5` gets a gloss, a level and a confidence. A word that is a spelling of an entry of Rilly's
lexicon takes that entry, alone or as a stem with a known ending; masked names, numbers and the names of Griffith's
Karanòg tables are settled the same way. The 1,887 words this leaves went to seventeen independent analysts with
their contexts and the lexicon as a table: each cut the word into parts (an entry, a name, a number or an unknown
piece) and named its kind, and the script kept an answer only if its parts spell the word and its entries exist.
Two more analysed 230 of the most frequent a second time; where the two differ in level, the lower stands. A word
counts as translated when the parts that are words of their own are names, numbers or entries Rilly holds as
established or probable, and an analyst's cut has a confidence of 4 or 5. Near-copies of a text are counted once
in the headline and in the ranking of what blocks most texts. The gloss file leans on the
lexicon and is local-only; the counts, the brief and the list of unknown pieces are public
([`data/discovery/coverage.md`](data/discovery/coverage.md)).

Four corrections follow the first build (`correct`), each a rule: the rest of a masked name of several words that
the padding of the older corpus left behind its mask ("mokelowi", "mete l") is part of the name; a stem of two
signs counts as three letters when one of them is the sign se or ne and Rilly holds the entry as established
(`smlowi`, "is the wife of"); two or three neighbouring words are one word written apart when one of them has
one or two letters and the whole also stands written as one elsewhere (`wo Si` for `woSi`); and a piece that two
blind checkers took for a spelling of a word with an accepted meaning takes that meaning (for two of them,
`mXeyot` and `yetmetl`, the pack showed a word with their letters, and their gloss says so), as do three forms
of "sister" that a reader of the families of Karanòg read so. The corrected map is written beside the first one, whose list the Egyptian and the
variants searches read.

### 15. Egyptian words behind Meroitic ones (`src/egyptian.py`)

A scorer that knows only letters: Meroitic, Demotic and Coptic words are reduced to their consonants in one
alphabet, and an Egyptian word becomes a Meroitic one letter by letter (kept, changed, dropped, or with the article
p or t in front), with chances counted from the aligned known loans. The answer key is the 35 entries of Rilly's
lexicon that two independent readers took as accepted borrowings; each is searched with a model trained on the
others, among the entries of its own kind and then with the neighbouring kinds added (titles with nouns). A match
counts only as far as it beats the best matches of made-up words of the same length; the 64 words with an
accepted meaning and no Egyptian link beat that bar about as often as chance would (0 to 5 times, where 3 are
expected). The best matches for the unknown pieces went to two blind checkers with unmarked decoys. A second run
(`vowels`) compares the written vowels as well, on the Coptic entries only, since Demotic writes none, and keeps
the consonant figures of the same pool beside its own. The word lists, the key and the result files are
local-only; the page, the brief and the two lists of candidates are public
([`data/discovery/egyptian.md`](data/discovery/egyptian.md)).

### 16. Spellings of known words among the unknown pieces (`src/variants.py`)

The same scorer turned on Meroitic itself: each piece of the coverage map's list is compared, vowels included,
with the 688 words of Rilly's lexicon (655 different headword spellings), and may carry one of the 25 known
endings, which the search takes as the Egyptian search takes an article, on words read from their end. The model
starts flat, with no groups of like letters, and counts which letters alternate on the 307 spelling variants that
the lexicon lists under its entries. The test hides each listed variant of a word in turn, everywhere in the
lexicon, trains on the rest and asks for the entry that lists it as the single best match. The bar was written
down before the first run. A match counts only as far as it beats the best matches of 1,000 made-up words of the
same length, and the words with an accepted meaning that the lexicon links to nothing go through the same search,
to see what that yardstick is worth. Every match that beats the bar is packed for two blind checkers with 24
listed variants whose answer is known: 12 with the right entry among the candidates, and 12 decoys with it taken
out. A pack shows under a word only what the coverage map counts as translated or what the lookup took from the
lexicon, never an analyst's guess, and nothing under a word that the map finds the piece in (three items still
showed a word with their own letters that the map cuts otherwise, and the page also gives the count without the
two of them that were confirmed). A piece is confirmed when both
checkers say it is the same word and name one candidate; the script then counts, on the map's gloss file, the
running words that would move, and leaves the map as it is. The lexicon, the gloss file and the result files are
local-only; the page, the brief, the list of every searched piece with its best match and the list of the
confirmed pieces are public ([`data/discovery/variants.md`](data/discovery/variants.md)).

### 17. The map against two printed editions (`src/experts/`)

The coverage map has one source of meanings, so its figure was set beside two others: Millet's edition of the
Gebel Adda inscriptions (2005) and the entries on Meroitic texts in *Fontes Historiae Nubiorum* III (1998). An
entry is matched to a corpus text by the runs of five letters the two share, counted in both directions, and the
pairs are then read side by side (31 texts). A pack gives a judge the edition's printed entry and, beside it, our
words in order with our reading of each; the judge marks every word agree, partly, differ, new, silent or absent
and notes the edition's meaning. One judge reads each of three packs and a second reads one of them again. A
tenth of the readings with a meaning are swapped for another word's, unmarked, and left out of every figure: they
measure how lenient a judge is. A second pass lists every meaning the editions give at all (two readers), looks
each word up as the map does, and has two judges compare the meanings; there each judge sees decoys of its own
in place of our reading, on different lines, drawn so that a decoy shares no content word with our reading or
with the edition's meaning. The editions, the packs and the answers are local-only; the page, the figures and a
list of the words with their verdicts, without readings, are public
([`data/discovery/experts.md`](data/discovery/experts.md)).

### 18. One inscription once (`src/v6/`)

`corpus_v5` holds copies, masked names and phrases quoted in a grammar beside inscriptions. `src/v6/otten.py`
traces each of its older texts to the line of Otten's per-scholar files it was padded from: the line itself, or
the line with one stretch swapped. `src/v6/readings.py` lists every reading held (Griffith's print, the Karanòg
copies, the Newsletter, Millet 2005, FHN III, Otten's narratives and source lines) with the numbers its edition
gives, and compares texts by their runs of five letters, the formulae left out. `src/v6/build.py` makes the
inscriptions: readings that share a number are one, two different numbers of one numbering are two, and a text
without a number goes by letters, where a sure match to one inscription stands and a doubtful one goes to two
readers who see both texts, with known lines and decoys mixed in (`src/v6/packs.py`). A source line is a
reading of an inscription, an example phrase from a grammar, or an inscription not identified; one reading per
inscription is preferred by a fixed order, with the numerals another edition shows and Otten's name tags. The bar for the rule was written before it was scored, and missed.
`src/v6/recount.py` runs the coverage map and the check against the two editions on the new rows, without a new
analyst or judge, and `src/v6/public.py` writes the public table, the map of the old ids and the tables of the
page ([`data/discovery/corpus_v6.md`](data/discovery/corpus_v6.md)).

### 19. Analysts on the unread spellings of the clean corpus (`src/v6/readers.py`)

The recount of step 18 ran without a new analyst, so the spellings that `corpus_v5` does not have stood with the
lookup alone. `src/v6/readers.py packs` takes the words the lookup leaves on `corpus_v6`, without the words an
edition tags as personal names and without those a pack of the first run holds, and writes them into packs like
those of step 14, numbered after them and kept in a folder of their own; the most frequent go into one more pack
for a second analyst. `count` runs the corrected map of `corpus_v6` twice, with the first run's answers alone and
with the new ones added, and reports what moved. The bar on the two analysts' agreement and the gain expected
were written down before the run ([`data/discovery/v6_readers.md`](data/discovery/v6_readers.md)).

### 20. The same people in two scripts (`src/demotic.py`)

The entries of *Fontes Historiae Nubiorum* III are cut from the volume's text layer at the headings that
continue its numbering. Two readers take the 24 Demotic and Greek entries and one the nine Meroitic entries of
the same families; each lists the people an entry's ancient text names, with their titles, their kin and whom
the editors take for the same person elsewhere, and every place where the editors set a Meroitic word beside a
Demotic, Greek or Egyptian one. `merge` joins the lines into people (the same name in the editors' English, or
the editors' own identification, matched by the consonants of the name as the editors or the ancient text write
it, and never to a namesake with another letter or number) and checks two bars written before the run: how many
person lines both readers list, and whether both find the known equations. The equations go through the lookup
and the judges' table of step 17, each judge with decoys of its own
([`data/discovery/demotic.md`](data/discovery/demotic.md)).

### 21. A second scholar for every meaning (`src/lexicon.py`)

`layout` lists every entry of the lexicon that the map of the clean corpus uses, with Rilly's status and page,
the proposals of other scholars that the lexicon records, and the editors' verdicts of step 17 on words built on
the entry. `packs` sets each proposal on an entry Rilly states beside the lexicon's meaning, without the
scholar's name, for two judges, each with decoys of their own: another entry's meaning from outside the line's
field of meaning. `check` sends a sample of the lexicon's citations of Griffith to a reader with Griffith's own
texts. The bars and the rules for the four statuses were committed before any judge answered; `public` counts
them and writes the figures and a table of headwords, statuses and the scholars cited, without the meanings
([`data/discovery/lexicon.md`](data/discovery/lexicon.md)).

## Reproduce

From a clone of this repository and Otten's corpus, with nothing else:

```bash
git clone https://github.com/Joshua-Otten/Meroitic-Corpus data/otten
python3 -I src/pool.py && python3 -I src/dedup.py && python3 -I src/collapse.py && python3 -I src/corpus.py && python3 -I src/clean_v2.py
python3 -I src/expand.py
python3 -I src/score.py --answers runs/answers
python3 -I tests/test_harness.py && python3 -I tests/test_cognates_rules.py && python3 -I tests/test_lexique.py
python3 -I tests/test_karanog.py && python3 -I tests/test_newsletter.py && python3 -I src/mnl/test_mnl.py
python3 -I tests/test_coverage.py && python3 -I tests/test_egyptian.py && python3 -I tests/test_variants.py
python3 -I tests/test_experts.py && python3 -I tests/test_corpus_v6.py
python3 -I tests/test_v6_readers.py && python3 -I tests/test_demotic.py && python3 -I tests/test_lexicon.py
```

The second line ends `texts 662; tokens 18075; types 1622` (`data/corpus_v2.jsonl`). The third prints
`corpus_v2 662 texts 18075 words -> corpus_v3 748 texts 19066 words (+5%)` and ends
`corpus_v3 748 texts 19066 words -> corpus_v5 899 texts 21977 words (+15%)`. The tests print `skip` for each
check that reads a local-only file, and each file's last line counts the checks passed and skipped
(`src/mnl/test_mnl.py`, a unittest file, ends `OK`); none fails.

Ten things need files that are kept locally (Data, above), so they don't run from a clone:

- `python3 -I src/cloze_families.py copies runs/answers/C3_cloze.json runs/cloze_families_ngram.json` and the other
  restoration checks read the corpus snapshot several runs used (`data/corpus_v2_c3_snapshot.jsonl`, taken before
  the review's fixes to `src/corpus.py`, so it can't be rebuilt);
- `python3 -I src/lexique.py judged` (and the lexicon test's other commands) reads Rilly's lexicon;
- `python3 -I src/cognates_rules.py` reads the NES word lists and Rilly's sound correspondences;
- `python3 -I src/coverage.py first` (and `build`) reads Rilly's lexicon, `corpus_v5` and the analysts' answers;
- `python3 -I src/egyptian.py first` (and `build`, `vowels`) reads the two Egyptian word lists, Rilly's lexicon and the
  answer key drawn from it;
- `python3 -I src/variants.py first` (and `build`, `sample`, `check`, `merge`) reads Rilly's lexicon, `corpus_v5`
  and the coverage map's gloss file;
- `python3 -I src/experts/tally.py` (and the other scripts of `src/experts/`) reads the two editions' text layers,
  the coverage map's gloss file, Rilly's lexicon and the judges' answers;
- `python3 -I src/v6/build.py` (then `src/v6/recount.py` and `src/v6/public.py`; `src/v6/readings.py test` for the
  bar) reads Otten's files, `corpus_v5`, the Newsletter texts, the two editions' text layers, and for the recount
  Rilly's lexicon, the analysts' answers and the judges' answers;
- `python3 -I src/v6/readers.py count` reads Rilly's lexicon, `corpus_v6` and the analysts' answers of both runs;
- `python3 -I src/demotic.py merge` (and `packs`, `table`, `count`) reads the text layer of FHN III, the readers'
  and judges' answers, Rilly's lexicon, the coverage map's gloss file and the lines of the check against the two
  editions.

## Layout

- `src/`: corpus cleaning, task builders, scorers, the synthetic language, cognate tests, lexicon test, merge,
  the translation coverage map (`coverage.py`), the search for Egyptian sources (`egyptian.py`), the search
  for spellings of known words (`variants.py`), the check of the map against two printed editions (`experts/`),
  the corpus keyed by inscription and its analysts (`v6/`) and the same people in Demotic, Greek and Meroitic
  (`demotic.py`).
- `tests/`: the checks; `tests/local_only.py` lets a check skip when a local-only file is absent.
- `data/`: answer keys, leads, discovery write-ups, the Griffith transcriptions (`data/expansion/`) and the table
  of inscriptions (`inscriptions.jsonl`, `inscriptions_map.tsv`); the cleaned corpora (`corpus_v2.jsonl`,
  `corpus_v3.jsonl`, `corpus_v5.jsonl`, `corpus_v6.jsonl`), the word lists and Rilly's lexicon are local-only.
- `runs/`: prompts, the task each blind run saw, its answers, keys and scores; `runs/work/` holds the agents'
  working files (transcription scripts, timestamped blind readings).
- `docs/report.html`: the summary page's source; `docs/index.html` is the same page as GitHub Pages serves it
  (`python3 -I tests/test_harness.py pages` rebuilds it).
- `LICENSE` (MIT, the code) and `LICENSE-DATA.md` (CC BY 4.0, the data and write-ups, with what is excepted).
- `REPORT.md`: the results. `NEXT_STEPS.md`: what to do next.

## Licence

The code is under the MIT licence ([`LICENSE`](LICENSE)). The Griffith transcriptions, the answer keys, the runs and
the write-ups are under CC BY 4.0 ([`LICENSE-DATA.md`](LICENSE-DATA.md)), which also lists the third-party material
that keeps its own terms: the Wiktionary list and the list of Egyptian candidates (CC BY-SA 4.0), the readings
quoted from *Fontes Historiae Nubiorum*, the single words quoted from Millet 2005 and the glosses paraphrased
from Rilly's lexicon.

## Limits

- Blind tests on real Meroitic can't exclude memory: the model has read the decipherment literature.
- The synthetic language's difficulty depends on its generator.
- Judges and readers are the same model family; scoring files are kept line by line so a person can re-judge.
- Griffith's 1911–12 readings differ from the modern REM text in about 4% of signs; rows say they are Griffith's.
- The reading test for printed type covered 12 cursive texts from Philae. The 48 rows in hieroglyphic type were
  not scored, and their notes say so.
- Rilly 2007, Hintze's editions and Hallof 2024 are print-only and were not read; REM is online
  ([Persée](https://www.persee.fr/issue/rem_0000-0000_2000_num_1_1)) but was not read either.
