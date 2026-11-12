# The same people in Demotic, Greek and Meroitic

Run on 2026-11-12 with `src/demotic.py`, on the clean corpus's day. *Fontes Historiae Nubiorum* III prints, in
translation, 22 Demotic graffiti and two Greek inscriptions from Philae, Dakka and Maharraqa, and the Meroitic
epitaphs and inscriptions of people of the same families. This page sets them side by side: who appears in two
languages, which titles he carries in each, and where the editors set a Meroitic word beside a Demotic or Greek
one. It is the last open part of step 17 of [`NEXT_STEPS.md`](../../NEXT_STEPS.md). The numbers are in
[`demotic_figures.json`](demotic_figures.json) and are checked by `tests/test_demotic.py`.

## 1. Answer first

1. **Four people carry a title in Meroitic and in Demotic or Greek, and their titles line up as the lexicon
   says.** `perite` stands where the Demotic has "agent" (`rt`) for two of them; `peseto` where the Demotic has
   "the king's son" (`sy-nsw`) and the Greek `psentes` for one; `kroro` where the Demotic has `3krre` for one.
2. **The editors set 125 Meroitic words or phrases beside a word of another language or give them a meaning.**
   For the 64 different lines whose word our map translates, two judges agree with the map's reading on 36 of 58
   and on 41 of 57.
3. **It adds no meaning that is new and sure.** What the map lacks is mostly titles that the editors leave as
   titles too. The equations that say more than the map: `qoreñ` as a title built on `qore` "ruler" (Demotic
   `krny`), `arbetke` (Demotic `3rbtgy`) as a title of priests with economic duties, and the phrase
   `apote-lẖ Arome-li-s`, which a Demotic graffito of the same year gives as "the great envoy to Rome".
4. **Both bars set before the run were met** (section 5).

## 2. What was read

- **The entries:** 229 to 306 of FHN III for the Demotic and Greek texts (24 entries), and nine entries on
  Meroitic texts (246, 247, 264, 267 to 271, 291). The volume is in copyright and is kept on the author's
  machine; its text layer is an OCR of a scan.
- **The readers:** three Claude Opus 5.5 agents, each told to read its pack and nothing else: two on the Demotic
  and Greek entries, one on the Meroitic ones. A reader lists every person that an entry's ancient text names,
  with the titles the text gives him (as the editors translate them, and in the original where the entry prints
  it), his kin, and whom the editors take for the same person in another entry; and every place where the
  editors set a Meroitic word beside a Demotic, Greek or Egyptian word or give it a meaning.

| Reader | Person lines | Equations |
|---|---|---|
| Demotic and Greek entries, first | 74 | 28 |
| Demotic and Greek entries, second | 74 | 30 |
| Meroitic entries | 61 | 85 |

## 3. The people

The person lines are joined into people: two lines are one person when they carry the same name in the editors'
English, with its letter for namesakes, or when the editors say so. That gives 97 people, 21 of them in two
entries or more. Four have a title in a Meroitic text and a title in a Demotic or Greek one:

| Person (entries) | In Demotic or Greek | In Meroitic |
|---|---|---|
| Beke (244, 246) | "qêreñ of Isis", "agent of Isis" (`rt n 3st`) | `perite`, "agent" |
| Manitawawi (246, 247, 249, 252, 267) | "agent of Isis", "agent of the King of the Land of Nubia", "hont-priest of Isis" | `Wos-se perite`, "agent of Isis"; `ant qori-se`, "hont-priest of the king"; `qoreñ` |
| Abratoye (260, 265, 270, 271) | "the king's son" (`p3 sy-nsw`); in Greek `psentes` of the king of Aithiopia | `peseto`, `peseto Akiñ-te` |
| Bekemete (261, 267) | `3krre`; "general of the water" (`mr-mšꜥ n p3 mw`) | `kroro`; `pelmos adbli-se`, "strategus of the land" |

The identifications are the editors'. For Bekemete the Demotic text has the general "of the water" and the
Meroitic one the `pelmos` "of the land": two offices, held at two times or by two namesakes; the editors
discuss it and this page does not decide it.

## 4. The equations

The three readers list 143 equations; 18 only set two spellings of a name side by side and are left out. The
other 125 are 110 different lines by word and meaning. Each word was looked up as the coverage map looks a word
up (`src/experts/missing.py`):

