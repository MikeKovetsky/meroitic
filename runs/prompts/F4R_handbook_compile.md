<!-- F4, the rounds (data/discovery/f4_rounds.md): the instructions given by hand on 13 November 2026 to the
one agent that compiled the handbook, word for word. Its answer is data/sources/f4r/handbook_compiled.md (local). -->

You are compiling a short, sourced handbook that translators of Meroitic inscriptions will work from. Meroitic (kingdom of Kush, about 300 BC to AD 350) can be read aloud but is understood only in part. The handbook must state only what the sources below state, each statement with its source and page, and must say how sure each statement is.

Working directory: /Users/mike/repos/mike/meroitic

## What to write

One file: `data/sources/f4r/handbook.md` (create it; nothing else may be written anywhere). 2,500 to 4,000 words, plain Markdown, in this order:

1. **The noun phrase and its endings**: the determiner (-l, plural -leb), the genitive, the locative (-te), the dative or other case-like endings, the plural marker -b-, the copula (-o, as in -lowi = -l-o-wi; plural -lebkwi / -kwi), the vocative -i, and any other ending the sources treat as established or probable. For each: its form, what it does, one example with a word-by-word reading, the source and page, and whether the source calls it established, probable or a proposal.
2. **How an epitaph is built**, part by part, with the usual formula of each part and how it is read: the invocation of Isis and Osiris; the naming of the dead (the word qo / qowi and how scholars read it, with the dispute); the mother and the father (the verbs of filiation such as te-dḫe-lowi and t-erike-lowi); the "description" phrases that relate the dead to relatives who hold titles (yetmde, mde, kdite / kdise, ste, sem, wide and the like, with what each kin term is taken to mean and by whom, and how such a phrase is ordered: title, place, name, kin term, copula); and the closing benedictions (the lettered formulae A, B, C and so on, each with its usual wording, what is understood of it, and which words in it are still not understood).
3. **Titles and offices** that recur (for example pqr, peseto, pelmos, perite, ant, qorene, apote, beloloke, kroro, slẖs, ḫrpḫe / xrpxe, wyekiye-type names are NOT titles): for each, the meaning the sources give and how sure, in one line.
4. **Gods and places** that recur, each in one line: the Meroitic form, the god or the place, the modern or Greek/Egyptian name where the source gives it.
5. **Royal and temple texts, graffiti, documents**: what little is established about how they are built (regnal formulae, lists with numerals, verbs of giving or dedicating), in a short section.
6. **What a translator must not assume**: a short list of readings that are popular but disputed or unproven according to these sources.

Use the project's transliteration in examples: S is the sign s, s the sign se, N the sign ne, X the sign ẖ, x the sign ḫ; a dot is a lost sign. Where a source writes ḫ, ẖ, ñ, š, ê or z (Griffith's older values), give the project's letters and say so once at the top.

Every line that states a meaning or a rule ends with its source in brackets, for example `[Rilly 2003, p. 117, established]` or `[Rilly 2021, p. 12]` or `[Griffith 1911, p. 34]` or `[FHN III, p. 912]`. If two sources differ, give both. If you cannot find a source for something you believe, leave it out. Do not fill gaps from your own knowledge of Meroitic: a shorter handbook that is all sourced is better than a longer one that is not.

## Sources you may read (all local text files; read what you need, use grep to find passages)

- `data/rilly2003/lexique_*.jsonl`: Rilly's lexicon of 2003 as typed entries (headword, kind, status, page, meaning, other scholars' proposals). The entries whose headword starts with "-" are endings; kinds include "function word", "title", "noun", "verb", "place name", "god name".
- `data/sources/dotawo-text/pages.txt`: Rilly 2021, "Personal Markers and Verbal Number in Meroitic" (Dotawo 7), page by page.
- `data/sources/fhn2-text/pages.txt`, `data/sources/fhn-text/pages.txt` (FHN III), `data/sources/fhn4-text/pages.txt` (FHN IV, the index volume): Fontes Historiae Nubiorum, with its editors' comments on Meroitic texts. FHN III and IV are the useful ones for Meroitic.
- `data/sources/karanog-text/pages.txt`: Griffith 1911, Karanòg: The Meroitic Inscriptions of Shablûl and Karanòg, with his chapters on the formulae of the epitaphs.
- `data/sources/griffith-mi1-text/pages.txt` and `data/sources/griffith-mi2-text/pages.txt`: Griffith, Meroitic Inscriptions I and II (1911, 1912).
- `data/sources/lipinski2011-text/pages.txt`: Lipiński 2011, a review article on Rilly's 2010 book.
- `data/discovery/funerary.md` and `data/discovery/coverage.md`: the project's own pages on the funerary formulae and on what the word-by-word map covers.

## What you must not read or use (this is a blind test)

The translators will be scored against the renderings of one scholar, N. B. Millet, of the inscriptions from Gebel Adda. So:

- Do NOT open anything under `data/sources/jssea`, `data/sources/jssea-text`, `data/sources/expert`, `data/sources/f4`, `data/sources/f4r` (other than writing your handbook there), `data/sources/v6`, `data/sources/coverage`, or `data/discovery/experts.md`, `data/discovery/f4_pilot.md`, `data/discovery/lexicon.md`.
- Do NOT use or cite any statement that a source attributes to Millet, and do not mention Millet in the handbook. If an entry of the lexicon gives a meaning only on Millet's authority, leave it out.
- Do NOT write anything about a particular inscription from Gebel Adda (ids starting with GA).
- Do not search the web, and do not run the project's scripts or tests. Do not commit or change anything else in the repository.

## When you are done

Reply with: the word count of the handbook, how many statements carry a source, which of the six sections came out thin and why, and any source you could not open. Keep the reply under 200 words.
