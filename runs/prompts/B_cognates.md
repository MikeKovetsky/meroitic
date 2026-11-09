# Task: a cognate engine built on regular sound correspondences

Meroitic is classified (Rilly 2010) in the Northern East Sudanic family with Nubian, Nara, Taman and Nyima. A first test in this repo compared Meroitic words with same-meaning words in that family by raw string similarity and found no signal once Rilly's own reconstructions (partly built from Meroitic) were left out (p = 0.12; `src/cognates.py`). Raw similarity is the wrong tool: cognates follow regular sound correspondences, not surface likeness. Your job is to build the right tool and test it honestly.

Inputs (all under /Users/mike/repos/mike/meroitic/):
- `data/nes/sound_correspondences.tsv` and `.md`: 82 Meroitic ↔ Nubian/NES correspondences from Rilly (2003 thesis table and later rules), with sources.
- `data/nes/*.tsv`: word lists for Old Nubian, Nobiin, Kenzi, Dongolawi, Midob, Birgid, Hill Nubian, Nara, Taman, Nyima (`form`, `gloss`, `source`), and `proto_nes.tsv` (Rilly's reconstructions: circular for validation, since they were built with Meroitic in view; keep them out of the validation, you may use them afterwards as a separate, labelled source).
- `data/gold_lexicon.json`: Meroitic words with accepted meanings (standard transliteration in `form`).
- `src/cognates.py`: the raw-similarity test, for comparison and reuse.

Do:
1. Write `src/cognates_rules.py`: map each Meroitic form to the set of expected reflex patterns under the correspondences (consonant classes and vowel rules), and score each NES word by how well it fits one of those patterns (an alignment that rewards regular correspondences and penalises irregular ones; ignore tone and length marks; handle the main transcription systems in the lists).
2. Validate honestly on the gold words, independent lists only: for each Meroitic word with a same-meaning NES word, take the best rule-based score; compare with 2,000 shuffles of the Meroitic meanings (the same design as `src/cognates.py`). Report p. Also report precision at the top: among the gold words, how often is the top-scoring NES word (over ALL meanings, not just the same meaning) one with the same meaning? Compare with raw similarity on the same data. Leave loanwords from Egyptian or Greek out of the validation (e.g. pelmos, peseto, apote, ant, kisri, tewisti) and say which you left out.
3. Only if the validation shows a real signal: apply the engine to these Meroitic words of unknown meaning, listing for each the 5 best-fitting NES words with their glosses and the correspondences used: temey, tros, tlt, teketi, kroro, aribet, ateqi, Sklte, mlekeyos, tmNteleb, Smlo, brtoye, kemxr, kiN, mlolo, yiroXe, womnitX, SSimete. (Corpus spelling: x and X are h-signs, S the s sign, N n-tilde, o o.) If the validation shows no signal, say so plainly and do not produce candidate lists.
4. Add plain-assert tests in `tests/test_cognates_rules.py` (runnable with `python3 -I tests/test_cognates_rules.py`) for the correspondence mapping and the scorer.

Write the results to `data/discovery/cognates_rules.md`: method, validation numbers, the comparison with raw similarity, and (if earned) the candidate lists, each marked as a hypothesis. Commit nothing; another reviewer will review the code. Do not modify files you did not create. No web access is needed beyond what the files hold; if you consult a source online, cite it. Work for at most about 75 minutes.

Final message: the validation numbers and whether the candidate lists were earned.
