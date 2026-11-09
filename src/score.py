"""Score the matching answers against the keys, with a permutation p-value."""
import difflib, json, random, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLIND = Path("/private/tmp/claude-501/blind")


def p_at_least(k, c, sims=200000, seed=1):
    rng, hits, idx = random.Random(seed), 0, list(range(k))
    for _ in range(sims):
        rng.shuffle(idx)
        hits += sum(i == j for i, j in enumerate(idx)) >= c
    return hits / sims


def closest(meaning, options):
    m = re.sub(r"[^a-z]", "", meaning.lower())
    return max(options, key=lambda o: difflib.SequenceMatcher(None, m, re.sub(r"[^a-z]", "", o)).ratio())


def score(run, keys):
    key = keys[run]
    f = BLIND / run / "answer.json"
    if not f.exists():
        return None
    ans = json.load(open(f))["assignments"]
    options = sorted(set(key.values()))
    got = {a["word"].strip(): closest(a["meaning"], options) for a in ans}
    conf = {a["word"]: a.get("confidence", 0) for a in ans}
    right = [w for w in key if got.get(w) == key[w]]
    hi = [w for w in key if conf.get(w, 0) >= 4]
    hi_right = [w for w in hi if w in right]
    return {"run": run, "k": len(key), "correct": len(right), "p": p_at_least(len(key), len(right)),
            "answered": len(got), "confident": len(hi), "confident_correct": len(hi_right),
            "right_words": right}


if __name__ == "__main__":
    keys = json.load(open(ROOT / "runs/keys/step0.json"))
    rows = [score(r, keys) for r in sorted(keys)]
    rows = [r for r in rows if r]
    json.dump(rows, open(ROOT / "runs/step0_scores.json", "w"), indent=1)
    for r in rows:
        print(f"{r['run']:7} {r['correct']:3}/{r['k']:<3} p={r['p']:.5f}  confident {r['confident_correct']}/{r['confident']}")
