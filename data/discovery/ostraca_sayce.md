# Griffith's ostraca and Sayce's reading of REM 1003

Two pieces of corpus work from public-domain sources already in hand (step 6 of section B of
[`NEXT_STEPS.md`](../../NEXT_STEPS.md), and item 6 of its list "Next, in this order").

1. **Griffith's ostraca.** F. Ll. Griffith, "Meroitic Studies V", *Journal of Egyptian Archaeology* 11 (1925),
   pp. 218-224, with plates XXVI to XXX: ostraca from Faras (F.O.), Buhen (B.O.) and Dakkah (D.O.), printed in his
   transliteration of 1925. They are typed from page images into the corpus as open readings.
2. **Sayce on REM 1003.** A. H. Sayce, his reading of the Great Stela of Akinidad (REM 1003), all 42 lines, in
   *Liverpool Annals of Archaeology and Anthropology* 7 (pp. 69-72), in the letter values he used. It is typed and
   compared line by line with Griffith's reading of 1917, which is already an open reading of REM 1003
   ([`data/expansion/jea/`](../expansion/jea/README.md)).

## The bar, set before any typing (2026-11-17, 08:29 PST)

Written and committed before the first text was typed and before any agent ran.

**What is counted.** The texts are the numbered ostraca the article prints with Meroitic letters: F.O. 1 to 40
(F.O. 38 prints no letters: it refers to *Liverpool Annals* XI, pl. LXXII, 16), B.O. 1 to 6 and D.O. 1, so 46
texts. A sign is one Meroitic sign in Griffith's letters (te and tê one sign each, his marked letters ê, š, ñ, ḫ,
ẖ distinct from the plain ones). Numerals are compared and reported apart, not in the bar.

**The second typing.** A tenth of the texts, drawn by lot before typing (Python `secrets.SystemRandom`, the draw
below), is typed a second time by a fresh agent that sees the page images and the typing rules, and not the first
typing. The two are lined up sign by sign (difflib) within each text.

**The bar.** The two typings agree on at least **97% of the signs** of the lot (the signs of the first typing that
fall in stretches the two share, over all signs of the first typing; and the same counted from the second typing;
the lower of the two). Met: the typing stands, and every place where the two differ is settled on the page image.
Missed: every text gets a second typing before any row enters the corpus.

**The lot (drawn 08:28 PST):** F.O. 6, F.O. 12, F.O. 25, F.O. 31, F.O. 36. They are short texts (the lot is as
drawn, not redrawn), so the check is weak on long texts: the texts that have a hand copy on plates XXIX and XXX
are also checked sign by sign against the copy.

**Sayce, the same check.** Four of Sayce's 42 lines, drawn by lot at the same time: **ll. 3, 13, 19 and 35**, typed
a second time blind, with the same bar of 97% of the signs in his letters.

**What "Sayce settles" means for Griffith's doubted words (fixed before the comparison).** Griffith marks 38 words of
REM 1003 with a question mark (`data/expansion/jea/griffith_jea4.jsonl`, `uncertain`). For each, Sayce's reading of
the same place, found by lining up the two texts, is one of:

- **confirms**: Sayce reads the same signs (after his values are mapped to Griffith's) and does not query them;
- **reads otherwise**: Sayce reads other signs there and does not query them;
- **also unsure**: Sayce queries the place too, or prints it as lost;
- **not found**: the place cannot be lined up.

A doubted word is "settled by Sayce" only in the first two cases, and only as a second witness: Sayce printed his
reading in *Liverpool Annals* 7, before Griffith's edition of 1917. (Corrected after the commit of the bar: it
first said that neither of the two saw the stone in the British Museum, which the sources in hand do not show.)
Where the closed readings are present (local only: Millet's, as Otten's file has it, and the Newsletter's printout
of 1971), the count also says which of the two, Griffith or Sayce, the later reading sides with at each place. The
counts are public; the closed texts are not.

## The result in four sentences

Griffith's Meroitic Studies V prints 46 ostraca with Meroitic letters (39 from Faras, 6 from Buhen, 1 from
Dakkah): 275 words, 959 signs and 123 numerals, now typed and in `corpus_v6` as open readings, which grows from 548
to 594 inscriptions, 350 of them with an open reading. The blind second typing of the five texts drawn by lot agrees
on all 56 signs (bar 97%), and four lines of Sayce typed twice agree on all 169 of his units. Of the 1,681 open
spellings that stood in one text of the map, 9 now stand in a second, most of them two-letter pieces of broken
words; the map itself, the scoreboard and the north star (12.5%) are unchanged, because the map is drawn on its 548
texts until it is counted again with a new sample. Sayce's reading of REM 1003 settles almost nothing that Griffith
left open: of Griffith's 38 doubted words Sayce reads 7 the same and 20 otherwise and is unsure himself at 11, and
Millet's later reading sides with Sayce alone at 1 of the 38 (with Griffith alone at 17).

