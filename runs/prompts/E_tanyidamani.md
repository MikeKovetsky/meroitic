# Task: an interlinear reading of the Tanyidamani stela

The royal stela of King Tanyidamani (REM 1044, Gebel Barkal, now Boston MFA 23.736, about 100 BC) is one of the longest Meroitic texts and one of the least understood. Your job: push its understanding as far as the evidence goes, and be strict about what is established, proposed or guessed.

Inputs (all under /Users/mike/repos/mike/meroitic/):
- `data/corpus_v2.jsonl`, row with id `tanyidamani` (spelling: o for o, x and X the two h signs, S the s sign, N n-tilde; doubtful-sign stars removed), and the original file `data/otten/Data/TanyidamaniNarrative.txt` (stars and brackets kept).
- `data/gold_lexicon.json`, `data/gold_morphology.json`: established meanings and endings.
- `data/discovery/hamadab.md`: an earlier reading of the related Hamadab stela REM 1003 (shared formulas: abrse l yekedi kdise l arse li ..., counted captives, Amun of Napata), and `data/discovery/verification.md`: what an adversarial check found already published (learn from it: Millet 1968 glosses are in `data/otten/Data/MilletExamples.txt`; Hofmann 1981 and FHN commentary often anticipate "new" ideas).
- `src/kwic.py` for parallels in the rest of the corpus.
- Online: Rilly's Dotawo 7 article "Personal Markers and Verbal Number in Meroitic" (https://pages.sandpoints.org/dotawo/article/rilly), the open-access Fontes Historiae Nubiorum volumes (FHN II covers REM 1044), Rilly's HAL papers, and anything else you find. No accounts or credentials.

Do:
1. Segment the text into sections (it alternates narrative with lists of offerings counted with numerals, and long name/title sequences).
2. An interlinear gloss of the whole text: each word or morpheme with its established meaning (cite the gold entry or the publication), a labelled HYPOTHESIS where you propose one, "?" where nothing can be said.
3. The structure that the parallels reveal: repeated phrases, list formulas (item + numeral; `wi` + total), the god and place names, the verbs. Check each pattern against the corpus (kwic).
4. A short list of hypotheses for words or phrases, each with evidence, alternatives, confidence 1–5 and a test. Before labelling anything NEW, try hard to find it already published (FHN II commentary, Rilly 2007 via any quotation, Millet's glossary, Hofmann, Hintze, Griffith 1912 "Meroitic Inscriptions II", Priese, Török); label ESTABLISHED, PUBLISHED HYPOTHESIS (who, where, link) or NEW (what you searched).
5. A plain-English summary of what the stela says, as far as it can be said, marking every uncertain part.

Write `data/discovery/tanyidamani.md`. Do not modify any other file. Work for at most about 75 minutes.

Final message: the plain-English summary in 5–8 sentences, and the counts per label.
