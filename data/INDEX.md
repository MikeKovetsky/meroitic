# Index of the data

Everything the project holds, by folder: what it is, where it came from, how big it is, and whether it is in the
public repository. Counted on 2026-11-13 from the files on disk (the rows of `data/discovery/`, `data/sources/words/`, `data/sources/rare/`, `data/sources/g3/`, `data/sources/g5/`, `data/sources/g8/`, `data/sources/g8b/`, `data/sources/g9/` and `data/sources/g6/` on 2026-11-16).
"Local" means the folder is listed in `.gitignore` and stays on the author's machine, because the material has no
open licence or is in copyright ([`LICENSE-DATA.md`](../LICENSE-DATA.md) and the [README's section
"Data"](../README.md#data) say why for each).

## 1. Public, in this repository

| Path | What it holds | Size |
|---|---|---|
| `data/inscriptions.jsonl` | One row for each of the 585 inscriptions the project holds a reading of: REM or edition number, site, kind, every reading's source and licence, and the text of the readings that are open (304) | 0.6 MB |
| `data/inscriptions_map.tsv` | What each of the 899 texts of `corpus_v5` is: an inscription, a part of one, or an example phrase | 0.2 MB |
| `data/expansion/` | The open transcriptions: Griffith's *Meroitic Inscriptions* I and II and *Meroë* (152 inscriptions), Karanòg and Shablûl (151, with the 48 typed reference pages and the readers' files), the Akinidad stela REM 1003 from Griffith 1917 (`jea/`), Griffith's Faras texts 1 to 23 of 1922 typed from his hand copies (`faras/`, with the readers' files, the bar and the blind second typing), and the tests of the reading method | 3.7 MB, 503 files |
| `data/discovery/` | The pages of each study with their figures files and public tables: the coverage map, the Egyptian and variant searches, the check against two editions, `corpus_v6`, the readers, the Demotic step, the lexicon's statuses (`lexicon_statuses.tsv`, `lexicon_other_statuses.tsv`), the F4 pilot and rounds, the recurring open words, the count of distinct words, the open spellings in one or two texts (`rare_spellings.md` and its figures), the map with its layers (`map_layers.md`, `map_figures.json`), the open spellings the lexicon does not hold, the second scholar for the later meanings, the leftover parts and what Millet and Lipiński state (two pages and a figures file), the leftover stems (a page and a figures file), the blind test again (two runs, each with its page and its figures file), the grammar-first pilot (`grammar_pilot.md` and its figures file), the rules, bars and results of the three tracks of evidence from outside the texts (`outside_evidence.md`, with a figures file for each track) | 1.4 MB, 63 files |
| `data/gold_lexicon.json`, `data/gold_morphology.json` | The answer key of the first tests: 82 accepted meanings and 26 endings, each with its source | 0.1 MB |
| `data/leads/` | Four write-ups of leads and a README | 0.1 MB |
| `data/synth_corpus.txt` | The synthetic twin language of the leak-free test | 0.1 MB |
| `data/transliteration_map.md` | How the corpus's letters map to the scholars' transliteration | small |
| `data/nes/README.md`, `data/nes/meroitic_wiktionary.tsv` | The sources of the Northern East Sudanic word lists, and Wiktionary's 46 Meroitic lemmas | small |

## 2. Local: corpora and working files built by the project

