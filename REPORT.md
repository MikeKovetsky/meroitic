# Meroitic overnight: what a 2026 model can and can't do

Night of 2026-11-08/09, about five hours, Opus 5.5 subagents. Everything below is reproducible from `src/` and
`runs/`; every claim names the run it comes from.

## Answer first

1. **Opus 5.5 already knows the published Meroitic vocabulary.** On 35 accepted words it matched every meaning
   from memory alone (35/35), and again with the corpus (35/35). Asked openly, with no options, it recalled 52 of
   82 published words and said "unknown" to 30 (`runs/recall_open.json`).
2. **So the planned blind test can't be run on Meroitic.** Re-spelling the corpus with a random letter swap hides
   nothing: given only a 17-word glossary and no texts, the model broke the cipher and scored 35/35 (`S0_f0`,
   `S0_f1`). With the texts, the runs said outright they recognised Meroitic (`S_f0`, `S_f1`).
3. **On a language it cannot know, it still infers meanings from context.** On a synthetic corpus of the same size
   and texture (1,003 texts, 16k words, invented vocabulary), it matched RESULT_Y meanings where chance is about 2,
   and every high-confidence answer was right (`Y_f0`, `Y_f1`).
4. **Blind, it rebuilt much of the published grammar** from the scrambled corpus: the article -l and its plural
   -leb, the plural -b-, genitive -s, vocative -i, the demonstrative qo "this", the predicate ending -lowi split into
   its parts, the plural copula -kwi, the p- prefix of the benediction verbs, and the rule that the a-sign only
   starts words (`K_morph`; clean rerun `K2_morph`: RESULT_K2).
5. **Discovery:** three new, checkable proposals from the funerary texts and RESULT_D1D3 from the war stela and the
   Philae bilinguals, each labelled ESTABLISHED / PUBLISHED HYPOTHESIS / NEW after a literature search
   (`data/discovery/`). None is a decipherment; all need a specialist.

## The corpus

- The public corpus (Otten & Anastasopoulos, ALP 2025) has 18,090 lines, but it is padded: each text repeats with
  person names swapped from two pools (178 private names, 11 royal). Undoing that leaves 665 texts, about 19,700
  words (`src/pool.py`, `src/dedup.py`, `src/collapse.py`, `src/clean_v2.py`). The funerary study counts 442
  distinct funerary texts in 306 families.
- Two blind runs found leftovers my cleaning missed (17 multi-word names, then 5 name tails). The cloze run even
  worked out how the padding was made and used it.

## Tests

| Test | What it asks | Result |
|---|---|---|
| Matching, memory only (`M_f0/1`) | 35 words → 35 meanings, no texts | 35/35 |
| Matching, real texts (`R_f0/1`) | same, with the corpus | 35/35 |
| Matching, scrambled texts (`S_f0/1`) | same, letters swapped | 35/35, recognised Meroitic |
| Matching, scrambled, no texts (`S0_f0/1`) | glossary + words only | 35/35, cracked the cipher |
| Open recall (`F_recall`) | 82 words, no options | 52 answered, 30 unknown |
| Natural experiment (`N_open`) | the 17 unrecalled words, from the texts | RESULT_N |
| Synthetic language (`Y_f0/1`) | 56 invented words, from the texts | RESULT_Y |
| Restoration (`C2_cloze`) | 88 masked words in unseen contexts | RESULT_C2 vs n-gram 28/88 |
| Grammar, blind (`K_morph`, `K2_morph`) | scrambled corpus, no meanings | see above |

RESULT_DETAILS
