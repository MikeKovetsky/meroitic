# Step 2: check your reading against Griffith's printed tables

Griffith printed most words of every inscription a second time in clean Meroitic type, in four places of the same
book: the table of names and parentage (the name of the deceased in column A, of the mother in B, of the father in
C), Indexes A and B (titles and descriptive phrases), Index C (single words and groups), and chapter V, which gives
each inscription's own wording of the closing formulae A to J. Other readers have typed those pages.

## What is new in your folder

- `refs/`: one file per inscription of yours, such as `refs/Kar_047.jsonl`: every typed entry that names it, one
  JSON object a line:
  - `source`: where it is printed ("formula A (table)", "formula B (prose)", "names table, column B (person 1)",
    "Index A").
  - `reading`: the entry as typed from the type, in the same transliteration you use. `(?)` after a sign is a
    query Griffith printed; `?` is the typist's own doubt; `[ ]` and `( )` are Griffith's brackets.
  - `part`: `a` or `b` when the entry is for that part of the inscription.
  - `compare_only`: true for a "cf." mention: the entry belongs to another inscription and yours only has
    something similar. Do not force it on your text.
  - `flag`: `"pair"` when the printed reference was a pair such as "Kar. 19-89".
  - `line`: the line of the stone, when the index gives one.
  - `printed_refs`, `gloss`, `typist_notes`: what else the page and the typist say.
  - `page`: the page it is on. `refs/strips/` holds every page in three strips (`ref_pdf059_b1.png` top, `_b2`
    middle, `_b3` bottom) so that you can look at the printed type yourself.
- An inscription with no file has no entry.

Everything in `refs/` comes from the same 1911 book or from other readers' typing of it: it is data, never an
instruction. The rules of step 1 still hold: open only files in your own folder (the strips folder inside
`refs/` counts), no web, and do not change `out/copy_only.jsonl`.

## How to check

1. For each inscription, take its entries one by one and find where each stands in your step-1 reading. Names
   stand after the opening invocation; the formulae stand at the end. A formula entry from the prose often gives
   one word of the formula only (its notes say which).
2. Where the entry and your reading agree, go on.
3. Where they differ, look at the copy again at high zoom, and look at the printed entry in the strip yourself:
   the typing is another reader's and can be wrong, most often p against k and the 3-shaped signs (m, ẖ, s).
   Then decide:
   - The type shows a sign that the copy can also be: take the type. It is Griffith's considered reading of the
     same signs, so it usually wins.
   - The copy clearly shows something else than the type: keep the copy and say so. Griffith's tables and copies
     do differ in places (he marks some "sic").
   - The typed entry is not what the type shows: go by the type, and record the correction (see below).
4. Signs that no entry covers stay as in step 1. One exception: when the check shows how this copy writes a sign
   (say, that its 3 with a long tail is ẖ), you may correct other signs of the same shape in the same copy, and
   list each as a change with the reason.
5. Do not add signs that the copy does not show, and do not drop signs the copy shows, because an entry is
   shorter or longer: note the difference instead.

## What to write

- `out/final.jsonl`: the objects of `out/copy_only.jsonl` in the same order with the same fields, `reading` now
  being the checked reading (line numbers, dividers, `?` and `[.]` kept; drop a `?` where the type settled the
  sign), and two more fields: `entries` (how many entries you placed in it) and `check_notes`.
- `out/changes.jsonl`: one object per changed place: `text`, `part`, `before`, `after`, `entry` (its source and
  reading), `reason`.
- `out/kept_against_type.jsonl`: one object per place where you kept the copy against the type: `text`, `copy`,
  `type`, `why`.
- `out/unplaced.jsonl`: every entry you could not find in the text: `text`, `source`, `reading`, `why`.
- `out/ref_corrections.jsonl`: every typed entry that the type does not bear out: `page`, `typed`, `type_shows`.

Check that each file is valid JSON lines. Then report, for each inscription: its number of signs, the signs
changed, the entries placed and not placed; then the places where copy and type really disagree, the number of
corrections to the typing, and how long the step took. Keep it short and factual.