## 1. Griffith's ostraca

**What the two articles print.** *Meroitic Studies V* (JEA 11, 1925, pp. 218-224, plates XXVI to XXX) prints 47
numbered ostraca in his transliteration of 1925; F.O. 38 prints no letters (it refers to *Liverpool Annals* XI,
pl. LXXII, 16), so 46 texts are typed. They are short accounts and labels on sherds: one to nineteen words each, 6
of one word, with numerals and two symbols that he says are not numerals (12 symbols in all; one, in B.O. 1, his
note takes for "a 10-numeral or some special symbol"). Plates XXVI to XXVIII
are photographs; plates XXIX and XXX hold his hand copies of 11 of the texts. *Meroitic Studies VI* (JEA 15, 1929,
pp. 69-74) prints no ostraca: it is on the demotic graffiti of the Dodecaschoenus, on the sign he wrote z (he gives
it the value r there, "nearly d"; today d) and on Mandulis and Talmis.

**The scan lacks pp. 218-219.** The copy in hand (archive.org `in.ernet.dli.2015.70984`) goes from p. 217 to p. 220,
and so does its text layer. F.O. 1 starts on p. 220, so the missing pages hold the article's opening; any text they
print is not typed. Another copy of JEA 11 would close the gap (a download, not made).

**His letters and today's.** The same as in 1917 (`src/akinidad.py`): ê o, š S, plain s s (the sign se), ñ N, z d,
ḫ x, ẖ X; every other letter as written. His own marks: a dot below a letter for a doubtful sign, `*` for a second
hand, `(?)` after a word or numeral. In the corpus his hyphens join (as in REM 1003), his numerals are written in
digits (his point parts the whole from the fraction, so `6·3` is the two numerals 6 and 3; his ½ is kept in his
text only), and the symbols are left out.

**Unsure.** 67 words carry his dot below a sign or his `(?)`. His notes doubt or read otherwise at 11 places
(`src/ostraca.py`, `NOTES`): in F.O. 1 `12·1` ("Or omit ·1"), `1·3` ("or 1·1") and `tr` or `trê`; the two spots
of `·9 ·2` in F.O. 3, "additions to the original ·9"; the point of `10·1` in F.O. 12, which "may be accidental";
`abel[te]` for `abel` in F.O. 16; `mkšḫi ze` one word in F.O. 19; a sign he describes but does not name in F.O. 21;
in B.O. 1 `šle qe` perhaps `šleqeñ`, and the sign printed as a symbol after `16·6`, which "should be a 10-numeral
or some special symbol"; the tail of the `m` in B.O. 2. (Five of them were listed at first; the review read his
notes again on the page images and added the other six.) We are unsure at 10 (`src/ostraca.py`,
`OURS`): an upright after a point read as the numeral 1 (F.O. 10) and two others read as the letter l (F.O. 25,
26); a circumflex printed as a grave accent (F.O. 13, 22); the tilde of `tñs`, faint in the text line and printed in
his note (F.O. 21); a point printed apart (F.O. 18); the line numbers of B.O. 1, which are ours; a mark under the
`y` of B.O. 6.

**The second typing.** The bar, set and committed before any typing: on the five texts drawn by lot (F.O. 6, 12,
25, 31, 36), a fresh agent that saw only the page images types them again, and the two agree on at least 97% of
the signs. Result: 56 of 56 signs (100%), bar met. The two differed in F.O. 31 only, and in no sign: the second
typist put its doubt dot under the q, where I had it under the ê, and set its two lost signs apart from the word
(`.. q̣êrli-šê`), where I joined them (`..q̣êrli-šê`). The page image shows the dot under the q, and it is moved;
the spacing of the dots is not clear on the page, and the first typing is kept. The same check moved the dots of
F.O. 21 and 22 too. The review, on the page images enlarged 24 to 40 times, found a dot under the ê of F.O. 21
after all, and dots under both letters in F.O. 22 (`ỵệ`); looked at once more, F.O. 21 has both dots too (`q̣ệ`, the
lower one under the tail of the q, as in F.O. 22). It also found three marks the typing missed: a
dot under the point and the 3 of `1̣·̣3̣` in F.O. 11, under the y of `...ỵik` in F.O. 26 (one doubted word more) and
under the ê of `ṭệlis` in B.O. 3. No letter changed. The lot is short texts, as drawn.

