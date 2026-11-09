"""Restoration v3: hold out whole families of near-duplicate texts.

The v1 and v2 restoration tests were won by copying: the model found the
corpus's leftover name-swap copies. Here texts join one family when half or
more of the shorter one's word trigrams also occur in the other (union-find),
60 small families (6 texts or fewer, funerary, a text of 8+ words) are held out
whole, and two words are masked in one text of each. Nothing in Part B has a
copy in Part A. Built from data/corpus_v2_c3_snapshot.jsonl, the corpus as it
was when the run was made.

  python3 src/cloze_families.py baseline        # keys + n-gram baseline
  python3 src/cloze_families.py task             # also the blind task (new folder only)
  python3 src/cloze_families.py score FILE ...   # top-1 / top-3 against the key
  python3 src/cloze_families.py copies FILE NGRAM # the same, split into re-split copies and new texts

Trigram families miss copies that scribes or editors split into words
differently, so `copies` also counts a held-out text as a copy when 80% or
more of its letters (spaces removed) occur in Part A as runs of 12+ letters.
"""
import collections, json, random, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cloze import TASK as _TASK, ngram_guess   # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "data/corpus_v2_c3_snapshot.jsonl"
BLIND = Path("/private/tmp/claude-501/blind/C3_cloze")
KEY = ROOT / "runs/keys/cloze_families.json"
SEED = 23
SKIP = {"NAME", "RNAME"}
TASK = _TASK.replace("that also occurs somewhere in Part A.",
                     "that also occurs somewhere in Part A. No Part B text has a copy or near-copy in Part A.")


def trigrams(t):
    return {tuple(t[i:i + 3]) for i in range(len(t) - 2)} or {tuple(t)}


def families(rows):
    grams = [trigrams(r["text"].split()) for r in rows]
    parent = list(range(len(rows)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    index = collections.defaultdict(set)
    for i, g in enumerate(grams):
        for x in g:
            index[x].add(i)
    for i, g in enumerate(grams):
        shared = collections.Counter(j for x in g for j in index[x] if j != i)
        for j, n in shared.items():
            if n / max(1, min(len(g), len(grams[j]))) >= 0.5:
                a, b = find(i), find(j)
                if a != b:
                    parent[max(a, b)] = min(a, b)
    fam = collections.defaultdict(list)
    for i in range(len(rows)):
        fam[find(i)].append(i)
    return list(fam.values())


def split(rows):
    fams = families(rows)
    rng = random.Random(SEED)
    small = [f for f in fams if all(rows[i]["src"] == "funerary" for i in f)
             and max(len(rows[i]["text"].split()) for i in f) >= 8 and len(f) <= 6]
    held = rng.sample(small, min(60, len(small)))
    held_ids = {i for f in held for i in f}
    train = [rows[i] for i in range(len(rows)) if i not in held_ids]
    test = [rows[max(f, key=lambda i: len(rows[i]["text"].split()))] for f in held]
    freq = collections.Counter(w for r in train for w in r["text"].split())
    items, test_rows, lines = [], [], []
    for n, r in enumerate(test):
        bid = f"B{n + 1:03d}"
        t = r["text"].split()
        test_rows.append({"id": bid, "text": r["text"]})
        cand = [i for i, w in enumerate(t) if w not in SKIP and not w.isdigit() and freq[w] >= 2]
        masks = {p: f"[?{k + 1}]" for k, p in enumerate(sorted(rng.sample(cand, min(2, len(cand)))))}
        for p, mk in masks.items():
            items.append({"text": bid, "pos": p, "answer": t[p], "mask": mk, "src_id": r["id"]})
        lines.append(f"{bid}: " + " ".join(masks.get(i, w) for i, w in enumerate(t)))
    rng.shuffle(train)
    return fams, small, train, test_rows, items, lines


def build(write_task):
    rows = [json.loads(l) for l in open(SNAPSHOT)]
    fams, small, train, test_rows, items, lines = split(rows)
    KEY.parent.mkdir(parents=True, exist_ok=True)
    json.dump({f"{it['text']}{it['mask']}": it["answer"] for it in items}, open(KEY, "w"), indent=1)
    json.dump(ngram_guess(train, items, test_rows), open(ROOT / "runs/cloze_families_ngram.json", "w"), indent=1)
    if write_task:
        if (BLIND / "task.md").exists():
            sys.exit(f"{BLIND} already holds a task; refusing to overwrite a run")
        BLIND.mkdir(parents=True, exist_ok=True)
        trainblock = "\n".join(f"A{i + 1:04d}: {r['text']}" for i, r in enumerate(train))
        (BLIND / "task.md").write_text(TASK.format(n=len(test_rows), m=len(items), out=BLIND / "answer.json",
                                                   testblock="\n".join(lines), trainblock=trainblock)
                                       .replace('"T0123[?1]"', '"B001[?1]"'))
    print(f"families {len(fams)}; small funerary {len(small)}; held {len(test_rows)}; "
          f"train {len(train)}; masks {len(items)}")
    return lines


def coverage(text, blob, run=12):
    """Share of the text's letters (spaces removed) found in blob as runs of `run`+ letters."""
    s, i, cov = text.replace(" ", ""), 0, 0
    while i < len(s):
        n = run
        if i + n <= len(s) and s[i:i + n] in blob:
            while i + n < len(s) and s[i:i + n + 1] in blob:
                n += 1
            cov, i = cov + n, i + n
        else:
            i += 1
    return cov / max(1, len(s))


def copies(answer_path, ngram_path):
    rows = [json.loads(l) for l in open(SNAPSHOT)]
    _, _, train, test_rows, _, _ = split(rows)
    blob = "\n".join(r["text"].replace(" ", "") for r in train)
    copy = {r["id"] for r in test_rows if coverage(r["text"], blob) >= 0.8}
    key = json.load(open(KEY))

    def first(path):
        g = json.load(open(path))
        g = g.get("guesses", g)
        return {k: ([v] if isinstance(v, str) else list(v or []))[:1] for k, v in g.items()}
    ans, ngr = first(answer_path), first(ngram_path)
    print(f"re-split copies: {len(copy)} of {len(test_rows)} held-out texts")
    for name, keep in [("copies", lambda b: b in copy), ("new texts", lambda b: b not in copy)]:
        ks = [k for k in key if keep(k.split("[")[0])]
        hit = lambda g: sum(1 for k in ks if g.get(k) == [key[k]])
        print(f"  {name}: {len(ks)} masks; answer {hit(ans)}, n-gram {hit(ngr)}")


def score(path):
    key = json.load(open(KEY))
    g = json.load(open(path))
    g = g.get("guesses", g)

    def ranked(k):
        v = g.get(k, [])
        return [v] if isinstance(v, str) else list(v)
    t1 = sum(1 for k, a in key.items() if ranked(k)[:1] == [a])
    t3 = sum(1 for k, a in key.items() if a in ranked(k)[:3])
    print(f"{path}: top1 {t1}/{len(key)} ({t1 / len(key):.0%}), top3 {t3}/{len(key)} ({t3 / len(key):.0%})")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "baseline"
    if cmd == "score":
        for p in sys.argv[2:]:
            score(p)
    elif cmd == "copies":
        copies(sys.argv[2], sys.argv[3])
    else:
        build(write_task=(cmd == "task"))
