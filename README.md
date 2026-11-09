# Meroitic and Opus 5.5: what a frontier model can and can't do

Meroitic, the language of the kingdom of Kush (Sudan, about 300 BC to 400 AD), can be read aloud since Griffith
(1909–11), but most of it is not understood: there is no long bilingual text, and its relatives in the Northern East
Sudanic family split from it long before it was written. This repo is a two-day experiment (2026-11-08/09) on one
question: **can a frontier language model (Claude Opus 5.5, run as many independent subagents) find real patterns in
Meroitic and make it more understandable?**

Results, with every number traced to its run: [`REPORT.md`](REPORT.md). This file describes the methods.

## Short answer

1. The model already knows the published vocabulary. On real Meroitic, memory and reasoning can't be separated, and
   disguising the script doesn't help: it broke a letter-swap cipher from a 17-word glossary.
2. On a synthetic language it can't know, it infers word meanings from a corpus of the same size: 41 and 43 of 52 on
   two independent runs, where chance is about 2.
3. Its confidence is calibrated. In every test, all answers it gave at confidence 4–5 were right (74 of 74, after
   removing items a glossary gave away); at 1–2 it is right about a third of the time.
4. It restores masked words better than an n-gram model (48% vs 26% where nothing can be copied), reads Griffith's
   printed Meroitic type at 95.6% sign accuracy, and cannot read worn stones from photographs.
5. None of the "new" findings its discovery runs proposed survived an adversarial literature check (0 of 14):
   where the key literature is print-only, it can't tell a rediscovery from a discovery.
6. The binding constraint is data. The public corpus is small and padded; this repo cleans it, and adds 86 new texts
   out of 152 the model transcribed from Griffith's public-domain editions.

## Data

| Source | What | In this repo |
|---|---|---|
| Otten & Anastasopoulos, ALP 2025, [Meroitic-Corpus](https://github.com/Joshua-Otten/Meroitic-Corpus) | the only machine-readable corpus (18,090 lines) | not committed (no licence stated); clone it to `data/otten/` |
| Griffith, *Meroitic Inscriptions* I–II (1911–12) and Garstang/Sayce/Griffith, *Meroë* (1911), archive.org | printed Meroitic type, public domain | `data/expansion/griffith_*.jsonl`, read by the model |
| Rilly 2003, *Lexique méroïtique* (thesis vol. II, HAL [tel-04793700](https://hal.science/tel-04793700)) | the fullest open lexicon, 937 entries | `data/rilly2003/`, extracted from the scans for private research; **don't publish** |
| Rilly, Hintze, Griffith, Millet and others via web sources | the answer key: 82 accepted meanings, 26 grammatical endings, each sourced | `data/gold_lexicon.json`, `data/gold_morphology.json` |
| Starostin's GLD, IDS, ASJP, numerals (CC BY), Rilly 2003 vol. I (HAL) | Nubian, Nara, Taman, Nyima word lists; Rilly's 82 sound correspondences | `data/nes/` |
| *Fontes Historiae Nubiorum* II–III (Bergen, all rights reserved) | modern transliterations used as ground truth | quoted only in short excerpts |

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

Every test is a task file in a folder under `/private/tmp/claude-501/blind/` (copies in `runs/tasks/`), solved by a
fresh subagent told to read only that file, with no web access; answers go to `runs/answers/`, keys to `runs/keys/`.
Agents report the tools they used, and several runs were asked afterwards whether they recognised the language.
Builders refuse to overwrite a folder a run has used, and `src/build_extra.py check` and
`src/cloze_families.py baseline` rebuild later tasks byte for byte from the repo.

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
while `qor-o`, `qorise`, `qorene` and `qorode` were targets; `mk` and `kdi` for `mkdi`; `mlo` for `smlo`) and that three
items shouldn't have been test words; the report gives the corrected numbers, and the builder now refuses such pairs.

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
spelling, marking uncertain signs, with the REM number (REM 0001–0137 follow Griffith's numbers). `src/expand.py`
drops texts already in the corpus (half or more of their word trigrams in one corpus text) and writes
`data/corpus_v3.jsonl`.

### 13. Review

Code changes were reviewed by a fresh Opus 5.5 reviewer that saw the diff and a context pack, never the author's
reasoning, and fixed what it found (three full reviews). The fourth review, of `src/lexique.py` and `src/expand.py`,
was stopped partway on Mike's word so the repo could be pushed; its unfinished edits are included, compile, and pass
the tests, but were not re-reviewed. They found and fixed answer
leaks, a Monte Carlo p-value printed as 0.0, a baseline that saw less than the solver, a corpus bug that split words
at doubtful-sign marks, a copy detector that missed copies, and rules applied outside the positions Rilly gives
them; each fix changed a reported number, and the report shows the corrected one. Tests: `tests/`.

## Reproduce

```bash
git clone https://github.com/Joshua-Otten/Meroitic-Corpus data/otten
python3 -I src/pool.py && python3 -I src/dedup.py && python3 -I src/collapse.py && python3 -I src/corpus.py && python3 -I src/clean_v2.py
python3 -I src/score.py --answers runs/answers
python3 -I src/cloze_families.py copies runs/answers/C3_cloze.json runs/cloze_families_ngram.json
python3 -I src/expand.py
python3 -I tests/test_harness.py && python3 -I tests/test_cognates_rules.py
```

## Layout

- `src/`: corpus cleaning, task builders, scorers, the synthetic language, cognate tests, lexicon test, merge.
- `data/`: cleaned corpora (`corpus_v2.jsonl`, `corpus_v3.jsonl`), answer keys, word lists, leads, discovery
  write-ups, the Griffith transcriptions, Rilly's lexicon (private).
- `runs/`: prompts, the task each blind run saw, its answers, keys and scores.
- `REPORT.md`: the results.

## Limits

- Blind tests on real Meroitic can't exclude memory: the model has read the decipherment literature.
- The synthetic language's difficulty depends on its generator.
- Judges and readers are the same model family; scoring files are kept line by line so a person can re-judge.
- Griffith's 1911–12 readings differ from the modern REM text in about 4% of signs; rows say they are Griffith's.
- Rilly 2007, Hintze's editions, REM and Hallof 2024 are print-only and were not read.
