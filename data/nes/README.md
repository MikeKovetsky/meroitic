# Northern East Sudanic word lists for the Meroitic cognate search

Word lists for the languages Rilly (2010) groups with Meroitic in Northern East Sudanic (NES): Nubian, Nara, Taman and Nyima.
Every row comes from a source that was downloaded or read on 2026-11-08, and every row names that source in its `source` column.
No form was filled in from memory.

## What is here

| File | Rows | What it holds |
|---|---:|---|
| `old_nubian.tsv` | 459 | 86 GLD Swadesh rows (Browne 1996, page cited on each row), 318 Wiktionary lemmas (173 of them proper names), 55 ASJP items. |
| `nobiin.tsv` | 249 | 111 GLD, 75 Wiktionary, 27 numerals (two lists), 36 ASJP. |
| `kenzi.tsv` | 167 | 110 GLD (Kenuzi), 57 ASJP (two lists). |
| `dongolawi.tsv` | 276 | 114 GLD, 12 numerals, 2 Wiktionary, 148 ASJP (two lists). |
| `midob.tsv` | 162 | 105 GLD, 13 numerals, 6 Wiktionary, 38 ASJP. |
| `birgid.tsv` | 129 | 95 GLD, 3 Wiktionary, 31 ASJP (Birgid is extinct). |
| `hill_nubian.tsv` | 2,443 | 1,762 IDS (Uncunwee/Ghulfan, 1,310-concept dictionary), 440 GLD (Dilling, Kadaru, Debri, Karko, Wali), 35 numerals, 8 Wiktionary, 198 ASJP (also Dair, El Hugeirat). |
| `nara.tsv` | 320 | 204 GLD (Modern Nara from Bender, Old Nara from Reinisch 1874), 13 numerals, 1 Wiktionary, 102 ASJP. |
| `taman.tsv` | 978 | 659 GLD (Tama, Erenga, Sungor, Miisiirii, and Mararit as its Ibiri and Abuu Shaarib dialects), 64 numerals, 3 Wiktionary, 252 ASJP. |
| `nyima.tsv` | 485 | 226 GLD (Ama/Nyimang and Afitti), 24 numerals, 3 Wiktionary, 232 ASJP. |
| `proto_nes.tsv` | 330 | 290 published reconstructions from Rilly's open papers, 34 ASJP Proto-Nubian and Proto-Nile-Nubian forms (Bechhaus-Gerst 1984), 6 Wiktionary Proto-Nubian lemmas. |
| `sound_correspondences.md` | 82 entries | Meroitic ~ NES correspondences: 53 rows of Rilly's 2003 table, 29 rules stated in prose (2003–2022), the 17 lexical series behind them. |
| `sound_correspondences.tsv` | 82 | The same rows, tab-separated, with source, page and URL. |
| `meroitic_wiktionary.tsv` | 46 | Extra: Wiktionary's Meroitic lemmas with glosses, etymologies and references, for the other side of the comparison. |

Languages are one file each, except two clusters kept in one file with a `variety` column: `hill_nubian.tsv`
and `taman.tsv`. The brief names them as units ("Hill Nubian", "Taman (Tama, Merarit, Sungor)"). Merarit is the
same language as Mararit (ISO mgb): the GLD gives it as its Ibiri and Abuu Shaarib dialects.

### Columns of the language files

| Column | Meaning |
|---|---|
| `form` | The form as the source prints it. GLD: the citation form; its attested spellings in braces go to `note`. ASJP: ASJPcode, a simplified, lossy alphabet. Wiktionary: Wiktionary's own Latin transliteration, with the native script in `form_native`. Variants joined by ` ~ ` are kept in one row as printed. |
| `gloss` | Short English meaning: the Swadesh item (GLD), concept (ASJP, IDS), numeral, or Wiktionary definition. |
| `pos` | Part of speech when the source gives it (Wiktionary; `num` for numerals). Blank otherwise. |
| `source` | Original citation with page where given, then the dataset and its URL. |
| `variety` | Language, dialect or list name as the source gives it. |
| `concept` | Comparison key: `GLD <item> <meaning>`, `Concepticon <id> <gloss>`, `IDS <id>`, or `numeral <n>`. |
| `dataset` | `gld`, `asjp`, `numerals`, `ids` or `wiktionary`. |
| `cogid` | GLD cognate class: `gld-<group>-<item>-<class>`. Rows with the same id were judged cognate by Starostin within that group file. |
| `form_native` | Old Nubian or Meroitic script headword (Wiktionary rows). |
| `note` | Source annotation: GLD notes (page references, other quotations, plural forms), ASJP and numeral comments, Wiktionary etymology. |