| Path | What it holds | Size |
|---|---|---|
| `data/otten/` | A copy of Otten and Anastasopoulos's repository, Meroitic-Corpus: the padded corpus file, the per-scholar example files, their code and embeddings. No licence stated | 23.0 MB, 52 files |
| `data/corpus.jsonl`, `corpus_v2.jsonl`, `corpus_v2_c3_snapshot.jsonl`, `corpus_v3.jsonl`, `corpus_v5.jsonl`, `texts.jsonl` | The corpora of each stage, from Otten's file with the copies removed to the 899 texts of `corpus_v5` | 0.1 to 0.2 MB each |
| `data/corpus_v6.jsonl` | One row per inscription with real names: 570 inscriptions, 10,648 words (since the Faras texts, 2026-11-17; the map holds the 548 of before, 10,290 words). Built by `src/v6/build.py` | 0.2 MB |
| `data/name_pools.json`, `data/swap_partners.json` | The two pools of swapped names recovered from Otten's file, and which text was swapped with which | 0.3 MB |
| `data/rilly2003/` | Rilly's lexicon of 2003 as typed entries (headword, kind, status, page, meaning, other scholars' proposals), extracted from the scans of his thesis. In copyright | 0.6 MB, 7 files |
| `data/nes/*.tsv` | Word lists of ten Northern East Sudanic languages (5,668 rows by the folder's README), 330 proto-forms and 82 sound correspondences. Basic vocabulary for the most part; `data/nes/README.md` names the source of every row | 2.3 MB |
| `data/sources/v6/` | The files `corpus_v6` is built from and counted on: source lines, joins, the map of old ids, the readers' packs, and the word-by-word map of the clean corpus (`analysts/glosses.jsonl`), with the 548 texts it was made on (`analysts/corpus.jsonl`, a copy of `corpus_v6` as it stood before the Faras texts: the studies of the map read it) | 10.3 MB, 54 files |
| `data/sources/faras/` | The Faras work of 2026-11-17: every copy of Griffith's 46 cut out (an overview, enlarged pieces, a context crop; `cuts/`), and the readers' kits for Faras 24 to 46, cut and briefed but not run (`kits/`). Public domain, kept local for size; `runs/work/faras/cut2.py` makes the crops again from the PDF | 64.7 MB, 624 files |
| `data/sources/coverage/` | The first coverage map (on `corpus_v5`): the analysts' packs and answers, the glosses, the ranked unknown pieces | 18.3 MB, 83 files |
| `data/sources/dig/` | The six ways of finding meanings tried on 11 November: blessings, counted things, a crossword of parallels, Demotic, kin terms, proposals | 2.5 MB, 116 files |
| `data/sources/egyptian/` | The Egyptian search: the lexicon's 207 entries that mention Egyptian, Demotic, Coptic, Greek or Latin, two readers' answer keys, the Coptic lexicon (KELLIA, CC BY-SA 4.0) and the TLA's Demotic sentences (CC BY-SA 4.0; forms, no meanings) | 19.9 MB, 35 files |
| `data/sources/variants/` | The search for spellings of known words: the checkers' packs, answers and key | 1.9 MB, 39 files |
| `data/sources/expert/` | The check of the map against Millet 2005 and FHN III: the editions' rows, the checkers' answers, the decoys, the differences | 1.1 MB, 31 files |
| `data/sources/demotic/` | The same people in Demotic, Greek and Meroitic: the people of FHN III, the packs and the checked meanings | 0.5 MB, 17 files |
| `data/sources/lexicon/` | F2: the judges' packs, answers and keys of three rounds, and the entries with their statuses | 0.6 MB, 24 files |
| `data/sources/f4/` | The F4 pilot: the packs, the translators', splitter's and judges' answers, the key | 0.2 MB, 13 files |
| `data/sources/f4r/` | The F4 rounds: the handbook (as compiled and after its check), the checkers' verdicts, the splitters' units for all 18 renderings, and the packs, answers and keys of the rounds `r1`, `r1b` and `held` | 6.7 MB, 386 files |
| `data/sources/akinidad/` | REM 1003: the page images of Griffith 1917, the drafts, the word-by-word comparison with the other two readings | 5.0 MB, 39 files |
| `data/sources/mnl/` (other than the scans) | The 256 texts typed from the Newsletter (`mnl_texts.jsonl`), `corpus_v4`, the collation of editions, the oracular decrees, the grammar test, Meeks's word list, the numbers | part of the 229.6 MB below |
| `data/sources/recurring/` | The recurring open words (`src/recurring.py`): the 121 items with every place they stand, the dossiers and the readers' statements, the two readings of the stated meanings, the two checkers' verdict on each of the 1,108 places, the proposals on record, the blind test's packs, key and answers, the overlay on the map, and the first working scripts (`old_scripts/`, which hold the bar of class A as it was set) | 6.0 MB, 225 files |
| `data/sources/words/` | Distinct words (`src/words.py`): what every running word of the map is, the sample of 240 unnamed stems, the packs and the answers of the two readings (two checkers each), and the estimate | 1.4 MB, 84 files |
| `data/sources/rare/` | The open spellings in one or two texts (`src/rare.py`): for G4 the 323 entries with every place, the dossiers and the readers' statements, the two readings of the stated meanings, both readings of the places (two checkers each); for G2 the 116 entries and the checkers' verdicts; the lines each run lays in the map; the tokens of each agent; the first working script (`run.py`); and in `g4m/` the follow-up on what Millet 2005 and Lipiński 2011 state (`src/leftover.py`): the 15 entries, the two readings of the statements, the places (two checkers), the lines of the map's fifth layer | 9.8 MB, 287 files |
| `data/sources/g3/` | The open spellings the lexicon does not hold (`src/unnamed.py`): the packs, keys and answers of the two pilots and the full pass (two checkers each), the lines the step lays in the map, the tokens of each agent, the first working scripts (`run.py`, `layer.py`) | 3.0 MB, 142 files |
| `data/sources/g5/` | A second scholar for Rilly's later meanings (`src/second_later.py`): the entries with the other scholars' statements, the rows and decoys, the judges' packs and answers, the result, the tokens, the first working script (`run.py`) | 0.4 MB, 26 files |
| `data/sources/g8/` | The leftover parts, the first reading of the unnamed parts (`src/leftover.py`): the packs, the key and the answers of two checkers, the result, the tokens | 0.3 MB, 16 files |
| `data/sources/g8b/` | The leftover parts, the second reading of the unnamed parts (`src/leftover.py`): the packs with controls drawn anew, the key and the answers of two fresh checkers, the result, the lines of the map's sixth layer, the tokens | 0.3 MB, 17 files |
| `data/sources/g9/` | The leftover stems (`src/leftover.py`, the commands ending in `-stems`): the 8 packs with four kinds of control, the key and the answers of two fresh checkers a pack, the result, the lines of the map's seventh layer, the tokens | 0.4 MB, 21 files |
| `data/sources/g6/` | The blind test again (`src/blind2.py`): the 25 packs, the key, the answers of five readers a pack, the result, the tokens | 1.1 MB, 53 files |
| `data/sources/g6b/` | The blind test with all 83 accepted words (`src/blind2.py`, the commands ending in `-83`): the 40 packs, the key, the answers of five readers a pack, the result with its count by sort of word, the tokens of the 31 readers that reported them, the packs' wording of four meanings that the public files give in other words (`pack_wording.json`) | 1.7 MB, 84 files |
| `data/sources/grammar/` | The grammar-first pilot (`src/grammar.py`): the split of the texts, the tables of the tuning and the held-back texts as the finders and the tests saw them, the finders' briefs and rules of both rounds, the results of the frozen tests (which stand in `runs/grammar/`, public), the readers' packs and answers, the tokens | 1.4 MB, 55 files |
| `data/sources/nubian/` | Track A of the evidence from outside the texts (`src/nubian.py`): the 340 pages of the Nubian–German dictionaries of Reinisch 1879 and Lepsius 1880 typed one file a page (`typed/`), the 34 pages typed a second time (`typed2/`), the typists' notes, the known words with their meanings, the merged dictionary and its report, the typing's agreement, gate A1's result (`gate.json`), the tokens | 2.1 MB, 382 files |
| `data/sources/frames/` | Track B (`src/frames.py`): the six files of frames from the Egyptian texts of FHN I and II and their digest, the texts, folds, packs, key and briefs, the 80 aligners' answers in two arms, the judges' packs and answers, the result, the tokens | 3.3 MB, 209 files |
| `data/sources/names/` | Track C (`src/names.py`): the names with their roles, the parts learned from the tuning names, gate C1's result, the readers' packs, key and answers, the count of gate C2, the tokens | 0.6 MB, 32 files |
| `data/sources/notes/` | The progress log (`PROGRESS.md`) and the three parallel sessions' logs | 0.2 MB |

## 3. Local: the sources fetched, with where each came from

Public domain here means published before 1930; the files are kept local all the same, as scans. The nine rows from `cnd/` on were fetched on 2026-11-16 on Mike's word ("Yes, fetch all nine"), 23 files and 134.8 MB; every archive.org file has the size and the md5 that archive.org gives for it. Murray 1923 and Lukas 1933 were downloaded by Mike himself the same evening, because their hosts check for robots, and moved here from his Downloads folder (29,783,066 and 1,809,127 bytes).

| Path | Source | Fetched | Size | Rights | What it is for |
|---|---|---|---|---|---|
| `mnl/MeroNews1` to `MeroNews30` | *Meroitic Newsletter* 1 to 30 (1968 to 2003), scans at meroiticnewsletter.org | 9 Nov | 229.6 MB with the typed texts, 58 folders | in copyright | Printed transliterations with REM numbers; 256 texts typed; articles on the formulae |
| `karanog/`, `karanog-text/` | Griffith, *Karanòg: The Meroitic Inscriptions of Shablûl and Karanòg* (1911), archive.org `karangmeroitic00grifuoft` | 10 Nov | 42.7 MB | public domain | 151 hand copies read; his formula tables and indexes; his chapters on the formulae |
| `jssea/`, `jssea-text/` | Millet, "The Meroitic Inscriptions from Gebel Adda", JSSEA 32 (2005), the society's PDF | 12 Nov | 18.9 MB | in copyright | The renderings the translations are scored against |
| `fhn1/` | *Fontes Historiae Nubiorum* I, Bergen's server | 9 Nov (copied 13 Nov from the temporary folder) | 3.7 MB | all rights reserved | Not yet used |
| `fhn2/`, `fhn2-text/` | *Fontes Historiae Nubiorum* II, Bergen's server | 12 Nov | 40.0 MB | all rights reserved | The editors' comments on Meroitic texts |
| `fhn/`, `fhn-text/` | *Fontes Historiae Nubiorum* III, Zenodo record 821860 | 12 Nov | 54.4 MB | all rights reserved | Modern readings and comments; the check of the map; the Demotic step |
| `fhn4/`, `fhn4-text/` | *Fontes Historiae Nubiorum* IV (corrigenda and indexes), Zenodo record 821885 | 12 Nov | 15.3 MB | all rights reserved | Its Meroitic indexes gloss 62 titles and 51 words: a second stated source in F2 |
| `dotawo/`, `dotawo-text/` | Rilly, "Personal Markers and Verbal Number in Meroitic", Dotawo 7 (2021), eScholarship | 12 Nov | 3.8 MB | licence not checked | The newest study of the blessings' verbs; a source of the handbook |
| `griffith-jea/`, `griffith-jea-text/` | Griffith, "Meroitic Studies" I to IV, JEA 3 and 4 (1916 to 1917), Zenodo (CC0) | 12 Nov | 6.3 MB | public domain | The numerals; the whole text of REM 1003 |
| `lipinski2011/`, `lipinski2011-text/` | Lipiński, "Meroitic (Review article)", Rocznik Orientalistyczny 64/2 (2011), the Łódź repository | 12 Nov | 0.6 MB | in copyright | A second scholar's view of Rilly 2010; a source of the handbook |
| `survey-text/` | Text layers from the survey of 9 November: JEA 3, 4, 11 and 15; *Liverpool Annals* 7 to 15; ASE memoirs 18 to 21; *Meroë* (1911); *Areika*; *Buhen*; the *Recueil Champollion* | 9 Nov (copied 13 Nov) | 15.9 MB, 35 files | public domain | Finding passages; no page images |
| `laaa7/`, `laaa7-text/`, `laaa7-pages/` | *Liverpool Annals of Archaeology and Anthropology* 7 (1914 to 1915 by archive.org's record), the half archive.org holds (pp. 69 to 135) | 13 Nov | 5.0 MB and 6.5 MB of page images | public domain in the US | Sayce's reading of REM 1003, all 42 lines; not yet typed |
| `griffith-mi1/`, `griffith-mi1-text/` | Griffith, *Meroitic Inscriptions* I (1911), archive.org `archaeologicals19egyp` | 13 Nov | 12.0 MB | public domain | His translations and comments; a source of the handbook |
| `griffith-mi2/`, `griffith-mi2-text/` | Griffith, *Meroitic Inscriptions* II (1912), archive.org `archaeologicals20egyp` | 13 Nov | 16.8 MB | public domain | The same |
| `meroe1911/`, `meroe1911-text/` | Garstang, Sayce and Griffith, *Meroë, the City of the Ethiopians* (1911), archive.org `merocityofethiop00gars` | 13 Nov | 14.6 MB | public domain | The Meroë inscriptions and their comments |
| `champollion1922/`, `champollion1922-text/` | *Recueil d'études égyptologiques dédiées à Champollion* (1922), archive.org `bibliothquedel234ecol` | 13 Nov | 59.4 MB | public domain | Griffith's 46 Faras funerary texts (PDF pages 601 to 648); Faras 1 to 23 typed (`data/expansion/faras/`) |
| `jea11/` | *Journal of Egyptian Archaeology* 11 (1925), archive.org `in.ernet.dli.2015.70984` | 13 Nov | 25.5 MB | public domain | Griffith's Meroitic Studies V (the ostraca); page images, text in `survey-text/jea/` |
| `jea15/` | *Journal of Egyptian Archaeology* 15 (1929), archive.org `in.ernet.dli.2015.70988` | 13 Nov | 20.9 MB | public domain in the US | Meroitic Studies VI; page images, text in `survey-text/jea/` |
| `reinisch1879/` | Reinisch, *Die Nuba-Sprache* (1879), archive.org `sprachenvonnord03reingoog` | 13 Nov | 19.2 MB, 579 pages | public domain | A full Nubian dictionary, for the comparison by kind of word; page images, no text layer |
| `lepsius1880/` | Lepsius, *Nubische Grammatik* (1880), archive.org `nubischegrammat00lepsgoog` | 13 Nov | 19.5 MB, 658 pages | public domain | The same; page images, no text layer |
| `rilly2016/`, `rilly2016-text/` | Rilly, "Meroitic", UCLA Encyclopedia of Egyptology 1(1) (2016), eScholarship item 3128r3sw | 13 Nov, through the browser | 0.5 MB, 13 pages | all rights reserved | Which meanings Rilly accepts since the lexicon of 2003 |
| `cnd/` | van Gerven Oei (ed.), *Comparative Nubian Dictionary*, the data files of the GitHub repository `4nubianstudies/cnd-data` (8 files) | 16 Nov | 0.2 MB | CC BY 4.0 by its README; its LICENSE file is Apache 2.0 | 2,857 forms in 506 sets of related words, each form with its source: Old Nubian (482), Midob (388), Birgid (228), Proto-Nubian (218) and Proto-Kordofan Nubian (258) beside Nobiin, Andaandi and Mattokki. Not yet used |
| `reinisch1874/` | Reinisch, *Die Barea-Sprache* (1874), archive.org `diebareasprache00reingoog` | 16 Nov | 6.5 MB, 242 pages | public domain | The one dictionary of Nara found free; page images (the PDF has no usable text layer; archive.org's text is kept beside it). Not yet typed |
| `meinhof1918/` | *Zeitschrift für Kolonialsprachen* 9 and 10 (1918 to 1920), archive.org `afrikaundberse0910meinuoft` | 16 Nov | 52 MB, 616 pages | public domain | Meinhof's word lists of Hill Nubian (Dulman, Garko, Gulfan, Kadero, Koldegi), by the scout's search inside the item; not yet opened |
| `czermak1919/` | Czermak, *Kordufānnubische Studien* (Sitzungsberichte der Akademie der Wissenschaften in Wien 177, 1; 1919), archive.org `oahi-1771` | 16 Nov | 11 MB, 241 pages | 1919; the item states no licence | The word list of the Hill Nubian of Gebel Dair, by the scout's search inside the item; not yet opened |
| `macmichael1912/` | MacMichael's article of 1912 on the Zaghawa and Gebel Midob, Zenodo record 2198104 | 16 Nov | 3.2 MB, 58 pages | CC0 by Zenodo's record | A Midob vocabulary, by the scout's check; not yet opened |
| `macmichael1918/` | *Sudan Notes and Records* 1 (1918), archive.org `sudannotesrecord01philuoft` | 16 Nov | 6.9 MB, 68 pages | public domain | MacMichael on the Nubian of Darfur (Midob words); not yet opened |
| `macmichael1922/` | MacMichael, *A History of the Arabs in the Sudan*, vol. 1 (1922), archive.org `historyofarabsin01macm` | 16 Nov | 22 MB, 386 pages | public domain | Its table of Midob, Birgid and Nile Nubian words side by side, by the scout's check; not yet opened |
| `griffith1913/` | Griffith, *The Nubian Texts of the Christian Period* (1913), archive.org `nubiantextsofchr00grif` | 16 Nov | 7.8 MB, 148 pages | public domain | Its index of Old Nubian words with meanings; not yet opened |
| `almkvist1911/` | Almkvist, *Nubische Studien im Sudan* (1911), archive.org `nubischestudieni0000almk` | 16 Nov | 21 MB, 324 pages | public domain | A third dictionary of Nile Nubian (Mahas, Dongola, Kenzi); not yet opened |
| `murray1923/` | Murray, *An English-Nubian Comparative Dictionary* (Harvard African Studies 4, 1923), Heidelberg University Library, doi 10.11588/diglit.49263 | 16 Nov, by Mike (the site checks for robots) | 29.8 MB, 250 pages | public domain (the library's Public Domain Mark) | A Nubian–English dictionary of about 190 pages (PDF pages 50 to 240) with the dialects marked and Dair, Midob and Old Nubian compared; a text layer with reading errors. Not yet typed |
| `lukas1933/` | Lukas, "Beiträge zur Kenntnis der Sprachen von Wádai (Mararét, Mába)", *Journal de la Société des Africanistes* 3 (1933), pp. 25 to 55, Persée | 16 Nov, by Mike (the download asks a captcha) | 1.8 MB, 32 pages | in copyright; free to read on Persée | A sketch of Mararit, a Taman language, with a word list of about three pages at its end (from PDF page 30). Not yet typed |

## 4. Not held

| What | Why it matters | State |
|---|---|---|
| Hallof, *Analytisches Wörterbuch des Meroitischen*, with its volume 7 (2024), the texts of REM 0001 to 2780 | Five times our texts, and the newest dictionary | Print only; a purchase, parked |
| Rilly, *Le méroïtique et sa famille linguistique* (2010) | The cognate series that link Meroitic to Nubian | Print only; a purchase, parked |
| Rilly, *La langue du royaume de Méroé* (2007); Rilly and de Voogt (2012) | Later statements of grammar and lexicon | Print only; purchases, parked |
| Hofmann, *Material für eine meroitische Grammatik* (1981); Hintze (1979) | Earlier proposals, among them on the blessings | Print only |
| The first half of *Liverpool Annals* 7 (pp. 1 to 68, plates I to XIV) | The plates of the Akinidad stela | Not found online |
| The REM volumes on Persée (2000) | Photographs and drawings of REM 0001 to 1278 | Online, in copyright; not fetched |
| A Demotic word list with meanings | The Demotic side of a search for loans | Not looked for yet |
| A dictionary of a Taman or a Nyima language | Two of the family's branches | None found free (the scout's search of 16 November) |
