# Can the model read Griffith's Karanòg hand copies?

Work of 2026-11-09, 10:56 to 11:40 PST, by Claude Opus 5.5. Page images are in `/private/tmp/claude-501/expansion/karanog/`
and scripts, crops and readings in `/private/tmp/claude-501/handcopy_scripts/` (neither is in the repo).

## 1. Answer first

**No, not at 95%.** On the four Karanòg texts that FHN III prints in modern transliteration (Kar. 47, 77, 78 and 121 =
REM 0247, 0277, 0278, 0321), my blind reading of Griffith's hand copies agrees with FHN on **581 of 654 signs (88.8%)**,
and **81 of 125 FHN words** come out fully right (64.8%). Printed type, for comparison, reached 95.6%
(`printed_type_test.md`).

The 73 disagreements are of three kinds:

1. **50 are my misreadings** of what the copy shows.
2. **7 are a slip in writing down Kar. 77:** I read the last two words correctly as signs but wrote them in swapped
   order, which costs 7 signs in the alignment.
3. **16 are places where the copy itself differs from FHN or does not show the sign clearly:** Griffith hatched the
   sign as damaged, marked it "altered" or "sic", or it is lost at a break, or FHN restores it or stars it as uncertain.

So against what Griffith's copy shows, the reading is 581 of 638 signs (91.1%), or 588 of 638 (92.2%) without the
write-down slip. That is still below 95%.

Three findings decide the verdict:

1. **The errors are systematic, not random.** 46 of the 50 misreadings fall in five confusion sets (section 6): the
   3-shaped signs (m, ẖ, s and q written `/3`), 21; p against k, 7; `52` (a) against e followed by a long-tailed sign,
   6; te read as o + l, 6; e against l, 6.
2. **My uncertainty marks do not find them.** Only 23 of the 55 wrong signs I wrote carried a "?", and 68 of my 91
   "?" marks sat on signs that were right. Re-checking only the flagged signs, the fix that worked for printed type,
   would catch fewer than half of these errors.
3. **The errors fall in the new content.** Every invocation (`wosi`, `asoreyi`), filiation word (`tedḫelowi`,
   `terikelowi`), nomination ending (`qowi`, `qo`) and frequent title (`peseto`/`pesto`, `akiñtelo(wi)`, `yetmdelo`,
   `krorolo(wi)`, `ant`, `kdi`) and the water and bread formulae (`ato mẖe`, `at mẖe`) came out right. The two
   exceptions are one `tedḫelowi` where the copy itself has no e, and `pqrl` in Kar. 78, read `pqore` (`pqr` in Kar. 47
   was right). The misreadings sit in personal names, place names, rare titles and the benediction verbs, which is
   exactly what the corpus would gain from Karanòg.

**Speed:** setup (sign table, locating the pages) took 2.5 minutes. The first text, Kar. 47 (269 signs), then took
14 minutes, including building the sheet of confusable signs; Kar. 77, 78 and 121 took 4.7, 5.1 and 1.6 minutes
(27 to 41 signs a minute). That is 28 minutes for the four, 7 minutes a text on average. A fast pass from whole-row
images took under 1.5 minutes a text but marked 22.5% of signs uncertain, against 13.9% in the careful reading
(section 8).

**Verdict:** hand-copy reading is at about 89% against FHN and 91 to 92% against the copy itself, so it is not ready
for transcribing the 150 texts unchecked. Section 9 lists what would likely close the gap; each item is a hypothesis
until it is tested on texts with an independent reading, and FHN has no further Karanòg texts to test on.

## 2. The Karanòg hand: sign key