| How the map holds the word | Lines |
|---|---|
| translated | 64 |
| a proposal only (hypothesis) | 8 |
| the kind only | 12 |
| not in the map | 26 |

For the 93 lines where the map has any reading, two judges compared the editors' meaning with ours, each with
decoys of its own in place of our reading (8 and 9), as in [the check against two editions](experts.md). On the
lines whose word the map translates, the first judge agrees with our reading on 36 of 58 and the second on 41 of
57; on the 51 both saw with our reading they gave the same verdict on 46 (Cohen's kappa 0.81). Neither accepted
a decoy.

53 of the 110 lines are on a word or phrase that the check against the two editions had not listed.

What goes on the list of what the map lacks:

| | Lines | Stated as sure by the editors |
|---|---|---|
| the map has no accepted meaning for the word | 46 | 29 |
| the map translates the word and both judges say the editors read it otherwise | 15 | 8 |
| the same, on the word of the one judge who saw our reading | 5 | 2 |
| the same, one judge of two | 3 | 3 |
| all | 69 | 42 |

What is in it:

1. **Titles that the editors leave as titles:** `akroro`, `womnise`, `ḫbḫñ`, `ttñ`, "great" before each of them.
   The map has them as a kind or a proposal; the editors know no more.
2. **`qoreñ`:** "a frequent title" in the map; for the editors a title built on `qore`, "ruler", perhaps "the one
   belonging to the ruler", written `krny` in Demotic, where its holders are "qêreñ of Isis" and "qêreñ of the
   king".
3. **`arbetke`:** a title in the map; Demotic `3rbtgy`, for the editors a title of priests with economic duties,
   with a question mark on the detail.
4. **`apote-lẖ Arome-li-s`:** the map reads `apote-lẖ` as "great envoy" and does not hold the second word; the
   Demotic graffito of Pasan (AD 253) has "the great envoy to Rome" for the same office.
5. **The same differences as before:** `ant` ("priest" in the map; "hont-priest", "prophet"), `pelmos` ("general";
   "strategus, district commissioner"), `mete`, `tebwe` (the Abaton or Thebes), `nlote` (Karanòg or Aniba), and
   the ending `-te`, which a lookup of the bare ending gets wrong.
6. **Artefacts:** 4 of the 26 lines "not in the map" are words the map holds, misread by the OCR (`ri` for the
   letter ñ: `Akiri` for `Akiñ`); and two of our readings reached the judges cut short.

## 5. How far to trust it

1. **The bars, written before any reader answered.** The two readers of the Demotic and Greek entries should list
   the same person in at least 80% of each other's lines: they do in 72 of 74 (97.3%). Both should find at least
   four of five known equations (`pelmos`, `perite`, `ant`, `qoreñ`, `peseto`): both find four; `ant` is in the
   Meroitic entries only, where the third reader finds it.
2. **One reader for the Meroitic entries,** so the 85 equations from there have no second witness. Most of them
   are meanings the check against the two editions had already listed from the same entries.
3. **The identifications are the editors' own,** and so are the equations: this is a reading of one book, not an
   independent bilingual. What is independent of the lexicon is the Demotic and Greek wording of the titles.
4. **Four people are few.** They confirm three titles; they cannot weigh a rare one.
5. **The judges** are the same model with the same instructions; their agreement shows stable verdicts.

## 6. Files and rebuild

| File | What it holds | Where |
|---|---|---|
| `src/demotic.py` | the entries cut from the volume's text, the packs, the join of people, the table for the judges, the count | public |
| `tests/test_demotic.py` | the method on made-up lists, and the numbers of this page | public |
| `demotic_figures.json` | every number of this page | public |
| `data/sources/demotic/` | the packs, the readers' and judges' answers, the people with their titles, the lists | local |

```
python3 -I src/demotic.py packs      # refuses once a reader has answered
python3 -I src/demotic.py merge
python3 -I src/demotic.py table      # refuses once a judge has answered
python3 -I src/demotic.py count
python3 -I tests/test_demotic.py
```

**Cost,** from the task notifications, by hand: three readers 384,658 subagent tokens (136,380, 138,439 and
109,839), two judges 126,264 (62,952 and 63,312); about three minutes each for the readers and half a minute for
the judges. The review is counted in [`REPORT.md`](../../REPORT.md).
