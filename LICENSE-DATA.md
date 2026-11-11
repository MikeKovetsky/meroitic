# Licence for the data and the write-ups

Copyright (c) 2026 Mike Kovetsky. Everything in this repository that is not code is licensed under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/), except
the third-party material listed below. The code (`src/`, `tests/`, the scripts under `runs/work/`) is under the MIT
licence in [`LICENSE`](LICENSE).

Cite as: Mike Kovetsky, *Meroitic with Opus 5.5* (2026), <https://github.com/MikeKovetsky/meroitic>.

## What CC BY 4.0 covers

- **The Griffith transcriptions**, `data/expansion/griffith_*.jsonl`: 152 inscriptions read from the Meroitic type
  printed in Griffith's *Meroitic Inscriptions* I–II (1911–12) and *Meroë* (1911), which are in the public domain.
  Each row names its source, page, site and object, and 127 name a REM number; 29 are partial, as Griffith printed
  only part of the text. The readings are Griffith's, transcribed by a language model at a measured 95.6% sign
  accuracy against the modern edition (`data/expansion/printed_type_test.md`): cite Griffith for the reading and this
  repository for the transcription.
- **The Karanòg transcriptions**, `data/expansion/karanog/`: 151 inscriptions read from the hand copies in
  Griffith's *Karanòg: The Meroitic Inscriptions of Shablûl and Karanòg* (1911), which is in the public domain,
  and checked against the words he prints in type in the same book, at a measured 97.7% sign accuracy on the four
  texts a modern edition prints (`data/expansion/karanog/README.md`). With them: the 48 typed reference pages and
  the readers' files. The readings are Griffith's: cite Griffith for the reading and this repository for the
  transcription.
- The answer keys compiled from cited publications (`data/gold_lexicon.json`, `data/gold_morphology.json`), the
  synthetic corpus (`data/synth_corpus.txt`) and the transliteration map.
- The write-ups: `README.md`, `REPORT.md`, `NEXT_STEPS.md`, `data/discovery/`, `data/leads/`, the `.md` files under
  `data/expansion/`, and `docs/`.
- The runs: the prompts, answers, keys and scores under `runs/`, and the agents' readings under `runs/work/`.

## What it does not cover

Third-party material keeps its own terms, and CC BY 4.0 gives no rights in it:

- `data/nes/meroitic_wiktionary.tsv` comes from Wiktionary: CC BY-SA 4.0, share-alike.
- `data/discovery/egyptian_candidates.tsv` holds lemma numbers and lemma forms, unchanged, from two works under
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), so the file is under CC BY-SA 4.0,
  share-alike (the search picked which forms stand in it):
  - [*Thesaurus Linguae Aegyptiae*, Demotic sentences, corpus v18, premium](https://huggingface.co/datasets/thesaurus-linguae-aegyptiae/tla-demotic-v18-premium),
    v1.1, 2024, ed. by Tonio Sebastian Richter and Daniel A. Werning on behalf of the Berlin-Brandenburgische
    Akademie der Wissenschaften and Hans-Werner Fischer-Elfert and Peter Dils on behalf of the Sächsische Akademie
    der Wissenschaften zu Leipzig;
  - *Comprehensive Coptic Lexicon: Including Loanwords from Ancient Greek*, v1.2, 2020, by Dylan Michael Burns,
    Frank Feder, Katrin John, Maxim Kupreyev and others (Berlin-Brandenburgische Akademie der Wissenschaften and
    Freie Universität Berlin), doi:10.17169/refubium-27566, from [KELLIA's dictionary](https://github.com/KELLIA/dictionary);
    the licence is the one its own TEI header states.
- Readings quoted from *Fontes Historiae Nubiorum* II–III (Eide, Hägg, Pierce and Török, Bergen 1996–98, all rights
  reserved) as ground truth for the reading tests: about twenty short texts, each with its REM number, in
  `data/expansion/pilot.jsonl` (four), `data/expansion/printed_type_test.md`, `data/expansion/hand_copy_test.md` and
  the scoring scripts under `runs/work/`, some of them quoted again in `data/discovery/`.
- Glosses from Claude Rilly's *Lexique méroïtique* (2003 thesis, HAL tel-04793700), paraphrased in English for 68
  words as the answer key of the lexicon test: `runs/keys/lexique_*.json` and `runs/lexique_judge.json`.
- Short quotations from other publications in the write-ups, each cited where it stands.

Other data without an open licence is not in this repository: the README's Data section lists what is kept out.
