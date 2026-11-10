# REM 1044, the Gebel Barkal stela of King Tanyidamani (Boston MFA 23.736)

Written 2026-11-09 from the inputs in this repo, the FHN II commentary, Rilly's *Dotawo* 7 article and four more
publications found online, in about 75 minutes. Every meaning below carries a tag:

- **[G]** is an accepted meaning from `data/gold_lexicon.json` or `data/gold_morphology.json` (ESTABLISHED), with the
  gold entry's source.
- **[P: who]** is a published proposal that is not in the gold files (PUBLISHED HYPOTHESIS), with the source in
  section 9.
- **[H0]** to **[H14]** are the hypotheses examined in section 6. Each carries its label there: ESTABLISHED, PUBLISHED
  HYPOTHESIS or NEW.
- **[R]** is a reading from Rilly 2020 (*Dotawo* 7), a published proposal like [P].
- **?** means nothing can be said.

## 1. Answer first

1. **Most of the text is still "?"; its frame can be read.** What can be read is a royal protocol (l. 1-3), two
   war reports with the formula "I killed each man, I took each woman" (l. 4-5 and l. 129-132), lists of gods,
   officials and goods counted with numerals and handed to Amun, a long report of killings and seizures of named
   people of "the palace (?)" (l. 141-155), and a close that echoes the funerary benedictions (water, good bread,
   l. 158-161). FHN II calls the contents obscure, and for most clauses that is still true (counts in section 8).
2. **The parallels show a clear skeleton** (section 5):
   - Items are counted "word + numeral"; a total can come after its items (`mk lte wi 12` after twelve 1s, l. 12)
     or before them (`pteno 3` before `apette 1 sber 1 dd 1`, l. 18-19 and 21).
   - The clause `qoleb (Amnp/Amnpte) (i/e)-de-bx(i)` "I gave(?) them (to Amun)" closes four lists or episodes
     (l. 26-27, 115-116, 125-126, 136-137). Rilly translated the first one.
   - The verb(?) `iXlXto` opens four episodes (l. 4, 38, 42-43, 129), three times after `qes` "Kush". Twice the
     kill/take formula follows.
   - Two paragraphs repeat almost word for word (l. 37-40 and 41-44), and the first line of the verso (l. 36) comes
     back as the last line of the text (l. 158-161).
3. **Most of what looked new is already in print.** The "12 gods in all" reading of `mk lte wi 12` and `Mt` = Mut
   are Macadam's, printed by Abdalla in 1969. The second `iblkmni` (l. 34) and the shared `Amnp Nte-se-l` (also in
   REM 1003) are Abdalla's too. `aleqese` has three published meanings, and `-se mlo-l` "the good ..." is Rilly's.
   Seven hypotheses remain NEW (H3 to H8 and H11). The strongest are the `qoleb ... de-bx` formula (H6) and the
   `pteno 3` sub-total (H3).
