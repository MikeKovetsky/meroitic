# The Nubian dictionaries: what the typists are given

Written on 2026-11-16, before any typist was started. The rules and the bars are in
[`data/discovery/outside_evidence.md`](../../data/discovery/outside_evidence.md), track A. Each typist gets the
brief below with its own book, its own pages and its own folder (`typed` for the first typing, `typed2` for the
pages read a second time).

## The brief

    # Type pages of a Nubian–German dictionary

    You type pages of a 19th-century Nubian–German dictionary from page images, one file a page. A program will
    compare the entries with the words of another language sound by sound, so every letter and every mark on a
    letter counts, and so does the meaning.

    **Your pack:** book `<R or L>`, PDF page indexes `<first>` to `<last>` (`<n>` pages), files into
    `/Users/mike/repos/mike/meroitic/data/sources/nubian/<typed or typed2>/`.

    ## The books and the images

    - `R` is Leo Reinisch, *Die Nuba-Sprache*, volume 3, *Wörterbuch* (Vienna 1879), the Nubian–German part.
      Images: `/Users/mike/repos/mike/meroitic/data/sources/reinisch1879/pages/`. Printed page = index − 332.
    - `L` is Richard Lepsius, *Nubische Grammatik* (Berlin 1880), its *Nubisch-Deutsches Wörterbuch*.
      Images: `/Users/mike/repos/mike/meroitic/data/sources/lepsius1880/pages/`. Printed page = index − 147.

    For the index 345 there are three images: `p0345.png` (the whole page), `p0345_top.png` (its upper 56%) and
    `p0345_bot.png` (its lower 56%; the two overlap in the middle of the page). Read the two halves for the
    letters and the whole page for the layout. Read every page of your pack yourself, image by image.

    ## How the books print an entry

    - **Reinisch.** The headword stands in italics at the left margin; the lines of its entry are indented. After
      it may come `plur. -x`, then the dialect in brackets: `(K)` Kenzi, `(D)` Dongola, `(F)` Fadidscha, `(M)`
      Mahas, or several, `(KD)`, `(FM)`. Then the German meanings, then examples in italics with their German
      translation. `Ar.` followed by Arabic script marks a loan from Arabic. `s.` and `s. a.` point to other
      entries. `nom.` gives a verbal noun, and derived words follow inside the entry. Reinisch writes German
      without capitals and in a reformed spelling (`kind`, `tun`, `nemen`): copy it as printed.
    - **Lepsius.** The headword stands in italics; a star `*` before it marks a loan (mostly from Arabic), and
      the source word follows in square brackets. After the headword comes the dialect: `M.` Mahas, `K.` Kenzi,
      `D.` Dongola, or several (`KD.`, `MKD.`). Then the German meanings. Numbers such as `12, 19. 20` or
      `H. 4, 31` are references to the Gospel text: leave them out. `Obj.` and `Pl.` give forms. `=` gives the
      word of the other dialect (`= KD. wissi`), `s.` points to another entry.

    ## The file for a page

    One file a page, named by book and index: `R0345.tsv`, `L0470.tsv`. Tab-separated, UTF-8, this header line
    first:

        book	index	page	n	headword	dialect	loan	plural	pos	gloss_de	gloss_en	see	parent	note

    One row for each entry, in the order of the page (`n` counts the rows of the page from 1):

    - `book`, `index`, `page`: `R` or `L`, the PDF index, the printed page number.
    - `headword`: exactly as printed, with every mark: the macron (`ā ē ī ō ū`), the acute (`á é í ó ú`), `š`,
      `ž`, `ñ`, `ṅ`, a `g` or `j` with a mark, a hyphen inside the word. Use the Unicode letter that has the
      mark where one exists, the letter with a combining mark where none does. Do not modernise, do not
      normalise, do not correct. Without the star and without a final full stop.
    - `dialect`: the dialect letters as printed, without brackets and stops (`K`, `KD`, `FM`, `MKD`); empty if
      the entry gives none.
    - `loan`: `Ar` where Reinisch writes `Ar.`; `*` where Lepsius prints the star; any other language the entry
      names as the source, as printed; empty otherwise. Do not type the Arabic script. Put Lepsius's bracketed
      source word into `note` in its Latin letters (`[ḥabb]`).
    - `plural`: the plural as printed (`-rī`, `ažkī`), empty if none.
    - `pos`: `n`, `v`, `adj`, `adv`, `num`, `pron`, `postp`, `conj`, `interj` or `part`, judged from the German
      meaning; empty if you cannot tell.
    - `gloss_de`: the German meanings as printed, all senses in their order, joined by `; `. No examples, no
      references. If the entry is long, the senses only.
    - `gloss_en`: a plain and exact English translation of `gloss_de`, in the same order. Add nothing.
    - `see`: the entries pointed to (`s.`, `s. a.`), joined by `, `; a dialect equivalent as `= KD wissi`.
    - `parent`: empty for an entry. For a **sub-row** it is the headword of the entry the row stands in.
    - `note`: `unsure: ...` where a letter or a mark stays unclear after the closer image (say which); `runs on`
      where the last entry of the page goes on to the next page; a clear misprint, typed as printed and named
      here; Lepsius's bracketed source word.

    **Sub-rows.** A derived word, a compound or a verbal noun that is printed inside an entry *with a meaning of
    its own* gets a row of its own, with `parent` set (Reinisch: `nom. awīd das tun` under `Au`; `au-tir jemand
    einen dienst erweisen` under `Au`). Forms without a meaning of their own (a perfect, an imperative, `Obj.`),
    examples and sentences are not typed.

    **A page that begins inside an entry.** Do not invent a headword for those lines. If they hold derived
    words with meanings, type them as sub-rows with `parent` = `(continued)`.

    **The last line of every file** is a count: `# entries=<rows without a parent> subrows=<rows with one>`. A
    page without an entry (blank, or a title) gets the header, the line `# blank` and `# entries=0 subrows=0`.

    ## Rules

    - Type what is printed. Do not use what you know of Nubian to complete or to correct a word.
    - Do not open any file under `data/sources/nubian/` but the ones you write, and no other typist's work.
    - No tab and no line break inside a cell.
    - Before you finish, check every file of your pack: the header, one row an entry, `n` running from 1, the
      count line agreeing with the rows, and `<n>` files in all.

    ## What you return

    For each page its index, its printed page number, the number of entries and of sub-rows, and how many rows
    carry `unsure`; and one or two sentences on anything in the print that this brief does not cover.
