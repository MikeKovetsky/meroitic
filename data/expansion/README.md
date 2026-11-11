# More Meroitic text: what is online, and a Karanog pilot

Work of 2026-11-09, about 75 minutes. Downloads are in `/private/tmp/claude-501/expansion/` (not in the repo).

**Update, 2026-11-10:** Karanòg has since been read in full ([`karanog/README.md`](karanog/README.md)), and the
texts printed in the *Meroitic Newsletter* have been typed ([`newsletter_reading.md`](newsletter_reading.md)). The
survey below stands as written on 2026-11-09.

## Answer first

1. **Cut, said first:** the pilot did not transcribe 20 inscriptions sign by sign. Griffith printed no Latin text for
   any inscription: Karanog (and Meroitic Inscriptions I and II, and Meroe) give the Meroitic only as hand copies or
   cursive type, so the OCR is garbage and every text has to be read from the image. In the time I could read the
   alphabet and the formula words, not 20 texts. The pilot is therefore 20 Karanog inscriptions **checked**: 4 with
   full text (the four Karanog texts that FHN III prints in modern transliteration) and 16 checked on the words
   Griffith's catalogue gives for them.
2. **Karanog is not in our corpus.** All 4 full texts are new: none of their distinctive words occurs in any funerary
   text of `corpus_v2.jsonl` (`akiNtel`, `deklo`, `amoke`, `wwikel`, `sekesek`, `qorbt` and others, 0 texts each).
   Of the 16 others, 6 are new on their key words (5 name Amanap, `amnp`, which occurs in no funerary text of ours; one
   has `areqeb`), and 10 cannot be decided because, with names masked, they hold nothing but the standard formulae.
   **Pilot: 10 new, 0 already present, 10 undecidable.**
3. **Estimated gain from the public-domain sources: about 460 new texts and 6,000 to 11,000 words**, a third to
   three fifths more than the corpus's 18,000 words. Only about 36 of those texts (FHN, about 600 to 2,000 words) exist as clean Latin
   transliteration; the rest must be read from page images of Meroitic cursive.

## 1. Sources online

Checked on 2026-11-09. "PD" means published before 1930 with authors dead before 1956: public domain in the US and
the UK. archive.org marks the Griffith items `NOT_IN_COPYRIGHT`.

