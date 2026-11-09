# Task: calibrated readings of unknown Meroitic words

Meroitic (ancient Kush) can be read aloud but is mostly not understood. Below are 31 frequent words or word-pieces whose meaning is not securely established. For each, work out from the corpus what it most likely means or does.

Inputs (all under /Users/mike/repos/mike/meroitic/):
- `data/corpus_v2.jsonl`: about 660 texts (mostly funerary, plus three royal narratives with ids hamadab, tanyidamani, kharamadoye). Spelling: o for o, x and X for the two h signs, S for the s sign, N for the n-tilde sign. Person names are masked as NAME, royal names as RNAME. Some texts are near-copies of one inscription; count texts, not tokens.
- `data/gold_lexicon.json` and `data/gold_morphology.json`: meanings and grammatical endings that ARE established. Use them as known.
- `src/kwic.py`: concordance, `python3 -I src/kwic.py WORD [--re] [--width 6] [--max 200]`.

Do NOT open `data/discovery/`, `data/leads/`, `runs/` (except to write your own answer) or `REPORT.md`: other analyses are kept there and this run must be independent of them. Do not use web search or fetch any page.

For each target:
1. Collect every context (kwic, including the target inside longer words where relevant).
2. Decide what slot it fills (title before a name, kin term, counted noun, verb, epithet, place, dating term...) and what its company says about its meaning.
3. Give your best reading as a short English gloss, plus up to two alternatives.
4. Give a confidence from 1 to 5, calibrated strictly: 5 = the texts force this reading; 4 = strong, consistent distributional evidence and one clear reading; 3 = plausible but other readings fit; 2 = weak; 1 = guess. In earlier tests on languages with known answers, readings at 4 or 5 were right every time, so only give 4 or 5 when the evidence would convince a sceptical specialist.
5. Separate what comes from the corpus from what you remember: field `corpus_evidence` (counts, contexts, parallels, with text ids) and field `recalled` (any published gloss you remember for this word and whose it is, or "none"). Your confidence must rest on the corpus evidence alone.

Targets: wetrri (with its variant qetrri), wetNyiNqeli, temey (with temeylX), keN, tros, tlt, teketi, plSn, SlXS, SSimete, Stmdes, kroro, qoreN, womnitX, aribet, ateqi, Sklte, mlekeyos, tmNteleb, Smlo, brtoye, kemxr, penn, kiN, mlolo, Sq, yiroXe, qorete, SSor, tbo, perite.

Write JSON to `OUTFILE`:
{"readings": [{"word": "...", "slot": "...", "reading": "...", "alternatives": ["...", "..."], "confidence": 1, "corpus_evidence": "...", "recalled": "..."}]}

Final message: a table of word, reading and confidence, then one line listing the tools you used.
