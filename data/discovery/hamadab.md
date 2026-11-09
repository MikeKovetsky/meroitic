# REM 1003, the Hamadab stela of Amanirenas and Akinidad (British Museum EA 1650)

Written 2026-11-08 from the inputs in this repo and web searches, in about 70 minutes. Every meaning below
carries a tag:

- **[G]** is an accepted meaning from `data/gold_lexicon.json` or `data/gold_morphology.json`, with the gold
  entry's source.
- **[P: who]** is a published proposal that is not in the gold files, with the source.
- **[H1]** to **[H5]** are hypotheses made here (section 6). None of them is accepted.
- **?** means nothing can be said.

## 1. Answer first

1. **The stela does not line up with the Roman account.** Nothing in REM 1003 names Syene, Elephantine,
   Philae, Pselchis or Primis, and no numbers match. Statues and a treaty are not identifiable. The best
   matches are the two rulers, who are also in Strabo, and possibly Napata in l. 8 ([H3]). This agrees with
   Rilly 2014: REM 1003 tells of campaigns against tribes, and the Roman war is in its continuation, REM 1039.
2. **The grammar of the war formula is already published.** Rilly's
   [*Personal Markers and Verbal Number in Meroitic*](https://pages.sandpoints.org/dotawo/article/rilly)
   (*Dotawo* 7, dated 2020 by Glottolog and 2021 by library catalogues) analyses REM 1003's formula, and the
   gloss below follows it. It reads `abr-se-l ye-ked-i` as "I killed each man", `kdi-se-l ar-se-li tk-k` as
   "each woman (and) all the boys I seized one by one", and `qo-leb apote be-se tk-k` as "I seized them and
   their envoy". `(y)emoqe` is "belongings (?)" and `(e)qebese` is "their". None of this is new here.
3. **Five hypotheses are offered (section 6).** The two strongest:
   - [H1]: `wi` directly before a numeral marks a total. In the Tanyidamani stela, `mk lte wi 12` follows
     exactly twelve items each counted "1".
   - [H2]: the closing numbers 1626 and 1032 count animals (`asr`), not people. Every `asr` written as one
     word in the corpus stands within two words of a numeral.

   Neither was found in the literature searched. Hofmann 1981 and Griffith 1917 are in print only and were
   not checked.
4. **Four errors in the inputs change readings** (section 7):
   - The Otten file and the corpus read `ymope` in l. 4 and `yetkbxk` in l. 13. FHN II and Rilly read
     `yemoqe` and `yetkbḫi`.
   - `src/corpus.py` turns every doubtful-sign star into a word break, so `tkk` becomes `tk k` and `qor`
     becomes `q o r`. Many spaces in the corpus row are therefore not morpheme boundaries.
   - The gold lexicon lists `arme` as a "certain" spelling of Rome. Rilly withdrew that reading for this
     stela.
   - The numbers are not settled: Rilly reads the women in l. 10 as `1[.]2`, not 100, and FHN II's "wi 3348"
     (l. 25, as quoted in lead 02) is in neither local file.

## 2. The text and its witnesses

| Witness | What it is | Use here |
|---|---|---|
| FHN II no. 176, pp. 719-723, ll. 1-15 as quoted in `data/leads/02-war-with-rome.md` | Printed edition after REM; `,,` word dividers, `*` doubtful signs | Line numbers 1-15 and the readings that differ |
| `data/otten/Data/HamadabStelaOfAmanirenasNarrative.txt` | One continuous line with stars and brackets kept; no line numbers | The text for ll. 15-42 |
| `data/corpus.jsonl`, row `hamadab` | The Otten file normalized by `src/corpus.py` | Concordances |
| `data/corpus.jsonl`, rows `T0957`, `T0825`, `T0238`, `T0359`, `T0742` (all filed as `funerary`) | A second full copy of REM 1003 from the Otten mero-corpus (T0957), plus fragments of its titulary | Every concordance count for this stela's words is doubled |

Line numbers after l. 15 were not checked against the FHN II plate, because the PDF is 42 MB and too large to
fetch. They are given below only where a publication cites them: Rilly's (51) is ll. 23-24 and his (52) is
ll. 31-35; Baldi puts `Amnpte` in l. 37.

## 3. Segmentation

The text has a protocol, then the queen's part (P to B), then Akinidad's part (C). The brief's "three times
with numbers" is right, but the formula has a fourth, numberless run (S4). A long refrain ending in a total
closes both rulers' parts.

| Id | FHN lines | Content | Key words |
|---|---|---|---|
| P | 1-2 | Protocol: Amanirenas *qore*, *kdwe*; Akinidad *pqr*, *pesto* | `amnirense qore-li kdwe-li ... akinidd pqr-ñyi pesto-ñyi` |
| S1 | 2-6 | Titles and places, the razzia formula, an official, **abr 32 kdi 135**, a verb, then a damaged coda | `... qes armeyose-li ... abr-se-l ye-ked-i ... adḫite qeper abr 32 kdi 135 qo-leb yedḫi ...` |
| S2 | 7-10 | The same, opening with `qes npto`, then **abr 100 kdi 100 [...]**, and "their envoy" | `... ḫrpḫe-l qes npto aro bel abr-se-l ye-ked-i ... adḫite perite abr 100 kdi 100 qo-leb apote-be-se tk-k ...` |
| S3 | 11-13 | The same, then **abr 58 kdi 223**, and "their envoy" | `... adḫite prite abr 58 kdi 223 qo-leb apote qebese ye-tk-bḫ-i ...` |
| S4 | 13-15 | The formula a fourth time, with no numbers | `alle-leb aberse-l ye-ked kdi-se-l ar-se-li tk-k de qebese wi ... e-tk-bḫ-i ... aqebese wi erbḫi` |
| B | 15 to about 26 | The queen's narrative continues: Amun of Napata, perhaps Meroe, then the **refrain** | ... `seb krte-li artḫnke ... kdi-se-l-w abr-se-l-w yemoqe eqebese-wit w-kb-te ... asr aḫidebḫ wi 1626` |
| C | about 26-42 | Akinidad's part: his titles, Amun of Arre, the **refrain** again, "Amun of Napata", and the close | `akinidd qo pqr-l-o pesto-l-o ... asr aḫidebḫe wi 1032` |

The refrain starts at `seb krte-li` in B and in C and runs to the closing `asr aḫidebḫ(e) wi N`. In B it
is 82 corpus tokens long; there are fewer real words, because the corpus splits words at stars. Rilly's (51) and (52) are the same clause from the two copies, and he notes they differ only in
spelling. The full extent of the repetition was not found stated in the sources searched.

## 4. Interlinear gloss

Spelling follows the corpus: `x` = ḫ, `X` = ẖ, `N` = ñ, `S` = š. Words that the corpus splits at stars are
rejoined, as in `tkk` and `qor`. Doubtful signs are not marked here; they are in the Otten file and FHN.
Abbreviations:

- DET is the singular determiner `-l/-li` [G `-l`, Rilly 2016 pp. 7-8], and PL.DET is `-leb` [G, Rilly 2016
  p. 7].
- GEN is `-se` [G, Rilly 2016 p. 7], and EACH is `-se` on a noun [G `-se (each)`, debated, Rilly 2010 p. 138;
  used by Rilly in *Dotawo* 7].
- COP is `-o` [G, Rilly 2016 p. 8], and ACC is `-w` [G probable, Rilly 2016 p. 7; "det-acc" in Rilly,
  *Dotawo* 7].
- VN is the verbal number marker, `-ḫ` singular and `-bḫ` plural [G `-ḫ(e)/-bḫ(e)`, probable; Rilly,
  *Dotawo* 7, reads it as a verbal number marker].
- [R] marks the analyses in Rilly, *Dotawo* 7, which are published proposals, not gold:
  - 1SG is the prefix `(y)e-` "I".
  - PLC is the pluractional `-k`.
  - `qoleb` is the 3PL pronoun "they, them".
  - `(a/e)qebese` is the 3PL possessive "their".
  - `(y)emoqe` is "belongings (?)".
  - `ar-se-li` is "all the boys".

### P (l. 1-2)

| Meroitic | Gloss | Status |
|---|---|---|
| `amnirense` | Amanirenas (royal name) | Name, read with FHN II and lead 03 |
| `qore-li` | ruler-DET | [G `qore`, Rilly 2016 p. 9] |
| `kdwe-li` | ?-DET (a title) | ?; REM 0092 calls the same queen `kdke`, which is [G `ktke`] "Candace". The spelling `kdwe` differs, and the equation is not established. |
| `yitnidebxe-l` | ?-DET | ? Compare `tbi tnideb xe qore` in C. |
| `qore-ñyi`, `pqr-ñyi`, `pesto-ñyi` | ruler-?, prince-?, viceroy-? | [G `qore`, `pqr` Rilly 2016 pp. 8-9, `peseto` Kuckertz 2021 pp. 18, 20]. The suffix `-ñyi` is ?; it also ends the titles in Kharamadoye's protocol (`qrNyi`, `sobNyi`, `xrpxNyi`). |
| `akinidd` | Akinidad (name) | Name |

### S1 (l. 2-6)

| Meroitic | Gloss | Status |
|---|---|---|
| `pqr qori-se-l` | prince ruler-GEN-DET: "prince of the ruler" | [G `pqr`, `qore`, `-se`]. The same phrase opens a clause in Tanyidamani (`pqr qorise l`). |
| `qor xrpxe-l-w` | ruler ḫrpḫe-DET-ACC | [G `ḫrpḫe` "governor (?)", **debated**, Millet 1968]; `-l-w` [R] |
| `qes armeyose-li` | Kush ?-DET | [G `qes`, probable]. `armeyose` was read as "Rome" (Griffith 1917, FHN II p. 721); **withdrawn by Rilly 2014**, so it is ? |
| `qor xrpxe-l axro-se-l atbe tmot` | ruler ḫrpḫe-DET ?-GEN/EACH-DET two(?) ? | `axro` is ?. For `atbe` "two", see [P: Millet], local `MilletExamples.txt` ll. 11, 456, and [G `tbo/tbe` "two", probable]. For `tmot` "truly" in Kharamadoye, see [P: Millet], local `Kalabsha_Millet.txt` l. 44. Millet files the whole phrase as titulary (`MilletExamples.txt` ll. 535-536). |
| `xrpxe armi-l qes to` | ḫrpḫe ?-DET Kush ? | `armi` is ? (ex-"Rome", withdrawn). `to` is ?. |
| `abr-se-l ye-ked-i` | man-EACH-DET 1SG-kill-?: "I killed each man" | [G `abr`, `ked` "kill" Rilly 2016 p. 9]; `ye-`, `-i` [R] |
| `kdi-se-l ar-se-li tk-k` | woman-EACH-DET boy-EACH-DET seize-PLC: "each woman (and) all the boys I seized one by one" | [G `kdi`; `ar` "boy" probable; `tkk` "plunder" probable, Rilly 2010]; segmentation and translation [R, n. 96]. **Not** [G `kdite/kdise` "sister"]: here `kdi-se` stands parallel to `abr-se`. |
| `yemoqe qebese wi ye-erk-i` | belongings(?) their ? 1SG-take-? | `yemoqe` and `qebese` [R]. `erk` is [G `are-`/`erk-` "take, seize", probable]. `wi` is ? (Rilly has `-wit` as "3pl.gen-det(?)" in (51)). Otten and the corpus read `ymope`; see section 6. |
| `armesye lxe` | ? ? | ? `lxe` is spelled with ḫ and is not [G `lẖ` "great"] (spelled with ẖ); see section 6. |
| `adxite qeper` | ? ?(an official) | ?; [H4] |
| `abr 32 kdi 135` | man 32 woman 135 | [G `abr`, `kdi`] |
| `qo-leb ye-dx-i` | them ? | `qoleb` [R] (FHN II: "living persons", Griffith 1917, now superseded); `yedxi` is a verb, possibly 1SG [R pattern], meaning ? |
| `arbxteke pqr-li yedo qes-li imloke` | ? prince-DET ? Kush-DET ? | [G `pqr`, `qes`]; the rest is ? |
| `trodeb abepb msedeleñ ñro edeteq mroñl lroñ lbkte eqelbxe yedk aro bel skte qesto` | ? ... ? Kushite | Damaged (stars throughout). `qesto` "Kushite" [P: Rilly, local `RillyExamples.txt`]; all else is ? |

### S2 (l. 7-10)

| Meroitic | Gloss | Status |
|---|---|---|
| `qor xrpxe-l axro-qese-l atbe tmot` | as in S1 | As above. `axro-qese` stands where S1 has `axro-se`. |
| `xrpxe-l qes npto` | ḫrpḫe-DET Kush Napata(?) | FHN `npto`; Otten and the corpus `npt`. "Napata" is [H3] only. |
| `aro bel` | ? ? | ? (it occurs three times, in S1, S2 and S2) |
| `abr-se-l ye-ked-i kdi-se-l ar-se-li tk-t` | as in S1 | FHN `*tk*t`, with doubtful signs, where the other runs have `tk-k` |
| `emoqe qebese wi erk` | belongings(?) their ? take | [R]; `erk` without `ye-`, as in Tanyidamani's `kdise l erk` |
| `skte aro bel` | ? ? ? | ? |
| `adxite perite` | ? agent | [G `perite` "agent (administrator)", Griffith 1911 p. 22]; `adxite` is ? ([H4]) |
| `abr 100 kdi 100 [...]` | man 100 woman 100(?) | FHN `kdi 100 [...]`; Rilly reads `kdi 1[.]2` (his ex. 36) |
| `qo-leb apote be-se tk-k` | them envoy their seize-PLC: "(I) seized them and their envoy" | [G `apote`, Rilly 2016 pp. 8-9]. The rest is [R, ex. 36 and n. 70: "their" refers to the captives, and *apote* does not mean "tribal chief"]. |
| `mkiñ y qor mki weste-l` | ? ? ruler(?) ? ?-DET | Damaged. ? |

### S3 (l. 11-13)

| Meroitic | Gloss | Status |
|---|---|---|
| `abr-se-l ye-ked kdi-se-l arese-li tk-k` | "I killed each man; each woman (and) all the boys I seized" | As in S1. `ye-ked` lacks `-i`, which Rilly calls optional. |
| `emoqe qebese wi ye-erk-i` | as in S1 | [R] |
| `apese bmki wete lxe` | ? ? ? ? | ? |
| `adxite prite` | ? agent | [G `perite`, variant `prite`] |
| `abr 58 kdi 223` | man 58 woman 223 | FHN has the star on 58. |
| `qo-leb apote qebese ye-tk-bx-i` | them envoy their 1SG-seize-VN.PL-?: "I seized them and their envoy" | [R ex. 37]. FHN reads `yetkbḫi`; Otten and the corpus have `yetkbxk`, which is wrong. |
| `yqol meX aleqe qesto` | ? ? ? Kushite | `qesto` [P: Rilly]; `meX` is not [G `mẖe` "abundant"] as spelled (the sign order differs), so ? |

### S4 (l. 13-15)

| Meroitic | Gloss | Status |
|---|---|---|
| `alle-leb aberse-l ye-ked` | ?-PL.DET man-EACH-DET 1SG-kill | `aberse` is a spelling of `abr-se`; `alle` is ? |
| `kdi-se-l ar-se-li tk-k` | as in S1 | [R] |
| `de qebese wi awete e-tk-bx-i` | house(?) their ? ? 1SG-seize-VN.PL-? | FHN `deqeb ese`. Rilly (n. 95, read through a fetch tool, footnote text not seen) takes a word in l. 14 as `d` "house", comparing Andaandi *daa* "residence" and Nara *dà* "village". `awete` is ? |
| `arkedni aqebese wi erbxi` | ? their ? seize-VN.PL-? | `aqebese` [R, Table 6]; segmenting `er-bḫ-i` as [G `are-/er-`] plus VN is our own segmentation, not a meaning claim. `arkedni` is ? |

### B (l. 15 to about 26; line numbers not checked)

| Meroitic | Gloss | Status |
|---|---|---|
| `alleb so pertese qes` | ? ? ? Kush | ? |
| `qo-leb wi xrpxN mle kse lke aleqese wide-l-o eqetedlbxi seb` | them ? ḫrpḫñ ? ? ? ? brother(?)-DET-COP ? ? | [G `ḫrpḫe` variant `xrpxN`]. [G `wide` "brother"] plus `-l-o` gives "is the brother", but that reading is a guess in this context. |
| `qo-leb witese yesebe ns ns-l qor ate eqepi mede wite-l ayosesbi tkk dd` | ... | ?. `tkk` here is [G "plunder", probable]. |
| `seb qo-leb witese yesebe qebese wite sb-l mded wite-li qor nl-l yedxbx` | ... their ... ruler ... | ?. `qebese` [R]. |
| `amn[.]ñ qor mlo lX amnp` | ? ruler good great Amun-of-Napata | [G `mlo` Rilly 2016 p. 9, `lẖ` Rilly 2016 p. 9, `amnpte/amnp` Rilly 2016 p. 8]. Amun of Napata against Amun of Luxor is debated (FHN II p. 722; Baldi 2016). |
| `pnkk axro xrpxte bwike s wido qo-leb yebe-l yesebe witese ns ns-l` | ? ... ? | ? |
| `amnp yiroX mdewi ns` | Amun-of-Napata ? Meroe(?) ? | [G `bedewe`/`medewi` "Meroe", certain in general]. **Here** the identification is doubted (Hofmann 1981, 309, via FHN II; Baldi 2016). |
| refrain (B): `seb krte-li artxnki teNke-l tewwibxe` · `seb meke adb-l-elxe enoqe` · `seb mdeybe-li sqteseN-li adb-lelx lbrete` · `qes-li Xolitke seb seb lxe eno wite w-lbrte xrpxe-ke s wido irxxi` · `seb wi eqese wi-l ekte` | ... land ... Kush ... ḫrpḫe ... | [G `adb` "land, territory", probable, Kuckertz 2021 p. 18; `qes`; `ḫrpḫe`]; all else is ? |
| `kdi-se-l-w abr-se-l-w yemoqe eqebese-wit w-kb-te` | woman-EACH-DET-ACC man-EACH-DET-ACC belongings(?) their-? ?-seize-?: "? seized each man, each woman (and) their belongings(?)" | [R ex. 51, ll. 23-24] |
| `teNke lxe etewwite mmo-li dmbe-li mdeweyi mpde[.]yi bik wwi-ke wi erote tinNke w-likidbte asente qer-li-se-l-w` | ... | ?. `mdeweyi` may contain Meroe ([G `medewi`]), which is a guess. |
| `asr axidebx wi 1626` | animal ? total(?) 1626 | [G `asr` "meat, animal", Rilly 2016 p. 9]; `wi` before a numeral [H1]; the count being animals is [H2] |

### C (about l. 26-42; line numbers not checked)

| Meroitic | Gloss | Status |
|---|---|---|
| `akinidd qo pqr-l-o pesto-l-o` | Akinidad he prince-DET-COP viceroy-DET-COP: "Akinidad, he is the prince, he is the viceroy" | Built from gold entries: [G `qo`, Rilly 2016 p. 8; `qo` as a 3sg pronoun is R], [G `-l`, `-o`, `pqr`, `peseto`] |
| `pqri-lke mno-n-li eqetxN` · `ant mno-te-se-lke mno-n-li eqetxN` · `pqri-li pesti-li` | prince-? ? ... priest ... prince-DET viceroy-DET | [G `ant` "priest", Rilly 2016 pp. 7-9]; `mno` is ? (a divine name? compare `mno 1` in REM 1044's list of gods) |
| `tbi tnideb xe qore bki npbix amre mxrloseN` | ? ... ruler ... | ? |
| `amni arrese-se prtedse xrpxe wse-l lk-l` | Amun of-Arre ? ḫrpḫe ? | [G `amni`, Rilly 2016 p. 4]. "Amun (living) in Arre" is [P: Baldi 2016, after Griffith's Arre = *arrAzA* on Nastasen's stela, as spelled in the search snippet]. |
| refrain (C): `seb krte-li artxnoke wi teNke-l tewwibxe` ... `kdi-se-l-w abr-se-l-w emoqe qebese wi-l w-kb-te` | as in B | [R ex. 52, ll. 31-35] |
| `pede kese-lke xrpxe-ke qo-leb wte dete mk wite pide-lke` | ? ... ḫrpḫe ... them ... god ... | [G `mk` "god", Rilly 2016 p. 7]; `pide-lke` occurs four times in C and is ? `pede` is **not** `Pedeme` (Qasr Ibrim): it lacks `-me`, and no-one has proposed it. |
| `qo-l xrpxe pbo-li tkk wte dete-leb k axi-l plke wte dete` | ... plunder ... | [G `tkk`]; the rest is ? |
| `amnpte pide-lke seb wrewxe-li [.]p[..]em mke no wi teNke-l lbr/tbr ke qorteb e-tk-bx-e` | Amun-of-Napata ... I seized them(?) | [G `amnpte`; Baldi puts it in l. 37]. `e-tk-bḫ-e` follows the [R] pattern. The corpus keeps the editor's note "EITHER LBR OR TBR" as a word; see section 6. |
| `xrpxe wse-l tkt amni arresese amnp nete-se-li amnp pide-lke qo-leb stedebte/wtedebte seb teNke lxe` | ... Amun of-Arre Amun-of-Napata ... | [G `amni`, `amnp`]; [P: Baldi] for Arre |
| `wwi-ke wi erote tinnki w-likidbte asente qer-li-se-l-w asr axidebxe wi 1032` | ... animal ? total(?) 1032 | as at the end of B: [G `asr`], [H1], [H2] |

## 5. Alignment with the Roman account

Roman texts: Strabo 17.1.54, Cassius Dio 54.5.4-6, Pliny 6.181-182 and *Res Gestae* 26, in full in lead 02.

| Roman event (source) | REM 1003 section | Match | Why |
|---|---|---|---|
| "Queen Candace", ruler of the Aethiopians (Strabo; Dio) | P: `amnirense qore-li kdwe-li` | **Moderate** | A ruling queen in the right decades (FHN II nos 175, 179). But REM 1003 writes `kdwe`, not `kdke`, and nothing in the text dates it. |
| "Her son" at Napata, who fled (Strabo) | P, C: `akinidd pqr pesto` | **Weak to moderate** | FHN II identifies him with Akinidad. REM 1003 states no filiation: there is no `tedḫe` or `terike`. |
| Syene, Elephantine and Philae taken (Strabo; Dio to Elephantine) | none | **None** | No `Sewane`, `Pilqe` or `Yeb/Abu` in REM 1003. Rilly 2014 finds `Sewane` in REM 1039. |
| Inhabitants enslaved (Strabo) | S1-S4: "I killed each man; each woman and all the boys I seized" | **Weak (generic)** | The same formula is in Tanyidamani (REM 1044, 2nd c. BC: `abrse l eked kdise l erk`) and at Dakka (REM 0092: `kede-to`, `are-de-to`). It is a genre formula. Rilly reads REM 1003 as campaigns against two tribes, and in REM 1039 the Romans (`Tmey`) are the ones who enslave. |
| Statues of Caesar pulled down, later offered back (Strabo) | none | **None** | No word for "statue" is identified. |
| Envoys: Petronius's at Pselchis, Candace's at Napata, the embassy to Samos (Strabo) | S2, S3: `qo-leb apote be-se tk-k` "I seized them and their envoy" | **Weak, and against a match** | Here the Meroitic ruler seizes the defeated party's envoy along with the captives (Rilly n. 70). No Roman episode has that. |
| Pselchis/Dakka battle and the generals captured (Strabo; Pliny) | none | **None** | Akinidad's Dakka graffito REM 0092 uses the same kill/seize formula, but REM 1003 names no Dakka. |
| Premnis/Primis (Qasr Ibrim, `Pedeme`) taken and garrisoned (Strabo; Pliny) | none | **None** | `pede` in C is not `Pedeme`. |
| Napata, Candace's residence, razed (Strabo; Dio; Pliny; RG 26) | S2 l. 8 `qes npto`; B, C `amnp`/`amnpte` "Amun of Napata" | **Weak** | `npto` as Napata is [H3] only. If it is Napata, it stands in a title phrase (`ḫrpḫe-l qes npto`), not in a sack. `amnp` is a god's name. |
| Captives: 1,000 sent to Caesar (Strabo) | C: `wi 1032` | **None (rejected)** | The direction is reversed: those were Kushites captured by Rome, while REM 1003 counts what the Meroitic ruler took. By [H2], 1032 counts animals. REM 1041 is also quoted (lead 02) with `abr wi 1032`; check that for a mix-up. |
| 3 cohorts; under 10,000 infantry and 800 cavalry against 30,000; 3 days; 400 men for 2 years; 870 miles (Strabo; Pliny) | numbers 32, 135, 100, 100 (or 1[.]2), 58, 223, 1626, 1032, and [3348?] | **None** | No number matches or sums to a Roman figure. The visible counts sum to 648 (190 men, 458 women). |
| Treaty at Samos; tribute remitted (Strabo) | none | **None** | Nothing identifiable |

Verdict: REM 1003 gives the rulers and a war formula but no checkable event of 25-21 BC. The Roman events would
be in REM 1039, which Rilly 2014 calls the second half of the same continuous text. His reading of it was not
found in print or online.

## 6. Hypotheses

Each hypothesis has its evidence, alternatives, confidence, a test, and a literature check. "Not found" means
the searches listed returned no prior proposal. It does not mean the idea is new in print: Hofmann 1981 and
Griffith 1917 (JEA 4, 159-173; the citation is confirmed in the
[Griffith Institute archive](https://archive.griffith.ox.ac.uk/index.php/griffith-5-32-27-35)) could not be
read.

### H1. `wi` directly before a numeral marks a total ("in all")

- **Evidence:**
  - In REM 1044 (corpus `tanyidamani`), twelve items are each followed by `1`, and then comes `mk lte wi 12`
    (`mk` is "god" [G]). There are twelve 1s: `edxN 1`, `mno 1`, `amnpte 1`, `aqedise 1`, `iwxne 1`,
    `axboroteN 1`, `amnb 1`, a bare `1`, `meke 1`, `pxtotN 1`, `mt 1` and `yose 1`. It is the only
    `wi` + numeral in REM 1044. Its other 22 numerals are bare (`aqqibese 120`, `asr deb 5000`, `mrm 8`,
    and so on), and none of them sums what precedes it. One bare total does exist: `pteno 3` heads three
    items of `1` (`apette 1 sber 1 dd 1`, twice). So a total can also be bare and come first. H1 claims
    only that `wi` + numeral marks a total, not that every total takes `wi`.
  - In REM 1003, `wi` + numeral occurs only at the two closing positions, `wi 1626` and `wi 1032`, plus
    `wi 3348` in l. 25 per FHN as quoted in lead 02. Hofmann 1981: 326 (via FHN II p. 722) found that a sum
    of the `abr`/`kdi` counts appears in l. 25.
- **Alternatives:**
  1. `wi` is the emphatic particle [G `-wi`, Rilly 2016 p. 8], and "total" comes only from the context.
  2. `wi` is a noun such as "number" or "count".
  3. "Brother" [G `wide`, variant `wi`] is excluded by context.
- **Confidence:** moderate for REM 1044 (one clean case); low for REM 1003. Its visible counts sum to 648
  ≠ 1626, and the lines that could hold the summed items are damaged and unglossed.
- **Test:**
  1. Every `wi` + numeral elsewhere in REM (temple inventories, ostraca, REM 1041, REM 1333) should be the
     sum of a complete preceding list. One `wi N` that is not a sum over a complete list refutes H1.
  2. Read the numerals of ll. 16-25 on the FHN II plate and check 1626 and 3348.
- **Literature:** searched
  - "Meroitic "wi" numeral total sum Hofmann Akinidad stela 3348";
  - "Meroitic numerals "wi" before numbers "total" Tanyidamani stela gods twelve Hintze OR Rilly OR Hofmann";
  - "méroïtique "wi" total nombres stèle Tanyidamani "12" dieux Rilly".

  None of them found a proposal. Rilly (*Dotawo* 7) treats `-wi` only as emphatic and says nothing about
  `wi` before numbers. **Status: not found; partly anticipated by Hofmann's l. 25 sum (not seen).**

### H2. The closing numbers 1626 and 1032 count animals: `asr …deb… N` is a livestock-count formula

- **Evidence:**
  - Both closings read `asr axidebx(e) wi N`, where `asr` is "meat, animal" [G, certain, Rilly 2016 p. 9;
    Rilly 2010 p. 118].
  - REM 1044 has `itrek asr deb 5000`: `asr`, then `deb`, then a numeral. `deb` also sits inside
    `axi-deb-x`.
  - In the whole corpus, the one-word `asr` occurs only in these three places, each time within two words of
    a numeral (1626, 1032, 5000). Caveat: REM 1044 also has `as r meke idNte` a few words after
    `asr deb 5000`, written with a space in the Otten file. If that is `asr`, it is not followed by a number.
  - The human counts in REM 1003 are small (32-223 per run) and are written with `abr`/`kdi`, not `asr`.
- **Alternatives:**
  1. `asr` is a homograph, or part of a phrase that goes with the preceding `qer-li-se-l-w`.
  2. The totals sum all booty, people included.
  3. `deb` is the independent pronoun that Rilly lists in his summary table (*Dotawo* 7, conclusion). That
     would change the parse of `axidebx` but not the reading of `asr`.
- **Confidence:** low to moderate.
- **Test:**
  1. In REM 1333 (Abratoye), REM 1041 and REM 0094, `asr` should come after the human counts and before
     large numbers.
  2. On the plate, `asr` must be a whole word in both closings.
  3. A closing `asr … N` in which N equals a sum of `abr`+`kdi` counts would refute H2.
- **Literature:** searched
  - "Meroitic Hamadab stela Akinidad "cattle" OR "livestock" "asr" numbers totals 1626 1032";
  - "Meroitic royal inscription booty cattle "asr" Rilly meat animal Tanyidamani 5000".

  Neither found a proposal. **Status: not found online; Griffith 1917 and Hofmann 1981 not checked.**

### H3. `npto` (l. 8, FHN) is the toponym Napata (`Npte`)

- **Evidence:**
  - FHN l. 8 reads `qes,, npto,, aro bel`, where `Npte` is Napata [G, Griffith 1911 p. 23].
  - REM 1039 names `Npte` (Rilly 2014), and REM 1044 has `npte` twice.
  - The slot is parallel to S1's `armi-l qes to`.
- **Alternatives:**
  1. `np-to` is a verb with the tense or aspect suffix `-to` that Rilly finds in REM 1044 and 0092
     (`e-kede-to`). This is a live alternative.
  2. The word is part of a title or name.
  3. The Otten and corpus reading `npt` (with no `-o`) is right.

  Note: the gold variant `npt` of `npte` has no Meroitic attestation in the corpus outside this passage, so
  citing it as support would be circular.
- **Confidence:** low.
- **Test:** if REM 1039's `Npte` (Rilly) stands in a phrase like `qes Npte`, or with `ḫrpḫe`, H3 gains. If
  `-to` turns up on unambiguous verbs right after place names in REM 1003, H3 loses.
- **Literature:** searched "Meroitic "npto" OR "npte" Napata Hamadab stela REM 1003 line 8". Nothing found.
  FHN II prints `npto` without comment (lead 02). **Status: not found online.** The resemblance is obvious
  enough that Griffith 1917 or Hofmann 1981 may discuss it, so check them before claiming priority.

### H4. `qeper` (S1) names an official, like `perite`/`prite` "agent" in the same slot of S2 and S3

- **Evidence:**
  - The fixed slot `adxite` + X + `abr N kdi M` has X = `qeper` in S1, `perite` in S2 and `prite` in S3.
    `perite` is [G "agent (administrator)", Griffith 1911 p. 22].
  - REM 1044 has `xrpxN wi t qeper ado-l`, with `qeper` next to the title `ḫrpḫñ`.
  - `qeper` occurs nowhere else in the corpus.
- **Alternatives:**
  1. `qe` (demonstrative) + `per` (an abbreviation of `perite`).
  2. A personal name.
  3. `adxite` is a verb (Rilly n. 100: `-te` is frequent on verbs in REM 1003), and X is its subject, of
     any meaning.
- **Confidence:** low.
- **Test:** the parallel sections of REM 1039, if Rilly's reading appears, should show the same slot with a
  title. A funerary text with `qeper` in a title slot (for example before `yetmde-lowi`) would confirm it.
  None is in this corpus.
- **Literature:** searched "Meroitic "qeper" OR "adḫite" OR "aḫite" OR "adhite" Hamadab Akinidad stela word".
  Nothing found. **Status: not found online.**

### H5. Women and boys are counted, not killed men: `abr N` counts adult men taken alive despite the "each man I killed" formula

- **Evidence:**
  - Women outnumber men in every legible count: 135 to 32, and 223 to 58 (100 to 100 in FHN; Rilly reads
    `1[.]2`).
  - The formula kills the men and seizes the women and boys.
  - Rilly's ex. 36 and 37 translate the counts as seized: "(I) seized 100 men … (and) their envoy". So the
    small `abr` counts are survivors taken, and "each man I killed" is formulaic.
- **Alternatives:** `abr N` is the number killed and `kdi M` the number seized. That would make each run read
  "killed 32, seized 135". The syntax (`abr N kdi M qo-leb … tk-k`, with the counts as objects of "seize")
  favours Rilly's reading, but word order alone cannot settle it.
- **Confidence:** low to moderate; this mainly sharpens Rilly's reading.
- **Test:** a text where the kill count and the seize count carry separate verbs. REM 1039's lines 3-4 (men,
  women, girls and boys enslaved, per Rilly 2014) would be one if the numbers survive.
- **Literature:** this follows from Rilly's translations of ex. 36 and 37. **Status: implicit in Rilly
  (*Dotawo* 7); not new.**

Already proposed, and used rather than claimed here: the `(y)e-` "I", `-se` "each", `tk-k`, `ar-se-li` "all
the boys", `qoleb` "them", `apote be-se` "their envoy", `(e)qebese` "their" and `(y)emoqe` "belongings (?)"
readings (Rilly, *Dotawo* 7); `atbe` "two" and `tmot` "truly" (Millet); `amni arrese` "Amun (living) in Arre"
(Baldi 2016, after Griffith); and `armeyose`/`armi` not Rome, `Tmey`, `Sewane`, `Pedeme` and `Npte` in
REM 1039 (Rilly 2014).

## 7. What is wrong or risky in the inputs

1. **The corpus breaks words at stars.** `src/corpus.py` `norm()` replaces `*` with a space. So `*tk*k`
   becomes `tk k`, `s*kte` becomes `s kte`, `*q*o*r` becomes `q o r`, `m*ki*N` becomes `m ki N`, and
   `axideb*x*e` becomes `axideb x e`. The brief's "separates morphemes with spaces" is often false for this
   row. `kwic.py tkk` finds 1 of the 6 `tkk` in the stela; the other five appear as `tk k`.
2. **Editorial notes became words.** `(EITXER-LBR-OR-TBR)` and `(EITXER-STEDEBTE-OR-WTEDEBTE)` are in the
   corpus row as `oitXor-lbr-or-tbr` and `oitXor-Stodobto-or-wtodobto`.
3. **Two readings disagree with FHN II and with Rilly.** In l. 4, Otten and the corpus have `ymope` where FHN
   has `yemoqe`. In l. 13, they have `yetkbxk` where FHN has `yetkbḫi` and Rilly ex. 37 has `ye-tk-bx-i`.
   Rilly notes that `-k` never combines with `-bx` in REM 1003.
4. **Smaller differences:** in l. 8, Otten has `npt` where FHN has `npto`. In l. 6, Otten has `abe*pd` where
   FHN has `abe*pb`. In l. 10, the women are `100` in Otten, `100 [...]` in FHN and `1[.]2` in Rilly.
5. **l. 25:** FHN's `abri *k,, wi 3348`, as quoted in lead 02, is in neither local file. The lead's sentence
   on ll. 25-26 also contradicts itself: it says line 26 ends with `wi 1626` and also that line 26 begins
   Akinidad's part. Check the plate.
6. **Duplicates:** the funerary pool contains REM 1003 (T0957 in full; T0825, T0238, T0359 and T0742 in
   part), Tanyidamani (T0396) and Kharamadoye (T0411, T0732). Concordance counts for royal-narrative words
   are doubled.
7. **The gold lexicon has traps for this stela:**
   - `arome` lists `arme` as a "certain" variant of Rome, which contradicts Rilly 2014 for REM 1003.
   - `kdite` lists `kdise` as "sister", but in REM 1003 `kdi-se` is "each woman".
   - `wide` lists `wi` as "brother", which does not fit `wi` before numerals.
   - `lẖ` "great" lists `lx`, but the corpus keeps `x` (ḫ) apart from `X` (ẖ). `lX` is "great", and `lxe`
     is another word.
   - `l-` "give" and the determiner `-l` share a spelling.
8. **The gold morphology lacks the 1SG prefix `(y)e-`,** which Rilly (*Dotawo* 7) needs to read this text.
9. **Lead 02 contradicts itself on `apote`:** it calls it "Accepted" in one table and "a hypothesis" in the
   other.
10. **REM 1041's `abr wi 1032`** (lead 02) repeats REM 1003's last number exactly. Verify it in FHN II no. 178.

## Sources

- C. Rilly, [*Personal Markers and Verbal Number in Meroitic*](https://pages.sandpoints.org/dotawo/article/rilly),
  *Dotawo* 7 ([volume](https://escholarship.org/uc/dotawo/7/0)). It was read through a fetch tool that
  summarizes, so the example numbers and glosses are as reported. Footnote 95 was not seen directly.
- C. Rilly 2014, "Fragments of the Meroitic report of the war between Rome and Meroe", abstract:
  [HAL API record](https://api.archives-ouvertes.fr/search/?q=halId_s:halshs-01482774&fl=title_s,abstract_s,citationFull_s).
- M. Baldi 2016, [*Amun in Meroitic Nubia: The Case of the Hamadab Stela*](https://journals.librarypublishing.arizona.edu/jaei/article/id/1245),
  JAEI 11(1): 1-4. It is behind a bot check, so it was seen only through search snippets.
- C. Rilly 2016, [*Meroitic* (UCLA Encyclopedia of Egyptology)](https://escholarship.org/uc/item/3128r3sw),
  the source of most [G] entries.
- FHN II ([PDF, 42 MB](https://data.ub.uib.no/files/manlib/ubb/ubb-msref/ubb-msref-0939/ubb-msref-0939-078/ubb-msref-0939-078-fon/ubb-msref-0939-078-fon-02/pdf/ubb-msref-0939-078-fon-02_orig.pdf)),
  through lead 02 only; it is too large to fetch.
- [British Museum EA 1650](https://www.britishmuseum.org/collection/object/Y_EA1650), which refused the
  fetch (HTTP 403), and [Wikipedia, Hamadab Stela](https://en.wikipedia.org/wiki/Hamadab_Stela), which has no
  readings.
- Local files: `MilletExamples.txt`, `Kalabsha_Millet.txt` and `RillyExamples.txt` in `data/otten/Data/`.
