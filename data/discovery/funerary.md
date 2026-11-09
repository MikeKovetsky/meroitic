# Funerary corpus: the 30 most frequent unglossed words and pieces

Task D2, run on 2026-11-08 (night). Inputs:

- `data/corpus.jsonl`: 1,019 rows with src "funerary".
- `data/gold_lexicon.json`: re-read at the end of the run. It had 82 entries (md5 `ea5f50ff…`); it had 66 when the run started.
- `src/kwic.py`.

`data/gold_morphology.json` does not exist in the repo, so no bound morpheme counts as glossed by gold.

## Bottom line

**Labels across the 30 items:**

| Label | Count | Items |
|---|---|---|
| ESTABLISHED | 8 | 1–6, 8, 9 |
| PUBLISHED HYPOTHESIS | 19 | 7, 10–13, 15–17, 19–24, 26–30 |
| NEW | 3 | 14, 18, 25 |

Two NEW proposals also sit inside published items: the etymology of plSn (item 26) and the reading of penn (item 15).

**The corpus is still padded.**
- Otten's name-swap augmentation survives in two forms: 17 multi-word names and 5 "second words" of two-word names slipped the NAME mask (section C).
- After masking them and merging near-duplicates, the 1,019 funerary rows are 442 distinct texts in 306 families.
- Raw counts are dominated by copies. womnitX (441 raw tokens), aribet (400), ateqi (348) and beloloke (262) come almost entirely from one inscription that sits in the file 86 to 105 times.

**What the frequent unglossed material is:**
- Most of it is the grammar of the formula: determiner, copula, genitive, locative, plural and the benediction verb. Rilly has published all of these.
- Below that come titles and list words. Millet's 1968 dissertation glossed them tentatively, and Otten's own data file `data/otten/Data/MilletExamples.txt` reproduces those glosses.
- **Lead for the project:** that file has not been used by the gold lexicon so far. It is the quickest published source for half of this list.

**Strictness.**
- "ESTABLISHED" means published and not disputed in the sources read.
- "PUBLISHED HYPOTHESIS" covers both Rilly's firm-but-single-author readings and Millet's queried glosses.
- "NEW" means no published proposal was found in the searches listed under that item. Rilly 2007, Hintze 1979, Rilly & de Voogt 2012 (grammar chapter) and FHN were not searchable online. A specialist should check NEW items there first.

## A. How the counts were made

**1. Mask the slipped names.**
- Replace each multi-word string that alternates with NAME inside near-duplicate texts by NAME. There are 17 of them, listed in section C1.
- Collapse "NAME + tail" to NAME, where the tail is mokelowi, kroro, mXewitr, Smedeli or "mete l".

**2. Drop exact duplicates.** 1,019 rows become 442 texts.

**3. Merge near-duplicates into families.**
- Two texts join one family when 60% or more of the shorter one's word trigrams also occur in the other.
- This gives 306 families. For each family, the member closest to all the others (the medoid) is kept.

**4. Count.**
- "fam" is the number of families containing the item.
- "tok" is the number of tokens in the kept members.
- "raw" is `python3 src/kwic.py PATTERN --re --src funerary --max 0` on the uncleaned file. It is shown only to expose the inflation.

**5. What the ranking excludes.**
- Gold forms and their spelling variants.
- NAME, RNAME and digits.
- Single-letter splinters of split words (see section D).
- Items that the gold lexicon gained during the run. Those are listed in D.
- The ranking is by fam.

**6. Formula slots** follow the standard epitaph:
- invocation (woSi Soreyi);
- nomination (qo NAME qowi);
- filiation (NAME tedxelowi, NAME terikelowi);
- relationship and career (titles, kin terms, places);
- benedictions (ato mXe …, at mXe …).

Many "funerary" rows are not epitaphs: Philae graffiti, lists, and royal narrative lines (C4).

**7. Reproducing the contexts.**
- `src/kwic.py` gives every raw context, duplicates included. Example: `python3 src/kwic.py '.*lowi' --re --src funerary --max 3000`.
- The family-level contexts below cite the family's kept row id.

## B. The 30 items

Spelling: o = o, x = ḫ, X = ẖ, S = š, N = ñ. The hyphens below are my segmentation; the file spaces them inconsistently.

The "Proposed meaning or function" column gives my reading, with its confidence (1 to 5) in brackets. The published view is in the item notes.