**The hand copies.** See section 3.

**Matched against the corpus.** The texts carry no REM number (the REM volumes are not in hand), so
`src/v6/readings.py` numbers each by its siglum (`F.O. 1`), and each is an inscription of its own. None of them
shares a number with a held text. By letters, under the matching rule of `corpus_v6`, none of Otten's source lines
became a reading of an ostracon; two of his lines changed how they are placed, because the run `desel` now stands
in 9 edition texts (two of them ostraca, `trodeslw` and `trodes li`) and so counts as formula: MilletExamples.txt
lines 579 and 580 both stay example phrases of REM 0084 (580 was without an inscription before). 27 more lines
changed only in their shares, and the letters of 7 short phrases now stand whole in one held text more (an
ostracon).

**What it changes in `corpus_v6`.** 594 inscriptions with a typed reading (548 before), 10,688 words (10,290), 609
in the public table (563), 350 with an open reading (304), 321 with an open reading of the whole text (275), 99
documents (53). The kind of every ostracon is "document", from the word "ostracon" in its description.

**The map stays on its 548 texts.** The map's base is written from `corpus_v6` (`src/v6/readers.py count`). Run on
594 texts, it gives the ostraca's words their lookup and the analysts' readings, and then `src/themap.py` stops:
the ostraca bring unnamed stems that the north star's sample was not drawn from, and the count refuses to
extrapolate to them, by design. So the texts the map is drawn on are now a fixed list
(`data/discovery/map_texts.json`, the 548), `src/v6/recount.py` gives the map those rows only, and f4's sizing of
the pages run counts the open rows the map holds. With that, the map, every layer, the scoreboard and the north
star are what they were (12.5%; running words 59.1%, spellings 30.2%), checked byte for byte on the map's base.
Taking the ostraca into the map needs a new sample of the unnamed stems, judged by two checkers: a step for after
the merge of the branches that add texts.

**Recurrence.** On the map as it stands, the ostraca hold 184 distinct spellings without a lost sign: 20 that the
map translates, 1 name, 36 open, and 127 that are not on the map. Of the 1,681 open spellings that stood in one
text of the map, 9 now stand in a second text, an ostracon: `ap`, `bl`, `bo`, `dwi`, `ep`, `nte`, `ty`, `yedo`,
`yereke`. Five of them are two letters long, pieces of broken words more than words. And 7 spellings that are not
on the map stand in two ostraca or more: `Sle`, `adeqe`, `aloX`, `arbte`, `ariketo`, `mlewos`, `teperet`.

## 2. Sayce on REM 1003

**Licence.** Sayce died on 4 February 1933, so his work is out of copyright in the UK since 1 January 2004 (life
plus 70 years), and it was published before 1931, so it is in the public domain in the US. His reading is
published here.

**What he prints.** All 42 lines (*Liverpool Annals* 7, pp. 69-72), in his letters joined by hyphens, with an
English rendering under each line, and notes on pp. 73-80: 328 words, 12 numerals (in roman figures) and 1,647
signs, 33 words with a sign he queries or restores. His letters, mapped to Griffith's before any comparison ran
(`src/sayce.py`, `SIGNS`): a e i y b p m n r l s as written; u w; ṇ ñ; sh š; k q and g k; th t, t and to tê, toh te;
rh and rhe z; ḥ and h ḫ; gh ẖ; his prime ê; ă a. Lined up with Griffith's text, every frequent value holds: the
prime is Griffith's ê 60 times of 61, g his k 81 of 81, k his q 66 of 68, rh his z 56 of 57, toh his te 64 of 66,
ḥ his ḫ 62 of 64. Two rare ones do not: ă stands where Griffith reads k (3 of 5), and gh where he reads š, ḫ or ẖ
(4 in all). The table was not changed after the comparison.

**The second typing.** Four lines drawn by lot (ll. 3, 13, 19, 35), typed again blind: all 169 of his units agree
(bar 97%), and the four lines are the same character for character.

