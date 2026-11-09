You are helping with an open research question: can a careful reader push the understanding of Meroitic (language of ancient Kush) further using the texts we have? This task is the royal narrative of the Hamadab stela of Queen Amanirenas and Prince Akinidad (REM 1039), which scholars think describes the war with Rome in 25–21 BC.

Inputs (all under /Users/mike/repos/mike/meroitic/):
- `data/corpus.jsonl`: the corpus; the stela is the row with id `hamadab` (spelling: o for o, x and X for the two h signs, S for the s sign, N for n-tilde; FHN-style transcription that often separates morphemes with spaces). The Tanyidamani and Kharamadoye narratives are also there.
- `data/otten/Data/HamadabStelaOfAmanirenasNarrative.txt`: the same text with brackets and stars (doubtful signs) kept.
- `data/gold_lexicon.json` and `data/gold_morphology.json`: accepted meanings and morphemes with sources.
- `data/leads/`: the Roman-side accounts (Strabo 17.1.54, Cassius Dio, Pliny, Res Gestae) and published proposals about this stela, if present.
- `src/kwic.py`: a concordance tool: `python3 src/kwic.py WORD [--re] [--src narrative]`.

Do:
1. Segment the stela into its repeated sections (it repeats a pattern three times with numbers: abr 32 kdi 135, abr 100 kdi 100, abr 58 kdi 223, then wi 1626 and wi 1032).
2. Produce an interlinear gloss of the whole text: each word or morpheme with its accepted meaning where one exists (cite the gold entry), a labelled HYPOTHESIS where you propose one, and "?" where nothing can be said. Never present a hypothesis as accepted.
3. Align the sections with the Roman account: places (Syene, Elephantine, Philae, Pselchis/Dakka, Primis/Qasr Ibrim, Napata), the captives and statues, the numbers, the treaty. Build a table: Meroitic section ↔ Roman event, with how strong the match is.
4. From that alignment, list concrete new hypotheses (a word's meaning or a morpheme's function), each with: the evidence lines, the alternatives, a confidence, and a test (another text or context where the hypothesis predicts something checkable). Check every one against the literature with web search: say whether it was already proposed and by whom (Rilly, Hallof, Török, Millet, Hintze, Griffith, Priese, Hofmann, Kuckertz), with a link. Only call something new if you searched and found no prior proposal, and say what you searched.

Write `data/discovery/hamadab.md` (create the folder). Be strict: the value of this file is that a specialist can trust which parts are established and which are guesses. Work for at most about 60 minutes.

Final message: the five strongest hypotheses with their status (new / already proposed by X), and anything in the inputs you found wrong.
