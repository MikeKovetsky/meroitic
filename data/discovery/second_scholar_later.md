# A second scholar for the meanings Rilly states in 2016 and 2021 (step G5)

Status on 2026-11-16: the rows, the decoys and the bars are set; no judge has answered yet. Working script (local
until the step is counted): `data/sources/g5/run.py`. What the judges are given:
[`runs/prompts/G5_judges.md`](../../runs/prompts/G5_judges.md).

## 1. What was asked

Mike, 2026-11-16, to "Start G3's pilot and G5 now, while the review runs?": "Yes, both". The step, as section G of
[`NEXT_STEPS.md`](../../NEXT_STEPS.md) has it:

> **G5. A second scholar for the stated meanings.** The 26 meanings of point 18 are Rilly's alone. The method of
> F2 on them: does FHN, Millet 2005 or Griffith state the same, or dissent, as Millet does on `sete`? The result
> is a status for each meaning (agreed by two, stated by one, disputed), not a higher count.

| | Requirement | State |
|---|---|---|
| R1 | "The 26 meanings of point 18", with the meanings that step G4 added the same day. | Set: section 2. |
| R2 | "The method of F2 on them: does FHN, Millet 2005 or Griffith state the same, or dissent" | Set: sections 2 and 3. |
| R3 | "a status for each meaning (agreed by two, stated by one, disputed), not a higher count" | Set: section 3. No count of the map changes. |

## 2. The meanings and the other scholars' statements

- **The meanings:** the 66 entries of the lexicon for which two readers found a meaning stated by Rilly in 2016 or
  2021: 26 among [the recurring open words](recurring_words.md), 57 among [the rare spellings](rare_spellings.md), 17 in both.
- **The other scholars:** 260 statements about these entries by someone other than Rilly. 118 are from the
  scholars' own works in hand (Griffith, Millet 2005, FHN II to IV, Lipiński 2011), as the literature passes of
  the two steps collected them, each quote found in its file by script; only statements that take a stance on a
  meaning count, not bare mentions. 142 are proposals that the lexicon of 2003 reports of a scholar
  (Hintze, Hofmann, Zyhlarz and others, whose works are not in hand). 8 entries have no such statement.
- **The rows:** each statement beside Rilly's later meaning of its entry, 260 rows, and 26 decoys: an entry's
  meaning beside a statement about another entry, drawn by a fixed seed (20261116). The rows are shuffled.
- **The judges:** two for each of 5 packs, each a fresh agent (Opus). For each row: the same meaning, partly the
  same, another meaning, or no meaning stated. A judge opens no file.

## 3. The bars and the rule, set before any judge is started

1. Every row is answered by both judges of its pack.
2. Cohen's kappa of the two judges on "same" against the rest, over the real rows, is 0.6 or more.
3. Each judge calls at most 10% of the decoys "same".
4. If a bar is missed, nothing is taken: the brief is corrected and fresh judges read the same rows.

**The status of a meaning:**

- **agreed by two scholars:** both judges call a row of its entry "same";
- **disputed:** no such row, and both judges call a row "other" (another scholar gives a different meaning);
- **stated by one:** the rest, also when there is no statement of another scholar.

An entry with a row that both call "same" and a row that both call "other" is agreed, with a dissent.

## 4. What this cannot show

- A proposal that the lexicon of 2003 reports is Rilly's report of that scholar, not the scholar's own page.
- "Same" is judged from two short statements. A later work that follows an older proposal is not an independent
  confirmation of it: a status says that two scholars state the meaning, not that it is proved.
- No count of the map changes with this step.
