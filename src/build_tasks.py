"""Build the blind matching tasks for the Step 0 test.

Conditions (same folds, same instructions):
  R   real spelling, corpus given
  S   scrambled spelling, corpus given (the test that matters)
  S0  scrambled spelling, no corpus (chance with word-shape cues)
  M   real spelling, no corpus, told the language is Meroitic (memory only)
Each task: a glossary of the other fold's words, then K test words and the K
meanings shuffled; the solver assigns them one to one.
Blind task folders go outside the repo; answer keys stay in runs/keys/.
Corpus lines are tagged L0000, L0001, ... in corpus order, never with the
corpus ids, which name the royal inscriptions (hamadab, tanyidamani, ...).
A folder that already holds a task is never rebuilt: its answers are scored
against the keys saved with it.
"""
import collections, json, random, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from corpus import norm            # noqa: E402
from scramble import make_map, text, word   # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BLIND = Path("/private/tmp/claude-501/blind")
PROPER = {"deity", "place", "people"}
# grammatical words that would make a test item ambiguous
FUNCTION = {"wi", "l", "li", "lo", "s", "se", "te", "qo", "qe", "ye", "yi", "k", "e", "a", "o", "i", "t", "lw", "leb"}
SEED = 7


def load_corpus():
    return [json.loads(l) for l in open(ROOT / "data/corpus.jsonl")]


def fresh(runs):
    """Create the runs' blind folders; exit, writing nothing, if any already holds a task."""
    taken = [r for r in runs if (BLIND / r / "task.md").exists()]
    if taken:
        sys.exit(f"{BLIND} already holds {', '.join(taken)}: their answers are scored against the saved keys. "
                 "Move those folders (and their keys) away to rebuild.")
    for r in runs:
        (BLIND / r).mkdir(parents=True, exist_ok=True)


def save_keys(keys):
    """Add these runs' keys to runs/keys/step0.json, keeping every other run's."""
    p = ROOT / "runs/keys/step0.json"
    old = json.load(open(p)) if p.exists() else {}
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({**old, **keys}, indent=1))


def eligible(corpus, min_freq):
    freq = collections.Counter(w for r in corpus for w in r["text"].split())
    gold = json.load(open(ROOT / "data/gold_lexicon.json"))
    items, seen_gloss, seen_form = [], set(), set()
    for g in gold:
        if g.get("category") in PROPER or g.get("confidence") == "debated":
            continue
        forms = [g.get("corpus_form") or g["form"]] + list(g.get("corpus_variants") or [])
        forms = [norm(f) for f in forms if f]
        forms = [f for f in forms if len(f) >= 2 and f not in FUNCTION]
        if not forms:
            continue
        best = max(forms, key=lambda f: freq[f])
        gloss = g["gloss"].strip().lower()
        if freq[best] < min_freq or gloss in seen_gloss or best in seen_form:
            continue
        seen_gloss.add(gloss)
        seen_form.add(best)
        items.append({"form": best, "gloss": gloss, "freq": freq[best], "category": g.get("category")})
    return items


def corpus_block(corpus, m=None, width=100):
    out = []
    for n, r in enumerate(corpus):
        ws = (r["text"] if m is None else text(r["text"], m)).split()
        for k in range(0, len(ws), width):
            tag = f"L{n:04d}" if len(ws) <= width else f"L{n:04d}.{k // width + 1}"
            out.append(f"{tag}: {' '.join(ws[k:k + width])}")
    return "\n".join(out)


HEAD = """# Task: match words to meanings

You are given {what}. {spelling}

Work only from what is written in this file. Do not use web search or fetch any page, and do not read any other file. You may run code (for example Python) that reads only this file, to count and compare forms.

## Known words (glossary)

These words' meanings are known:

{glossary}

## The test

Below are {k} words{fromcorpus} and {k} meanings. Each word has exactly one of these meanings, and each meaning belongs to exactly one word. Assign every word a meaning, one to one. Use any evidence you can find{evidence}.

Words:
{words}

Meanings (shuffled):
{meanings}

## Answer

Write your answer as JSON to `{out}` (and also put the same JSON in your final message), in this shape:

{{"assignments": [{{"word": "...", "meaning": "...", "confidence": 1, "evidence": "one line"}}]}}

confidence is 1 (guess) to 5 (sure). Every word once, every meaning once.
"""
CONDITIONS = ["R", "S", "S0", "M"]


def build(min_freq=2, folds=2):
    fresh([f"{c}_f{f}" for f in range(folds) for c in CONDITIONS])
    corpus = load_corpus()
    items = eligible(corpus, min_freq)
    random.Random(SEED).shuffle(items)
    m = make_map(SEED)
    keys = {}
    for f in range(folds):
        test = items[f::folds]
        given = [it for i, it in enumerate(items) if i % folds != f]
        meanings = [t["gloss"] for t in test]
        random.Random(SEED + f).shuffle(meanings)
        for cond in CONDITIONS:
            scr = cond.startswith("S")
            sp = (lambda w: word(w, m)) if scr else (lambda w: w)
            run = f"{cond}_f{f}"
            d = BLIND / run
            if cond == "M":
                what = "words from the Meroitic language of ancient Kush (Sudan), in an ASCII transliteration (x and X are the two h signs, S is the s sign, N is the n-tilde sign)"
                spelling = "No corpus is provided: answer from what you know."
            elif cond == "S0":
                what = "words from an ancient language, written in a substitute Latin alphabet"
                spelling = "No texts are provided: only the words themselves."
            else:
                what = "a corpus of ancient inscriptions in one language, one text per line (long texts are split across numbered lines)"
                spelling = ("The script has been transliterated letter by letter into a Latin alphabet. Spaces mark word boundaries. "
                            "NAME stands for a personal name and RNAME for a royal name (the names were masked). Digits are numerals.")
                if scr:
                    spelling = spelling.replace("into a Latin alphabet", "into a substitute Latin alphabet")
            gl = "\n".join(f"- {sp(g['form'])}: {g['gloss']}" for g in given)
            body = HEAD.format(
                what=what, spelling=spelling, glossary=gl, k=len(test),
                fromcorpus=" from the corpus" if cond in ("R", "S") else "",
                evidence=" in the corpus: where each word occurs, what it occurs with, its affixes, the glossary words around it" if cond in ("R", "S") else "",
                words="\n".join(f"- {sp(t['form'])}" for t in test),
                meanings="\n".join(f"- {x}" for x in meanings),
                out=d / "answer.json")
            if cond in ("R", "S"):
                body += "\n## Corpus\n\n" + corpus_block(corpus, m if scr else None) + "\n"
            (d / "task.md").write_text(body)
            keys[run] = {sp(t["form"]): t["gloss"] for t in test}
    save_keys(keys)
    json.dump(m, open(ROOT / "runs/keys/scramble_map.json", "w"))
    json.dump(items, open(ROOT / "runs/keys/items.json", "w"), indent=1)
    print(f"eligible {len(items)}; per fold {[len(items[f::folds]) for f in range(folds)]}")
    for p in sorted(BLIND.glob("*/task.md")):
        print(p, len(p.read_text()))


if __name__ == "__main__":
    build(int(sys.argv[1]) if len(sys.argv) > 1 else 2)
