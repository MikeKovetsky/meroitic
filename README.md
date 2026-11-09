# Meroitic: can a model find real structure?

A night's experiment (2026-11-08/09) on Meroitic, the language of ancient Kush.

- `data/otten/` is Otten & Anastasopoulos's public corpus (ALP 2025), cloned, not committed:
  `git clone https://github.com/Joshua-Otten/Meroitic-Corpus data/otten`.
- `src/pool.py`, `src/dedup.py`, `src/collapse.py` undo that corpus's name-swap augmentation
  (18,090 lines → 1,019 distinct texts, names masked as NAME / RNAME).
- `src/corpus.py` adds the three royal narratives and normalizes spelling → `data/corpus.jsonl`.
- `src/scramble.py` re-spells everything with a random letter swap (the blind condition).
- `src/build_tasks.py` builds the Step 0 matching tests; `src/score.py` scores them.
- `src/build_morph.py` builds the blind grammar (Kober) test.

Results and the write-up: `REPORT.md`.