Source: Griffith's table "The Demotic Alphabet", Karanòg p. 19, column 14 "Kar."
([archive.org leaf n34](https://archive.org/details/karangmeroitic00grifuoft/page/n34)), cut into a strip
(`kar_strip2.png`, `cmp_strip.png`), checked against the copies. The forms are Unicode look-alikes of the hand.

| Griffith | FHN | Form in the Karanòg copies | Confused with (count of my errors) |
|---|---|---|---|
| a | a | `52`, an S and a 2 whose tail runs long to the lower right | e + k or d + e, when an S stands before a long-tailed sign (6) |
| e | e | `S`, larger | l (6) |
| ê | o | `/` | part of q (`/3`), part of te (`/ϟ`) |
| i | i | `4`; once `Ꮭ` with a bar | t (1) |
| y | y | `///`, `////` or `//` | o + y (1) |
| w | w | `б`, a closed loop under a flat top | — |
| b | b | `ν` with a hooked right arm | m (FHN marks that m uncertain) |
| p | p | `ξ` with a long tail to the lower right | k (7, both ways) |
| k | k | `Σ`-topped `Ʒ` with a long tail | p |
| m | m | `)` or `ℸ`, or a 3 with a short tail to the lower left | s, ẖ (3-shaped set, 21 in all) |
| ẖ | ẖ | 3 with a longer tail; once `ℸ` | s, m |
| s (Griffith's š) | s | closed 3 | m, ẖ, and `/3` = q against o + s or ẖ + o |
| q | q | `/3`, slash and 3 | o + s, ẖ + o |
| n | n | `ℛ`: a rising stroke, a 3 and a long tail; once `ʌ` with a long tail | ñ (1), d (1) |
| ñ | ñ | `ꭓ`, crossed strokes under a loop | d |
| d | d | `ϰ`, a rising stroke with a hook | ñ, n |
| r | r | `ω` | — |
| l | l | `ϟ`, small with a flat top | e (6) |
| ḫ | ḫ | `c` or `⊏`; in one place a 3 (FHN ḫ in `ḫẖll`) | — |
| se | se | `ʋ//` | — |
| t | t | `·ϟ`, a dot before a hook | — |
| te | te | `/ϟ` with a bar | o + l (6) |
| tê | to | `ب` with a dot below; `ɷ` | — |
| : | : | divider | — |

The trap named in the pilot is real and larger than expected: in this hand m, ẖ, s and q all take a 3-like shape,
and m also appears as `)`. Shape alone did not separate them on 21 signs.

## 3. Method

1. **Pages.** The hand copies were located from the page numbers in archive.org's OCR word boxes (`kar_djvu.xml`; the
   copy numbers sit under each text). Leaves downloaded from archive.org's page endpoint, 3132 x 4094 px:
   [n161](https://archive.org/details/karangmeroitic00grifuoft/page/n161) (p. 146, Kar. 47–48),
   [n171](https://archive.org/details/karangmeroitic00grifuoft/page/n171) (p. 156, Kar. 76–77),
   [n172](https://archive.org/details/karangmeroitic00grifuoft/page/n172) (p. 157, Kar. 78–79) and
   [n186](https://archive.org/details/karangmeroitic00grifuoft/page/n186) (p. 171, Kar. 121–123). The sign table
   leaves n33 and n34 were already there.
2. **Reading.** Each copy row was cut out and read right to left from crops at 1.25x, with 1.6x to 2.4x zooms on doubtful
   groups (`bands.py`, `rows.py`, `zoom.py`, `stack.py`). Griffith's superscript line numbers match REM's line numbers
   and were used only to check that the rows run continuously.
3. **Blind rule.** Each reading was appended to `readings.md` with a timestamp and copied to a frozen file:
   Kar. 47 at 11:12:43, Kar. 77 at 11:17:22, Kar. 78 at 11:22:27 and Kar. 121 at 11:24:03 (`readings_frozen_47.md` to
   `readings_frozen_121.md`). FHN's text was first opened at about 11:25, after all four were frozen. The pilot rows
   (`pilot.jsonl`) and the README's pilot table were never opened, and Griffith's English catalogue was not read.
4. **FHN text.** Taken from the FHN III page scans, PDF pages 274–275 (REM 0278), 288 (0247), 290 (0277) and 292 (0321),
   because the OCR drops the diacritics. At 3.5x the scans separate ḫ (breve below) from ẖ (line below).
5. **Scoring.** `score_hc.py` reuses the printed-type scorer: edit distance on signs, with se, te, to and ñ as one
   sign each and ḫ and ẖ distinct. Dividers, line numbers and FHN's `[=...]` forms are ignored; FHN's bracketed letters
   count as signs and its starred letters as read. My "[.]" (a lost sign) counts as no sign. Two fixes were needed in
   the tokenizer, not in the readings: my `arwte` is the five signs a r w t e, and my `ḫseo` is ḫ s e o (the tokenizer
   would merge t+e and s+e into te and se).
6. **Kar. 121 is scored on the spout only.** The copy shows only the spout of the offering table: the starts of stone
   lines 1, 7–8, 14–15 and 21–22. FHN prints the whole table (REM 0321, joined by Leclant), so only the matching
   stretches of FHN are scored: `(W)osi Sore`, `ant Boq(ḫ)w dik Pe`, `roẖeleb`, `btesw`, `kete ḫ mlol ẖol kete`.
7. **Second look.** Each disputed group was zoomed again to decide whether the copy shows FHN's sign (my misreading)
   or something else (`recheck_a.png` to `recheck_c.png`, plus the zooms in section 7).

## 4. Results per text

| Text | REM | Page (leaf) | FHN signs | Right | % | FHN words fully right | My misreadings | Copy ≠ FHN or unclear | Time |
|---|---|---|---|---|---|---|---|---|---|
| Kar. 47, stela | 0247 | p. 146 (n161) | 268 | 246 | 91.8 | 38/53 | 21 | 1 | 16.6 min: 2.5 setup, 14.1 reading |
| Kar. 77, offering table | 0277 | p. 156 (n171) | 134 | 106 | 79.1 | 13/27 | 9, plus 7 from the write-down slip | 12 | 4.7 min |
| Kar. 78, offering table | 0278 | p. 157 (n172) | 206 | 190 | 92.2 | 22/32 | 14 | 2 | 5.1 min |
| Kar. 121, table spout | 0321 | p. 171 (n186) | 46 | 39 | 84.8 | 8/13 | 6 | 1 | 1.6 min |
| **Total** | | | **654** | **581** | **88.8** | **81/125** | **50 + 7** | **16** | **28 min** |

Notes on the table:

1. **Kar. 77 with the two last words in the order the copy runs** scores 113 of 134 (84.3%) and 16 of 27 words, and the
   total becomes 588 of 654 (89.9%).
2. **Six of the README's words had been seen before reading** (`akiNtel`, `deklo`, `amoke`, `wwikel`, `sekesek`,
   `qorbt`, in its answer-first section). All six were read right. Without the 77 FHN signs in those words the score is
   504 of 577 (87.3%).
3. **Uncertainty marks:** 91 "?" on 651 signs written (13.9%); 23 of them on wrong signs, 68 on right ones.

## 5. The readings

Mine is the frozen text (right to left, "|" a copy row, "?" after an uncertain sign). FHN is given without its line
numbers, with `,,` shown as spaces.

**Kar. 47 (REM 0247)**

1. Mine: `qo : ḫ?witror qo : | peseto : akiñtelo : n?k? : akiñtelo : | ḫrpḫñ? k?mrsetelo : | l?ssslowoto : tb?qo :
   tmñ?telo : | qoredeklo : amoke : nl?otilo : | m?lom?rse : akiñtelo : wosnits? : akiñtelo : | ant : b?oqḫw : d?ik? :
   ked?emeyo?tito : | pqr : qorise : aetm?etñ? : tb?o : yetmdelo : | q?tnk?el? : yetmdelo : tb?ḫemḫr : yetmdelo : |
   l?itḫror : yetmdelo : | kdi : ap?w : k?nw : ḫtek?k?es?des?tee : mloto : | qore?sem?l?e : a?wekdil? : m?loto : arwte :
   m?loto : | m?lolo : tei?[.]we : wwikelo :`
2. FHN: `qo Ḫwitrorqo peseto Akiñtelo nk Akiñtelo ḫrpḫñ Pẖrsetelo lẖ smlo Woto tbqo Tmñtelo qore deklo amoke Nlotilo
   mlomrse Akiñtelo womnitẖ Akiñtelo ant boqḫw dik Pedemeyotito pqr qorise Atmetñ tbo yetmdelo Sotnkel yetmdelo Tbḫemḫr
   yetmdelo Litḫror yetmdelo kdi akw knw ḫte kke s destel mteto qorese mle Dewekdil mteto arwtl mteto mlolo Tebwe wwikelo`
3. Differences: `k?mrse-` against `Pẖrse-` (k for p, m for ẖ); `lsss-` against `lẖ sm-` (s for ẖ and m); `wosnits`
   against `womnitẖ` (s for m and ẖ); `ked-` against `Ped-`; `aetm-` against `Atm-` (the S of `52` read as e);
   `qtnkel` against `Sotnkel` (`/3` read as q); `apw` against `akw`; `destee` against `destel` and `arwte` against
   `arwtl` (e for l); `mloto` three times against `mteto` (te read as o + l); `awekdil` against `Dewekdil` (`Sꭓ` read
   as a); `tei[.]we` against `Tebwe` (the copy hatches this sign).

**Kar. 77 (REM 0277)**

1. Mine: `wosi : asoreyi : m?lotonqowi : | ḫdḫdiyoe : tedḫlowi : | d?k?retri : sm?l?d?y?i : terikelowi : | peseto :
   akiñtelowi : | bs?e[.][.]k?e ñ?ktetelowi : | wom?dise : krorolowi : | ato mh̲e : ps?te at mh̲e ps[.]ḫrate : | pq?lkete
   : ḫblol? :`
2. FHN: `Wosi Asoreyi Mlotonqowi ḫdḫiye tedḫelowi dk*retr*i Smedtli terikelowi peseto Akiñtelowi bel*i*l*oke
   Nptetelowi womnise krorolowi ato mẖe pẖte at mẖe ps(i) ḫr kete ḫ *mlol p ẖol kete`
3. Differences: the copy runs `ḫblol : pqlkete`; I wrote the two words in swapped order (7 signs). Mine: `ñkte-`
   against `Npte-` (ñ for n, k for p); `womdise` against `womnise`; `pste` against `pẖte`; `ḫrate` against `ḫr kete`
   (`S` + long-tailed k read as `52`); `pqlkete` against `p ẖol kete` (`/3` read as q); `ḫdḫdiyoe` against `ḫdḫiye`
   (the o is mine). The copy's own departures are in section 7.

**Kar. 78 (REM 0278)**

1. Mine: `wosi : asoreyi : ñ?tewitrqowi : | dk?re?tri : h̲?s?idt : terikelowi : | s?litrs?ii?de : ted?ḫelowi : | pesto :
   akiñtelowi | wleke krorolowi : | sekesekiñ? : s?s?ih̲?etelowi : | s?m?rso : krorolo : abso?lowi : | qorbtowi : nbr :
   wñ?l?it?kḫetelowi : | pqore : yetmdelowi : | ato mh̲e : psih̲ete : at mh̲e : ps?ḫ?ra?te : | ḫ?s?eol : yi?d?otedik?te :
   s?s?ll : p?s?iklte`
2. FHN: `Wosi Asoreyi Ñtewitrqowi dkretri Msidt terikelowi Mlitrqide ted(ḫ)elowi pesto Akiñtelowi wleke krorolowi
   sekesekiñ ssimetelowi smrso krorolo absolowi qorbtowi nbr wñli ipḫetelo wi pqrl yetmdelowi atomẖe psiẖete atmẖe
   psḫrkte ḫmlol yidetedikte ḫẖll psiplte`
3. Differences: `ẖsidt` against `Msidt`; `slitrsiide` against `Mlitrqide` (s for m, `s i` for q); `ssiẖe-` against
   `ssime-`; `wñlitkḫe-` against `wñli : ipḫe-` (the `Ꮭ` is i and the dot a divider; k for p); `pqore` against `pqrl`;
   `psḫrate` against `psḫrkte`; `ḫseol` against `ḫmlol`; `yidote-` against `yidete-` (the copy has o); `ssll` against
   `ḫẖll`; `psiklte` against `psiplte`.

**Kar. 121 (REM 0321), spout only**

1. Mine: `wo?si : sore[...] | antboq ḫw? : dik ke[...] | [...]rosl?leb : [...]btesw[...] | [...]kete : ḫseo[...]l? :
   s?o?lke[.]`
2. FHN, matching stretches: `(W)osi Sore | ant Boq(ḫ)w dik Pe | roẖeleb | btesw | kete ḫ mlol ẖol kete`
3. Differences: `ke-` against `Pe-`; `roslleb` against `roẖeleb`; `ḫseol` against `ḫ mlol`; `solke` against `ẖol ke`;
   the final te is broken off in the copy. Griffith's copy shows the ḫ of `Boq(ḫ)w`, which FHN restores in brackets.

## 6. My misreadings, by confusion set

| Set | Count | Examples (mine → FHN) | What would separate them |
|---|---|---|---|
| 3-shaped: m, ẖ, s, and q as `/3` | 21 | `ℸ` read m, FHN ẖ (`Pẖrse`); 3 read s or ẖ, FHN m (`smlo`, `Msidt`, `mlol`); `/3` read q, FHN s + o (`Sotnkel`) or ẖ + o (`ẖol`) | Shape alone failed. The lexicon decides: `smlo`, `mlol`, `ẖol kete`, `mẖe`, `pẖte`, `Pẖrse` |
| p and k | 7 | `ked-` → `Ped-`, `apw` → `akw`, `ke-` → `Pe-`, `psiklte` → `psiplte` | Rounded `ξ` top (p) against flat `Σ` top (k) is visible only at 2x and not always; titles and places decide |
| `52` against S + long-tailed sign | 6 | `aetm-` → `Atm-`, `awek-` → `Dewek-`, `ḫrate` → `ḫr kete`, `psḫrate` → `psḫrkte` | A is one sign whose 2 is a free stroke; an S followed by a k or d with its own tail is two signs |
| te against o + l | 6 | `mloto` → `mteto`, three times | The bar on the ϟ marks te |
| e against l | 6 | `destee` → `destel`, `pqore` → `pqrl`, `roslleb` → `roẖeleb` | Size: e is the larger S, l the small flat-topped ϟ |
| Others | 4 | ñ → n (`ʌ` with a long tail), d → n, t → i (`Ꮭ`), o + y → y | — |
| Write-down slip | 7 | two words of Kar. 77 in swapped order | A check that the frozen text runs in the copy's order |

## 7. Where the copy differs from FHN, or does not show the sign (16)

| REM | Copy | FHN | Signs | Backed by |
|---|---|---|---|---|
| 0247 | hatched sign, read `i` | `b` in `Tebwe` | 1 | Griffith's hatching (damage) |
| 0277 | `tedḫlowi`, Griffith writes "sic" over the l | `tedḫelowi` | 1 | Griffith's "sic" |
| 0277 | an extra `ꭓ` (d) joined to the i of `ḫdḫiye` | `ḫdḫiye` | 1 | zoom (`recheck_b.png`) |
| 0277 | `Smedtli` drawn hatched | `Smedtli` | 3 | Griffith's hatching |
| 0277 | group marked "altered" in `beliloke` | `bel*i*l*oke` (FHN stars three signs) | 5 | Griffith's note and FHN's stars |
| 0277 | hatched gap in `ps(i)` | `(i)` restored | 1 | FHN's brackets |
| 0277 | `ν` (b) in `mlol` | `*m` | 1 | FHN's star |
| 0278 | `pq/r`: a stroke between q and r | `pqrl` | 1 | zoom (`recheck_c.png`, e) |
| 0278 | `/` (o) in `yidote-` | `yidete-` | 1 | zoom (`recheck_c.png`, d) |
| 0321 | te broken off at the spout's edge | `ke*te` | 1 | the copy's break line |

The zooms are my own second look at the copy, not an independent source. The hatching, "sic" and "altered" are
Griffith's own marks, and the stars and brackets are FHN's.

## 8. Four more texts, read blind for speed

Read after the FHN comparison (as the task order asks), from whole-row crops at 0.75x and 1x with no zooms, so they
benefit from the lessons of sections 6 and 7 but have no ground truth. None of them is in FHN.

| Text | REM | Page (leaf) | Signs read | Marked uncertain | Time |
|---|---|---|---|---|---|
| Kar. 48, stela | 0248 | p. 146 (n161) | 70 | 21 (30.0%) | 1.3 min |
| Kar. 76, stela | 0276 | p. 156 (n171) | 111 | 31 (27.9%) | 0.9 min |
| Kar. 79, offering table | 0279 | p. 157 (n172) | 161 | 37 (23.0%) | 0.8 min |
| Kar. 122, offering table | 0322 | p. 171 (n186) | 133 | 18 (13.5%) | 0.7 min |
| **Total** | | | **475** | **107 (22.5%)** | **3.7 min** |

The readings are in `readings.md` (frozen in `readings_frozen_extra.md`). Consistency: the formula words come out the
same in all four (`wosi`, `(a)soreyi`, `qowi`, `terikelowi`, `tedḫelowi`, `yetmdelowi`, `ato mẖe`, `at mẖe`, `psiẖte`,
`psiḫrkte`, `ḫmlol`, `ẖolkte`), and two names recur from the scored texts: Kar. 79 has `msidt` beside `terikelowi`, the
father's name in Kar. 78, and `beloloke` in Kar. 122 matches `bel*i*l*oke` in Kar. 77. Those recurrences were read
after FHN had been seen, so they are not independent evidence. The fast pass doubles the uncertain share (22.5%
against 13.9%), and section 1 shows the uncertain share understates the error rate, so this speed is not usable as is.

## 9. What would likely raise the accuracy (hypotheses, untested)

1. **A per-hand rule sheet from section 6**, read before every text: te is the barred ϟ; `52` is one sign only when
   its 2 is a free stroke; e is the large S and l the small ϟ.
2. **A lexicon pass on every 3-shaped and long-tailed sign.** The misreadings above are mostly fixed by the attested
   words: `smlo`, `mlol`, `ẖol kete`, `pẖte`, `psḫrkte`, `psiplte`, `Pẖrse-`, `Pedeme-`, `mteto`, `pqrl`, `akw`. Names
   stay unchecked by this.
3. **A second reading of all 3-shaped and long-tailed signs**, not only the flagged ones, since flags caught 42%.
4. **A ground truth for the retest.** FHN prints no further Karanòg texts. Candidates: the REM edition (not online),
   Hintze or Millet where they cite Karanòg words, and, for names only, Griffith's English catalogue on pp. 54–78.

## 10. Contamination and limits

1. **Seen before reading:** the README's answer-first section, with six words of these texts (section 4, note 2), and
   its sign table (look-alike forms, values). Its `ʌ` for ñ misled me once (`Npte-`).
2. **Not seen before freezing:** FHN's text for these four, the pilot rows and the README's pilot table, and Griffith's
   English catalogue and commentary.
3. **Prior knowledge:** the funerary formulae (invocation, filiation, `ato mẖe`, `at mẖe`) and the title `peseto`.
   Section 1 shows these are the parts read right; the score on names and rare words is lower than the total.
4. **Kar. 121** is scored on 46 signs of the spout only, and FHN's restorations there come from the Tomas table.
5. **The extra texts** have no ground truth; their numbers are speed and the uncertain share only.
6. **No account or credential was used.** Only archive.org page images were downloaded. No repo file other than this
   one was changed, and nothing was committed.

## 11. Files

All outside the repo:

1. `/private/tmp/claude-501/expansion/karanog/`: leaves `leaf_161.jpg`, `leaf_171.jpg`, `leaf_172.jpg`, `leaf_186.jpg`
   (new), and the earlier `leaf_33.jpg`, `leaf_34.jpg` (sign table).
2. `/private/tmp/claude-501/handcopy_scripts/`:
   1. Readings: `readings.md`, `readings_frozen_47.md`, `readings_frozen_77.md`, `readings_frozen_78.md`,
      `readings_frozen_121.md`, `readings_frozen_extra.md`.
   2. Scoring: `score_hc.py` (sign and word scores, error list), `score_hc.json`, `flagcheck.py` (uncertainty marks
      against errors), `extra_stats.py`.
   3. Image tools: `nums.py` (copy numbers from the OCR boxes), `strip.py`, `cmp.py`, `bands.py`, `rows.py`,
      `fullrows.py`, `zoom.py`, `stack.py`, `signcmp.py`, `fhnpages.py`, `fhncomp.py`.
   4. Images: `kar_strip2.png`, `cmp_strip.png` (sign key), `cmp_dn.png` (d against ñ), `recheck_a.png` to
      `recheck_c.png`, and the FHN page composites in `fhn/`.
