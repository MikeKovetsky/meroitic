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

A doubted word is "settled by Sayce" only in the first two cases, and only as a second witness: Sayce read in
1914, before Griffith's edition, and neither saw the stone in the British Museum the way the later editors did.
Where the closed readings are present (local only: Millet's, as Otten's file has it, and the Newsletter's printout
of 1971), the count also says which of the two, Griffith or Sayce, the later reading sides with at each place. The
counts are public; the closed texts are not.
