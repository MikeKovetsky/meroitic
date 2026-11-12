# Philae and the Dodecaschoenus: the Meroitic texts set beside the Demotic and Greek ones

Run D3, 2026-11-08/09, about 60 minutes. Inputs: `data/leads/01-philae-dodecaschoenus.md`,
`data/leads/04-foreign-renderings.md`, `data/gold_lexicon.json`, `data/gold_morphology.json`, `data/corpus.jsonl`
(through `src/kwic.py`), Ashby 2016 read in full text (below), and web searches.

## Answer first

1. **Six text groups align.** The Meroitic texts of Bekemete, Manitawawi, Abratoye, Wayekiye A and the
   envoy-to-Rome stela REM 0129 have counterparts in Ph. 410, 416, 417, 421, Ph. 344, Dak. 33 and
   I. Philae II 180-181. The central donation list of the Meroitic Chamber (REM 0101) also aligns, but only by
   theme. As lead 1 says, nothing aligns sentence for sentence. What lines up is names, titles, kinship and
   the gods named.
2. **There are 14 hypotheses: 1 ESTABLISHED, 6 PUBLISHED HYPOTHESIS, 7 NEW.** None is presented as accepted
   unless a source accepts it.
3. **The strongest new finding is a pair of alignments that solve two puzzles in the existing readings.**
   REM 0098 says that Bekemete was "begotten by a general of the water". That settles a Demotic ambiguity in
   Ph. 417: "general of the water" is the father's title, not Bekemete's. REM 0097 calls Manitawawi, a man,
   Bekemete's `sete`, although the gold file glosses `ste` as "mother". That fits Rilly's published
   refinement to "tutor".
4. **The envoy titles form a fixed chain.** The stela REM 0129 (corpus T0046) gives the same three titles in
   the same order as Sasan's Ph. 416, line 1: `qoreñ`, then `kroro`, then "great envoy to Rome".
5. **Some readings differ between FHN III and the corpus, and both are flagged below.** FHN III reads
   `Bekemete ste` in REM 0098 where the corpus reads `bekemete mte`. In REM 0089, FHN III reads `penn*ani`
   where the corpus reads `penn 5 ni`. Hypotheses that rest on one reading say which reading they use.

## Sources added in this run