| Source | Where | Licence | Meroitic texts, and in what form | Likely new to us |
|---|---|---|---|---|
| Griffith, *Karanòg: The Meroitic Inscriptions of Shablûl and Karanòg* (1911) | archive.org [`karangmeroitic00grifuoft`](https://archive.org/details/karangmeroitic00grifuoft) (Toronto, 400 ppi, used here), [`karanogmeroitici00grif`](https://archive.org/details/karanogmeroitici00grif), [`karangmeroitici00grifgoog`](https://archive.org/details/karangmeroitici00grifgoog), [`karangmeroitici01grifgoog`](https://archive.org/details/karangmeroitici01grifgoog) | PD | Karanog 1–132 and Shablul 1–19/20 (Griffith counts 150 texts), as **hand copies** pp. 129–181 (archive.org leaves n144–n196) and photographs Pl. I–XXIX. English catalogue pp. 54–78 gives names, titles and formula letters, not the text. | Yes (see pilot) |
| Griffith, *Meroitic Inscriptions I: Sôba to Dangêl* (1911, ASE memoir 19) | archive.org [`archaeologicals19egyp`](https://archive.org/details/archaeologicals19egyp); HathiTrust `mdp.39015084761363` | PD | Nos. 1–74 and 35 plates, in Meroitic cursive **type**; no Latin text | Mostly yes (Soba, Naga, Musawwarat, Meroe) |
| Griffith, *Meroitic Inscriptions II: Napata to Philae and Miscellaneous* (1912, memoir 20) | archive.org [`archaeologicals20egyp`](https://archive.org/details/archaeologicals20egyp); HathiTrust `mdp.39015082599666`, `uva.x004604430`, `njp.32101020972608` | PD | Nos. 75–137 (97–111 are several Philae texts) and 48 plates, cursive type | Mostly; No. 94 (Kalabsha) is in |
| Garstang, Sayce, Griffith, *Meroë, the City of the Ethiopians* (1911) | archive.org [`merocityofethiop00gars`](https://archive.org/details/merocityofethiop00gars); HathiTrust `mdp.39015033276299` | PD | Meroe Inscr. 1–51 (temples, about 25 altars), type and plates | Yes |
| Griffith, "Meroitic Studies" I–VI, *JEA* 3, 4, 11, 15 (1916–1929) | archive.org `in.ernet.dli.2015.70975` (vol. 3), `.70976` (4), `.70984` (11), `.70988` (15); HathiTrust `njp.32101067696011`, `njp.32101067696029`, `inu.30000112983550`, `inu.30000112983592` | PD to 1925; vol. 15 (1929) PD in the US only if not renewed, check | Latin transliteration: Wayekiye stela REM 0089 (I), Akinidad stela REM 1003 (IV, already in), about 45 ostraca from Faras, Buhen, Dakka (V) | REM 0089, the ostraca |
| Griffith, "Meroitic funerary inscriptions from Faras", *Recueil Champollion* (1922), pp. 565–600 | archive.org [`bibliothquedel234ecol`](https://archive.org/details/bibliothquedel234ecol) | PD | 46 Faras funerary texts, facsimile + English | Probably (Karanog was not in; Faras untested) |
| *Areika* (1909), *Buhen* (1911), LAAA "Oxford Excavations in Nubia" (1921–28) | `areika00rand`, `buhentext00rand`, `annals-of-archaeology-and-anthropology_1921_8` etc. | PD | 0 texts: script discussion and site catalogues only | — |
| *Fontes Historiae Nubiorum* II and III (Bergen 1996, 1998) | [FHN II PDF](https://data.ub.uib.no/files/manlib/ubb/ubb-msref/ubb-msref-0939/ubb-msref-0939-078/ubb-msref-0939-078-fon/ubb-msref-0939-078-fon-02/pdf/ubb-msref-0939-078-fon-02_orig.pdf), [FHN III PDF](https://data.ub.uib.no/files/manlib/ubb/ubb-msref/ubb-msref-0939/ubb-msref-0939-078/ubb-msref-0939-078-fon/ubb-msref-0939-078-fon-03/pdf/ubb-msref-0939-078-fon-03_orig.pdf) (University of Bergen Library) | Free to read; imprint "All rights reserved", no open licence: fine for research use, ask before republishing | Modern (REM) transliteration of about 36 REM texts in 20 entries, e.g. REM 0405, 0092, 0412, 1041, 1001/1038, 0407, 0097–0111 (Philae), and Karanog 0247, 0277, 0278, 0321 | About 30 texts |
| Lepsius, *Denkmäler* Abt. VI | [Lepsius-Projekt, Halle](https://edoc3.bibliothek.uni-halle.de/lepsius/tafelwa6.html) | PD | 53 texts, images only | Mostly the same texts as Griffith's |
| *Meroitic Newsletter* 1–30 | meroiticnewsletter.org (third-party scans) | Unclear | REM preliminaries and supplements (e.g. REM 1001–1110 in no. 6) | Probably many; not opened in this survey (outside the allowed hosts). Read since: 256 texts, 185 new ([`newsletter_reading.md`](newsletter_reading.md)) |
| Trismegistos, Hallof 2024 (*Analytisches Wörterbuch* 7, REM 0001–2780), REM 2000 | — | Print or metadata only | — | Not machine-recoverable |
| Other digital corpora | GitHub: only Otten's; Wiktionary: 48 lemmas | — | — | — |

Numbering: REM 0001–0137 follow Griffith's *Meroitic Inscriptions* numbers, and **Karanog N = REM 0200+N**
(FHN III: Kar. 47 = REM 0247, Kar. 77 = REM 0277).

Not checked to the end (survey by a subagent): the HathiTrust ids come from its volumes API (its catalog search
returned 403); Trismegistos returned 403; the Sudan & Nubia and HAL Sedeinga reports (a few texts each) and Rilly
2022 on Musawwarat graffiti (CC BY 4.0, HAL `hal-03956626`) were found but not opened.

## 2. Griffith's transliteration and the corpus spelling

Griffith 1911 (Karanog, "The phonetic values of the signs", pp. 11–16, leaves n26–n31) numbers 23 signs. His values,
and the corpus spelling (the `corpus_v2.jsonl` convention: Millet's, with `o` for his E):

| Griffith 1911 | Modern (Hintze/Rilly) | Corpus | Cursive form in the Karanog copies |
|---|---|---|---|
| a, e, i, y, w, b, p, m, n, r, l, k, q, t, te | same | same | a `ϛ2`, e `ϛ`, i `4`, y `///` or `//`, w `ʒ`, b `ν`, p `ξ`, m `)`, n `ꝶ`, r `ω`, l `ϟ`, k `ξ` with long tail, q `13`, t `7`, te `/ϟ-` |
| ê (sign 3) | o | o | `/` |
| ñ (sign 11) | ne | N | `ʌ` |
| ḫ (sign 14; "kh" in his names) | ḫ | x | `<` |
| ẖ (sign 15; "h" in his words: *ate mhe*) | ẖ | X | `3` |
| s (sign 16, "s followed by a vowel") | se | s | `J//` |
| š (sign 17; "sh" in his names) | s | S | `3` with tail |
| tê (sign 22) | to | to | `ب` |
| z (sign 23, "provisionally") | d | d | `ʎ` |

Apply in this order: `tê`→`to`, `ê`→`o`, `š`/`sh`→`S`, `ñ`→`N`, `z`→`d`, `ḫ`/`kh`→`x`, `ẖ`/`h`→`X`; plain `s` stays
`s` (it is the se sign). His English renderings add an `a` where no vowel is written ("In transcribing Meroitic names
I have frequently supplied the vowel a", p. 16) and hyphens: drop both (`Mali-tarqize` → `mltrqd...`, not usable
for names; names are masked anyway).

Checked on the words known in both systems (Griffith's form from the Karanog text and his JEA articles):

| Word | Griffith | Mapped | Corpus | |
|---|---|---|---|---|
| Isis | Wêš (names Wesh-; "Transcribed Wes", p. 11) | woS | woS, woSi | ok |
| Osiris | Šorêi | Sorey | Sorey, Soreyi | ok |
| ato | atê (*ate mhe ps-te*, p. 46; read in the copy as `a`+`to`) | ato | ato | ok |
| at | at (*at mhe ps-hr-te*) | at | at | ok |
| qore | qêre (*qêren*, catalogue) | qore | qore | ok |
| terike | terike | terike | terike | ok |
| tedhe | tezḫe | tedxe | tedxe, tdxe | ok |
| yetmde | yetmze (*yet-mze-le*, JEA) | yetmde | yetmde | ok |

The mapping is from Griffith's sign list; the forms marked as his were seen in his text, but not every diacritic was
checked on a page image (the OCR drops them).

The Karanog copies are easy to read except for one trap: in this hand **m, ẖ and s (Griffith's š) are all 3-shaped**;
context (the formulae, the parentage words) decides. The invocation `ʒ/34 : 3/ωϛ//4` reads `woSi Soreyi`, and formula
A begins `ϛ2ب )3ϛ` = `ato mXe`, which fixed the key.

## 3. Pilot: 20 Karanog inscriptions

Method: for each inscription, the words that can't be names (titles, places, gods), in corpus spelling, searched in
the 659 funerary texts of `corpus_v2.jsonl` (with `e` allowed for `o`); a text counts as present if half or more of
its key words occur together in one corpus text. Script:
`/private/tmp/claude-501/-Users-mike--claude-spares-spare-HctKIa/8d71d8e2-2a2b-4d11-9e18-5d4c3de9a504/scratchpad/pilot.py`
(`python3 -I pilot.py` rewrites `pilot.jsonl`). Output: `pilot.jsonl`, one row per inscription.

| Griffith | REM | Text | Key words in our funerary texts | Verdict |
|---|---|---|---|---|
| Kar. 47 | 0247 | full, 54 words (FHN III 268) | akiNtel 0, deklo 0, amoke 0, nlotil 0, wwikel 0, pedemey 0 | new |
| Kar. 77 | 0277 | full, 23 words (FHN III 269) | akiNtel 0, womnise kroro 0, nptetel 1 | new |
| Kar. 78 | 0278 | full, 34 words (FHN III 264) | akiNtel 0, sekesek 0, absol 0, qorbt 0, iphetel 0 | new |
| Kar. 121 | 0321 | full, 78 words (FHN III 270) | akiNtel 0, pedemey 0, tweteli 0, boqX 0 (adblis 19: a common title) | new |
| Kar. 1, 3, 6, 13, 15 | 0201, 0203, 0206, 0213, 0215 | key words only | amnp (Amanap) 0; Kar. 3 also nlot 0 | new |
| Kar. 10 | 0210 | key words only | areqeb 0 | new |
| Kar. 2, 4, 5, 7, 8, 9, 11, 12, 14, 16 | 0202 … 0216 | key words only | names and standard formulae only, or titles common in ours (SlxS, SSor, pesto) | undecidable |

The FHN texts are converted from FHN's printing of the REM edition: `s`→`S`, `se`→`s`, `ñ`→`N`, the h signs (whose
marks the OCR lost) as `x` in `tedxe`, `xrpxN` and `X` elsewhere, names masked as NAME. They were not compared with
Griffith's copies. Kar. 9 mentions Mash (`mS`), which 3 of our funerary texts also name, so our corpus may hold some
texts of the same region; Karanog's own, judged by Amanap and the viceroys "in Akin", it does not.

## 4. Estimate of the total gain

Method: text counts from the tables of contents and numbering above; words per text from the corpus itself (18,075
words over 662 texts, 27 on average; the four Karanog texts above average 47, but altars are short, so 15 to 27);
overlap from the pilot (Karanog absent) and from what the corpus visibly holds (the three narratives).

| Source | Texts | New texts | Words (15–27 each) |
|---|---|---|---|
| Karanog and Shablul | 150 | about 150 | 2,300–4,000 |
| Meroitic Inscriptions I–II | about 150 | about 140 | 2,100–3,800 |
| Meroe | 51 | about 50 | 750–1,350 |
| Faras (Recueil Champollion) | 46 | up to 46 | 700–1,250 |
| JEA ostraca and REM 0089 | about 46 | about 46 | 300–600 (ostraca are a few words) |
| FHN (overlaps Griffith, counted once) | about 36 | about 30 | (included above) |
| **Total** | **about 480** | **about 460** | **about 6,000–11,000** |

Machine-recoverable today as Latin text: only FHN (about 30 new texts, 600 to 2,000 words, after OCR) and the JEA
transliterations. Everything else needs the Meroitic cursive read from images: by a person at about 2 to 3 minutes
a short text, or by a glyph classifier, which is realistic because Griffith's type and copies use one consistent set
of 23 forms (pp. 18–19 give the table).

## Files

- `data/expansion/pilot.jsonl`: 20 rows (`source`, `page`, `griffith_no`, `rem_no`, `text` or `content`,
  `key_word_hits`, `already_in_corpus` true/false/null, `status`).
- `/private/tmp/claude-501/expansion/karanog/`: the Karanog OCR text, PDF and page images (leaf n144 = p. 129,
  Kar. 1–3).
- `/private/tmp/claude-501/expansion/survey/`: OCR texts of the other volumes and the FHN PDFs with full OCR
  (`fhn/fhn02_ocr.txt`, `fhn/fhn03_ocr.txt`).