| # | Item (forms) | fam | tok | raw | Slot | Proposed meaning or function (confidence) | Label |
|---|---|---|---|---|---|---|---|
| 1 | lo / -lo, clause-final | 80 | 104 | 499 | relationship, filiation | determiner -l + copula -o, "is (a/the)" (5) | ESTABLISHED |
| 2 | -li / li | 72 | 170 | 1076 | filiation, titles, places | singular article, the -l variant used before more suffixes (4) | ESTABLISHED |
| 3 | -lowi (also "lo wi") | 68 | 177 | 2361 | filiation, relationship | -l-o-wi: article + copula + particle (5) | ESTABLISHED |
| 4 | -s / -se / -lis | 67 | 110 | 364 | titles ("X of Y"), lists | genitive "of" (5) | ESTABLISHED |
| 5 | -te / -teli / -tel | 51 | 74 | 250 | titles + place, Philae graffiti | locative "in, at" (5) | ESTABLISHED |
| 6 | -leb / leb | 39 | 83 | 244 | relationship (plural possessors), graffiti | plural article -l-b (5) | ESTABLISHED |
| 7 | wi, a separate word after lo | 36 | 67 | 333 | end of relationship and nomination clauses | clause-final particle after the copula, so-called "emphatic" (position 5, function 2) | PUBLISHED HYPOTHESIS |
| 8 | l, a separate word | 27 | 127 | 1165 | titles + place, lists, graffiti | singular article and phrase boundary (5) | ESTABLISHED |
| 9 | benediction verb endings -x(e)/-bx(e), -k(e)te, -kes | 25 | 46 | 262 | benedictions | -x/-bx singular/plural beneficiary; -k(e) 2nd person plural; -te optative (4) | ESTABLISHED (mood debated) |
| 10 | -lw / lw | 24 (lw alone 11) | 43 (lw 26) | 37 (lw) | lists, benedictions | article + objective -w (2) | PUBLISHED HYPOTHESIS |
| 11 | ye, a separate piece | 20 | 24 | 2140* | relationship (ye t mde), graffiti | eroded yet- "person" in kin terms, or a verbal prefix (2) | PUBLISHED HYPOTHESIS |
| 12 | benediction prefix p(i)S- / pso- / bS- | 18 | 27 | 207 | benedictions | verbal prefix, causative or optative (3) | PUBLISHED HYPOTHESIS |
| 13 | (a)qe-bes(e) "bes" | 12 | 12 | 18 | end of relationship clause | 3rd person plural possessive "their" (4) | PUBLISHED HYPOTHESIS |
| 14 | wetrri / qetrri | 11 | 13 | 88 | invocation, after Osiris | an epithet of Osiris that takes the vocative -i at its end (structure 3, meaning ?) | NEW |
| 15 | penn (penno, penni) | 11 | 12 | 41 | graffiti datelines | a counted, dated term (2) | PUBLISHED HYPOTHESIS (+ NEW reading) |
| 16 | temey (temey-lX, temey-kdi) | 10 | 18 | 161 | career titles; Kalabsha lists | a class of persons, with a "great/chief" rank (2) | PUBLISHED HYPOTHESIS |
| 17 | keN (ken) | 10 | 16 | 36 | dates and counted lists | "year" in datelines (3) | PUBLISHED HYPOTHESIS |
| 18 | wetNyiNqeli / qetNyinqeli | 9 | 10 | 76 | invocation, after Isis | an epithet of Isis that takes the vocative -i at its end (structure 3, meaning ?) | NEW |
| 19 | ke, a separate piece | 8 | 20 | 265* | benediction verbs; lists | in verbs, 2nd person plural -k(e) (4); elsewhere unclear (1) | PUBLISHED HYPOTHESIS |
| 20 | tros | 8 | 9 | 16 | relationship clauses | a kin term ("parent"?) (2) | PUBLISHED HYPOTHESIS |
| 21 | ni, after numerals | 8 | 9 | 38* | dates and counts | ordinal or numeral suffix (3) | PUBLISHED HYPOTHESIS |
| 22 | mde | 7 | 8 | 16 | relationship (ye-t-mde) | "mother's kin", the second part of yetmde (3) | PUBLISHED HYPOTHESIS |
| 23 | Sq- (Sqe-, Sq kdi) | 7 | 7 | 35 | relationship; Kalabsha lists | an ethnic or class term, "Saqa people" (2) | PUBLISHED HYPOTHESIS |
| 24 | tlt | 5 | 5 | 20 | counted lists | a unit, "talent", or "three" (2) | PUBLISHED HYPOTHESIS |
| 25 | teketi | 4 | 5 | 36 | counted lists next to nbr "gold" and tlt | a counted commodity or unit (1) | NEW |
| 26 | plSn / plsn | 4 | 4 | 45 | opens graffiti before a name | a temple title, "high priest" (2), from Egyptian pꜣ mr-šn "the lesonis" (NEW, 2) | PUBLISHED HYPOTHESIS (+ NEW etymology) |
| 27 | SlXS | 4 | 4 | 23 | opens short texts before a name | a title, meaning unknown (title 3, meaning 1) | PUBLISHED HYPOTHESIS |
| 28 | SSimete | 4 | 4 | 16 | career titles | title, "steward" (2) | PUBLISHED HYPOTHESIS |
| 29 | Stmdes | 4 | 4 | 7 | career and relationship | kin-title "kinsman (of the viceroy)", built on mde (3) | PUBLISHED HYPOTHESIS |
| 30 | dbre (dbre-te) | 3 | 6 | 50 | career, place of office | a place name, "in Dbre" (3) | PUBLISHED HYPOTHESIS |

\* The raw count for a short piece also catches unrelated tokens of the same shape. ye, ke and ni are mostly augmentation and name residue in the raw file; the fam and tok columns are the real figures.

Sources used below, with short keys:

- **[R16]** Rilly 2016, "Meroitic", UCLA Encyclopedia of Egyptology: <https://escholarship.org/content/qt3128r3sw/qt3128r3sw.pdf> (printed page numbers).
- **[RD]** Rilly, "Personal Markers and Verbal Number in Meroitic", *Dotawo* 7 (2020/21), DOI 10.5070/D67052246: <https://pages.sandpoints.org/dotawo/article/rilly>. Also at <https://journalpub.escholarship.org/dotawo/article/53835/galley/40735/download>.
- **[L11]** Lipiński 2011, review of Rilly 2010, *Rocznik Orientalistyczny* 64/2, pp. 87–104: <https://repozytorium.uni.lodz.pl/xmlui/bitstream/handle/11089/4031/No_2_2011.87-104.pdf>.
- **[G11]** Griffith 1911, *Karanòg*: <https://archive.org/details/karangmeroitic00grifuoft>.
- **[M68]** Millet 1968, *Meroitic Nubia* (PhD thesis, Yale). I used his translated examples as transcribed in Otten's corpus: <https://github.com/Joshua-Otten/Meroitic-Corpus/blob/main/Data/MilletExamples.txt>. Line numbers refer to that file; page numbers are Millet's, from the file's "# pg." headers. I read Millet only through this transcription, not the thesis.

