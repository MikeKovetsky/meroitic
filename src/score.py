"""Score the matching answers against the keys, with an exact p-value.

A meaning counts only if it is one of the task's options, compared on letters
alone (case, spaces and punctuation ignored); anything else is unmatched, so
wrong. The p-value is the exact chance of at least that many right if the key
dealt its meanings to its words at random, for the answer as given (one to one
or not).

  python3 src/score.py [--answers DIR]   DIR holds <run>.json (default: the blind folders)
"""
import argparse, collections, json, re
from math import comb, factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLIND = Path("/private/tmp/claude-501/blind")


def letters(s):
    return re.sub(r"[^a-z]", "", str(s or "").lower())


def option(meaning, options):
    """The option this meaning names, or None."""
    return {letters(o): o for o in options}.get(letters(meaning))


def level(confidence):
    try:
        return int(float(confidence))
    except (TypeError, ValueError):
        return 0


def p_at_least(answer, key, c):
    """Exact P(at least c right) over all one-to-one keys, for this answer (word -> option or None).

    Rook polynomial of the answer's cells: rooks[i] counts the ways to pick i
    answered words with distinct meanings, and inclusion-exclusion turns those
    into the number of keys that get exactly j of the answers right.
    """
    k = len(key)
    per_meaning = collections.Counter(m for w, m in answer.items() if w in key and m is not None)
    rooks = [1]
    for n in per_meaning.values():
        rooks = [a + n * b for a, b in zip(rooks + [0], [0] + rooks)]
    exactly = [sum((-1) ** (i - j) * comb(i, j) * rooks[i] * factorial(k - i) for i in range(j, len(rooks)))
               for j in range(len(rooks))]
    return sum(exactly[c:]) / factorial(k)


def score(run, key, path):
    if not path.exists():
        return None
    options = sorted(set(key.values()))
    if len({letters(o) for o in options}) < len(options):
        raise ValueError(f"{run}: two meanings differ only in case or punctuation")
    got, conf = {}, {}
    for a in json.load(open(path))["assignments"]:
        w = str(a.get("word", "")).strip()
        got[w] = option(a.get("meaning"), options)
        conf[w] = level(a.get("confidence"))
    right = [w for w in key if got.get(w) == key[w]]
    hi = [w for w in key if conf.get(w, 0) >= 4]
    return {"run": run, "k": len(key), "correct": len(right), "p": p_at_least(got, key, len(right)),
            "answered": sum(1 for w in key if w in got), "unmatched": sum(1 for w in key if w in got and got[w] is None),
            "confident": len(hi), "confident_correct": sum(1 for w in hi if w in right), "right_words": right}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", type=Path, help="folder of saved answers, <run>.json")
    a = ap.parse_args()
    keys = json.load(open(ROOT / "runs/keys/step0.json"))
    rows = [score(r, keys[r], a.answers / f"{r}.json" if a.answers else BLIND / r / "answer.json") for r in sorted(keys)]
    rows = [r for r in rows if r]
    json.dump(rows, open(ROOT / "runs/step0_scores.json", "w"), indent=1)
    for r in rows:
        print(f"{r['run']:7} {r['correct']:3}/{r['k']:<3} p={r['p']:.1e}  unmatched {r['unmatched']}  "
              f"confident {r['confident_correct']}/{r['confident']}")
