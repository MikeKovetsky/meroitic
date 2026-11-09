# Licence for the data and the write-ups

Copyright (c) 2026 Mike Kovetsky. Everything in this repository that is not code is licensed under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/), except
the third-party material listed below. The code (`src/`, `tests/`, the scripts under `runs/work/`) is under the MIT
licence in [`LICENSE`](LICENSE).

Cite as: Mike Kovetsky, *Meroitic with Opus 5.5* (2026), <https://github.com/MikeKovetsky/meroitic>.

## What CC BY 4.0 covers

- **The Griffith transcriptions**, `data/expansion/griffith_*.jsonl`: 152 inscriptions read from the Meroitic type
  printed in Griffith's *Meroitic Inscriptions* I–II (1911–12) and *Meroë* (1911), which are in the public domain.
  Each row names its source, page, site, object and REM number. The readings are Griffith's, transcribed by a
  language model at a measured 95.6% sign accuracy against the modern edition (`data/expansion/printed_type_test.md`):
  cite Griffith for the reading and this repository for the transcription.
- The answer keys compiled from cited publications (`data/gold_lexicon.json`, `data/gold_morphology.json`), the
  synthetic corpus (`data/synth_corpus.txt`) and the transliteration map.
- The write-ups: `README.md`, `REPORT.md`, `NEXT_STEPS.md`, `data/discovery/`, `data/leads/`, the `.md` files under
  `data/expansion/`, and `docs/`.
- The runs: the prompts, answers, keys and scores under `runs/`, and the agents' readings under `runs/work/`.

## What it does not cover

Third-party material keeps its own terms, and CC BY 4.0 gives no rights in it:

- `data/nes/meroitic_wiktionary.tsv` comes from Wiktionary: CC BY-SA 4.0, share-alike.
- Readings quoted from *Fontes Historiae Nubiorum* II–III (Eide, Hägg, Pierce and Török, Bergen 1996–98, all rights
  reserved) as ground truth for the reading tests: four texts in `data/expansion/pilot.jsonl` and about twenty short
  texts in the scoring scripts under `runs/work/`, each with its REM number.
- Glosses from Claude Rilly's *Lexique méroïtique* (2003 thesis, HAL tel-04793700), paraphrased in English for 68
  words as the answer key of the lexicon test: `runs/keys/lexique_*.json` and `runs/lexique_judge.json`.
- Short quotations from other publications in the write-ups, each cited where it stands.

Data without an open licence is not in this repository at all: the README's Data section lists what is kept out.