`proto_nes.tsv` has `form`, `gloss`, `pos`, `source`, then `proto_language` (as the source names it; Rilly's
"Proto-SON" is Proto-NES), `meroitic_comparandum`, `reflexes_cited`, `gloss_language` (Rilly's thesis glosses are
French and kept as printed), `dataset` and `note` (the verbatim line the row was copied from).

## Sources, licences and terms

1. **Global Lexicostatistical Database (GLD)**, G. Starostin, "Annotated Swadesh wordlists" for the Nubian (2015),
   Nara (2014), Tama (2014) and Nyimang (2015) groups: [nub.xls](https://starling.rinet.ru/new100/nub.xls),
   [nar.xls](https://starling.rinet.ru/new100/nar.xls), [tam.xls](https://starling.rinet.ru/new100/tam.xls),
   [nyi.xls](https://starling.rinet.ru/new100/nyi.xls), with PDF versions next to each. The best source here: 110 meanings,
   original transcriptions, a page reference on nearly every form (Browne 1996, Werner 1987 and 1993, Armbruster 1965, Hofmann 1986,
   Kauczor 1920, Thelwall 1977/1978/1983, Krell 2012, Bender 1968/1971, Reinisch 1874, Edgar 1991, Stevenson 2000) and
   cognate classes. **Terms:** no licence statement was found on the pages read. The files are openly downloadable; cite
   the GLD and the original sources, and ask the authors before republishing the data.
2. **ASJP** v21 (Wichmann, Holman, Brown, Dryer and Ran, eds., 2025), CLDF at [lexibank/asjp](https://github.com/lexibank/asjp).
   **CC BY 4.0.** 40-item lists in ASJPcode; good for coverage, too coarse for sound laws.
3. **Numeral Systems of the World's Languages** (Chan 2019), CLDF at [lexibank/numerals](https://github.com/lexibank/numerals).
   **CC BY 4.0.** Numerals 1–10, 20 and 100. The Dongolawi list was contributed by Claude Rilly from Armbruster 1960.
4. **Intercontinental Dictionary Series** (Key and Comrie, eds., 2023), Uncunwee (Ghulfan) by Robert Williams,
   [ids.clld.org/contributions/318](https://ids.clld.org/contributions/318), CLDF at [lexibank/ids](https://github.com/lexibank/ids).
   **CC BY 4.0.** The only full culture vocabulary (house, cattle, milk, kin terms) for any modern NES language here.
5. **Wiktionary** (English), category "<language> lemmas" for each NES language, Proto-Nubian and Meroitic, read through the
   MediaWiki API. **CC BY-SA 4.0** (and GFDL): rows from it carry share-alike. Old Nubian entries cite Browne 2002, the
   Database of Medieval Nubian Texts and others; the references are kept in `source`.
6. **Literature** (proto forms and correspondences), read openly online:
   - Rilly 2003, thesis Vol. I, [HAL tel-04794259](https://hal.science/tel-04794259/document). The precursor of Rilly 2010.
     Image-only scan; forms were transcribed by eye from page images. HAL labels it "HAL Authorization"; no licence text seen.
   - Rilly 2004, "The linguistic position of Meroitic", Arkamani, [Wayback copy](http://web.archive.org/web/20050405190957/http://www.arkamani.org:80/arkamani-library/meroitic/rilly.htm). Its IPA glyphs are lost in the HTML; those rows say so.
   - Rilly 2011, Ityopis 1, [PDF](http://www.ityopis.org/Issues-1_files/ITYOPIS-I-Rilly.pdf).
   - Rilly 2016, "Meroitic", UCLA Encyclopedia of Egyptology, [eScholarship](https://escholarship.org/uc/item/3128r3sw).
   - Rilly 2020, "Personal Markers and Verbal Number in Meroitic", Dotawo 7, [open HTML](https://pages.sandpoints.org/dotawo/article/rilly/).
   - Rilly 2022, [HAL hal-03925556](https://hal.science/hal-03925556/document); Rilly 2006 in *Kerma et Méroé*; Starostin 2020, [Dotawo 7](https://pages.sandpoints.org/dotawo/article/starostin/).
   These are copyrighted publications; the rows are short factual extracts with page references. Licence lines were not
   stated or not checked (Dotawo is open access).

## Encoding notes

The GLD spreadsheets use 37 private-use code points from the Starling Serif font. The 26 that occur in forms were
identified by rendering the matching words from the GLD PDFs, and are written as standard Unicode:

| Code point | Written as | Code point | Written as | Code point | Written as |
|---|---|---|---|---|---|
| U+E909 | ə̀ | U+E92D | ɪ́ | U+E259 | ə̄ |
| U+E90B | ɛ̀ | U+E935 | ɔ́ | U+E25B | ɛ̄ |
| U+E90D | ɪ̀ | U+E937 | ʊ́ | U+E269 | ɪ̄ |
| U+E915 | ɔ̀ | U+E93F | ʌ́ | U+E28B | ʊ̄ |
| U+E917 | ʊ̀ | U+E94B | ɛ̂ | U+E585 | ɛ̌ |
| U+E91F | ʌ̀ | U+E955 | ɔ̂ | U+E1F9 | n̄ (Old Nubian superline) |
| U+E929 | ə́ | U+E254 | ɔ̄ | U+EE6F | t̄ (Old Nubian superline) |
| U+E92B | ɛ́ | U+E81D | ṯ (underlined t, Nara) | U+E811 | ḏ (underlined d, Nara) |
| U+EE2D | i̯ | U+E183 | β | | |

The font draws the vowels written here as ɪ and ʊ with the older letters ɩ and ʋ. Three glyphs in forms could not be
located in the PDFs and are left as private-use characters: U+EDC1 (Birgid, one form and one note) and U+E099 (Modern Nara, one form).
Nine more occur only in notes (14 occurrences) and are also left as they are. GLD marks such as `#` after a form are kept as printed.

## What I could not get

1. **Browne 1996, *Old Nubian Dictionary*** (CSCO, Peeters) is not openly available. Old Nubian coverage comes from the GLD
   (86 Swadesh rows, each with its Browne page) and Wiktionary (318 lemmas, 173 of them proper names). Van Gerven Oei's
   *A Reference Grammar of Old Nubian* (2021) is not open either. The Database of Medieval Nubian Texts, which Wiktionary
   cites, was not explored.
2. **Rilly 2010** and Rilly & de Voogt 2012 are not open, so their proto-NES forms are missing. `proto_nes.tsv` uses the 2003
   thesis lists (pp. 263, 299, 301–306) and later open papers. The thesis Annexe (pp. 319–423, about 200 series with reflexes in
   every NES language, Proto-Nubian, Bechhaus-Gerst's, Ehret's and Bender's forms) is the richest open lead left: only series 11
   and 12 were transcribed.
3. **Ehret 2001, Bender 1996, Bechhaus-Gerst 1984/2011, Edgar 1991**: not open. Their forms appear only where Rilly cites
   them, and as ASJP's 34 Proto-Nubian forms (Bechhaus-Gerst 1984, ASJPcode).
4. **Starling etymological databases**: the Tower of Babel database list has no Nubian, Eastern Sudanic or Nilo-Saharan
   etymology database (Africa is Khoisan only). Starling's Nubian data is the GLD lists above.
5. **A 200-item core**: the GLD gives 110 items, ASJP 40, plus numerals. Beyond those, culture and kin words (bread, food,
   king, god, child, brother, sister, mother, father, house, cattle, milk) are missing for every modern language except
   Hill Nubian (Ghulfan, through IDS); Nobiin and Old Nubian have a few through Wiktionary.
6. **Numerals** are missing for Kenzi and Birgid (Old Nubian has some through Wiktionary).
7. **Leads not used:** [escalay/nubian](https://github.com/escalay/nubian) has about 9,470 OCR- and LLM-extracted entries from
   Armbruster 1965, Murray 1923 and Sambaj, but no licence and machine-generated fields, so it was left out. Murray's 1923
   *English-Nubian Comparative Dictionary* (Kenzi, Mahas, Dongolawi, Dair, Midob), Lepsius 1880 and Reinisch 1879 (Nile Nubian)
   and Reinisch 1874 (Nara) are public-domain scans that would need OCR. PanLex was not tried.
