You are helping with an open research question: can a careful reader push the understanding of Meroitic (language of ancient Kush) further using the texts we have? This task is the closest thing Meroitic has to bilingual material: the Philae and Dodecaschoenus inscriptions, where the same Meroitic envoys and officials appear in Meroitic texts and in Demotic or Greek ones.

Inputs (all under /Users/mike/repos/mike/meroitic/):
- `data/leads/README.md` and `data/leads/01-philae-dodecaschoenus.md`: the texts and the person/title pairings found so far (8 persons, 24 titles/words/names), with sources (FHN III, Ashby 2016, Griffith 1911). Also `04-foreign-renderings.md`.
- `data/gold_lexicon.json`, `data/gold_morphology.json`: accepted meanings and morphemes with sources.
- `data/corpus.jsonl` and `src/kwic.py` (`python3 src/kwic.py WORD [--re]`): the wider corpus, to check how words in the Philae texts behave elsewhere. Spelling there: o for o, x and X the two h signs, S the s sign (Millet's s-hat), N n-tilde; names are masked as NAME. FHN uses standard transliteration, so map between them.

Do:
1. For each Meroitic Philae text whose author or subject also appears in a Demotic or Greek text, set the two side by side: the Meroitic transliteration with known words glossed, and the Demotic/Greek translation. Mark which parts of the Meroitic text must refer to the same facts (titles, offices, the mission to Rome, offerings, the king who sent them, years).
2. From those alignments, list concrete hypotheses for Meroitic words or phrases whose meaning is not in the gold files: each with the aligned evidence, alternatives, a confidence 1 to 5, and a check elsewhere in the corpus (kwic) that supports or weakens it.
3. Check each hypothesis against the literature with web search (Rilly, Pope, Ashby, Hofmann, Török, Griffith, Burkhardt, Cruz-Uribe, Hallof). Label it ESTABLISHED, PUBLISHED HYPOTHESIS (with who and a link) or NEW (say what you searched). Never present a guess as accepted.

Write `data/discovery/philae.md` (create the folder if needed). Work for at most about 60 minutes.

Final message: counts per label and the five strongest hypotheses, one line each with their status.
