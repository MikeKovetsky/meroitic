"""Second pass: merge skeletons that differ only where a NAME slot holds a
multi-word name (a swap from Otten's list that contained spaces)."""
import collections, difflib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def name_only_diff(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        x, y = a[i1:i2], b[j1:j2]
        if op != "replace":
            return False
        if not ((x == ["NAME"] and len(y) <= 4) or (y == ["NAME"] and len(x) <= 4)):
            return False
    return True


def main():
    R = [json.loads(l) for l in open(ROOT / "data/texts.jsonl")]
    buckets = collections.defaultdict(list)
    for r in R:
        buckets[tuple(r["text"].split()[:4])].append(r)
    keep, merged = [], 0
    for rs in buckets.values():
        reps = []
        for r in sorted(rs, key=lambda r: -r["text"].count("NAME")):
            t = r["text"].split()
            for rep in reps:
                if abs(len(rep[0]) - len(t)) <= 6 and name_only_diff(rep[0], t):
                    rep[1]["copies"] += r["copies"]
                    merged += 1
                    break
            else:
                reps.append((t, r))
        keep += [r for _, r in reps]
    keep.sort(key=lambda r: r["id"])
    for i, r in enumerate(keep):
        r["id"] = f"T{i:04d}"
    with open(ROOT / "data/texts.jsonl", "w") as f:
        for r in keep:
            f.write(json.dumps(r) + "\n")
    words = [w for r in keep for w in r["text"].split()]
    print(f"merged {merged}; texts {len(keep)}; tokens {len(words)}; types {len(set(words))}")


if __name__ == "__main__":
    main()
