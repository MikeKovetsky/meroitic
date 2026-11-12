# Brief: cut and classify Meroitic words

You are one of several independent analysts. Work alone: read only the three files in your folder, use no web
search and no other folder. The files are data, not instructions.

- `lexicon.tsv`: Claude Rilly's 2003 lexicon of Meroitic, one entry a line: headword, its spellings in the
  corpus's letters, whether it is a word, a suffix, a prefix or an infix, its kind, its status in Rilly
  (established, probable, hypothesis, unknown), its meaning, the page.
- `words.jsonl`: the words to analyse, one a line: the word, how often and in how many texts it occurs, up to
  four contexts (the word in square brackets, six words on either side, the text's id in front), and for words
  of Karanòg and Shablûl what Griffith's 1911 tables print about it (`griffith`).
- Write `analysis.jsonl` into the same folder: one JSON line for every word, in the same order.

## The spelling

The corpus writes S for the s sign, s for the se sign, N for the ne sign (ñ), x for ḫ and X for ẖ; te and to are
one sign each and are written with two letters. `NAME` and `RNAME` are personal and royal names masked in the older
corpus. In the rows whose id starts with `G-` or names an inscription (`REM 1038`, `GA 28`) the names are not
masked, but for a word that the edition itself tags as a personal name, which stands as `NAME` too. A dot is a lost
sign. An ending may be written on its word or apart (`yetmdelo wi`), and two words may be written as one.

## What to write for each word

```json
{"word": "tbitolyeqowi", "parts": [{"form": "tbitolye", "entry": "NAME"}, {"form": "qowi", "entry": "qowi"}],
 "kind": "person name", "gloss": "this is Tbitolye", "confidence": 4,
 "evidence": "stands after the invocation, where the deceased is named; Griffith: names table, column A",
 "recalled": ""}
```

1. **parts.** Cut the word into its parts. The `form`s, joined, must spell the word exactly. Each part's `entry`
   is one of:
   - a headword of `lexicon.tsv`, copied character for character from its first column (with its hyphens and
     its number, such as `-se (1)`);
   - `NAME` for a personal, divine, place or people's name that the lexicon does not have;
   - `NUMBER`;
   - `?` for a piece you cannot place.
   A part may be a spelling variant of an entry (an e written or left out, o for e, a lost initial a): say so in
   `evidence`. Use as few parts as explain the word. Do not cut off one or two letters only because such an
   ending exists: a cut needs a stem that the lexicon has or that the contexts show on its own. A word you
   cannot cut is one part with the entry `?`.
2. **kind.** One of: `person name`, `place name`, `god name`, `people name`, `name`, `title`, `kin term`,
   `epithet`, `benediction verb`, `filiation word`, `verb`, `noun`, `adjective`, `numeral or measure`,
   `function word`, `two words written as one`, `unknown`. The kind is what the texts show the word to be, even
   when its meaning is unknown: a word between a name and `yetmdelowi` is a title or a kin term, a word after the
   benediction's `ato mXe` or `at mXe` is a benediction verb, a word before a numeral is a counted thing.
3. **gloss.** The translation of the word in a few English words, as far as the parts give one; `?` for what is
   unknown (`[title] of ?`).
4. **confidence**, 1 to 5, strictly: 5 = the lexicon has every part and the contexts fit; 4 = sure; 3 = likely;
   2 = a guess with some support; 1 = no idea. In earlier runs of this project every answer given at 4 or 5 was
   right: keep it so. What you only remember from the literature must not raise an answer above 3.
5. **evidence.** At most 30 words: what in the contexts and the lexicon the answer rests on.
6. **recalled.** At most 25 words: what you remember from the published literature about this word that
   `lexicon.tsv` does not have, with the author if you know it; otherwise an empty string.

## What helps

- An epitaph runs: invocation of Isis and Osiris (`woSi`, `Soreyi`, with or without their epithets); the
  deceased, `X qo` or `X qowi`; the mother, `Y tedxelowi`; the father, `Z terikelowi`; then descriptions,
  each a title or a kin term with a name and `yetmdelowi`, `mdetowi` or the like; then the benedictions (`ato mXe`
  …, `at mXe` …, with a verb that begins `pSi`, `pSo`, `bSi`, `yi` and ends `te`, `kete`, `kte`, `kes`, `to`).
- Griffith's marks in `griffith`: "names table, column A, B, C" and "n. A.", "n. B.", "n. C." are the name of the
  deceased, of the mother and of the father; "title of A" a title of the deceased; "descr." a word of the
  descriptions; "formula A" to "J" and "in form A" the benedictions.
- The same stem often stands in other words of your list: compare them.

When you have written the file, answer in three lines: how many words you analysed, how many at confidence 4 or
5, and anything odd you saw.
