# Cognates by regular sound correspondences: no real signal

**Answer.** A rule-based engine built on Rilly's correspondences finds no signal that generalises. On all 51
eligible gold words it beats 2,000 meaning shuffles (p = 0.026), but that comes entirely from the 20 words the
correspondences were built from (p = 0.0005 on those alone). On the 31 gold words the rules were not built
from, it does no better than chance (p = 0.58). Precision at the top is at chance (0.004 against 0.003, p = 0.17).
The test that decides whether candidate lists are earned was written into the code before the first run:
p < 0.05 on all gold words **and** on the held-out words. It failed, so **no candidate lists were produced**
for the 18 words of unknown meaning.

Code: `src/cognates_rules.py`. Tests: `tests/test_cognates_rules.py`. Run on 2026-11-09.

## 1. Validation numbers

Same design as `src/cognates.py`: for each Meroitic word, take the best score among NES words with the same
meaning (gloss keywords overlap), average over words, and compare with 2,000 shuffles of the Meroitic meanings
(seed 3; p counts the real pairing as one arrangement). Raw similarity is `cognates.sim` run on exactly the same
words, NES rows and spelling variants.

| Test | Words (with a same-meaning NES word) | Rule-based engine | Raw similarity |
|---|---|---|---|
| Mean best same-meaning score, all gold words | 51 (44) | 0.227; 50 of 2,000 shuffles ≥ real; **p = 0.026** | 0.253; 215 ≥ real; p = 0.108 |
| The same, held-out words only (not used to build the rules) | 31 (26) | −0.041; 1,152 ≥ real; **p = 0.58** | 0.192; 1,385 ≥ real; p = 0.69 |
| The same, the 20 rule words only | 20 (18) | 0.615; 0 ≥ real; p = 0.0005 | 0.342; 22 ≥ real; p = 0.012 |
| Precision at top-1, over all 5,442 NES rows and all meanings | 44 | **0.0043** (chance 0.0028); p = 0.17 | 0.0000 (chance 0.0028); p = 1.0 |
| Precision at top-1, held-out words | 26 | 0.0000 (chance 0.0022); p = 1.0 | 0.0000; p = 1.0 |
| Precision at top-10 | 44 | 0.0055 (chance 0.0028); p = 0.12 | 0.0020; p = 0.40 |
| Rank of the best same-meaning row among 5,442, median | 44 | 471 (in the top 10 for 3 words) | 551 (top 10 for 3) |
| The same, held-out words | 26 | 806 (top 10 for 1) | 1,124 (top 10 for 0) |

Precision at the top is the share of a word's top-scoring NES row (over every meaning) that carries the word's
meaning; when rows tie at the top, the share is taken over the tied rows (random tie-breaking). Only two words
have a same-meaning row among their tied top rows, and both are rule words: *kdi* 'woman' (2 of 42 tied rows,
Ama/Nyima *kírī* and *kiri* 'woman') and *ato* 'water' (1 of 7, Old Nubian *etu* 'water').

For reference, `src/cognates.py` as it stands (its own data, loans and names included) gives p = 0.115 (230 of
2,000), close to the raw row above.

## 2. Why p = 0.026 on all gold words is not a discovery signal

1. **The rules were fitted to these words.** Rilly derived the correspondences (his 2003 table, pp. 307–308) from
   17 lexical series: *abr, are-, ato, dime, dm-, ḫlbi, ḫre, kdi, ked, l-, lẖ, mte, pwrite, st, tre-, wle, yer*.
   His later prose rules cite *wide, abore, qore, nob, ms* as examples. An engine that encodes those rules
   re-finds those pairs by construction. 18 of the 44 scored words are such rule words, and they carry the whole
   effect: p = 0.0005 on them alone, p = 0.58 on the other 26.
2. **The rule words were chosen because they match.** Rilly picked the series for their NES resemblances, so
   even raw similarity beats chance on them (p = 0.012). Leaving each series out of the rules when scoring its own
   word would undo the first problem but not this one, so the held-out words are the fair test.
3. **The correspondences are many-to-many.** Each Meroitic consonant has three to six regular NES reflexes, and
   Meroitic writes few vowels, so a two- or three-consonant word fits hundreds of NES words regularly. *l-*
   'give' ties 242 rows at its top score; the median best same-meaning word ranks 471st of 5,442. The engine
   ranks true equivalents only slightly better than raw similarity does (471 against 551).

The held-out test is weaker than the rule-word test in one respect: its words have fewer comparanda (median 6.5
same-meaning NES rows against 10.5), and 10 of the 26 are compared with Hill Nubian (Ghulfan) alone, since only
that list has a culture vocabulary. Even so, the real pairing scores in the middle of the shuffle distribution
(p = 0.58), not near its edge.

