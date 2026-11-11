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
8. **About 60% of the corpus's running words can be translated today, word by word.** Every word of the 899 texts
   was glossed from Rilly's 2003 lexicon, by lookup and then by analysts: 13,292 of 21,977 words (60.5%) are a
   name, a number or a word with an accepted meaning or function (59.9% with near-copies counted once), 17% have a
   proposal only, 10% are known by their kind only and 12% are unknown. Every word is translated in 85 of 608
   texts. The 1,292 pieces without an accepted meaning are listed with their kind and the texts they block
   ([`data/discovery/coverage.md`](data/discovery/coverage.md)).

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
| Rilly, Hintze, Griffith, Millet and others via web sources | the answer key: 82 accepted meanings, 26 grammatical endings, each sourced | `data/gold_lexicon.json`, `data/gold_morphology.json` |
| Starostin's GLD (no licence stated), IDS, ASJP, numerals (CC BY), Rilly 2003 vol. I (HAL) | Nubian, Nara, Taman, Nyima word lists; Rilly's 82 sound correspondences | not committed: `data/nes/README.md` lists every source and how the lists were built; `meroitic_wiktionary.tsv` (CC BY-SA) is included |
| *Fontes Historiae Nubiorum* II–III (Bergen, all rights reserved) | modern transliterations used as ground truth | the readings of about twenty short texts the reading tests are scored against, each with its REM number (`data/expansion/pilot.jsonl`, `printed_type_test.md` and `hand_copy_test.md` there, the scoring scripts in `runs/work/`); otherwise short excerpts |

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
Karanòg tables are settled the same way. The 1,887 words this leaves went to nineteen independent analysts with
their contexts and the lexicon as a table: each cut the word into parts (an entry, a name, a number or an unknown
piece) and named its kind, and the script kept an answer only if its parts spell the word and its entries exist.
The 230 most frequent were analysed twice; where the two differ in level, the lower stands. A word counts as
translated when its parts are names, numbers or entries Rilly holds as established or probable. Near-copies of a
text are counted once in the headline and in the ranking of what blocks most texts. The gloss file leans on the
lexicon and is local-only; the counts, the brief and the list of unknown pieces are public
([`data/discovery/coverage.md`](data/discovery/coverage.md)).

## Reproduce

From a clone of this repository and Otten's corpus, with nothing else:

```bash
git clone https://github.com/Joshua-Otten/Meroitic-Corpus data/otten
python3 -I src/pool.py && python3 -I src/dedup.py && python3 -I src/collapse.py && python3 -I src/corpus.py && python3 -I src/clean_v2.py
python3 -I src/expand.py
python3 -I src/score.py --answers runs/answers
python3 -I tests/test_harness.py && python3 -I tests/test_cognates_rules.py && python3 -I tests/test_lexique.py
python3 -I tests/test_karanog.py && python3 -I tests/test_newsletter.py && python3 -I src/mnl/test_mnl.py
python3 -I tests/test_coverage.py
```

The second line ends `texts 662; tokens 18075; types 1622` (`data/corpus_v2.jsonl`). The third prints
`corpus_v2 662 texts 18075 words -> corpus_v3 748 texts 19066 words (+5%)` and ends
`corpus_v3 748 texts 19066 words -> corpus_v5 899 texts 21977 words (+15%)`. The tests print `skip` for each
check that reads a local-only file, and each file's last line counts the checks passed and skipped
(`src/mnl/test_mnl.py`, a unittest file, ends `OK`); none fails.

Four things need files that are kept locally (Data, above), so they don't run from a clone:

- `python3 -I src/cloze_families.py copies runs/answers/C3_cloze.json runs/cloze_families_ngram.json` and the other
  restoration checks read the corpus snapshot several runs used (`data/corpus_v2_c3_snapshot.jsonl`, taken before
  the review's fixes to `src/corpus.py`, so it can't be rebuilt);
- `python3 -I src/lexique.py judged` (and the lexicon test's other commands) reads Rilly's lexicon;
- `python3 -I src/cognates_rules.py` reads the NES word lists and Rilly's sound correspondences;
- `python3 -I src/coverage.py first` (and `build`) reads Rilly's lexicon, `corpus_v5` and the analysts' answers.

## Layout

- `src/`: corpus cleaning, task builders, scorers, the synthetic language, cognate tests, lexicon test, merge,
  and the translation coverage map (`coverage.py`).
- `tests/`: the checks; `tests/local_only.py` lets a check skip when a local-only file is absent.
- `data/`: answer keys, leads, discovery write-ups and the Griffith transcriptions (`data/expansion/`); the cleaned
  corpora (`corpus_v2.jsonl`, `corpus_v3.jsonl`, `corpus_v5.jsonl`), the word lists and Rilly's lexicon are local-only.
- `runs/`: prompts, the task each blind run saw, its answers, keys and scores; `runs/work/` holds the agents'
  working files (transcription scripts, timestamped blind readings).
- `docs/report.html`: the summary page's source; `docs/index.html` is the same page as GitHub Pages serves it
  (`python3 -I tests/test_harness.py pages` rebuilds it).
- `LICENSE` (MIT, the code) and `LICENSE-DATA.md` (CC BY 4.0, the data and write-ups, with what is excepted).
- `REPORT.md`: the results. `NEXT_STEPS.md`: what to do next.

## Licence

The code is under the MIT licence ([`LICENSE`](LICENSE)). The Griffith transcriptions, the answer keys, the runs and
the write-ups are under CC BY 4.0 ([`LICENSE-DATA.md`](LICENSE-DATA.md)), which also lists the third-party material
that keeps its own terms: the Wiktionary list (CC BY-SA 4.0), the readings quoted from *Fontes Historiae Nubiorum*
and the glosses paraphrased from Rilly's lexicon.

## Limits

- Blind tests on real Meroitic can't exclude memory: the model has read the decipherment literature.
- The synthetic language's difficulty depends on its generator.
- Judges and readers are the same model family; scoring files are kept line by line so a person can re-judge.
- Griffith's 1911–12 readings differ from the modern REM text in about 4% of signs; rows say they are Griffith's.
- The reading test for printed type covered 12 cursive texts from Philae. The 48 rows in hieroglyphic type were
  not scored, and their notes say so.
- Rilly 2007, Hintze's editions and Hallof 2024 are print-only and were not read; REM is online
  ([Persée](https://www.persee.fr/issue/rem_0000-0000_2000_num_1_1)) but was not read either.