Literature checks were run by me and by two research subagents. The reports name the searches; they are repeated here only for the NEW items.

### Grammar pieces (items 1–13, 19, 21)

**1. lo / -lo**
- **Contexts:**
  - "NAME yet mde lo wi" (T0040)
  - "pqr l yet mde lo wi" (T0093)
  - "kdite lo wi" (T0612, T0017)
  - "ye t mde aqe bes lo" (T0316, T1002)
  - "Ste bes lo" (T0365)
  - "ni ye teke lo" (T0025)
  - "qore ydke mlolo" (T0986)
  - "x mlo l … pso-Xe-kete" (Rilly's examples in Otten's `RillyExamples.txt`)
- **Slot:** the predicate of every relationship clause and some filiation clauses. With wi in about half the families (item 7), and alone in the rest.
- **Co-occurs with:** kin terms (kdite, Ste, yetmde), bese (item 13) and titles.
- **Published:** [R16] p. 8 gives -l (determiner) + -o (copula, singular); -wi is optional ("ktke-l-o 'she is the Candace'"). [RD] §3.1 has the same; Hintze had copula -o ± particle -wi, as reported by Rilly.
- **Not found:** a dating or regional explanation of when -wi is dropped. I see no split in this corpus either: lo and lowi occur in the same texts (T0016, T0026).
- **Label:** ESTABLISHED.

**2. -li**
- **Contexts:**
  - "NAME tedxeli tedxelowi" (T0015, T0083)
  - "terikeli terike lowi" (T0083)
  - "Steli", "mteli" (T0006)
  - "pilqe te li", "tebwe te li s li wi" (T0016)
  - "pesto-li-s", "adb-li-s" (T0017)
  - "tros li Xi qore mXo li s l" (T0382)
- **Slot:** the first half of the doubled filiation verb (tedxeli tedxelowi); before -se and -te in titles.
- **Published:** [R16] p. 7 gives the singular article "-l or -li"; plural -leb. In te-dxe-l / t-erike-l the article "has a nominalizing role" ([RD] §4.3).
- **My addition, not published:** the doubled "tedxeli tedxelowi" (4 families) looks like a nominal (-li) form followed by the predicate (-lowi), "the one born … , she bore (her)".
- **Not found:** what chooses -li over -l.
- **Label:** ESTABLISHED.

**3. -lowi**
- **Contexts:** yetmde-lowi (20 families), terike-lowi (13), tedxe-lowi (6), qo-wi, smlowi, Stelowi, mdetowi, aqebetowi. Also split: "yetmdelo wi" (T0014), "terik elowi" (T0059).
- **Slot:** the end of every filiation and relationship clause.
- **Published:** [R16] p. 8: -l-o-wi is determiner + copula + "emphatic" particle; "apote-l-o-wi 'he was an envoy'". The past tense comes from context only.
- **Label:** ESTABLISHED.

**4. -s / -se / -lis**
- **Contexts:**
  - "pelmoS adb-li-s" (T0017; general of the land)
  - "nbr-lis 1" (T0021, in a list)
  - "Stmdes peste-lis RNAME" (T0083)
  - "SSimete kdke li s" (T0981)
  - "qore s" (T0016)
  - "polmoS s ye ye yetmdelowi" (T0013)
  - "SlXS mnp s l sm lo" (T0644)
- **Slot:** inside titles (office + of + institution) in the career section.
- **Published:** [R16] p. 7: -se is the second, alienable genitive, after the article (mk-li-se); [L11] p. 99 agrees; [G11] already had a "genitive termination". Homonyms to watch are -se "each" (Rilly 2010 p. 138 per [L11]) and the verbal particle -se (item 9).
- **Label:** ESTABLISHED.

**5. -te / -teli**
- **Contexts:**
  - "xrpxN pXrs te (l)" (T0612, T0012)
  - "woS pilqe te l … woS tebwe te l" (T0016, T0334)
  - "aSori tebwe te li" (T0016)
  - "temeylX dbrete" (T0059)
  - "Stmdes teN te" (T0306)
- **Slot:** the place of office in career titles; the place of a god in Philae graffiti.
- **Published:** [R16] p. 8: locative, Bedewi-te "in Meroe", and -te-li-se-l-o in "ant Mnp Bedewi-te-li-se-l-o". [G11] found the locative in "Isis in Philae". Not to be confused with the -te of kdite ([L11] p. 96).
- **Label:** ESTABLISHED.

**6. -leb**
- **Contexts:**
  - "pelmoS leb apote leb xrpx leb kdite bes lo wi" (T0352)
  - "pesto leb ye t mde aqe bes lo" (T1002)
  - "atoliteb", "Sqekiteleb" (T0010)
  - "aSori pilqeteleb" (T0026)
  - "pqr-leb yetmde-lo" (Millet)
- **Slot:** plural possessors in the relationship section.
- **Published:** [R16] pp. 7–8: plural article -l-b, mk-leb "the gods"; "pqr-leb yetmde-leb-kwi" "they were nephews of princes". [L11] p. 104 agrees.
- **Label:** ESTABLISHED.

