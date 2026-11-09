"""Restoration test: mask words in held-out texts and restore them.

100 funerary texts are held out; up to two words in each (not names or
numerals; often a grammatical word) are masked as [?1], [?2]. The solver sees
the other texts plus the masked ones. A baseline n-gram restorer (left/right
context with backoff) sets the bar; it counts what the solver sees, the other
texts and the masked ones with every mask unknown. This is the
skill Ithaca brought to Greek inscriptions; here it also measures how much an
LLM adds over plain statistics. Built from data/corpus_v2_c3_snapshot.jsonl,
corpus_v2 as it was when the C2_cloze run was made (the later cleanup changed
data/corpus_v2.jsonl).

  python3 src/cloze.py build
  python3 src/cloze.py baseline     # rewrite runs/cloze_ngram.json for the saved key
  python3 src/cloze.py [--key runs/keys/cloze.json] ANSWER.json ...
"""
import argparse, collections, json, random, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_tasks import BLIND, fresh   # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data/corpus_v2_c3_snapshot.jsonl"
SEED = 11
SKIP = {"NAME", "RNAME"}
UNKNOWN = "<mask>"


def load():
    return [json.loads(l) for l in open(CORPUS)]


def seen_contexts(train):
    seen = set()
    for r in train:
        t = ["<s>", "<s>"] + r["text"].split() + ["</s>", "</s>"]
        for i in range(2, len(t) - 2):
            seen.add((t[i - 1], t[i + 1]))
    return seen


def split(corpus, n_test=100):
    """Masks go only where the word's immediate left+right context never occurs
    in the reference texts, so copying a parallel line can't restore it."""
    rng = random.Random(SEED)
    fun = [r for r in corpus if r["src"] == "funerary" and len(r["text"].split()) >= 8]
    test = rng.sample(fun, n_test)
    ids = {r["id"] for r in test}
    train = [r for r in corpus if r["id"] not in ids]
    freq = collections.Counter(w for r in train for w in r["text"].split())
    seen = seen_contexts(train)
    items = []
    for r in test:
        t = r["text"].split()
        pad = ["<s>"] + t + ["</s>"]
        cand = [i for i, w in enumerate(t) if w not in SKIP and not w.isdigit() and freq[w] >= 2
                and (pad[i], pad[i + 2]) not in seen]
        for k, i in enumerate(sorted(rng.sample(cand, min(2, len(cand))))):
            items.append({"text": r["id"], "pos": i, "answer": t[i], "mask": f"[?{k + 1}]"})
    return train, test, items


def masked(test, items):
    by = collections.defaultdict(dict)
    for it in items:
        by[it["text"]][it["pos"]] = it["mask"]
    out = []
    for r in test:
        t = r["text"].split()
        out.append(f"{r['id']}: " + " ".join(by[r['id']].get(i, w) for i, w in enumerate(t)))
    return out


def contexts(t, i):
    """Context keys of position i in a padded sequence, most specific first."""
    return [("LR2", t[i - 2], t[i - 1], t[i + 1], t[i + 2]), ("LR", t[i - 1], t[i + 1]),
            ("L2", t[i - 2], t[i - 1]), ("R2", t[i + 1], t[i + 2]), ("L", t[i - 1]), ("R", t[i + 1]), ("U",)]


def shown(test, items):
    """The held-out texts as the solver sees them: every masked word is UNKNOWN."""
    hidden = {(it["text"], it["pos"]) for it in items}
    return {r["id"]: [UNKNOWN if (r["id"], j) in hidden else w for j, w in enumerate(r["text"].split())] for r in test}


def ngram_guess(train, items, test):
    """Three guesses per mask; counts come from what the solver sees: the reference texts and the masked ones."""
    seen = shown(test, items)
    ctx = collections.defaultdict(collections.Counter)
    for words in [r["text"].split() for r in train] + list(seen.values()):
        t = ["<s>", "<s>"] + words + ["</s>", "</s>"]
        for i in range(2, len(t) - 2):
            for k in contexts(t, i):
                if t[i] != UNKNOWN and UNKNOWN not in k:     # a mask is neither a word nor a context
                    ctx[k][t[i]] += 1
    guesses = {}
    for it in items:
        t = ["<s>", "<s>"] + seen[it["text"]] + ["</s>", "</s>"]
        votes = {}
        for rank, k in enumerate(contexts(t, it["pos"] + 2)):
            for w, c in ctx[k].most_common(5):
                votes.setdefault(w, (-rank, c))     # a more specific context always outranks a bigger count
        guesses[f"{it['text']}{it['mask']}"] = sorted(votes, key=votes.get, reverse=True)[:3]
    return guesses


