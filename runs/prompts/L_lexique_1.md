# Task: extract Rilly's 2003 Meroitic lexicon, pages 1 to 51

Claude Rilly's thesis "Le méroïtique. Données grammaticales, lexicales, position linguistique", vol. II "Lexique méroïtique" (EPHE 2003, HAL tel-04793700) is the fullest open lexicon of Meroitic. It is a scanned PDF with no text layer: `/private/tmp/claude-501/-Users-mike--claude-spares-spare-HctKIa/8d71d8e2-2a2b-4d11-9e18-5d4c3de9a504/scratchpad/rilly_lex/lex.pdf` (304 PDF pages; the printed page number is about one less than the PDF page).

Your range: PDF pages 1 to 51. Extract each page's scan with:

    /Users/mike/repos/mike/viewfy/backend/.venv/bin/python -I -c "import pypdf,sys; r=pypdf.PdfReader(sys.argv[1]); [open(f'{sys.argv[2]}/p{i:03d}.jpg','wb').write(r.pages[i-1].images[0].data) for i in range(int(sys.argv[3]),int(sys.argv[4])+1)]" /private/tmp/claude-501/-Users-mike--claude-spares-spare-HctKIa/8d71d8e2-2a2b-4d11-9e18-5d4c3de9a504/scratchpad/rilly_lex/lex.pdf OUTDIR 1 52

with OUTDIR a new folder `/private/tmp/claude-501/lexique_1/`, then look at each page image with the Read tool.

For every lexicon entry that STARTS on a page in your range, write one JSON object per line to `/Users/mike/repos/mike/meroitic/data/rilly2003/lexique_1.jsonl`:

{"headword": "mdese", "variants": ["medese"], "category": "substantif", "meaning_fr": "relation (de parenté ?) entre un membre de la famille royale et une divinité", "meaning_en": "a relation between a royal and a god, probably 'direct descendant'", "status": "probable", "rilly_view": "follows Millet's 'direct descendant'", "proposals": [{"author": "Griffith 1912", "proposal": "of the seed (or kin) of"}, {"author": "Hofmann", "proposal": "protection"}, {"author": "Millet", "proposal": "direct descendant"}], "rem": ["0034A-D", "0084", "0088"], "page_pdf": 121, "page_printed": 120}

Rules:
- `headword` exactly as printed (Rilly's transliteration, with its diacritics: ḫ, ẖ, ñ, š etc.). `variants` from "(var. ...)".
- `category` as printed (substantif, verbe, titre, nom propre, toponyme, théonyme, adjectif, morphème, particule...).
- `meaning_fr`: Rilly's own meaning, short, in his words; "" if he gives none. `meaning_en`: a faithful short English rendering; "" if none.
- `status`: "established" if Rilly presents the meaning as secure; "probable" for "probablement / vraisemblablement / sans doute"; "hypothesis" for "peut-être", a question mark, or competing proposals he leaves open; "unknown" if only the category or context is given ("titre", "sens inconnu").
- `proposals`: other scholars' proposals as he reports them (author + short proposal), including ones he rejects.
- `rem`: the REM numbers he cites for the word.
- If an entry continues onto the next page, read the next page to finish it (that is why your extraction runs one page past 51). Skip text at the top of page 1 that continues an entry from the page before (unless 1 is 1). Skip front matter, abbreviation lists and bibliography pages, but if they contain a conventions table for transliteration, note it in your final message.
- Copy faithfully; do not add meanings from your own knowledge. If a passage is unreadable, put "[illegible]".

Do not modify any other file. This is for private research analysis; do not post the content anywhere.

Final message: number of entries written, the first and last headwords, any page you could not read.
