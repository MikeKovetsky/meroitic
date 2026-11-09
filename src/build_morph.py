"""Blind morphology task (the Kober test): the scrambled corpus only; the
solver lists the bound morphemes and proposes what each one does."""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_tasks import BLIND, SEED, corpus_block, load_corpus   # noqa: E402
from scramble import make_map                                    # noqa: E402

TASK = """# Task: work out the grammar of an unknown language

Below is a corpus of ancient inscriptions in one language, one text per line (long texts are split across numbered lines). The script has been transliterated letter by letter into a substitute Latin alphabet. Spaces mark word boundaries, but scribes often run words and endings together. NAME stands for a personal name and RNAME for a royal name (masked). Digits are numerals.

No meanings are given. Work only from this file: do not use web search or fetch any page, and do not read any other file. You may run code (for example Python) that reads only this file.

Do what a decipherer like Alice Kober did with Linear B:

1. Find the recurring text types (formulas) and segment the most common one into its parts.
2. List the bound morphemes (endings, prefixes, clitics) that recur across many stems, each with the stems it attaches to.
3. For each morpheme, propose its grammatical function in plain terms (for example number, case, definiteness, copula, or a verb's person, tense or mood), with the evidence and a confidence 1 to 5.
4. Propose word classes for the frequent words (nouns, verbs, numerals, titles, and so on), and what role each slot of the main formula plays.

Write your answer as JSON to `{out}` (and repeat it in your final message):

{{"formulas": [{{"name": "...", "segments": [{{"form": "...", "role": "..."}}]}}],
  "morphemes": [{{"form": "...", "type": "suffix|prefix|clitic|word", "function": "...", "evidence": "...", "confidence": 1}}],
  "word_classes": [{{"form": "...", "class": "...", "note": "..."}}]}}

## Corpus

{corpus}
"""

if __name__ == "__main__":
    m = make_map(SEED)
    d = BLIND / "K_morph"
    d.mkdir(parents=True, exist_ok=True)
    (d / "task.md").write_text(TASK.format(out=d / "answer.json", corpus=corpus_block(load_corpus(), m)))
    print(d / "task.md", len((d / "task.md").read_text()))