**7. wi, as a separate word**
- **Contexts:**
  - "kdite lo wi" (T0612, T0017)
  - "yet mde lo wi" (T0040, T0093)
  - "dbrete lo wi" (T0059)
  - "ye teke lo wi" (T0070)
  - "pilqe te li s li wi" (T0016)
- **Slot:** always clause-final, after lo or li.
- **Published:**
  - [R16] p. 8 calls -wi an "emphatic marker", in quotation marks.
  - [RD] calls it a "so-called 'emphatic particle' after the copula".
  - Hintze called it a "particle", as reported by Rilly.
  - The position is established; the function is not.
- **Homograph in gold:** gold lists wi as a short form of wide "brother". None of the 67 cleaned tokens is in a slot where "brother" fits.
- **Label:** PUBLISHED HYPOTHESIS.

**8. l, as a separate word**
- **Contexts:**
  - "xrpxN pXrs te l" (T0012)
  - "woS pilqe te l xe l woS tebwe te l xe l" (T0016)
  - "l pesto NAME l pesto …" (T0019, a list of viceroys)
  - "x mlo l" (Rilly's examples)
- **Slot:** closes a noun phrase in titles and lists. Very frequent in a few list-like texts: 127 tokens in only 27 families.
- **Published:** [R16] p. 8 says the article is a "connector and group boundary marker", weakly definite.
- **Homograph in gold:** gold's l- "give" ([R16] p. 7) is a verb root, not this.
- **Label:** ESTABLISHED.

**9. Benediction verb endings**
- **Contexts:**
  - "ato mXe piSiXekes at mXe piSixrkes" (T0011)
  - "ato bSiXebxes at mXe bSixrbxes" (T0002)
  - "ato mXe pSXekete" (T0046)
  - "pi So Xe bx ke te" (T0917)
  - "ato SXekes at mXe bSxrkes" (T0015)
- **Slot:** benedictions A (water, with the root Xe) and B (bread, with the root xr).
- **Published:** [RD] §5.1 and Table 4:
  - -x(e) and -bx(e) mark singular and plural beneficiary;
  - -k(e) marks the 2nd person plural;
  - -te / -to is optative ("may you (pl.) make him drink …");
  - -se is an optional imperative particle, and -kese may be -kete-se.
  - In 2016 Rilly called these imperatives ([R16] p. 8), so the mood is debated.
- **Corpus check:** -bx- forms (bSiXebxes, bSixrbxes) appear in texts naming two or more people (T0002 has several "NAME yetmdelo" clauses). That fits a plural beneficiary, but I checked only these few texts.
- **Label:** ESTABLISHED for number and person; PUBLISHED HYPOTHESIS for the mood.

**10. -lw / lw**
- **Contexts:**
  - "kdis-lw abrs-lw" (T0195)
  - "tros lw mlo lowi" (T0252)
  - "apote lw qore te" (T0207)
  - "apotelw qorete" (T0046)
  - "NAME ptros li s lw ar mte kw" (T0016)
  - kelw (gold "and") counted separately: 12 tokens.
- **Published:** [RD] ex. 51 glosses kdi-se-l-w abr-se-l-w as "each woman, each man", -l-w = article + objective (accusative/dative) -w. [R16] p. 7 says objective marking is rare and perhaps local.
- **Note on T0195:** this suggests T0195 is a royal text (REM 1003, Akinidad), not an epitaph.
- **Not found:** -lw as "and", or as a plural predicate.
- **Label:** PUBLISHED HYPOTHESIS.

**11. ye, as a separate piece**
- **Contexts:**
  - "ye t mde" for yetmde (T0706, T0316, T0597, T1002)
  - "ni ye teke lo" (T0025)
  - "eSxini ye teke lo wi" (T0070)
  - "polmoS s ye ye yetmdelowi" (T0013)
- **Published:** [RD] §4.2–4.3 gives three homonyms:
  - ye- is the 1st singular subject prefix in royal texts;
  - ye-/yi- is a rare causative prefix in benedictions;
  - ye- and te- in filiation are "probably two eroded forms of yet-" "person".
  - [R16] p. 5: initial ye/yi is also just how /e/ and /i/ are written.
- **My reading, not published:** "ye teke lo" may be ye- + tke "love, revere" (gold) + -l-o. That is a guess, confidence 1; [RD] has no "yeteke".
- **Label:** PUBLISHED HYPOTHESIS.

**12. Benediction prefix p(i)S- / pso- / bS-**
- **Contexts:** see item 9. The prefix is spelled pS-, piS-, pso-, bS-, ps- and, in T0015, is perhaps lost (SXekes).
- **Published, with disagreement:**
  - [RD] §4.3: pVsV- (and ye-/yi-) are "best interpreted as causative markers". Required before "drink" (Xe) and "eat" (xr), optional before "present"; "not yet fully understood".
  - [R16] p. 8: "p- could be an optative auxiliary".
  - [L11] p. 99: causative.
  - p/b spelling alternation in native words: [R16] p. 6.
- **Label:** PUBLISHED HYPOTHESIS.

**13. bes = (a)qe-bes(e)**
- **Contexts:**
  - "pelmoS leb apote leb xrpx leb kdite bes lo wi" (T0352)
  - "leb ye t mde qe bes lo" (T0706)
  - "pesto leb ye t mde aqe bes lo" (T1002)
  - "mlekeyos p kelw ye t mde bes lo" (T0597)
  - "Ste bes lo" (T0365)
  - "kdis-lw abrs-lw yemeqe eqe bes wi" (T0195)
- **Slot:** between a kin term and the predicate, in clauses whose possessor is plural (marked with -leb).
- **Corpus evidence:** in all 4 families where the possessor is marked, it is plural (-leb). No singular possessor (-l, -li-s) precedes bes. aqe and qe occur only right before bes (6 families), so "aqe bes" is one word, (a)qe-bese.
- **Published:**
  - [RD] p. 21 and n. 31: bese, qebese, aqebese, aqobese mean "their"; e.g. "yetmde qebese-l-o-wi 'he was their nephew'", "ste-bese 'their mother'". The initial a- is "unexplained".
  - Millet [M68] l. 95 (p. 108) translates kdite-bes-lo-wi as "sister of the generals, the envoys, and the governors", taking bes as part of the plural possessive.
- **Label:** PUBLISHED HYPOTHESIS. Rilly states it firmly but is the only grammar source found.

**19. ke, as a separate piece**
- **Contexts:**
  - "pi So Xe bx ke te" (T0917)
  - "ate mXe pi So ke te" (T0680)
  - "nob brlX l do ke lo" (T0529)
  - "as enis 14 ni ke lo" (T0695)
  - "pesto li yi kid ke ames 1" (T1006; elsewhere yikidke)
- **Published:**
  - In verbs, -k(e) is the 2nd person plural ([RD] Table 4).
  - After nouns the direction is disputed: Lipiński reads Bedewi-k as "to Meroe" ([L11] p. 99); Wikipedia lists -k(e) as "ablative" without a source.
- **Not found:** the non-verbal contexts above ("do ke lo", "14 ni ke lo").
- **Label:** PUBLISHED HYPOTHESIS.

**21. ni, after numerals**
- **Contexts:**
  - "penn 5 ni ye teke lo" (T0025)
  - "plsn qbnti penn 5 ni yetekele" (T0441)
  - "penn 5 ni" (T0707; "5ni" in T0711)
  - "as enis 14 ni ke lo" (T0695)
  - "as tkereXetmS 5 ni" (T0043, T0892)
  - "sbe 3 ni bqo lo" (T0741)
- **Corpus evidence:** 8 of the 9 cleaned tokens follow a numeral. The ninth is "no b brlX l ni dtweti" (T0928).
- **Proposal:** a suffix on numerals, ordinal or adverbial ("the 5th", "5 times"). Confidence 3.
- **Published:** Millet [M68] l. 215 (p. 185/186) translates "penn 5 ni" as "the 5th penn", which implies an ordinal reading; he gives no analysis.
- **Not found:** a grammar statement. [R16], [L11] and [RD] were searched full-text for "-ni"; the only hit is y-ni in amulet decrees ([RD] ex. 66), which is unrelated.
- **Label:** PUBLISHED HYPOTHESIS, implicit in Millet's translation. The distribution count is mine.

### Invocation epithets (items 14 and 18)

**14. wetrri / qetrri** and **18. wetNyiNqeli / qetNyinqeli**

**All 11 families:**

| Row | Opening |
|---|---|
| T0002 | woS wetNyiNqeli Sori wetrri qo NAME qowi |
| T0005 | woSi wetNyi Nqeli Sori wetrri qo … |
| T0010 | woS wetNyiNqeli Soriqetri qo … |
| T0011 | woS weNyi Nqeli So ri qetrri qo … |
| T0015 | woS wetNyiNqeli Soriwetrri qo … |
| T0019 | woS wet NyiNqeli So ri wetrri Stmdes … |
| T0023 | woS qetNyinqeli Sori qetrri qo … |
| T0037 | woS wetNyiNqeli Seriqetrri qe … |
| T0303 | woS wetNyi Nqeli Sori qe trri qo … |
| T0074 | woS wetNyiNqeliSori qetrri qo … |
| T0892 | woS wetNyi Nqeli Sori qetrri qo … |

**Slot:** the invocation, an extended form of "woSi Soreyi" (O Isis, O Osiris). It is immediately followed by the nomination (qo … qowi).

**Proposal (NEW):** the vocative suffix -i is phrase-final. It closes the whole "god + epithet" phrase rather than the god's name. Evidence:
1. **Osiris never has his vocative form beside the epithet.** In all 11 families Osiris is Sori/Seri/So ri, never the vocative Soreyi, which opens 11 other families. Both epithets end in -i: wetNyiNqel-i, wetrr-i.
2. **Isis behaves the same way.** She is bare woS in 10 of 11 epithet families, against woSi in 19 families with the short invocation. The exception is T0005.
3. **It fits Meroitic grammar.** Meroitic marks a phrase once at its end: the article is a "group boundary marker" ([R16] p. 8).
4. **The two epithets share their opening.** Both begin wet-/qet-, and the w/q choice tends to match within a text (w…w in T0002 and T0005; q…q in T0023). That suggests a shared element wet-/qet- + stem (NyiNqe-l, rr).

**Confidence:** 3 for the distribution, 2 for the phrase-final vocative, 1 for any meaning.

**Alternative:** the epithets are fixed titles borrowed whole, so their final -i is accidental. A test: an epithet text with Soreyi + epithet would refute the proposal. None exists in this corpus; check REM.

**Published:** Millet [M68] l. 400 (p. 309) and l. 439 (pp. 332–335) transcribes these lines and leaves the epithets untranslated ("o isis wetNyiNqel! o osir…").

**Searches with no proposal found:**
- my web search for "qetneyineqeli" OR "wetneyineqeli" OR "qetrri" with Isis and Osiris;
- a subagent's web search plus full-text searches of [R16], [L11] and [RD] for wetr, qetr and neyin;
- the Griffith OCR (no hit except the name Qeqeli).

**Label:** NEW, for both items.

### Titles, terms and list words (items 15–17, 20, 22–30)

**15. penn**
- **Contexts:**
  - "plSn NAME penn 5 ni ye teke lo" (T0025)
  - "plsn qbnti penn 5 ni yetekele qbn s li penn 5 ni" (T0441)
  - "penn 34" (T0440, T0664)
  - "keN 6 Snswe penno" (T0080, T0876)
  - "qeren penni li s le" (T0295)
  - "appoye penn tewisti" (T0986, a proskynema)
- **Slot:** graffiti and dated texts, never in epitaph clauses.
- **Corpus evidence:** a numeral follows penn in 7 of 12 tokens.
- **Published:** Millet [M68] ll. 213–215 (pp. 185/186):
  - "keN 6 : Snswe(?) pennE" = "year 6, (month of) Sansawe (??), pennE";
  - "plsn qbnti penn 5 ni" = "the high-priest of the qbn (of) the 5th penn";
  - "qeren penni-li-s-le" = "qeren of the penni".
  - No meaning is given.
- **Proposal (NEW reading):** a term in datelines or counted service, used with ordinals (5 ni), after year (keN) and month in one formula. "day" is ruled out by "penn 34", above 30. Confidence 2.
- **Label:** PUBLISHED HYPOTHESIS (Millet's partial translation), plus my reading.

**16. temey**
- **Contexts:**
  - "temeylX NAME XlXili tetelitreli yetmdelowi" (T0006)
  - "temeylX dbrete … yetmdelowi" (T0059)
  - "temeykdi lX dbretelowi" (T0006)
  - "temey lX p tros lowi" (T0250)
  - "mXo temey nsdoke kdi abr nxbreS kbx" (T0746, T0863; Kharamadoye, see C4)
- **Slot:** career titles (temey + lX "great", temey + kdi "woman").
- **Published:** Millet [M68] ll. 159, 168, 219–223 (pp. 151–201):
  - "temey-lX" = "chief temey" / "chief of the temeya";
  - "temey-kdi" = female temeya;
  - in Kalabsha: "the temeya (and/or) the nasadEke carry off a woman".
- **Corpus evidence:** temey takes kdi "woman" and lX "great" like a noun of persons. That supports a class or office of people over a place.
- **Label:** PUBLISHED HYPOTHESIS.

**17. keN**
- **Contexts:**
  - "atmi wes 12 keN 2 aritewil" (T0016, T0026)
  - "do 5 keN tmi 10 keN aro tros" (T0016)
  - "keN 6 Snswe penno" (T0080, T0876)
  - "beltore le 10 keN l tlt" (T0346)
  - "teketi 59 e 10 keN 1 tlt" (T0671)
- **Corpus evidence:** keN is adjacent to a numeral in 10 of 16 tokens.
- **Published:** Millet [M68] l. 213 (p. 185/186) translates "keN 6" as "year 6".
- **Corpus caveat:** the lists in T0346 and T0671 (with tlt and teketi) look more like counted goods than dates. Two keN words, or "year" in a list of yearly dues, cannot be told apart here.
- **Label:** PUBLISHED HYPOTHESIS.

**20. tros**
- **Contexts:**
  - "temey lX p tros lowi" (T0250)
  - "temey lX bereqedo li tros lowi" (T0541)
  - "tros lw mlo lowi" (T0252)
  - "tros li Xi qore mXo li s l" (T0382, T0611)
  - "aro l tros" (T0486)
  - "ptros li s" (T0016)
- **Slot:** the relationship predicate (tros-lowi), like a kin term.
- **Published:** Millet [M68] l. 160 (p. 151) has "trEs parent"; ll. 320–321 (p. 261) has "arE (l) trEs" "the mother of Horus" and "p-trEs-l" "the mother of p".
- **Label:** PUBLISHED HYPOTHESIS.

**22. mde**
- **Contexts:**
  - "arome li s NAME yet mde lo wi" (T0040)
  - "pqr l yet mde lo wi" (T0093)
  - "ye t mde (a)qe bes lo" (T0706, T0316, T1002, T0597)
  - "mni si mde lw" and "qorisew s mde se lw" in T0396 (Tanyidamani, see C4)
- **Published:**
  - [RD] p. 46: yet- + mde, where mde "refers to the mother's family"; yet- is compared with Proto-Nubian *id "person".
  - Millet [M68] ll. 240–241 (pp. 229–232): "mde: to be related … in general", "mdes: direct descendant?".
  - Lipiński's Semitic etymology ([L11] p. 102) is not followed by others.
- **Not found:** "maternal uncle" for mde alone.
- **Label:** PUBLISHED HYPOTHESIS.

**23. Sq-**
- **Contexts:**
  - "xrpxN Sqekiteleb kditebetowi" (T0010)
  - "kroroleb … xrpxN Sqekiteleb yetmdelowi" (T0045)
  - "NAME (qo) Sq kdi" (T0041, T0049)
  - "SqyeS nsdokeS tmeyyeS nxbreS" (T0136, T0815; Kharamadoye)
- **Published:** Millet [M68] l. 365 (p. 288): "the Saqa-people"; l. 368 (p. 290/291): "Sqkdi" "woman of the saqa-people"; l. 301 (p. 251): "Sqte-lX-lo" "chief Sqte?".
- **Label:** PUBLISHED HYPOTHESIS.

**24. tlt**
- **Contexts:**
  - "teketi 59 yed tlt 16 kelw" (T0015)
  - "keN l tlt my tk teketi" (T0346)
  - "10 keN 1 tlt my tkteketi" (T0671)
- **Published:**
  - Rilly ([RD] p. 18) reads tlt in REM 1165 as "talent", a unit.
  - Lipiński ([L11] p. 102) reads "three (times)".
  - "tlt 16", a word followed by a numeral, fits Rilly's unit better.
- **Label:** PUBLISHED HYPOTHESIS.

**25. teketi**
- **Contexts:**
  - "kiSri NAME axid kiN kisrisqtile nbrlis 1 belebeltor 1 tsl teketi mesrekelis beltore 1" (T0021)
  - "axid kiN kiSrisqtile nbrlis l belebeltor 1 bXeyedlis 1 teketi 59 yed tlt 16 kelw" (T0015)
  - "teketi 59 e 10 keN 1 tlt my tkteketi" (T0671)
  - "keN l tlt my tk teketi" (T0346)
- **Slot:** counted lists that open with kiSri "Caesar" (gold) and count nbr-lis "of gold" (gold nbr) item by item.
- **Proposal:** a counted commodity or measure (59 of them) in an inventory headed by Caesar's name. Confidence 1. The texts may be graffiti or ostraca rather than epitaphs.
- **Alternative:** a verb form, given "tk teketi" and "tkteketi" beside tkk "plunder" (gold).
- **Searches:** a subagent's full-text searches of [R16], [L11] and [RD]; my grep of Otten's Millet, Rilly and Lobban lists. No hit.
- **Label:** NEW.

**26. plSn**
- **Contexts:**
  - "plSn NAME penn 5 ni ye teke lo" (T0025)
  - "plSn NAME (qo)" (T0066, T0564)
  - "plsn qbnti penn 5 ni" (T0441)
- **Slot:** opens graffiti, before a personal name.
- **Published:** Millet [M68] l. 215 (p. 185/186): "plsn = high priest".
- **Proposal (NEW etymology):** Egyptian pꜣ mr-šn, "the lesonis", the temple's administrative head. It would give p-l-šn exactly as pꜣ mr mšꜥ gives pelmoS "general", a published etymology ([R16] p. 9). Confidence 2.
- **Test:** a Demotic graffito at Philae naming the same man as mr-šn.
- **Searches:** two subagent web searches (plšn/plsn with lesonis and Philae; a Meroitic "lesonis" loanword); my web search "plšn lesonis mr-šn Philae". No proposal found.
- **Label:** PUBLISHED HYPOTHESIS for the title, NEW for the etymology.

**27. SlXS**
- **Contexts:**
  - "SlXS NAME" (T0007, 20 augmentation copies)
  - "SlXS NAME qo" (T0519)
  - "SlXS mnp s l sm lo" (T0644)
  - "SlXS terek lo" (T0694)
- **Published:** Millet [M68] l. 122 (p. 121): "wife of the SlxS of Amanap", a title left untranslated.
- **Corpus evidence:** SlXS + god-genitive (mnp-s-l) + sm "wife" (gold) shows an office tied to Amanap.
- **Label:** PUBLISHED HYPOTHESIS for the title; no meaning.

**28. SSimete**
- **Contexts:**
  - "bokemetel yetmdelowi SSimete ktkelis NAME smlowi" (T0005)
  - "NAME SSimete mxtebedetel yetmdelowi NAME SSimetel yetmdelowi" (T0023)
  - "SSimete kdke li s" (T0981)
  - "SSimete mleyos" (T0734)
- **Published:** Millet [M68] l. 20 (p. 25): "steward" (TITULARY); l. 190 (p. 174/175): "SSimete kdke-li-s" "steward?? of the queen-mother".
- **Corpus evidence:** the genitive ktke-li-s ties the office to the Candace (gold ktke).
- **Label:** PUBLISHED HYPOTHESIS.

**29. Stmdes**
- **Contexts:**
  - "So ri wetrri Stmdes pe stolis RNAME qowi" (T0019)
  - "qo niye qowi Stmdes peste lis RNAME terikeli" (T0083)
  - "Stmdes teN te" (T0306)
  - "Stmdes pestolis" (T0941)
- **Published:** Millet [M68] ll. 107–108 (pp. 115–117): "Stmdes of the prince", "kinsman (of the prince)"; l. 188: "Stmdes teN-te" "kinsman-of-the-prince in teN".
- **Corpus evidence:** S-t-mde-s contains mde (item 22) and always governs pesto-li-s "of the viceroy".
- **Label:** PUBLISHED HYPOTHESIS.

**30. dbre (dbre-te)**
- **Contexts:**
  - "temeylX dbrete XlXili" (T0059)
  - "temey lX dbre te S qoye" (T0268)
  - "temeykdi lX dbretelowi" (T0006)
  - "temeykdilX dbrete lo wi" (T0059)
- **Slot:** the place of office in the career section; only with temey (item 16).
- **Published:** Millet [M68] l. 420 (p. 325/326): "related to the chief of the temeya in dbre", a place name.
- **Label:** PUBLISHED HYPOTHESIS.

## C. Where the corpus file looks wrong

**1. Multi-word names escaped the mask.** The name-swap augmentation is still in the file.
- These 17 strings fill NAME slots in copies of the same text:

  `tqo mete l`, `pte oye`, `x lonk`, `tNlxe aror`, `msxte trobit`, `a kye`, `mlitr ide`, `li ye`, `mh witr`, `mli tewen`, `beke mete`, `apN blye`, `kdi qebts`, `Swe ibr`, `dteqox qo`, `S qo ye`, `qo eye`

  They come from Otten's swap list; names with spaces were not caught by `src/dedup.py` or `src/collapse.py`. Each sits in 15 to 21 family medoids.
- **Second words of two-word names** follow NAME: mokelowi, kroro, mXewitr, Smedeli and "mete l".
  - `swap_partners.json` gives mEkelEwi the partners {Smedeli, krErE, mXewitr, qE}.
  - Within families, "+mokelowi", "+qo" and "+mete l" are inserted about 2,700 times each.
- **Result:**
  - Masking these and removing exact duplicates leaves 442 of 1,019 rows.
  - Whole "texts" are only augmentation, e.g. "NAME kroro", "Swe ibr mXewitr", "NAME mokelowi mokelowi" (family T0008, 80 members).
  - Words such as tNlxe (95 raw tokens), aror, apN, blye, msxte, trobit and lonk are name fragments, not vocabulary.
- **Caution on "qo":** "NAME qo" is both a real nomination and a swap artifact. Only the within-family comparison tells them apart.

**2. Inflated near-duplicates remain.** The inscription in T0014 (86 words) and its fragment T0001 sit in 105 rows. So womnitX (441 raw), aribet (400), ateqi (348), beloloke (262), Sklte (213) and mdetowi (172) are frequent only because of copies. The same holds, at about 20 copies each, for:
- T0006 (tereke Sklw weXoke …)
- T0038 (mlekeyos …)
- T0021 (kiSri … nbrlis)
- T0025 (plSn … penn)
- T0029 (qo xbxN … perite woSto)

**3. Names joined to neighbouring words, so the mask missed them:**
- `ateqiSitkemoli`, where SitkemEli is in the private name pool;
- `amXyemokelowi` (T0303), from amxye (pool) + mokelowi;
- `yetmdelowiateqi` and `tedxelowimlekeyos`, missing spaces;
- `woSi Sorieyiorye qowitdxelowiterikelowiXliterwi` (T0168), a whole formula run together.
- `bekemete` (T0124, T0225, T0751, T0009) is a personal name in Millet [M68] l. 304 ("the akrErE, bekemete") and is not masked.

**4. Rows labelled "funerary" that are not epitaphs.**
- **Philae graffiti and datelines:** T0016, T0026 (woS pilqe-te-l … woS tebwe-te-l), T0080, T0876 (keN 6 …).
- **Kharamadoye (Kalabsha) lines in Millet's transcription:** T0136, T0746, T0815, T0863, T0130, T0243 (SqyeS nsdokeS temeyyeS nxbreS …; Simlok dik …). They duplicate the narrative row `kharamadoye` in another spelling.
- **T0396 (721 words):** contains "tNyidamani", so it is very likely the Tanyidamani stela again.
- **T0957 (490 words):** pqr qorise l qor xrpxe … qes armeyose … looks royal. I have not identified it.
- **T0195:** "kdis-lw abrs-lw" matches [RD]'s quotation from REM 1003.
- **Consequence:** frequency work on "funerary" texts should drop these rows.

**5. Spacing is inconsistent.** Morpheme-split and run-together transcriptions are mixed, so one word appears in several shapes:
- "yetmdelowi" / "yetmdelo wi" / "yet mde lo wi" / "ye t mde";
- "Sori" / "So ri";
- "pesto" / "pe s to" (T0019);
- "terik elowi" (T0059);
- "5ni" (T0711);
- "34N" (T0368).

Token counts of any word depend on this. Count pieces, not whole tokens.

**6. Possible mis-readings.** Each needs checking against REM:
- "ato mXo piSiXekes" (T0083) for the usual mXe;
- "SXekes" without p(i)- (T0015);
- "pilege" for pilqe (T0334);
- "Soriqetri" for qetrri (T0010);
- "phrstel" beside pXrstel (T0301).

**7. Missing input.** `data/gold_morphology.json`, named in the task, is not in the repo.

## D. High-frequency items left out, and why

**Glossed in gold:** at the start, or added while this ran (gold went from 66 to 82 entries).
- Present at the start: qo/qowi (this), woS/woSi, Sori/Soreyi, lX, mXe (and mXo, its spelling variant), ato/ate, at, pelmoS/polmoS, pqr, qore/qor, kdi, kdite, Ste, mte/mete, yetmde, terike, tdxe/tedxe, apote, ant, amnp, kelw, tbo, tewisti, mlo, sm (smlowi).
- Added during the run: pesto/peseto, perite, beloloke, kiSri, qes, adb (adblis), arome, atiye, xrpxe/xrpxN (ḫrpḫe, "governor (?)"), tebwe (Abaton; Millet [M68] l. 290 had it), tkk and sye.

**Augmentation residue (C1):** mokelowi, kroro (when after NAME), mXewitr, Smedeli, tNlxe, aror, apN, blye and the other slip pieces.

**Single-letter splinters:** t (14 families, mostly "ye t mde"), a (11), p (9), e, d, N, w, y, b, q, r, i. Also "So" (the split "So ri", Osiris). These are pieces of split known words, not morphemes I could test.

**Spelling variants and names:**
- qe / qewi is an older or variant spelling of qo / qowi in the nomination (T0014 "qe NAME qewi"); gold's qo note already mentions qe.
- bekemete is a personal name.
