# Next steps

Written 2026-11-09, after two days of runs. Ordered by what they would change; each says why, how, the cost and
what "done" looks like. Results so far: [`REPORT.md`](REPORT.md); methods: [`README.md`](README.md).

## A. Grow the corpus (the binding constraint)

1. **Karanòg by consensus transcription** (about 150 funerary texts, the largest single gain).
   - Why: the corpus lacks the whole Karanòg cemetery; one reader reads Griffith's hand copies at 88.8% (91.1% on
     clearly drawn signs), with errors in names and rare titles and most of them unflagged
     (`data/expansion/hand_copy_test.md`).
   - How: two independent readers per text; every sign where they disagree, and every 3-shaped (m, ẖ, s, q) and
     long-tailed sign, goes to a third look beside a sheet of this scribe's forms; then check each rare word against
     the spellings Rilly cites with that REM number (Karanòg N = REM 0200+N) in `data/rilly2003/`.
   - Test first: score the consensus pipeline on Kar. 47, 77, 78 and 121 with fresh agents. The bar is 95% of
     signs; a rule sheet built from those four texts' errors overfits them, so state that, or hold one text out.
   - Cost: about 1 hour for the test, 2 to 3 hours for 150 texts with 3 readers each. Done: `griffith_karanog.jsonl`,
     merged by `src/expand.py`, with the measured accuracy in its notes.
2. **Faras funerary texts** (46, Griffith 1922, hand copies, archive.org `bibliothquedel234ecol`): same pipeline
   once Karanòg passes.
3. **FHN's modern transliterations** (about 30 texts, `/private/tmp/claude-501/expansion/survey/fhn/` holds the OCR):
   clean modern readings, the quickest gain. FHN is "all rights reserved": fine for this private analysis, not for
   republishing.
4. **Griffith's JEA "Meroitic Studies"** (about 45 ostraca printed in Latin letters): OCR, then check every word
   against the page image.
5. **A glyph classifier for Griffith's type** (23 forms): would replace agent reading for the remaining printed
   texts and cut the cost to near zero; the 12 scored texts in `runs/work/griffith/` are its test set.
6. **Mask names in the Griffith rows** the way `corpus_v2` masks them, so frequency counts in `corpus_v3` mean the
   same thing; and relax `src/expand.py`'s duplicate test, which counts a short label inside a longer text as
   present (the +86 texts are a lower bound).

## B. Re-run the measurements cleanly

7. **Rebuild and rerun the corpus meaning test** with the fixed builder (`src/lexique.py` now refuses a glossary
   that gives a target away) instead of removing leaked items afterwards; judge again. Cost: about 40 minutes.
8. **Does more data help?** Rerun the same test on `corpus_v3` (and on a corpus with Karanòg once it exists) and
   compare with `corpus_v2`: the cleanest answer to whether the bottleneck is data.
9. **Finish the stopped review** of `src/lexique.py` and `src/expand.py` (stopped on Mike's word to push), and add
   `tests/test_lexique.py`.
10. **A second synthetic language** with a different generator (other formula types, number-conditioned plurals) to
    check that the 79–83% matching rate isn't an artefact of one design.

## C. Specialists

11. **Tell Joshua Otten** (George Mason University) that the public Meroitic-Corpus is padded with name-swapped
    copies: 18,090 lines are 662 distinct texts (`src/pool.py` shows the two swap pools).
12. **Send the two open leads** to a specialist (Claude Rilly, CNRS; Stefan Hallof; Henriette Ashby):
    - `wi` before a numeral marks a total: in the Tanyidamani stela, `mk lte wi 12` follows exactly twelve items
      each counted "1" (Hofmann 1981 found a sum on REM 1003; check Hintze 1960 first);
    - the vocative `-i` placed at the end of "god + epithet" (Osiris is never `Soreyi` before an epithet in 11 texts;
      Rilly published the "Isis + Osiris" case; check Rilly & de Voogt 2012, p. 155, and Heyler 1964).
    Any future "new" claim goes through the adversarial check first (`data/discovery/verification.md` shows how),
    and now also through Rilly's lexicon in `data/rilly2003/`.

## D. Lower priority

13. **Cognates:** the sound-law engine found no signal on held-out words. A real test needs more independent NES
    vocabulary (culture and kin words are missing for most languages) rather than a better scorer.
14. **Publishing:** the repo is private because `data/rilly2003/` is an extraction of Rilly's thesis and
    `data/corpus*.jsonl` derive from a corpus with no licence. A public version would drop `data/rilly2003/`,
    `runs/tasks/` and the derived corpora, or get permission first.
