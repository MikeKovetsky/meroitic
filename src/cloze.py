"""Restoration test: mask words in held-out texts and restore them.

100 funerary texts are held out; two content words in each are masked as [?1],
[?2]. The solver sees the other texts plus the masked ones. A baseline n-gram
restorer (left/right context with backoff) trained on the same other texts sets
the bar. This is the skill Ithaca brought to Greek inscriptions; here it also
measures how much an LLM adds over plain statistics.
"""
import collections, json, random, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLIND = Path("/private/tmp/claude-501/blind")
SEED = 11
SKIP = {"NAME", "RNAME"}


def load():
    return [json.loads(l) for l in open(ROOT / "data/corpus.jsonl")]


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


def ngram_guess(train, items, test):
    ctx = collections.defaultdict(collections.Counter)
    for r in train:
        t = ["<s>", "<s>"] + r["text"].split() + ["</s>", "</s>"]
        for i in range(2, len(t) - 2):
            w = t[i]
            ctx[("LR2", t[i - 2], t[i - 1], t[i + 1], t[i + 2])][w] += 1
            ctx[("LR", t[i - 1], t[i + 1])][w] += 1
            ctx[("L2", t[i - 2], t[i - 1])][w] += 1
            ctx[("R2", t[i + 1], t[i + 2])][w] += 1
            ctx[("L", t[i - 1])][w] += 1
            ctx[("R", t[i + 1])][w] += 1
            ctx[("U",)][w] += 1
    texts = {r["id"]: r["text"].split() for r in test}
    guesses = {}
    for it in items:
        t = ["<s>", "<s>"] + texts[it["text"]] + ["</s>", "</s>"]
        i = it["pos"] + 2
        keys = [("LR2", t[i - 2], t[i - 1], t[i + 1], t[i + 2]), ("LR", t[i - 1], t[i + 1]),
                ("L2", t[i - 2], t[i - 1]), ("R2", t[i + 1], t[i + 2]), ("L", t[i - 1]), ("R", t[i + 1]), ("U",)]
        votes = collections.Counter()
        for rank, k in enumerate(keys):
            for w, c in ctx[k].most_common(5):
                if w not in votes:
                    votes[w] = (len(keys) - rank) * 1000 + c
        guesses[f"{it['text']}{it['mask']}"] = [w for w, _ in votes.most_common(3)]
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


def build():
    corpus = load()
    train, test, items = split(corpus)
    d = BLIND / "C_cloze"
    d.mkdir(parents=True, exist_ok=True)
    trainblock = "\n".join(f"{r['id']}: {r['text']}" for r in train)
    (d / "task.md").write_text(TASK.format(n=len(test), m=len(items), out=d / "answer.json",
                                           testblock="\n".join(masked(test, items)), trainblock=trainblock))
    (ROOT / "runs/keys").mkdir(parents=True, exist_ok=True)
    json.dump({f"{it['text']}{it['mask']}": it["answer"] for it in items}, open(ROOT / "runs/keys/cloze.json", "w"), indent=1)
    json.dump(ngram_guess(train, items, test), open(ROOT / "runs/cloze_ngram.json", "w"), indent=1)
    print("masks", len(items), "task chars", len((d / "task.md").read_text()))


def score(path):
    key = json.load(open(ROOT / "runs/keys/cloze.json"))
    g = json.load(open(path))
    g = g.get("guesses", g)
    top1 = sum(1 for k, a in key.items() if g.get(k, [None])[:1] == [a])
    top3 = sum(1 for k, a in key.items() if a in g.get(k, [])[:3])
    return top1, top3, len(key)


if __name__ == "__main__":
    if sys.argv[1:] == ["build"]:
        build()
    else:
        for p in sys.argv[1:]:
            t1, t3, n = score(p)
            print(f"{p}: top1 {t1}/{n} ({t1 / n:.0%}), top3 {t3}/{n} ({t3 / n:.0%})")
