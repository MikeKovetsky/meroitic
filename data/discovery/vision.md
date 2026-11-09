# Can the model read Meroitic cursive from a photograph?

Run D_vision, 2026-11-09, 08:14 to 08:43 PST, by Claude Opus 5.5 (`runs/prompts/D_vision.md`).

## 1. Answer first

**No.** On four inscriptions in five openly licensed photographs, the model got 0 of about 80 signs on the
Hamadab stela and none of the three personal names on the Karanog offering table. On the one clean, deeply cut
stela (BM EA 1585) it found lines, word dividers and the reading direction, and it split about 150 signs. But it
could not give most of them values. Of the roughly 30 words on that stone, its 15 lines yield three
recognisable ones: `wos`, `asori?` and `terike-` (l. 14). `tedḫe`, which nearly every Nubian epitaph carries,
is not among them.

| # | Photograph | Inscription | Published reading reached? | Signs right / signs in the published text | Words fully right |
|---|---|---|---|---|---|
| 1 | Hamadab stela, two photos | REM 1003, BM EA 1650 | Yes: FHN II no. 176 and the Otten corpus file | **0 / about 80** (lines about 2 and 24) | **0** |
| 2 | Karanog offering table (Griffith 1911 plate) | Kar. 1 or Kar. 24 (identification uncertain) | Partly: Griffith 1911 prints names in English rendering and formula letters, not a sign transliteration | Not scorable at sign level | **Names: 0 / 3** (for either candidate) |
| 3 | BM EA 1585, stela with tenon (left stela in the photo) | Probably Faras (registration 1912 points to Griffith's Faras dig); REM number not found | **No.** The BM collection site refused the fetcher (HTTP 403); Griffith's Faras corpus (1922) and REM (2000) are print only | Not scorable | Not scorable. Three recognisable words out of about 30 (`wos`, `asori?`, `terike-`), all formula words |
| 4 | Sai stela | REM 1273 | **No.** REM and the catalogue no. 313 cited on Commons are print only | Not scorable | Not scorable (one line attempted) |

What a reader needs to know before using these numbers:

- **Only one image has a sign-level gold**, and it is the hardest one (worn sandstone). The clean photos
  (EA 1585, Sai) have no published transliteration reachable online in the hour, so they are judged by an
  internal check (section 3, image 3), not by a score.
- **The reading used a sign chart.** The model's own memory of the cursive letter shapes was too weak to start
  from, so it used the public-domain chart
  [File:Meroitic.png](https://commons.wikimedia.org/wiki/File:Meroitic.png) (Hintze values, printed font forms).
  That is what a human beginner would do. The chart's font forms differ from the carved hands, and that gap is
  the main source of error.
- **The blind rule was kept.** All readings were written to a timestamped file (08:27:25, 08:31:21, 08:33:05
  PST) before any published text was opened (first fetch after 08:33). The contamination that did happen is
  listed in section 5.

## 2. Images

All files are in `/private/tmp/claude-501/vision/` (images only, all from `upload.wikimedia.org`). Scripts and
crops are in `/private/tmp/claude-501/vision_scripts/`. Pillow came from the Viewfy backend venv
(`python -I`), because the system `python3` has no PIL.

| File | Used for | Licence | URL | Bytes | Pixels |
|---|---|---|---|---|---|
| `hamadab_peel.jpg` | Image 1 | CC BY-SA 4.0, Mike Peel | https://upload.wikimedia.org/wikipedia/commons/b/b5/At_the_British_Museum_2024_318.jpg | 22,530,475 | 4640 x 6960 |
| `hamadab_bm02.jpg` | Image 1 (close-up) | CC BY 3.0, Pymouss | https://upload.wikimedia.org/wikipedia/commons/f/fb/British_Museum_-_Hamadab_Stela_02.jpg | 14,085,286 | 5472 x 3648 |
| `karanog_altar.png` | Image 2 | Public domain (Griffith 1911) | https://upload.wikimedia.org/wikipedia/commons/e/eb/Karanog_altar.PNG | 868,305 | 692 x 769 |
| `bm_ea1585_and_sai.jpg` | Images 3 and 4 | CC BY-SA 3.0, Piero d'Houin dit Triboulet | https://upload.wikimedia.org/wikipedia/commons/2/2e/%C3%89criture_m%C3%A9ro%C3%AFtique_cursive.jpg | 3,644,513 | 3278 x 2047 |
| `sai_rem1273.png` | Image 4 | GPL (uploader Mustafaa, en.wikipedia) | https://upload.wikimedia.org/wikipedia/commons/8/8f/Meroitic_stela.png | 1,633,141 | 728 x 1164 |
| `signchart_meroitic.png` | Sign key | Public domain | https://upload.wikimedia.org/wikipedia/commons/b/b6/Meroitic.png | 30,682 | 1932 x 2419 |

These 1280-px thumbnails were downloaded only to screen candidates. They came from the same host, under
`/wikipedia/commons/thumb/...`, and were not read for the test:

- `t_hamadab_bm01.jpg`: CC BY 3.0, 839,055 B.
- `t_hamadab_bm02.jpg`: CC BY 3.0, 567,032 B.
- `t_hamadab_j1.jpg`: CC BY-SA 3.0, 701,958 B.
- `t_hamadab_peel.jpg`: CC BY-SA 4.0, 716,236 B.
- `t_ecriture.jpg`: CC BY-SA 3.0, 238,343 B.
- `t_munich.jpg`: Munich ÄS 2624, REM 1195. CC BY-SA 3.0, 566,277 B.
- `t_amanikhatashan.jpg`: CC0, 216,622 B.
- `t_sedeinga.jpg`: CC BY 3.0, 236,890 B.
- `t_mesa.jpg`: CC BY-SA 4.0, 222,045 B.
- `t_walters_back.jpg`: Walters 22.258. Public domain, 426,997 B.

The full manifest with timestamps is `/private/tmp/claude-501/vision_scripts/manifest.tsv`.

Four candidates were dropped because no published transliteration could be reached: the Munich block (REM 1195,
the clearest large-sign photo), the Walters Tanyidamani plaque, and the Sedeinga and Madrid offering tables.
The Walters and BM sites return 403 to the fetcher, and FHN II (42 MB PDF) is over the fetch limit.

## 3. Readings and comparison, per image

Convention: right to left; `:` is a divider seen on the stone; `?` marks an uncertain sign; `[.]` marks a sign
that was seen but not identified.

### Image 1. Hamadab stela, REM 1003 (BM EA 1650)

- **Photos:** [Mike Peel 2024](https://commons.wikimedia.org/wiki/File:At_the_British_Museum_2024_318.jpg)
  (whole stela), and the [Pymouss close-up](https://commons.wikimedia.org/wiki/File:British_Museum_-_Hamadab_Stela_02.jpg)
  (about lines 16 to 31).
- **Published:** FHN II no. 176, pp. 719-723 (ll. 1-15, as cited in `data/leads/02-war-with-rome.md`), and the
  Otten corpus file `data/otten/Data/HamadabStelaOfAmanirenasNarrative.txt`. That file has about 1,680 signs over
  42 lines, so about 40 signs a line.
- **Model reading:** the first clear line under the relief (about l. 2; crops 1.15x and autocontrast) and line 9
  of the close-up (about l. 24). The model could see that the lines are there and roughly where the signs fall.
  It could not separate the signs from the grain of the sandstone, and it identified **no sign** with any
  confidence. The written reading for l. ~24 is `[.] [.] a? [.] :? [.] y? [.] ...`, which is too little to align.
- **Score:** 0 of about 80 signs, and 0 words.
- **Error kind:** wear and grain. At this resolution the strokes are no deeper than the surface texture. The
  published text was established from the stone and squeezes, not from photos like these.

### Image 2. Karanog offering table (Griffith 1911 plate)

- **Photo:** [File:Karanog altar.PNG](https://commons.wikimedia.org/wiki/File:Karanog_altar.PNG). It is a 1911
  halftone at 692 x 769 px. Its Commons source points to the
  [plate](https://archive.org/details/karangmeroitic00grifuoft/page/n199) and to
  [p. 54 for the description](https://archive.org/details/karangmeroitic00grifuoft/page/54).
- **Which text:** the OCR of the [other scan](https://archive.org/details/karanogmeroitici00grif) puts the
  Chapter VI introduction and **Kar. 1** on p. 54. Kar. 1 is "Altar of fine pink sandstone", Cairo 40121,
  formulae A B. The decoration, a pylon-shaped altar in the sunk field that the text ends on, matches
  **Kar. 24** better: Philadelphia 7088, formulae ABC. The identification is open.
- **Published:** Griffith 1911 prints no sign-by-sign transliteration in the OCR, only the names in his English
  rendering and the formula letters:
  - Kar. 1: "Asheye or Akheye ... of Amanap", father "Masakhte-Trebihti" (restored), mother "Sharbiye"; formulae A, B.
  - Kar. 24: "Sharbetanize, born of Kharakebe, begotten of Yeyamakhar"; formulae ABC.
- **Model reading (blind):**

  ```
  Spout, right column:    wosi? :
  Spout, left column:     [.] o? [.][.] :
  Spout, middle column:   m? t? : | [.] l? y? [.] e k? l? s s?
  Top border, left part:  s o r e [.] y i      ("soreyi"?)
  Top border, right part: e? y s e te? r [.][.]
  Left side:              t? n [.][.] y [.] k e [.] l? s e y [.]
  Right side:             e? te? : s r r? o
  Bottom, central altar:  not read
  ```

- **Score:** names 0 of 3 for either candidate; no reading resembles them. The invocation `wosi : soreyi` is
  plausible but unverified, because Griffith's summary does not print the invocation.
- **Error kind:** resolution (signs are 12-20 px), text running round the border and needing rotation, and the
  formula prior (below).

### Image 3. BM EA 1585, stela with tenon (left stela in the photo)

- **Photo:** [File:Écriture méroïtique cursive.jpg](https://commons.wikimedia.org/wiki/File:%C3%89criture_m%C3%A9ro%C3%AFtique_cursive.jpg).
  The stela shows "1585" on the tenon and "1912 11-9 608" at lower left, so BM EA 1585, reg. 1912,1109.608.
  That number range is the 1912 distribution of the Oxford excavations at Faras (EA 1576 is a Faras offering
  table); this is an inference, not confirmed. It has 15 ruled lines, deeply cut, and is sharp at about 90 px a line.
- **Published:** not reached. The BM page returns 403. Griffith, *Meroitic Funerary Inscriptions from Faras,
  Nubia* (1922) and REM (Leclant et al. 2000) are in print only.
- **Model reading (blind, R to L, best guess):**

  ```
  L1  wos weaḫyi?ḫ? asori? : kse?          [alt.: second group s?o?r?e?yi = soreyi?]
  L2  t? : wea? ato?rte? : nos[.]no[.]e[.][.]b?
  L3  ywte? : tlei | yse : se[.]
  L4  yeiosebl? : | syeltolei o
  L5  wi : torrte?s | s[.]se : l[.]
  L6  te?te? : kei | [.]se[.]r :
  L7  yeltne[.] | eowete? : lr
  L8  te?sese : l | lse[.][.]re
  L9  te? : te?qs | ill[.]e :
  L10 ye[.]tnei | te?w[.] : [.]ey
  L11 lte?[.]to : | : te?n[.]ete?
  L12 sn[.] : ste?[.]t | ry[.] : [.]ste?
  L13 yete?so : | s[.]tete?td?
  L14 te[.]l : te?r | rikete? : tso
  L15 te?
  ```

- **Internal check (no gold):** a Lower Nubian epitaph names the mother with `tedḫe` and the father with
  `terike-` (`terikelowi`), and ends with benedictions (`ato mhe ...`, `at mhe ...`).
  - The reading has `tedḫe` nowhere, and no benediction.
  - It has `terike-` once, at l. 14: `te?r | rikete?`. The `r` is counted twice because the two half-crops
    overlap, so it reads `terikete?`. That supports `/`+cross = `te`, wave = `r`, cross = `i`, `2` = `k` and
    `S` = `e` in this hand.
  - Besides that, only `wos` (Isis) and `asori?` (Osiris) came out. Those are exactly the words a
    formula-primed reader expects in line 1.
  - So three recognisable words out of roughly 30. Most of the other sign values are unverified and probably
    wrong.
- **What the model did right:** reading direction (the short last line is right-aligned), line count,
  dividers, and sign segmentation.
- **Error kind:** the "3" family. `s`, `m`, `k`, `ẖ`, `w` and a vertical `r` are all 3-like in this hand, and the
  model could not separate them. It could not decide whether `/` plus a cross is `te` or `o` plus `i`, nor
  whether `///` is `y`, `se` or `i` plus `y`. And it kept forcing the formula onto the signs.

### Image 4. Sai stela, REM 1273

- **Photos:** [File:Meroitic stela.png](https://commons.wikimedia.org/wiki/File:Meroitic_stela.png), 728 x 1164.
  The same stone is the right stela in image 3's photo.
- **Published:** not reached. REM 1273 is in print only. The Commons note "Cat no. 313" probably refers to the
  catalogue of the BM's 2004 exhibition *Sudan: Ancient Treasures*; this is an inference. The caption on
  [de.wikipedia](https://de.wikipedia.org/wiki/Meroitische_Sprache) gives only "REM 1273". The other nine wikis
  that use the photo were not checked.
- **Model reading (blind), line 1 only:** `wos? te? : sos? (or sor-?) [....]`. The other 8 lines are too shallow
  at this resolution for the model.
- **Score:** not scorable.

## 4. Verdict

The model cannot read Meroitic cursive from photographs well enough to help check disputed readings or read
unpublished stones. On worn or low-resolution stones it cannot segment the signs at all. On a clean stone it
segments them but assigns values that are mostly wrong.

Its readings are also biased toward the expected formula. It "found" `wos`, `soreyi` and `asori` where it
looked for them, so it would tend to confirm whichever reading it was primed with. That is the opposite of
what checking a disputed sign needs.

What might change this, untested:

1. A palaeography of carved forms by site and period (Griffith's Karanog and Faras tables, Rilly's
   palaeography), shown next to each crop.
2. Raking-light or squeeze photographs at 100 px or more per sign.
3. Scoring on stones whose published text can be fetched. The next run should pick from texts whose
   transliteration is online first. [de.wikipedia](https://de.wikipedia.org/wiki/Meroitische_Sprache), for
   example, prints Griffith's and Hofmann's reading of the Karanog offering table REM 0246. Then look for an
   open photo of that same stone.

## 5. Contamination and limits

- **Seen before reading:**
  - The Commons description of `Meroitic stela.png` names the Sai stela's owner and father ("Waleye son of
    Kadite"). This did not matter, since the reading never reached the names.
  - One masked row of `data/texts.jsonl` (T0001, a funerary text with names as NAME) was printed by accident
    while checking ids. It shows formula vocabulary only.
  - The model knows the funerary formula from training and used it as a prior. That use is flagged in the
    readings.
- **Seen after reading:** the opening of the Otten Hamadab text, Griffith's renderings for Kar. 1 to 5, 23 to 25
  and others, and the FHN pointers in this repo.
- **Effort:** the run took about 29 of the 60 minutes (08:14 to 08:43 PST). Roughly 12 went on reading and
  18 on finding images and published texts.
- **Not done:** no account, no credential and no non-image download. No other repo file was changed, and
  nothing was committed.
