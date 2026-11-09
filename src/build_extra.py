"""Builders for the runs made after the first harness, so each is reproducible:

  F_recall   open recall of all 82 answer-key words, no options (runs/gold_v2.json)
  N_open     the 17 words recall missed, recovered from the corpus (runs/recall_rows.json)
  K2_morph   blind grammar on the scrambled corpus with neutral line ids
  YK_morph   blind grammar on the synthetic language

They read the corpus as it was when the runs were made
(data/corpus_v2_c3_snapshot.jsonl). `check` rebuilds every task in memory and
compares it with the task file the run actually used; `write NAME` writes a
task into a new folder and refuses to overwrite one that exists.
"""
import json, random, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_morph import TASK as MORPH_TASK   # noqa: E402
from scramble import make_map, text          # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BLIND = Path("/private/tmp/claude-501/blind")
SNAPSHOT = ROOT / "data/corpus_v2_c3_snapshot.jsonl"
# the words open recall could not give (or gave wrongly) that occur at least twice in the corpus
RECALL_MISSES = {"asr", "kdite", "mte", "tre-", "mkdi", "ar", "are-", "ḫlbi", "nse", "tbo", "yireqe", "kelw",
                 "ssor", "perite", "pẖrs", "tkk", "tebwe"}


def numbered(texts, width=100):
    lines = []
    for i, t in enumerate(texts):
        ws = t.split()
        for k in range(0, len(ws), width):
            tag = f"L{i:04d}" if len(ws) <= width else f"L{i:04d}.{k // width + 1}"
            lines.append(f"{tag}: {' '.join(ws[k:k + width])}")
    return lines


def f_recall(d):
    forms = [x["form"] for x in json.load(open(ROOT / "runs/gold_v2.json"))]
    random.Random(5).shuffle(forms)
    return f"""# Task: Meroitic vocabulary from memory

Below are {len(forms)} words of Meroitic, the language of ancient Kush (Sudan), in the standard scholarly transliteration (Hintze/Rilly: h and ẖ are written h and h with a line, ne/se/te/to are single signs).

For each word, write what it means, from your own knowledge only. If you do not know, write "unknown". Do not guess wildly: a confident wrong answer is worse than "unknown". Work only from this file and your memory: do not use web search or fetch any page, and do not read any other file.

Write JSON to `{d / 'answer.json'}` (and repeat it in your final message):

{{"answers": [{{"word": "...", "meaning": "... or unknown", "confidence": 1}}]}}

confidence is 1 (vague) to 5 (sure).

Words:
""" + "\n".join(f"- {w}" for w in forms) + "\n"


def n_open(d):
    rows = json.load(open(ROOT / "runs/recall_rows.json"))
    targets = [(r[3], r[1]) for r in rows if r[0] in RECALL_MISSES]
    given = [(r[3] or r[0], r[1]) for r in rows if r[0] not in RECALL_MISSES and r[3]]
    corpus = [json.loads(l) for l in open(SNAPSHOT)]
    rng = random.Random(3)
    rng.shuffle(corpus)
    lines = numbered([r["text"] for r in corpus])
    words = [t for t, _ in targets]
    rng.shuffle(words)
    return f"""# Task: work out what these Meroitic words mean, from the texts

Below is a corpus of Meroitic inscriptions (ancient Kush), one text per line (long texts split across numbered lines), in an ASCII transliteration: o for o, x and X for the two h signs, S for the s sign, N for the n-tilde sign. Person names are masked as NAME (royal names as RNAME). Digits are numerals.

The glossary gives words whose meanings are known. For each of the {len(words)} target words, propose what it means, from the evidence in the corpus: where it occurs, what it occurs with, its endings, the glossary words around it, parallel passages. Give your three best candidate meanings, best first, each a short English gloss, with the evidence for the first one and a confidence 1 to 5. If the texts give no basis, say so with confidence 1.

Work only from this file and your own reasoning: do not use web search or fetch any page, and do not read any other file. You may run code (for example Python) that reads only this file.

Write JSON to `{d / 'answer.json'}` (and repeat it in your final message):

{{"answers": [{{"word": "...", "candidates": ["best", "second", "third"], "confidence": 1, "evidence": "..."}}]}}

## Target words

""" + "\n".join(f"- {w}" for w in words) + """

## Glossary (known words)

""" + "\n".join(f"- {f}: {g}" for f, g in given) + """

## Corpus

""" + "\n".join(lines) + "\n"


def k2_morph(d):
    rows = [json.loads(l) for l in open(SNAPSHOT)]
    random.Random(99).shuffle(rows)
    m = make_map(7)
    return MORPH_TASK.format(out=d / "answer.json", corpus="\n".join(numbered([text(r["text"], m) for r in rows])))


def yk_morph(d):
    texts = [l for l in (ROOT / "data/synth_corpus.txt").read_text().split("\n") if l.strip()]
    random.Random(4).shuffle(texts)
    body = MORPH_TASK.format(out=d / "answer.json", corpus="\n".join(numbered(texts)))
    return body.replace("The script has been transliterated letter by letter into a substitute Latin alphabet.",
                        "The script has been transliterated letter by letter into a Latin alphabet. A dot marks a lost sign.")


BUILDERS = {"F_recall": f_recall, "N_open": n_open, "K2_morph": k2_morph, "YK_morph": yk_morph}


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        for name, fn in BUILDERS.items():
            used = BLIND / name / "task.md"
            same = used.exists() and fn(BLIND / name) == used.read_text()
            print(f"{name}: {'identical to the task the run used' if same else 'DIFFERS or missing'}")
    elif cmd == "write":
        name = sys.argv[2]
        d = BLIND / name
        if (d / "task.md").exists():
            sys.exit(f"{d} already holds a task; refusing to overwrite a run")
        d.mkdir(parents=True, exist_ok=True)
        (d / "task.md").write_text(BUILDERS[name](d))
        print("wrote", d / "task.md")
