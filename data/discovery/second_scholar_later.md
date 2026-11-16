# A second scholar for the meanings Rilly states in 2016 and 2021 (step G5)

Status on 2026-11-16: counted, its bars are met (section 5). Figures: `second_scholar_later_figures.json`. Script:
`src/second_later.py`. Checks: `tests/test_second_later.py`. What the judges were given:
[`runs/prompts/G5_judges.md`](../../runs/prompts/G5_judges.md). Sections 2 to 4 are the rules as they were set
before any judge was started.

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

## 5. The result

10 judges answered all 286 rows. On "same" against the rest their Cohen's kappa is 0.95 (bar 0.6); each
called 1 of the 26 decoys "same" (bar: at most 10%). The bars are met.

| Status of Rilly's later meaning | Entries |
|---|---|
| Agreed by two scholars | 18 |
| Agreed by two scholars, with a dissent | 15 |
| Disputed | 13 |
| Stated by one | 20 |

- **33 of the 66 meanings are also stated by another scholar;** for 15 of them a third scholar gives a different
  one.
- **13 are disputed:** no other scholar gives the same meaning, and at least one gives another.
- **20 rest on Rilly alone,** 8 of them because no other scholar says anything of the entry.
- Of the 25 words of the dictionary that step G4 laid with a meaning, 11 are agreed by two scholars, 4
  disputed and 10 stated by one.

The entries by status:

- **Agreed by two scholars:** `-i (2)`, `-k (2)`, `-kete`, `-se (1)`, `-td`, `Aritene`, `Stqo`, `arede`, `aroẖe`, `asr`, `ato`, `mreke`, `nbr`, `sr`, `wese`, `wi (1)`, `ḫr`, `ẖol`.
- **Agreed, with a dissent:** `-wi (5)`, `Aqedise`, `Ms`, `bqo`, `kdke`, `l (2)`, `mde`, `pqr`, `ps-`, `sete`, `t- (1)`, `tlt`, `wide`, `wte`, `yiroẖe`.
- **Disputed:** `-lw (1)`, `-w (1)`, `ad`, `eqe-`, `erk`, `mlowi`, `nobow`, `pl (2)`, `tk (3)`, `wse`, `ye- (2)`, `yerki`, `yet (2)`.
- **Stated by one:** `-bete-`, `-bte`, `-bto`, `-kese`, `-ketese`, `-lowi`, `-te (4)`, `Dqri`, `abrse`, `anese`, `aqebese`, `kb`, `ntk`, `plete`, `pso`, `pẖo`, `tk (1)`, `tḫ (1)`, `yel`, `yi-`.

The judges' pairs of verdicts on the 260 real rows: same / same: 83; no meaning / no meaning: 56; other / other: 55; partly / partly: 40; other / partly: 7; other / no meaning: 5; no meaning / other: 4; partly / same: 3; partly / no meaning: 2; same / no meaning: 2; same / partly: 1; partly / other: 1; no meaning / partly: 1.

Cost: 704,095 subagent tokens, from the task notifications.

A disputed meaning is not a wrong one. The older proposals often come from before the texts that Rilly's later
analysis uses were read as they are now; the status says only that the scholars in hand do not agree.