## 3. Robustness: other cost settings

The decision used the default costs. These other settings were run afterwards and are all reported; none
changes the result.

| Setting | p, all words | p, held-out words |
|---|---|---|
| Defaults (near sound +0.3, irregular −1.0, missing −0.8, extra −0.6, other position ×0.7) | 0.0255 | 0.576 |
| Near sounds earn nothing (NEAR = 0) | 0.0280 | 0.630 |
| Irregular costs half (SUB = −0.5) | 0.0175 | 0.503 |
| Extra NES consonant costs half (INS = −0.3) | 0.0245 | 0.621 |
| Missing and extra both cost half (DEL = −0.4, INS = −0.3) | 0.0280 | 0.667 |
| Position-specific rules apply everywhere (×1.0) | 0.0215 | 0.545 |

## 4. Method

### 4.1 Words compared

1. **Meroitic.** `data/gold_lexicon.json`, minus deities, places and peoples (as in `cognates.py`): 62 words. Left
   out: 10 loans and 1 word of debated meaning, leaving 51.
   1. *ant*: Egyptian hm-ntr 'prophet' (gold note).
   2. *apote*: Egyptian wpwtj 'messenger' (gold note).
   3. *pelmos*: Egyptian p3-mr-msa 'the general' (gold note).
   4. *peseto*: named as a loan in the brief.
   5. *ssor*: Egyptian sš 'scribe' (gold note).
   6. *perite*: Egyptian, Coptic prit 'agent' (gold note).
   7. *nbr*: Egyptian nbw 'gold' (gold note).
   8. *tewiseti* (the brief's *tewisti*): Demotic 'adoration' (gold note).
   9. *kisri*: Greek Kaisar (gold note).
   10. *aroẖe-*: Lipiński compares Demotic hrh 'watch over' (gold note), so it may be a loan.
   11. *ḫrpḫe*: the gold lexicon marks its meaning as debated.
2. **NES.** The ten independent lists (Old Nubian, Nobiin, Kenzi, Dongolawi, Midob, Birgid, Hill Nubian, Nara,
   Taman, Nyima): 5,442 rows, 6,874 spellings. `proto_nes.tsv` is kept out (Rilly built it with Meroitic in view),
   and so are 226 Wiktionary rows that are proper names, alphabet letters or symbols (`pos` column).
3. **Held-out words.** The 31 eligible gold words that are neither in Rilly's 17 series nor cited in his prose
   rules: *asr, at, kdite, mẖe, mlo, sem, ste, mk, mkdi, tedḫe, terike, yetmde, ar, tke-, nse, sdk, sḫi, tbo,
   teneke, yireqe, yirewke, ẖr, kelw, abese, pete, ktke, pqr, qo, beloloke, adb, tkk*. One of them, *ar* 'boy,
   son', owes its meaning partly to an NES comparison (gold note); its best score is −0.05, so it does not
   change the held-out result.

### 4.2 Reading a Meroitic word (`pattern`)

The engine reads standard transliteration and the corpus spelling (x ḫ, X ẖ, S the s sign, N the ne sign, E or o
the o sign) as slots. A bare consonant sign carries the inherent /a/, which gets no slot: Rilly's table pairs
medial *a* with every NES vowel and with nothing (T3–T13). Initial *y* before *e* or *i* is a dummy. Each
consonant slot is marked initial (the word begins with it), final (the last consonant) or medial. Examples, as
`expected(form)` prints them for a Nubian list (one group per slot, vowel slots in brackets, j the palatal
ɟ or dʒ, ° only under a stated condition, Ø the sound may vanish):

| Meroitic | Expected reflex pattern |
|---|---|
| *kdi* | k\|ŋ · d\|r\|t · (i\|e) |
| *ḫre* | g\|j°\|gw\|kw · r · (e\|o\|a\|i) |
| *qore* | kw\|gw\|Ø° · (u\|o\|i\|a) · r · (e\|o\|a\|i) |
| *dime* | t\|d\|r · (i\|e) · m\|Ø · (e\|o\|a\|i) |

### 4.3 The correspondences used

"T*n*" is the *n*-th data row of `data/nes/sound_correspondences.tsv` (Rilly 2003's table, then the prose rules
of 2003–2022). Weights are the reward for that pair (1.0 = stated regular reflex). A rule stated for one position
counts at 0.7 in another; a rule stated for one language applies only there.

| Meroitic | NES reflexes (weight) | Rows |
|---|---|---|
| b | b 1.0; f 0.8 (Nyima); g 0.9 next to o/u | T18, T19, T64, T71, T73, T79 |
| p | as b: p is a spelling of /b/ | T58 |
| m | m 1.0; nothing 0.5 word-finally (*dime* ~ *tii*) | T38–T40 |
| n | n 1.0 (*nob* ~ *nogu*) | T73 |
| t | t 1.0; d 1.0 medially; s 0.8; st 1.0 medially | T47–T51, T60, T66 |
| d | t 1.0 initially; d 1.0; r 1.0 (*wide* ~ *wer-i*, initial *r > d); n 0.8 initially (Nara); nothing 0.4 finally (Nyima) | T20–T23, T57, T78, T81 |
| l | d 1.0 initially (lambdacism); n 0.8 initially (Nara); r 0.9 finally; l 1.0 | T34–T37, T55, T61, T65, T69 |
| r | r 1.0; l 0.9 (Nyima); nothing 0.4 finally (Taman) | T41–T45 |
| s | s 1.0; ʃ 1.0 (*ms* ~ *mašal*); t 0.7 finally (Taman) | T46, T51, T67, T82 |
| k | k 1.0; ŋ 0.9 initially (Nubian, from *ᵑk); t 0.8 initially and d 0.6 (Nyima) | T32, T33, T63, T75 |
| ḫ, ẖ | g 1.0; gw 0.9–1.0; ɟ 0.8 next to i/e (Nubian); h 0.9 (Nara); ŋ 0.9 medially (Nyima), 0.8 finally (Taman, Nyima); k 0.7 initially, t 0.7, d 0.6 (Nyima) | T26–T28, T54, T56, T62, T74–T76 |
| w | w 1.0; g 0.8 initially (Nyima), 0.7 finally (accusative -w) | T53, T69, T72 |
| q | nothing 0.9 before an NES word-initial u/o (*qore* ~ *ouru*); kw, gw 0.6 (its value /kʷa/, no row) | T80 |
| y | no slot as initial dummy (*yer* ~ *er-ti*); elsewhere y 0.8 | T70 |

Vowels weigh little because the script hardly writes them: initial *a* ~ a or e 0.25, u 0.2 (T1, T2, T17);
initial *e/i* ~ e 0.25, i 0.2 (T24); *e* ~ e or o 0.2, a or i 0.1, or no vowel (T25); *i* ~ i 0.25, e 0.2
(T29–T31); *o* ~ u or o 0.25, i 0.15, a 0.1 (T52); any other vowel −0.1.

### 4.4 NES spellings (`segments`)

Each NES cell is split into its variants (`~`, `/`, `,`, braces and brackets), and a form with morpheme breaks
is also tried as its first and its longest piece; a row scores its best variant. Tone, length and stress marks
are dropped and every system is mapped onto 5 vowels and 21 consonants:

1. GLD and IDS IPA: ɛ ə ɪ ɔ ʊ ʌ to plain vowels; ʈ ɖ ɽ ṯ ḏ t̪ d̪ to t d r; č š ǯ ʒ ʓ ɟ to c ʃ j; ɣ χ ħ ʕ to h.
2. ASJPcode: E 3 N 5 S Z C T L X G 7 8 4 read as their ASJP values; its `~ * " $` modifiers are removed, not read
   as variant breaks.
3. Wiktionary Old Nubian (Coptic): ⲟⲩ (ou) is w before a vowel and u otherwise, ⲉⲓ (ei) is i, ⳝ (ç) is j, ñ is ɲ.
4. Numeral lists: tone letters (˥ ˧) dropped.

### 4.5 Scoring (`align`)

Dynamic-programming alignment of the Meroitic slots with the NES segments. A pair earns its rule weight; a near
sound with no rule (same class, such as d ~ l) earns +0.3; an irregular consonant costs −1.0. A Meroitic
consonant with no counterpart costs −0.8 (−0.3 for w, −0.2 for y) unless a rule lets it vanish. An extra NES
consonant costs −0.6 (−0.3 for y, w, h) and nothing when it is a nasal before a consonant: Meroitic does not
write a nasal there, and T59 gives prenasalised and plain consonants the same reflex. An extra NES vowel costs
nothing. The score is the total divided by the number of Meroitic consonants. On Rilly's own pairs it gives,
for example, *ḫre* ~ Dongolawi *goor* 1.00 (raw 0.00), *qore* ~ Nobiin *ūru* 1.07 (raw 0.29), *lẖ* ~ *dig* 1.00
(raw 0.00), against −0.82 for *qore* ~ *tii*.

## 5. The engine does encode Rilly's correspondences (labelled circular check)

As a separate check, not evidence: `proto_nes.tsv` names, for 83 rows (with repeats across Rilly's papers), the
Meroitic word Rilly compared with each proto-form. Among all 330 proto rows, his proto-form ranks first for
the Meroitic word in 38 of the 83 under the engine and 21 under raw similarity (top 5: 42 against 40). This is
circular by design: Rilly made both the proto-forms and the correspondences with these Meroitic words in view.
It shows the engine implements his rules; it says nothing about whether they find new cognates.

## 6. Best same-meaning match per gold word (rule engine)

Every match is a same-meaning pair from the validation, not a proposed cognate. Rule words are in bold.

| Score | Raw | Meroitic | NES word | Correspondences used |
|---:|---:|---|---|---|
| 1.50 | 0.67 | **ato** 'water' | Old Nubian *etu* 'water' | t~t |
| 1.12 | 0.67 | **kdi** 'woman' | Ama/Nyima *kírī* 'woman' | k~k; d~r |
| 1.07 | 0.29 | **qore** 'king' | Nobiin *ūru* 'king' | q~Ø (T80); r~r |
| 1.00 | 0.67 | **wle** 'dog' | Dongolawi *wɛl* 'dog' | w~w; l~l |
| 0.95 | 0.33 | asr 'meat, animal' | Hill Nubian *ʃar* 'animal' | s~ʃ; r~r |
| 0.90 | 0.50 | **ḫre** 'meal' | Nyima *ṯùlɔ̀* 'eat' | ḫ~t (Nyima); r~l (Nyima) |
| 0.88 | 0.25 | **dime** 'cow' | Hill Nubian *ti* 'cow' | d~t; m~Ø |
| 0.80 | 0.00 | **l-** 'give' | Nara *ni* 'give' | l~n (Nara) |
| 0.75 | 0.40 | **are-** 'take' | Hill Nubian *aŋíri* 'take' | r~r |
| 0.75 | 0.00 | **dm-** 'take' | Old Nubian *eit* 'to take' | d~t; m~Ø |
| 0.75 | 0.25 | pete 'snake' | Nara *wɔso* 'snake' | p~w (near); t~s |
| 0.68 | 0.33 | **wide** 'brother' | Hill Nubian *ɪntáŋŋwar* 'older brother' | w~w; d~r |
| 0.65 | 0.50 | **ked** 'kill' | Hill Nubian *hur* 'kill' | k~h (near); d~r |
| 0.63 | 0.33 | yetmde 'relative' | Hill Nubian *ɪntannikoru* 'nephew' | t~t; m~n (near); d~r |
| 0.62 | 0.40 | sḫi 'small' | Midob *sàŋ* 'small' | s~s; ḫ~ŋ (near) |

The other 29 words score below 0.6; the full list prints with `python3 -I src/cognates_rules.py`. Some of Rilly's
pairs cannot be scored by this design at all: he compares *yer* 'milk' with Nubian *er-ti* 'breasts', a meaning the
same-meaning test does not count, and the lists hold no Nyima *élo* 'milk' (the only 'milk' rows are three Hill
Nubian ones), so *yer* scores −0.30.

## 7. Candidate lists

Not produced. The brief asks for them only if the validation shows a real signal, and it does not: the
signal on all gold words is the rules recovering the words they were built from, and on the held-out words the
engine scores at chance. Lists for *temey, tros, tlt, teketi, kroro, aribet, ateqi, Sklte, mlekeyos, tmNteleb,
Smlo, brtoye, kemxr, kiN, mlolo, yiroXe, womnitX, SSimete* were never computed: the code computes them only
when the preset test passes.

## 8. Limitations

1. Meaning matching is `cognates.py`'s gloss-keyword overlap, which pairs some wrong senses (*pqr* 'prince'
   with Old Nubian *kaisara*, a Greek loan glossed 'crown prince') and misses shifted ones (milk ~ breast).
2. Coverage is thin outside the 110-item GLD lists: titles, kinship terms and directions are compared mostly
   with Hill Nubian (Ghulfan, through IDS).
3. The weights are set by hand from the rows, not estimated, and the correspondences come from Rilly's 2003
   table and later open papers; Rilly 2010's full set is not openly available.
4. Old Nubian GLD spellings in braces keep their Coptic ou and ei unconverted (only Wiktionary's are mapped).

## 9. Reproduce

```
python3 -I src/cognates_rules.py
```

It prints every number above in about 30 seconds (2,000 shuffles; pass another count as the first argument).

```
python3 -I tests/test_cognates_rules.py
```

It runs 12 plain-assert checks of the correspondence mapping, the spellings, the scorer and the statistics, and
ends with "12/12 passed".