4. **The inputs have reading errors that change the gloss** (section 2):
   - The Otten file has `iblp mni` (l. 1) and `ibln mnise` (l. 34). Abdalla (from Dunham's photographs) and Ferrandino
     & van Gerven Oei read `iblkmni` both times.
   - The file has `a 500 tero l` (l. 69). Rilly reads `ahtero-l`, with no 500.
   - Spaces in the file often fall at the stone's line ends, not at word ends: `qo leb`, `xl bi`, `e kedtd`,
     `er td`, `ek edeto`, `as r`, `te ritkto`.
   - The gold files have traps here: `sem` "wife" (here `-se mlo-l`), `kdise` "sister" (here `kdi-se-l` "each woman"),
     `wi` "brother" (here `wi` before a numeral) and `lx` listed as a spelling of `lẖ` "great" (here `lxe` and `lX`
     are kept apart).

## 2. The text and its witnesses

| Witness | What it is | Use here |
|---|---|---|
| FHN II no. 152, pp. 665-667 (text), 669-671 (comments) | Printed edition after Hintze 1960 and REM: recto l. 1-35, verso 36-67, right side 68-116, left side 117-161; `,,` dividers, `*` doubtful signs, `[...]` gaps, `( )` restorations | Line numbers and the comments; read from the PDF's text layer (OCR prints ḫ and ẖ both as `h` and ñ as `ri`/`fi`) |
| `data/otten/Data/TanyidamaniNarrative.txt` | One line, stars and brackets kept, `x` = ḫ, `X` = ẖ | The text glossed below |
| `data/corpus_v2.jsonl`, row `tanyidamani` | The Otten file without stars: 721 tokens, 35 numerals | Counts, n-grams, concordances. No second copy of the stela is in `corpus_v2` (checked by 4-gram overlap). |
| Rilly 2020, *Dotawo* 7 | Glossed translations of l. 4-5, 25-26, 68-70, 130-132 and 141-155 | [P: Rilly] |
| Ferrandino & van Gerven Oei 2020 | Glossed translation of l. 1-3 | [P: F&vGO] |
| Abdalla 1969 (Durham PhD thesis) | Notes on dozens of REM 1044 words, partly from Macadam and from Dunham's photographs | [P: Abdalla] |
| Hintze 1960 (*Kush* 8: 125-162), the edition | Not online; seen only through FHN II and Abdalla | [P: Hintze] when cited by them |

Readings that differ, and what is used here:

| Line | Otten file | Other reading | Used here |
|---|---|---|---|
| 1 | `iblp mni` | `iblkmni` (Abdalla 1969, vol. I part 2, pp. 250, 256 n., who calls the `-k-` certain on Dunham's photographs; F&vGO 2020, p. 294) | `iblkmni` |
| 2 | `si mde lw` | `simde-l-w` (F&vGO) | both segmentations shown |
| 2 | `amnpte*,*,*, tese lw te ritkto` | `amnepteteselw teritkto` (F&vGO) | `Amnpte-te-se-lw teritkto` |
| 3 | `sorse` | `qrse` (F&vGO) | both shown |
| 25-26 | `atNN ss mrte l` | `Atnene ssmrte-l` (Rilly ex. 8) | Rilly |
| 34 | `ibln mnise l` | `iblk-mn[i]-s-l` (Abdalla 1969, pp. 250, 256 n.) | `iblkmni-se-l` |
| 40-41 | `ss mrte l` (FHN `ssm-rte`) | `s-ẖr-te-l` (Hintze, via Abdalla 1969, p. 269); `shrte` (Hallof 2020, p. 16) | `ssmrte-l`, disputed |
| 69 | `*a *500 tero l` (FHN the same) | `ahtero-l` (Rilly ex. 49) | both shown; the 500 is doubtful |
| 123-124 | `as r meke` | `asr: meke` (Abdalla 1969, p. 215) | `asr meke` (a line break) |
| 146-147 | `Xol *k leb` | `holno-leb` (Rilly ex. 54) | both shown |
| 21, 23 | `pteno 3`, `mrm 9` | FHN prints `(pteno)` and `(9)` in parentheses: restored, not read | marked as restored |

## 3. Segmentation

The text alternates protocol and narrative with counted lists. Of the list sections, S3 ends in a total
(`wi 12`), S6, S14 and S15 end in the `qoleb ... de-bx` clause [H6], and S4 and S5 end in neither.

| Id | FHN lines | Kind | Content | Key words |
|---|---|---|---|---|
| S1 | 1-3 | Protocol | King, name, `aleqese`, epithets, Amun of Napata, Kush | `qore Tñyidamani aleqese iblkmni ... Amnpte-te-se-lw ... qes ... iplte` |
| S2 | 3-6 | War report 1 | Kush, then "I killed each man, I took each woman" | `tqN-l qes iXlXto abr-se-l e-ked kdi-se-l e-r-k` |
| S3 | 6-12 | List of gods | Amun of Arre(?); twelve deities, each "1"; total 12 | `Amnp arreto mk lte ... edxN 1 Mno 1 ... Mk lte wi 12` |
| S4 | 13-17 | List | Items with 120 and 10 | `aqqibese 120 ... stn 10 ...` |
| S5 | 17-23 | Two parallel lists | For `qore mdese` and for `nmrolde s qorese`: 3, a total 3 = 1+1+1, then `amote mrm 8` / `9` | `pteno 3 apette 1 sber 1 dd 1 ... amote mrm 8` |
| S6 | 23-27 | Officials to Amun | Titles with 3s; two named officials "given" to Amun | `ameloloke imlotror wtotrse 3 ... qoleb Amnp i-de-bx` |
| S7 | 27-35 | Narrative, titles | Governors, Amun "great", the protocol epithet again, `-to` verbs | `xrpx se-mlo-l ... eqeloXe lX ... iblkmni-se-l ... ixXtto` |
| S8 | 36-37 | Verso opening | A line that returns as the last line | `sedew tbe tXe lw qes molk seb eqetxe` |
| S9 | 37-45 | Two parallel episodes | "And also" the crown prince ..., Kush + verb, `ed kete`, `wkete` (twice) | `kelw ... pqr qorise-l itnkk iXlXto seb-l ed kete kek ...` |
| S10 | 45-55 | Gods and places | Prophet(?) of Amun of Napata, Isis and Horus of Sai, Meroe, Amun | `Amnpte mk sxN-l ... Wost Sye(te) Art Syete ... Mdedewi-k` |
| S11 | 56-67 | Damaged lists | Women, `wi` after items, bulls(?), Adenodor-te | `kdi-l ... adenodorte ... xlbe tke ... xlbi wi` |
| S12 | 68-74 | Seizure | "seized them" (Rilly), Amun of Napata, bulls(?) | `qoleb ahtero-l am w-kb-bx-te Amnpte ... xlbi wido edeto` |
| S13 | 75-103 | Narrative | Amun, Meroe twice, "the palace (?)" three times | `qorte drte aqqe qorte msyose ... Medewite li ... Amnp Nte-se-l` |
| S14 | 103-116 | List with a verb after each item | Officials or priests with 3, 5, 8; each then `ipxto`; close `qoleb de-bx` | `ameloloke-l mse 3 ipxto ... ameri 5 ipxto ... qoleb de-bx` |
| S15 | 117-126 | List | Napata; animals 5000; given to Amun of Napata | `itrek asr deb 5000 Npte ... qoleb Amnpte i-de-bx-i` |
| S16 | 126-156 | War report 2 and the killings | Kush, kill/take formula again, Amun, then named victims "of the palace (?)" | `qes iXlXto tqN-l abr-se-l e-ked-td ... e-kede-to ... w-er-k` |
| S17 | 157-161 | Close | Water, good bread, Kush, the verso's first line again | `ato sedew ato mlo qes Xolk seb eqetx[e]` |

## 4. Interlinear gloss

Spelling follows the corpus (`x` = ḫ, `X` = ẖ, Rilly's `h`; `N` = ñ; `S` = š), with words that the Otten file splits
at line ends rejoined. Abbreviations:

- DET `-l/-li` [G `-l`, Rilly 2016 pp. 7-8]; PL.DET `-leb` [G, Rilly 2016 p. 7]; GEN `-se` [G, Rilly 2016 p. 7];
  LOC `-te` [G, Rilly 2016 p. 8]; ACC `-w` [G, probable, Rilly 2016 p. 7]; COP `-o` [G].
- EACH `-se` on a counted noun [G `-se (each)`, debated, Rilly 2010 p. 138; Rilly 2020].
- VN `-x(e)` singular, `-bx(e)` plural object [G `-ḫ(e)`, `-bḫ(e)`, probable; Rilly 2020].
- [R] marks Rilly 2020's analyses: 1SG `e-` (and `i-` in `i-de-bx`), PLC `-k` "repeatedly", TAM `-to`/`-td`
  "tense or aspect", PM `w-` "a person marker, unexplained", `qoleb` 3PL "them".

### S1. Protocol (l. 1-3)

| Meroitic | Gloss | Status |
|---|---|---|
| `qore` | king, ruler | [G `qore`, Rilly 2016 p. 9] |
| `Tñyidamani` | Tanyidamani (royal name) | Name (FHN II no. 150) |
| `aleqese` | ? | Three published meanings, none settled: "monument, inscription" [P: Hintze 1960, 142, via FHN II p. 669]; an adverb, cognate of Old Nubian ⲁⲗⲉⲥⲛ̄ "if" [P: F&vGO 2020, p. 299]; "(written) announcement" [P: Hallof 2020, p. 13]. Also in REM 1003 l. 16, REM 1041A, REM 1141. See [H12]. |
| `iblkmni` | ?-Amun | `mni` [G `amni`, variant `mni`, Rilly 2016 p. 4]; `iblk-mni` "iblk-Amon" [P: F&vGO, p. 294]. Recurs at l. 34 [P: Abdalla 1969, pp. 250, 256 n.]. |
| `simde-l-w` (Otten `si mde lw`) | ?-DET-ACC | F&vGO (n. 12): unknown, apparently built on a noun `mde`. `mde` also in l. 135-136 `s mde se lw`. |
| `terite` | ? | ?; `terit-` recurs in `teritkto` (l. 2-3) and `teritibre` (l. 17-18) |
| `Amnpte-te-se-lw` | Amun of Napata-LOC-GEN-DET.ACC | [G `amnpte`, Rilly 2016 p. 8]; "under the protection of Amon at Napata" [P: F&vGO] |
| `teritkto` | ? (verb, `-to` TAM?) | `-to` [R] |
| `qes` | Kush | [G `qes`, probable] |
| `sorse` / `qrse` | ? / qr-GEN | F&vGO read `qrse`; their n. 13 suggests `qr` may mean "royal" |
| `iplte` | 1SG?-grant(?)-? | [P: F&vGO: `i-pl-te`, 1SG prefix + "grant(?)"]; compare `ipleto` (l. 50), `iple` (l. 44), `iplemX` (l. 83). [H4] |

F&vGO's translation of l. 1-3, in outline: King Taneyidamani; `aleqese` and the epithets left untranslated; Amun at
Napata as protector; then "I(?) grant(?)" with Kush as the object.

### S2. War report 1 (l. 3-6)

| Meroitic | Gloss | Status |
|---|---|---|
| `eqeXm de` | ? | `eqe-` a past-tense or "temporal" prefix [P: Hintze 1960, 143 f., via FHN II p. 669]; the rest ? |
| `nk[.]pom kek` | ? ? | ? (`kek` 5 times in the stela, nowhere else in the corpus) |
| `tqN-l` | ?-DET | ?; again before the second war report (l. 130), so a name or a noun of that formula [H5] |
| `qes iXlXto` | Kush 1SG?-?-TAM? | `qes` [G]; `iXlXto` ? as a word; as an `i-…-to` verb [H4]; `iXlXto` opens four episodes [H5] |
| `abr-se-l e-ked` | man-EACH-DET 1SG-kill | "I killed each man" [G `abr`, `ked`; R ex. 35] |
| `kdi-se-l e-r-k` | woman-EACH-DET 1SG-take-PLC | "I (repeatedly) took each woman" [G `kdi`, `are-/erk-`; R ex. 35]. Not [G `kdise` "sister"]. |
| `esebe nt[.]k` | ? ? | ? |

### S3. Amun of Arre and the twelve gods (l. 6-12)

| Meroitic | Gloss | Status |
|---|---|---|
| `Amnp arreto` | Amun ?-? | "Amun of Opet (Luxor) of Arere (Wadi es-Sebua?)", read `Arre-se-lo` [P: FHN II p. 670, after Török 1979]. Compare REM 1003 `amni arrese-se` "Amun (living) in Arre" [P: Baldi 2016, after Griffith]. |
| `mk lte` | god ?-? | `mk` [G "god", Rilly 2016 p. 7]; `mk-l-te` god-DET-LOC, "divinity" or "temple, shrine" [P: Hintze 1960, 145, via Abdalla 1969, p. 215] |
| `ntkte` | ? | ? |
| `Amnpte` | Amun of Napata | [G] |
| `eqeti sxe eqeloXe` | ? ? ? | `eqe-` [P: Hintze]; `eqeti pxe` recurs (l. 17, 25), `eqeloXe` three times (l. 7, 31, 32) |
| `Amnp qoro mrtxe` | Amun ? ? | `Amnp` [G variant of `amnpte`]; but this text also has `Amnpte` as a separate god [H13]; `qoro` ? (again in l. 9) |
| `edxN 1` | ? 1 | A heading word that goes with numerals in records of donations (?) or taxes (?) [P: Török 1984, 175 ff., via FHN II p. 670]. But `Amnp qoro mrtxe edxN 1` has the same shape as `Amnp qoro axboroteN 1` two items later, and a heading would not take its own `1`; Abdalla counts this `Amnp` as the first of the twelve [H1]. |
| `Mno 1` | Amun 1 | [P: FHN II p. 670]; compare [G `amni` variants `mni`, `amn`] |
| `Amnpte 1` | Amun of Napata 1 | [G] |
| `Aqedise 1` | Khonsu 1 | [P: FHN II p. 670, from the god's caption in REM 0009] |
| `Wos txN mtotiwxne 1` | Isis ? ? 1 | `Wos` [G "Isis"]; `txN`, `mtotiwxne` ? (epithets?) |
| `Amnp qoro axboroteN 1` | Amun ? ? 1 | "Amun of Luxor" [P: FHN II p. 670] [H13]; the rest ? |
| `Amnb 1` | Amun of Pnubs (?) 1 | [P: FHN II p. 670, with "?"] |
| `[...] 1` | [lost] 1 | Lacuna |
| `Mne meke 1` | Amun ? 1 | `Mne` = Amun [P: FHN II]; `meke` a theonym, compare REM 1003 [P: FHN II p. 670] |
| `Mkedo pxtotN 1` | ? ? 1 | `mke-do` [P: Abdalla 1969, p. 216, in his count of deities]; otherwise ? |
| `Mt 1` | Mut 1 | [P: Abdalla 1969, p. 216, "mt (Mūt)"] [H2] |
| `tepede xtebemeyose 1` | ? ? 1 | Counted as a twelfth "group" [P: Abdalla 1969, p. 216] |
| `Mk lte wi 12` | god-DET-LOC total(?) 12 | "total (is) 12 gods" [P: Macadam, in Abdalla 1969, p. 216] [H1] |

### S4. List with 120 and 10 (l. 13-17)

| Meroitic | Gloss | Status |
|---|---|---|
| `aqqibese 120` | ?-GEN? 120 | ? |
| `(Am)np apnewke` | Amun ? | `Amnp` [G]; `apnewke` ? |
| `ameri mrmse li` | ? ?-GEN?-DET | `ameri` a temple official for augury and oracles [P: Abdalla 1969, vol. I part 2, p. 240, tentative]; `mrm-` recurs in `mrm 8/9` (S5) and `mrmr lw` (S11) |
| `eqe[...]r mlotey etepnk` | ? ? ? | `eqe-` [P: Hintze]; ? |
| `stn 10` | ? 10 | ? |
| `[...]tepi ttN ten wekid` | ? | ? |
| `eqesero(r) asrlitoN` | ? ? | `asr` "meat, animal" [G] may be inside `asrlitoN`; a guess |
| `mse` | child (?) | [G `mte` variant `mse`]; `mse` occurs nowhere outside this stela in `corpus_v2`, so the gloss is not checked |
| `wte mro si` | life ? ? | `wte` "life" [P: Priese 1977, 47 f., via FHN II p. 664]; FHN compares the cartouche epithet `wte lhte`. `wte mre-se` "well-being" [P: Monneret de Villard, via Abdalla 1969, p. 37] |

### S5. Two parallel lists (l. 17-23)

| Meroitic | Gloss | Status |
|---|---|---|
| `eqeti pxe mrxi keN teritibre` | ? ? ? ? ? | `eqe-` [P: Hintze]; `teritibre` shares `terit-` with l. 2 |
| `qore mdese 3` | king ? 3 | `qore` [G]; `mdes` "direct descendant (?)" [P: Millet 1968, Kharamadoye `qore ariteN-l mdes`, `Kalabsha_Millet.txt` l. 15] |
| `ti mXe` | ? abundant | `mXe` [G "abundant, plenty"] |
| `pteno 3` | ? 3 | A total of the next three items [H3] |
| `apette 1 sber 1 dd 1` | ? 1 ? 1 ? 1 | `apette` ? (looks like [G `apote`/`apete` "envoy"], unproven) [H3]; `sber` ? (again in `sberxi`, l. 50); `dd` ? (Rilly 2020 n. 95 has `d` "house" in booty lists) |
| `a[..] aripe[..]` | ? | Damaged |
| `amote mrm 8` | ? ? 8 | ? |
| `nmrolde s qorese mse 3` | ? GEN king-GEN child(?) 3 | `qore-se` [G]; `mse` see S4 |
| `ti mXe (pteno) 3 apette 1 sber 1 dd 1` | as above | FHN restores `pteno`; the 3 and the 1s are read |
| `a[...]bete leb tbi te[...]` | ? PL.DET ? ? | `tbi` again in l. 37 and REM 1003 (`tbi tnideb xe qore`) |
| `am(ote) mrm (9)` | ? ? 9 | FHN restores `ote` and the 9 |

### S6. Officials given to Amun (l. 23-27)

| Meroitic | Gloss | Status |
|---|---|---|
| `[...]ke amotror` | ? ? | ? (`amote` in S5) |
| `ameloloke` | a title | "title of official" [P: FHN II p. 670]; = `beloloke` [H8] |
| `imlotror wtotrse 3` | Imalutarura (name) title 3 | Name [P: FHN II p. 670 "probably a personal name"; Rilly ex. 8 "Imalutarura"]; `wtotrse` a title [R ex. 8]. The `3` here stands where l. 26 has `-l`. |
| `iddne ssime` | ? title | `ssime` compare the priestly title `ssimete` [P: Török 1977, 416, via FHN II p. 670] |
| `Amnise 3` | Amun-GEN 3 | [G `amni`, `-se`] |
| `areN li` | ?-DET | ? |
| `eqeti pxe` | ? ? | as in l. 17 |
| `Atnene ssmrte-l` | Atanene title-DET | [R ex. 8]; the title `ssmrte` again in l. 40-41 [P: Abdalla 1969, p. 269] |
| `Imlotror wtotrse-l` | Imalutarura title-DET | [R ex. 8] |
| `qoleb Amnp i-de-bx` | them Amun 1SG-give(?)-VN.PL | "Atanene, the ssmrte (and) Imalutarura, the wtotrse, I gave(?) them to Amanap" [R ex. 8]. The same clause closes three more sections [H6]. |

### S7. Narrative with titles (l. 27-35)

| Meroitic | Gloss | Status |
|---|---|---|
| `atrXli-l Xrto` | ?-DET ? | `Xrto` a verb "without prefix" in Hintze's classification [P: Hintze, via Abdalla 1969, p. 268] |
| `mk abenbidpete wi abenbk` | god ? ? ? | `mk` [G]; the rest ? (`wi` here is not before a numeral) |
| `epxwN eqxwN ipxpx mrXdtose` | ? ? ? ? | ? |
| `xrpx se-mlo-l` (Otten `xrpx sem lo l`) | governor(?) GEN?-good-DET | `xrpx(e)` [G "governor (?)", debated, Millet 1968]; `-se-mlo-l` "the good" [R ex. 54] [H10]; not [G `sem` "wife"] |
| `trek adt wi ipk` | ? ? ? ? | ? |
| `Amnp yotre mle wideto` | Amun ? good? ? | `mle` compare [G `mlo` "good"]; `wide` [G "brother"] would be a guess here |
| `pmsen eqeloXe lX` | ? ? great | `lX` [G `lẖ` "great"] |
| `Ariteñyose-l Merose-li si tesont` | ?-DET ?-DET ? ? | `ariteN` also opens Kharamadoye's protocol (`qore ariteN-l mdes`); ? |
| `eqeloXe lX-l` | ? great-DET | as above |
| `qoleb elbto` | them ?-TAM | `qoleb` [R]; `elbto` compare [G `l-` "give"] with `-b` and `-to`: a guess |
| `Amnp atoo lX itwdto` | Amun ? great ? | `lX` [G]; `itwdto` again at l. 119 |
| `nir ketp wi` | ? ? ? | `nir` also in REM 1141 (`nir-l`) [P: Hallof 2020, p. 14]; ? |
| `iblkmni-se-l yonpxto` | ?-Amun-GEN-DET ? | The protocol epithet again [P: Abdalla 1969]; `yonpxto` ? |
| `Aro eqe` | ? ? | `aro` also in REM 1003 (`aro bel`); ? |
| `xrpxN wit qeper ado-l` | governor(?) ? ? ?-DET | [G `ḫrpḫe`, variant `xrpxN`]; `qeper` also in REM 1003 l. 4, in the slot of `perite` "agent" (`hamadab.md` H4) |
| `tedeqe-l elx ixXtto` | ?-DET ? ? | `elx` compare `el-x` in REM 1141, glossed "to give" + suffix [P: F&vGO, p. 295], and [G `l-` "give"]: a guess |

### S8. Verso opening (l. 36-37)

| Meroitic | Gloss | Status |
|---|---|---|
| `sedew tbe tXe lw` | ? two(?) ? DET.ACC? | `tbe` [G `tbo`, variant `tbe`, "two"]: in this context a guess |
| `qes molk seb` | Kush ? ? | `qes` [G]; `seb` 9 times in this stela and 16 in REM 1003, nowhere else: a narrative connective? `molk` compare `Xolk` (l. 41, 160) [H11] |
| `eqetxe kwi` | ? ? | `kwi` looks like [G `-kwi` "plural copula"]; as a free word it is ? |
| `ittmito` | ? | an `i-…-to` form [H4] |

### S9. Two parallel episodes (l. 37-45)

| Meroitic | Gloss | Status |
|---|---|---|
| `kelw tbi ble` | and ? ? | `kelw` [G "and, also"] |
| `pqr qorise-l` | prince king-GEN-DET | "pqr of the king", the crown prince's title [G `pqr`; FHN II p. 670, after Török 1977a] |
| `itnkk iXlXto` | ? ? | `i-…-to` forms [H4]; `qes iXlXto` [H5] |
| `seb-l ed kete kek` | ?-DET ? ? ? | `-kete` is [G plural imperative/optative ending of benedictions]; whether `ed kete` is that ending in a narrative is ? |
| `dqnik nmrok yoto sbw wkete qesN` | ? ? ? ? ? Kush? | `dqni` and its forms (`dqnik`, `dqeni`) six times in the stela, nowhere else in the corpus; `wkete` compare PM `w-` [R]: a guess |
| `kelw ssmrte-l Xolk tme` | and title-DET ? ? | `ssmrte` as in l. 26 [P: Abdalla 1969, p. 269]; Hintze and Hallof read this word with ẖ (section 2) |
| `pkr tr qorise kdise lxe no-l` | prince great(?) king-GEN ? ? ?-DET | `pkr tr qori-se` the crown prince's title [P: FHN II p. 670]; F&vGO (p. 295) gloss `pkr-tr` in REM 1141 as title + adjective "great" |
| `qes itnk iXlXto` | Kush ? ? | as in l. 38 [H5] |
| `seb-l ed kete kek yoto wkete` | as in l. 39-40 | Repeats l. 39-40 [H5] |
| `adb wse-li` | land his-DET | `adb` [G "land, territory", probable]; `wse` "his" [H7] |
| `iple mo kete dqni brN sqtdon kek` | ? ? ? ? ? ? ? | ? |

### S10. Gods and places (l. 45-55)

| Meroitic | Gloss | Status |
|---|---|---|
| `Amnpte mk sxN-l` | Amun of Napata prophet(?)-DET | `mk-sxe` "prophet" (Egyptian ḥm-nṯr) [P: Abdalla 1969, pp. 218-219] |
| `irxto idktey` | ? ? | `i-…-to` [H4] |
| `armi Mnise` | ? Amun-GEN | `armi` a title [P: Abdalla 1969, p. 169]; not "Rome" |
| `s qorose Amnptese yotkto` | GEN ? Amun-of-Napata-GEN ? | `yotkto` read `ye-tk-te`, a form of the verb `tk` [P: Abdalla 1969, pp. 109-110]; compare [G `tkk` "plunder"] |
| `edeke adbite li` | ? land-LOC DET | `adb-ite` [G `adb`, `-te`] |
| `imliN ndeye lte ynkteketo` | ? ? ? ? | ? |
| `Amnp kek Sor sberxi ipleto` | Amun ? ? ? ? | FHN capitalises `Sor` as a name; `ser` "book" [P: Griffith 1916, JEA 3, 26, and Hintze 1960, 152 on this line, via Abdalla 1969]; ? |
| `mk Sor lxe ple` | god ? ? ? | ? (`lxe` is not [G `lẖ`], which is spelled `lX`) |
| `Amni-s kdite` | Amun-GEN sister? | `kdite` [G "sister"]; in this list "Amun's sister" is a guess |
| `Wost Sye(te)` | Isis of Sai | [P: FHN II p. 670, after Priese 1984, 492; Abdalla 1969, p. 171]; `Sye` [G "Sai"] |
| `Art Syete` | Horus of Sai | [P: FHN II p. 670; Abdalla 1969, p. 171] |
| `s wey senbote [...]te lise` | GEN ? ? ?-GEN.DET? | `s wey senbote` twice (l. 52, 53-54) |
| `Mdedewi-k esxte [..]Nbe[...]ke` | Meroe-to/from ? ? | `Medewi` [G `bedewe` variant `medewi`]; `-k` with place names [P: Griffith 1912, 30, via FHN II p. 670]; [G `-ke`, debated] |
| `senbote ptri lise` | ? ? ? | ? |
| `dqni ere tese` | ? ? ? | ? |
| `Amnp netese mlo-l eqe[...]de[.]wo` | Amun ? good-DET ? | `Amnp Nte-se` epithet [H9]; `mlo` [G "good"] |

### S11. Damaged lists (l. 56-67)

| Meroitic | Gloss | Status |
|---|---|---|
| `seb at[...] kdi-l [..]w` | ? ? woman-DET ? | `kdi` [G] |
| `q[...]me qryonew mr tb r ke lw` | ? | ? |
| `apeNsebo se wi` | ? ? ? | ? |
| `mrmr lw adenodorte` | ? ? Adenodor-LOC | "unidentified toponym" [P: FHN II p. 670] |
| `[...][ik/me] s Mni esetesi er syt-l moste[.]q mrotese adose bose wi` | ... Amun ... | `Mni` [G]; the rest ? |
| `mrmr lw s wey xlbe tke` | ? ? GEN ? bull(?) ? | `xlbe` compare [G `xlbi` "bull, ox"]; `tke` compare [G `tke-` "love"]: both guesses |
| `s qr li p[...]se attiw alwi lX-l ere tese` | ... great-DET ... | `attiw alwi` again in l. 72 |
| `Nte Amnpte pelxelq [...]rte npletno wi trw[...]nide tereqebte d[...]t b[.]k` | ... Amun of Napata ... | ? |
| `xlbi wi mdetese p[...]` | bull(?) ? ? | `xlbi` [G], but `xlbiN` is also a title (l. 108) [P: Hofmann 1981, 103, via FHN II] |

### S12. Seizure (l. 68-74)

| Meroitic | Gloss | Status |
|---|---|---|
| `axle qoleb ahtero-l am w-kb-bx-te` | ? them ?-DET ? PM-seize-VN.PL-TAM | "? seized ? them ???" [R ex. 49, reading `heHle` for `axle` and `ahtero-l`]. FHN and Otten read `a 500 tero-l`. |
| `Amnpte eqetid` | Amun of Napata ? | `eqe-` [P: Hintze] |
| `attiw alwi-l dtrep[.] lw` | ? ?-DET ? ? | ? |
| `xlbi wido edeto` | bull(?) ? ? | ? (`wido` also in REM 1003 and Kharamadoye) |

### S13. Narrative with Meroe and the palace (l. 75-103)

| Meroitic | Gloss | Status |
|---|---|---|
| `Amnp nexeose dqni bereqob artroti ax plete apreqn` | Amun ? ... | ? |
| `seb lxe noke ke[.]ot nbrtd` | ? ? ? ? ? | `seb lxe` also in REM 1003 (`seb lxe eno wite`) |
| `ado bese-l yo plet erew ke iplemX stxN bere ke aqen li erese` | ? ... | ? |
| `Medewi yoto` (Otten `mede wi yoto`) | Meroe ? | `Medewi` [P: FHN II p. 670 lists l. 85]; [G `medewi`] |
| `s qdte lise sbe[..] bere ke aroqi tm` | ? ... | `aroqi tm` compare the name `Aroqitm` (l. 153-154) |
| `qorte drte aqqe qorte msyose [.]eto qorte tqeyose li` | palace(?) ? ? palace(?) ? ? palace(?) ?-DET | `qorte` "palace (?)" [R ex. 50, 54]; `drte` compare `drteyose-l` (l. 142) |
| `Xrote mwetre li qoleb troXe li wi mke` | ? ? them ? ? god? | `qoleb` [R]; `mke` compare [G `mk`] |
| `[..]ed[..]td kdi-l emo[..]l ntk-l wb-l` | ... woman-DET ... | `kdi` [G] |
| `Medewite li yodrpt` | Meroe-LOC-DET ? | [G `medewi`, `-te`]; FHN II lists l. 97 f. |
| `Amnp Nte-se-l seb ayol pe[..]bede li` | Amun ?-GEN-DET ? ? | [H9] |
| `mXo ken t[.]te qes lX-l` | ? ? ? Kush great-DET | `qes` [G], `lX` [G]; `mXo` compare [G `mẖe`] |

### S14. List with a verb after each item (l. 103-116)

| Meroitic | Gloss | Status |
|---|---|---|
| `[...]se-l [...]a[...]to ere[...]de yo [...]` | damaged | ? |
| `xlbiN ameloloke-l mse 3 ipxto` | title title-DET child(?) 3 1SG?-?-TAM | `xlbiN` "title of an official, mainly in Lower Nubia" [P: Hofmann 1981, 103, via FHN II]; `ameloloke` [H8]; `ipxto` [H4] |
| `pwore s sor-l ameri 5 ipxto` | ? GEN priest(title)-DET ? 5 ? | `ssor` priestly title [P: FHN II p. 670; Török 1977]; [G `ssor` "scribe", Rilly 2016]; `ameri` [P: Abdalla 1969, p. 240, who segments `s-sor-l ameri (number) i-p[x]-te`] |
| `Amni-l de [..] ipxto` | Amun-DET ? ? | [G `amni`] |
| `pti pXete p Xol 8 ipxto` | ? ? ? ? 8 ? | `Xol` [H11] |
| `qoleb de-bx akli [...]` | them give(?)-VN.PL ? | [H6]; `de-b-x` is grouped with `i-de-b-x` and `e-de-b-x` as one verb [P: Abdalla 1969, vol. I part 1, p. 43] |

### S15. Napata and 5000 animals (l. 117-126)

| Meroitic | Gloss | Status |
|---|---|---|
| `[...]d[..]i Amnpte attomi[.] itwdto` | ... Amun of Napata ? ? | `itwdto` as in l. 33 |
| `ibereqo k ilolto` | ? ? ? | `i-lel-te` a verb [P: Hintze 1960, 161 no. 1, via Abdalla 1969, p. 250]; [H4] |
| `dqeni w-l itrek` | ? ?-DET ? | ? |
| `asr deb 5000` | meat/animal ? 5000 | `asr` [G "meat, animal", Rilly 2016 p. 9]; `deb` ? (also in REM 1003 `axi-deb-x`); the count is of animals ([P: none]; see `verification.md`, claim 4) |
| `Npte wel nlo-l akitkto` | Napata ? ?-DET ? | `Npte` [G "Napata"]; `a-ki-tk-te` listed with the verb `tk` [P: Abdalla 1969, vol. I part 2, p. 9]; compare [G `tkk` "plunder"] |
| `asr meke idNte nd kete` | animal god(?) ? ? ? | `asr` [G]; `meke` [P: FHN II "theonym"] |
| `qoleb Amnpte i-de-bx-i` | them Amun of Napata 1SG-give(?)-VN.PL-? | [H6]; compare [R ex. 8] |

### S16. War report 2 and the killings (l. 126-156)

| Meroitic | Gloss | Status |
|---|---|---|
| `seb krte dse-l 7 k be sxto` | ? ? ?-DET 7 ? ? ? | `seb krte` also opens REM 1003's refrain (`seb krte-li`) |
| `kedd Npte p lw` | ? Napata ? ? | `kedd` ?; compare [G `ked` "kill"]: a guess; `Npte` [G] |
| `qes iXlXto tqN-l` | Kush ? ?-DET | [H5] |
| `abr-se-l e-ked-td` | man-EACH-DET 1SG-kill-TAM | [G `abr`, `ked`; R Table 2] |
| `kdi-se-l e-r-td` | woman-EACH-DET 1SG-take-TAM | [G `kdi`, `are-`; R Table 2] |
| `ayot Amnp Nte se-mlo-l` | ? Amun ? GEN-good-DET | [H9], [H10] |
| `ese be Amni elx` | ? ? Amun ? | ? |
| `mr de qorisew s mde se lw inweto` | ? ? king-GEN-ACC? GEN ? ? ? | `inweto` [H4] |
| `qoleb e-de-bx` | them 1SG-give(?)-VN.PL | [H6] |
| `krtedse xrpxe-se-mlo-l tk lise wdto artde` | ? governor(?)-GEN-good-DET seize? ? ? ? | Rilly's `krtedse` as one word (ex. 54); `tk` [G `tkk` "plunder"] |
| `krte d sete tkk` | ? ? ? plunder | `tkk` [G, probable, Rilly 2010] |
| `Ahotone qorte drteyose-l e-kede-to` | Akhutune palace(?) ?-DET 1SG-kill-TAM | "I killed Akhutune, the ??? of the palace(?)" [R ex. 54] |
| `Nhror wide-l e-kede-to` | Nakharura brother-DET 1SG-kill-TAM | "I killed (his) brother Nakharura" [R ex. 42; G `wide` "brother"] |
| `kdi ste-bese dnetro` | woman tutor-their ? | "I ??? their mother" [R ex. 54]; [G `ste` "mother (tutor)"] |
| `sxse li holno-leb asxdose tedd` (Otten `sxse li Xol k leb as xdose tedd`) | ? | "???" [R ex. 54] |
| `qoleb axro tewideb-wit e-ked-b-to` | them ? ? 1SG-kill-VN.PL-TAM | "I killed them, ???" [R ex. 43] |
| `krtedse xrpxe-se-mlo-l tk-to` | ? governor(?)-GEN-good-DET seize-TAM | "I seized the good ??? governor" [R ex. 54] |
| `qorte dxe-leb wide-bese Aroqitm Tdxsene w-er-k` | palace(?) child-PL.DET brother-their Aruqitama Tadakhesene(?) PM-take-PLC | "? captured the children of the palace(?) (and) their brothers Aruqitama and Tadakhesene(?)" [R ex. 50]. Rilly also offers a second reading, in which the children and Aruqitama are the topic and Tadakhesene the one captured. |
| `seb erewese lo se wi aw i[...]bx` | ? ? ? ? ? ? ? | ? |

### S17. Close (l. 157-161)

| Meroitic | Gloss | Status |
|---|---|---|
| `dqni ibtd[...]rq Xrw [...]ki` | ? ? ? ? | `Xrw` compare [G `ẖr` "north", variant `ẖrw`]: a guess |
| `ato sedew` | water ? | `ato` [G "water"]; `sedew` as in l. 36 [H11] |
| `at mlo` (FHN `*a*to mlo`) | bread good | "good bread" [P: FHN II p. 671, after Griffith 1911, 49; Hintze 1960, 160 relates the passage to benediction formulae A and B]; [G `at`, `mlo`] |
| `qes Xolk seb eqetx[...]` | Kush ? ? ? | as in l. 36 [H11] |

## 5. The structure the parallels reveal

Counts are from `corpus_v2` (the stela 721 tokens; the rest of the corpus 659 funerary texts plus REM 1003 and
Kharamadoye), with `src/kwic.py` and two short n-gram and regex scripts run in the session scratchpad (not part of
the repo).

### 5.1 Repeated phrases inside the stela

| Phrase | Where (FHN lines) | What repeats |
|---|---|---|
| `3 ti mXe pteno 3 apette 1 sber 1 dd 1 a[..]` | 18-19, 21 | A whole list, for two recipients (`qore mdese`, `nmrolde s qorese mse`) |
| `amote mrm 8` / `am(ote) mrm (9)` | 20, 23 | The line after each of those two lists |
| `iXlXto seb-l ed kete kek ... yoto ... wkete` | 38-40, 43-44 | A whole paragraph, after `pqr qorise-l` and after `pkr tr qorise` |
| `qes iXlXto` | 4, 129 (and `itnk(k) iXlXto` 38, 42-43) | Opening of an episode [H5] |
| `tqN-l` + `abr-se-l e-ked` + `kdi-se-l e-r-` | 4-5, 130-132 | The war formula, with `e-r-k` the first time and `e-r-td` the second |
| `qoleb (Amnp/Amnpte) (i/e)-de-bx(i)` | 26-27, 115-116, 125-126, 136-137 | Closing clause [H6] |
| `krtedse xrpxe-se-mlo-l` + verb | 137-139, 150-151 | "the good governor" seized (Rilly) |
| `qorte` | 89, 90, 91-92, 142, 152 | "palace (?)" (Rilly) |
| `Amnp Nte-se(-mlo)-l` | 54-55, 99-100, 132-133 | An epithet of Amun [H9] |
| `eqeti pxe` | 17, 25 | ? |
| `eqeloXe lX` | 31, 32 | "... great" |
| `imlotror wtotrse` | 24, 26 | A named official with his title |
| `ssmrte-l` | 26, 40-41 | A title (the reading at 40-41 is disputed, section 2) |
| `iblkmni` | 1, 34 | The protocol epithet |
| `s wey senbote` | 52, 53-54 | ? |
| `attiw alwi` | 63, 72 | ? |
| `mk lte` | 6, 12 | "god(s)" + DET + LOC |
| `sedew ... qes molk/Xolk seb eqetxe` | 36-37, 158-161 | The verso's first line is the text's last [H11] |

### 5.2 List formulas

- **Item + numeral.** The stela has 35 numerals. Wherever the counted item is known (the gods, the `pteno` items),
  the numeral follows it (`edxN 1`, `Wos ... 1`, `apette 1`). The 18 ones are 12 in the god list and 6 in the two
  `pteno` lists.
- **Totals.** `wi` + numeral occurs once here, `Mk lte wi 12` after exactly twelve 1s. In the whole corpus it occurs
  only twice more, at REM 1003's closings `wi 1626` and `wi 1032` (`verification.md`, claim 3). A bare total
  stands before its items in `pteno 3: apette 1, sber 1, dd 1` [H3].
- **Numbers that close nothing.** `aqqibese 120`, `stn 10`, `mrm 8`, `mrm 9`, `wtotrse 3`, `Amnise 3`,
  `mse 3` (twice), `ameri 5`, `Xol 8`, `deb 5000` and `dse-l 7` add up to no stated total.
- **A verb after each counted item.** In S14 each item is followed by `ipxto`: `ameloloke-l mse 3 ipxto`,
  `ameri 5 ipxto`, `Amni-l de [..] ipxto`, `p Xol 8 ipxto`, and then `qoleb de-bx`. That is the shape of an
  allocation list: "N of X, I ...; N of Y, I ...; them I gave(?)".

### 5.3 Gods and places

- **Gods:** Amun as `Mno`, `Mne`, `Mni`, `Amni` [G `amni`]; Amun of Napata `Amnpte` (8 times) [G]; `Amnp`
  (12 times) [G as a variant; FHN II: Amun of Luxor] [H13]; Amun of Arre `Amnp arreto` [P: FHN II]; Amun of Pnubs (?)
  `Amnb` [P: FHN II]; Khonsu `Aqedise` [P: FHN II]; Isis `Wos` [G], Isis of Sai `Wost Sye(te)` [P: FHN II];
  Horus of Sai `Art Syete` [P: FHN II]; Mut `Mt` [H2]; `Meke` [P: FHN II]; `mk` "god" (5 times) [G]; `Sor` (twice)
  ?. The lunette shows Amun of Thebes and Amun of Napata side by side, and Amun with Mut (FHN II pp. 668-669).
- **Places:** Kush `qes` (7 times as a word, plus `qesN`) [G]; Napata `Npte` (l. 122, 128) [G]; Meroe `Medewi`
  (l. 53 `Mdedewi-k`, 85, 97-98 `Medewite`) [G]; Sai `Sye` [G]; `Adenodor-te` [P: FHN II, unidentified];
  `Arre` [P: FHN II]. `armi` is a title [P: Abdalla], not Rome.
- **Corpus check:** `Amnp` occurs 12 times here and 4 times in the rest of the corpus (all REM 1003); `qes` 7 and 7
  (all REM 1003); `seb` 9 and 16 (all REM 1003). Of the stela's 381 word types (numerals left out), 274 never occur
  outside it, so most parallels are internal or in REM 1003.

### 5.4 Verbs

- **Prefixes.** `e-` before `ked` "kill" and `er` "take" (l. 5, 131-132, 143-151) [R]; `i-` in `i-de-bx` [R] and
  `i-pl-te` [P: F&vGO]; `w-` in `w-kb-bx-te`, `w-er-k` [R], and perhaps `wkete`, `wdto`.
- **Suffixes.** `-to` (`e-kede-to`, `tk-to`, `e-ked-b-to`) and `-td` (`e-ked-td`, `er-td`) [R: tense or aspect];
  `-k` "repeatedly" in `e-r-k` [R]; `-bx` plural object in `i-de-bx`, `w-kb-bx-te` [R; G `-bḫ(e)`]; `-kete`
  [G plural optative] in `ed kete` (twice), `wkete` (twice), `mo kete`, `nd kete`.
- **The `i-…-to` shape** (`iXlXto` ×4, `ipxto` ×4, `itwdto` ×2, `irxto`, `ipleto`, `ilolto`, `ixXtto`, `inweto`,
  `ittmito`) occurs 16 times in this stela and in no other text of the corpus (regex `i[a-zA-Z]+to`: 0 hits outside
  it) [H4].

## 6. Hypotheses

Labels follow the brief: ESTABLISHED (the gold files or an accepted reading), PUBLISHED HYPOTHESIS (who, where) or
NEW (what was searched). "Searched" lists the queries and full texts read; it does not prove that nothing exists
in print. Hintze 1960, Hofmann 1981, Rilly 2007, Rilly & de Voogt 2012 and Hallof's dictionary beyond its sample
could not be read.

### H0. The war formula: `abr-se-l e-ked kdi-se-l e-r-k` "I killed each man, I took each woman" (l. 4-5, 130-132)

- **Label: ESTABLISHED** for the words (`abr` "man", `kdi` "woman", `ked` "kill", `are-/erk-` "take": gold, Rilly
  2016 p. 9); **PUBLISHED HYPOTHESIS** for the grammar (1SG `e-`, EACH `-se`, PLC `-k`: Rilly 2020, ex. 35 and
  Table 2).
- **Corpus:** the same formula with `ye-` opens each campaign in REM 1003 (`abrse l yekedi kdise l arse li tkk`).
- **Confidence:** 5 for the words, 4 for "I".

### H1. `Mk lte wi 12`: "in all, 12 gods" (l. 12)

- **Label: PUBLISHED HYPOTHESIS.** Macadam, in Abdalla 1969, vol. I part 2, pp. 215-216 (checked on the page
  scan): if `wi` means total, the phrase reads "total (is) 12 gods", and Abdalla counts the deities from l. 7.
  Hofmann 1981, 326 (via FHN II p. 722) showed that REM 1003's `wi 3348` is a sum.
- **Evidence:** exactly twelve 1s precede it (12 items, one lost in a lacuna); `mk` is "god" [G]; `mk lte` also
  heads the list in l. 6. The count of twelve works if the first item is `Amnp qoro mrtxe edxN 1`, parallel to the
  sixth, `Amnp qoro axboroteN 1`; it does not work if `edxN` is only a heading (FHN II), since that leaves its `1`
  unexplained.
- **Alternatives:** `wi` is a copula "are": "the gods are 12" (Hallof 2022, entry *awreste*, for REM 1138); `wi` the
  emphatic [G `-wi`]; Millet 1968 (p. 263) glosses a `wi` in a Philae list as "one".
- **Confidence:** 5 that 12 sums the list; 3 that `wi` itself means "total".
- **Test:** every `wi` + numeral elsewhere (REM 1138, REM 1041 `abr wi 1032`) should sum a complete list; a `wi N`
  over a list that does not add up refutes "total" and leaves "are".
- **Tested on unseen texts, 2026-11-09:** weaker. REM 1003's `wi` number is not the sum of its counts in any
  edition, and the new cases favour "are" (`verification.md`, claim 3, "Out-of-sample test").

### H2. The god list includes the Theban triad: `Mno`/`Mne` Amun, `Mt` Mut, `Aqedise` Khonsu (l. 8-11)

- **Label: PUBLISHED HYPOTHESIS.** `Mt` = Mut: Abdalla 1969, p. 216. `Aqedise` = Khonsu: FHN II p. 670. That the three
  form the Theban triad was not found stated, but it follows directly.
- **Evidence:** the lunette shows Amun with Mut (FHN II p. 668); the list has two `Amnp qoro ...` entries (the first
  and the sixth), and FHN takes the sixth as Amun of Luxor (Thebes), the triad's home.
- **Alternatives:** `Mt` is an abbreviation of another name; or `Mt 1 tepede` belongs together.
- **Confidence:** 3.
- **Test:** a Meroitic caption naming Mut (`Mt`) beside her image would settle it.

### H3. `pteno 3` is a total placed before its items: `pteno 3: apette 1, sber 1, dd 1` (l. 18-19, 21)

- **Label: NEW.** Searched: "pteno" Meroitic; "apette" Meroitic; the full texts of FHN II, Abdalla 1969, Rilly 2020,
  the Hallof samples and Millet's glosses. `hamadab.md` H1 noted the arithmetic; no publication was found.
- **Evidence:** 3 = 1 + 1 + 1 both times; in the second list the 3 and the three 1s are read and only `pteno` is
  restored (FHN prints `(pteno)`). The two lists are parallel word for word, for two recipients.
- **Alternatives:** `pteno 3` is a fourth item, and the match is chance; `apette` is `apete` "envoy" [G `apote`]
  and the list counts persons, not goods.
- **Confidence:** 3.
- **Test:** another list where a word + numeral is followed by items whose numbers add up to it. A `pteno N` whose
  items do not sum to N refutes it.
- **Tested on unseen texts, 2026-11-09:** no new case, and sums of small numbers turn up by chance about as often
  (`verification.md`, claim 3, "Out-of-sample test", point 4).

### H4. Every `i-…-to` verb has the 1st-person prefix: `i-` = `e-` "I", `-to` tense or aspect

- **Label: NEW** (an extension). Published pieces: `i-de-bx` "I gave(?)" (Rilly 2020, ex. 8); `i-pl-te` "I grant(?)"
  (F&vGO 2020, p. 294); `-to` "tense or aspect" (Rilly 2020); `y(e)-` and `i-` interchangeable, with no person value
  (Abdalla 1969, vol. I part 2, pp. 109-110). Rilly says the prefix is written `e-` throughout REM 1044, so he did
  not extend it to these verbs. Searched: "qes ihlhto" OR "ihlhto" OR "ixlxto"; "ipleto" OR "iplte" OR "yplt";
  the Abdalla and Hallof full texts. Hallof 2020 (p. 15 n. 27) reads `-to` in `ipleto` as a 3rd-plural pronoun
  instead.
- **Evidence:** 16 `i-…-to` tokens; the shape is absent from the rest of the corpus, as the 1st-person narrative is;
  `i-` alternates with `e-` on the same verb (`i-de-bx`, `e-de-bx`, `de-bx`), as `e-`/`ye-` alternate in REM 1003.
- **Alternatives:** `i-` is a different prefix (Abdalla: no person value); `-to` is a 3rd-plural object (Hallof).
- **Confidence:** 2.
- **Test:** an `i-…-to` verb with a nominal subject directly before it, or in a clause with the 3rd-person `w-`,
  refutes it.

### H5. `(qes) (itnk) iXlXto` "Kush + verb" opens a campaign episode (l. 4, 38, 42-43, 129)

- **Label: NEW.** Searched as for H4; Hallof 2020 (p. 16 n. 35) only cites `itnk[i]hlhto` (l. 42-43).
- **Evidence:** `iXlXto` occurs 4 times and nowhere else in the corpus: `qes iXlXto` (l. 4, 129), `qes itnk
  iXlXto` (l. 42-43) and `itnkk iXlXto` without `qes` (l. 38). At l. 4 and l. 129 it stands next to `tqN-l` and
  the kill/take formula follows; at l. 38 and l. 43 the same paragraph follows (`seb-l ed kete kek ... wkete`),
  after the crown prince's title.
- **Alternatives:** `qes` is not "Kush" here; the phrase closes the preceding episode.
- **Confidence:** 4 for the structure; 1 for any meaning ("I went to / fought in Kush" is a guess).
- **Test:** a third royal text (REM 1003, 1333) with `qes` + verb before its kill/take formula.

### H6. `qoleb (Amnp/Amnpte) (i/e)-de-bx(i)` "I gave(?) them (to Amun)" closes four lists or episodes

- **Label: NEW** (an extension of Rilly's reading of one instance). Published pieces: l. 25-26, "I gave(?) them to
  Amanap" (Rilly 2020, ex. 8); `i-de-b-x`, `i-de-b-xi`, `e-de-b-x`, `de-b-x` are one verb (Abdalla 1969, vol. I
  part 1, p. 43).
  Searched: the full texts of Rilly 2020, Abdalla 1969, FHN II and F&vGO 2020; no one connects the four.
- **Evidence:**
  1. l. 26-27: two named officials, then `qoleb Amnp i-de-bx`.
  2. l. 115-116: an allocation list with `ipxto` after each item, then `qoleb de-bx`.
  3. l. 125-126: `asr deb 5000 Npte ...`, then `qoleb Amnpte i-de-bx-i`, so the 5000 animals at Napata would go to
     Amun of Napata.
  4. l. 136-137: after the second kill/take formula and `Amnp`, `Amni`, `qoleb e-de-bx`, so the captives would go
     to Amun.
  5. The genre has it: Nastasen's stela, an earlier royal stela from the same Amun temple at Gebel Barkal (Rilly
     2020, §4.1), twice says the king gave a captured chief, once with his property, to Amun of Napata (FHN II
     no. 84, pp. 489-490). There a pronoun object is spelled out by the noun, much as `qoleb` resumes the two named
     officials in Rilly's reading of l. 25-26.
- **Alternatives:** `de` is not "give" (Rilly marks it "?"); `qoleb` is "living persons" (Griffith 1917, 167;
  Hintze 1960, 148), which still fits 1 and 4 but not 3.
- **Confidence:** 3.
- **Test:** in other royal texts, `qoleb` + verb with `-bx` should follow a list of people or goods; a clause that
  ends a list with a god's name before the verb would support "give to".

### H7. `wse` is the 3rd-person possessive "his/her" also in REM 1044 (`adb wse-li` "his land", l. 44) and REM 1003 (`xrpxe wse-l` "his governor")

- **Label: NEW** (an extension). Published for REM 0094 only: Millet 2003 (via F&vGO, p. 297), Rilly 2020 §4.5
  (`semle w-si` "his wife", `ste wese` "his mother"). F&vGO n. 26 adds that `wse` could be a noun. Searched: Meroitic
  "wse" possessive Kharamadoye Millet "qese" "hrphe"; the REM 1003 and 1044 literature above.
- **Evidence:** `wse` is written as a word 10 times in `corpus_v2`: here once, in REM 1003 twice and in
  Kharamadoye 7 times. Every time it directly follows a noun or title: `adb` "land" [G], `xrpxe` (twice), `ado`,
  `mte` "child" (twice), `mtr` (four times). This matches Millet's and Rilly's possessive in Kharamadoye.
- **Alternatives:** a noun or title (F&vGO); a plural or locative ending.
- **Confidence:** 2.
- **Test:** `wse` after `wide` "brother" or `ste` "mother" in REM 1003 or 1044 would support it; `wse` heading a
  noun phrase would refute it.

### H8. `ameloloke` (l. 24, 108-109) is the priestly title `beloloke` with `a-` and m for b

- **Label: NEW.** Searched: "ameloloke" OR "beloloke" Meroitic title; "beloloke" high priest OR "grand-prêtre";
  FHN II, Abdalla and Millet in full. FHN II calls `ameloloke` only "title of official".
- **Evidence:** [G `beloloke` "priest (a rank)", Griffith 1911 p. 55; variants `belileke`, `beleleke`]; the m/b
  alternation is accepted in [G `bedewe`/`medewi`]; both REM 1044 instances are in lists of temple personnel next
  to `ssime`, `wtotrse`, `ameri` and `ssor`.
- **Alternatives:** an unrelated title; `a-` + `meloloke` with another root.
- **Confidence:** 2.
- **Test:** a spelling `abeloloke` or `meloloke` in another text, or `ameloloke` in a priestly title chain.

### H9. `Amnp Nte-se-l` is a fixed epithet of Amun shared with REM 1003 (l. 54-55, 99-100, 132-133)

- **Label: PUBLISHED HYPOTHESIS.** Abdalla 1969, vol. I part 2, p. 67 lists the REM 1044 instances beside REM 1003
  `amnp nte-s-li` (Ak I 38, Ak II 17). The meaning of `Nte` is unknown.
- **Corpus:** `nete` occurs once outside the stela, in REM 1003 (`amnp nete se li amnp pide lke`).
- **Confidence:** 4 for the parallel; 1 for any meaning.

### H10. `sem lo l` after titles is `-se mlo-l` "the good ...", not `sem` "wife" (l. 29, 133, 138, 151)

- **Label: PUBLISHED HYPOTHESIS.** Rilly 2020, ex. 54: `xrpxe-se-mlo-l` "the good ... governor". Abdalla 1969, p. 67
  takes `-s-mle-l` as an epithet.
- **Evidence:** `mlo` "good" [G]; `sem` "wife" [G] fits none of the four contexts.
- **Confidence:** 3.

### H11. The verso is framed: l. 36 returns at l. 158-161, and `Xol(k)` may be the verb "serve (a meal)"

- **Label: NEW.** FHN II (p. 671) relates l. 158 ff. to benediction formulae A and B (after Hintze 1960, 160), but
  the repetition of l. 36 was not found stated. Rilly 2020 (ex. 41 and formula C in §5.1) has `hol` "serve, present"
  in the funerary benedictions (`x(re) mlo-l-w hol-kete`). Searched: "sedew" Meroitic; the full texts of FHN II,
  Abdalla and Rilly 2020.
- **Evidence:** l. 36-37 `sedew tbe tXe lw qes molk seb eqetxe`; l. 158-161 `ato sedew ato mlo qes Xolk seb
  eqetx[...]`. The run `sedew ... qes molk/Xolk seb eqetx(e)` recurs: four words are identical and in the same
  order, and `molk`/`Xolk` differ by one sign. `sedew` occurs nowhere else in the corpus, and `eqetxe` only as
  `eqetxN` in REM 1003. `Xol` also
  stands in `ssmrte-l Xolk` (l. 41) and `p Xol 8` (l. 114).
- **Alternatives:** chance repetition of common words; `molk` and `Xolk` are different words.
- **Confidence:** 3 for the frame; 1 for "serve".
- **Test:** the FHN II plate or Hintze's facsimile at l. 36: `m` or `X`?

### H12. `aleqese` (l. 1)

- **Label: PUBLISHED HYPOTHESIS** (three competing): "monument, inscription" (Hintze 1960, 142, via FHN II p. 669);
  an adverb, cognate of Old Nubian ⲁⲗⲉⲥⲛ̄ "if" (F&vGO 2020, pp. 295, 299, who reject Hintze); "(written)
  announcement" (Hallof 2020, p. 13).
- **Confidence:** none is settled; 2 each.

### H13. `Amnp` and `Amnpte` are two different gods in this text

- **Label: PUBLISHED HYPOTHESIS.** FHN II p. 670: `Amnp` = Amun of Luxor, `Amnpte` = Amun of Napata. Against it,
  Rilly 2020 (ex. 8) reads `Amnp` as Amanap, "Amun of Napata", and the gold file lists `amnp` as a variant of
  `amnpte`. Baldi 2016 discusses the question for REM 1003.
- **Evidence:** both stand as separate items, each counted "1", in the god list of l. 8-9; the lunette shows Amun of
  Thebes and Amun of Napata together.
- **Confidence:** 3 for "two gods here"; which is which stays open.

### H14. `pqr qorise-l` (l. 38) and `pkr tr qorise` (l. 41-42) are the crown prince's title

- **Label: ESTABLISHED.** [G `pqr` "prince, crown prince", certain, Rilly 2016 pp. 8-9]; FHN II p. 670, after Török
  1977a, calls it the highest official title on record, held by crown princes in REM 0005, 0017 and 0020. The same
  phrase is in REM 1003 (`pqr qorise l`).
- **Confidence:** 5.

## 7. What the stela says, in plain English

The reading below keeps every uncertain part in brackets or marks it with "(?)".

King Tanyidamani begins with his title and a word, `aleqese`, whose meaning is disputed (Hintze: "monument,
inscription"; others: "if" or "announcement"), followed by epithets and a mention of Amun of Napata and Kush. He then
reports a campaign: something (`iXlXto`) concerning Kush, and "I killed each man, I took each woman". Next comes a
list of offerings or obligations for twelve gods, among them Amun in several forms (of Napata, of Luxor (?), of Arre
(?), of Pnubs (?)), Khonsu, Isis and probably Mut, one unit each, with the total "12 (gods)". Further lists count
unknown items (120, 10, 3, 8, 9) for the king's descendants (?) and the king's children (?). Two officials,
Atanene and Imalutarura, are handed over to Amun (Rilly: "I gave(?) them to Amanap"), and later 5000 animals at
Napata and the captives of a second campaign seem to go to Amun the same way (our hypothesis H6). The verso tells of
the crown prince and other officials in two parallel, untranslatable paragraphs, names Isis and Horus of Sai and
the city of Meroe, and repeats "the palace (?)" several times. Near the end the king says he killed a man named
Akhutune of "the palace (?)", his brother Nakharura and others, seized "the good governor", and that the children
of the palace (?) and their brothers Aruqitama and Tadakhesene (?) were captured, apparently by someone other than
the king, since that verb carries `w-` instead of `e-` (Rilly). The text closes with words
from the funerary blessings, "water" and "good bread", in a line that repeats the first line of the verso; who
receives them, and why, is unknown.

## 8. Counts per label (section 6)

| Label | Count | Items |
|---|---|---|
| ESTABLISHED | 2 | H0 (the words of the war formula), H14 |
| PUBLISHED HYPOTHESIS | 6 | H1, H2, H9, H10, H12, H13 (and H0's grammar, counted under ESTABLISHED above) |
| NEW | 7 | H3, H4, H5, H6, H7, H8, H11 |

In the interlinear gloss (section 4), counted by script over its 174 rows: 66 rows cite a [G] meaning for at least
one word, 69 a published reading ([P] or [R]), 34 point to a hypothesis of section 6, and 59 have neither a gold nor
a published meaning for any word (they are "?" or a marked guess). A row with a [G] word can still be mostly "?".

## 9. Sources and searches

Read in full text this session (page numbers are the printed ones):

1. FHN II = Eide, Hägg, Pierce and Török, *Fontes Historiae Nubiorum* II (1996), nos 150-153, pp. 662-671, from the
   text layer of the [UiB PDF](https://data.ub.uib.no/files/manlib/ubb/ubb-msref/ubb-msref-0939/ubb-msref-0939-078/ubb-msref-0939-078-fon/ubb-msref-0939-078-fon-02/pdf/ubb-msref-0939-078-fon-02_orig.pdf).
   Numbers were not checked against the page images.
2. C. Rilly, [*Personal Markers and Verbal Number in Meroitic*](https://pages.sandpoints.org/dotawo/article/rilly),
   *Dotawo* 7 (2020): ex. 8, 35, 42, 43, 49, 50, 54; Table 2; §4.5.
3. V. Ferrandino and V. W. J. van Gerven Oei 2020,
   [*Potential Old Nubian cognates for Meroitic aleqese*](https://unora.unior.it//retrieve/handle/11574/198508/87076/S&N_24_FerrandinoandvanGervenOei.pdf),
   *Sudan & Nubia* 24: 292-301, pp. 294-299.
4. A. G. M. Abdalla 1969, [*Meroitic Personal Names*](https://etheses.durham.ac.uk/id/eprint/988/), PhD thesis,
   Durham: vol. I part 1, p. 43; vol. I part 2 ([PDF](https://etheses.durham.ac.uk/id/eprint/988/2/988_v2.pdf)),
   pp. 9, 37, 67, 109-110, 169-171, 215-219, 240, 250, 256, 268-269. Read from OCR, with printed page numbers taken
   from the page headers; the p. 216 passage was checked on the page scan.
5. J. Hallof 2020, *The Meroitic Inscriptions from Qasr Ibrim* III, publisher's
   [sample](https://roell-verlag.de/WebRoot/Store28/Shops/bffcc1fb-060d-4066-bf9c-ddec607b2cb7/MediaGallery/Neuer_Ordner/1576-SRaT-9-5-Leseprobe.pdf),
   pp. 12-17; J. Hallof 2022, *Analytisches Wörterbuch des Meroitischen* I,
   [sample](https://www.lehmanns.ch/media/103617094), entry *awreste*.
6. FHN II no. 84 (Nastasen), pp. 489-490, for the gifts of captives to Amun of Napata (H6).
7. Local: `data/otten/Data/MilletExamples.txt` (l. 240, `mdes`) and `Kalabsha_Millet.txt` (Millet 1968),
   `data/discovery/hamadab.md`, `data/discovery/verification.md`, the gold files.

Items 3 to 5 were found and read by a helper agent this session; the passages cited from items 1, 2, 3 and 4 were
re-read here.

Searched and not found (queries as run): "qes ihlhto" OR "ihlhto" OR "ixlxto"; "ipleto" OR "iplte" OR "yplt";
"ameloloke" OR "beloloke" Meroitic title; "apette" Meroitic; "pteno" Meroitic; "beloloke" high priest OR
"grand-prêtre"; Meroitic "wse" possessive Kharamadoye Millet "qese" "hrphe"; "sedew" in the full texts above.

Not reached: Hintze 1960 (*Kush* 8 is not online; UiB has vols 4-6 only), Hofmann 1981, Priese 1977 and 1984,
Török 1984, Rilly 2007, Rilly & de Voogt 2012 beyond pp. 1-10, Hallof's dictionary beyond its sample, Baldi 2016
(bot check), the MFA object page for 23.736 (HTTP 403). Griffith 1917 (JEA 4) is online
([archive.org](https://archive.org/details/in.ernet.dli.2015.70976)) but treats REM 1003 only.
