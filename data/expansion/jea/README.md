# REM 1003 from Griffith 1917, Griffith's ostraca of 1925, and Sayce on REM 1003

Three open texts in this folder: REM 1003 as Griffith printed it in 1917 (below), the 46 ostraca of his "Meroitic
Studies V" (1925), and Sayce's reading of REM 1003 (1914-15). The last two came in on 2026-11-17
([`data/discovery/ostraca_sayce.md`](../../discovery/ostraca_sayce.md) has the method, the bar and the results).

| File | What |
|---|---|
| `griffith1925_ostraca.txt` | the 46 ostraca of *JEA* 11 (1925), pp. 220-224, as printed, typed by hand from page images; the head says how his marks are typed |
| `griffith_jea11.jsonl` | their rows, one per text, in the shape of the other `griffith_*.jsonl` rows, written by `src/ostraca.py` |
| `ostraca_figures.json` | their counts, the blind second typing of the lot, and what their spellings are on the map |
| `sayce1914_rem1003.txt` | Sayce's 42 lines of REM 1003 (*Liverpool Annals* 7, pp. 69-72), typed by hand from page images |
| `sayce_rem1003.json` | his words in Griffith's letters and the corpus spelling, written by `src/sayce.py` |
| `sayce_comparison.json` | the comparison with Griffith 1917 and, as counts only, with the two closed readings; his values against Griffith's signs; Griffith's 38 doubted words |

## REM 1003 from Griffith 1917

The Great Stela of Queen Amanirenas and Prince Akinidad (REM 1003, British Museum EA 1650, from Hamadab near
Meroe) is the longest Meroitic text. Its reading in the corpus, Millet's as Otten typed it, has no licence. F. Ll.
Griffith printed the whole text in "Meroitic Studies IV: The Great Stela of Prince Akinizaz", *Journal of
Egyptian Archaeology* 4 (1917), pp. 159-173, in his transliteration of 1917. The article is in the public domain
(the JSTOR copy is on [Zenodo, record 2497984](https://zenodo.org/records/2497984), CC0).

| File | What |
|---|---|
| `griffith1917_rem1003.txt` | his 21 sections (§§ 1-21, ll. 1-42) as printed, typed by hand from page images on 2026-11-12 and checked again on pages rendered at high resolution; the head says how his marks are typed |
| `griffith_jea4.jsonl` | the row, in the shape of the other `griffith_*.jsonl` rows: his text (`text_std`), the corpus spelling (`text_corpus`), the words by line of the stela (`lines`), the places that are unsure (`doubts`) |
| `rem1003_comparison.json` | the counts of the comparison with the two closed readings, by line (no closed text) |

`python3 -I src/akinidad.py` writes the row from the text, and the comparison where the closed readings are
present (local only). `src/v6/readings.py` reads the row as an open reading of REM 1003, and the ostraca's rows as
open readings of 46 inscriptions numbered by the article's sigla (F.O. 1). `src/expand.py` does not read this
folder, so `corpus_v3` and `corpus_v5` are as they were. `python3 -I src/ostraca.py` writes the ostraca's rows and
figures, `python3 -I src/sayce.py` Sayce's words and the comparison.

**His signs and today's.** ê `o` (tê is the sign `to`), š `S`, plain s `s` (the sign se), ñ `N`, z `d`, ḫ (his h
with a breve below) `x`, ẖ (his h with a line below) `X`; every other letter as written, names lowered. The map is
his sign list of 1911 ([`../README.md`](../README.md), section 2). Every h of the sections carries one of the two
marks, so a plain h is no letter of the row, and the tests fail on one.

**What he prints.** 337 words on all 42 lines, 1,645 signs; he marks 38 words with a question mark, above a sign or
after the word. The row lists 17 more places that are unsure: 14 where his footnotes or his notes on the sections
doubt a sign or read it otherwise (`Armil`, "m fairly certain"; `ytes`, which "might be read yter"), and 3 of ours
(the numeral printed `1·2`, read as 1 and 2; `Mnê teslke`, two words or one across a printed line; the hatched last
digit of `1032`). His word division is kept: he joins some endings that later editions write apart
(`yemêqe(l. 24)eqebeswit`), and Otten's file divides more (485 words for the same text).

**The comparison.** Both texts spelled alike and lined up letter by letter; a word of his agrees when all its
letters lie in a stretch the two share. Against Millet's reading (the preferred one): 278 of 337 words (82.5%),
94.7% of the letters. Against the Newsletter's printout of 1971: 276 (81.9%), and 275 (81.6%) with no spelling
folded, which shows that the map of signs holds. The letters agree with the article's text layer, apart from places
where the layer misreads or drops a letter with a mark, reads a lone l as 1, or adds a stray letter from a brace;
and every mark was checked on the page images rendered at high resolution: the words that differ are his readings of
1917, not slips of the typing. The lines that differ most are ll. 25 (3 of 8 words agree), 32 (2 of 5), 22 (5 of 9),
18 and 24 (4 of 7 each).

**What adding it changed elsewhere in `corpus_v6`** (two builds compared on 2026-11-12, the same code with and
without the row). A run of five letters that eight edition texts hold is formula in the matching rule
(`src/v6/readings.py`), and REM 1003 now has two typed editions, so a few runs became formula. Of the 1,159 source
lines, 33 changed: 27 only in their shares, 5 quoted from REM 1003 now name this row as their closest reading, and
one, MilletExamples.txt line 933 (p. 242 of Millet's thesis), lost its sure match to GA 29: this row shares 7 of the
line's own runs, half as many as GA 29 and one more than the Newsletter's printout, and an inscription that close is
a rival (`CLOSE` in `src/v6/build.py`). It stays an example phrase, without an inscription. In the public map, 62 of
the 899 rows changed, all but that one in their shares or in the reading they were compared with. REM 1003 now has a
site (Hamadab) and the kind "royal or temple" instead of "funerary", from this row's description of the object. The
coverage recount did not change.