TASK = """# Task: restore masked words in inscriptions

Below are ancient inscriptions in one language, transliterated into Latin letters (x and X are two h sounds, S an s sound, N a nasal; NAME and RNAME mask personal and royal names; digits are numerals). Part A is the reference corpus. Part B holds {n} further texts in which {m} words are masked as [?1] and [?2]. Each mask hides exactly one word (one space-separated token) that also occurs somewhere in Part A.

Restore every mask: give your three best guesses, best first. Use any pattern you can find. Work only from this file: do not use web search or fetch any page, and do not read any other file. You may run code (for example Python) that reads only this file.

Write JSON to `{out}` (and repeat it in your final message):

{{"guesses": {{"T0123[?1]": ["best", "second", "third"], ...}}}}

## Part B: texts to restore

{testblock}

## Part A: reference corpus

{trainblock}
"""


def task_text(train, test, items, d=BLIND / "C2_cloze"):
    trainblock = "\n".join(f"{r['id']}: {r['text']}" for r in train)
    return TASK.format(n=len(test), m=len(items), out=d / "answer.json",
                       testblock="\n".join(masked(test, items)), trainblock=trainblock)


def build():
    fresh(["C2_cloze"])
    corpus = load()
    train, test, items = split(corpus)
    d = BLIND / "C2_cloze"
    (d / "task.md").write_text(task_text(train, test, items, d))
    (ROOT / "runs/keys").mkdir(parents=True, exist_ok=True)
    json.dump({f"{it['text']}{it['mask']}": it["answer"] for it in items}, open(ROOT / "runs/keys/cloze.json", "w"), indent=1)
    json.dump(ngram_guess(train, items, test), open(ROOT / "runs/cloze_ngram.json", "w"), indent=1)
    print("masks", len(items), "task chars", len((d / "task.md").read_text()))


def baseline():
    """Rewrite the C2_cloze n-gram baseline; the rebuilt masks must be the saved key's."""
    train, test, items = split(load())
    if {f"{it['text']}{it['mask']}": it["answer"] for it in items} != json.load(open(ROOT / "runs/keys/cloze.json")):
        sys.exit("the rebuilt masks differ from runs/keys/cloze.json")
    json.dump(ngram_guess(train, items, test), open(ROOT / "runs/cloze_ngram.json", "w"), indent=1)


def guesses(path):
    """An answer's (or the baseline's) guesses by mask, each a list, best first."""
    g = json.load(open(path))
    g = g.get("guesses", g)
    return {k: [v] if isinstance(v, str) else list(v or []) for k, v in g.items()}


def score(path, key_path=ROOT / "runs/keys/cloze.json"):
    """Top-1 and top-3 hits, the number of masks, and how many masks the answer has no guess for."""
    key = json.load(open(key_path))
    g = guesses(path)
    top1 = sum(1 for k, a in key.items() if g.get(k, [])[:1] == [a])
    top3 = sum(1 for k, a in key.items() if a in g.get(k, [])[:3])
    return top1, top3, len(key), sum(1 for k in key if k not in g)


if __name__ == "__main__":
    if sys.argv[1:] == ["build"]:
        build()
    elif sys.argv[1:] == ["baseline"]:
        baseline()
    else:
        ap = argparse.ArgumentParser()
        ap.add_argument("answers", nargs="+")
        ap.add_argument("--key", default=ROOT / "runs/keys/cloze.json", help="runs/keys/cloze_v1.json for the C_cloze run")
        a = ap.parse_args()
        for p in a.answers:
            t1, t3, n, missing = score(p, a.key)
            note = f"  ({missing} masks have no guess: is this the right --key?)" if missing else ""
            print(f"{p}: top1 {t1}/{n} ({t1 / n:.0%}), top3 {t3}/{n} ({t3 / n:.0%}){note}")
