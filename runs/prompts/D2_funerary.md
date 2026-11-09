You are helping with an open research question: can a careful reader push the understanding of Meroitic (language of ancient Kush) further using the texts we have? This task is the funerary inscriptions, which make up most of the corpus.

Inputs (all under /Users/mike/repos/mike/meroitic/):
- `data/corpus.jsonl`: about 1,000 funerary texts (src "funerary") plus three royal narratives. Spelling: o for o, x and X for the two h signs, S for the s sign, N for n-tilde. Person names are masked as NAME (royal names as RNAME), because the published corpus had been padded with name-swapped copies.
- `data/gold_lexicon.json` and `data/gold_morphology.json`: accepted meanings and morphemes, with sources.
- `src/kwic.py`: concordance tool: `python3 src/kwic.py WORD [--re] [--src funerary]`.

Do:
1. Find the 30 most frequent words or recurring word-pieces in the funerary texts whose meaning is NOT in the gold files (titles and offices count; masked names do not).
2. For each: all its contexts (use kwic), its position in the formula (invocation, name, filiation, relationship/career section, benediction), what it co-occurs with, and a proposed meaning or function with the evidence, alternatives and a confidence 1 to 5.
3. Check each against the literature with web search (Rilly 2007 and 2010, Rilly & de Voogt 2012, Hintze, Griffith, Millet, Török, Hallof, the Meroitic Newsletter, Kuckertz), and give the published view with a link when there is one. Label every item: ESTABLISHED (published, accepted), PUBLISHED HYPOTHESIS (published, debated), or NEW (you searched and found no published proposal; say what you searched).
4. Note any place where the corpus file looks wrong (spacing, a mis-transcription, a name that slipped through the masking).

Write `data/discovery/funerary.md` (create the folder). Be strict: never present a guess as accepted. Work for at most about 60 minutes.

Final message: counts per label, and the five most interesting NEW items with their evidence in one line each.