1. **Ashby 2016**, [*Calling Out to Isis*](https://knowledge.uchicago.edu/records/c229v-78575/files/Ashby_uchicago_0330D_13172.pdf).
   The PDF was fetched once and its text extracted with macOS PDFKit into the scratchpad, outside the repo.
   Pages cited below are the printed page numbers. Used: the glossary (pp. ix-x); the Wayekiye family's titles
   (p. 144 nn. 78-81); `qoreñ` (pp. 149-150 nn. 99-105); Tami (p. 148); `ḫbḫñ` in Demotic (p. 165 n. 148); the
   dating of the Meroitic Chamber (pp. 171-172 n. 161); Appendices B and C, the tables of Phase II
   inscriptions with Ashby's readings of REM 0097-0125 (pp. 279-283).
2. **Thesaurus Linguae Aegyptiae lemma pages**, found by search. The pages themselves sit behind a bot check,
   so only the search snippets were read:
   1. [ꜣkrre, dm520](https://thesaurus-linguae-aegyptiae.de/lemma/dm520): a Meroitic title, from Ph. 416
      line 1, citing Zibelius-Chen 2011 pp. 284f.; no meaning given.
   2. [qrnjꜣ, d6401](https://thesaurus-linguae-aegyptiae.de/lemma/d6401): Zibelius-Chen doubts a derivation
      from `qore` and points to `qorise`, which would make the title "qorene of the king".
   3. [ḫbh̭ne, dm6015](https://thesaurus-linguae-aegyptiae.de/lemma/dm6015): a title, from Ph. 403 line 1,
      citing Zibelius-Chen 2011 p. 292.
3. **[Wikipedia, "Wayekiye family"](https://en.wikipedia.org/wiki/Wayekiye_family)**, after Török 2009
   pp. 456-464. Its family tree differs from Ashby's (H2).
4. **Not reached.** FHN III's commentary on Ph. 417 and the Meroitic Chamber (pp. 1010-1031) was not reread;
   the PDF is 57 MB, and lead 1 already quotes it. Rilly 2007 pp. 144-148 (on REM 0097, cited by Ashby) and
   Rilly 2010 p. 63 were not read directly; Rilly 2010 p. 63 is known only through Ashby's quotation. The
   Cambridge excerpt of Rilly & de Voogt 2012 returned HTTP 503.

Corpus convention below: `o` = o, `x`/`X` = ḫ/ẖ, `S` = s (s-hat), `N` = ñ, as in `data/corpus.jsonl`. Hit
counts come from the de-augmented corpus, but many lines are still name-swap copies, so a count says that a
formula exists, not how often it was used.

## Step 1. The alignments

### A. Bekemete: REM 0098, 0106, 0107 beside Ph. 417 l. 3 and Ph. 416

| Meroitic (FHN III; corpus T0318, T0124, T0225) | Gloss from the gold files | Demotic counterpart |
|---|---|---|
| `qo kroro Bekemete` | "This (is) the *kroro* Bekemete" (`qo` "this", nomination) | Ph. 417 l. 3 `Bk-mty pꜣ ꜣkrre`, "Bekmeti the akrere" |
| `ste` (FHN) / `mte` (corpus) | FHN: "his `ste` [mother/tutor]"; corpus: "the child" | none |
| `pelmos atolise-l yerike-lo` | "he was begotten (`terike`/`yerike`) by a general (`pelmos`) of the water (`ato-li-se`)" | Ph. 417 `pꜣ šre Ḳrnyꜣ pꜣ mr-mšꜥ n pꜣ mw`, "the son of Qêreñya, the general of the water" |
| `Mni-se mte-lo` | "he was a child (`mte`) of Amun (`Mni-se`)" | none |
| `peseto-lo` (also REM 0106) | "he was a *peseto* (king's son, viceroy)" | Ph. 416 l. 15 gives this title to Abratoye; Ph. 417 does not give it to Bekemete |
| `pelmos adbli-se-lo` (also REM 0107) | "he was a general of the land (`adb`)" | none (no Demotic "general of the land" found) |
| `nobow 35 kelbo` | not glossed (`nob` "slave; Nubian"?, numeral 35) | none; Ph. 417 dates by "year 10" |

Facts that must match: the name; `kroro` = ꜣkrre; the filiation to a "general of the water". The Demotic
gives Bekemete only "the akrere". The Meroitic adds `peseto` and "general of the land", so in Meroitic his
rank is higher than the Demotic suggests.

### B. Manitawawi: REM 0097, 0105, 0088, 0089 beside Ph. 410, with Ph. 416 and 417 around him

REM 0097, FHN III reading; the corpus (T0009) has `RNAME` in the name slot:

| Line | Meroitic | Gloss from the gold files |
|---|---|---|
| 1-6 | `qo pelmos atolise Bekemete-li sete Mnitwwi-qo` | "This (is) the general of the water, Bekemete's `sete` (mother?), Manitawawi" |
| 7-12 | `wete *Siyete-li yetetke womneselḫ Pilqete-lo` | `wete`, `Siyete`, `yetetke` unglossed; "he was the great (`-lḫ`) *womnis* in Philae (`Pilqe-te`)" |
| 12-13 | `ant qori-to [= qori-se-lo]` | "he was a prophet (`ant`) of the king (`qore-se`)" |
| 14-15 | `ste-li qore *sem-lo` | "...`ste` ... king ... wife (`sem`)?": does not parse with the gold glosses |
| 16-18 | `ḫbḫñ sqote-lḫ-lo` | "he was ḫbḫñ ... great ..." (`ḫbḫñ` unglossed) |
| 18-19 | `mlo sto*se-lo` | "good ..." (unclear) |

REM 0105 gives only `qo pelmos atolise Mnitwwi-qo`. REM 0089 calls him `Mtewwi plmos adblit`, "general of the
land". REM 0088 calls him `qoreñ Wosse perite Mtwye`, "*qoreñ* of Isis, agent (`perite`), Mtwye".

The Demotic Ph. 410 gives him seven titles (Ashby pp. 279-280): prophet (ḥm-nṯr), qêreñ, agent of Isis, agent of
the King of Kush, prince of the land of Takompso, royal scribe of Kush, and astronomer.

| Fact | Meroitic | Demotic | Match |
|---|---|---|---|
| qêreñ of Isis, agent of Isis | REM 0088 `qoreñ Wosse perite` | Ph. 410 | yes (known; Griffith 1911 p. 9) |
| prophet | REM 0097 `ant qorise-lo`, "prophet of the king" | Ph. 410 "prophet (of Isis)" | the office matches; the god does not |
| general of the water / of the land | REM 0097, 0105 / REM 0089 | not in Ph. 410; Ph. 416 gives it to his son Wayekiye B | Meroitic only |
| ḫbḫñ | REM 0097 | not in Ph. 410; Ph. 120 and Ph. 403 give it to Wayekiye B (Ashby p. 165 n. 148) | the title runs in his branch of the family |
| `womnis-lḫ` "in Philae" | REM 0097 | prince of Takompso? prophet? | open (H7) |
| royal scribe of Kush, astronomer | none | Ph. 410 | Demotic only |
| relation to Bekemete | `Bekemete-li sete` | Ph. 417: Bekemete is "son of Qêreñya, the general of the water" | see H1 and H2 |

### C. The envoys to Rome: REM 0129 (Faras; corpus T0046) beside Ph. 416 ll. 1 and 18

The corpus line for REM 0129 runs: `... qoreN krorolowi qoreN nkdeyotowi [NAME] krorolowi apotelX
aromelitowi apote mXeyotowi apotelw qorete mXeyot ...`

Segmented and glossed: "he was *qoreñ* (and) *kroro*; he was *qoreñ* of Nkde(yo); he was the *kroro* of
[NAME]; he was the great envoy (`apote-lḫ`) of Rome (`Arome-li-to` = `-li-se-lo`); he was envoy of mẖe(yo)
...; envoy ... to the king (`qore-te`) ...".

Ph. 416 l. 1, Sasan son of Paese, reads `pꜣ ḳrnjꜣ ꜣkrre n Pr-ꜥꜣ pꜣ wpte ꜥꜣ n Hrme`: "the qêreñ, the akrere
of Pharaoh, the great envoy to Rome". Ph. 416 l. 18, Harwoj, reads `ḳrny ꜣkrr ...` (Ashby p. 149 n. 99).
FHN III p. 1008 adds a second Meroitic text, REM 0312 (`apote Arome-li-s`), probably the corpus line
`apote arome li s NAME yet mde lo wi` (T0040).

Facts that must match: the three titles, in the same order (H5). The Demotic "of Pharaoh" after akrere
answers to a possessor before `kroro-lowi` in the Meroitic (H4). Rome = `Arome` = `Hrme` is known
(gold: `arome`).

### D. Abratoye: REM 0321 and REM 0544 beside Ph. 416 l. 15 and I. Philae II 180 (27 Dec. AD 260)

| Fact | Meroitic | Demotic / Greek |
|---|---|---|
| name | `Brtoye-qowi` (REM 0321); `peseto Brtoye` (REM 0544, entries 3 and 7) | `ꜣbrṭy` (Ph. 416); `Αβρατοεις` (I. Philae II 180) |
| king's son | `peseto Akiñte-lo`, "*peseto* in Lower Nubia" | `pꜣ sꜣ-nsw`; `ψεντης βασιλέως Αἰθιόπων` "psentes of the king of the Ethiopians" |
| the king | `qori-se` in the other texts | `Pr-ꜥꜣ`; `βασιλέως Αἰθιόπων` |
| other titles | `womnise-lḫ Akiñte-lo`, `womnise kroro-lo`, `ant Mnp Pedemete-li-se-lo`, `aribet Twete-li-se-lo`, `pelmos adbli-se-lo`, `ḫrpḫñ Pḫrse-te-lo` | none: Ashby p. 165 notes that the Philae graffito gives only the title that mattered there |
| two terms as viceroy | REM 0544 lists him twice | Ph. 416 (AD 253) and I. Philae II 180 (AD 260) |

### E. Wayekiye A and his wife's kin: REM 0089 and 0088 beside Ph. 421, Ph. 344 and Dak. 33

| Fact | Meroitic | Demotic | Match |
|---|---|---|---|
| Makaltami, strategus in Meroe | `Mqoltemoye pelmos Bedewe-te-l` | Ph. 344 "strategus in Meroe" | yes (FHN III p. 973; gold `bedewe`, `-te`) |
| Bêk, agent | `Beke piri-te-l` | Dak. 33 Bêk | the person matches; the title is Meroitic only |
| Pakhom, great qoreñ | `Pḫeme qoreñ-lḫ-l` | none | none |
| Wayekiye A's own office | none: the stela lists only his kin | Ph. 421 "chief ritualist of the King of Kush" | none |
| a lesonis | `plsn qbñ-li penn *a/5 ni yeteke-lo` | Ph. 223: two lesonis of the family, one "in year 31" (Ashby p. 83 n. 125) | see H9 and H14 |
| numerals | `penn 34 nekw ḫ*tke-lo` | none dated | see H9 |

### F. The central text of the Meroitic Chamber: REM 0101 beside the Demotic and Greek embassy texts

| Meroitic (FHN III; corpus T0026) | Gloss | Demotic / Greek |
|---|---|---|
| `Wos Pilqete-l ḫe 1`, `Wos Tebwete-l ḫe 1` | "Isis of Philae: 1 `ḫe`; Isis of Tebwe: 1 `ḫe`" | I. Philae II 180-181 `Ἴσιδι Φιλῶν καὶ Ἀβάτου`, "Isis of Philae and of the Abaton" |
| `Asori Pilqete-leb tbo yinitḫe-b-to`, `Asori Tebwete-li ynitḫe-lo` | "Osiris of Philae ... two (`tbo`) ...; Osiris of Tebwe ..." | the Demotic reports gilding "the statue of Isis and the statue of Osiris" (Ph. 254) and making the shrine of Isis of the Abaton "in new work" (Ph. 421) (Ashby pp. 128, 136) |
| `Wos Aro-l trot`, `keñ Aro trot` | Horus (`Aro`); `trot` unglossed | none |
| `sdrte-lḫ 2 do 6`, `atmi wese 12 keñ 2`, `sdrte do 5`, `keñ-t ḫi 10` | numerals; nouns unglossed (`at` "bread"?) | Ph. 416 ll. 12-13: eight days of dining on wine, beer and meat; gifts of gold (Ashby p. 128 n. 41) |
| `ḫbḫñ qorises Mstrq qo yetebḫe` | "this (is) Mstrq, ḫbḫñ of the king ..." | the title ḫbḫñ appears in Demotic in Ph. 120 and Ph. 403 |

The theme matches: royal donations to Isis and Osiris of Philae and of the Abaton during an embassy. No
Demotic list of items or numbers was found that could be matched figure by figure.

### G. Tami: no Meroitic text

Ph. 417 and I. Philae II 181 give his Meroitic title as Demotic `ꜣrbtgyꜣ n ꞽst`, "arbetke of Isis". He
held it for 10 years (Ashby p. 148). Seven years later he "made peace" and crowned the prophet. The Meroitic
title is `aribet` (H13).

## Step 2 and 3. The hypotheses, each checked in the corpus and the literature

Confidence runs from 1 (a guess with one support) to 5 (near certain). The label is the literature status.

### H1. `ste`/`sete` can name a man: a guardian ("tutor"), not only the mother

- **Status: PUBLISHED HYPOTHESIS.** Rilly 2010 p. 63 says the term seems to mark a role in raising children
  through the passing on of an office ("tutor"); this is known here only through Ashby 2016 p. 281 n. 2,
  which applies it to REM 0097. The gold file already says "Rilly refines to tutor".
- **Confidence: 3.**
- **Aligned evidence.** In REM 0097, `Bekemete-li sete Mnitwwi-qo` makes Manitawawi the `sete` of Bekemete
  (possessor + `-li` + head, the juxtaposed genitive in the gold morphology). Manitawawi is a man: he is the
  brother-in-law of Wayekiye A and the father of Wayekiye B (Ph. 410, Ph. 416; Wikipedia after Török 2009
  p. 456; Ashby p. 144 n. 79).
- **Alternatives.**
  1. `sete` is a different word from `ste` "mother".
  2. The phrase is cut differently: Ashby reads "Manitawawi, `sete` of the strategos of the water".
- **Corpus.** `Ste`/`ste` has 75 hits. Most are in women's kin lists (`NAME Stelowi`); one is plural,
  `kroroleb Stebetowi`, "`ste` of the kroros" (T0565). No second male `ste` was found in this pass, so the
  gold gloss "mother" stands for the usual case. The bilingual case only shows that it is not exclusive.

### H2. REM 0098 settles Ph. 417: the "general of the water" in Tami's text is Bekemete's father

- **Status: NEW.** Ashby p. 144 n. 79 reads Ph. 417 the other way and counts Bekemete among the holders of
  "strategos of the water". FHN III's own note was not reread. Searches for "Bekemete" with "son of",
  `sete` and "general of the water" found nothing that uses REM 0098 for this.
- **Confidence: 3.**
- **Aligned evidence.**
  1. Ph. 417 reads `Bk-mty pꜣ ꜣkrre pꜣ šre Ḳrnyꜣ pꜣ mr-mšꜥ n pꜣ mw`. "The general of the water" can stand in
     apposition to Bekemete or to his father.
  2. REM 0098 reads `(s/m)te pelmos atolise-l yerike-lo`, "begotten by a general of the water". `yerike` is a
     listed variant of `terike` "begotten by (father)" (gold).
  3. None of REM 0098, 0106 or 0107 gives Bekemete himself "general of the water". He is "general of the
     land" (REM 0107).
- **What follows.**
  1. Bekemete's father was a general of the water.
  2. `Ḳrnyꜣ` is either his name (Török's tree: a son of Wayekiye A called Qorene) or the title "the qêreñ".
  3. If it is the title, it names a qêreñ who was general of the water. Manitawawi was both (Ph. 410,
     REM 0105), and so was his son Wayekiye B (Ph. 416).
- **Alternatives.**
  1. The corpus reading `mte` gives "the child begotten by a general of the water"; the sense is the same.
  2. The Demotic and the Meroitic name different generals of the water: three held the title in this family.
- **Corpus.** `yerike` occurs only here (T0318). `terike` is in hundreds of epitaphs, always after the
  father's name.

### H3. `Tebwe` is the Abaton (Biga), not Thebes

- **Status: PUBLISHED HYPOTHESIS.** Griffith 1911 pp. 62 and 82 proposes it with "perhaps" (gold, probable).
  Ashby pp. 281-283 reads "Isis of Philae and the Abaton" and, for MI 125, "Harendotes in the Abaton
  (`Aretete Tebawe-teli`)". FHN III prints "Thebes (?)".
- **Confidence: 4.**
- **Aligned evidence.**
  1. REM 0101 pairs `Wos Pilqete-l` with `Wos Tebwete-l` and `Asori Pilqete` with `Asori Tebwete`.
  2. The Greek proskynemata of the same embassies pair the same two places: Ἴσιδι Φιλῶν καὶ Ἀβάτου
     (I. Philae II 180, 181).
  3. The Demotic texts of the Wayekiye family centre on Isis's procession to the Abaton (Ph. 421; Ashby
     pp. 128-129).
  4. Thebes plays no part in any of these texts.
- **Alternative.** Thebes, as FHN III prints; it is supported by no text here.
- **Corpus.** `tebwe` is in 13 texts, always beside Isis or Osiris (`aSori tebweteli yinitxe lo`, T0085).
  That is the distribution of a cult place.

### H4. `kroro` takes a possessor: "the kroro of X", as Demotic has "akrere of Pharaoh"

- **Status: NEW for the construction.** The equation `kroro` = ꜣkrre is ESTABLISHED (Griffith 1911 p. 10;
  FHN III; TLA dm520 citing Zibelius-Chen 2011 pp. 284f.). No source found gives a meaning. Searched:
  "akrere" or "kroro" Meroitic title meaning; the TLA.
- **Confidence: 2.**
- **Aligned evidence.**
  1. Ph. 416 l. 1 has `ꜣkrre n Pr-ꜥꜣ`, "akrere of Pharaoh".
  2. REM 0129 has `[NAME] krorolowi`: a personal-name slot (masked; filled with swapped names in the
     augmented file) directly before "he was *kroro*". By the juxtaposed genitive this is "he was the kroro of
     N". N may be the king, but the original name is lost to the masking.
  3. `Siremroke kroro` occurs twice (REM 0129; T0565 `Siremroke kroroleb Stebetowi`), which looks like a
     place or a person as the possessor.
- **Alternative.** `kroro` is a rank that needs no complement, and the names before it are the holders.
- **Corpus.** 56 hits: `kroroli`, `kroroleb` (plural "the kroros"), `krorolowi`, and `NAME kroro` (T0008).

### H5. REM 0129 holds the same cursus of titles as Sasan and Harwoj in Ph. 416

- **Status: NEW.** Lead 1 and FHN III p. 1008 use REM 0129 only for the phrase "great envoy to Rome". No
  source found compares the whole title chain. Searched: REM 0129 / Faras with "envoy to Rome" and the TLA
  ꜣkrre page.
- **Confidence: 3** for the shared chain; **1** for the owner being Sasan or Harwoj.
- **Aligned evidence.**
  1. REM 0129 reads `qoreN krorolowi ... [NAME] krorolowi apotelX aromelitowi`.
  2. Ph. 416 l. 1 reads `pꜣ ḳrnjꜣ ꜣkrre n Pr-ꜥꜣ pꜣ wpte ꜥꜣ n Hrme`, and l. 18 reads `ḳrny ꜣkrr`.
  3. The order is the same: qoreñ, then kroro, then great envoy to Rome.
- **What follows.**
  1. The three titles went together for the 3rd-century envoys to Rome.
  2. The REM 0129 stela belongs to such an envoy.
  3. Its other envoy titles (`apote mẖe-yo-to-wi`, `apote-l-w qore-te`) would be the next words to align,
     against the parts of Ph. 416 not yet compared.
- **Alternative.** The order is the normal hierarchy of any Meroitic official's titles, not a fixed
  envoy cursus.
- **Corpus.** The chain occurs only in REM 0129 (T0046, T0064, T0271, which are copies). `apote arome li s`
  (T0040) has no `kroro`.

### H6. `qoreñ` is built on `qore` "king" and heads its own genitives

- **Status: PUBLISHED HYPOTHESIS.** Ashby pp. ix and 149-150, citing Hofmann 1981 p. 62 and Török 1979
  pp. 42 ff., says it is built on `qore`. Zibelius-Chen 2011 doubts it and relates it to `qorise` "of the
  king" (TLA [d6401](https://thesaurus-linguae-aegyptiae.de/lemma/d6401)). Brugsch derived it from Greek
  κλίνη (Ashby p. 150 n. 105). Ashby notes the old gloss "royal scribe" is doubted by Rilly 2007
  pp. 142-143.
- **Confidence: 2.**
- **Aligned evidence.**
  1. The Demotic `ḳrny(ꜣ)` is a transliteration, never a translation, and takes either "of Pharaoh" or "of
     Isis".
  2. The Meroitic `qoreñ` heads `Wos-se` "of Isis" (REM 0088, 0111), `ponni-li-se` (REM 0100) and `-lḫ`
     "great" (REM 0089). So it is a noun that heads its own phrase, not an adjective "royal".
- **Corpus.** 16 hits. One weighs against reading `-ñ` as a suffix that only makes this title: REM 1003
  (T0957) has `qoreNyi akinidd pqrNyi pestoNyi`, the same `-ñ(yi)` on `qore`, `pqr` and `peseto`. So `-ñ` is
  a productive element on titles, which makes the derivation less certain.

### H7. `womnis-lḫ` "in [place]" is a territorial office

- **Status: NEW**, with a published alternative. Ashby p. 281 renders REM 0097's `womnese-lḫ Pilqeteli` as
  "great prophet of Amun in Philae", citing Rilly 2007 pp. 144-148, which implies a split `wo-Mni-se`.
  Searched: "womnis", "wmnis", "womnise", "wemnes" with Meroitic; nothing found.
- **Confidence: 1.**
- **Aligned evidence.**
  1. Manitawawi is `womnise-lḫ Pilqete-lo` in REM 0097, and his Demotic Ph. 410 gives him "prince of the land
     of Takompso", a regional rank.
  2. Abratoye is `womnise-lḫ Akiñte-lo`, "great womnis in Lower Nubia", next to `peseto Akiñte-lo`, the
     viceroy of the same province (REM 0321).
- **Alternatives.**
  1. Ashby's "prophet of Amun".
  2. A temple-finance office.
- **Corpus.** `womn-` tokens have 441 hits, nearly all `womnitX` in copies of one long list
  (`womnitX Sklte NAME yetmdelowi`). The title is followed by a place there too, which fits a place-bound
  office.
- **Tested on 2026-11-11, and weakened.** If `womnise` were the "prince of Takompso" of the Demotic, its place
  should be Takompso. Manitawawi's is Philae (REM 0097) and Abratoye's is Akiñ. The Demotic sentences of the TLA
  name a second holder of that Demotic title, Patahutresi, "qorene of Isis, agent of Isis, prophet of Isis,
  prince of the land (Ta)kompso", so the title went with those offices; nothing ties it to `womnise`.

### H8. `Mni-se mte` "child of Amun" is a title or epithet

- **Status: PUBLISHED HYPOTHESIS.** Ashby p. 281 gives Bekemete "mte of Amun" for REM 0098. The parts are in
  the gold files: `Mni`/`amni` Amun, `-se` "of", `mte` child.
- **Confidence: 3.**
- **Aligned evidence.** It sits in Bekemete's list of offices, between his filiation and `peseto`. Ph. 417
  has no counterpart.
- **Alternative.** `Mnise` is a personal name ("he was the child of Mnise"), giving a second filiation.
- **Corpus.** The same pair stands alone as a label in T0771 (`mnis mte`). A repeated two-word label fits a
  title better than a one-off name.

### H9. `penn` + numeral counts years

- **Status: NEW.** Searched: a Meroitic word for "year" with plsn, lesonis, Wayekiye and REM 0089; nothing
  found.
- **Confidence: 1.**
- **Aligned evidence.**
  1. REM 0089 has `plsn qbñli penn*ani yetekelo` (the corpus reads `penn 5 ni`) and `penn 34 nekw
     ḫ*tkelo`.
  2. The Demotic texts of this family count years: a lesonis "in year 31" (Ph. 223); Tami ten years as
     arbetke (Ph. 417); "after seven years" (I. Philae II 181).
  3. A lesonis held a fixed-term office.
- **Weakening evidence.**
  1. FHN III reads `*a` where the corpus has 5.
  2. `qeren penni li s le` (T0295) and `qoreñ ponni-li-se-lo` (REM 0100) make `penni` something a qoreñ can be
     "of". Ashby (p. 281) gives `Pennay?` as a place for MI 122.
- **Alternatives.** A place name; a unit of measure.
- **Corpus.** One formula, `plSn X penn 5 ni ye teke lo`, makes up 203 lines of the augmented raw file and
  about 25 texts in `corpus.jsonl`. Besides it: `penn 34N kw`, `penn 34 ati...`, `keN 6 Snswe penno` (T0080)
  and `penn tewisti` (T0035).

### H10. `ḫe` in REM 0101 is a counted cult object given to each Isis

- **Status: NEW.** Searched: REM 0101 offerings, the Meroitic Chamber, numerals; no reading of the item words
  was found.
- **Confidence: 1.**
- **Aligned evidence.**
  1. REM 0101 has `Wos Pilqete-l ḫe 1` and `Wos Tebwete-l ḫe 1`: one for each Isis.
  2. The Demotic reports of the same period give each cult image or shrine one gift: gilding "the statue of
     Isis and the statue of Osiris", and the shrine of Isis of the Abaton (Ashby pp. 128, 136).
- **Alternatives.** A measure of gold; a kind of offering, such as a meal (cf. gold `ḫre` "food").
- **Corpus.** The corpus fuses the numeral into the word (`pil qetelxe l`, `tebwetel xe l`). There are no
  independent hits.

### H11. `ḫbḫñ` is a native Meroitic title that the Demotic writes `ḫbḫn`, and `ḫbḫñ-lḫ` = "great ḫbḫn"

- **Status: ESTABLISHED** as a title equation: Ashby p. ix, p. 144 n. 81 and p. 165 n. 148 (Ph. 120,
  Ph. 403); TLA [dm6015](https://thesaurus-linguae-aegyptiae.de/lemma/dm6015) citing Zibelius-Chen 2011
  p. 292. Its meaning is unknown ("as-yet-undefined", Ashby p. 144).
- **Confidence: 4** for the equation; **1** for any meaning.
- **Aligned evidence.**
  1. Ph. 403's "great ḫbḫn" (Ashby pp. 279-280) matches REM 0110 `ḫbḫñ-lḫ`. That is another case of Demotic ꜥꜣ =
     Meroitic `-lḫ`, which is already gold.
  2. The holders are Payesi, Manitawawi, his son Wayekiye B, and his daughter Ame-ye (a woman: GA 20).
     Outside the family, Mštrqye holds it "of the king" (`qorise`), and others "of Dr" or "in Daqaḫr".
  3. A weak NEW guess: it is a place-bound civil office of the water-general branch.
- **Corpus.** `xbxN` is in 30 texts.

### H12. `Wos qer` is an office of Isis, and Ph. 403 renders it

- **Status: NEW.** No source found discusses `qer`.
- **Confidence: 1.**
- **Aligned evidence.**
  1. Mštrqye is `ḫbḫñ Wos qer` (REM 0102), `Wos qer-lo` (REM 0109), and `qoreñ Wos-se perite Wos-se Wos qer`
     (REM 0111).
  2. Ph. 403 gives "great ḫbḫn, qeren of the king, *huite* (?) of Isis" (Ashby pp. 279-280). The same kind of trio
     appears: ḫbḫñ, qoreñ, and an X of Isis.
- **Alternatives.** `qer` is part of a name, or a verb form.
- **Corpus.** 19 hits of `qer`. The Philae ones are all `woS qer`; the others (`SSimetel yetmdelowi qer tesk`)
  look unrelated.

### H13. `aribet`/`arbetke` = Demotic ꜣrbtgyꜣ, an office of grain measuring or tax collecting

- **Status: PUBLISHED HYPOTHESIS.**
  1. Griffith 1937 p. 120 links it to the artaba, a grain measure (via FHN III p. 1014).
  2. Török in FHN III (quoted by Ashby p. 148) reads it as a collector of the grain taxes for Isis.
  3. FHN III renders REM 0321's `aribet Twete...` as "corn measurer (?) in Sedeinga".
- **Confidence: 3.**
- **Aligned evidence.** Tami's Demotic title in Ph. 417, held for ten years. No Meroitic text of Tami
  survives, so the pairing is by title only.
- **Corpus.** 400 hits (copied lists). It is always followed by a place or a qualifier (`aribet wetemtr`,
  `aribet tedeqeli`, `aribet tpoteNteli`), which fits a local fiscal post.

### H14. `plsn` = lesonis (Demotic mr-šn, Greek λεσῶνις)

- **Status: PUBLISHED HYPOTHESIS.** Ashby p. ix and FHN III p. 973 accept it; Hintze 1973 doubts it.
- **Confidence: 3.**
- **Aligned evidence.**
  1. The family held the lesonis office in Demotic: Hornakhtyotef I and Sosen in Ph. 223.
  2. Wayekiye A's stela (REM 0089) names a `plsn`.
  3. The sound match `p-l-s-n` = pꜣ mr-šn is of the same kind as `pelmos` = pꜣ mr-mšꜥ.
- **Corpus.** It appears only in the `plSn X penn 5 ni yeteke-lo` formula (about 25 lines) and in T0441-0442.

## Counts

| Label | Count | Hypotheses |
|---|---|---|
| ESTABLISHED | 1 | H11 (`ḫbḫñ` = Demotic ḫbḫn, meaning unknown) |
| PUBLISHED HYPOTHESIS | 6 | H1 (Rilly 2010 via Ashby), H3 (Griffith 1911, Ashby 2016), H6 (Hofmann 1981, Török 1979; Zibelius-Chen 2011 against), H8 (Ashby 2016), H13 (Griffith 1937, Török in FHN III), H14 (FHN III, Ashby; Hintze against) |
| NEW | 7 | H2, H4, H5, H7, H9, H10, H12 |

## What would test these next

1. **H2 and H1.** Reread FHN III pp. 1010-1016 (Ph. 417) and pp. 1028-1031 (REM 0097, 0098) for whether the
   editors attach "general of the water" to Bekemete or to his father. Check the REM 0098 sign `ste`/`mte`
   on Griffith 1912's plate.
2. **H5 and H4.** Get Griffith's or REM's reading of REM 0129, to recover the masked name before
   `krorolowi`.
3. **H9.** Check FHN III's image of REM 0089 lines 10-13 for numeral against `*a`, and look for `penn` with
   numerals in REM texts outside this corpus.
4. **H10.** Use the Demotic item lists in Pope 2014, *Meroitic Diplomacy and the Festival of Entry*, for
   numbers to set against REM 0101.
