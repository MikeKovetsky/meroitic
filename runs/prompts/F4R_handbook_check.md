<!-- F4, the rounds (data/discovery/f4_rounds.md): the instructions given by hand on 13 November 2026 to the
four agents that checked the handbook, word for word but for FROM, TO, PART and EXAMPLE: part 1, lines 11 to
34 (example 17); part 2, lines 35 to 78 (41); part 3, lines 79 to 119 (81); part 4, lines 120 to 172 (122).
`python3 -I src/f4r.py handbook` applies their answers (data/sources/f4r/handbook_check/, local). -->

You are checking a sourced handbook of Meroitic grammar line by line against the sources it cites. Another agent compiled it; translators will rely on it, so a line that says more than its source, or something else, must be caught.

Working directory: /Users/mike/repos/mike/meroitic
The handbook: `data/sources/f4r/handbook.md` (172 lines). Read its first 10 lines for how pages, certainty labels and letters are written. Do NOT edit the handbook.

## Your part

Check every line from line FROM to line TO (inclusive) that ends in a bracketed source, for example `[Rilly 2003, p. 117, established]`. For each such line:

1. Open the cited page or pages of the cited source and read what it says.
2. Decide: does the source state what the line states (the form, the function or meaning, the example and its word-by-word reading), and does the certainty label match the source (for Rilly 2003 the entry's own status; for the others the source's wording, as the handbook's "How sure" line defines it)?
3. Give one verdict:
   - "confirmed": the source says it and the label fits;
   - "corrected": the line is partly right; give the full corrected line, saying only what the source says, with the right pages and label;
   - "unsupported": you cannot find the statement at the cited place or anywhere near it in that source.

## Where the sources are (local text files; use grep to find a form or a page)

- Rilly 2003: `data/rilly2003/lexique_*.jsonl`, typed entries with fields such as headword, page, status, meaning, proposals. An entry's `page` is the printed page; its `status` is established, probable, hypothesis (the handbook's "proposal") or unknown.
- Rilly 2021: `data/sources/dotawo-text/pages.txt` (page markers `=== page N ===`; the handbook cites these marker numbers).
- FHN II: `data/sources/fhn2-text/pages.txt`; FHN III: `data/sources/fhn-text/pages.txt`; FHN IV: `data/sources/fhn4-text/pages.txt`. The handbook cites printed pages, which stand in the running heads of the text; the `=== page N ===` markers are PDF pages and differ.
- Griffith 1911 (Karanòg): `data/sources/karanog-text/pages.txt`; Griffith MI I and II: `data/sources/griffith-mi1-text/pages.txt`, `data/sources/griffith-mi2-text/pages.txt`. Printed pages again; Griffith writes ê for o and z for d, and his Meroitic type is not in the text layer.
- Lipiński 2011: `data/sources/lipinski2011-text/pages.txt`.
- The project's pages: `data/discovery/funerary.md`, `data/discovery/coverage.md`.

## What you must not do (a blind test depends on it)

- Do NOT open anything under `data/sources/jssea`, `data/sources/jssea-text`, `data/sources/expert`, `data/sources/f4`, `data/sources/f4r/split`, `data/sources/v6`, `data/sources/coverage`, or the files `data/discovery/experts.md`, `data/discovery/f4_pilot.md`, `data/discovery/f4_rounds.md`, `data/discovery/lexicon.md`.
- Do not use or add any statement a source attributes to Millet, and do not write his name. If a line you check rests on Millet alone in its source, its verdict is "unsupported" with the reason "rests on a withheld source".
- Do not search the web, do not run the project's scripts or tests, do not commit, and do not change any file but your answers file.
- Do not add knowledge of your own: a corrected line may say only what the cited source says.

## Your answer

Write JSON lines to `data/sources/f4r/handbook_check/partPART.jsonl`, one line per handbook line you checked, in order, nothing else in the file:

    {"line": EXAMPLE, "verdict": "confirmed", "text": "", "why": "at most twenty words: what the source says"}

For "corrected", "text" holds the whole corrected line exactly as it should stand in the handbook (starting with its "- " if it had one). For the others "text" is "".

Then reply in under 100 words: how many lines you checked, how many of each verdict, and anything you could not check.
