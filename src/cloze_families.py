"""Restoration v3: hold out whole families of near-duplicate texts.

The v1 and v2 restoration tests were won by copying: the model found the
corpus's leftover name-swap copies. Here texts join one family when half or
more of the shorter one's word trigrams also occur in the other (union-find),
60 small families (6 texts or fewer, funerary, a text of 8+ words) are held out
whole, and two words are masked in the longest text of each. Built from
data/corpus_v2_c3_snapshot.jsonl, the corpus as it was when the run was made.

No Part B text shares half its word trigrams with a Part A text, but trigram
families miss copies with other word breaks or another letter for a sign:
T0825 (B052) is part of REM 1003, which is in Part A. So `copies` splits the
masks instead: a mask has a parallel when its word sits inside a run of 12 or
more letters, spaces and case ignored, that reaches past the word and also
occurs in what the solver reads (Part A, or Part B with its masks hidden), so
the answer could be copied from there. (The task told the solver no Part B text
had a copy; that sentence stays, as the run saw it.)

  python3 src/cloze_families.py baseline         # check key and task against the saved ones; rewrite the n-gram baseline
  python3 src/cloze_families.py task             # also write the blind task (new folder only)
  python3 src/cloze_families.py score FILE ...   # top-1 / top-3 against the key
  python3 src/cloze_families.py copies FILE NGRAM  # masks with and without a parallel, exact McNemar p
"""
import collections, json, math, random, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cloze   # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "data/corpus_v2_c3_snapshot.jsonl"
BLIND = Path("/private/tmp/claude-501/blind/C3_cloze")
SAVED_TASK = ROOT / "runs/tasks/C3_cloze.md"
KEY = ROOT / "runs/keys/cloze_families.json"
NGRAM = ROOT / "runs/cloze_families_ngram.json"
COPIES = ROOT / "runs/cloze_families_copies.json"
SEED = 23
SPAN = 12          # letters: the shortest stretch that counts as a parallel


def edited(text, edits):
    for old, new in edits:
        if old not in text:
            raise ValueError(f"cloze.TASK no longer says {old!r}")
        text = text.replace(old, new)
    return text


# the C2 instructions with the edits the C3 run's task carried, word for word
TASK = edited(cloze.TASK, [
    ("that also occurs somewhere in Part A.",
     "that also occurs somewhere in Part A. No Part B text has a copy or near-copy in Part A."),
    ("Use any pattern you can find.", "Use any pattern you can find, including what you know about the language."),
    ("(and repeat it in your final message)", "(and repeat a short summary in your final message)"),
    ('"T0123[?1]"', '"B001[?1]"')])


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
    items, test_rows = [], []
    for n, r in enumerate(test):
        bid = f"B{n + 1:03d}"
        t = r["text"].split()
        test_rows.append({"id": bid, "text": r["text"]})
        cand = [i for i, w in enumerate(t) if w not in cloze.SKIP and not w.isdigit() and freq[w] >= 2]
        for k, p in enumerate(sorted(rng.sample(cand, min(2, len(cand))))):
            items.append({"text": bid, "pos": p, "answer": t[p], "mask": f"[?{k + 1}]", "src_id": r["id"]})
    rng.shuffle(train)
    return fams, small, train, test_rows, items


def task_text(train, test_rows, items):
    trainblock = "\n".join(f"A{i + 1:04d}: {r['text']}" for i, r in enumerate(train))
    return TASK.format(n=len(test_rows), m=len(items), out=BLIND / "answer.json",
                       testblock="\n".join(cloze.masked(test_rows, items)), trainblock=trainblock)


def keep(path, data):
    """Write a run's key if it is missing; if it exists, the rebuild must match it (the run is scored against it)."""
    if path.exists():
        if json.load(open(path)) != data:
            sys.exit(f"{path} differs from the rebuild; refusing to overwrite what the run is scored against")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    json.dump(data, open(path, "w"), indent=1)


