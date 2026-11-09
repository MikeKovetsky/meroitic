# Can the model read Griffith's printed Meroitic cursive type?

Work of 2026-11-09, 09:24 to 09:57 PST, by Claude Opus 5.5. Downloads are in `/private/tmp/claude-501/griffith/` and
scripts, crops and readings in `/private/tmp/claude-501/griffith_scripts/` (neither is in the repo).

## 1. Answer first

**Yes.** On 12 short texts that Griffith printed in Meroitic cursive type in *Meroitic Inscriptions II* (1912), the
reading agrees with FHN III's modern transliteration on **482 of 504 signs (95.6%)**, and **86 of 103 FHN words**
come out fully right (83.5%).

The 22 disagreements are of three kinds:

1. **2 are my misreadings.** Both are m read where the type has h̲ (Griffith's ẖ), and I had marked both "[m?]" when
   reading.
2. **18 are places where Griffith's printed type itself differs from FHN.** These are later re-readings of the stones,
   or FHN's editorial choices. Each was checked on a second look at the type at 2.5x, beside clear examples of the
   same signs on the same page. For three of them, Griffith's own Latin rendering in his commentary also backs the
   type (section 7).
3. **2 are h-signs whose diacritic in FHN is too small to read on the scan.**

So against what Griffith printed, the reading is 500 of 502 signs (99.6%). On the three texts whose Griffith rendering
I had not seen (nos. 106, 107, and the 119/120 text read fully blind), it is 81 of 84 FHN signs (96.4%), with no
misreading.

Read these numbers with three caveats:

1. **Cut: one line of no. 103 was not read.** My crop missed the third type line of no. 103 (stone lines 4 to 6,
   about 25 signs). By the time I found it, FHN's text had been seen, so it is left out of the score rather than read
   unblind.
2. **Most texts were not fully blind to Griffith.** He prints his English translation directly under each text, with
   the names in his own spelling (Manitawawi, Mashtaraqaye). I saw those renderings for 8 of the 12 texts before
   reading them (section 9). That helps with names, but it cannot supply the sign-by-sign string, and FHN was never
   seen before a reading was frozen.
3. **Type covers about 190 texts, not 300.** The type-set volumes are *Meroitic Inscriptions* I (nos. 1 to 74),
   *Meroitic Inscriptions* II (nos. 75 to 137) and *Meroë* (nos. 1 to 51). Karanòg's 150 texts and the 46 Faras texts
   are hand copies, a different test (the README notes that m, ẖ and s all look like a 3 there).

**Verdict:** printed type is readable well enough to transcribe. What comes out is *Griffith's 1911–12 reading*,
which differs from the REM text in about 4% of signs here (18 of 504). Rows taken from Griffith should carry the source
and the REM number, and REM's reading should win wherever FHN or REM prints it.

## 2. Sign key used

The source is Griffith's "Table of the Meroitic Alphabets", *Meroitic Inscriptions II*, p. xv
([archive.org leaf n18](https://archive.org/details/archaeologicals20egyp/page/n18)). It gives the same 23 values as
the Karanòg list in `README.md` section 2. The forms below are Unicode look-alikes of the printed type. The picture,
cut from the table and labelled, is `/private/tmp/claude-501/griffith_scripts/signstrip.png`, and it was placed above
every crop while reading.

| Griffith | FHN / modern | Corpus | Type form (look-alike) | Mixed up with, and how to tell |
|---|---|---|---|---|
| a | a | a | `ϛ2`, two strokes | — |
| e | e | e | `ς`, a single hook like 9 or S | the left half of a |
| ê | o | o | `/`, one slash | the slash inside q |
| i | i | i | `4` with a long cross-bar | — |
| y | y | y | `///`, three slashes | se (`J//` has a J) |
| w | w | w | `ƃ`, flat top with a loop at the foot | — |
| b | b | b | `ν`, a v with a hooked right arm | — |
| p | p | p | `ξ`, rounded ε top with a long tail to the lower right | k: top rounded, not a flat Z |
| m | m | m | `ʒ`, smooth open top and a long straight descender to the lower left | h̲ (angular), s (closed) |
| n | n | n | `ꝶ`, R-like with a long tail to the right | — |
| ñ | ne | N | `ʎ`, λ with a loop at the top | n + e |
| r | r | r | `ω` | — |
| l | l | l | `ϟ`, an angular 5 | t |
| ḫ | ḫ | x | `⊂`, a c open to the right, with a long top stroke | — |
| ẖ | h̲ | X | `ɜ`, a pointed `>` middle and a descender to the lower left | m (smooth) |
| s | se | s | `J//`, a J and two strokes | y |
| š | s | S | `3`, a closed rounded 3 with no long tail | m |
| k | k | k | `ʓ`, a flat Z top and a curling foot | p |
| q | q | q | `/ɔ`, slash and ɔ as one sign | o + q (`//ɔ` is q then o, "qo") |
| t | t | t | `ϑ`, hooked, with a dot-like start at the top left | l (angular, no dot) |
| te | te | te | `/<-`, a slash and a barred hook | to |
| tê | to | to | `<-` with a dot below, like Arabic ب | te |
| z | d | d | `ꞥ`, N-like with a hooked foot | — |
| : | : | : | word divider | — |

Two facts about Griffith's printing make it easier:

1. **The type runs right to left like the stone.** Spaces are Griffith's word division; ":" is a divider on the
   stone.
2. **The superscript numbers 5, 10, 15 in the type are the stone's line numbers.** They match FHN's "(5)", "(10)",
   "(15)" exactly, often in mid-word (no. 97: `yetet¹⁰ke`, FHN `yetet(10)ke`). That gives a free alignment with REM.

## 3. Method

1. **Sign table.** I downloaded page images only, from archive.org's page endpoint, for *Meroitic Inscriptions II*
   ([`archaeologicals20egyp`](https://archive.org/details/archaeologicals20egyp)): leaves n17 to n20 and n52 to n64,
   about 14 MB. On this scan, p. N is leaf n(N+19).
2. **Texts.** The Philae "Meroitic Chamber" labels, nos. 97 to 111, are on pp. 34 to 42. FHN III no. 267 ("Philae,
   Meroitic Chamber", pp. 1024–1027) prints REM 0097–0111 in full. Nos. 119/120 (Hadrian's Gate) are on p. 45, and FHN III no. 276
   (p. 1049) prints them. FHN III is the PDF already saved at
   `/private/tmp/claude-501/expansion/survey/fhn/fhn03.pdf`, with page images taken from its PDF pages 281–283 and 305.
3. **Blind rule.** Each reading was appended to `readings.md` with a timestamp. Frozen copies were made at 09:41:28
   (`readings_frozen_094128.md`, the 11 Philae chamber texts) and at 09:49:28 (`readings_frozen2_094928.md`,
   no. 119/120). Before a freeze, the only FHN material seen was the REM ids and line numbers (from `grep -o`) and a
   masked layout of nos. 267 and 276, with every word replaced by `x`. FHN's text was first printed after each freeze.
4. **Scoring.** `score2.py` runs an edit-distance alignment on signs. `se`, `te`, `to` and `ñ` each count as one sign,
   and ḫ and h̲ count as distinct. Dividers, line numbers and FHN's `[=...]` normalisations are ignored. FHN's
   asterisked (uncertain) signs count as read. FHN's letters in round brackets, which the editor supplies, are kept.
   A word is "fully right" when no edit falls inside it.
5. **Re-check of each disagreement.** Every disagreement was looked at again at 2.5x, beside clear examples of the
   confusable signs from the same page (`disp1.png`, `disp2.png`, `disp4.png`, `disp5.png`). Griffith's commentary
   OCR (`expansion/survey/ia/archaeologicals20egyp.txt`) was searched for his Latin form of the disputed words.

## 4. Results per text

| REM | MI II page (leaf) | Griffith's English seen before reading | FHN signs | Right | % | FHN words fully right | My misreadings | Griffith ≠ FHN (unclear) |
|---|---|---|---|---|---|---|---|---|
| 0097 | p. 37 (n56) | yes | 104 | 98 | 94.2 | 17/20 | 1 | 5 |
| 0098 | p. 38 (n57) | first line | 71 | 69 | 97.2 | 12/14 | 0 | 2 |
| 0102 | p. 40 (n59) | yes, ll. 1–2 | 55 | 52 | 94.5 | 11/14 | 1 | 2 |
| 0103 | p. 40 (n59) | yes, l. 1 | 38 | 36 | 94.7 | 7/9 | 0 | 2 |
| 0104 | p. 41 (n60) | yes | 21 | 20 | 95.2 | 4/5 | 0 | 1 |
| 0105 | p. 37 (n56) | yes | 22 | 22 | 100 | 4/4 | 0 | 0 |
| 0106 | p. 38 (n57) | no | 22 | 22 | 100 | 4/4 | 0 | 0 |
| 0107 | p. 38 (n57) | no | 28 | 28 | 100 | 5/5 | 0 | 0 |
| 0108 | p. 41 (n60) | names only, in the commentary | 13 | 11 | 84.6 | 1/2 | 0 | 2 |
| 0109 | p. 41 (n60) | yes | 18 | 18 | 100 | 4/4 | 0 | 0 |
| 0111 | p. 41 (n60) | yes, ll. 1–2 | 78 | 75 | 96.2 | 14/17 | 0 | 2 (1) |
| 0120 (with 0119) | p. 45 (n64) | no, fully blind | 34 | 31 | 91.2 | 3/5 | 0 | 2 (1) |
| **Total** | | | **504** | **482** | **95.6** | **86/103** | **2** | **18 (2)** |

Notes on the table:

1. **No. 103** is scored on stone lines 1 to 3 only (see the cut in section 1).
2. **No. 119/120:** Griffith prints one composite text for the two nearly identical graffiti (his "(y)" is taken from
   120). It is scored against REM 0120, the closer of the two.
3. **That is 12 texts, two more than the 6 to 10 asked:** no. 105 is a single line, and 119/120 was added as the fully
   blind control.

## 5. The readings

All readings are right to left, as frozen. A space is Griffith's word space, ":" his divider, and `[x?]` a sign I
marked uncertain. For FHN, the line numbers are dropped, the dividers shown as ":", and `*` (uncertain) kept.

**REM 0097** (no. 97, MI II p. 37)

1. Mine: `qo pelmos atolise bekemeteli | sete mnitwwiqo | wete siyeteli yetetke womñt[m?] : | pilqetelo : | ant qo rito steli qo re : semlo | ḫbḫñ : sqtelh̲lo | mlostoh̲elo`
2. FHN: `qo pelmos atolise Bekemeteli sete Mnitwwiqo wete *Siyeteli yetetke womneth̲ : Pilqetelo : ant qorito steli qore : *semlo ḫbḫñ : sqotelh̲lo mlo sto*selo`
3. Differences: `womñt[m]` against `womneth̲`. The type has ʎ (ñ) where FHN writes n + e (Griffith ≠ FHN), and h̲ where
   I read m (mine). `sqtel` against `sqotel`: the type has no o after q, and Griffith renders it "shaqate" (G ≠ F).
   `stoh̲elo` against `sto*selo`: the type has h̲ + e, rendered by Griffith "malêshatêkhe" (G ≠ F).

**REM 0098** (no. 98, p. 38)

1. Mine: `qo kroro bekemete mte pelmos | a tolit yerikelo | mni se mtelo | pesetolo : | pelmos adblito | nobow : × nke[l?][b?]o`
2. FHN: `qo kroro Bekemete ste pelmos atolit yerikelo *Mnise mtelo pesetolo pelmos adblito nobow : 35 kelbo`
3. Differences: `mte` against `ste`. The type has m (smooth ʒ with a long descender), the same form as the m of
   `pelmos` beside it (G ≠ F). The type has `× n` where FHN prints "35" (G ≠ F; FHN's "35" is unexplained).

**REM 0102** (no. 102, p. 40)

1. Mine: `ḫbḫñ wosqer : qo mstrqyeqo : | wosi : yntke : pikl : pḫil[m?] : | p[l?]i : ptroti pikn : pbḫ`
2. FHN: `ḫbḫñ Wos qer : qo Mstrqye qo : Wosi : yntk*e : pipl : pḫilh̲ : p*li : Ptroti pipn : pbḫ :`
3. Differences: `pikl` and `pikn` against `pipl` and `pipn`. In both words the type has a flat-Z-topped k, unlike the
   rounded p that starts each word (G ≠ F, twice). `pḫil[m]` against `pḫilh̲`: the type has h̲ (mine).

**REM 0103** (no. 103, p. 40)

1. Mine: `qo mstrq : qo : wosi : bedewi | psdk : pro h̲eñ : dḫ[e?] : wiyleb :`
2. FHN, stone lines 1 to 3: `qo Mstrq : qo : Wosi : Bedewi *ksdk : proḫeñ : dḫe : wiyleb :`
3. Differences: `psdk` against `*ksdk`. The type has a rounded p, with Griffith's "?" above it, and FHN marks its k
   uncertain (G ≠ F). `h̲` against `ḫ`: the type has the angular h̲, not the c-shaped ḫ (G ≠ F).

**REM 0104** (no. 104, p. 41)

1. Mine: `qo apmloqo pelmos adlito :`
2. FHN: `qo Apmlo qo pelmos ad(b)lito :`
3. Differences: FHN supplies the b in brackets, and the stone and the type have none (G ≠ F, editorial).

**REM 0105** (p. 37): mine `qo pelmos atolise mnitwwiqo`, the same as FHN. 22/22.

**REM 0106** (p. 38): mine `qo kroro bekemetelo pesetolo`, the same as FHN. 22/22.

**REM 0107** (p. 38): mine `qo kroro bekemetelo | pelmos adblito`, the same as FHN. 28/28.

**REM 0108** (no. 108, p. 41)

1. Mine: `snneblilo mseqeto`, with an uncertain mark on the e of `mseqe`.
2. FHN: `Snñ*blilo mseqeto`
3. Differences: the type plainly has two n signs and an e (`ꝶꝶς`) where FHN reads n + ñ (G ≠ F). Griffith's
   "Shananebli" fits his type.

**REM 0109** (p. 41): mine `qo : mstrqoye wosqerlo`, the same as FHN (Griffith marks the o "sic"). 18/18.

**REM 0111** (no. 111, p. 41, foot of the left column and head of the right)

1. Mine: `qo qoreñ wosse perite wosse wos | qer mstrq : ye yewi wosi yntke | lw pibr ph̲e qleb ksbñ wosse | bto skel nḫeñ`
2. FHN: `qo qoreñ Wosse perite Wosse Wos qer Mst(rqo)ye *qewi W*osi yntkelw pibr pḫeq*leb ksbñ Wosse bto skelnḫeñ`
3. Differences: the type has a divider ":" where FHN supplies o (G ≠ F). The type has `///` (y) where FHN reads `*q`
   (G ≠ F). `ph̲e` against `pḫe`: FHN's diacritic is unclear on the scan (unclear).

**REM 0119/0120** (nos. 119/120, p. 45; fully blind)

1. Mine: `yeseboh̲e tniqo : qoro : m?ret | me(y)te : tlo : wos selo :`
2. FHN 0120: `Yesebohemniqo : qoro : mretmeteyte : tlo : Wosselo :`
3. FHN 0119, for comparison: `Yesebohemniqo : qoro : mret metet : lo Wosselo :`
4. Differences: the type has t (hooked, with the dot) where FHN reads m in the royal name Yesbokheamani, which needs
   m (G ≠ F, probably Griffith's misprint or misreading). The type has `me(y)te` where FHN 0120 has `meteyte`, one te
   fewer (G ≠ F). FHN's h diacritic is illegible on the scan (unclear).

## 6. Confusions

My errors:

| Read | Should be | Count | Where | Why |
|---|---|---|---|---|
| m | h̲ (ẖ) | 2 | 0097 l. 3 (`womneth̲`), 0102 l. 2 (`pḫilh̲`) | Both are 3-shaped with a long descender. h̲ has a pointed `>` middle and m a smooth curve, which is visible at 2.5x but not at 1x. Both were marked "[m?]". |

Near-confusions that the reference strip or a zoom resolved, all correctly: p against k (rounded ε top against flat
Z top); m against s (open with a long tail against a closed 3); t against l (dot and hook against an angular 5); q
against o + q (`/ɔ` is one sign, `//ɔ` is "qo"); ñ against n + e; y against se.

## 7. Where Griffith and FHN differ (not my error)

| REM | Griffith's type | FHN | Backed by |
|---|---|---|---|
| 0097 | `womñt-` (ñ) | `womnet-` (n + e) | zoom (`disp2.png` I) |
| 0097 | `sqte-` | `sqote-` | zoom (H); Griffith's "shaqate" |
| 0097 | `stoh̲e-` | `sto*se-` | zoom (G); Griffith's "malêshatêkhe" |
| 0098 | `mte` | `ste` | zoom (`disp1.png` C) |
| 0098 | `× n kelbo` | `35 kelbo` | zoom (L) |
| 0102 | `pikl`, `pikn` | `pipl`, `pipn` | zoom (D, E) |
| 0103 | `psdk` (Griffith's "?") | `*ksdk` | zoom (F) |
| 0103 | `proh̲eñ` | `proḫeñ` | zoom (N) |
| 0104 | `adlito` | `ad(b)lito` | FHN's own brackets |
| 0108 | `snneb-` | `snñ*b-` | zoom (K); Griffith's "Shananebli" |
| 0111 | `mstrq : ye` | `Mst(rqo)ye` | zoom (`vv111.png`) |
| 0111 | `yewi` | `*qewi` | zoom (M) |
| 0120 | `…h̲e tniqo` | `…hemniqo` | zoom (`disp5.png`) |
| 0120 | `meyte` | `meteyte` | zoom (`disp4.png`) |

Panel letters refer to `disp1.png` (A to F) and `disp2.png` (G to O). Six of the 18 sign differences fall on signs
that FHN itself marks uncertain (`*`) or supplies in brackets. FHN III no. 267 describes the scribe as working
crudely, and Griffith calls no. 111 "ill-written". The zooms are my own second look at the type, not an independent
source. Griffith's commentary is independent, but it backs only three of the 18.

## 8. Speed, and what would make it faster

Wall-clock times are taken from the save timestamps in `readings.md`:

| Step | Texts | Signs | Time |
|---|---|---|---|
| Setup (sign table, strip, finding the Philae pages) and no. 97, the first text | 1 | 103 | 09:24–09:34, 10 min |
| Nos. 98, 106, 107 (p. 38) | 3 | 122 | 2.2 min |
| Nos. 102, 103 (p. 40), with zooms | 2 | 93 | 2.6 min |
| Nos. 104, 108, 111 (p. 41) | 3 | 111 | 1.3 min |
| Nos. 105, 109 (inline on pp. 37, 41) | 2 | 40 | 1.1 min |
| No. 119/120 (p. 45), from download to reading | 1 | 33 | 1.2 min |

After the first text, 399 signs took 8.4 minutes: about 45 signs a minute, or 1 to 3 minutes for a page of type
(50 to 110 signs). Finding the type lines among Griffith's English took about as long as reading them. The whole
test, scoring and report included, took about 35 minutes.

What would make it faster and cleaner:

1. **A fixed crop pipeline driven by archive.org's OCR word boxes.** The `_djvu.xml` gives coordinates for every word,
   and the type lines come out as garbage words with low confidence. Selecting those lines would find every text
   without a person, or the model, ever seeing Griffith's English. A line-height test alone (type at least 46 px tall
   at this scan) also caught some English lines.
2. **The reference strip above every crop.** This was used throughout, and it settled p against k and s against m.
3. **A forced 2.5x zoom on every sign marked uncertain**, against clear examples of its confusable set (m, h̲, s, k,
   w; p and k; t and l). Both errors were signs I had marked uncertain; this rule alone would have caught them.
4. **Two independent readings compared**, kept for the flagged signs only. With 2 slips in 502 signs, a full second
   pass doubles the cost to catch about 0.4%.
5. **Keep Griffith's superscript line numbers in the output.** They align each text with REM line by line.

## 9. Contamination and limits

1. **Griffith's English, seen before reading:**
   1. Nos. 97 and 105: the full translations under the type, including Manitawawi, Bekemete, pelamêš, khabkhañ and
      shaqate.
   2. No. 98: the first line of its translation ("akrêrê, second(?) Beke-"), plus Amani, pesatê and azab on a locator
      sheet.
   3. Nos. 99, 100, 102, 103, 104 and 109: Mashtaraq(aye), Apamalê, Pênani, Bezewe and Patrêt on the pp. 40–41 locator
      sheet.
   4. No. 108: Shananebli and Masaqe in the commentary.
   5. No. 111, ll. 1 and 2: the translation.
   6. Not seen: nos. 106, 107 and 119/120.
2. **FHN:** only the REM ids, line numbers and the masked layout before each freeze. The scorer input had two typing
   slips against the frozen file (`womñetm` for `womñt[m?]`, `qorene` for `qoreñ`, where my "ne" meant the ñ sign).
   Both were corrected to the frozen text before the final score.
3. **Prior knowledge:** the funerary and Philae formula words (qo, pelmos, wos, qore). The meaning of lh̲ ("great") was
   used once, to choose h̲ over m in no. 97 l. 6, which FHN confirms.
4. **FHN's h diacritics** were read from 1926-px scans. Two stay unclear and are not counted against the reading.
5. **Not done:** nos. 99, 100, 101 and 110. Nos. 99, 100 and 110 are printed inline in the commentary and their English
   had been seen; no. 101 is long and interleaved with commentary.
6. **Not tested:** *Meroitic Inscriptions* I, *Meroë*, and the hand copies of Karanòg and Faras.
7. **No account and no credential were used.** Only page images and metadata were downloaded. No repo file other than
   this one was changed, and nothing was committed.

## 10. Files

All of these are outside the repo:

1. `/private/tmp/claude-501/griffith/`: archive.org metadata and page-number JSON for MI I, MI II and Karanòg; MI II
   leaves `mi2_n17`–`n20` and `n52`–`n64` (JPEG, about 3107 x 4130 px); FHN III page composites `fhn3_p281`–`p283`
   and `p305`.
2. `/private/tmp/claude-501/griffith_scripts/`:
   1. Scripts: `crop.py`, `thumb.py`, `strip.py` (the sign strip), `compose.py` (the strip above a crop), `bands.py`
      (line finder), `zoomsheet.py`, `score.py` and `score2.py` (the scoring).
   2. Readings: `readings.md`, `readings_frozen_094128.md`, `readings_frozen2_094928.md`.
   3. Images: `signstrip.png`, and the zoom sheets `disp1.png`, `disp2.png`, `disp4.png`, `disp5.png`.
