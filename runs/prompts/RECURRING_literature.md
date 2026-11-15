# What the sources in hand say about the recurring open words: the brief of the literature pass

Meroitic (kingdom of Kush, about 300 BC to AD 350) can be read aloud but is understood only in part. The project's
word-by-word map of its corpus (548 inscriptions) leaves 154 spellings without an accepted meaning that stand in
three texts or more. They are grouped into 121 items: an entry of Rilly's lexicon of 2003, or a spelling that
lexicon does not hold. Your batch file lists some of these items, each with its spellings, what the lexicon of 2003
records, and up to twelve of the places where it stands.

Your task: for each item of your batch, find what the sources below say about it, and report it with quotes copied
exactly from the files. This pass collects; it does not decide and it does not propose. Do not give a meaning of
your own, and do not state anything from your own knowledge of Meroitic: only what these files say.

## The sources (all local; use grep or a short script to search; paths are from the repository's root)

| Name to use | File | Notes |
|---|---|---|
| Rilly 2003 | `data/rilly2003/lexique_*.jsonl` | Typed entries of his lexicon: headword, kind, status, page, meaning, proposals. The batch file already gives the entry of each item; look for other entries that speak of it |
| Rilly 2016 | `data/sources/rilly2016-text/pages.txt` | "Meroitic", UCLA Encyclopedia of Egyptology: his overview, with the words he counts as translated |
| Rilly 2021 | `data/sources/dotawo-text/pages.txt` | "Personal Markers and Verbal Number in Meroitic": the verbs and endings of the blessings |
| FHN II, FHN III, FHN IV | `data/sources/fhn2-text/pages.txt`, `data/sources/fhn-text/pages.txt`, `data/sources/fhn4-text/pages.txt` | Fontes Historiae Nubiorum: comments on Meroitic texts; IV has indexes of Meroitic titles and words with glosses |
| Griffith 1911 | `data/sources/karanog-text/pages.txt` | Karanòg: his chapters on the formulae, titles and names |
| Griffith MI I, Griffith MI II | `data/sources/griffith-mi1-text/pages.txt`, `data/sources/griffith-mi2-text/pages.txt` | Meroitic Inscriptions I and II |
| Meroe 1911 | `data/sources/meroe1911-text/pages.txt` | Garstang, Sayce and Griffith |
| Griffith MS I to IV | `data/sources/griffith-jea-text/*` | Meroitic Studies I to IV (1916 to 1917) |
| Griffith MS V, Griffith MS VI | `data/sources/survey-text/jea/in.ernet.dli.2015.70984.txt`, `data/sources/survey-text/jea/in.ernet.dli.2015.70988.txt` | Whole journal volumes without page markers: search for "Meroitic Studies"; give page 0 |
| Millet 2005 | `data/sources/jssea-text/pages.txt` | The Meroitic Inscriptions from Gebel Adda: texts, comments and renderings |
| Lipinski 2011 | `data/sources/lipinski2011-text/pages.txt` | A review article on Rilly 2010 |
| Project | `data/discovery/funerary.md`, `data/discovery/coverage.md`, `data/discovery/hamadab.md`, `data/discovery/tanyidamani.md`, `data/discovery/philae.md`, `data/discovery/egyptian.md`, `data/discovery/variants.md`, `data/discovery/demotic.md`, and the folders under `data/sources/dig/` | What this project already found or tried on these words. Quote it as a source like the others |

In the files with `=== page N ===` markers, the page of a quote is the number of the nearest marker above it.

## Letters

The batch file writes the project's letters: `S` is the sign s, `s` the sign se, `N` the sign ne, `X` the sign ẖ,
`x` the sign ḫ; a dot is a lost sign. The sources write otherwise, and you have to search for their spellings:
Rilly writes ḫ and ẖ (or x and h), ñ or ne, s and se; Griffith writes ê for o, z for d, š, ñ, ḫ, ẖ. His Meroitic
type is not in the text layers, so search his transliterations and his English. So `pSxrkete` may stand as
psi-ḫr-kete, psiḫrkete, pšeḫrkete or p-ši-ẖr-kete, and `Xol` as ẖol, hol or ḫêl.

## Your answer

Write to the file named at the end of this brief, one JSON line per item of your batch, in the batch's order,
nothing else in the file:

    {"item": "<the item's name as the batch file gives it>", "statements": [{"source": "<a name from the table>", "file": "<the file's path>", "page": 12, "quote": "<5 to 40 words copied exactly from the file, on one line>", "says": "<what it says about the item, in one sentence of your own>", "stance": "accepts"}], "state": "<one sentence: what the sources in hand know of it>", "newer_than_2003": "<a meaning or an analysis that a source later than 2003 gives and the entry of 2003 does not; else empty>", "piece": "<empty, or why this spelling is not a word of its own: a piece of a longer word cut by a divider or a line end, a part of a name, a slip of word division; with the ids of the texts that show it>", "kind": "<the kind of word the sources and the places support: verb, noun, title, epithet, name, ending, particle, not a word>", "tests": ["<a check that could be run on the corpus to confirm or to refute the leading reading>"]}

- "stance" is one of: "accepts" (states the meaning without reserve), "probable", "proposes" (a suggestion, a
  question mark), "doubts", "rejects", "mentions" (names the word without a meaning).
- A quote has to be found in the file, character for character but for line breaks and runs of spaces: a script
  checks every quote, and a statement whose quote it does not find is thrown away. So copy, do not retype from
  memory; keep the quote short enough to be exact.
- An item for which the sources say nothing gets "statements": [].
- For a spelling that looks like a piece of a longer word, open its texts in `data/corpus_v6.jsonl` (one JSON row
  per inscription, field `id`; the text is the field `text`) and look at the words on each side before you fill
  in "piece".

Do not change or create any other file, do not search the web, and do not run the project's scripts or tests
(grep and short scripts of your own for searching are fine). When the file is written, reply in under 80 words:
how many items you wrote, how many statements, and which items the sources say nothing about.
