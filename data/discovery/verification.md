# Verification of the seven "NEW" claims

Adversarial check, run 2026-11-09, about 60 minutes. Each claim was tested twice: against the literature (searched again,
with different terms and in French and German) and against the corpus (`data/corpus_v2.jsonl`, the concordance tool,
and Otten's unmasked raw file `data/otten/Data/mero-corpus.txt`).

## Verdicts first

| # | Claim | Verdict | Why, in one line |
|---|---|---|---|
| 1 | REM 0129 has Sasan's title chain (Ph. 416) in the same order | **WEAKENED** | The masked word in REM 0129 is the title `womnis`, so the "chain" is five or more titles, not three; FHN III already pairs REM 0129 with Sasan's envoy title, and `qoreñ-kroro` precedes `apote` in another family's text too. |
| 2 | REM 0098 settles Ph. 417: "general of the water" is Bekemete's father's title | **WEAKENED** (core alignment already published) | Griffith 1911, p. 21, already set Ph. 417 beside REM 0098 "begotten of the mate and strategus of the water"; Millet 1968 translates it the same way; Török 2009, p. 464, reportedly makes the father a *pelmos*. REM 0098 shows the father held the title, not that Bekemete did not. |
| 3 | `wi` before a numeral marks a total | **WEAKENED** (partly published) | Hofmann 1981, p. 326 (via FHN II, p. 722), found that line 25 of REM 1003, whose only number is `wi 3348`, gives the exact sum of the men and women counted. REM 1041 has `abr wi 1032 kdi 2623`, where `wi` stands before the men's count only. The Tanyidamani "12" holds. |
| 4 | The closing 1,626 and 1,032 of REM 1003 count animals (`asr`) | **WEAKENED** | REM 1041 counts **1032 men** (`abr wi 1032`): the same number, in a stela of the same court. The sum in l. 25, just before `wi 1626`, counts people (Hofmann). Zach 2017 discusses a correction of the l. 26 numeral and was not read. |
| 5 | `plsn` comes from Egyptian pꜣ mr-šn, "the lesonis" | **ALREADY PUBLISHED** | FHN III, p. 973 with n. 599 (proposal reported, Hintze 1973b, p. 335, doubting it); Ashby 2016, p. ix. Lead 01 and `philae.md` H14 already cite both. |
| 6 | The vocative `-i` goes to the end of "god + epithet"; Osiris is never `Soreyi` before an epithet | **WEAKENED** | Rilly already published a phrase-final single vocative for "Isis + Osiris" (2007, p. 297; *Dotawo* 7, n. 127). Isis carries both `woSi` and an epithet in one family (T0005). The Osiris distribution holds in the corpus. |
| 7 | `penn` is a counted time unit in datelines (numbers up to 34), not "day" | **ALREADY PUBLISHED**, and weakened | Millet 1968 translates `penn 34` as "regnal year 34" and `penn 5 ni` as "fifth year of the penn-cycle" (tagged DATE). `penn`/`ponni` also occurs where no time unit fits (`qoreñ ponni-li-se`, Kharamadoye `penn tlte`). No source was found that proposed "day". |

None of the seven stands as a clean new finding. The nearest to new are the Tanyidamani observation in 3 (twelve 1s,
then `mk lte wi 12`) and the extension in 6 from "Isis + Osiris" to "god + epithet". Both still need checks in print:
Hintze 1960 for 3, and Rilly 2007, Rilly & de Voogt 2012 (p. 155) and Heyler 1964 for 6.

## Sources used in this run

Local copies, read in full text (they were fetched earlier this session; page numbers are the printed ones):

1. [FHN II](https://data.ub.uib.no/files/manlib/ubb/ubb-msref/ubb-msref-0939/ubb-msref-0939-078/ubb-msref-0939-078-fon/ubb-msref-0939-078-fon-02/pdf/ubb-msref-0939-078-fon-02_orig.pdf),
   pp. 716-725 (REM 1003, REM 1041), from the PDF's text layer. Numbers were not checked against the page images.
2. [FHN III](https://data.ub.uib.no/files/manlib/ubb/ubb-msref/ubb-msref-0939/ubb-msref-0939-078/ubb-msref-0939-078-fon/ubb-msref-0939-078-fon-03/pdf/ubb-msref-0939-078-fon-03_orig.pdf),
   pp. 972-975 (REM 0089, REM 0088, the family tree), 992 (Dak. 31), 1008 (Ph. 416), 1014 (Ph. 417), 1029-1031
   (Meroitic Chamber), from the text layer.
3. [Ashby 2016](https://knowledge.uchicago.edu/records/c229v-78575/files/Ashby_uchicago_0330D_13172.pdf), pp. ix, 82-83,
   144 n. 79, 281 (Appendix C).
4. [Griffith 1911, *Karanòg*](https://archive.org/details/karangmeroitic00grifuoft), pp. 10 and 21 (OCR text).
5. Millet 1968, *Meroitic Nubia*, through Otten's transcription,
   [`MilletExamples.txt`](https://github.com/Joshua-Otten/Meroitic-Corpus/blob/main/Data/MilletExamples.txt) (local copy
   `data/otten/Data/MilletExamples.txt`). Line numbers below are that file's.
6. Rilly, [*Personal Markers and Verbal Number in Meroitic*](https://pages.sandpoints.org/dotawo/article/rilly),
   *Dotawo* 7, §5.1 and nn. 126-129; Rilly 2016, [*Meroitic*](https://escholarship.org/uc/item/3128r3sw), p. 9; Rilly &
   de Voogt 2012, excerpt pp. 1-10 and the table of contents; Lipiński 2011 (review of Rilly 2010).

New this run, read online:

1. Otten & Anastasopoulos 2025, [*Towards Ancient Meroitic Decipherment*](https://aclanthology.org/2025.alp-1.11.pdf),
   the passage on the Isis and Osiris epithets.
2. [Wikipedia, "Wayekiye family"](https://en.wikipedia.org/wiki/Wayekiye_family), raw wikitext, after Török 2009.

Found but not readable here:

1. Zach 2017, [*A Remark on the 'Akinidad' Stela REM 1003*](https://www.sudarchrs.org.uk/wp-content/uploads/2020/03/SARS_SN21_Zach.pdf),
   *Sudan & Nubia* 21: 148-150. The certificate on sudarchrs.org.uk has expired, Academia.edu returned 403, and the
   [Vienna record](https://ucrisportal.univie.ac.at/en/publications/a-remark-on-the-akinidad-stela-rem-1003-british-museum-ea-1650/)
   has no abstract.
2. Ferrandino & van Gerven Oei 2020,
   [*Potential Old Nubian cognates for Meroitic aleqese*](https://www.sudarchrs.org.uk/wp-content/uploads/2021/10/SARS_SN24_Ferrandino_vanGervenOei.pdf),
   *Sudan & Nubia* 24. Same certificate problem; it was seen only through a search snippet.
3. Google Books search inside Török 2009 hit Google's bot check, which was not bypassed. The Google Books API returned
   nothing. web.archive.org cannot be reached by the fetch tool.

## Claim 1. REM 0129 gives Sasan's title chain in the same order

**Verdict: WEAKENED.** The evidence rests partly on a masking artifact.

**Corpus check.**

1. The `[NAME]` before the second `krorolowi` is not a name. Otten's raw file keeps one unswapped copy of REM 0129:
   `qEreN krErElEwi qEreN nkdeyEtEwi wEmnis krErElEwi apEtelX arEmelitEwi`. Millet's transcription of the same text
   (`MilletExamples.txt` l. 1398) has `wEmnis krErElEwi` too. The other corpus copies put swapped names there
   (`.eqetme`, `Ntewitr`, `BrEXekye` and others), which is why `corpus_v2` masks it.
2. So REM 0129 reads, in order: `qoreñ kroro-lowi`; `qoreñ Nkdeyo-to-wi`; `womnis kroro-lowi`; `apote-lḫ
   Arome-li-to-wi` ("great envoy to Rome"); `apote mḫeyo-to-wi`; `apote-l-w qore-te mḫeyo-t ...`; and later
   `apote Xlite-te-lowi`. Sasan's Ph. 416, l. 1 has three elements: "qêreñ akrere of Pharaoh, great envoy to Rome".
   The shared part is only the subsequence "qoreñ-kroro ... great envoy to Rome", with two other titles between them
   in REM 0129.
3. `qoreñ kroro` is a compound title, not a chain of two. Millet lists `qEreN-krErE` as a TITULARY (ll. 840, 1399,
   1404), beside `wEmnis-krErE` (ll. 550, 1403) and `SiremrEke-krErE` "envoy of the king" (l. 517). That matches the
   Demotic pairing `ḳrnjꜣ ꜣkrre` as one unit.
4. The order is not envoy-specific. T0045, a kin list of another family, has `qoreN kroroleb yetmdelowi xrpxN
   Sqekiteleb yetmdelowi apote...`: qoreñ-kroro again comes before an envoy. This fits the alternative already listed
   in `philae.md` H5: ordinary rank order.
5. A side effect for `philae.md` H4: "kroro of N" loses its evidence, because the possessor slot is the title
   `womnis` (also in REM 0321, `womnise krorolo`).

**Literature.**

1. FHN III, p. 1008 (Török, on Ph. 416) reads Sasan's "qoreñ akroro of the King" as one Meroitic title built on
   `qore`, and "great envoy to Rome" as `apote-lḫ Arome-li-s`, citing REM 0129 and 0312. Griffith 1911 already had the
   envoy equation (p. 10), and on p. 21 n. 1 notes the "Akrer, the great envoy to Rome" of the same Demotic text. The
   pairing of REM 0129 with Sasan's titles is therefore published for the envoy title. The remark that REM 0129 also
   opens with `qoreñ kroro` was not found stated.
2. The places where it would be, if anywhere, were not read: Pope 2008/9 (*Enchoria* 31: 68-103, the edition of
   Ph. 416), Pope 2014, and Zibelius-Chen 2011, pp. 284f. (ꜣkrre, [TLA dm520](https://thesaurus-linguae-aegyptiae.de/lemma/dm520))
   and pp. 295f. (qrnjꜣ, [TLA d6401](https://thesaurus-linguae-aegyptiae.de/lemma/d6401)).

**Searched:** "Philae 416 Sasan qereñ akrere Meroitic titles REM 0129 Faras envoy to Rome Pope Enchoria"; "Zibelius-Chen
2011 Nubisches Sprachmaterial ꜣkrre akrere qrnjꜣ meroitisch kroro qoreñ Titel"; full text of FHN III, Ashby, Griffith
1911 and Millet's transcription for `kroro`, `akrere`, `envoy`, `0129`.

**What would settle it:** Pope 2008/9 on line 1 of Ph. 416, and the REM edition of REM 0129 for the order of its titles.

## Claim 2. REM 0098 shows that "general of the water" in Ph. 417 is the father's title

**Verdict: WEAKENED.** The alignment it rests on is a century old, and the inference is weaker than "settles".

**Literature.**

1. **Griffith 1911, p. 21:** "'Bekemate the Akrere, son of Qeren, the strategus of the water', mentioned in an undated
   but certainly late Egyptian demotic text at Philae, is probably identical with 'the krer Bekemate, begotten of the
   mate and strategus of the water' ... (Inscr. 98)". Griffith set the two texts side by side, with "begotten of ...
   strategus of the water" in the Meroitic. He did not say in so many words which person holds the Demotic title.
2. **Millet 1968, pp. 252/253** (`MilletExamples.txt` l. 305): `mte pelmES atElit yerike-lE` = "begotten of the mte
   (and) general of the water".
3. **Török 2009, p. 464**, as summarised on [Wikipedia](https://en.wikipedia.org/wiki/Wayekiye_family): "Wayekiye (A)
   had another son, Qorene, who was also *pelmos* ... His son Bekemete reached the position of *peseto*". If the
   summary is accurate, Török gives the father a general's title, which is claim 2's conclusion. The page itself was
   not seen, because Google Books returned its bot check.
4. **Against the claim:** FHN III, p. 1014 (Ph. 417): "the ꜣkrre ... and strategus 'of the water' ..., Bekemete, son
   of Qêreñ". Ashby 2016, p. 144 n. 79 and p. 281 also give the title to Bekemete. The FHN III family tree (p. 975,
   after Burkhardt 1985: 96) gives Qêreñ no title, and his own graffito Dak. 31 (FHN III no. 254) has none. FHN III's
   list of Bekemete's titles in the Meroitic Chamber (p. 1029) leaves out the `yerike` phrase.

So the explicit argument "REM 0098 decides the apposition in Ph. 417, against FHN III and Ashby" was not found in print,
but its evidence is Griffith's, and Török 2009 may already state the conclusion.

**Logic.** REM 0098 shows that Bekemete's begetter was a general of the water. It does not show that Bekemete was not
one too. The title ran in the family (Ashby n. 79 lists four holders), and REM 0097 can be cut "the `sete` of the
general of the water Bekemete" (Ashby p. 281), which would make Bekemete a holder. "Settles" should become "favours".

**Corpus check.** `yerike` occurs only in REM 0098 (T0318, and the fragment T0237): `qo kroro bekemete mte pelmoS atolit
yerike lo mnis mte lo pesto lo pelmoS ...`. The corpus and Millet read `mte`; FHN III reads `ste`; Griffith reads
"mate". The sense "begotten by a general of the water" holds under all three readings.

**Searched:** "Bekemete strategos OR strategus of the water son of Qeren OR Qêreñ father Meroitic Chamber Philae 417";
the raw Wikipedia text; Google Books inside Török 2009 (blocked); full text of FHN III, Ashby, Griffith 1911 and
Millet's transcription.

**What would settle it:** Török 2009, p. 464, read directly, and Griffith 1937's note on Ph. 417.

## Claim 3. `wi` before a numeral marks a total

**Verdict: WEAKENED, and partly ALREADY PUBLISHED.**

**Literature.**

1. FHN II, p. 722: "As shown by Hofmann (1981, 326), a precise addition of the numbers of abr, man, and kdi, woman
   given in the course of the narrative is to be found in line 25." The only number in l. 25 (FHN II, p. 720) is
   `abri *k„ wi 3348`. So the one REM 1003 case of `wi` + numeral that has been tested against its list was shown to
   be a total in 1981. Whether Hofmann went on to call `wi` itself a total marker was not seen (print only).
2. No source was found for the Tanyidamani case. Hintze 1960 (*Kush* 8: 125-162), the edition, was not reachable.

**Corpus check.**

1. There are only three `wi` + numeral cases in `corpus_v2` (and the same three in `corpus.jsonl` and Otten's raw
   files): REM 1044 `mk lte wi 12`, and REM 1003 `asr axidebx wi 1626` and `asr axidebxe wi 1032`. REM 1003 l. 25
   `wi 3348` is in neither corpus file.
2. Tanyidamani holds. Exactly twelve `1`s precede `mk lte wi 12` (token positions 48 to 76 of the row): `edxN`, `mno`,
   `amnpte`, `aqedise`, `mtotiwxne`, `axboroteN`, `amnb`, one bare `1`, `meke`, `pxtotN`, `mt`, `xtebemeyose`.
3. REM 1003's closings do not check. The legible counts in FHN II sum to 648 (32 + 135 + 100 + 100 + 58 + 223), which
   is neither 1626 nor 3348. Hofmann's sum must use readings the corpus lacks.
4. **A case against:** REM 1041, fragment B l. 4 (FHN II, p. 725): `abr wi 1032 kdi 2623 be qore lw`. Here `wi` stands
   before the men's count but not the women's. This is the test that `hamadab.md` H1 names. It cannot refute the
   claim, because the fragment shows no preceding list, but it does not support "total" either.

**Searched:** "Hofmann Material für eine meroitische Grammatik Hamadab Stele Zahlen Summe 3348 OR 1626 OR 1032";
"Tanyidamani stela Meroitic list of gods 12 total Hintze 1960 Kush 8 numerals"; "Tañyidamani Stele Götterliste 12
Summe Hintze meroitisch Zahlzeichen wi"; full text of FHN II and *Dotawo* 7 for "total", "numeral" and the numbers.

**What would settle it:** Hofmann 1981, pp. 288-326, and Hintze 1960 on the Tanyidamani god list.

## Claim 4. The closing 1,626 and 1,032 of REM 1003 count animals

**Verdict: WEAKENED.** No published proposal was found, but the strongest parallel goes the other way.

**Literature and parallels.**

1. **REM 1041** (Amanishakheto, Meroe City; FHN II no. 178, p. 725, fragment B l. 4): `abr wi 1032 kdi 2623`. The
   same number, 1032, counts **men**, in a royal stela of the generation after Amanirenas. If the two stelae record
   the same tally, REM 1003's `wi 1032` counts people, not animals. The number was read from FHN II's text layer, not
   from the page image.
2. **Hofmann 1981, p. 326** (via FHN II, p. 722): the `wi 3348` in l. 25, one line before `asr aḫidebḫ wi 1626`,
   is a sum of men and women. FHN II adds that the large numbers "fit much better into the context of a record of a
   war".
3. **Zach 2017** (*Sudan & Nubia* 21: 148-150) reports a deleted and re-cut numeral at the end of l. 26, which is the
   position of 1626. One search summary said Zach ties the numbers to booty or livestock, and a second summary of the
   same results did not confirm it. The PDF could not be opened. It must be read before anything is claimed.
4. **For the claim (genre only):** Kushite royal booty lists count cattle in large numbers. Nastasen's stela (FHN II
   no. 84, p. 488) has "long-horned oxen: 209,659 (head); livestock: 505,349 (head)".
5. The gloss `asr` "meat, animal" is in Rilly 2016, p. 9, among the words "for which a translation is currently
   available".

**Corpus check.** One-word `asr` occurs three times: REM 1003 twice (`asr axidebx wi 1626`, `asr axidebxe wi 1032`, the
same refrain) and REM 1044 once (`itrek asr deb 5000`). Each is within three tokens of a numeral, so the pattern
holds, but there are two independent contexts, not three. REM 1044 also has `as r meke` and `asrlitoN` with no number.

**Searched:** "Meroitic Hamadab stela Akinidad numbers cattle captives 1626 OR 1032 OR 3348 asr animals" (extended); "Zach
A Remark on the Akinidad Stela REM 1003 Sudan & Nubia 21 numeral line 26 correction livestock booty" (extended); the
Vienna record; Academia.edu (403); the *Dotawo* article "Gender as Frame of War" (it does not discuss the numbers);
full text of FHN II, Rilly 2016, *Dotawo* 7 and Lipiński 2011 for `asr`, cattle and animals.

**What would settle it:** Zach 2017; the FHN II plate of REM 1041 to confirm `abr wi 1032`; Hofmann 1981, p. 326, for which
numbers make 3348.

## Claim 5. `plsn` comes from Egyptian pꜣ mr-šn, "the lesonis"

**Verdict: ALREADY PUBLISHED.**

**Literature.**

1. FHN III, p. 973 (on REM 0089): "plsn is supposed to derive from Egyptian Greek λεσῶνις, a high priestly title with
   the meaning 'Tempelvorsteher' in the Roman period (Otto 1905, 39, 49)". Note 599 adds: "Hintze 1973b, 335, however,
   doubts this derivation." So the derivation was proposed before 1973 and argued about.
2. Ashby 2016, p. ix (glossary): `plsn` "lesonis", from Demotic pꜣ mr-šn. Ashby pp. 82-83 shows the Wayekiye family
   holding the lesonis office at Philae and Dakka (Ph. 223; Dak. 30).
3. These two sources are already cited in this project: lead 01 (titles table) and `philae.md` H14, labelled
   PUBLISHED HYPOTHESIS. `funerary.md` item 26 missed them.

**Corpus check.** `plSn`/`plsn` has 18 hits in `corpus_v2`, all in the `plSn X penn 5 ni ye teke lo` formula and in
T0441-0442. This is consistent with a title, and adds nothing on the etymology.

**Searched:** full text of FHN II, FHN III, Ashby and Griffith 1911 for "lesonis", "mr-šn" and "plsn".

## Claim 6. The vocative `-i` goes to the end of "god + epithet"

**Verdict: WEAKENED.** The distribution holds for Osiris. The mechanism is published, and Isis breaks the
generalisation.

**Literature.**

1. **Rilly, *Dotawo* 7, §5.1:** "in some epitaphs, the two deities Isis and Osiris ... were syntactically regarded as a
   single god, as shown by the use of a single vocative suffix for both, located after the second noun." Note 127
   cites Rilly 2007, p. 297. A phrase-final vocative is therefore published. The extension to "god + epithet" was not
   found, but it applies Rilly's principle.
2. **The epithets themselves are studied.** Otten & Anastasopoulos 2025 cite Rilly 2007 for their regional spelling:
   `q-` near Meroe and the Third Cataract, `w-` around the Second Cataract (`qetneyineqeli`/`wetneyineqeli`).
   Ferrandino & van Gerven Oei 2020 (*Sudan & Nubia* 24) cite `wetneyineqeli`/`qetneyineqeli` for Isis and
   `wettri`/`qettri` for Osiris; this was seen only in a search snippet.
3. **Not read, and the first places to check:** Rilly & de Voogt 2012, ch. on grammar, "13. The Vocative", p. 155;
   Rilly 2007, p. 297 and the chapter on the funerary formula; Heyler 1964, "L'invocation solennelle des épitaphes
   méroïtiques", *Revue d'égyptologie* 16, whose title (from a bibliography found by search) names exactly this kind of
   invocation.

**Corpus check.**

1. **Osiris holds.** `corpus_v2` has 67 rows (3,713 copies) that open with an epithet. In every family, Osiris is
   `Sori`, `Seri` or `So ri` before `wetrri`/`qetrri`, never `Soreyi`. `Soreyi` (68 tokens) never precedes an epithet.
2. **Isis breaks the generalisation.** The T0005 family (7 rows in v2; T0005 itself stands for 387 copies) opens `woSi wetNyi Nqeli Sori
   wetrri`: Isis has the vocative on her name and an epithet ending in `-i`. Millet transcribes the same opening
   (`MilletExamples.txt` l. 479: `wESi : wetNyi : Nqeli : SEri wetrri`). `funerary.md` noted this exception; it means
   the rule is not exceptionless.
3. **The stem differs.** `Sori` is not just `Soreyi` without its `-i`. The non-vocative name is `(A)sori`
   (`aSori pilqeteleb`, T0026), so `Sori` before the epithet may be the bare stem. It may also be `Sor-i`, with its own
   vocative. The corpus cannot tell these apart.
4. **The epithet is not tied to Osiris.** `qetrri` also follows `mklX` "great god" in REM 0129's benediction (T0046
   and copies: `at mXe pStrri mklX qetrri nsdokeli`). That fits a vocative "O great god ...", but it also shows the
   word is not an Osiris-only form.
5. **No `woS Soreyi` exists** in the corpus (Rilly's single-vocative pattern), so it cannot be compared here.

**Searched:** "Meroitic qetneyineqeli OR wetneyineqeli OR qetrri OR wetrri Isis Osiris epithet" (extended); "méroïtique
invocation Wos Sori épithètes Isis Osiris vocatif -i Rilly formule funéraire"; "Heyler 1964 invocation solennelle
épitaphes méroïtiques Revue d'égyptologie 16"; "Rilly La langue du royaume de Méroé vocatif -i Isis Osiris un seul
suffixe épithètes qetneyineqeli p. 297"; full text of *Dotawo* 7, Rilly 2016, Rilly 2022 (BSFE) and the Rilly & de Voogt
excerpt.

## Claim 7. `penn` is a counted time unit in datelines (numbers up to 34), not "day"

**Verdict: ALREADY PUBLISHED** (Millet 1968), and weakened by the other contexts.

**Literature.**

1. Millet 1968, as transcribed in `MilletExamples.txt`:
   1. l. 498 (pp. 367-370): `penn 5 ni` = "fifth penn; fifth year of the penn-cycle", tagged DATE.
   2. l. 519 (pp. 381/382): `penn : 34` = "regnal year 34".
   3. l. 213 (pp. 185/186): `keN 6 : Snswe(?) pennE` = "year 6, (month of) Sansawe (??), pennE".

   `funerary.md` item 15 cited only ll. 213-215 and said Millet gives no meaning. Lines 498 and 519 give one: a year
   count, which is claim 7's "counted time unit in datelines, up to 34".
2. FHN III, p. 974, reads REM 0089's closing `penn 34 nekw` differently: "an expression consisting of a numeral
   (referring to funerary offerings?)".
3. No source was found that proposed "day", so the "not day" half argues against no one.

**Corpus check.**

1. There are 32 hits of `penn*`/`ponn*`. The numerals are `5 ni`/`5ni` (the `plSn` formula and its copies), `34`/`34N`
   (REM 0089 lines, T0368, T0440, T0664), and `penno` after `keN 6 Sns(we)` (T0080, T0375, T0876).
2. Contexts where a time unit does not fit:
   1. `qeren penni li s le` (T0295, "qeren of the penni", Millet).
   2. REM 0100 `qoreñ ponni-li-se-lo`. Ashby (p. 281) renders it "qeren of Ponnili-se-lo", capitalised as a name,
      and cross-refers MI 122, "... in Pennay?".
   3. `appoye penn tewisti` (T0035).
   4. Kharamadoye, twice: `pro dole plw penn tlte br ...` (FHN III's REM 0094, ll. 13-14 and 29), where `penn` is
      followed by `tlte` (Lipiński reads `tlt` as "three"; Rilly reads "talent"), not by a numeral.

   So either `penn` is several words, or it is not only a time unit.

**Searched:** "Meroitic penn year OR day dating formula Philae graffiti regnal year Millet Meroitic Nubia 1968"; full
text of FHN III, Ashby, Griffith 1911 and the Rilly texts for `penn`, `ponni` and `penni`; Otten's Millet and Kalabsha
files.

## What was not searched or not reached

1. Persée, HAL, JSTOR and Trismegistos were not queried separately. The web searches above reach them only through the
   general index. HAL and Google Books both serve bot checks, which were not bypassed.
2. These print-only works could decide claims 1, 3, 4 and 6 and were not seen: Hofmann 1981; Hintze 1960 and 1979;
   Rilly 2007; Rilly & de Voogt 2012 beyond pp. 1-10; Pope 2008/9 and 2014; Griffith 1912, 1917 and 1937; Heyler 1964;
   Zibelius-Chen 2011.
3. FHN II and III were read from their OCR text layer. The numbers quoted (3348, 1626, 1032, 2623) should be checked on
   the page images before anyone cites them.

## Tanyidamani (REM 1044)

Adversarial check of the seven hypotheses that `tanyidamani.md` labels NEW (H3 to H8 and H11), run 2026-11-09, about
45 minutes. Same method as above: the literature searched again with other terms and sources, and the corpus checked
again (`corpus_v2`, Otten's raw `mero-corpus.txt`, and the REM texts transcribed in the Hallof samples).

### Verdicts first

| H | Claim | Verdict | Why, in one line |
|---|---|---|---|
| H3 | `pteno 3` is the total of `apette 1, sber 1, dd 1` | **WEAKENED** | `pteno` is a noun in a titulary elsewhere (REM 0088 `kroro ptenowi`); each list has a second 3 (`qore mdese 3`, `mse 3`) that 1 + 1 + 1 fits as well; 3 is 7 of the stela's 35 numerals. |
| H4 | Every `i-…-to` verb has a 1SG `i-` = `e-` | **WEAKENED** (partly published) | Rilly 2020 already reads the royal narrative verbs as 1SG and glosses the `i-` of `i-de-bx` as 1SG; Abdalla 1969 and Hallof 2020 read the prefix and `-to` otherwise; the shape occurs outside REM 1044 (REM 0075 `ipleto`, `i[p]lemketo`) and beside `y(o)-…-to` in the same text. |
| H5 | `(qes) (itnk) iXlXto` opens a campaign episode | **WEAKENED** (nearest to standing) | Not found in print, and the narrow pattern holds: `qes iXlXto` stands before the kill/take formula at l. 4 and 129, as `qes-to` does in REM 1003. But no war report follows at l. 38 and 42-43, and REM 1003 fills the slot with `qes-to`, so "verb" and "campaign" are not shown. |
| H6 | `qoleb (Amnp) (i/e)-de-bx` "I gave them (to Amun)" closes four lists | **WEAKENED** (every part published) | Abdalla 1969 (vol. I part 1, p. 74) already grouped all four verb forms; Macadam 1966 gave `d(e)` "give"; Rilly 2020 translated one clause; Hintze 1960 commented on `qoleb` at l. 26 and again on p. 156. Only two of the four name Amun. |
| H7 | `wse` "his" also in REM 1044 and 1003 | **WEAKENED** | The possessive is one of four published readings of `wse`; Millet 1973a (after Zyhlarz 1956) reads "of the country", which fits `xrpxe wse-l` "governor of the country" at least as well; four of the seven Kharamadoye tokens are route phrases (`mtr wse`). |
| H8 | `ameloloke` = `beloloke` with `a-` and m for b | **ALREADY PUBLISHED** | Rilly 2003, *Lexique méroïtique*, p. 23 ("sans doute variante archaïque de *beloloke*") and p. 58, with a phonetic account of both changes; Hofmann 1981a had already joined the two words through a prenasalised *ᵐb. |
| H11 | l. 36 returns at l. 158-161; `Xol(k)` "serve" | **WEAKENED** | The repetition itself was not found in print, but Hintze 1960 (pp. 158, 160) already read the close as a benediction, with `sedew` "abundant", and discussed `ẖol` there; `qes (li) ẖol(i)t(e)ke seb` also stands twice in REM 1003, so the shared run is a royal formula, not a frame peculiar to this stela; FHN II reads `molk`, not `ẖolk`, at l. 36. |

None of the seven stands as a clean new finding. The nearest are H5 in its narrow form (Kush + `iXlXto` directly before
the kill/take formula, twice) and the bare repetition in H11.

### Sources used in this run

New this run:

1. Rilly 2003, thesis vol. II, [*Lexique méroïtique*](https://hal.science/tel-04793700) (HAL tel-04793700). About 800
   words, each with the views published to 2003 and a full bibliography. It is an image-only scan of 304 pages; the
   entries cited below were read from rendered page images (printed page = PDF page minus 1 or 2). This source decided
   H8 and most of H6, H7 and H11. The HAL search API found it; the earlier runs had only vol. I.
2. Hallof 2024, *Analytisches Wörterbuch des Meroitischen* 7: *Dokumente*,
   [publisher's sample](https://www.lehmanns.ch/media/116874085): transcriptions of REM 0075 (p. 12) and REM 0088
   (p. 15).

Read again, from the local copies made earlier this session: FHN II pp. 665-671 (REM 1044) and 720-722 (REM 1003);
FHN III on REM 0094; Abdalla 1969, vols. I-II (OCR, searched with hyphen-tolerant patterns, since he writes
`i-de-b-x`); Rilly 2020 (*Dotawo* 7); Hallof 2020 and the Hallof 2022 sample; Griffith 1917 (JEA 4); Millet's glosses
(`MilletExamples.txt`, `Kalabsha_Millet.txt`); `LobbanVocabList.txt`.

Web searches run (none found a new publication): "ameloloke" Meroitic; "qoleb" Meroitic Tanyidamani "de-b" give Amun;
"pteno" OR "apette" Meroitic stela list numerals Tanyidamani; Meroitic "ihlhto" OR "iḫlḫto" OR "iẖlẖto" OR "ihlhte";
Meroitic "sedew" OR "eqetxe" OR "eqethe" Tanyidamani verso; stèle de Taneyidamani méroïtique traduction qoleb
"Amanap"; Hintze 1960 "Die meroitische Stele des Königs Tanyidamani" Kush 8 Formel Segensformel; Meroitic royal
inscription Taneyidamani first person prefix "i-" "e-" Hallof Rilly; Rilly 2003 thèse "Lexique" HAL; the HAL API for
Rilly's titles on Meroitic.

### H3. `pteno 3` is a total placed before its items

**Verdict: WEAKENED.** No publication was found, but the arithmetic that carries it is weak, and a new attestation
points the other way.

**Literature.** Nothing found. FHN II comments on l. 17 (`wte mrosi`) and l. 24-25 (`ssime`, `Imlotror`), not on
l. 18-23. Abdalla 1969 has no `pteno` or `apette`. Rilly's *Lexique* has no entry for either word: *Apedemk* is
followed by *apḫoletri* and *apote* (pp. 30-31), and *pso* by *Ptrme* (p. 178). So none of the roughly 300
publications Rilly surveyed to 2003 seems to have glossed them.

**Corpus check.**

1. `pteno` occurs outside REM 1044. Hallof's transcription of REM 0088 (rock inscription of Tayesi at Medik; Griffith
   1912, pp. 17-18), l. 4, reads `pelmo(4)s: yetmdelowi: kroro: ptenowi:`. In a funerary titulary, `pteno-wi` is a
   noun with the copula, next to the title `kroro`: a title or part of one. REM 0088 is in neither `corpus_v2` nor
   Otten's raw file, and the reading was not checked on Griffith's plate. If it is the same word, `pteno 3` counts
   three persons, as `qore mdese 3`, `mse 3`, `wtotrse 3` and `Amnise 3` do in the same section, and with `apette`
   (compare `apote` "envoy") the list is one of personnel. Then `pteno 3` is an item, not a total.
2. Each list has two 3s before the three 1s: `qore mdese 3 ti mXe pteno 3 apette 1 sber 1 dd 1` and
   `nmrolde s qorese mse 3 ti mXe (pteno) 3 apette 1 sber 1 dd 1`. The sum 1 + 1 + 1 = 3 fits the recipients' 3 as
   well as `pteno 3`.
3. 3 is the stela's commonest numeral after 1: 7 of 35 (`qore mdese 3`, `pteno 3` twice, `mse 3` twice, `wtotrse 3`,
   `Amnise 3`). A 3 next to three 1s is unremarkable, so the sum test carries little weight. The second list's `pteno`
   is restored (FHN `(pteno)`), so the parallel is one reading plus one restoration.

**Searched:** the web query above; Rilly's *Lexique*, a- and p-sections; full text of FHN II, Abdalla 1969
(`pte-no`, `a-pe-tte`, `s-ber`), Rilly 2020 and the Hallof samples (which gave REM 0088).

**What would settle it:** Griffith 1912, pls. VIII-IX, for `ptenowi` in REM 0088; Hintze 1960 on l. 17-23; Hallof's
dictionary entries for `apette` and `pteno` (not in the samples).

### H4. Every `i-…-to` verb has the 1st-person prefix

**Verdict: WEAKENED, and partly ALREADY PUBLISHED.**

**Literature.**

1. Rilly 2020, §4.3, concludes "that the verbs in the narratives of the royal inscriptions are in the first person
   singular", and ex. 8 glosses `i-de-bx` as "1sg.s-give(?)", with the prefix `i-`. The 1SG reading of REM 1044's
   narrative verbs, one `i-` form included, is therefore his; H4 extends it from one `i-` verb to sixteen. Rilly also
   writes that the prefix "is spelled e- everywhere" in REM 1044, so he did not state `i-` = `e-` beyond ex. 8.
2. Against it, in print: Abdalla 1969 (vol. I part 2, pp. 109-110) takes `y(e)-` and `i-` as interchangeable prefixes
   with no person value. Hallof 2020 (pp. 15 and 20) reads `-to` in `elto` (REM 1141) as "the pronoun 3rd person
   plural" and lists `e-`, `i-`, `y-` as prefixes of royal inscriptions without a person value. Rilly 2003 (*Lexique*,
   p. 79, s.v. *e-*) still took `e-` for a benediction prefix, so the 1SG reading dates from 2020.

**Corpus check.**

1. The shape is not confined to REM 1044 once the wider REM corpus is counted. REM 0075, an archaic Isis statue with
   an *aleqese* inscription from Gebel Barkal (Hallof 2024, p. 12), has `ipleto` (as REM 1044 l. 50) and
   `i[p]lemketo`. Hallof 2020 adds `yplt` (REM 1367/1, p. 15 n. 27) and `ytepleto` (REM 1141, p. 20). In `corpus_v2`
   itself, Kharamadoye has `ytpoto` and `ywito`, and the funerary rows have `yinitxebto` (4 times). The argument
   "absent elsewhere, as the 1st-person narrative is" holds only inside `corpus_v2`.
2. REM 1044 has the same shape with `y(o)-`: `yonpxto` (l. 34), `yotkto` (l. 48, Abdalla's `ye-tk-te`), `ynkteketo`
   (l. 49) and `yoto` (3 times), and a prefixless `tk-to` (l. 151). H4 makes `i-` a second spelling of `e-` and
   leaves `y(o)-` unexplained.
3. H4's own test: a noun phrase stands directly before the verb in `Amnp atoo lX itwdto` (l. 33), `Amnpte attomi
   itwdto` (l. 118-119), `Amni-l de [..] ipxto` (l. 112-113) and `Amnp kek Sor sberxi ipleto` (l. 49-50). If Amun is
   the subject in any of them, H4 fails; the corpus cannot tell subject from object here.

**Searched:** the web query on first-person prefixes above; Rilly 2020, §§2-4.3 and Table 2; Hallof 2020, pp. 15-20;
Abdalla 1969; Rilly's *Lexique*, s.v. *e-* and the i-section; the regex `(i|y|ye|yi)[a-zA-Z]+to` over `corpus_v2`.

**What would settle it:** an `i-…-to` clause whose subject is fixed by context; Rilly 2007 on the verbal prefixes.

### H5. `(qes) (itnk) iXlXto` opens a campaign episode

**Verdict: WEAKENED.** It is the nearest to standing: in its narrow form it holds and was not found in print.

**Literature.** Nothing was found on `iḫlḫto` as an opener. Rilly 2020, ex. 35, starts at `abr-se-l` and leaves
`qes iḫlḫto` aside. FHN II (p. 669) only lists the lines with Qes. Hallof 2020 (p. 16 n. 35) cites `itnk[i]hlhto`
for its word division only. Rilly's *Lexique* has no entry for it (its i-section, pp. 95-96, has *-i* (1)-(4),
*-id(e)*, *Indo*, *Iphe*, *ireqe*, *itebereke*, *-iwl*). Two points come close:

1. FHN II (p. 722) already reads a REM 1003 sentence with `qes arme-yose-li` (l. 2-3) as the opening of a war
   narrative. "A Kush sentence opens the war report" is therefore in print for REM 1003.
2. Hallof's dictionary (2022 sample, s.v. *ayotepe[te]bede*) reads REM 1044D/96-97 as `... tmte⁝ qes[l] ihl---`,
   where FHN II and Otten have `qes lḫ-l` (l. 102-103). That would be a fifth `qes ... iḫl[ḫto]`, without the
   kill/take formula after it, and it shows that Hallof's dictionary catalogues the form; its i-entry was not seen.

**Corpus check.**

1. `iXlXto` occurs 4 times, only in this stela: `tqN-l qes iXlXto abrse-l e-ked` (l. 4), `qes iXlXto tqN-l abrse-l
   e-ked-td` (l. 129), `itnkk iXlXto seb-l ed kete` (l. 38) and `qes itnk iXlXto seb-l ed kete` (l. 42-43). The count
   holds.
2. Only l. 4 and l. 129 lead into the kill/take formula. At l. 38 and 42-43 the untranslated `seb-l ed kete kek ...
   wkete` follows. "Campaign episode" is shown for two of the four.
3. REM 1003 supports the narrow pattern and undercuts "verb": `qes to abrse-l yekedi` (row `hamadab`, token 29),
   `qesto alle leb aberse-l yeked` (token 150) and `qes npt aro bel abrse-l yekedi` (token 85). There the slot after
   Kush is filled by `-to`, usually read as a locative ending, so `iXlXto` could as well be an adverbial or locative
   form. Nothing in the corpus shows that it is a verb.

**Searched:** the web query on `ihlhto` above; Abdalla 1969 (OCR patterns `i-h-l-h`, `x-l-x`, "Tan 4", "Tan 129");
Rilly 2020, ex. 35 and Table 2; Hallof 2020 and 2022; Rilly's *Lexique*, i-section; the contexts of `qes` in REM 1003.

**What would settle it:** Hintze 1960 on l. 4 and 129; Hallof's dictionary entry for `iḫlḫto`; the stone at
l. 102-103.

### H6. `qoleb (Amnp/Amnpte) (i/e)-de-bx(i)` "I gave(?) them (to Amun)" closes four lists or episodes

**Verdict: WEAKENED.** Every component is in print. The synthesis as a closing formula was not found, and its evidence
is thinner than stated.

**Literature.**

1. **Abdalla 1969, vol. I part 1, p. 74** (A2 II i), already groups all four verbs: "The same verb, prefixless or
   prefixed with i(e)-, used with the plural dative in the verbal complexes i-de-b-x: Tan 27, i-de-b-xi: Tan 126,
   e-de-b-x: Tan 137, de-b-x: Tan 115-116". `tanyidamani.md` cites p. 43, which treats `ke-de-b-x`; there Abdalla also
   derives `e-ke-d` "kill" (Tan 5) from the same verb `-d(e)-`.
2. **"Give" is Macadam's.** Rilly 2003, *Lexique*, p. 67, s.v. *d* (var. *de*): a verb of benediction formulae B and C
   "et les textes historiques"; Zyhlarz translated "envoyer", Macadam (1966, p. 60) "donner (?)", Priese "produire".
3. **The pronoun and its clauses were discussed.** Rilly 2003, *Lexique*, p. 187, s.v. *qoleb*, lists eight REM 1044
   lines (2, 26, 32, 34, 115, 125, 136, 148) and cites Hintze 1960a, pp. 148 and 156. Hintze commented on `qoleb` at
   l. 26 (FHN II, p. 670: "Hintze 1960, 148 ad line 26") and again on p. 156, which by its place in the edition covers
   the lines around l. 115-126, probably one of the other clauses. That page was not seen.
4. Rilly 2020, ex. 8 and n. 26, translates l. 25-26 "I gave(?) them to Amanap" and notes that `qoleb` "is particularly
   attested in royal chronicles". Griffith 1917 (p. 167; FHN II, p. 722) built his gloss "living persons" on `qo leb`
   standing after counts of men and women in REM 1003.

**Corpus check.**

1. The four clauses are there (row `tanyidamani`, tokens 171, 560, 591 and 637).
2. Only two name Amun (l. 26 `Amnp`, l. 125-126 `Amnpte`); `qoleb de-bx` (l. 115-116) and `qoleb e-de-bx`
   (l. 136-137) name no recipient. "To Amun" is an inference for half of them.
3. "Closes" is partly circular: the section ends of S6, S14 and S15 were drawn at these clauses, and l. 136-137 sits
   inside the narrative, with killings before and after it (l. 129-155).
4. `qoleb` + verb is the stela's general pronoun-object construction: `qoleb elbto` (l. 32-33), `qoleb ...
   w-kb-bx-te` (l. 68-70), `qoleb troXe-li` (l. 94), `qoleb axro ... e-ked-b-to` "I killed them" (l. 148-150). In
   REM 1003 `qo leb` follows `abr N kdi N` three times (`abr 32 kdi 135 qo leb yedxi`, `abr 100 kdi 100 qo leb
   apotebese tkk`, `abr 58 kdi 223 qo leb apote qebese yetkbxk`). Standing after a list is a property of the pronoun;
   the `de-bx` clauses are 4 of its 8 uses in this stela.
5. The stela's own hieroglyphic caption (REM 1044A) uses `l-` for "give" (`lxte`; Rilly 2020, note on REM 0003-0004),
   so "give" for `de` on the same monument stays a guess, as Rilly's "(?)" says.

**Searched:** the two web queries on `qoleb` above; Rilly's *Lexique*, s.v. *d*, *qoleb*, *-bḫ-*; Abdalla 1969,
vol. I part 1, pp. 43 and 74; Rilly 2020, §3.1; FHN II, pp. 670 and 722; Griffith 1917; `qo leb` contexts in
`corpus_v2`.

**What would settle it:** Hintze 1960, pp. 148 and 156.

### H7. `wse` "his/her" also in REM 1044 (`adb wse-li`) and REM 1003 (`xrpxe wse-l`)

**Verdict: WEAKENED.** The extension was not found in print, but the possessive is one of four published readings,
and the corpus pattern cited for it fits the others equally.

**Literature.** Rilly 2003, *Lexique*, p. 261, s.v. *wse*, collects the readings:

1. Griffith 1912: a simple noun, plural `wteb` (= `wse-leb`, REM 0094/23).
2. Millet 1973a (pp. 43-47), after Zyhlarz 1956: the genitive of a noun *w "country": `ado wse` "fortress (?) of the
   country", `mte wse` "child of the country", `mtr wse` "frontier (?) of the country", `qore 8 ẖrese wse-leb` "the
   eight kings of the North of the country". Rilly adds that `wse` could be a variant of `wte`. Hallof 2022 (sample,
   s.v. *ayeke*) still renders `mte wse` "child of the country".
3. For `mtr wse`, FHN III (REM 0094, comment on l. 21 f.) gives "Kushwards to Adere, northwards to Philae", and
   Lobban's list (`LobbanVocabList.txt` l. 192) "witness; testimony?".
4. The possessive: Millet 2003 (via F&vGO, p. 297) and Rilly 2020, §4.5 (`semle w-si` "his wife", `ste wese` "his
   mother"). F&vGO (n. 26): perhaps a noun.

With Millet's reading, REM 1003's `xrpxe wse-l` is "the governor of the country", as natural as "his governor"
(compare `pelmos adblise` "general of the land").

**Corpus check.**

1. The count holds: 10 tokens in `corpus_v2` (REM 1044 once, REM 1003 twice, Kharamadoye 7 times), each after a
   noun. That fits any genitive or postposition, so it does not favour "his".
2. Four of the seven Kharamadoye tokens are `mtr wse` in the route phrases that FHN III reads as directions. Rilly's
   own possessive examples (`semle wsi`, `ste wese`) are spellings H7 did not count.
3. H7's own test (`wse` after `wide` or `ste` in REM 1003 or 1044) finds nothing.

**Searched:** Rilly's *Lexique*, s.v. *wse*; FHN III on REM 0094; Millet's glosses (`Kalabsha_Millet.txt` has `ws`,
and Millet 1968 renders `smle wSi` as a name or word "waSi"); Lobban's list; the Hallof 2022 sample; Rilly 2020,
§4.5; F&vGO; FHN II on REM 1003 (no comment on `wse`).

**What would settle it:** a `wse` after a kinship term in a royal text; Hallof's dictionary entry for `wse`.

### H8. `ameloloke` is the priestly title `beloloke` with `a-` and m for b

**Verdict: ALREADY PUBLISHED.**

**Literature.**

1. Rilly 2003, *Lexique*, p. 23, s.v. *ameloloke*: "titre en REM 1044/24, sans doute variante archaïque de
   *beloloke*". Bibliography: Hintze 1960a, p. 147; Millet 1973c, p. 312; Hofmann 1979, p. 34; Hofmann 1980a, p. 275;
   FHN II, p. 670.
2. Rilly 2003, *Lexique*, p. 58, s.v. *beloloke* (var. *beliloke*, arch. *ameloloke*): the archaic form "se serait
   prononcée [əm(ə)luluk(ə)] jusqu'à la chute des schwas", with [-ml-] later becoming [-bl-] (compare Greek βροτός
   < *μρότος); "Il n'est donc pas nécessaire d'envisager ici de prénasalisée *ᵐb, comme le propose Hofmann 1981a."
   Hofmann 1981a had therefore already joined the two words, and Rilly explains both the initial vowel and the m/b.
3. Millet 1968 lists `amelElEkes` (`ameloloke-s`) on p. 182 (`MilletExamples.txt` l. 857), without a gloss in
   Otten's transcription.

**Corpus check.** `ameloloke` occurs only in REM 1044 (l. 24 and 108-109), both times among temple personnel, as
stated. The label in `tanyidamani.md` should be PUBLISHED HYPOTHESIS (Hofmann 1981a; Rilly 2003).

**Searched:** "ameloloke" Meroitic (web); Rilly's *Lexique*, s.v. *ameloloke*, *beliloke*, *beloloke*; Abdalla 1969
(OCR, no hit); Millet's glosses; `corpus_v2` and the raw file.

### H11. The verso is framed (l. 36 returns at l. 158-161), and `Xol(k)` may be "serve"

**Verdict: WEAKENED.** The repetition itself was not found stated, but both readings it rests on are Hintze's, and the
shared run is a formula that REM 1003 has too.

**Literature.**

1. Rilly 2003, *Lexique*, p. 203, s.v. *sedew*: "adjectif en REM 1044/159 à valeur positive, dans une bénédiction
   finale. Hintze, exploitant un parallèle évident avec *mhe* dans les formules de bénédictions funéraires, propose un
   sens 'abondant'." Bibliography: Hintze 1960a, p. 160; Trigger-Heyler 1970; Meeks 1973; Bender 1981a-b; Hofmann
   1982a. The entry also cites an anthroponym `Sedew-li` (REM 1063/7), so `sedew` is not confined to this stela.
2. Rilly 2003, *Lexique*, p. 92, s.v. *ẖol*: the verb of benedictions C, C', D and E, "accorder" or "procurer" after
   Griffith. Its bibliography cites Hintze 1960a, pp. 158 and 160, the edition's pages on the last lines (about
   l. 146-161). Hintze therefore discussed `ẖol` in this stela's close; what he said was not seen.
3. The *sedew* entry lists only REM 1044/159, not l. 36, which suggests that none of the works Rilly surveyed noted
   the repetition. That part may be new. The *Lexique* has no entry for `molk` (m-section, pp. 139-142).

**Corpus check.**

1. The run holds: l. 36 `sedew tbe tXe lw qes molk seb eqetxe`, l. 158-161 `ato sedew ato mlo qes Xol k seb eqetx`.
2. `qes (li) ẖol(i)t(e)ke seb` also stands twice in REM 1003, inside a paragraph that itself repeats: FHN II l. 22
   (p. 720) `qes li„ holitke„ seb„ seb lhe„ eno wite` and l. 32 (p. 721) `qes li„ holiteke„ seb„ seb lh„ eno wite`
   (row `hamadab`, tokens 263 and 380). "Kush + ẖol-…-k(e) + seb" is thus a formula of two royal texts, and its return
   at l. 36 and l. 160 is weak evidence of a deliberate frame.
3. FHN II prints `molk` at l. 36 with no doubt mark, against `hol k` at l. 160. The funerary verb is spelled with ẖ
   (`Xolketes`, `Xolkte` in T0046 and its copies, T0113), which matches l. 160 only. The "serve" reading reaches l. 36
   only if the stone has ẖ there.
4. `eqetxe` has parallels outside the stela: REM 1003 `eqetxN`, and REM 0075 `eqetḫno` (Hallof 2024, p. 12).

**Searched:** the web queries on `sedew` and on Hintze's *Segensformel* above; Rilly's *Lexique*, s.v. *sedew*,
*ẖol* and the m-section; FHN II, pp. 669-671 and 720-721; `sedew`, `Xol*`, `[mXx]olk` and `eqet[xX]*` in
`corpus_v2`.

**What would settle it:** the stone or Hintze's facsimile at l. 36; Hintze 1960, pp. 158-160.

### What this means for `tanyidamani.md`

1. H8 becomes PUBLISHED HYPOTHESIS (Hofmann 1981a; Rilly 2003, *Lexique*, pp. 23 and 58).
2. H3 to H7 and H11 stay hypotheses, each with the points above, but none is cleanly NEW. The line in section 1,
   "Seven hypotheses remain NEW", no longer holds.
3. Three statements in the gloss hold only inside `corpus_v2`: `kek` "nowhere else" (REM 0075 has `kek`, Hallof 2024,
   p. 12); `sedew` "nowhere else" (REM 1063/7 has `Sedew-li`); the `i-…-to` shape "in no other text" (REM 0075 has
   `ipleto` and `i[p]lemketo`).
4. The Abdalla page for the four `de-b-x` forms is vol. I part 1, p. 74; p. 43 is about `ke-de-b-x`.
5. Rilly's *Lexique* (HAL tel-04793700) should be the first source checked for any future "NEW" claim on REM 1044: it
   covers about 800 words with the views published to 2003.

### Not reached

1. Hintze 1960a (*Kush* 8: 125-162), the edition, is still the main gap. Rilly's bibliographies show that it
   discussed `ameloloke` (p. 147), `qoleb` (pp. 148, 156), `ẖol` (pp. 158, 160) and `sedew` (p. 160).
2. Hofmann 1981a; Rilly 2007; Millet 1973a and 1973c; Hallof's dictionary beyond the samples; Griffith 1912's plates
   of REM 0088.
3. Rilly's thesis vol. I (grammar), on HAL as an image scan, was not searched for the `i-` prefix.