def build(write_task):
    rows = [json.loads(l) for l in open(SNAPSHOT)]
    fams, small, train, test_rows, items = split(rows)
    task = task_text(train, test_rows, items)
    saved = [p for p in (SAVED_TASK, BLIND / "task.md") if p.exists()]
    if write_task and saved:
        sys.exit(f"{saved[0]} holds the run's task; refusing to overwrite a run")
    if any(p.read_text() != task for p in saved):
        sys.exit("the rebuilt task differs from the one the run used")
    keep(KEY, {f"{it['text']}{it['mask']}": it["answer"] for it in items})
    json.dump(cloze.ngram_guess(train, items, test_rows), open(NGRAM, "w"), indent=1)
    if write_task:
        for p in (BLIND / "task.md", SAVED_TASK):
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(task)
    print(f"families {len(fams)}; small funerary {len(small)}; held {len(test_rows)}; train {len(train)}; "
          f"masks {len(items)}; task {'written' if write_task else 'as the run used' if saved else 'not saved'}; "
          f"key as saved; baseline written")


def parallel(words, pos, blob, span=SPAN):
    """Whether the word at pos can be copied from a parallel: some stretch of `span`+ letters of the text
    (spaces and case ignored) holds the whole word, reaches past it, and occurs in blob (see visible())."""
    ws = [w.lower() for w in words]
    s = "".join(ws)
    start = sum(len(w) for w in ws[:pos])
    end = start + len(ws[pos])
    for a in range(start + 1):
        b = max(a + span, end + (a == start))     # a substring of a match matches, so the shortest stretch decides
        if b <= len(s) and s[a:b] in blob:
            return True
    return False


def mcnemar(b, c):
    """Exact two-sided McNemar p from the discordant pairs: b masks only one side got, c only the other."""
    n = b + c
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n)


def visible(train, test_rows, items):
    """Everything the solver reads, lower-cased with spaces removed, one text per line, a mask as '#'."""
    seen = [r["text"].split() for r in train] + list(cloze.shown(test_rows, items).values())
    return "\n".join("".join("#" if w == cloze.UNKNOWN else w for w in t).lower() for t in seen)


def parallels():
    """For each mask key, whether its word has a parallel in what the solver reads (see parallel())."""
    rows = [json.loads(l) for l in open(SNAPSHOT)]
    _, _, train, test_rows, items = split(rows)
    blob = visible(train, test_rows, items)
    words = {r["id"]: r["text"].split() for r in test_rows}
    return {f"{it['text']}{it['mask']}": parallel(words[it["text"]], it["pos"], blob) for it in items}


def split_scores(par, answer_path, ngram_path):
    """(group, masks, answer top-1, n-gram top-1, exact McNemar p) for all masks, with and without a parallel."""
    key = json.load(open(KEY))
    if set(key) != set(par):
        sys.exit(f"{KEY} does not match the rebuilt masks")
    ans, ngr = cloze.guesses(answer_path), cloze.guesses(ngram_path)
    out = []
    for name, ks in [("all masks", list(key)), ("with a parallel", [k for k in key if par[k]]),
                     ("no parallel", [k for k in key if not par[k]])]:
        a = {k for k in ks if ans.get(k, [])[:1] == [key[k]]}
        n = {k for k in ks if ngr.get(k, [])[:1] == [key[k]]}
        out.append((name, len(ks), len(a), len(n), mcnemar(len(a - n), len(n - a))))
    return out


def copies(answer_path, ngram_path):
    par = parallels()
    json.dump({"rule": f"a parallel: a run of {SPAN}+ letters of the held-out text, spaces and case ignored, "
                       "that holds the whole masked word, reaches past it, and also occurs in what the solver reads "
                       "(Part A, or Part B with its masks hidden)",
               "with_parallel": sorted(k for k in par if par[k]), "no_parallel": sorted(k for k in par if not par[k])},
              open(COPIES, "w"), indent=1)
    for name, n, a, ng, p in split_scores(par, answer_path, ngram_path):
        print(f"  {name}: {n}; answer {a}, n-gram {ng}; exact McNemar p {p:.1e}")


def score(path):
    t1, t3, n, missing = cloze.score(path, KEY)
    note = f"; {missing} masks have no guess" if missing else ""
    print(f"{path}: top1 {t1}/{n} ({t1 / n:.0%}), top3 {t3}/{n} ({t3 / n:.0%}){note}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "baseline"
    if cmd == "score":
        for p in sys.argv[2:]:
            score(p)
    elif cmd == "copies":
        copies(sys.argv[2], sys.argv[3])
    elif cmd in ("baseline", "task"):
        build(write_task=(cmd == "task"))
    else:
        sys.exit(__doc__)
