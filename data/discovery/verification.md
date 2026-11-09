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
