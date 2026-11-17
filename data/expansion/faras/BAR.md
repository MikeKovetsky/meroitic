# Faras: the bar, set before any reader ran

Written 2026-11-17, 08:29 (Pacific), before any reader was sent out and before any text of the article was typed.
Committed on its own, so that the history shows it came first.

## What is measured

Griffith's 46 Faras funerary texts (*Recueil Champollion*, 1922, PDF pages 601 to 648) are typed into the corpus
spelling from the page images by readers (Claude Opus 5.5 subagents), one pack of pages each. A tenth of the texts
is typed a second time by a fresh reader who sees nothing of the first typing: same kit, same brief, its own
folder.

## The draw

Five of the 46 texts (a tenth, rounded), drawn by lot with a fixed seed before typing:

```
python3 -I -c "import random; print(sorted(random.Random(20261117).sample(range(1, 47), 5)))"
```

prints `[2, 10, 13, 14, 15]`: **Faras 2, 10, 13, 14 and 15.**

## The bar

**The two typings agree on 95% or more of the signs of the five texts together**, after each reader's check
against what Griffith prints in Latin letters (his renderings of the names, titles and formula words, and his notes
on the formulae).

The measure is the one used for the Karanòg readers (`data/expansion/karanog/README.md`, section 6): the signs of
the first typing less the edit distance between the two typings, over the signs of the first typing. Lost signs
and line numbers are left out; a sign that only one typing has counts against it.

Reported beside it, with no bar: the same measure on the readings each reader wrote before the check, and, for
every Faras text the corpus already holds in a modern edition, the typing against that edition (by the same
measure, letters spelled alike).

## What follows either way

- The rows go into the corpus with the measured agreement in their notes, whether the bar is met or not; a miss
  is said in the first line of the report and on the page.
- After the measure, each place where the two typings differ is settled against the page image, and the row takes
  the settled reading. The measure is not computed again after that.
- Nothing is typed a third time to pass the bar.