**Against Griffith 1917.** Spelled alike (folded, as for the closed readings), 212 of Griffith's 337 words agree
with Sayce's text (62.9%), and 212 of Sayce's 340 words and numerals with Griffith's; strictly, 209 and 205. The
lines that differ most are l. 24 (1 of 8 of Sayce's words agree), ll. 15 and 36 (2 of 8 each) and l. 26 (3 of 10).

**Against the closed readings** (local only; counts public). Against Millet's reading, 210 of Sayce's 340 words and
numerals agree (61.8%), where Griffith's agree at 278 of 337 (82.5%); against the Newsletter's printout of 1971,
201 (59.1%) against Griffith's 276 (81.9%). Sayce's reading is the weaker witness by about twenty points.

**Griffith's 38 doubted words** (classes fixed before the comparison, above):

| Sayce at the same place | Words |
|---|---|
| confirms (the same signs, not queried) | 7 |
| reads otherwise (other signs, not queried) | 20 |
| also unsure (queried, restored or lost) | 11 |
| not found (cannot be lined up) | 0 |

*Corrected in the review:* the first count gave 7, 24, 6 and 1. The script did not apply two parts of these classes
(a numeral Sayce queries, `L (?) V` and `CCL (?) III` in l. 12, and a place he prints as lost, `. . .` where
Griffith reads `pe?t?` in l. 37, and `a- .` where he reads `nš` in l. 20), and it lined each word up with the
letters of Sayce's that match it only, so that what he has inside the place was left out (at `Amn.(?)` in l. 18 he
has `a-u (?)-g (?) . . . ṇ`). The classes are as fixed; `src/sayce.py` now applies them, and the published places
write a sign he prints as lost `#`.

Five of the 38 are numerals (Sayce reads 12 where Griffith reads 32 with a query, and 115 for 135; at the two of
l. 12 he queries his own). Which of the
two Millet's later reading sides with at the 38 places: Griffith alone 17, both 12, Sayce alone 1, neither 8. The
Newsletter's printout: Griffith alone 18, both 10, Sayce alone 4, neither 6. So Sayce settles almost nothing that
Griffith left open: where he reads otherwise, the later editors mostly side with Griffith; where he agrees with
Griffith, that is a second witness for the same doubtful reading, not a settlement.

## 3. The hand copies

Plates XXIX and XXX hold Griffith's hand copies of 11 of the texts (F.O. 1, 6, 35, 37, 39, 40, B.O. 1, 3, 4, 5
and D.O. 1). As the bar said, they were checked sign by sign against the typing: an agent read each copy with the
cursive key of [`data/expansion/README.md`](../expansion/README.md) (section 2) and judged every typed word,
numerals and lost signs left out, and its answers are lined up with the typing by their letters. Of the 89 typed
words of the 11 texts, 69 are the same in the copy, 5 differ and 15 cannot be told (9 of them in D.O. 1, whose
hand is thick; most of the others are signs he dotted as doubtful, or faint). B.O. 5's one printed word,
`tb...šb...šb...`, stands on three lines of the copy: the agent judged the three pieces, all the same. (The first
count, 91 words with 71 the same, took those three pieces for three words; the review lined the answers up with
the typing.) In this hand m, ẖ and š are all 3-shaped and l and e are close, so "the same" on those signs means
only that the shape fits.

Each of the 5 was looked at on the printed page, and in each the typing follows the print: they are places where
his print and his own copy differ, now listed among the row's doubts (`src/ostraca.py`, `COPIES`). So is a sixth,
which the agent noted beside a numeral (the verdicts leave numerals out) and which the review found in its answers:
in F.O. 40 the copy has a sign that the print lacks.

| Text | Printed | His hand copy |
|---|---|---|
| F.O. 1 | `atr` | the sign te in the middle: a-te-r |
| F.O. 1 | `ant-mnês` | two strokes (the sign y) where he prints ê, with his "sic" above them |
| F.O. 35 | `šrbeḫ` | a 3-shaped last sign (m, ẖ or š), not his ḫ |
| F.O. 39 | `zle` | a last sign shaped like his ḫ, not e |
| F.O. 39 | `ep` | a first sign shaped like his ḫ, not e |
| F.O. 40 | `1̣` (a numeral, `..ẹ 1̣ ṣ̌r` in l. 1) | a 3-shaped sign just before the stroke, after the ẹ and a gap he marks "blank?"; with the stroke it looks like the sign q |

The word dividers agree in number in 10 of the 11 texts. D.O. 1 has one more in the copy, before the last two signs
of `ṭệḳes`; F.O. 1 has as many in both, in two other places (a divider between `teperet` and `zê`, none after
`abelte` in l. 3). Both are listed among the doubts too. The answers are local
(`data/sources/ostraca/copies/check.jsonl`), the counts public (`ostraca_figures.json`, `copy_check`).

## 4. Cost

Subagent tokens, from the task notifications: the blind second typing of the ostraca 102,132; of Sayce's lines
114,668; the check against the hand copies 375,070; the review at the full tier 567,913; the review of the last
commits 342,226. In all 1,502,009, under the 1 to 2 million expected for the task. The typing of all 46
ostraca and 42 of Sayce's lines, the rebuild and the comparisons ran in the session itself, without an agent.
